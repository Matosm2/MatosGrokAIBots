"""CLI: python -m backtest.path_b.mtf_ohlcv [--refresh] [--tfs 1h,4h,1d]

Runs owned-tf-sweep-v1 scoreboard (10 strategies × TFs).
"""

from __future__ import annotations

import argparse

from backtest.path_b.mtf_ohlcv.sweep import run_sweep, write_scoreboard
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS, mapping_table, ordered_tfs


def main() -> None:
    ap = argparse.ArgumentParser(description="owned-tf-sweep-v1 scoreboard")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--years", type=float, default=2.5)
    ap.add_argument(
        "--tfs",
        type=str,
        default="",
        help="Comma list of TFs (default: priority then backfill all 16)",
    )
    ap.add_argument("--mapping-only", action="store_true")
    args = ap.parse_args()

    if args.mapping_only:
        print("TF → source mapping")
        for m in mapping_table():
            htf = f" | M2/M4 HTF={m.m2_m4_htf}" if m.m2_m4_htf else ""
            print(f"  {m.tf:4} <- {m.rule}{htf}")
        return

    if args.tfs.strip():
        tfs = tuple(x.strip() for x in args.tfs.split(",") if x.strip())
    else:
        tfs = ordered_tfs()
        # ordered_tfs is priority+rest of SWEEP_TFS
        assert set(tfs) >= set(SWEEP_TFS)

    results = run_sweep(years=args.years, refresh=args.refresh, tfs=tfs)
    path = write_scoreboard(results)
    passes = [r for r in results if r.gate == "PASS"]
    print(f"
Scoreboard written: {path}")
    print(f"Cells: {len(results)}  PASS: {len(passes)}  FAIL/ERR: {len(results) - len(passes)}")
    for r in passes:
        print(f"  PASS {r.strategy_id} @ {r.tf} ratio={r.ratio:.3f}")


if __name__ == "__main__":
    main()
