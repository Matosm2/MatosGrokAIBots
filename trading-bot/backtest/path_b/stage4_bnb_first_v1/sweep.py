"""stage4-bnb-first-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (1->5):
1. rvol-pivot-structure-break-v1
2. emv-zero-rvol-atr-gate-v1
3. pvo-gate-sma-mom-v1
4. p4h-hl-accept-break-v1
5. zlema-sma-cross-v1

Design Bias: BNB-survival-FIRST + SOL-dense.
Mandatory BNB smoke per strategy: log FAIL reasons; fail smoke -> do not promote that param cell.
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
from backtest.path_b.stage4_bnb_first_v1 import (
    DEFAULT_SYMBOLS,
    EMV_TFS,
    P4H_TFS,
    PVO_TFS,
    RESEARCH_ID,
    RVOL_PIVOT_TFS,
    STRATEGY_IDS,
    ZLEMA_TFS,
)
from backtest.path_b.stage4_bnb_first_v1.emv_zero_rvol_atr_gate_v1 import (
    EmvGateParams,
    SYMBOL_DIVISORS,
    compute_signals as emv_signals,
)
from backtest.path_b.stage4_bnb_first_v1.p4h_hl_accept_break_v1 import (
    P4HParams,
    compute_signals as p4h_signals,
)
from backtest.path_b.stage4_bnb_first_v1.pvo_gate_sma_mom_v1 import (
    PvoMomParams,
    compute_signals as pvo_signals,
)
from backtest.path_b.stage4_bnb_first_v1.rvol_pivot_structure_break_v1 import (
    RvolPivotParams,
    compute_signals as rvol_pivot_signals,
)
from backtest.path_b.stage4_bnb_first_v1.zlema_sma_cross_v1 import (
    ZlemaSmaParams,
    compute_signals as zlema_signals,
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
    bnb_smoke: str = "Y"  # Y / N / N/A
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
        f"6m={cell.gate_6m}({g6.ratio:.3f}x) ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [BNB_smoke={cell.bnb_smoke}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# BNB Smoke Validation Helpers
# ---------------------------------------------------------------------------

def validate_rvol_pivot_bnb_smoke(tf: str, params: RvolPivotParams) -> tuple[bool, str]:
    """Check BNB smoke constraints for rvol-pivot-structure-break-v1."""
    if tf == "15m":
        return False, "15m TF rejected on BNB smoke (requires 1H+)"
    if params.rvol_k < 1.5:
        return False, f"RVOL k={params.rvol_k} < 1.5 floor on BNB"
    if not params.atr_filter:
        return False, "ATR% range floor is OFF"
    if params.mode == "mode_b" and params.lookback_l < 10:
        return False, f"Mode B lookback L={params.lookback_l} < 10 (noise flood)"
    return True, "SMOKE_PASS"


def validate_emv_bnb_smoke(tf: str, params: EmvGateParams, symbol: str) -> tuple[bool, str]:
    """Check BNB smoke constraints for emv-zero-rvol-atr-gate-v1."""
    if tf == "15m":
        return False, "15m TF rejected on BNB smoke (requires 1H+)"
    if params.rvol_k < 1.5:
        return False, f"RVOL k={params.rvol_k} < 1.5 floor on BNB"
    if params.atr_pct_min < 0.002:
        return False, f"ATR% min={params.atr_pct_min} < 0.002 floor on BNB"
    if symbol == "BNBUSDT" and params.divisor > 10_000_000.0:
        return False, f"BNB divisor {params.divisor} unscaled (expected 1e7)"
    return True, "SMOKE_PASS"


def validate_pvo_bnb_smoke(tf: str, params: PvoMomParams) -> tuple[bool, str]:
    """Check BNB smoke constraints for pvo-gate-sma-mom-v1."""
    if tf == "15m":
        return False, "15m TF rejected on BNB smoke (requires 1H+)"
    if not params.exit_on_gate_loss:
        return False, "exit_on_gate_loss=False (mandatory True for BNB smoke)"
    if params.sma_len > 34:
        return False, f"SMA len={params.sma_len} > 34 bound"
    return True, "SMOKE_PASS"


def validate_p4h_bnb_smoke(tf: str, params: P4HParams) -> tuple[bool, str]:
    """Check BNB smoke constraints for p4h-hl-accept-break-v1."""
    if params.rvol_k < 1.5:
        return False, f"RVOL k={params.rvol_k} < 1.5 floor on BNB"
    if tf == "15m":
        return False, "15m TF rejected for BNB ladder (1H preferred)"
    if params.min_range_pct < 0.002:
        return False, "min_range_pct < 0.002 floor on BNB"
    return True, "SMOKE_PASS"


def validate_zlema_bnb_smoke(tf: str, params: ZlemaSmaParams) -> tuple[bool, str]:
    """Check BNB smoke constraints for zlema-sma-cross-v1."""
    if tf == "15m":
        return False, "15m TF rejected on BNB smoke (requires 1H+)"
    if params.rvol_k < 1.2:
        return False, f"RVOL k={params.rvol_k} < 1.2 floor required on BNB"
    return True, "SMOKE_PASS"


# ---------------------------------------------------------------------------
# Strategy Run Functions
# ---------------------------------------------------------------------------

# 1. RVOL + Pivot Structure Break
def run_rvol_pivot_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "rvol-pivot-structure-break-v1"
    for tf in RVOL_PIVOT_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: k in {1.2, 1.5, 2.0}; volLen in {20, 50}; mode_a vs mode_b
        configs = [
            # Mode A (pivot lb=rb=2)
            ("mode_a", 1.2, 20, 2, 10, True, "mode_a|k1.2|v20|p2"),
            ("mode_a", 1.5, 20, 2, 10, True, "mode_a|k1.5|v20|p2"),
            ("mode_a", 2.0, 20, 2, 10, True, "mode_a|k2.0|v20|p2"),
            ("mode_a", 1.5, 50, 2, 10, True, "mode_a|k1.5|v50|p2"),
            ("mode_a", 1.5, 20, 3, 10, True, "mode_a|k1.5|v20|p3"),
            # Mode B (lookback close break)
            ("mode_b", 1.2, 20, 2, 5, True, "mode_b|k1.2|v20|L5"),
            ("mode_b", 1.5, 20, 2, 10, True, "mode_b|k1.5|v20|L10"),
            ("mode_b", 2.0, 20, 2, 20, True, "mode_b|k2.0|v20|L20"),
            ("mode_b", 1.5, 50, 2, 10, True, "mode_b|k1.5|v50|L10"),
        ]
        for mode, k, vlen, plen, l_len, atr_flt, tag in configs:
            p = RvolPivotParams(
                mode=mode,
                rvol_k=k,
                vol_len=vlen,
                pivot_len=plen,
                lookback_l=l_len,
                atr_filter=atr_flt,
            )
            # Check BNB smoke if symbol is BNBUSDT
            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_rvol_pivot_bnb_smoke(tf, p)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=tag,
                bnb_smoke="Y" if smoke_ok else "N",
            )
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = rvol_pivot_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as e:
                cell.error = str(e)
            results.append(cell)
            _print_cell(cell)
    return results


# 2. EMV Zero-Cross + RVOL/ATR% Gates
def run_emv_gate_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "emv-zero-rvol-atr-gate-v1"
    divisor = SYMBOL_DIVISORS.get(symbol, 10_000_000.0)

    for tf in EMV_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: eomLen in {10, 14, 20}; k in {1.0, 1.5}; atrPctMin in {0.0, 0.002, 0.004}
        configs = [
            ("mode_a", 14, 1.0, 0.002, "mode_a|len14|k1.0|atr0.002"),
            ("mode_a", 14, 1.5, 0.002, "mode_a|len14|k1.5|atr0.002"),
            ("mode_a", 14, 1.5, 0.004, "mode_a|len14|k1.5|atr0.004"),
            ("mode_a", 10, 1.5, 0.002, "mode_a|len10|k1.5|atr0.002"),
            ("mode_a", 20, 1.5, 0.002, "mode_a|len20|k1.5|atr0.002"),
            ("mode_a", 14, 1.0, 0.0, "mode_a|len14|k1.0|atr_off"),
            ("mode_b", 14, 1.5, 0.002, "mode_b|len14|k1.5|atr0.002"),
        ]
        for mode, eom_l, k, atr_pct, tag in configs:
            p = EmvGateParams(
                mode=mode,
                eom_len=eom_l,
                divisor=divisor,
                rvol_k=k,
                atr_pct_min=atr_pct,
            )
            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_emv_bnb_smoke(tf, p, symbol)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=tag,
                bnb_smoke="Y" if smoke_ok else "N",
            )
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = emv_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as e:
                cell.error = str(e)
            results.append(cell)
            _print_cell(cell)
    return results


# 3. PVO Gate + SMA Momentum
def run_pvo_mom_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "pvo-gate-sma-mom-v1"
    for tf in PVO_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: gate pvo>0 vs pvo>sig; len in {10, 20, 34}; Mode A vs B; exit_on_gate_loss
        configs = [
            ("mode_a", "pvo_pos", 10, True, "mode_a|pvo_pos|len10|exit_loss_on"),
            ("mode_a", "pvo_pos", 20, True, "mode_a|pvo_pos|len20|exit_loss_on"),
            ("mode_a", "pvo_pos", 34, True, "mode_a|pvo_pos|len34|exit_loss_on"),
            ("mode_a", "pvo_sig", 20, True, "mode_a|pvo_sig|len20|exit_loss_on"),
            ("mode_b", "pvo_pos", 20, True, "mode_b|pvo_pos|len20|exit_loss_on"),
            ("mode_a", "pvo_pos", 20, False, "mode_a|pvo_pos|len20|exit_loss_off"),
            ("mode_a", "pvo_pos", 50, True, "mode_a|pvo_pos|len50|exit_loss_on"),  # exploratory non-BNB
        ]
        for mode, gvar, slen, exit_loss, tag in configs:
            p = PvoMomParams(
                mode=mode,
                gate_variant=gvar,
                sma_len=slen,
                exit_on_gate_loss=exit_loss,
            )
            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_pvo_bnb_smoke(tf, p)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=tag,
                bnb_smoke="Y" if smoke_ok else "N",
            )
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = pvo_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as e:
                cell.error = str(e)
            results.append(cell)
            _print_cell(cell)
    return results


# 4. Prior-4H H/L Accept-Break
def run_p4h_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "p4h-hl-accept-break-v1"
    for tf in P4H_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: Mode A vs B; RVOL k in {0.0, 1.2, 1.5}; one_trade_per_bucket
        configs = [
            ("mode_a", 1.5, True, "mode_a|k1.5|1trade"),
            ("mode_a", 1.2, True, "mode_a|k1.2|1trade"),
            ("mode_a", 0.0, True, "mode_a|k_off|1trade"),
            ("mode_b", 1.5, True, "mode_b|k1.5|1trade"),
            ("mode_a", 1.5, False, "mode_a|k1.5|multi"),
        ]
        for mode, k, one_t, tag in configs:
            p = P4HParams(
                mode=mode,
                rvol_k=k,
                one_trade_per_bucket=one_t,
            )
            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_p4h_bnb_smoke(tf, p)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=tag,
                bnb_smoke="Y" if smoke_ok else "N",
            )
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = p4h_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as e:
                cell.error = str(e)
            results.append(cell)
            _print_cell(cell)
    return results


# 5. ZLEMA x SMA Cross
def run_zlema_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "zlema-sma-cross-v1"
    for tf in ZLEMA_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: (lenZ, lenS) in {(10, 30), (20, 50), (34, 89)}; RVOL k in {0.0, 1.2, 1.5}; Mode A vs B
        configs = [
            ("mode_a", 20, 50, 1.2, "mode_a|(20,50)|k1.2"),
            ("mode_a", 20, 50, 1.5, "mode_a|(20,50)|k1.5"),
            ("mode_a", 10, 30, 1.2, "mode_a|(10,30)|k1.2"),
            ("mode_a", 34, 89, 1.2, "mode_a|(34,89)|k1.2"),
            ("mode_a", 20, 50, 0.0, "mode_a|(20,50)|k_off"),
            ("mode_b", 20, 50, 1.2, "mode_b|(20,50)|k1.2"),
        ]
        for mode, zlen, slen, k, tag in configs:
            p = ZlemaSmaParams(
                mode=mode,
                zlema_len=zlen,
                sma_len=slen,
                rvol_k=k,
            )
            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_zlema_bnb_smoke(tf, p)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=tag,
                bnb_smoke="Y" if smoke_ok else "N",
            )
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = zlema_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as e:
                cell.error = str(e)
            results.append(cell)
            _print_cell(cell)
    return results


# ---------------------------------------------------------------------------
# Stop-Ladder Coordinator
# ---------------------------------------------------------------------------

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
        if sid == "rvol-pivot-structure-break-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            k = float(parts[1].replace("k", ""))
            vlen = int(parts[2].replace("v", ""))
            if mode == "mode_a":
                plen = int(parts[3].replace("p", ""))
                p = RvolPivotParams(mode=mode, rvol_k=k, vol_len=vlen, pivot_len=plen, atr_filter=True)
            else:
                L = int(parts[3].replace("L", ""))
                p = RvolPivotParams(mode=mode, rvol_k=k, vol_len=vlen, lookback_l=L, atr_filter=True)

            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_rvol_pivot_bnb_smoke(tf, p)
            cell.bnb_smoke = "Y" if smoke_ok else "N"
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                return cell
            buys, sells, stops = rvol_pivot_signals(bars, p)

        elif sid == "emv-zero-rvol-atr-gate-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            eom_len = int(parts[1].replace("len", ""))
            k = float(parts[2].replace("k", ""))
            atr_pct = 0.0 if parts[3] == "atr_off" else float(parts[3].replace("atr", ""))
            divisor = SYMBOL_DIVISORS.get(symbol, 10_000_000.0)
            p = EmvGateParams(mode=mode, eom_len=eom_len, divisor=divisor, rvol_k=k, atr_pct_min=atr_pct)

            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_emv_bnb_smoke(tf, p, symbol)
            cell.bnb_smoke = "Y" if smoke_ok else "N"
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                return cell
            buys, sells, stops = emv_signals(bars, p)

        elif sid == "pvo-gate-sma-mom-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            gvar = parts[1]
            slen = int(parts[2].replace("len", ""))
            exit_loss = (parts[3] == "exit_loss_on")
            p = PvoMomParams(mode=mode, gate_variant=gvar, sma_len=slen, exit_on_gate_loss=exit_loss)

            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_pvo_bnb_smoke(tf, p)
            cell.bnb_smoke = "Y" if smoke_ok else "N"
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                return cell
            buys, sells, stops = pvo_signals(bars, p)

        elif sid == "p4h-hl-accept-break-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            k = 0.0 if parts[1] == "k_off" else float(parts[1].replace("k", ""))
            one_t = (parts[2] == "1trade")
            p = P4HParams(mode=mode, rvol_k=k, one_trade_per_bucket=one_t)

            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_p4h_bnb_smoke(tf, p)
            cell.bnb_smoke = "Y" if smoke_ok else "N"
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                return cell
            buys, sells, stops = p4h_signals(bars, p)

        elif sid == "zlema-sma-cross-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            pair_str = parts[1].strip("()")
            zlen, slen = [int(x) for x in pair_str.split(",")]
            k = 0.0 if parts[2] == "k_off" else float(parts[2].replace("k", ""))
            p = ZlemaSmaParams(mode=mode, zlema_len=zlen, sma_len=slen, rvol_k=k)

            smoke_ok, smoke_reason = (True, "SMOKE_PASS")
            if symbol == "BNBUSDT":
                smoke_ok, smoke_reason = validate_zlema_bnb_smoke(tf, p)
            cell.bnb_smoke = "Y" if smoke_ok else "N"
            if symbol == "BNBUSDT" and not smoke_ok:
                cell.skipped = True
                cell.notes.append(f"BNB_smoke FAIL: {smoke_reason}")
                return cell
            buys, sells, stops = zlema_signals(bars, p)
        else:
            raise ValueError(f"Unknown sid: {sid}")

        cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
        _finish(cell)
    except Exception as exc:  # noqa: BLE001
        cell.error = repr(exc)
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"

    return cell


def run_strategy_on_symbol(strategy_id: str, symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    if strategy_id == "rvol-pivot-structure-break-v1":
        return run_rvol_pivot_cells(symbol, bars_by_tf)
    if strategy_id == "emv-zero-rvol-atr-gate-v1":
        return run_emv_gate_cells(symbol, bars_by_tf)
    if strategy_id == "pvo-gate-sma-mom-v1":
        return run_pvo_mom_cells(symbol, bars_by_tf)
    if strategy_id == "p4h-hl-accept-break-v1":
        return run_p4h_cells(symbol, bars_by_tf)
    if strategy_id == "zlema-sma-cross-v1":
        return run_zlema_cells(symbol, bars_by_tf)
    raise ValueError(f"Unknown strategy_id: {strategy_id}")


def run_stage4_bnb_first_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    *,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    """Execute locked encode order (1->5) on BTC first, then stop-ladder ETH -> SOL -> BNB."""
    needed_tfs = tuple(dict.fromkeys([*RVOL_PIVOT_TFS, *EMV_TFS, *PVO_TFS, *P4H_TFS, *ZLEMA_TFS, "15m", "1h", "4h", "5m", "1d"]))

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
                    g6 = next((m for m in cell.metrics if m.window == "6m" and m.mode == "gate"), None)
                    if g6:
                        ratio_str = f"{g6.ratio:.3f}x"
                print(f"  [STOP-LADDER] {oos_sym} FAILED ({ratio_str}) for {sid} @ {tf} {params_tag} (Stopped ladder)", flush=True)

        active_passing_cells = next_passing_cells

    return all_results


# ---------------------------------------------------------------------------
# Scoreboard Generator
# ---------------------------------------------------------------------------

def _format_cell_row(r: CellResult) -> tuple[list[str], list[str]]:
    g6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "gate"), None)
    gf = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
    o6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "ops"), None)
    of = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"), None)

    note_str = "; ".join(r.notes) if r.notes else ""

    p6_str = f"**{r.gate_6m}**" if r.gate_6m == "PASS" else r.gate_6m
    pf_str = f"**{r.gate_full}**" if r.gate_full == "PASS" else r.gate_full

    md_cols = [
        r.symbol,
        r.tf,
        f"`{r.mode_params}`",
        r.bnb_smoke,
        p6_str,
        f"{g6.return_pct:.2f}%" if g6 else "—",
        f"{g6.bh_return_pct:.2f}%" if g6 else "—",
        f"{g6.ratio:.3f}×" if g6 else "—",
        f"{g6.win_rate_pct:.1f}%" if g6 else "—",
        str(g6.trades) if g6 else "—",
        pf_str,
        f"{gf.ratio:.3f}×" if gf else "—",
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

    md_path = output_dir / "stage4-bnb-first-v1-scoreboard.md"
    csv_path = output_dir / "stage4-bnb-first-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage4-bnb-first-v1 scoreboard (BNB-survival-FIRST)",
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
        "- **Mandatory BNB smoke test:** Each strategy must satisfy BNB smoke constraints before parameter cells are promoted on BNB.",
        "- **Closed-bar only;** UTC wall-clock hour reset for P4H; long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-3 IDs, no ALMA/T3/VWMA/PHH/PWH/Decycler/ITrend, no EMA/RSI, SMA200, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **RVOL Pivot Structure (`rvol-pivot-structure-break-v1`):** RVOL volLen in {20, 50}, k in {1.2, 1.5, 2.0}. Mode A confirmed pivots (lb=rb=2,3); Mode B close > close[L] (L in {5, 10, 20}). BNB smoke requires k>=1.5, ATR% floor, 1H+.",
        "- **EMV Gate (`emv-zero-rvol-atr-gate-v1`):** Divisor locked per symbol (BTC 1e7, ETH 1e7, SOL 1e8, BNB 1e7). eomLen in {10, 14, 20}. RVOL and ATR% participation gates. BNB smoke requires k>=1.5, atrPctMin>=0.002, 1H+.",
        "- **PVO Gate (`pvo-gate-sma-mom-v1`):** PVO(12, 26, 9) participation gate + SMA momentum (len in {10, 20, 34}, len!=200). Exit on gate loss mandatory for BNB smoke.",
        "- **Prior-4H H/L (`p4h-hl-accept-break-v1`):** Prior UTC 4H bucket via session-reset var trackers (no request.security). RVOL on by default for BNB (k>=1.5). 1H preferred for BNB.",
        "- **ZLEMA x SMA (`zlema-sma-cross-v1`):** Canonical lag-compensation ZLEMA (NOT EC gain form) x SMA. Pairs in {(10,30), (20,50), (34,89)}. RVOL>=1.2 required on BNB smoke/ladder.",
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
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}) [BNB_smoke={r.bnb_smoke}]: 6m ret={g.return_pct:.2f}% "
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
            "| symbol | tf | mode/params | BNB_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | "
            "full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |"
        )
        lines.append(
            "|--------|----|-------------|-----------|---------|---------|--------|------|--------|------|"
            "-----------|-----------|--------|---------|-----------|-------|"
        )

        for r in fam:
            if r.skipped:
                note_str = "; ".join(r.notes)
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | {r.bnb_smoke} | N/A | — | — | — | — | — | N/A | — | — | — | — | {note_str} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params, r.bnb_smoke,
                    "", "", "", "", "", "N/A",
                    "", "", "", "", "", "N/A",
                    "", "", note_str,
                ])
                continue

            if r.error:
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | {r.bnb_smoke} | ERR | — | — | — | — | — | ERR | — | — | — | — | {r.error} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params, r.bnb_smoke,
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
