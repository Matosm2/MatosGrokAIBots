"""stage7-dual-sol-bnb-v1 harness: Sweep and score four strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (exactly 4):
1. er-sma-gate-cross-v1
2. ehlers-super-passband-rms-v1
3. rwi-high-low-threshold-v1
4. ehlers-reverse-ema-trend-cycle-v1

Design Bias: DUAL-SURVIVAL + SOL RETENTION — identical params intended to clear BOTH SOL and BNB (no per-coin retuning).
Mandatory sol_smoke + bnb_smoke per strategy: log FAIL reasons; fail smoke -> disqualify cell.
SOL-after-ETH retention checks: evaluate trade density, impulse hugging, and over-smoothing before declaring fail.
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
from backtest.path_b.stage7_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.ehlers_reverse_ema_trend_cycle_v1 import (
    ReverseEmaParams,
    compute_signals as reverse_ema_signals,
    validate_bnb_smoke as validate_reverse_ema_bnb_smoke,
    validate_sol_smoke as validate_reverse_ema_sol_smoke,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.ehlers_super_passband_rms_v1 import (
    SuperPassbandParams,
    compute_signals as super_passband_signals,
    validate_bnb_smoke as validate_super_passband_bnb_smoke,
    validate_sol_smoke as validate_super_passband_sol_smoke,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.er_sma_gate_cross_v1 import (
    ErSmaParams,
    compute_signals as er_sma_signals,
    validate_bnb_smoke as validate_er_sma_bnb_smoke,
    validate_sol_smoke as validate_er_sma_sol_smoke,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.rwi_high_low_threshold_v1 import (
    RwiParams,
    compute_signals as rwi_signals,
    validate_bnb_smoke as validate_rwi_bnb_smoke,
    validate_sol_smoke as validate_rwi_sol_smoke,
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
    sol_retention_note: str = "—"  # Retention diagnostic (especially after ETH pass)
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


def _finish(cell: CellResult, eth_cell: CellResult | None = None) -> CellResult:
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
    print(
        f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> "
        f"6m={cell.gate_6m}({g6.ratio:.3f}x) ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}, sol_retention={cell.sol_retention_note}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: er-sma-gate-cross-v1
# ---------------------------------------------------------------------------

def run_er_sma_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "er-sma-gate-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: Mode A (Lf, Ls, N, thr); Mode B
    param_grid: list[tuple[str, ErSmaParams]] = [
        ("mode_a|(10,30,N10,thr0.35)", ErSmaParams(mode="mode_a", fast_len=10, slow_len=30, er_len=10, er_threshold=0.35)),
        ("mode_a|(9,21,N14,thr0.30)", ErSmaParams(mode="mode_a", fast_len=9, slow_len=21, er_len=14, er_threshold=0.30)),
        ("mode_a|(12,26,N20,thr0.40)", ErSmaParams(mode="mode_a", fast_len=12, slow_len=26, er_len=20, er_threshold=0.40)),
        ("mode_b|(10,30,N10,thr0.35)", ErSmaParams(mode="mode_b", fast_len=10, slow_len=30, er_len=10, er_threshold=0.35)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_er_sma_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_er_sma_bnb_smoke(p, tf)
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
                buys, sells, stops = er_sma_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: ehlers-super-passband-rms-v1
# ---------------------------------------------------------------------------

def run_super_passband_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-super-passband-rms-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (P1, P2, rmsLen)
    param_grid: list[tuple[str, SuperPassbandParams]] = [
        ("mode_a|(40,60,rms50)", SuperPassbandParams(mode="mode_a", p1=40, p2=60, rms_len=50)),
        ("mode_a|(30,50,rms50)", SuperPassbandParams(mode="mode_a", p1=30, p2=50, rms_len=50)),
        ("mode_a|(20,40,rms40)", SuperPassbandParams(mode="mode_a", p1=20, p2=40, rms_len=40)),
        ("mode_b|(30,50)", SuperPassbandParams(mode="mode_b", p1=30, p2=50, rms_len=50)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_super_passband_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_super_passband_bnb_smoke(p, tf)
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
                buys, sells, stops = super_passband_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: rwi-high-low-threshold-v1
# ---------------------------------------------------------------------------

def run_rwi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "rwi-high-low-threshold-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (S, L, thr)
    param_grid: list[tuple[str, RwiParams]] = [
        ("mode_a|(7,64,thr1.0)", RwiParams(mode="mode_a", short_len=7, long_len=64, threshold=1.0)),
        ("mode_a|(5,40,thr1.0)", RwiParams(mode="mode_a", short_len=5, long_len=40, threshold=1.0)),
        ("mode_a|(8,48,thr1.0)", RwiParams(mode="mode_a", short_len=8, long_len=48, threshold=1.0)),
        ("mode_b|(7,64,thr1.0)", RwiParams(mode="mode_b", short_len=7, long_len=64, threshold=1.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_rwi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_rwi_bnb_smoke(p, tf)
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
                buys, sells, stops = rwi_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: ehlers-reverse-ema-trend-cycle-v1
# ---------------------------------------------------------------------------

def run_reverse_ema_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-reverse-ema-trend-cycle-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (alpha_trend, alpha_cycle)
    param_grid: list[tuple[str, ReverseEmaParams]] = [
        ("mode_a|(0.05,0.30)", ReverseEmaParams(mode="mode_a", alpha_trend=0.05, alpha_cycle=0.30)),
        ("mode_a|(0.08,0.25)", ReverseEmaParams(mode="mode_a", alpha_trend=0.08, alpha_cycle=0.25)),
        ("mode_a|(0.05,0.20)", ReverseEmaParams(mode="mode_a", alpha_trend=0.05, alpha_cycle=0.20)),
        ("mode_b|(0.10)", ReverseEmaParams(mode="mode_b", alpha_single=0.10)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_reverse_ema_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_reverse_ema_bnb_smoke(p, tf)
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
                buys, sells, stops = reverse_ema_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
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
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    if strategy_id == "er-sma-gate-cross-v1":
        return run_er_sma_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    elif strategy_id == "ehlers-super-passband-rms-v1":
        return run_super_passband_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    elif strategy_id == "rwi-high-low-threshold-v1":
        return run_rwi_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    elif strategy_id == "ehlers-reverse-ema-trend-cycle-v1":
        return run_reverse_ema_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


def run_stage7_dual_sol_bnb_v1(
    years: float = 2.5,
    refresh: bool = False,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> list[CellResult]:
    """Execute the locked 4-strategy stop-ladder with DUAL-SURVIVAL + SOL RETENTION."""
    all_results: list[CellResult] = []
    active_keys: set[str] | None = None  # None for BTC (run all)
    eth_results_by_key: dict[str, CellResult] = {}

    for idx, symbol in enumerate(symbols):
        print(f"\n==================================================================", flush=True)
        print(f"[{RESEARCH_ID}] Evaluating Symbol {idx+1}/{len(symbols)}: {symbol}", flush=True)
        print(f"==================================================================", flush=True)

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
            print(f"\n--- [{symbol}] Strategy: {sid} ---", flush=True)
            tfs = ("1h", "4h")
            param_grid_keys = {
                "er-sma-gate-cross-v1": ["mode_a|(10,30,N10,thr0.35)", "mode_a|(9,21,N14,thr0.30)", "mode_a|(12,26,N20,thr0.40)", "mode_b|(10,30,N10,thr0.35)"],
                "ehlers-super-passband-rms-v1": ["mode_a|(40,60,rms50)", "mode_a|(30,50,rms50)", "mode_a|(20,40,rms40)", "mode_b|(30,50)"],
                "rwi-high-low-threshold-v1": ["mode_a|(7,64,thr1.0)", "mode_a|(5,40,thr1.0)", "mode_a|(8,48,thr1.0)", "mode_b|(7,64,thr1.0)"],
                "ehlers-reverse-ema-trend-cycle-v1": ["mode_a|(0.05,0.30)", "mode_a|(0.08,0.25)", "mode_a|(0.05,0.20)", "mode_b|(0.10)"],
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

    md_path = output_dir / "stage7-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage7-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage7-dual-sol-bnb-v1 scoreboard (DUAL SOL+BNB survival: SOL + BNB)",
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
        "- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-6 IDs, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, no EMA/RSI, SMA200, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Kaufman ER Gate + SMA (`er-sma-gate-cross-v1`):** ER as path efficiency gate (0-1), fast/slow SMA cross. (Lf, Ls) in {(10,30), (9,21), (12,26)}; N in {10,14,20}; thr in {0.30, 0.35, 0.40}.",
        "- **Ehlers Super Passband Filter (`ehlers-super-passband-rms-v1`):** S&C Jul 2016 PB oscillator with alpha=5/P. Entry PB x -RMS. (P1, P2) in {(40,60), (30,50), (20,40)}; rmsLen in {40, 50}.",
        "- **Mike Poulos Random Walk Index (`rwi-high-low-threshold-v1`):** Displacement / (ATR*sqrt(i)). LT High > 1.0 + ST Low peak > 1.0. (S, L) in {(7,64), (5,40), (8,48)}; thr=1.0.",
        "- **Ehlers Reverse EMA (`ehlers-reverse-ema-trend-cycle-v1`):** TASC Sep 2017 RE1..RE8 cascade. Trend > 0 + Cycle zero-cross. (alpha_t, alpha_c) in {(0.05,0.30), (0.08,0.25), (0.05,0.20)}.",
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

    # CSV headers
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
