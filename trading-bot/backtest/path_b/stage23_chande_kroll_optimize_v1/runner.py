"""Comprehensive sweep runner and scoreboard generator for Stage 23 Chande Kroll Optimize v1.

LEAN Mode A First.
Neighborhood sweep around banked near-miss (p=10, x=1.0, q=9) ~1.194x BTC Mode-A.
TF 1H vs 4H.
Coins: BTCUSDT -> ETHUSDT -> SOLUSDT -> BNBUSDT (identical params across all four).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backtest.data import Bar
from backtest.path_b.stage23_chande_kroll_optimize_v1.data import (
    filter_last_months,
    get_bars_for_timeframe,
)
from backtest.path_b.stage23_chande_kroll_optimize_v1.signals import (
    BacktestRunResult,
    ChandeKrollParams,
    run_chande_kroll_backtest,
)


@dataclass
class ScoreboardEntry:
    strategy_id: str
    timeframe: str
    mode: str
    p: int
    x: float
    q: int
    # 6m Primary Lead Metrics (Full clip 100%)
    btc_n_6m: int
    btc_wr_6m: float
    btc_ret_6m: float
    btc_bh_6m: float
    btc_x_bh_6m: float
    btc_pass_6m: bool
    btc_smoke: str
    # Ladder metrics (if BTC passes or for complete comparison)
    eth_n_6m: int
    eth_ret_6m: float
    eth_bh_6m: float
    eth_x_bh_6m: float
    eth_pass_6m: bool
    eth_smoke: str
    sol_n_6m: int
    sol_ret_6m: float
    sol_bh_6m: float
    sol_x_bh_6m: float
    sol_pass_6m: bool
    sol_smoke: str
    bnb_n_6m: int
    bnb_ret_6m: float
    bnb_bh_6m: float
    bnb_x_bh_6m: float
    bnb_pass_6m: bool
    bnb_smoke: str
    # Full ladder result
    full_ladder_pass_6m: bool
    # 2y Full History Metrics
    btc_ret_2y: float
    btc_n_2y: int
    btc_bh_2y: float
    btc_ops_ret_2y: float  # 2.5% clip
    notes: str


def evaluate_smoke(
    coin: str,
    n_6m: int,
    ret_6m: float,
    bh_6m: float,
    x_bh_6m: float,
    pass_6m: bool,
    p: int,
    x: float,
    q: int,
) -> str:
    """Evaluate coin smoke criteria per CODING_KICK specs."""
    if coin == "BTC":
        if n_6m == 0:
            return "KILL: 0 trades"
        if n_6m <= 5:
            return f"KILL: tiny-n (n={n_6m} <= 5)"
        if ret_6m <= 0:
            return "KILL: negative ret"
        if not pass_6m:
            if x_bh_6m < 1.0:
                return f"FAIL: lag B&H ({x_bh_6m:.3f}x)"
            elif x_bh_6m < 1.194:
                return f"FAIL: under banked 1.194x ({x_bh_6m:.3f}x)"
            elif x_bh_6m < 1.20:
                return f"FAIL: near-miss 1.194-1.20x ({x_bh_6m:.3f}x)"
        return "PASS_SMOKE"
    elif coin == "ETH":
        if n_6m <= 5:
            return f"KILL: tiny-n (n={n_6m})"
        if not pass_6m:
            return f"FAIL: under 1.2x B&H ({x_bh_6m:.3f}x)"
        return "PASS_SMOKE"
    elif coin == "SOL":
        if n_6m <= 5:
            return f"KILL: tiny-n (n={n_6m})"
        if not pass_6m:
            return f"FAIL: under 1.2x B&H ({x_bh_6m:.3f}x, 0.922x rhyme)"
        return "PASS_SMOKE"
    elif coin == "BNB":
        if n_6m <= 5:
            return f"KILL: tiny-n (n={n_6m})"
        if not pass_6m:
            return f"FAIL: under 1.2x B&H ({x_bh_6m:.3f}x, quiet wipe)"
        return "PASS_SMOKE"
    return "UNKNOWN"


def is_pass_6m(ret_6m: float, bh_6m: float, n_6m: int) -> tuple[bool, float]:
    """Check if strategy meets Mode-A >= 1.2x B&H gate with n > 5."""
    if n_6m <= 5:
        return False, (ret_6m / bh_6m if bh_6m != 0 else 0.0)

    if bh_6m > 0:
        ratio = ret_6m / bh_6m
        passed = (ret_6m >= 1.20 * bh_6m) and (ret_6m > 0)
        return passed, ratio
    else:
        # If buy-and-hold is negative or flat:
        # Outperforming negative B&H by positive margin or ratio
        ratio = (ret_6m / abs(bh_6m)) if bh_6m != 0 else (100.0 if ret_6m > 0 else 0.0)
        passed = ret_6m > 0
        return passed, ratio


def run_sweep(
    symbols: list[str] = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"],
    timeframes: list[str] = ["1h", "4h"],
    p_vals: list[int] = [8, 10, 12, 14],
    x_vals: list[float] = [0.8, 1.0, 1.2, 1.5],
    q_vals: list[int] = [5, 7, 9, 11, 14],
    mode: str = "A",
    results_dir: Path | None = None,
) -> list[ScoreboardEntry]:
    results_dir = results_dir or Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load bars for all symbols and timeframes
    bars_full: dict[str, dict[str, list[Bar]]] = {}
    bars_6m: dict[str, dict[str, list[Bar]]] = {}

    for sym in symbols:
        bars_full[sym] = {}
        bars_6m[sym] = {}
        for tf in timeframes:
            print(f"Loading {sym} {tf}...", flush=True)
            b = get_bars_for_timeframe(sym, tf, years=2.0)
            bars_full[sym][tf] = b
            bars_6m[sym][tf] = filter_last_months(b, months=6.0)
            print(
                f"  Loaded {len(b)} 2y bars, {len(bars_6m[sym][tf])} 6m bars",
                flush=True,
            )

    entries: list[ScoreboardEntry] = []
    total_combos = len(timeframes) * len(p_vals) * len(x_vals) * len(q_vals)
    print(f"\nStarting sweep over {total_combos} parameter combinations...", flush=True)

    combo_idx = 0
    for tf in timeframes:
        for p in p_vals:
            for x in x_vals:
                for q in q_vals:
                    combo_idx += 1
                    params = ChandeKrollParams(p=p, x=x, q=q, mode=mode)

                    # 1. Run BTC first (LEAD)
                    btc_6m = run_chande_kroll_backtest(
                        "BTCUSDT",
                        bars_6m["BTCUSDT"][tf],
                        params=params,
                        timeframe=tf,
                        buy_qty_pct=100.0,
                    )
                    btc_n_6m = len(btc_6m.trades)
                    btc_ret_6m = btc_6m.strategy_return_pct
                    btc_bh_6m = btc_6m.buy_hold_return_pct
                    btc_pass, btc_x_bh = is_pass_6m(btc_ret_6m, btc_bh_6m, btc_n_6m)
                    btc_smk = evaluate_smoke(
                        "BTC", btc_n_6m, btc_ret_6m, btc_bh_6m, btc_x_bh, btc_pass, p, x, q
                    )

                    # 2. Run ETH
                    eth_6m = run_chande_kroll_backtest(
                        "ETHUSDT",
                        bars_6m["ETHUSDT"][tf],
                        params=params,
                        timeframe=tf,
                        buy_qty_pct=100.0,
                    )
                    eth_n_6m = len(eth_6m.trades)
                    eth_ret_6m = eth_6m.strategy_return_pct
                    eth_bh_6m = eth_6m.buy_hold_return_pct
                    eth_pass, eth_x_bh = is_pass_6m(eth_ret_6m, eth_bh_6m, eth_n_6m)
                    eth_smk = evaluate_smoke(
                        "ETH", eth_n_6m, eth_ret_6m, eth_bh_6m, eth_x_bh, eth_pass, p, x, q
                    )

                    # 3. Run SOL (PRIMARY CRITICAL)
                    sol_6m = run_chande_kroll_backtest(
                        "SOLUSDT",
                        bars_6m["SOLUSDT"][tf],
                        params=params,
                        timeframe=tf,
                        buy_qty_pct=100.0,
                    )
                    sol_n_6m = len(sol_6m.trades)
                    sol_ret_6m = sol_6m.strategy_return_pct
                    sol_bh_6m = sol_6m.buy_hold_return_pct
                    sol_pass, sol_x_bh = is_pass_6m(sol_ret_6m, sol_bh_6m, sol_n_6m)
                    sol_smk = evaluate_smoke(
                        "SOL", sol_n_6m, sol_ret_6m, sol_bh_6m, sol_x_bh, sol_pass, p, x, q
                    )

                    # 4. Run BNB
                    bnb_6m = run_chande_kroll_backtest(
                        "BNBUSDT",
                        bars_6m["BNBUSDT"][tf],
                        params=params,
                        timeframe=tf,
                        buy_qty_pct=100.0,
                    )
                    bnb_n_6m = len(bnb_6m.trades)
                    bnb_ret_6m = bnb_6m.strategy_return_pct
                    bnb_bh_6m = bnb_6m.buy_hold_return_pct
                    bnb_pass, bnb_x_bh = is_pass_6m(bnb_ret_6m, bnb_bh_6m, bnb_n_6m)
                    bnb_smk = evaluate_smoke(
                        "BNB", bnb_n_6m, bnb_ret_6m, bnb_bh_6m, bnb_x_bh, bnb_pass, p, x, q
                    )

                    full_ladder = btc_pass and eth_pass and sol_pass and bnb_pass

                    # 5. Run full 2y on BTC
                    btc_2y = run_chande_kroll_backtest(
                        "BTCUSDT",
                        bars_full["BTCUSDT"][tf],
                        params=params,
                        timeframe=tf,
                        buy_qty_pct=100.0,
                    )
                    btc_2y_ops = run_chande_kroll_backtest(
                        "BTCUSDT",
                        bars_full["BTCUSDT"][tf],
                        params=params,
                        timeframe=tf,
                        buy_qty_pct=2.5,
                    )

                    # Notes on comparison to baseline
                    notes_list = []
                    if (p, x, q) == (10, 1.0, 9):
                        notes_list.append("BANKED_BASELINE_(10,1.0,9)")
                    if btc_x_bh >= 1.194:
                        notes_list.append(f">=1.194x_near_miss({btc_x_bh:.3f}x)")
                    if btc_pass:
                        notes_list.append(f"BTC_PASS_1.20x({btc_x_bh:.3f}x)")
                    if btc_n_6m > 9:
                        notes_list.append(f"denser_n({btc_n_6m}>>9)")
                    elif btc_n_6m <= 5:
                        notes_list.append(f"tiny_n({btc_n_6m}<=5)")
                    else:
                        notes_list.append(f"n={btc_n_6m}")

                    entry = ScoreboardEntry(
                        strategy_id="chande-kroll-stop-flip",
                        timeframe=tf,
                        mode=mode,
                        p=p,
                        x=x,
                        q=q,
                        btc_n_6m=btc_n_6m,
                        btc_wr_6m=btc_6m.win_rate_pct,
                        btc_ret_6m=btc_ret_6m,
                        btc_bh_6m=btc_bh_6m,
                        btc_x_bh_6m=btc_x_bh,
                        btc_pass_6m=btc_pass,
                        btc_smoke=btc_smk,
                        eth_n_6m=eth_n_6m,
                        eth_ret_6m=eth_ret_6m,
                        eth_bh_6m=eth_bh_6m,
                        eth_x_bh_6m=eth_x_bh,
                        eth_pass_6m=eth_pass,
                        eth_smoke=eth_smk,
                        sol_n_6m=sol_n_6m,
                        sol_ret_6m=sol_ret_6m,
                        sol_bh_6m=sol_bh_6m,
                        sol_x_bh_6m=sol_x_bh,
                        sol_pass_6m=sol_pass,
                        sol_smoke=sol_smk,
                        bnb_n_6m=bnb_n_6m,
                        bnb_ret_6m=bnb_ret_6m,
                        bnb_bh_6m=bnb_bh_6m,
                        bnb_x_bh_6m=bnb_x_bh,
                        bnb_pass_6m=bnb_pass,
                        bnb_smoke=bnb_smk,
                        full_ladder_pass_6m=full_ladder,
                        btc_ret_2y=btc_2y.strategy_return_pct,
                        btc_n_2y=len(btc_2y.trades),
                        btc_bh_2y=btc_2y.buy_hold_return_pct,
                        btc_ops_ret_2y=btc_2y_ops.strategy_return_pct,
                        notes="; ".join(notes_list),
                    )
                    entries.append(entry)

                    if combo_idx % 10 == 0 or (p, x, q) == (10, 1.0, 9):
                        print(
                            f"[{combo_idx}/{total_combos}] {tf} ({p},{x},{q}) -> "
                            f"BTC: n={btc_n_6m} ret={btc_ret_6m:.2f}% bh={btc_bh_6m:.2f}% "
                            f"xBH={btc_x_bh:.3f}x pass={btc_pass} | ETH pass={eth_pass} | "
                            f"SOL pass={sol_pass} | BNB pass={bnb_pass}",
                            flush=True,
                        )

    # Sort entries by BTC x_bh_6m descending
    entries.sort(key=lambda e: (e.btc_pass_6m, e.btc_x_bh_6m, e.btc_n_6m), reverse=True)
    return entries


def write_scoreboard(
    entries: list[ScoreboardEntry],
    results_dir: Path,
) -> tuple[Path, Path]:
    csv_path = results_dir / "scoreboard.csv"
    md_path = results_dir / "scoreboard.md"

    # 1. Write CSV
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "strategy_id",
                "TF",
                "mode",
                "p",
                "x",
                "q",
                "btc_n_6m",
                "btc_wr_6m",
                "btc_ret_6m",
                "btc_bh_6m",
                "btc_x_bh_6m",
                "btc_pass_6m",
                "btc_smoke",
                "eth_n_6m",
                "eth_ret_6m",
                "eth_bh_6m",
                "eth_x_bh_6m",
                "eth_pass_6m",
                "eth_smoke",
                "sol_n_6m",
                "sol_ret_6m",
                "sol_bh_6m",
                "sol_x_bh_6m",
                "sol_pass_6m",
                "sol_smoke",
                "bnb_n_6m",
                "bnb_ret_6m",
                "bnb_bh_6m",
                "bnb_x_bh_6m",
                "bnb_pass_6m",
                "bnb_smoke",
                "full_ladder_pass_6m",
                "btc_ret_2y",
                "btc_n_2y",
                "btc_bh_2y",
                "btc_ops_ret_2y",
                "notes",
            ]
        )
        for e in entries:
            w.writerow(
                [
                    e.strategy_id,
                    e.timeframe,
                    e.mode,
                    e.p,
                    e.x,
                    e.q,
                    e.btc_n_6m,
                    f"{e.btc_wr_6m:.2f}",
                    f"{e.btc_ret_6m:.2f}",
                    f"{e.btc_bh_6m:.2f}",
                    f"{e.btc_x_bh_6m:.3f}",
                    "Y" if e.btc_pass_6m else "N",
                    e.btc_smoke,
                    e.eth_n_6m,
                    f"{e.eth_ret_6m:.2f}",
                    f"{e.eth_bh_6m:.2f}",
                    f"{e.eth_x_bh_6m:.3f}",
                    "Y" if e.eth_pass_6m else "N",
                    e.eth_smoke,
                    e.sol_n_6m,
                    f"{e.sol_ret_6m:.2f}",
                    f"{e.sol_bh_6m:.2f}",
                    f"{e.sol_x_bh_6m:.3f}",
                    "Y" if e.sol_pass_6m else "N",
                    e.sol_smoke,
                    e.bnb_n_6m,
                    f"{e.bnb_ret_6m:.2f}",
                    f"{e.bnb_bh_6m:.2f}",
                    f"{e.bnb_x_bh_6m:.3f}",
                    "Y" if e.bnb_pass_6m else "N",
                    e.bnb_smoke,
                    "Y" if e.full_ladder_pass_6m else "N",
                    f"{e.btc_ret_2y:.2f}",
                    e.btc_n_2y,
                    f"{e.btc_bh_2y:.2f}",
                    f"{e.btc_ops_ret_2y:.2f}",
                    e.notes,
                ]
            )

    # 2. Write Markdown
    pass_entries = [e for e in entries if e.btc_pass_6m]
    full_ladder_entries = [e for e in entries if e.full_ladder_pass_6m]
    baseline_entries = [e for e in entries if (e.p, e.x, e.q) == (10, 1.0, 9)]

    md_lines = [
        "# Scoreboard: stage23-chande-kroll-optimize-v1",
        "",
        f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}_",
        "",
        "## Summary",
        f"- **Strategy ID:** `chande-kroll-stop-flip`",
        f"- **Total Configurations Tested:** {len(entries)}",
        f"- **Banked Baseline Evaluated:** (p=10, x=1.0, q=9) across 1H and 4H",
        f"- **BTC PASS_6m Count (>=1.20x B&H, n > 5):** {len(pass_entries)}",
        f"- **Full Ladder PASS_6m Count (BTC->ETH->SOL->BNB):** {len(full_ladder_entries)}",
        "",
        "## Baseline vs Banked Near-Miss (~1.194x)",
        "| TF | Params (p,x,q) | BTC n | BTC Ret% | BTC B&H% | x B&H | BTC Smoke | PASS 6m | Notes |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for b in baseline_entries:
        md_lines.append(
            f"| {b.timeframe} | ({b.p}, {b.x}, {b.q}) | {b.btc_n_6m} | {b.btc_ret_6m:+.2f}% | "
            f"{b.btc_bh_6m:+.2f}% | {b.btc_x_bh_6m:.3f}x | {b.btc_smoke} | "
            f"{'YES' if b.btc_pass_6m else 'NO'} | {b.notes} |"
        )

    md_lines.extend(
        [
            "",
            "## Top 20 Configurations by BTC Performance",
            "| Rank | TF | Params (p,x,q) | BTC n | BTC Ret% | BTC B&H% | x B&H | ETH xB&H | SOL xB&H | BNB xB&H | Full Ladder | Notes |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for i, e in enumerate(entries[:20], 1):
        md_lines.append(
            f"| {i} | {e.timeframe} | ({e.p}, {e.x}, {e.q}) | {e.btc_n_6m} | {e.btc_ret_6m:+.2f}% | "
            f"{e.btc_bh_6m:+.2f}% | {e.btc_x_bh_6m:.3f}x | {e.eth_x_bh_6m:.3f}x | "
            f"{e.sol_x_bh_6m:.3f}x | {e.bnb_x_bh_6m:.3f}x | "
            f"{'**PASS**' if e.full_ladder_pass_6m else 'FAIL'} | {e.notes} |"
        )

    md_lines.extend(
        [
            "",
            "## Full Ladder PASS_6m Candidates",
            f"Total configurations passing all 4 coins: **{len(full_ladder_entries)}**",
            "",
        ]
    )
    if full_ladder_entries:
        md_lines.extend(
            [
                "| TF | Params | BTC Ret (n) | ETH Ret (n) | SOL Ret (n) | BNB Ret (n) | BTC 2y Ret | Ops 2.5% 2y |",
                "|---|---|---|---|---|---|---|---|",
            ]
        )
        for fl in full_ladder_entries:
            md_lines.append(
                f"| {fl.timeframe} | ({fl.p}, {fl.x}, {fl.q}) | {fl.btc_ret_6m:+.2f}% ({fl.btc_n_6m}) | "
                f"{fl.eth_ret_6m:+.2f}% ({fl.eth_n_6m}) | {fl.sol_ret_6m:+.2f}% ({fl.sol_n_6m}) | "
                f"{fl.bnb_ret_6m:+.2f}% ({fl.bnb_n_6m}) | {fl.btc_ret_2y:+.2f}% | {fl.btc_ops_ret_2y:+.2f}% |"
            )
    else:
        md_lines.append(
            "None of the swept configurations achieved Mode-A >= 1.20x B&H simultaneously "
            "across all four coins (BTC, ETH, SOL, BNB) with n > 5."
        )

    md_lines.extend(
        [
            "",
            "## Complete Sweep Results (All 80 Parameter Sets x 2 Timeframes)",
            "See `scoreboard.csv` for the full dataset.",
            "",
        ]
    )
    md_path.write_text("\n".join(md_lines))
    return csv_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sweep runner for Stage 23 Chande Kroll Optimize v1"
    )
    parser.add_argument(
        "--timeframes",
        default="1h,4h",
        help="Comma-separated timeframes (e.g. 1h,4h)",
    )
    parser.add_argument(
        "--mode",
        default="A",
        choices=["A", "B"],
        help="Mode A or Mode B",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
        help="Results output directory",
    )
    args = parser.parse_args(argv)

    tfs = [t.strip() for t in args.timeframes.split(",") if t.strip()]
    entries = run_sweep(
        timeframes=tfs,
        mode=args.mode,
        results_dir=args.out_dir,
    )
    csv_p, md_p = write_scoreboard(entries, args.out_dir)
    print(f"\nWrote results to:\n  {csv_p}\n  {md_p}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
