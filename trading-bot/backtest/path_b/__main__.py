"""CLI: python -m backtest.path_b [--refresh] [--no-full]

Path B research: five IDs, dual sizing, 6m Mode-A ≥1.2×B&H gate + full window.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from backtest.path_b import STRATEGY_IDS
from backtest.path_b.data_ccxt import load_or_fetch_ccxt
from backtest.path_b.engine import apply_position_gate, run_long_only, slice_result_to_window
from backtest.path_b.report import (
    GATE_SIZE_PCT,
    OPS_SIZE_PCT,
    summarize_path_b,
    write_batch_summary,
    write_strategy_report,
)
from backtest.path_b.bb_squeeze_breakout_v1 import (
    STRATEGY_ID as BB_ID,
    compute_signals as bb_signals,
)
from backtest.path_b.kama_er_trend_v1 import (
    STRATEGY_ID as KAMA_ID,
    compute_signals as kama_signals,
)
from backtest.path_b.sma200_trend_v1 import (
    STRATEGY_ID as SMA_ID,
    compute_signals as sma_signals,
)
from backtest.path_b.supertrend_atr_v1 import (
    STRATEGY_ID as ST_ID,
    compute_signals as st_signals,
)
from backtest.path_b.dual_mom_btc_eth_v1 import (
    STRATEGY_ID as DM_ID,
    run_dual_mom,
)

RESULTS_DIR = Path(__file__).resolve().parent / "results"

RULES = {
    BB_ID: [
        "TF Daily | BTCUSDT primary (ETH OOS if BTC 6m interesting)",
        "Squeeze: BB width(20,2) ≤ 20th percentile of prior 100 bars (no lookahead)",
        "Entry: prior bar in squeeze (or squeeze true) AND close > upper BB AND volume > SMA(vol,20)",
        "Exit: close < middle BB OR close < entry − 2.5×ATR(14) (ATR frozen at entry)",
        "Pyramiding 0",
    ],
    KAMA_ID: [
        "TF Daily | BTC then ETH if needed",
        "KAMA(10, fast=2, slow=30) + ER(10)",
        "Entry: close > KAMA AND ER > 0.30 (and flat)",
        "Exit: close < KAMA OR ER < 0.20",
    ],
    DM_ID: [
        "TF Daily | BTC+ETH book",
        "mom = total return over 20 closed days",
        "If max(BTC_mom, ETH_mom) ≤ 0 → flat (cash)",
        "Else allocate to argmax symbol (switch on bar close)",
        "Primary B&H: 50/50 BTC+ETH | Secondary: BTC-only B&H",
        "Gate on primary 50/50 ≥1.2×",
    ],
    SMA_ID: [
        "TF Daily | BTCUSDT primary",
        "Entry: close crosses above SMA(200) while flat (or first bar close > SMA200 after flat)",
        "Exit: close < SMA(200)",
        "No EMA add-ons; no SuperTrend on this ID",
    ],
    ST_ID: [
        "TF Daily | BTCUSDT primary",
        "SuperTrend(ATR length 10, mult 3)",
        "Entry: flip to bullish (direction +1) while flat",
        "Exit: flip to bearish",
        "Long-only Spot; no param spray",
    ],
}

SIZING = [("gate", GATE_SIZE_PCT), ("ops", OPS_SIZE_PCT)]


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc).timestamp() * 1000
    return int(now - months * 30.4375 * 24 * 3600 * 1000)


def _mask_before(flags, bars, start_ms):
    out = list(flags)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            out[i] = False
    return out


def _run_single(
    strategy_id: str,
    signal_fn,
    symbol: str,
    *,
    years: float,
    windows: list[tuple[str, float]],
    refresh: bool,
    fee: float,
    slip: float,
    initial: float,
    with_stops: bool = False,
):
    print(f"[{strategy_id}] {symbol} 1d (~{years:g}y) via ccxt...", flush=True)
    bars = load_or_fetch_ccxt(symbol, "1d", years=years, refresh=refresh)
    if with_stops:
        buys_full, sells_full, stops_full = signal_fn(bars)
    else:
        buys_full, sells_full = signal_fn(bars)
        stops_full = None
    out = {}
    for label, months in windows:
        start = _window_start_ms(months)
        # Recompute gated signals with entries masked pre-window
        if with_stops:
            raw_buys = _mask_before(buys_full, bars, start)
            # For stop strategies, re-gate from raw is messy; mask buys then re-run gate
            # Use: zero buys before window, keep sells; engine won't enter pre-window
            buys = raw_buys
            sells = sells_full
            stops = stops_full
        else:
            # Prefer remasking raw via signal_fn path: zero buy opportunities pre-window
            buys = _mask_before(buys_full, bars, start)
            sells = sells_full
            stops = None
        mode_res = {}
        for mode_name, buy_pct in SIZING:
            res = run_long_only(
                symbol,
                strategy_id,
                bars,
                buys,
                sells,
                stop_prices=stops,
                initial_equity=initial,
                buy_qty_pct=buy_pct,
                fee_rate=fee,
                slippage_rate=slip,
                window_label=label,
            )
            sliced = slice_result_to_window(res, bars, start, window_label=label)
            m = summarize_path_b(sliced)
            gate = "PASS" if m["gate_pass"] else "FAIL" if mode_name == "gate" else "—"
            print(
                f"  {symbol} {label} [{mode_name} {buy_pct:g}%]: n={m['trades']} "
                f"wr={m['win_rate_pct']:.1f}% ret={m['return_pct']:+.2f}% "
                f"bh={m['buy_hold_return_pct']:+.2f}% ratio={m['ret_bh_ratio']:.3f} [{gate}]",
                flush=True,
            )
            mode_res[mode_name] = sliced
        out[label] = mode_res
    return out


def _run_dual_mom(*, years, windows, refresh, fee, slip, initial):
    print(f"[{DM_ID}] BTC+ETH 1d (~{years:g}y) via ccxt...", flush=True)
    btc = load_or_fetch_ccxt("BTCUSDT", "1d", years=years, refresh=refresh)
    eth = load_or_fetch_ccxt("ETHUSDT", "1d", years=years, refresh=refresh)
    out = {}
    for label, months in windows:
        start = _window_start_ms(months)
        mode_res = {}
        for mode_name, buy_pct in SIZING:
            dm = run_dual_mom(
                btc,
                eth,
                initial_equity=initial,
                buy_qty_pct=buy_pct,
                fee_rate=fee,
                slippage_rate=slip,
                window_label=label,
                window_start_ms=start,
            )
            sk = dm.as_sketch()
            m = summarize_path_b(sk)
            # attach secondary BH in notes for report
            sk.notes = list(sk.notes) + [
                f"Secondary BTC-only B&H ({label}): {dm.btc_only_bh_return_pct:+.2f}%"
            ]
            gate = "PASS" if m["gate_pass"] else "FAIL" if mode_name == "gate" else "—"
            print(
                f"  BTC+ETH {label} [{mode_name} {buy_pct:g}%]: n={m['trades']} "
                f"wr={m['win_rate_pct']:.1f}% ret={m['return_pct']:+.2f}% "
                f"bh50={m['buy_hold_return_pct']:+.2f}% btc_bh={dm.btc_only_bh_return_pct:+.2f}% "
                f"ratio={m['ret_bh_ratio']:.3f} [{gate}]",
                flush=True,
            )
            mode_res[mode_name] = sk
        out[label] = mode_res
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Path B research backtests")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--no-full", action="store_true", help="6m only (skip ~2y full)")
    ap.add_argument("--years", type=float, default=2.5)
    ap.add_argument("--fee", type=float, default=0.001)
    ap.add_argument("--slip", type=float, default=0.0005)
    ap.add_argument("--initial", type=float, default=10_000.0)
    ap.add_argument(
        "--strategies",
        type=str,
        default=",".join(STRATEGY_IDS),
        help="comma-separated strategy ids",
    )
    args = ap.parse_args()
    wanted = {s.strip() for s in args.strategies.split(",") if s.strip()}
    windows: list[tuple[str, float]] = [("6m", 6.0)]
    if not args.no_full:
        windows.append(("full(~2y)", 24.0))

    summary_rows: list[dict] = []
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # --- bb-squeeze ---
    if BB_ID in wanted:
        by_sym = {}
        for sym in ("BTCUSDT",):
            by_sym[sym] = _run_single(
                BB_ID, bb_signals, sym,
                years=args.years, windows=windows, refresh=args.refresh,
                fee=args.fee, slip=args.slip, initial=args.initial, with_stops=True,
            )
        # ETH OOS only if BTC 6m interesting (near gate: ratio>=1.0 or ret close)
        btc6 = by_sym["BTCUSDT"]["6m"]["gate"]
        mb = summarize_path_b(btc6)
        if mb["ret_bh_ratio"] >= 1.0 or mb["gate_pass"]:
            print(f"[{BB_ID}] BTC 6m interesting — running ETH OOS", flush=True)
            by_sym["ETHUSDT"] = _run_single(
                BB_ID, bb_signals, "ETHUSDT",
                years=args.years, windows=windows, refresh=args.refresh,
                fee=args.fee, slip=args.slip, initial=args.initial, with_stops=True,
            )
        rbwm = {}
        for label, _ in windows:
            rbwm[label] = {
                "gate": [by_sym[s][label]["gate"] for s in by_sym],
                "ops": [by_sym[s][label]["ops"] for s in by_sym],
            }
        write_strategy_report(
            strategy_id=BB_ID, rules_md=RULES[BB_ID],
            results_by_window_mode=rbwm, path=RESULTS_DIR / f"{BB_ID}.md",
        )
        for sym in by_sym:
            g = summarize_path_b(by_sym[sym]["6m"]["gate"])
            o = summarize_path_b(by_sym[sym]["6m"]["ops"])
            summary_rows.append({
                "strategy_id": BB_ID, "symbol": sym, "trades": g["trades"],
                "wr": g["win_rate_pct"], "gate_ret": g["return_pct"],
                "ops_ret": o["return_pct"], "bh": g["buy_hold_return_pct"],
                "ratio": g["ret_bh_ratio"],
                "gate": "PASS" if g["gate_pass"] else "FAIL",
            })

    # --- kama-er ---
    if KAMA_ID in wanted:
        by_sym = {}
        for sym in ("BTCUSDT",):
            by_sym[sym] = _run_single(
                KAMA_ID, kama_signals, sym,
                years=args.years, windows=windows, refresh=args.refresh,
                fee=args.fee, slip=args.slip, initial=args.initial,
            )
        btc6 = by_sym["BTCUSDT"]["6m"]["gate"]
        mb = summarize_path_b(btc6)
        if mb["ret_bh_ratio"] >= 1.0 or mb["gate_pass"]:
            print(f"[{KAMA_ID}] BTC 6m interesting — running ETH OOS", flush=True)
            by_sym["ETHUSDT"] = _run_single(
                KAMA_ID, kama_signals, "ETHUSDT",
                years=args.years, windows=windows, refresh=args.refresh,
                fee=args.fee, slip=args.slip, initial=args.initial,
            )
        rbwm = {}
        for label, _ in windows:
            rbwm[label] = {
                "gate": [by_sym[s][label]["gate"] for s in by_sym],
                "ops": [by_sym[s][label]["ops"] for s in by_sym],
            }
        write_strategy_report(
            strategy_id=KAMA_ID, rules_md=RULES[KAMA_ID],
            results_by_window_mode=rbwm, path=RESULTS_DIR / f"{KAMA_ID}.md",
        )
        for sym in by_sym:
            g = summarize_path_b(by_sym[sym]["6m"]["gate"])
            o = summarize_path_b(by_sym[sym]["6m"]["ops"])
            summary_rows.append({
                "strategy_id": KAMA_ID, "symbol": sym, "trades": g["trades"],
                "wr": g["win_rate_pct"], "gate_ret": g["return_pct"],
                "ops_ret": o["return_pct"], "bh": g["buy_hold_return_pct"],
                "ratio": g["ret_bh_ratio"],
                "gate": "PASS" if g["gate_pass"] else "FAIL",
            })

    # --- dual-mom ---
    if DM_ID in wanted:
        dm_out = _run_dual_mom(
            years=args.years, windows=windows, refresh=args.refresh,
            fee=args.fee, slip=args.slip, initial=args.initial,
        )
        rbwm = {}
        for label, _ in windows:
            rbwm[label] = {
                "gate": [dm_out[label]["gate"]],
                "ops": [dm_out[label]["ops"]],
            }
        write_strategy_report(
            strategy_id=DM_ID, rules_md=RULES[DM_ID],
            results_by_window_mode=rbwm, path=RESULTS_DIR / f"{DM_ID}.md",
            extra_notes=["Gate uses primary 50/50 B&H; secondary BTC-only in notes."],
        )
        g = summarize_path_b(dm_out["6m"]["gate"])
        o = summarize_path_b(dm_out["6m"]["ops"])
        summary_rows.append({
            "strategy_id": DM_ID, "symbol": "BTC+ETH", "trades": g["trades"],
            "wr": g["win_rate_pct"], "gate_ret": g["return_pct"],
            "ops_ret": o["return_pct"], "bh": g["buy_hold_return_pct"],
            "ratio": g["ret_bh_ratio"],
            "gate": "PASS" if g["gate_pass"] else "FAIL",
        })

    # --- sma200 ---
    if SMA_ID in wanted:
        by_sym = {}
        for sym in ("BTCUSDT",):
            by_sym[sym] = _run_single(
                SMA_ID, sma_signals, sym,
                years=args.years, windows=windows, refresh=args.refresh,
                fee=args.fee, slip=args.slip, initial=args.initial,
            )
        rbwm = {}
        for label, _ in windows:
            rbwm[label] = {
                "gate": [by_sym[s][label]["gate"] for s in by_sym],
                "ops": [by_sym[s][label]["ops"] for s in by_sym],
            }
        write_strategy_report(
            strategy_id=SMA_ID, rules_md=RULES[SMA_ID],
            results_by_window_mode=rbwm, path=RESULTS_DIR / f"{SMA_ID}.md",
        )
        for sym in by_sym:
            g = summarize_path_b(by_sym[sym]["6m"]["gate"])
            o = summarize_path_b(by_sym[sym]["6m"]["ops"])
            summary_rows.append({
                "strategy_id": SMA_ID, "symbol": sym, "trades": g["trades"],
                "wr": g["win_rate_pct"], "gate_ret": g["return_pct"],
                "ops_ret": o["return_pct"], "bh": g["buy_hold_return_pct"],
                "ratio": g["ret_bh_ratio"],
                "gate": "PASS" if g["gate_pass"] else "FAIL",
            })

    # --- supertrend ---
    if ST_ID in wanted:
        by_sym = {}
        for sym in ("BTCUSDT",):
            by_sym[sym] = _run_single(
                ST_ID, st_signals, sym,
                years=args.years, windows=windows, refresh=args.refresh,
                fee=args.fee, slip=args.slip, initial=args.initial,
            )
        rbwm = {}
        for label, _ in windows:
            rbwm[label] = {
                "gate": [by_sym[s][label]["gate"] for s in by_sym],
                "ops": [by_sym[s][label]["ops"] for s in by_sym],
            }
        write_strategy_report(
            strategy_id=ST_ID, rules_md=RULES[ST_ID],
            results_by_window_mode=rbwm, path=RESULTS_DIR / f"{ST_ID}.md",
        )
        for sym in by_sym:
            g = summarize_path_b(by_sym[sym]["6m"]["gate"])
            o = summarize_path_b(by_sym[sym]["6m"]["ops"])
            summary_rows.append({
                "strategy_id": ST_ID, "symbol": sym, "trades": g["trades"],
                "wr": g["win_rate_pct"], "gate_ret": g["return_pct"],
                "ops_ret": o["return_pct"], "bh": g["buy_hold_return_pct"],
                "ratio": g["ret_bh_ratio"],
                "gate": "PASS" if g["gate_pass"] else "FAIL",
            })

    write_batch_summary(rows=summary_rows, path=RESULTS_DIR / "path-b-gate-summary-6m.md")
    print(f"\nWrote {RESULTS_DIR / 'path-b-gate-summary-6m.md'}", flush=True)


if __name__ == "__main__":
    main()
