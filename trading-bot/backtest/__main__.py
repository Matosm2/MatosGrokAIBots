"""CLI: python -m backtest [--years 2] [--refresh] [--symbols BTCUSDT,ETHUSDT]"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import load_or_fetch
from backtest.engine import run_backtest
from backtest.metrics import summarize
from backtest.report import write_results_markdown
from backtest.signals import StrategyParams


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Offline backtest: ema-rsi-trend-v1.1")
    p.add_argument("--years", type=float, default=2.0, help="Years of 1h history (default 2)")
    p.add_argument("--refresh", action="store_true", help="Ignore cache and re-fetch")
    p.add_argument(
        "--symbols",
        default="BTCUSDT,ETHUSDT",
        help="Comma-separated symbols",
    )
    p.add_argument("--initial", type=float, default=10_000.0)
    p.add_argument("--buy-qty-pct", type=float, default=2.5)
    p.add_argument(
        "--fee",
        type=float,
        default=0.001,
        help="Fee fraction per side (default 0.001 = 0.1%)",
    )
    p.add_argument(
        "--slippage",
        type=float,
        default=0.0005,
        help="Adverse slippage vs close (default 0.0005 = 5 bps)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent / "results" / "ema-rsi-trend-v1.1.md",
    )
    args = p.parse_args(argv)

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    params = StrategyParams(cooldown_bars=6)
    results = []
    bars_by_symbol = {}

    for sym in symbols:
        print(f"Loading {sym} 1h (~{args.years:g}y)...", flush=True)
        bars = load_or_fetch(sym, "1h", years=args.years, refresh=args.refresh)
        if len(bars) < 100:
            print(f"ERROR: insufficient bars for {sym}: {len(bars)}", file=sys.stderr)
            return 1
        bars_by_symbol[sym] = bars
        print(
            f"  {len(bars)} bars  "
            f"{datetime.fromtimestamp(bars[0].open_time_ms/1000, tz=timezone.utc):%Y-%m-%d} → "
            f"{datetime.fromtimestamp(bars[-1].open_time_ms/1000, tz=timezone.utc):%Y-%m-%d}",
            flush=True,
        )
        r = run_backtest(
            sym,
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
            f"  trades={m.trades} win={m.win_rate_pct:.1f}% "
            f"exp={m.expectancy_usdt:+.2f} ret={m.return_pct:+.2f}% "
            f"dd={m.max_drawdown_pct:.2f}% bh={m.buy_hold_return_pct:+.2f}%",
            flush=True,
        )

    write_results_markdown(
        results=results,
        bars_by_symbol=bars_by_symbol,
        path=args.out,
        years=args.years,
    )
    dated = args.out.with_name(
        f"{args.out.stem}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    )
    shutil.copyfile(args.out, dated)
    print(f"Wrote {args.out}", flush=True)
    print(f"Wrote {dated}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
