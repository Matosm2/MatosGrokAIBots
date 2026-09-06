"""CLI: python -m backtest.path_b.mtf_ohlcv [--refresh] [--tfs 1h,4h,1d] [--longwin] [--dual-mom-oos]

Runs owned-tf-sweep-v1 (6m), owned-tf-sweep-v1-longwin (LEAD full~2y + 6m),
or dual-mom-oos (dual-mom @ 1d+2d only).
"""

from __future__ import annotations

import argparse

from backtest.path_b.mtf_ohlcv.sweep import run_sweep, write_scoreboard
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS, mapping_table, ordered_tfs


def main() -> None:
    ap = argparse.ArgumentParser(
        description="owned-tf-sweep-v1 / longwin / dual-mom-oos scoreboard"
    )
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--years", type=float, default=2.5)
    ap.add_argument(
        "--tfs",
        type=str,
        default="",
        help="Comma list of TFs (default: priority then backfill all 16)",
    )
    ap.add_argument("--mapping-only", action="store_true")
    ap.add_argument(
        "--longwin",
        action="store_true",
        help="LEAD full(~2y) Mode-A gate + report 6m (owned-tf-sweep-v1-longwin)",
    )
    ap.add_argument(
        "--dual-mom-oos",
        action="store_true",
        help="dual-mom-btc-eth-v1 @ 1d+2d only (vs 50/50; research-only)",
    )
    args = ap.parse_args()

    if args.mapping_only:
        print("TF → source mapping")
        for m in mapping_table():
            htf = f" | M2/M4 HTF={m.m2_m4_htf}" if m.m2_m4_htf else ""
            print(f"  {m.tf:4} <- {m.rule}{htf}")
        return

    if args.dual_mom_oos:
        from backtest.path_b.mtf_ohlcv.dual_mom_oos import (
            run_dual_mom_oos,
            write_dual_mom_oos_report,
        )

        results = run_dual_mom_oos(years=args.years, refresh=args.refresh)
        path = write_dual_mom_oos_report(results)
        print(f"\nDual-mom OOS report written: {path}")
        for r in results:
            print(
                f"  {r.strategy_id} @ {r.tf}: full={r.gate_full} 6m={r.gate_6m}"
                + (f" ERR={r.error}" if r.error else "")
            )
        return

    if args.tfs.strip():
        tfs = tuple(x.strip() for x in args.tfs.split(",") if x.strip())
    else:
        tfs = ordered_tfs()
        assert set(tfs) >= set(SWEEP_TFS)

    if args.longwin:
        from backtest.path_b.mtf_ohlcv.longwin import (
            run_longwin_sweep,
            write_longwin_scoreboard,
        )

        results = run_longwin_sweep(years=args.years, refresh=args.refresh, tfs=tfs)
        path = write_longwin_scoreboard(results)
        lw = [r for r in results if r.gate_longwin == "PASS"]
        s6 = [r for r in results if r.gate_6m == "PASS"]
        print(f"\nLongwin scoreboard written: {path}")
        print(
            f"Cells: {len(results)}  PASS_longwin: {len(lw)}  "
            f"PASS_6m: {len(s6)}  ERROR: {sum(1 for r in results if r.error)}"
        )
        for r in lw:
            g = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
            print(
                f"  PASS_longwin {r.strategy_id} @ {r.tf} "
                f"ratio={g.ratio:.3f} n={g.trades} wr={g.win_rate_pct:.1f}% "
                f"(6m={r.gate_6m})"
            )
        return

    results = run_sweep(years=args.years, refresh=args.refresh, tfs=tfs)
    path = write_scoreboard(results)
    passes = [r for r in results if r.gate == "PASS"]
    print(f"\nScoreboard written: {path}")
    print(
        f"Cells: {len(results)}  PASS: {len(passes)}  "
        f"FAIL/ERR: {len(results) - len(passes)}"
    )
    for r in passes:
        print(f"  PASS {r.strategy_id} @ {r.tf} ratio={r.ratio:.3f}")


if __name__ == "__main__":
    main()
