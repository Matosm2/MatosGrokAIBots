"""stage5-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (1->5):
1. cti-fast-slow-threshold-v1
2. atrpct-percentile-sma-cross-v1
3. mad-channel-break-rvol-v1
4. vidya-dual-or-close-cross-v1
5. supersmoother-dual-cross-v1

Design Bias: DUAL-SURVIVAL — identical params intended to clear BOTH SOL and BNB (do not retune per coin).
Mandatory sol_smoke + bnb_smoke per strategy: log FAIL reasons; fail smoke -> disqualify cell.
Stop-ladder: BTC -> ETH -> SOL (HARD) -> BNB (HARD).
LEAD gate: last-6m Mode-A return >= 1.2x buy-and-hold (same window). WR info.
Full(~2y) Mode-A + ops 2.5% sizing.
Costs: 0.1%/side + 5 bps. Closed-bar only; pyramiding 0.
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
from backtest.path_b.stage5_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.atrpct_percentile_sma_cross_v1 import (
    AtrPctSmaParams,
    compute_signals as atrpct_signals,
    validate_bnb_smoke as validate_atrpct_bnb_smoke,
    validate_sol_smoke as validate_atrpct_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.cti_fast_slow_threshold_v1 import (
    CtiParams,
    compute_signals as cti_signals,
    validate_bnb_smoke as validate_cti_bnb_smoke,
    validate_sol_smoke as validate_cti_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.mad_channel_break_rvol_v1 import (
    MadChannelParams,
    compute_signals as mad_signals,
    validate_bnb_smoke as validate_mad_bnb_smoke,
    validate_sol_smoke as validate_mad_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.supersmoother_dual_cross_v1 import (
    SuperSmootherParams,
    compute_signals as ss_signals,
    validate_bnb_smoke as validate_ss_bnb_smoke,
    validate_sol_smoke as validate_ss_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.vidya_dual_or_close_cross_v1 import (
    VidyaParams,
    compute_signals as vidya_signals,
    validate_bnb_smoke as validate_vidya_bnb_smoke,
    validate_sol_smoke as validate_vidya_sol_smoke,
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
    sol_smoke: str = "Y"  # Y / FAIL: reason / N/A
    bnb_smoke: str = "Y"  # Y / FAIL: reason / N/A
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
    if 0.9 <= g6.ratio < 1.2:
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
        f"6m={cell.gate_6m}({g6.ratio:.3f}x) ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: cti-fast-slow-threshold-v1
# ---------------------------------------------------------------------------

def run_cti_cells(symbol: str, bars_by_tf: dict[str, list[Bar]], active_keys: set[str] | None = None) -> list[CellResult]:
    sid = "cti-fast-slow-threshold-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (fastL, slowL) in {(10, 20), (20, 40)}; buyTh in {0.3, 0.5}; Mode A & Mode B
    param_grid: list[tuple[str, CtiParams]] = [
        ("mode_a|(20,40)|buy0.5", CtiParams(mode="mode_a", fast_len=20, slow_len=40, buy_th=0.5, sell_th=0.0)),
        ("mode_a|(20,40)|buy0.3", CtiParams(mode="mode_a", fast_len=20, slow_len=40, buy_th=0.3, sell_th=0.0)),
        ("mode_a|(10,20)|buy0.5", CtiParams(mode="mode_a", fast_len=10, slow_len=20, buy_th=0.5, sell_th=0.0)),
        ("mode_a|(10,20)|buy0.3", CtiParams(mode="mode_a", fast_len=10, slow_len=20, buy_th=0.3, sell_th=0.0)),
        ("mode_b|fast20", CtiParams(mode="mode_b", fast_len=20, buy_th=0.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            # Validate smokes
            sol_ok, sol_msg = validate_cti_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_cti_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = cti_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                _finish(cell)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: atrpct-percentile-sma-cross-v1
# ---------------------------------------------------------------------------

def run_atrpct_sma_cells(symbol: str, bars_by_tf: dict[str, list[Bar]], active_keys: set[str] | None = None) -> list[CellResult]:
    sid = "atrpct-percentile-sma-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (f, s) in {(10, 30), (20, 50)}; (lo, hi) in {(25, 85), (30, 100), (40, 80)}; W in {100, 150}
    param_grid: list[tuple[str, AtrPctSmaParams]] = [
        ("mode_a|(20,50)|(25,85)|W100", AtrPctSmaParams(mode="mode_a", fast_len=20, slow_len=50, rank_lo=25.0, rank_hi=85.0, window_w=100)),
        ("mode_a|(20,50)|(30,100)|W100", AtrPctSmaParams(mode="mode_a", fast_len=20, slow_len=50, rank_lo=30.0, rank_hi=100.0, window_w=100)),
        ("mode_a|(20,50)|(40,80)|W100", AtrPctSmaParams(mode="mode_a", fast_len=20, slow_len=50, rank_lo=40.0, rank_hi=80.0, window_w=100)),
        ("mode_a|(20,50)|(25,85)|W150", AtrPctSmaParams(mode="mode_a", fast_len=20, slow_len=50, rank_lo=25.0, rank_hi=85.0, window_w=150)),
        ("mode_a|(10,30)|(25,85)|W100", AtrPctSmaParams(mode="mode_a", fast_len=10, slow_len=30, rank_lo=25.0, rank_hi=85.0, window_w=100)),
        ("mode_a|(10,30)|(30,100)|W100", AtrPctSmaParams(mode="mode_a", fast_len=10, slow_len=30, rank_lo=30.0, rank_hi=100.0, window_w=100)),
        ("mode_b|sma20|(25,85)|W100", AtrPctSmaParams(mode="mode_b", sma_len=20, rank_lo=25.0, rank_hi=85.0, window_w=100)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_atrpct_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_atrpct_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = atrpct_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                _finish(cell)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: mad-channel-break-rvol-v1
# ---------------------------------------------------------------------------

def run_mad_cells(symbol: str, bars_by_tf: dict[str, list[Bar]], active_keys: set[str] | None = None) -> list[CellResult]:
    sid = "mad-channel-break-rvol-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: N in {20, 34}; k in {1.5, 2.0, 2.5}; kr in {1.0, 1.2}; Mode A primary
    param_grid: list[tuple[str, MadChannelParams]] = [
        ("mode_a|N20|k2.0|kr1.0", MadChannelParams(mode="mode_a", channel_n=20, k_mult=2.0, rvol_k=1.0, rvol_filter=True)),
        ("mode_a|N20|k2.0|kr1.2", MadChannelParams(mode="mode_a", channel_n=20, k_mult=2.0, rvol_k=1.2, rvol_filter=True)),
        ("mode_a|N20|k1.5|kr1.0", MadChannelParams(mode="mode_a", channel_n=20, k_mult=1.5, rvol_k=1.0, rvol_filter=True)),
        ("mode_a|N20|k2.5|kr1.0", MadChannelParams(mode="mode_a", channel_n=20, k_mult=2.5, rvol_k=1.0, rvol_filter=True)),
        ("mode_a|N34|k2.0|kr1.0", MadChannelParams(mode="mode_a", channel_n=34, k_mult=2.0, rvol_k=1.0, rvol_filter=True)),
        ("mode_a|N34|k2.0|kr1.2", MadChannelParams(mode="mode_a", channel_n=34, k_mult=2.0, rvol_k=1.2, rvol_filter=True)),
        ("mode_b|N20|k2.0|kr1.0", MadChannelParams(mode="mode_b", channel_n=20, k_mult=2.0, rvol_k=1.0, rvol_filter=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_mad_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_mad_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = mad_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                _finish(cell)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: vidya-dual-or-close-cross-v1
# ---------------------------------------------------------------------------

def run_vidya_cells(symbol: str, bars_by_tf: dict[str, list[Bar]], active_keys: set[str] | None = None) -> list[CellResult]:
    sid = "vidya-dual-or-close-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: Mode A (9,12)x(20,50); slopeMin in {0.0003, 0.0006, 0.0}; Mode B close x VIDYA
    param_grid: list[tuple[str, VidyaParams]] = [
        ("mode_a|(9,12)x(20,50)|slope0.0003", VidyaParams(mode="mode_a", slope_min=0.0003, slope_filter=True)),
        ("mode_a|(9,12)x(20,50)|slope0.0006", VidyaParams(mode="mode_a", slope_min=0.0006, slope_filter=True)),
        ("mode_a|(9,12)x(20,50)|slope_off", VidyaParams(mode="mode_a", slope_min=0.0, slope_filter=False)),
        ("mode_b|vidya20|slope0.0003", VidyaParams(mode="mode_b", slope_min=0.0003, slope_filter=True)),
        ("mode_b|vidya20|slope_off", VidyaParams(mode="mode_b", slope_min=0.0, slope_filter=False)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_vidya_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_vidya_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = vidya_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                _finish(cell)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 5: supersmoother-dual-cross-v1
# ---------------------------------------------------------------------------

def run_supersmoother_cells(symbol: str, bars_by_tf: dict[str, list[Bar]], active_keys: set[str] | None = None) -> list[CellResult]:
    sid = "supersmoother-dual-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: pairs (8, 16), (10, 30), (12, 24); atr_regime_gate off / on (lo=25)
    param_grid: list[tuple[str, SuperSmootherParams]] = [
        ("mode_a|(10,30)|gate_off", SuperSmootherParams(mode="mode_a", fast_len=10, slow_len=30, atr_regime_gate=False)),
        ("mode_a|(10,30)|gate_lo25", SuperSmootherParams(mode="mode_a", fast_len=10, slow_len=30, atr_regime_gate=True, rank_lo=25.0)),
        ("mode_a|(8,16)|gate_off", SuperSmootherParams(mode="mode_a", fast_len=8, slow_len=16, atr_regime_gate=False)),
        ("mode_a|(8,16)|gate_lo25", SuperSmootherParams(mode="mode_a", fast_len=8, slow_len=16, atr_regime_gate=True, rank_lo=25.0)),
        ("mode_a|(12,24)|gate_off", SuperSmootherParams(mode="mode_a", fast_len=12, slow_len=24, atr_regime_gate=False)),
        ("mode_a|(12,24)|gate_lo25", SuperSmootherParams(mode="mode_a", fast_len=12, slow_len=24, atr_regime_gate=True, rank_lo=25.0)),
        ("mode_b|ss30|gate_off", SuperSmootherParams(mode="mode_b", slow_len=30, atr_regime_gate=False)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_ss_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_ss_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = ss_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                _finish(cell)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Stop-Ladder Dispatcher
# ---------------------------------------------------------------------------

def run_strategy_cells(
    strategy_id: str,
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
) -> list[CellResult]:
    if strategy_id == "cti-fast-slow-threshold-v1":
        return run_cti_cells(symbol, bars_by_tf, active_keys=active_keys)
    elif strategy_id == "atrpct-percentile-sma-cross-v1":
        return run_atrpct_sma_cells(symbol, bars_by_tf, active_keys=active_keys)
    elif strategy_id == "mad-channel-break-rvol-v1":
        return run_mad_cells(symbol, bars_by_tf, active_keys=active_keys)
    elif strategy_id == "vidya-dual-or-close-cross-v1":
        return run_vidya_cells(symbol, bars_by_tf, active_keys=active_keys)
    elif strategy_id == "supersmoother-dual-cross-v1":
        return run_supersmoother_cells(symbol, bars_by_tf, active_keys=active_keys)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


def run_stage5_dual_sol_bnb_v1(
    years: float = 2.5,
    refresh: bool = False,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> list[CellResult]:
    """Execute the locked 5-strategy stop-ladder with DUAL-SURVIVAL constraint."""
    all_results: list[CellResult] = []
    active_keys: set[str] | None = None  # None for BTC (run all)

    for idx, symbol in enumerate(symbols):
        print(f"\n==================================================================", flush=True)
        print(f"[{RESEARCH_ID}] Evaluating Symbol {idx+1}/{len(symbols)}: {symbol}", flush=True)
        print(f"==================================================================", flush=True)

        if active_keys is not None and len(active_keys) == 0:
            print(f"[{symbol}] Stop-ladder halted: no active cells promoted from previous symbol.", flush=True)
            continue

        print(f"[{symbol}] Materializing 1h and 4h bars (~{years:g}y)...", flush=True)
        bars_by_tf = materialize_symbol(symbol, tfs=("1h", "4h"), years=years, refresh=refresh)

        sym_results: list[CellResult] = []
        for sid in STRATEGY_IDS:
            print(f"\n--- [{symbol}] Strategy: {sid} ---", flush=True)
            res = run_strategy_cells(sid, symbol, bars_by_tf, active_keys=active_keys)
            sym_results.extend(res)
            all_results.extend(res)

        # Stop-ladder filtering: only cells with gate_6m == "PASS" advance to next symbol
        passed_cells = [
            r for r in sym_results
            if not r.skipped and not r.error and r.gate_6m == "PASS"
        ]
        next_active: set[str] = {f"{r.strategy_id}@{r.tf}@{r.mode_params}" for r in passed_cells}

        print(f"\n[{symbol}] Evaluation Summary: Scored={len(sym_results)}, PASS_6m={len(passed_cells)}", flush=True)
        for r in passed_cells:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            print(f"  -> PROMOTED: {r.strategy_id} @ {r.tf} {r.mode_params} (6m={g6.return_pct:.2f}%, {g6.ratio:.3f}x B&H, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke})", flush=True)

        active_keys = next_active

    return all_results


# ---------------------------------------------------------------------------
# Scoreboard Writer (Markdown + CSV)
# ---------------------------------------------------------------------------

def _row_to_cols(r: CellResult) -> tuple[list[str], list[str]]:
    g6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "gate"), None)
    gf = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
    o6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "ops"), None)
    of = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"), None)

    note_str = "; ".join(r.notes)
    if r.error:
        note_str = f"ERROR: {r.error}"
    elif r.skipped:
        note_str = "Pruned by ladder"

    md_cols = [
        r.symbol,
        r.tf,
        r.mode_params,
        r.sol_smoke,
        r.bnb_smoke,
        r.gate_6m,
        f"{g6.return_pct:.2f}%" if g6 else "—",
        f"{g6.bh_return_pct:.2f}%" if g6 else "—",
        f"{g6.ratio:.3f}x" if g6 else "—",
        f"{g6.win_rate_pct:.1f}%" if g6 else "—",
        str(g6.trades) if g6 else "—",
        r.gate_full,
        f"{gf.ratio:.3f}x" if gf else "—",
        str(gf.trades) if gf else "—",
        f"{o6.return_pct:.2f}%" if o6 else "—",
        f"{of.return_pct:.2f}%" if of else "—",
        note_str,
    ]

    csv_cols = [
        r.symbol,
        r.strategy_id,
        r.tf,
        r.mode_params,
        r.sol_smoke,
        r.bnb_smoke,
        str(g6.trades) if g6 else "",
        f"{g6.win_rate_pct:.1f}" if g6 else "",
        f"{g6.return_pct:.2f}" if g6 else "",
        f"{g6.bh_return_pct:.2f}" if g6 else "",
        f"{g6.ratio:.3f}" if g6 else "",
        r.gate_6m,
        str(gf.trades) if gf else "",
        f"{gf.win_rate_pct:.1f}" if gf else "",
        f"{gf.return_pct:.2f}" if gf else "",
        f"{gf.bh_return_pct:.2f}" if gf else "",
        f"{gf.ratio:.3f}" if gf else "",
        r.gate_full,
        f"{o6.return_pct:.2f}" if o6 else "",
        f"{of.return_pct:.2f}" if of else "",
        note_str,
    ]

    return md_cols, csv_cols


def write_scoreboard(
    results: list[CellResult],
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    output_dir = output_dir or RESULTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / "stage5-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage5-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage5-dual-sol-bnb-v1 scoreboard (DUAL-SURVIVAL: SOL + BNB)",
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
        "- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).",
        "- **Mandatory Smoke Tests:** Both sol_smoke and bnb_smoke are logged per strategy cell.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-4 IDs, no Decycler/ITrend/PVO/P4H, no Roofing, no EMA/RSI, SMA200, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **CTI Fast/Slow (`cti-fast-slow-threshold-v1`):** Pearson correlation vs ideal rising line over L. Defaults (20,40,0.5,0). Fast cross > buyTh, slow cross < sellTh. Sol smoke: no 15m Mode B, dead-bar filter on. BNB smoke: slowL<60 on 4H, identical params.",
        "- **ATR% Percentile SMA Cross (`atrpct-percentile-sma-cross-v1`):** atrPct percentrank regime band + SMAxSMA (10,30)/(20,50) NOT 200. Regime leave exit on. BNB smoke requires rank_lo>=25.",
        "- **Median / MAD Channel Break (`mad-channel-break-rvol-v1`):** Rolling median +/- k*(1.4826*MAD). Mode A breakout (close-beyond only). Light RVOL kr in {1.0, 1.2} on by default for dual smoke.",
        "- **VIDYA Dual Cross (`vidya-dual-or-close-cross-v1`):** Chande VIDYA with locked CMO scale (|CMO|/100). Mode A (9,12)x(20,50). slopeMin ON for BNB smoke.",
        "- **SuperSmoother Dual Cross (`supersmoother-dual-cross-v1`):** 2-pole SuperSmoother fast x slow ONLY (strictly NO High-Pass / != Roofing). Pairs (8,16)/(10,30)/(12,24). Optional Brief-2 atrPct gate.",
        "",
        "## PASS_6m cells (LEAD)",
        "",
    ]

    pass_6m_cells = [r for r in results if not r.skipped and not r.error and r.gate_6m == "PASS"]
    if not pass_6m_cells:
        lines.append("_none_")
    else:
        for r in pass_6m_cells:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}) [sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}]: 6m ret={g.return_pct:.2f}% "
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
            "sol_smoke",
            "bnb_smoke",
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
            "| symbol | tf | mode/params | sol_smoke | bnb_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | "
            "full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |"
        )
        lines.append(
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
        )
        for r in fam:
            md_cols, csv_cols = _row_to_cols(r)
            lines.append(f"| {' | '.join(md_cols)} |")
            csv_rows.append(csv_cols)
        lines.append("")

    lines.append("## Dual-Survival & Ladder Analysis")
    lines.append("")
    lines.append("1. **Stop-Ladder Attrition:**")
    btc_pass = len([r for r in results if r.symbol == "BTCUSDT" and r.gate_6m == "PASS"])
    eth_pass = len([r for r in results if r.symbol == "ETHUSDT" and r.gate_6m == "PASS"])
    sol_pass = len([r for r in results if r.symbol == "SOLUSDT" and r.gate_6m == "PASS"])
    bnb_pass = len([r for r in results if r.symbol == "BNBUSDT" and r.gate_6m == "PASS"])
    lines.append(f"   - BTC PASS_6m: {btc_pass}")
    lines.append(f"   - ETH PASS_6m: {eth_pass}")
    lines.append(f"   - SOL PASS_6m: {sol_pass} (HARD FILTER)")
    lines.append(f"   - BNB PASS_6m: {bnb_pass} (HARD FILTER)")
    lines.append("")
    lines.append("2. **Smoke Outcomes:**")
    lines.append("   - All cells verified against mandatory sol_smoke and bnb_smoke rules.")
    lines.append("   - Dual identical parameter constraint strictly preserved across all symbols.")

    md_content = "\n".join(lines) + "\n"
    md_path.write_text(md_content, encoding="utf-8")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
