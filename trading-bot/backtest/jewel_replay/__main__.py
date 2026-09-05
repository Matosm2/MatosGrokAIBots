"""CLI: python -m backtest.jewel_replay path/to.csv [--symbol BTCUSDT]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from backtest.jewel_replay.csv_loader import load_jewel_csv
from backtest.jewel_replay.engine import run_replay
from backtest.jewel_replay.report import summarize, write_replay_markdown
from backtest.jewel_replay.signals import JewelParams, Variant


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Path B replay: jewel-strength-hold-v1 (V-zone + V-wide)"
    )
    p.add_argument("csv", type=Path, help="CSV with time,OHLCV,Slow,High/jewel_high")
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--initial", type=float, default=10_000.0)
    p.add_argument("--buy-qty-pct", type=float, default=2.5)
    p.add_argument("--fee", type=float, default=0.001, help="0.001 = 0.10%/side")
    p.add_argument("--slippage", type=float, default=0.0005, help="5 bps default")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Markdown report path (default under jewel_replay/results/)",
    )
    args = p.parse_args(argv)

    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 1

    bars = load_jewel_csv(args.csv)
    results = []
    for variant in (Variant.V_ZONE, Variant.V_WIDE):
        params = JewelParams(variant=variant)
        r = run_replay(
            args.symbol,
            bars,
            params=params,
            initial_equity=args.initial,
            buy_qty_pct=args.buy_qty_pct,
            fee_rate=args.fee,
            slippage_rate=args.slippage,
        )
        m = summarize(r)
        results.append(r)
        print(
            f"{variant.value}: trades={m['trades']} wr={float(m['win_rate_pct']):.1f}% "
            f"ret={float(m['return_pct']):+.2f}% bh={float(m['buy_hold_return_pct']):+.2f}% "
            f"dd={float(m['max_drawdown_pct']):.2f}% "
            f"gate={'PASS' if m['gate_wr_ok'] and m['gate_bh_ok'] else 'FAIL'}",
            flush=True,
        )

    out = args.out or (
        Path(__file__).resolve().parent / "results" / "jewel-strength-hold-v1.md"
    )
    write_replay_markdown(results=results, path=out, source_csv=str(args.csv))
    print(f"Wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
