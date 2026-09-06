"""CLI: python -m backtest.path_b.fresh_wave_v2 [--refresh] [--tfs ...]"""

from __future__ import annotations

import argparse

from backtest.path_b.fresh_wave_v2 import COARSE_FIRST_TFS, RESEARCH_ID, STRATEGY_IDS
from backtest.path_b.fresh_wave_v2.sweep import run_fresh_wave_v2, write_scoreboard
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS


def main() -> None:
    ap = argparse.ArgumentParser(description=f"{RESEARCH_ID} scoreboard (BTCUSDT)")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--years", type=float, default=2.5)
    ap.add_argument(
        "--tfs",
        type=str,
        default="",
        help="Comma TFs (default: coarse-first 16)",
    )
    args = ap.parse_args()

    if args.tfs.strip():
        tfs = tuple(x.strip() for x in args.tfs.split(",") if x.strip())
    else:
        tfs = COARSE_FIRST_TFS
        assert set(tfs) == set(SWEEP_TFS)

    print(f"{RESEARCH_ID}: {len(STRATEGY_IDS)} IDs × {len(tfs)} TFs", flush=True)
    results = run_fresh_wave_v2(years=args.years, refresh=args.refresh, tfs=tfs)
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
