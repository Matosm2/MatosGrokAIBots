"""CLI: python -m backtest.path_b.fresh_wave [--refresh] [--tfs ...] [--oos-ladder]"""

from __future__ import annotations

import argparse

from backtest.path_b.fresh_wave import RESEARCH_ID, STRATEGY_IDS
from backtest.path_b.fresh_wave.sweep import run_fresh_wave, write_scoreboard
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS, ordered_tfs


def main() -> None:
    ap = argparse.ArgumentParser(description=f"{RESEARCH_ID} scoreboard / OOS ladder")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--years", type=float, default=2.5)
    ap.add_argument("--tfs", type=str, default="", help="Comma TFs (default: all 16)")
    ap.add_argument(
        "--oos-ladder",
        action="store_true",
        help="Stop-ladder OOS: ETH→SOL→BNB on PASS_6m cells",
    )
    args = ap.parse_args()

    if args.oos_ladder:
        from backtest.path_b.fresh_wave.oos_ladder import (
            OOS_RESEARCH_ID,
            run_oos_ladder,
            write_oos_ladder_report,
        )

        print(f"{OOS_RESEARCH_ID}: stop-ladder ETH→SOL→BNB", flush=True)
        results = run_oos_ladder(years=args.years, refresh=args.refresh)
        path = write_oos_ladder_report(results)
        ran = [r for r in results if not r.skipped and not r.error]
        passes = [r for r in ran if r.gate_6m == "PASS"]
        skips = [r for r in results if r.skipped]
        print(f"\nReport written: {path}")
        print(
            f"Ran: {len(ran)}  PASS_6m: {len(passes)}  SKIP: {len(skips)}  "
            f"ERROR: {sum(1 for r in results if r.error)}"
        )
        for r in passes:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            print(
                f"  PASS_6m {r.symbol} {r.strategy_id}@{r.tf} "
                f"ratio={g.ratio:.3f} n={g.trades}"
            )
        return

    if args.tfs.strip():
        tfs = tuple(x.strip() for x in args.tfs.split(",") if x.strip())
    else:
        tfs = ordered_tfs()
        assert set(tfs) >= set(SWEEP_TFS)

    print(f"{RESEARCH_ID}: {len(STRATEGY_IDS)} IDs × {len(tfs)} TFs", flush=True)
    results = run_fresh_wave(years=args.years, refresh=args.refresh, tfs=tfs)
    path = write_scoreboard(results)
    passes = [r for r in results if r.gate_6m == "PASS"]
    print(f"\nScoreboard written: {path}")
    print(
        f"Cells: {len(results)}  PASS_6m: {len(passes)}  "
        f"PASS_full: {sum(1 for r in results if r.gate_full == 'PASS')}  "
        f"ERROR: {sum(1 for r in results if r.error)}"
    )
    for r in passes:
        g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
        print(f"  PASS_6m {r.strategy_id} @ {r.tf} ratio={g.ratio:.3f} n={g.trades}")


if __name__ == "__main__":
    main()
