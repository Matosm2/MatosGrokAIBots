"""CLI: python -m backtest.jewel_replay csv1 [csv2 ...] [--window 6m|all|both]"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from backtest.jewel_replay.csv_loader import load_jewel_csv
from backtest.jewel_replay.engine import run_replay
from backtest.jewel_replay.prepare import prepare_closed_sample
from backtest.jewel_replay.report import (
    MODE_A_PCT,
    MODE_B_PCT,
    DualModeRow,
    summarize,
    write_dual_gate_markdown,
    write_replay_markdown,
)
from backtest.jewel_replay.signals import JewelParams, Variant
from backtest.jewel_replay.window import WindowMode, apply_window, resolve_windows


def infer_symbol(path: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    name = path.stem.lower()
    if "btc" in name:
        return "BTCUSDT"
    if "eth" in name:
        return "ETHUSDT"
    # fallback: uppercase stem fragment
    m = re.search(r"([a-z]{3,10})usdt", name)
    if m:
        return m.group(0).upper()
    return path.stem.upper()[:12] or "UNKNOWN"


def run_dual_for_bars(
    *,
    symbol: str,
    bars,
    variant: Variant,
    initial: float,
    fee: float,
    slippage: float,
) -> tuple:
    params = JewelParams(variant=variant)
    mode_a = run_replay(
        symbol,
        bars,
        params=params,
        initial_equity=initial,
        buy_qty_pct=MODE_A_PCT,
        fee_rate=fee,
        slippage_rate=slippage,
    )
    mode_b = run_replay(
        symbol,
        bars,
        params=params,
        initial_equity=initial,
        buy_qty_pct=MODE_B_PCT,
        fee_rate=fee,
        slippage_rate=slippage,
    )
    return mode_a, mode_b


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Path B replay: jewel-strength-hold-v1 dual sizing "
            f"(Mode A {MODE_A_PCT:g}% gate / Mode B {MODE_B_PCT:g}% ops) + window tables"
        )
    )
    p.add_argument(
        "csv",
        type=Path,
        nargs="+",
        help="One or more CSVs with time,OHLCV,Slow,High/jewel_high",
    )
    p.add_argument(
        "--symbol",
        default=None,
        help="Override symbol for all CSVs (default: infer from filename)",
    )
    p.add_argument("--initial", type=float, default=10_000.0)
    p.add_argument(
        "--buy-qty-pct",
        type=float,
        default=None,
        help=(
            "If set, run legacy single-sizing report only (skips dual Mode A/B). "
            f"Default dual: Mode A={MODE_A_PCT:g}, Mode B={MODE_B_PCT:g}."
        ),
    )
    p.add_argument("--fee", type=float, default=0.001, help="0.001 = 0.10%/side")
    p.add_argument("--slippage", type=float, default=0.0005, help="5 bps default")
    p.add_argument(
        "--window",
        choices=[m.value for m in WindowMode],
        default=WindowMode.BOTH.value,
        help="Report window: all | 6m | both (default both)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Markdown report path (default under jewel_replay/results/)",
    )
    p.add_argument(
        "--waiting-real-csvs",
        action="store_true",
        help="Annotate report that real BTC/ETH Jewel CSVs are still pending",
    )
    p.add_argument(
        "--no-prep",
        action="store_true",
        help="Skip closed-bar prep (drop open last + 2017-12-31 sample start)",
    )
    args = p.parse_args(argv)

    missing = [c for c in args.csv if not c.is_file()]
    if missing:
        for c in missing:
            print(f"ERROR: CSV not found: {c}", file=sys.stderr)
        return 1

    windows = resolve_windows(args.window)
    dual_rows: list[DualModeRow] = []
    legacy_results = []
    all_prep_notes: list[str] = []

    for csv_path in args.csv:
        bars_raw = load_jewel_csv(csv_path)
        if args.no_prep:
            bars_full = bars_raw
            prep_notes: list[str] = ["Prep skipped (--no-prep)."]
        else:
            bars_full, prep_notes = prepare_closed_sample(bars_raw)
        for note in prep_notes:
            tagged = f"{csv_path.name}: {note}"
            if tagged not in all_prep_notes:
                all_prep_notes.append(tagged)
            print(f"PREP {tagged}", flush=True)
        symbol = infer_symbol(csv_path, args.symbol)
        for wlabel, wkind in windows:
            bars = apply_window(bars_full, wkind)
            if not bars:
                print(
                    f"WARN: {symbol} window={wlabel}: no bars after filter",
                    file=sys.stderr,
                )
                continue
            for variant in (Variant.V_ZONE, Variant.V_WIDE):
                if args.buy_qty_pct is not None:
                    params = JewelParams(variant=variant)
                    r = run_replay(
                        symbol,
                        bars,
                        params=params,
                        initial_equity=args.initial,
                        buy_qty_pct=args.buy_qty_pct,
                        fee_rate=args.fee,
                        slippage_rate=args.slippage,
                    )
                    m = summarize(r)
                    legacy_results.append(r)
                    print(
                        f"{symbol} {variant.value} [{wlabel}] size={args.buy_qty_pct:g}%: "
                        f"trades={m['trades']} wr={m['win_rate_display']} "
                        f"ret_mtm={float(m['return_pct']):+.2f}% "
                        f"closed={float(m['closed_return_pct']):+.2f}% "
                        f"bh={float(m['buy_hold_return_pct']):+.2f}% "
                        f"gate={'PASS' if m['gate_pass'] else 'FAIL'}",
                        flush=True,
                    )
                else:
                    mode_a, mode_b = run_dual_for_bars(
                        symbol=symbol,
                        bars=bars,
                        variant=variant,
                        initial=args.initial,
                        fee=args.fee,
                        slippage=args.slippage,
                    )
                    row = DualModeRow(
                        symbol=symbol,
                        variant=variant.value,
                        window_label=wlabel,
                        mode_a=mode_a,
                        mode_b=mode_b,
                        source_csv=str(csv_path),
                        prep_notes=prep_notes,
                    )
                    dual_rows.append(row)
                    sm = row.summarize()
                    print(
                        f"{symbol} {variant.value} [{wlabel}]: "
                        f"n={sm['trades']} wr={sm['win_rate_display']} "
                        f"A_mtm={float(sm['mode_a_return_pct']):+.2f}% "
                        f"A_closed={float(sm['mode_a_closed_return_pct']):+.2f}% "
                        f"B(ops)={float(sm['mode_b_return_pct']):+.2f}% "
                        f"bh={float(sm['buy_hold_return_pct']):+.2f}% "
                        f"A/BH={sm['mode_a_bh_ratio']} "
                        f"open={'Y' if sm['mode_a_open_long'] else 'N'} "
                        f"gate={sm['gate_label']}",
                        flush=True,
                    )

    results_dir = Path(__file__).resolve().parent / "results"
    if args.buy_qty_pct is not None:
        out = args.out or (results_dir / "jewel-strength-hold-v1.md")
        src = ", ".join(str(c) for c in args.csv)
        write_replay_markdown(results=legacy_results, path=out, source_csv=src)
    else:
        out = args.out or (results_dir / "jewel-pathb-dual-gate.md")
        write_dual_gate_markdown(
            rows=dual_rows,
            path=out,
            sources=[str(c) for c in args.csv],
            waiting_for_real_csvs=args.waiting_real_csvs,
            prep_notes=all_prep_notes,
        )
    print(f"Wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
