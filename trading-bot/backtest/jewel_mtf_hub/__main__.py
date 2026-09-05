"""CLI: python -m backtest.jewel_mtf_hub [--symbol BTCUSDT] [--refresh]

Runs M1–M4 open-proxy matrix with dual sizing; writes results markdown.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import load_or_fetch
from backtest.jewel_mtf_hub.engine import run_dual_modes
from backtest.jewel_mtf_hub.report import summarize, write_report
from backtest.jewel_mtf_hub.signals import build_all_signals

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESEARCH_ID = "jewel-mtf-hub-regime-v1"


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc).timestamp() * 1000
    return int(now - months * 30.4375 * 24 * 3600 * 1000)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=f"{RESEARCH_ID} open-proxy edition — M1–M4 backtest"
    )
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--years", type=float, default=3.0, help="Fetch lookback years")
    p.add_argument("--months-6m", type=float, default=6.0)
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--initial", type=float, default=10_000.0)
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Markdown path (default results/…-open-proxy.md)",
    )
    args = p.parse_args(argv)

    symbol = args.symbol.upper()
    print(f"[{RESEARCH_ID}] Loading {symbol} 1d+4h (~{args.years:g}y)...", flush=True)
    daily = load_or_fetch(symbol, "1d", years=args.years, refresh=args.refresh)
    bars_4h = load_or_fetch(symbol, "4h", years=args.years, refresh=args.refresh)
    print(
        f"  1d={len(daily)} bars ({daily[0].open_time.date()}→{daily[-1].open_time.date()}); "
        f"4h={len(bars_4h)}",
        flush=True,
    )

    frames = build_all_signals(daily, bars_4h, m1_ema21=True)
    start_6m = _window_start_ms(args.months_6m)
    rows = []
    for vid, frame in frames.items():
        for label, start in (("full", None), ("6m", start_6m)):
            dual = run_dual_modes(
                symbol,
                frame,
                window_start_ms=start,
                window_label=label,
                initial_equity=args.initial,
            )
            for mode, res in dual.items():
                m = summarize(res)
                gate = m["gate_label"] if mode == "Mode-A" else "—"
                print(
                    f"  {vid} {label} {mode}: trades={m['trades']} "
                    f"wr={m['win_rate_pct']:.1f}% ret={m['return_pct']:+.2f}% "
                    f"bh={m['buy_hold_return_pct']:+.2f}% gate={gate}",
                    flush=True,
                )
                rows.append(res)

    out = args.out or (RESULTS_DIR / f"{RESEARCH_ID}-open-proxy.md")
    data_notes = [
        "Source: Binance Spot public klines via data-api.binance.vision (no API key)",
        f"Symbol: {symbol}",
        f"1D bars: {len(daily)} "
        f"({daily[0].open_time:%Y-%m-%d} → {daily[-1].open_time:%Y-%m-%d} UTC)",
        f"4H bars: {len(bars_4h)} "
        f"({bars_4h[0].open_time:%Y-%m-%d} → {bars_4h[-1].open_time:%Y-%m-%d} UTC)",
        "2D: aggregate_1d_to_2d — consecutive daily pairs, drop trailing orphan",
        f"Fetch lookback ~{args.years:g}y; 6m window = last {args.months_6m:g} months",
    ]
    write_report(rows=rows, path=out, symbol=symbol, data_notes=data_notes)
    print(f"Wrote {out}", flush=True)

    # Console gate summary for parent
    print("\n=== 6m Mode-A gate summary ===", flush=True)
    for r in sorted(
        [x for x in rows if x.window_label == "6m" and x.mode == "Mode-A"],
        key=lambda z: z.variant,
    ):
        m = summarize(r)
        ratio = m["ratio_vs_bh"]
        ratio_s = f"{ratio:.2f}×" if ratio == ratio else "n/a"
        print(
            f"{m['variant']}: ret={m['return_pct']:+.2f}% bh={m['buy_hold_return_pct']:+.2f}% "
            f"ratio={ratio_s} wr={m['win_rate_pct']:.1f}% trades={m['trades']} "
            f"**{m['gate_label']}**",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
