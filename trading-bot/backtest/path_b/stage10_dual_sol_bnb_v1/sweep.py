"""stage10-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (exactly 4 + optional 5th DEMA last):
1. tii-midline-fifty-cross-v1
2. rainbow-osc-zero-cross-v1
3. dorsey-relvol-midline-fifty-v1
4. tcf-plus-sign-flip-v1
5. dema-fast-slow-cross-v1

Design Bias: DUAL SOL+BNB + DENSITY (anti stage7 ER tiny-n, stage8 PGO thin n=9). Identical params SOL+BNB.
TINY-N POLICY (critical): BTC Mode-A n <= 5 on 6m -> FAIL that cell even if xB&H >= 1.2; flag n approx 9 (6..10) as thin.
Mandatory sol_smoke + bnb_smoke per strategy: log FAIL reasons; fail smoke -> disqualify cell.
SOL-after-ETH retention checks: evaluate trade density, zero-flips, impulse response before declaring fail.
Stop-ladder: BTC -> ETH -> SOL (HARD) -> BNB (HARD).
LEAD gate: last-6m Mode-A return >= 1.2x buy-and-hold (same window) AND n > 5 on BTC. WR info.
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
from backtest.path_b.stage10_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.dema_fast_slow_cross_v1 import (
    DemaCrossParams,
    compute_signals as dema_signals,
    validate_bnb_smoke as validate_dema_bnb_smoke,
    validate_sol_smoke as validate_dema_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.dorsey_relvol_midline_fifty_v1 import (
    DorseyRelVolParams,
    compute_signals as relvol_signals,
    validate_bnb_smoke as validate_relvol_bnb_smoke,
    validate_sol_smoke as validate_relvol_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.rainbow_osc_zero_cross_v1 import (
    RainbowOscParams,
    compute_signals as ro_signals,
    validate_bnb_smoke as validate_ro_bnb_smoke,
    validate_sol_smoke as validate_ro_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.tcf_plus_sign_flip_v1 import (
    TcfSignFlipParams,
    compute_signals as tcf_signals,
    validate_bnb_smoke as validate_tcf_bnb_smoke,
    validate_sol_smoke as validate_tcf_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.tii_midline_fifty_cross_v1 import (
    TiiMidlineParams,
    compute_signals as tii_signals,
    validate_bnb_smoke as validate_tii_bnb_smoke,
    validate_sol_smoke as validate_tii_sol_smoke,
)

GATE_MULT = 1.2
TINY_N_THRESHOLD = 5  # BTC Mode-A n <= 5 -> FAIL cell even if xB&H >= 1.2
THIN_N_LOWER = 6
THIN_N_UPPER = 10     # Flag n approx 9 as thin (6..10)
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
    sol_retention_note: str = "—"  # Retention diagnostic (especially after ETH pass)
    tiny_n_kill: bool = False
    thin_n_flag: bool = False
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


def _gate_label(symbol: str, trades: int, ret: float, bh: float, window: str) -> tuple[str, bool, bool]:
    """Return (gate_label, tiny_n_kill, thin_n_flag).
    
    Tiny-n policy: on BTCUSDT 6m Mode-A, if trades <= TINY_N_THRESHOLD, FAIL even if ret >= 1.2*bh.
    Also flag n in [6..10] as thin.
    """
    if trades <= 0:
        return "FAIL", False, False
    
    passes_mult = ret >= GATE_MULT * bh
    tiny_kill = False
    thin_flag = False

    if symbol == "BTCUSDT" and window == "6m":
        if trades <= TINY_N_THRESHOLD:
            tiny_kill = passes_mult
            return "FAIL", tiny_kill, False
        if THIN_N_LOWER <= trades <= THIN_N_UPPER:
            thin_flag = True

    return ("PASS" if passes_mult else "FAIL"), False, thin_flag


def _eval_windows(
    symbol: str,
    strategy_id: str,
    bars: list[Bar],
    buys_full: list[bool],
    sells_full: list[bool],
    stop_prices: list[float | None] | None = None,
) -> tuple[list[WindowModeMetrics], bool, bool]:
    out: list[WindowModeMetrics] = []
    cell_tiny_kill = False
    cell_thin_flag = False
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
            n_trades = int(m["trades"])

            if mode_name == "gate":
                gate, tiny_kill, thin_flag = _gate_label(symbol, n_trades, ret, bh, label)
                if label == "6m":
                    if tiny_kill:
                        cell_tiny_kill = True
                    if thin_flag:
                        cell_thin_flag = True
            else:
                gate = "—"

            out.append(
                WindowModeMetrics(
                    window=label,
                    mode=mode_name,
                    size_pct=buy_pct,
                    return_pct=ret,
                    bh_return_pct=bh,
                    ratio=ratio,
                    win_rate_pct=float(m["win_rate_pct"]),
                    trades=n_trades,
                    wins=int(m["wins"]),
                    losses=int(m["losses"]),
                    max_drawdown_pct=float(m["max_drawdown_pct"]),
                    gate=gate,
                )
            )
    return out, cell_tiny_kill, cell_thin_flag


def _finish(cell: CellResult, eth_cell: CellResult | None = None) -> CellResult:
    if cell.error or cell.skipped or not cell.metrics:
        return cell
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate

    if cell.tiny_n_kill:
        cell.notes.append(f"TINY-N KILL (BTC 6m n={g6.trades} <= {TINY_N_THRESHOLD} despite {g6.ratio:.2f}x B&H)")
    elif cell.thin_n_flag:
        cell.notes.append(f"THIN-N FLAG (BTC 6m n={g6.trades} in thin band [6..10])")

    # Add notes for near-miss (0.9x <= ratio < 1.2x)
    if 0.9 <= g6.ratio < 1.2:
        cell.notes.append(f"Near-miss 6m ({g6.ratio:.2f}x B&H)")
    if cell.symbol == "SOLUSDT":
        cell.notes.append("SOL hard filter")
        # Retention check relative to ETH
        if eth_cell and eth_cell.metrics:
            eth_g6 = next(m for m in eth_cell.metrics if m.window == "6m" and m.mode == "gate")
            if eth_g6.trades > 0 and g6.trades == 0:
                cell.sol_retention_note = "RETENTION FAIL: 0 SOL trades vs ETH trades"
            elif eth_g6.trades > 0 and g6.trades < 0.5 * eth_g6.trades:
                cell.sol_retention_note = f"RETENTION WARN: trade density collapsed ({g6.trades} SOL vs {eth_g6.trades} ETH)"
            else:
                cell.sol_retention_note = f"RETENTION OK: {g6.trades} trades (ETH={eth_g6.trades})"
        else:
            if g6.trades == 0:
                cell.sol_retention_note = "RETENTION FAIL: 0 trades (under-trading / over-gate)"
            else:
                cell.sol_retention_note = f"RETENTION EVAL: {g6.trades} trades (no ETH predecessor)"
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
    tiny_tag = " [TINY-N KILL]" if cell.tiny_n_kill else (" [THIN-N]" if cell.thin_n_flag else "")
    print(
        f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> "
        f"6m={cell.gate_6m}({g6.ratio:.3f}x){tiny_tag} ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}, sol_retention={cell.sol_retention_note}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: tii-midline-fifty-cross-v1
# ---------------------------------------------------------------------------

def run_tii_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "tii-midline-fifty-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, TiiMidlineParams]] = [
        ("mode_a|(60,30)", TiiMidlineParams(mode="mode_a", major=60, minor=30)),
        ("mode_a|(40,20)", TiiMidlineParams(mode="mode_a", major=40, minor=20)),
        ("mode_a|(50,25)", TiiMidlineParams(mode="mode_a", major=50, minor=25)),
        ("mode_b|(60,30,ob80)", TiiMidlineParams(mode="mode_b", major=60, minor=30)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_tii_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_tii_bnb_smoke(p, tf)
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

            if not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = tii_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                eth_cell = eth_results.get(cell_key) if eth_results else None
                cell = _finish(cell, eth_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: rainbow-osc-zero-cross-v1
# ---------------------------------------------------------------------------

def run_ro_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "rainbow-osc-zero-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, RainbowOscParams]] = [
        ("mode_a|(p2,d10)", RainbowOscParams(mode="mode_a", p=2, depth=10)),
        ("mode_a|(p2,d8)", RainbowOscParams(mode="mode_a", p=2, depth=8)),
        ("mode_a|(p3,d10)", RainbowOscParams(mode="mode_a", p=3, depth=10)),
        ("mode_b|(p2,d10,rb38)", RainbowOscParams(mode="mode_b", p=2, depth=10, rb_thr=38.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_ro_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_ro_bnb_smoke(p, tf)
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

            if not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = ro_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                eth_cell = eth_results.get(cell_key) if eth_results else None
                cell = _finish(cell, eth_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: dorsey-relvol-midline-fifty-v1
# ---------------------------------------------------------------------------

def run_relvol_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "dorsey-relvol-midline-fifty-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, DorseyRelVolParams]] = [
        ("mode_a|(10,14)", DorseyRelVolParams(mode="mode_a", stdev_len=10, avg_len=14)),
        ("mode_a|(8,14)", DorseyRelVolParams(mode="mode_a", stdev_len=8, avg_len=14)),
        ("mode_a|(14,14)", DorseyRelVolParams(mode="mode_a", stdev_len=14, avg_len=14)),
        ("mode_a|(10,10)", DorseyRelVolParams(mode="mode_a", stdev_len=10, avg_len=10)),
        ("mode_b|(10,14,os40_ob60)", DorseyRelVolParams(mode="mode_b", stdev_len=10, avg_len=14)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_relvol_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_relvol_bnb_smoke(p, tf)
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

            if not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = relvol_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                eth_cell = eth_results.get(cell_key) if eth_results else None
                cell = _finish(cell, eth_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: tcf-plus-sign-flip-v1
# ---------------------------------------------------------------------------

def run_tcf_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "tcf-plus-sign-flip-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, TcfSignFlipParams]] = [
        ("mode_a|(N35)", TcfSignFlipParams(mode="mode_a", length=35)),
        ("mode_a|(N25)", TcfSignFlipParams(mode="mode_a", length=25)),
        ("mode_a|(N20)", TcfSignFlipParams(mode="mode_a", length=20)),
        ("mode_b|(N35)", TcfSignFlipParams(mode="mode_b", length=35)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_tcf_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_tcf_bnb_smoke(p, tf)
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

            if not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = tcf_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                eth_cell = eth_results.get(cell_key) if eth_results else None
                cell = _finish(cell, eth_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 5: dema-fast-slow-cross-v1
# ---------------------------------------------------------------------------

def run_dema_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "dema-fast-slow-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, DemaCrossParams]] = [
        ("mode_a|(10,30)", DemaCrossParams(mode="mode_a", fast_len=10, slow_len=30)),
        ("mode_a|(5,35)", DemaCrossParams(mode="mode_a", fast_len=5, slow_len=35)),
        ("mode_a|(8,21)", DemaCrossParams(mode="mode_a", fast_len=8, slow_len=21)),
        ("mode_a|(12,26)", DemaCrossParams(mode="mode_a", fast_len=12, slow_len=26)),
        ("mode_b|(close,30)", DemaCrossParams(mode="mode_b", fast_len=10, slow_len=30)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_dema_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_dema_bnb_smoke(p, tf)
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

            if not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = dema_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                eth_cell = eth_results.get(cell_key) if eth_results else None
                cell = _finish(cell, eth_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Unified Runner: Stop-Ladder BTC -> ETH -> SOL -> BNB
# ---------------------------------------------------------------------------

def run_strategy_cells(
    strategy_id: str,
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    if strategy_id == "tii-midline-fifty-cross-v1":
        return run_tii_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "rainbow-osc-zero-cross-v1":
        return run_ro_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "dorsey-relvol-midline-fifty-v1":
        return run_relvol_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "tcf-plus-sign-flip-v1":
        return run_tcf_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "dema-fast-slow-cross-v1":
        return run_dema_cells(symbol, bars_by_tf, active_keys, eth_results)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


def run_stage10_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Stop-ladder tracking: cells that pass BTC -> ETH -> SOL -> BNB
    active_keys: set[str] | None = None
    eth_results_by_key: dict[str, CellResult] = {}

    for symbol in symbols:
        print(f"\n{'='*70}\n[stage10-dual-sol-bnb-v1] Evaluating Symbol: {symbol}\n{'='*70}", flush=True)

        sym_bars_loaded = False
        bars_by_tf: dict[str, list[Bar]] = {}

        def _get_bars() -> dict[str, list[Bar]]:
            nonlocal sym_bars_loaded, bars_by_tf
            if not sym_bars_loaded:
                print(f"[{symbol}] Materializing 1h and 4h bars (~{years:g}y)...", flush=True)
                bars_by_tf = materialize_symbol(symbol, tfs=("1h", "4h"), years=years, refresh=refresh)
                sym_bars_loaded = True
            return bars_by_tf

        sym_results: list[CellResult] = []

        for sid in STRATEGY_IDS:
            param_grid_keys = {
                "tii-midline-fifty-cross-v1": ["mode_a|(60,30)", "mode_a|(40,20)", "mode_a|(50,25)", "mode_b|(60,30,ob80)"],
                "rainbow-osc-zero-cross-v1": ["mode_a|(p2,d10)", "mode_a|(p2,d8)", "mode_a|(p3,d10)", "mode_b|(p2,d10,rb38)"],
                "dorsey-relvol-midline-fifty-v1": ["mode_a|(10,14)", "mode_a|(8,14)", "mode_a|(14,14)", "mode_a|(10,10)", "mode_b|(10,14,os40_ob60)"],
                "tcf-plus-sign-flip-v1": ["mode_a|(N35)", "mode_a|(N25)", "mode_a|(N20)", "mode_b|(N35)"],
                "dema-fast-slow-cross-v1": ["mode_a|(10,30)", "mode_a|(5,35)", "mode_a|(8,21)", "mode_a|(12,26)", "mode_b|(close,30)"],
            }[sid]

            for tf in tfs:
                for desc in param_grid_keys:
                    cell_key = f"{sid}@{tf}@{desc}"
                    if active_keys is not None and cell_key not in active_keys:
                        res_cell = CellResult(
                            symbol=symbol,
                            strategy_id=sid,
                            tf=tf,
                            mode_params=desc,
                            sol_smoke="Y",
                            bnb_smoke="Y",
                            sol_retention_note="—",
                            skipped=True,
                            notes=["Pruned by stop-ladder (BTC PASS_6m required)" if symbol == "ETHUSDT" else ("Pruned by stop-ladder (ETH PASS_6m required)" if symbol == "SOLUSDT" else "Pruned by stop-ladder (SOL PASS_6m required)")],
                        )
                        sym_results.append(res_cell)
                        all_results.append(res_cell)
                        _print_cell(res_cell)
                    else:
                        bars = _get_bars()
                        res = run_strategy_cells(
                            sid,
                            symbol,
                            bars,
                            active_keys={cell_key},
                            eth_results=eth_results_by_key if symbol == "SOLUSDT" else None,
                        )
                        sym_results.extend(res)
                        all_results.extend(res)

        if symbol == "ETHUSDT":
            for r in sym_results:
                cell_key = f"{r.strategy_id}@{r.tf}@{r.mode_params}"
                eth_results_by_key[cell_key] = r

        # Stop-ladder filtering: only cells with gate_6m == "PASS" advance to next symbol
        passed_cells = [
            r for r in sym_results
            if not r.skipped and not r.error and r.gate_6m == "PASS"
        ]
        next_active: set[str] = {f"{r.strategy_id}@{r.tf}@{r.mode_params}" for r in passed_cells}

        print(f"\n[{symbol}] Evaluation Summary: Scored={len(sym_results)}, PASS_6m={len(passed_cells)}", flush=True)
        for r in passed_cells:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            print(f"  -> PROMOTED: {r.strategy_id} @ {r.tf} {r.mode_params} (6m={g6.return_pct:.2f}%, {g6.ratio:.3f}x B&H, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, sol_retention={r.sol_retention_note})", flush=True)

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

    note_str = "; ".join(r.notes) if r.notes else "—"
    if r.error:
        note_str = f"ERROR: {r.error}"
    elif r.skipped:
        note_str = "Pruned by ladder"

    md_cols = [
        f"`{r.symbol}`",
        f"`{r.strategy_id}`",
        f"`{r.tf}`",
        f"`{r.mode_params}`",
        f"`{r.sol_smoke}`",
        f"`{r.bnb_smoke}`",
        f"`{r.sol_retention_note}`",
        str(g6.trades) if g6 else "—",
        f"{g6.win_rate_pct:.1f}%" if g6 else "—",
        f"{g6.return_pct:+.2f}%" if g6 else "—",
        f"{g6.bh_return_pct:+.2f}%" if g6 else "—",
        f"{g6.ratio:.3f}×" if g6 else "—",
        f"**{r.gate_6m}**" if r.gate_6m == "PASS" else r.gate_6m,
        str(gf.trades) if gf else "—",
        f"{gf.win_rate_pct:.1f}%" if gf else "—",
        f"{gf.return_pct:+.2f}%" if gf else "—",
        f"{gf.bh_return_pct:+.2f}%" if gf else "—",
        f"{gf.ratio:.3f}×" if gf else "—",
        f"**{r.gate_full}**" if r.gate_full == "PASS" else r.gate_full,
        f"{o6.return_pct:+.2f}%" if o6 else "—",
        f"{of.return_pct:+.2f}%" if of else "—",
        note_str,
    ]

    csv_cols = [
        r.symbol,
        r.strategy_id,
        r.tf,
        r.mode_params,
        r.sol_smoke,
        r.bnb_smoke,
        r.sol_retention_note,
        str(g6.trades) if g6 else "",
        f"{g6.win_rate_pct:.2f}" if g6 else "",
        f"{g6.return_pct:.4f}" if g6 else "",
        f"{g6.bh_return_pct:.4f}" if g6 else "",
        f"{g6.ratio:.4f}" if g6 else "",
        r.gate_6m,
        str(gf.trades) if gf else "",
        f"{gf.win_rate_pct:.2f}" if gf else "",
        f"{gf.return_pct:.4f}" if gf else "",
        f"{gf.bh_return_pct:.4f}" if gf else "",
        f"{gf.ratio:.4f}" if gf else "",
        r.gate_full,
        f"{o6.return_pct:.4f}" if o6 else "",
        f"{of.return_pct:.4f}" if of else "",
        note_str,
    ]

    return md_cols, csv_cols


def write_scoreboard(
    results: list[CellResult],
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    output_dir = output_dir or RESULTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / "stage10-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage10-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage10-dual-sol-bnb-v1 scoreboard (DUAL SOL+BNB survival + density: SOL + BNB)",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**",
        "",
        "## Scoring Criteria",
        "",
        f"- **LEAD gate:** last-6m Mode-A return >= **{GATE_MULT}×** B&H (same window) with n > {TINY_N_THRESHOLD} on BTC -> `PASS_6m Y/N`. WR informational.",
        f"- **TINY-N POLICY:** BTC Mode-A n <= {TINY_N_THRESHOLD} on 6m -> FAIL cell even if xB&H >= {GATE_MULT} (over-gated / under-specified). Also flag n in [{THIN_N_LOWER}..{THIN_N_UPPER}] as thin.",
        f"- **Also reported:** full(~2y) Mode-A + ops **{OPS_SIZE_PCT}%** sizing.",
        f"- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **{GATE_SIZE_PCT:.0f}%** equity.",
        "- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.",
        "- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).",
        "- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-9 IDs, no ER-gate clones, no Super Passband/RWI/Reverse EMA/PGO, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Trend Intensity Index (`tii-midline-fifty-cross-v1`):** SMA-deviation intensity midline-50 cross. (60,30) preferred; (40,20), (50,25). Mode A 50-cross; Mode B 80-cross.",
        "- **Rainbow Oscillator (`rainbow-osc-zero-cross-v1`):** Widner recursive-SMA consensus zero-cross. p=2 depth=10 preferred; (2,8), (3,10). Mode A zero-cross; Mode B RB-filtered.",
        "- **Dorsey Relative Volatility Index (`dorsey-relvol-midline-fifty-v1`):** Stdev-direction midline-50 cross. (10,14) preferred; (8,14), (14,14), (10,10). Mode A 50-cross; Mode B 60/40.",
        "- **Trend Continuation Factor (`tcf-plus-sign-flip-v1`):** Pee +TCF sign polarity. N=35 preferred; 25, 20. Mode A +TCF zero flip; Mode B dual cross.",
        "- **Double EMA Fast×Slow (`dema-fast-slow-cross-v1`):** Mulloy DEMA fast×slow cross. (10,30) preferred; (5,35), (8,21), (12,26). Mode A fast×slow cross; Mode B close×slow.",
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
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}) [sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, sol_retention={r.sol_retention_note}]: 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f}x wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f}x n={gf.trades}"
            )

    lines.append("")
    lines.append("## All Scored Cells by Strategy")
    lines.append("")

    csv_rows: list[list[str]] = [
        [
            "symbol",
            "strategy_id",
            "tf",
            "mode_params",
            "sol_smoke",
            "bnb_smoke",
            "sol_retention_note",
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

    current_sid: str | None = None
    for r in results:
        if r.strategy_id != current_sid:
            current_sid = r.strategy_id
            lines.append(f"### `{current_sid}`")
            lines.append("")
            lines.append("| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |")
            lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")

        md_cols, c_cols = _row_to_cols(r)
        lines.append("| " + " | ".join(md_cols) + " |")
        csv_rows.append(c_cols)

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
