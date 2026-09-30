"""CLI entry point for stage25-dual-sol-bnb-v1."""

from __future__ import annotations

import argparse

from backtest.path_b.stage25_dual_sol_bnb_v1.sweep import (
    DEFAULT_SYMBOLS,
    run_stage25_dual_sol_bnb_v1,
    write_scoreboard,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="stage25-dual-sol-bnb-v1 sweep and scoreboard generation"
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=list(DEFAULT_SYMBOLS),
        help="Symbols to test (default: BTCUSDT ETHUSDT SOLUSDT BNBUSDT)",
    )
    parser.add_argument(
        "--years",
        type=float,
        default=2.5,
        help="History length in years (default: 2.5)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh data cache",
    )
    args = parser.parse_args()

    results = run_stage25_dual_sol_bnb_v1(
        symbols=tuple(args.symbols),
        years=args.years,
        refresh=args.refresh,
    )
    md_path, csv_path = write_scoreboard(results)
    print(f"\n[stage25-dual-sol-bnb-v1] Wrote scoreboard to {md_path} and {csv_path}")


if __name__ == "__main__":
    main()
