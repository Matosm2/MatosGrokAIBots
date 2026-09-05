"""CLI: python -m backtest.sketches [--months 6] [--also-2y] [--refresh]

Runs TV-free offline research sketches (not paper/live).

Dual sizing:
  Mode A (gate): 100% equity when in — PASS/FAIL vs B&H uses this only
  Mode B (ops):  2.5% equity — parallel ops realism column
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from backtest.data import Bar, load_or_fetch
from backtest.sketches import NEW_STRATEGY_IDS, STRATEGY_IDS
from backtest.sketches.daily_adx import STRATEGY_ID as ADX_ID
from backtest.sketches.daily_adx import compute_raw as adx_raw
from backtest.sketches.donchian_spot import STRATEGY_ID as DON_ID
from backtest.sketches.donchian_spot import compute_raw as don_raw
from backtest.sketches.ema20_hold import STRATEGY_ID as EMA20_ID
from backtest.sketches.ema20_hold import compute_raw as ema20_raw
from backtest.sketches.engine import apply_position_gate, run_long_only, slice_result_to_window
from backtest.sketches.htf_pullback import STRATEGY_ID as HTF_ID
from backtest.sketches.htf_pullback import compute_raw as htf_raw
from backtest.sketches.macd_hist import STRATEGY_ID as MACD_ID
from backtest.sketches.macd_hist import compute_raw as macd_raw
from backtest.sketches.report import (
    GATE_SIZE_PCT,
    OPS_SIZE_PCT,
    summarize_sketch,
    write_strategy_report,
    write_summary_gate_table,
)

RESULTS_DIR = Path(__file__).resolve().parent / "results"

RULES = {
    ADX_ID: [
        "Timeframe: **Daily**",
        "Entry: EMA50 > EMA200 AND ADX(14) ≥ 25 AND +DI > −DI",
        "Exit: −DI > +DI OR ADX < 20 OR close < EMA200",
        "State-based entry (hold while conditions allow); pyramiding 0",
    ],
    MACD_ID: [
        "Timeframe: **Daily**",
        "Entry: MACD histogram crosses above 0 AND close > EMA100",
        "Exit: MACD histogram crosses below 0",
        "MACD(12,26,9); pyramiding 0",
    ],
    HTF_ID: [
        "Daily bias: EMA50 > EMA200 on last **fully closed** daily bar (no lookahead)",
        "4h entry: pullback (low ≤ EMA50 within lookback 5) then close crosses back above EMA20 "
        "with close ≥ EMA50, while daily bias bullish",
        "Stop: entry close − 3 × ATR(14) on 4h (bar-close stop)",
        "Exit: stop OR daily bias lost OR 4h close < EMA50",
    ],
    EMA20_ID: [
        "Timeframe: **Daily**",
        "Entry: close > EMA20 AND EMA20 > EMA20[5] (rising EMA20)",
        "Exit: close < EMA20",
        "Optional ADX≥15 filter: **OFF by default**",
        "No EMA50>EMA200 filter",
        "State-based / hold while above; pyramiding 0",
    ],
    DON_ID: [
        "Timeframe: **Daily**",
        "Entry: close > highest high of the **prior 20 bars** (excluding current) — "
        "classic Donchian upper-band breakout",
        "Exit: close < lowest low of the **prior 10 bars** (excluding current)",
        "Spot long-only; pyramiding 0",
    ],
}

SIZING_MODES: list[tuple[str, float]] = [
    ("gate", GATE_SIZE_PCT),
    ("ops", OPS_SIZE_PCT),
]


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc).timestamp() * 1000
    return int(now - months * 30.4375 * 24 * 3600 * 1000)


def _mask_before(flags: list[bool], bars: list[Bar], start_ms: int) -> list[bool]:
    out = list(flags)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            out[i] = False
    return out


def _stops_for_gated(
    buys: list[bool],
    sells: list[bool],
    entry_stop: list[float | None],
) -> list[float | None]:
    stops: list[float | None] = [None] * len(buys)
    frozen: float | None = None
    in_pos = False
    for i in range(len(buys)):
        if buys[i]:
            in_pos = True
            frozen = entry_stop[i]
            stops[i] = frozen
        elif in_pos:
            stops[i] = frozen
            if sells[i]:
                in_pos = False
                frozen = None
    return stops


def _run_daily_dual(
    strategy_id: str,
    raw_fn: Callable,
    symbol: str,
    *,
    years_fetch: float,
    windows: list[tuple[str, float]],
    refresh: bool,
    fee: float,
    slip: float,
    initial: float,
) -> dict[str, dict[str, object]]:
    """Returns {window_label: {"gate": SketchResult, "ops": SketchResult}}."""
    print(f"[{strategy_id}] Loading {symbol} 1d (~{years_fetch:g}y)...", flush=True)
    bars = load_or_fetch(symbol, "1d", years=years_fetch, refresh=refresh)
    raw_long, raw_exit = raw_fn(bars)
    out: dict[str, dict[str, object]] = {}
    for label, months in windows:
        start = _window_start_ms(months)
        masked_long = _mask_before(raw_long, bars, start)
        buys, sells = apply_position_gate(masked_long, raw_exit)
        mode_res: dict[str, object] = {}
        for mode_name, buy_pct in SIZING_MODES:
            res = run_long_only(
                symbol,
                strategy_id,
                bars,
                buys,
                sells,
                initial_equity=initial,
                buy_qty_pct=buy_pct,
                fee_rate=fee,
                slippage_rate=slip,
                window_label=label,
            )
            sliced = slice_result_to_window(res, bars, start, window_label=label)
            m = summarize_sketch(sliced)
            if mode_name == "gate":
                gate = "PASS" if m["gate_pass"] else "FAIL"
            else:
                gate = "—"
            print(
                f"  {symbol} {label} [{mode_name} {buy_pct:g}%]: trades={m['trades']} "
                f"wr={m['win_rate_pct']:.1f}% ret={m['return_pct']:+.2f}% "
                f"bh={m['buy_hold_return_pct']:+.2f}% [{gate}]",
                flush=True,
            )
            mode_res[mode_name] = sliced
        out[label] = mode_res
    return out


def _run_htf_dual(
    symbol: str,
    *,
    years_fetch: float,
    windows: list[tuple[str, float]],
    refresh: bool,
    fee: float,
    slip: float,
    initial: float,
) -> dict[str, dict[str, object]]:
    print(f"[{HTF_ID}] Loading {symbol} 4h+1d (~{years_fetch:g}y)...", flush=True)
    bars_4h = load_or_fetch(symbol, "4h", years=years_fetch, refresh=refresh)
    daily = load_or_fetch(symbol, "1d", years=years_fetch, refresh=refresh)
    raw_long, raw_exit, entry_stop = htf_raw(bars_4h, daily)
    out: dict[str, dict[str, object]] = {}
    for label, months in windows:
        start = _window_start_ms(months)
        masked_long = _mask_before(raw_long, bars_4h, start)
        buys, sells = apply_position_gate(masked_long, raw_exit)
        stops = _stops_for_gated(buys, sells, entry_stop)
        mode_res: dict[str, object] = {}
        for mode_name, buy_pct in SIZING_MODES:
            res = run_long_only(
                symbol,
                HTF_ID,
                bars_4h,
                buys,
                sells,
                stop_prices=stops,
                initial_equity=initial,
                buy_qty_pct=buy_pct,
                fee_rate=fee,
                slippage_rate=slip,
                window_label=label,
            )
            sliced = slice_result_to_window(res, bars_4h, start, window_label=label)
            m = summarize_sketch(sliced)
            gate = "PASS" if m["gate_pass"] else "FAIL" if mode_name == "gate" else "—"
            print(
                f"  {symbol} {label} [{mode_name} {buy_pct:g}%]: trades={m['trades']} "
                f"wr={m['win_rate_pct']:.1f}% ret={m['return_pct']:+.2f}% "
                f"bh={m['buy_hold_return_pct']:+.2f}% [{gate}]",
                flush=True,
            )
            mode_res[mode_name] = sliced
        out[label] = mode_res
    return out


def _accumulate(
    strategy_id: str,
    symbols: list[str],
    runner,
    *,
    years_fetch: float,
    windows: list[tuple[str, float]],
    refresh: bool,
    fee: float,
    slip: float,
    initial: float,
    gate_rows: list[dict],
) -> dict[str, dict[str, list]]:
    """Build results_by_window_mode and append 6m gate rows."""
    by_window_mode: dict[str, dict[str, list]] = {
        lab: {"gate": [], "ops": []} for lab, _ in windows
    }
    for sym in symbols:
        got = runner(
            sym,
            years_fetch=years_fetch,
            windows=windows,
            refresh=refresh,
            fee=fee,
            slip=slip,
            initial=initial,
        )
        for lab, modes in got.items():
            for mode_name, res in modes.items():
                by_window_mode[lab][mode_name].append(res)
            if lab == "6m":
                mg = summarize_sketch(modes["gate"])
                mo = summarize_sketch(modes["ops"])
                gate_rows.append(
                    {
                        "strategy_id": strategy_id,
                        "symbol": sym,
                        "wr": mg["win_rate_pct"],
                        "gate_ret": mg["return_pct"],
                        "ops_ret": mo["return_pct"],
                        "bh": mg["buy_hold_return_pct"],
                        "gate": "PASS" if mg["gate_pass"] else "FAIL",
                    }
                )
    return by_window_mode


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Offline research sketches backtests (dual sizing)")
    p.add_argument("--symbols", default="BTCUSDT,ETHUSDT")
    p.add_argument("--months", type=float, default=6.0, help="Primary window months")
    p.add_argument("--no-2y", action="store_true", help="Skip ~2y window")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--fee", type=float, default=0.001)
    p.add_argument("--slippage", type=float, default=0.0005)
    p.add_argument("--initial", type=float, default=10_000.0)
    p.add_argument(
        "--strategies",
        default=",".join(NEW_STRATEGY_IDS),
        help="Comma-separated strategy ids (default: ema20 + donchian)",
    )
    args = p.parse_args(argv)

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    want = {s.strip() for s in args.strategies.split(",") if s.strip()}
    windows: list[tuple[str, float]] = [("6m", args.months)]
    if not args.no_2y:
        windows.append(("2y", 24.0))

    years_fetch = max(w[1] for w in windows) / 12.0 + 1.0

    gate_rows: list[dict] = []
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    daily_runners = {
        ADX_ID: adx_raw,
        MACD_ID: macd_raw,
        EMA20_ID: ema20_raw,
        DON_ID: don_raw,
    }

    for sid, raw_fn in daily_runners.items():
        if sid not in want:
            continue

        def _runner(sym: str, *, raw=raw_fn, sid_=sid, **kw):
            return _run_daily_dual(sid_, raw, sym, **kw)

        by_wm = _accumulate(
            sid,
            symbols,
            _runner,
            years_fetch=years_fetch,
            windows=windows,
            refresh=args.refresh,
            fee=args.fee,
            slip=args.slippage,
            initial=args.initial,
            gate_rows=gate_rows,
        )
        write_strategy_report(
            strategy_id=sid,
            rules_md=RULES[sid],
            results_by_window_mode=by_wm,
            path=RESULTS_DIR / f"{sid}.md",
        )

    if HTF_ID in want:
        by_wm = _accumulate(
            HTF_ID,
            symbols,
            lambda sym, **kw: _run_htf_dual(sym, **kw),
            years_fetch=years_fetch,
            windows=windows,
            refresh=args.refresh,
            fee=args.fee,
            slip=args.slippage,
            initial=args.initial,
            gate_rows=gate_rows,
        )
        write_strategy_report(
            strategy_id=HTF_ID,
            rules_md=RULES[HTF_ID],
            results_by_window_mode=by_wm,
            path=RESULTS_DIR / f"{HTF_ID}.md",
        )

    summary = RESULTS_DIR / "ema20-donchian-gate-summary-6m.md"
    write_summary_gate_table(rows=gate_rows, path=summary)
    print(f"Wrote summary {summary}", flush=True)
    for r in gate_rows:
        print(
            f"GATE {r['strategy_id']} {r['symbol']}: {r['gate']} "
            f"(WR={r['wr']:.1f}% gate_ret={r['gate_ret']:+.2f}% "
            f"ops_ret={r['ops_ret']:+.2f}% bh={r['bh']:+.2f}%)",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
