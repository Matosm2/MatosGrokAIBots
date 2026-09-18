"""CLI entrypoint for stage2-sol-aware-v1 research."""

from __future__ import annotations

import argparse
import sys

from backtest.path_b.stage2_sol_aware_v1.sweep import run_stage2_sol_aware_v1, write_scoreboard


def main() -> int:
    parser = argparse.ArgumentParser(description="stage2-sol-aware-v1 backtest harness")
    parser.add_argument("--years", type=float, default=2.5, help="Years of data to fetch (default 2.5)")
    parser.add_argument("--refresh", action="store_true", help="Force refresh data cache")
    args = parser.parse_args()

    print("[stage2-sol-aware-v1] Starting sweep...", flush=True)
    results = run_stage2_sol_aware_v1(years=args.years, refresh=args.refresh)
    md_path, csv_path = write_scoreboard(results)
    print(f"\n[stage2-sol-aware-v1] Scoreboard written to:\n  - {md_path}\n  - {csv_path}", flush=True)

    pass_6m = [r for r in results if r.gate_6m == "PASS"]
    print(f"\n[stage2-sol-aware-v1] Complete! Total cells: {len(results)}, PASS_6m: {len(pass_6m)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
