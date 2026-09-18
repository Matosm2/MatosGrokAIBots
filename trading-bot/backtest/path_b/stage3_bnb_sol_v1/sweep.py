"""stage3-bnb-sol-v1 harness: Sweep and score five strategies (BTCUSDT -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (1->5):
1. vwma-sma-cross-v1
2. phh-phl-accept-break-v1
3. t3-dual-cross-v1
4. decycler-osc-fast-slow-v1
5. itrend-trigger-v1

LEAD gate: last-6m Mode-A return >= 1.2x buy-and-hold (same window). WR informational.
Also report full(~2y) Mode-A + ops 2.5% sizing.
Costs: 0.1%/side + 5 bps (consistent with prior Path B waves).
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b
from backtest.path_b.stage3_bnb_sol_v1 import (
    DECYCLER_TFS,
    DEFAULT_SYMBOLS,
    ITREND_TFS,
    PHH_PHL_TFS,
    RESEARCH_ID,
    STRATEGY_IDS,
    T3_TFS,
    VWMA_SMA_TFS,
)
from backtest.path_b.stage3_bnb_sol_v1.decycler_osc_fast_slow_v1 import (
    DecyclerOscParams,
    compute_signals as decycler_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.itrend_trigger_v1 import (
    ITrendParams,
    compute_signals as itrend_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.phh_phl_accept_break_v1 import (
    PhhPhlParams,
    compute_signals as phh_phl_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.t3_dual_cross_v1 import (
    T3Params,
    compute_signals as t3_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.vwma_sma_cross_v1 import (
    VwmaSmaParams,
    compute_signals as vwma_sma_signals,
)

GATE_MULT = 1.2
FEE = 0.001
SLIP = 0.0005
INITIAL = 10_000.0
RESULTS_DIR = Path(__file__).resolve().parent / "results"

SIZING = (("gate", GATE_SIZE_PCT), ("ops", OPS_SIZE_PCT))
WINDOWS: tuple[tuple[str, float], ...] = (("6m", 6.0), ("full(~2y)", 24.0))


@dataclass
class WindowModeMetrics:
    window: str
    mode: str
    size_pct: float
    return_pct: float = 0.0
    bh_return_pct: float = 0.0
    ratio: float = 0.0
    win_rate_pct: float = 0.0
    trades: int = 0
    wins: int = 0
    losses: int = 0
    max_drawdown_pct: float = 0.0
    gate: str = "—"


@dataclass
class CellResult:
    symbol: str
    strategy_id: str
    tf: str
    mode_params: str
    gate_6m: str = "FAIL"
    gate_full: str = "FAIL"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    error: str = ""
    skipped: bool = False


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc).timestamp() * 1000
    return int(now - months * 30.4375 * 24 * 3600 * 1000)


def _mask_buys_before(buys: list[bool], bars: list[Bar], start_ms: int) -> list[bool]:
    out = list(buys)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            out[i] = False
    return out


def _ratio(ret: float, bh: float) -> float:
    if bh != 0:
        r = ret / bh
    else:
        r = float("inf") if ret > 0 else 0.0
    if r == float("inf"):
        return 999.0
    if r == float("-inf"):
        return -999.0
    return r


def _gate_label(trades: int, ret: float, bh: float) -> str:
    return "PASS" if (trades > 0 and ret >= GATE_MULT * bh) else "FAIL"


def _eval_windows(
    symbol: str,
    strategy_id: str,
    bars: list[Bar],
    buys_full: list[bool],
    sells_full: list[bool],
    stop_prices: list[float | None] | None = None,
) -> list[WindowModeMetrics]:
    out: list[WindowModeMetrics] = []
    for label, months in WINDOWS:
        start = _window_start_ms(months)
        buys = _mask_buys_before(buys_full, bars, start)
        for mode_name, buy_pct in SIZING:
            res = run_long_only(
                symbol,
                strategy_id,
                bars,
                buys,
                sells_full,
                stop_prices=stop_prices,
                initial_equity=INITIAL,
                buy_qty_pct=buy_pct,
                fee_rate=FEE,
                slippage_rate=SLIP,
                window_label=label,
            )
            sliced = slice_result_to_window(res, bars, start, window_label=label)
            m = summarize_path_b(sliced)
            ret = float(m["return_pct"])
            bh = float(m["buy_hold_return_pct"])
            ratio = _ratio(ret, bh)
            gate = _gate_label(int(m["trades"]), ret, bh) if mode_name == "gate" else "—"
            out.append(
                WindowModeMetrics(
                    window=label,
                    mode=mode_name,
                    size_pct=buy_pct,
                    return_pct=ret,
                    bh_return_pct=bh,
                    ratio=ratio,
                    win_rate_pct=float(m["win_rate_pct"]),
                    trades=int(m["trades"]),
                    wins=int(m["wins"]),
                    losses=int(m["losses"]),
                    max_drawdown_pct=float(m["max_drawdown_pct"]),
                    gate=gate,
                )
            )
    return out


def _finish(cell: CellResult) -> CellResult:
    if cell.error or cell.skipped or not cell.metrics:
        return cell
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate

    # Add notes for near-miss (0.9x <= ratio < 1.2x)
    if g6.ratio >= 0.9 and g6.ratio < 1.2:
        cell.notes.append(f"Near-miss 6m ({g6.ratio:.2f}x B&H)")
    if cell.symbol == "SOLUSDT":
        cell.notes.append("SOL hard filter")
    elif cell.symbol == "BNBUSDT":
        cell.notes.append("BNB hard filter")

    return cell


def _print_cell(cell: CellResult) -> None:
    if cell.skipped:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> N/A ({'; '.join(cell.notes)})", flush=True)
        return
    if cell.error:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> ERROR {cell.error}", flush=True)
        return
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    print(
        f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> "
        f"6m={cell.gate_6m}({g6.ratio:.3f}x) ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# 1. VWMA × SMA Cross
def run_vwma_sma_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "vwma-sma-cross-v1"
    for tf in VWMA_SMA_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: same-len in {10, 20, 34, 50}; fast/slow in {(10, 20), (20, 50)}; mode_a and mode_b
        configs = [
            ("mode_a", 10, 10, "mode_a|(10,10)"),
            ("mode_a", 20, 20, "mode_a|(20,20)"),
            ("mode_a", 34, 34, "mode_a|(34,34)"),
            ("mode_a", 50, 50, "mode_a|(50,50)"),
            ("mode_a", 10, 20, "mode_a|(10,20)"),
            ("mode_a", 20, 50, "mode_a|(20,50)"),
            ("mode_b", 10, 10, "mode_b|(10,10)"),
            ("mode_b", 20, 20, "mode_b|(20,20)"),
            ("mode_b", 10, 20, "mode_b|(10,20)"),
        ]
        for mode, v_len, s_len, tag in configs:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = VwmaSmaParams(vwma_len=v_len, sma_len=s_len, mode=mode)
                buys, sells, stops = vwma_sma_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 2. PHH / PHL Accept Break
def run_phh_phl_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "phh-phl-accept-break-v1"
    for tf in PHH_PHL_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: Mode A vs B, RVOL k in {0.0 (off), 1.0, 1.5}
        params_sweep = [
            ("mode_a", 0.0, "mode_a|rvol_off"),
            ("mode_a", 1.0, "mode_a|rvol1.0"),
            ("mode_a", 1.5, "mode_a|rvol1.5"),
            ("mode_b", 0.0, "mode_b|rvol_off"),
            ("mode_b", 1.0, "mode_b|rvol1.0"),
            ("mode_b", 1.5, "mode_b|rvol1.5"),
        ]
        for mode, rvol, tag in params_sweep:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = PhhPhlParams(mode=mode, rvol_k=rvol)
                buys, sells, stops = phh_phl_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 3. Tillson T3 Dual Cross
def run_t3_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "t3-dual-cross-v1"
    for tf in T3_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: pairs in {(5, 15), (8, 21), (10, 30)}, v_factor in {0.7, 0.5}
        configs = [
            (5, 15, 0.7, "mode_a|(5,15)|vf0.7"),
            (8, 21, 0.7, "mode_a|(8,21)|vf0.7"),
            (10, 30, 0.7, "mode_a|(10,30)|vf0.7"),
            (5, 15, 0.5, "mode_a|(5,15)|vf0.5"),
            (8, 21, 0.5, "mode_a|(8,21)|vf0.5"),
            (10, 30, 0.5, "mode_a|(10,30)|vf0.5"),
        ]
        for f_len, s_len, vf, tag in configs:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = T3Params(fast_len=f_len, slow_len=s_len, v_factor=vf, mode="mode_a")
                buys, sells, stops = t3_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 4. Decycler Osc Fast × Slow
def run_decycler_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "decycler-osc-fast-slow-v1"
    for tf in DECYCLER_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: (Pfast, Pslow) in {(100, 125), (50, 63), (40, 50)}, Mode A and Mode B
        configs = [
            ("mode_a", 100, 125, "mode_a|(100,125)"),
            ("mode_a", 50, 63, "mode_a|(50,63)"),
            ("mode_a", 40, 50, "mode_a|(40,50)"),
            ("mode_b", 100, 125, "mode_b|(100,125)"),
            ("mode_b", 50, 63, "mode_b|(50,63)"),
            ("mode_b", 40, 50, "mode_b|(40,50)"),
        ]
        for mode, pf, ps, tag in configs:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = DecyclerOscParams(p_fast=pf, p_slow=ps, k_fast=1.2, k_slow=1.0, mode=mode)
                buys, sells, stops = decycler_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 5. ITrend × Trigger
def run_itrend_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "itrend-trigger-v1"
    for tf in ITREND_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: alpha locked 0.07 first, plus optional 0.05 and 0.10
        configs = [
            (0.07, "mode_a|alpha0.07"),
            (0.05, "mode_a|alpha0.05"),
            (0.10, "mode_a|alpha0.10"),
        ]
        for a, tag in configs:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = ITrendParams(alpha=a, mode="mode_a")
                buys, sells, stops = itrend_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_strategy_on_symbol(strategy_id: str, symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    if strategy_id == "vwma-sma-cross-v1":
        return run_vwma_sma_cells(symbol, bars_by_tf)
    if strategy_id == "phh-phl-accept-break-v1":
        return run_phh_phl_cells(symbol, bars_by_tf)
    if strategy_id == "t3-dual-cross-v1":
        return run_t3_cells(symbol, bars_by_tf)
    if strategy_id == "decycler-osc-fast-slow-v1":
        return run_decycler_cells(symbol, bars_by_tf)
    if strategy_id == "itrend-trigger-v1":
        return run_itrend_cells(symbol, bars_by_tf)
    raise ValueError(f"Unknown strategy_id: {strategy_id}")


def _reconstruct_and_eval_cell(
    symbol: str,
    parent_cell: CellResult,
    sym_bars: dict[str, list[Bar]],
) -> CellResult:
    sid = parent_cell.strategy_id
    tf = parent_cell.tf
    params_tag = parent_cell.mode_params
    cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=params_tag)

    if tf not in sym_bars:
        cell.error = f"Missing TF {tf}"
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"
        return cell

    bars = sym_bars[tf]
    try:
        if sid == "vwma-sma-cross-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            pair_str = parts[1].strip("()")
            v_len, s_len = [int(x) for x in pair_str.split(",")]
            p = VwmaSmaParams(vwma_len=v_len, sma_len=s_len, mode=mode)
            buys, sells, stops = vwma_sma_signals(bars, p)
        elif sid == "phh-phl-accept-break-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            rvol = 0.0 if parts[1] == "rvol_off" else float(parts[1].replace("rvol", ""))
            p = PhhPhlParams(mode=mode, rvol_k=rvol)
            buys, sells, stops = phh_phl_signals(bars, p)
        elif sid == "t3-dual-cross-v1":
            parts = params_tag.split("|")
            pair_str = parts[1].strip("()")
            f_len, s_len = [int(x) for x in pair_str.split(",")]
            vf = float(parts[2].replace("vf", ""))
            p = T3Params(fast_len=f_len, slow_len=s_len, v_factor=vf, mode="mode_a")
            buys, sells, stops = t3_signals(bars, p)
        elif sid == "decycler-osc-fast-slow-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            pair_str = parts[1].strip("()")
            pf, ps = [int(x) for x in pair_str.split(",")]
            p = DecyclerOscParams(p_fast=pf, p_slow=ps, k_fast=1.2, k_slow=1.0, mode=mode)
            buys, sells, stops = decycler_signals(bars, p)
        elif sid == "itrend-trigger-v1":
            parts = params_tag.split("|")
            a = float(parts[1].replace("alpha", ""))
            p = ITrendParams(alpha=a, mode="mode_a")
            buys, sells, stops = itrend_signals(bars, p)
        else:
            raise ValueError(f"Unknown sid: {sid}")

        cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
        _finish(cell)
    except Exception as exc:  # noqa: BLE001
        cell.error = repr(exc)
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"

    return cell


def run_stage3_bnb_sol_v1(
    *,
    years: float = 2.5,
    refresh: bool = False,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> list[CellResult]:
    """Execute locked encode order (1->5) on BTC first, then stop-ladder ETH -> SOL -> BNB."""
    needed_tfs = tuple(dict.fromkeys([*VWMA_SMA_TFS, *PHH_PHL_TFS, *T3_TFS, *DECYCLER_TFS, *ITREND_TFS, "5m", "1d"]))

    # Step 1: Materialize BTC
    print(f"\n==================== MATERIALIZING BTCUSDT ====================", flush=True)
    btc_bars = materialize_symbol("BTCUSDT", tfs=needed_tfs, years=years, refresh=refresh)

    all_results: list[CellResult] = []

    # Execute BTC across all 5 strategies in locked encode order
    for sid in STRATEGY_IDS:
        print(f"\n==================== SCORING BTC: {sid} ====================", flush=True)
        res = run_strategy_on_symbol(sid, "BTCUSDT", btc_bars)
        all_results.extend(res)

    # Check for PASS_6m cells on BTC
    btc_pass_cells = [r for r in all_results if r.symbol == "BTCUSDT" and r.gate_6m == "PASS"]
    print(f"\n==================== BTC RUN COMPLETE: {len(btc_pass_cells)} PASS_6m CELLS ====================", flush=True)
    for c in btc_pass_cells:
        g6 = next(m for m in c.metrics if m.window == "6m" and m.mode == "gate")
        print(f"  BTC PASS: {c.strategy_id} @ {c.tf} {c.mode_params} ratio={g6.ratio:.3f}x n={g6.trades}", flush=True)

    # OOS Stop-Ladder: ETH -> SOL (HARD FILTER) -> BNB (HARD FILTER)
    ladder_symbols = ("ETHUSDT", "SOLUSDT", "BNBUSDT")
    active_passing_cells = list(btc_pass_cells)

    for oos_sym in ladder_symbols:
        if not active_passing_cells:
            print(f"\n[STOP-LADDER] No active passing cells remaining for {oos_sym}. Stop-ladder terminated.", flush=True)
            break

        print(f"\n==================== MATERIALIZING {oos_sym} ====================", flush=True)
        sym_bars = materialize_symbol(oos_sym, tfs=needed_tfs, years=years, refresh=refresh)

        next_passing_cells = []
        for parent_cell in active_passing_cells:
            sid = parent_cell.strategy_id
            tf = parent_cell.tf
            params_tag = parent_cell.mode_params
            print(f"\n[STOP-LADDER] Evaluating {oos_sym} on {sid} @ {tf} {params_tag} ...", flush=True)

            cell = _reconstruct_and_eval_cell(oos_sym, parent_cell, sym_bars)
            _print_cell(cell)
            all_results.append(cell)

            if cell.gate_6m == "PASS":
                next_passing_cells.append(parent_cell)
            else:
                ratio_str = "ERR"
                if cell.metrics:
                    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
                    ratio_str = f"{g6.ratio:.3f}x"
                print(f"  [STOP-LADDER] {oos_sym} FAILED ({ratio_str}) for {sid} @ {tf} {params_tag} (Stopped ladder)", flush=True)

        active_passing_cells = next_passing_cells

    return all_results


def _fmt(val: float | None, digits: int = 2, suffix: str = "") -> str:
    if val is None:
        return "—"
    return f"{val:.{digits}f}{suffix}"


def _get_metric(cell: CellResult, window: str, mode: str) -> WindowModeMetrics | None:
    for m in cell.metrics:
        if m.window == window and m.mode == mode:
            return m
    return None


def _format_cell_row(cell: CellResult) -> tuple[list[str], list[str]]:
    """Return (markdown_cols, csv_cols) for a cell."""
    g6 = _get_metric(cell, "6m", "gate")
    gf = _get_metric(cell, "full(~2y)", "gate")
    o6 = _get_metric(cell, "6m", "ops")
    of = _get_metric(cell, "full(~2y)", "ops")

    notes_str = "; ".join(cell.notes)

    # Markdown columns:
    # symbol, tf, mode/params, 6m PASS, 6m_ret%, 6m_bh%, xB&H, 6m_wr%, 6m_n, full PASS, full_xB&H, full_n, ops_6m%, ops_full%, notes
    p6_str = f"**{cell.gate_6m}**" if cell.gate_6m == "PASS" else cell.gate_6m
    pf_str = f"**{cell.gate_full}**" if cell.gate_full == "PASS" else cell.gate_full

    md_cols = [
        cell.symbol,
        cell.tf,
        f"`{cell.mode_params}`",
        p6_str,
        _fmt(g6.return_pct if g6 else None, 2, "%"),
        _fmt(g6.bh_return_pct if g6 else None, 2, "%"),
        _fmt(g6.ratio if g6 else None, 3, "×"),
        _fmt(g6.win_rate_pct if g6 else None, 1, "%"),
        str(g6.trades) if g6 else "—",
        pf_str,
        _fmt(gf.ratio if gf else None, 3, "×"),
        str(gf.trades) if gf else "—",
        _fmt(o6.return_pct if o6 else None, 2, "%"),
        _fmt(of.return_pct if of else None, 2, "%"),
        notes_str,
    ]

    csv_cols = [
        cell.symbol,
        cell.strategy_id,
        cell.tf,
        cell.mode_params,
        str(g6.trades) if g6 else "",
        _fmt(g6.win_rate_pct if g6 else None, 1),
        _fmt(g6.return_pct if g6 else None, 2),
        _fmt(g6.bh_return_pct if g6 else None, 2),
        _fmt(g6.ratio if g6 else None, 3),
        cell.gate_6m,
        str(gf.trades) if gf else "",
        _fmt(gf.win_rate_pct if gf else None, 1),
        _fmt(gf.return_pct if gf else None, 2),
        _fmt(gf.bh_return_pct if gf else None, 2),
        _fmt(gf.ratio if gf else None, 3),
        cell.gate_full,
        _fmt(o6.return_pct if o6 else None, 2),
        _fmt(of.return_pct if of else None, 2),
        notes_str,
    ]

    return md_cols, csv_cols


def write_scoreboard(results: list[CellResult], path: Path | None = None) -> tuple[Path, Path]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = path or (RESULTS_DIR / "stage3-bnb-sol-v1-scoreboard.md")
    csv_path = md_path.with_suffix(".csv")

    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**",
        "",
        "## Scoring Criteria",
        "",
        f"- **LEAD gate:** last-6m Mode-A return >= **{GATE_MULT}×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.",
        f"- **Also reported:** full(~2y) Mode-A + ops **{OPS_SIZE_PCT}%** sizing.",
        f"- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **{GATE_SIZE_PCT:.0f}%** equity.",
        "- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.",
        "- **Closed-bar only;** UTC wall-clock hour reset for PHH/PHL; long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1/stage2 IDs, no ALMA/Roofing/CG/CMO-zero/PWH, no EMA/RSI, SMA200, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **T3 (`t3-dual-cross-v1`):** vFactor locked at `0.7` (lead) and `0.5`; Pairs locked at `(5,15)`, `(8,21)`, `(10,30)`. Tillson nested GDEMA formula.",
        "- **ITrend (`itrend-trigger-v1`):** alpha locked at `0.07` lead (simplified Pine form); optional `0.05` and `0.10` after BTC smoke. Trigger = 2*ITrend - ITrend[2].",
        "- **Decycler (`decycler-osc-fast-slow-v1`):** K locked at `(1.2, 1.0)`; Pairs locked at `(100,125)`, `(50,63)`, `(40,50)`. 2-pole HighPass Decycler Oscillator.",
        "- **VWMA × SMA (`vwma-sma-cross-v1`):** Lengths in `{10, 20, 34, 50}` same-len, plus `(10,20)` and `(20,50)` fast/slow. Mode A cross & Mode B state.",
        "- **PHH/PHL (`phh-phl-accept-break-v1`):** Prior UTC clock-hour H/L. Mode A accept-break, Mode B break+retest. RVOL k in `{off, 1.0, 1.5}`.",
        "",
        "## PASS_6m cells (LEAD)",
        "",
    ]

    pass_6m_cells = [r for r in results if r.gate_6m == "PASS"]
    if not pass_6m_cells:
        lines.append("_none_")
    else:
        for r in pass_6m_cells:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}): 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f}x wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f}x n={gf.trades}"
            )

    lines.append("")
    lines.append("## All Scored Cells by Strategy")
    lines.append("")

    # CSV headers
    csv_rows: list[list[str]] = [
        [
            "symbol",
            "strategy_id",
            "tf",
            "mode_params",
            "n_6m",
            "wr_6m_pct",
            "mode_a_ret_6m_pct",
            "bh_ret_6m_pct",
            "ratio_bh_6m",
            "pass_6m",
            "n_full",
            "wr_full_pct",
            "mode_a_ret_full_pct",
            "bh_ret_full_pct",
            "ratio_bh_full",
            "pass_full",
            "ops_ret_6m_pct",
            "ops_ret_full_pct",
            "notes",
        ]
    ]

    for sid in STRATEGY_IDS:
        fam = [r for r in results if r.strategy_id == sid]
        if not fam:
            continue
        lines.append(f"### {sid}")
        lines.append("")
        lines.append(
            "| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | "
            "full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |"
        )
        lines.append(
            "|--------|----|-------------|---------|---------|--------|------|--------|------|"
            "-----------|-----------|--------|---------|-----------|-------|"
        )

        for r in fam:
            if r.skipped:
                note_str = "; ".join(r.notes)
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | N/A | — | — | — | — | — | N/A | — | — | — | — | {note_str} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params,
                    "", "", "", "", "", "N/A",
                    "", "", "", "", "", "N/A",
                    "", "", note_str,
                ])
                continue

            if r.error:
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | ERR | — | — | — | — | — | ERR | — | — | — | — | {r.error} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params,
                    "", "", "", "", "", "ERR",
                    "", "", "", "", "", "ERR",
                    "", "", r.error,
                ])
                continue

            md_cols, csv_cols = _format_cell_row(r)
            lines.append("| " + " | ".join(md_cols) + " |")
            csv_rows.append(csv_cols)

        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
