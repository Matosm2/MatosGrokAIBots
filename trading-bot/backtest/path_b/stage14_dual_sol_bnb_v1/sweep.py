"""stage14-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (ALL 5 — include optional #5):
1. pee-ttf-zero-cross
2. hannula-pfe-zero-cross
3. absolute-strength-hist-zero
4. leibfarth-apz-break-flip
5. nadaraya-rq-estimate-cross

Design Bias: BTC->ETH portability PRIMARY + BNB-portable SECONDARY. Dual SOL+BNB identical params.
TINY-N POLICY (critical): BTC Mode-A n <= 5 on 6m -> FAIL that cell even if xB&H >= 1.2; flag n approx 9 (6..10) as thin.
Mandatory btc_smoke + eth_smoke + sol_smoke + bnb_smoke per strategy: log FAIL reasons; fail smoke -> disqualify cell.
BNB-smoke stresses BNB-after-BTC+ETH+SOL kill conditions; run bnb_smoke before declaring BNB fail.
Stop-ladder: BTC -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).
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
from backtest.path_b.stage14_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.pee_ttf_zero_cross_v1 import (
    PeeTtfParams,
    compute_signals as ttf_signals,
    validate_bnb_smoke as validate_ttf_bnb_smoke,
    validate_btc_smoke as validate_ttf_btc_smoke,
    validate_eth_smoke as validate_ttf_eth_smoke,
    validate_sol_smoke as validate_ttf_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.hannula_pfe_zero_cross_v1 import (
    HannulaPfeParams,
    compute_signals as pfe_signals,
    validate_bnb_smoke as validate_pfe_bnb_smoke,
    validate_btc_smoke as validate_pfe_btc_smoke,
    validate_eth_smoke as validate_pfe_eth_smoke,
    validate_sol_smoke as validate_pfe_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.absolute_strength_hist_zero_v1 import (
    AbsoluteStrengthHistParams,
    compute_signals as ash_signals,
    validate_bnb_smoke as validate_ash_bnb_smoke,
    validate_btc_smoke as validate_ash_btc_smoke,
    validate_eth_smoke as validate_ash_eth_smoke,
    validate_sol_smoke as validate_ash_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.leibfarth_apz_break_flip_v1 import (
    LeibfarthApzParams,
    compute_signals as apz_signals,
    validate_bnb_smoke as validate_apz_bnb_smoke,
    validate_btc_smoke as validate_apz_btc_smoke,
    validate_eth_smoke as validate_apz_eth_smoke,
    validate_sol_smoke as validate_apz_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.nadaraya_rq_estimate_cross_v1 import (
    NadarayaRqParams,
    compute_signals as rq_signals,
    validate_bnb_smoke as validate_rq_bnb_smoke,
    validate_btc_smoke as validate_rq_btc_smoke,
    validate_eth_smoke as validate_rq_eth_smoke,
    validate_sol_smoke as validate_rq_sol_smoke,
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
    btc_smoke: str = "Y"  # Y / FAIL: reason / N/A
    eth_smoke: str = "Y"  # Y / FAIL: reason / N/A
    sol_smoke: str = "Y"  # Y / FAIL: reason / N/A
    bnb_smoke: str = "Y"  # Y / FAIL: reason / N/A
    retention_notes: str = "—"  # Retention diagnostic (post-BTC ETH retention, post-ETH SOL retention, post-SOL BNB)
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
    masked: list[bool] = []
    for b, bar in zip(buys, bars, strict=False):
        masked.append(bool(b and bar.open_time_ms >= start_ms))
    return masked


def _ratio(ret: float, bh: float) -> float:
    if bh > 0:
        return ret / bh
    elif bh < 0:
        return (ret - bh) / abs(bh)
    return 0.0


def _gate_label(symbol: str, trades: int, ret: float, bh: float, window: str) -> tuple[str, bool, bool]:
    ratio = _ratio(ret, bh)
    tiny_kill = False
    thin_flag = False

    if symbol == "BTCUSDT" and window == "6m":
        if trades <= TINY_N_THRESHOLD:
            tiny_kill = True
            return "FAIL", tiny_kill, thin_flag
        elif THIN_N_LOWER <= trades <= THIN_N_UPPER:
            thin_flag = True

    if trades == 0:
        return "FAIL", tiny_kill, thin_flag

    is_pass = ratio >= GATE_MULT
    return ("PASS" if is_pass else "FAIL"), tiny_kill, thin_flag


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


def _finish(
    cell: CellResult,
    prior_cell: CellResult | None = None,
) -> CellResult:
    if cell.error or cell.skipped or not cell.metrics:
        return cell
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate

    if cell.tiny_n_kill:
        cell.notes.append(f"TINY-N KILL (BTC 6m n={g6.trades} <= {TINY_N_THRESHOLD} despite {g6.ratio:.2f}x B&H)")
    elif cell.thin_n_flag:
        cell.notes.append(f"THIN-N FLAG (BTC 6m n={g6.trades} in thin band [{THIN_N_LOWER}..{THIN_N_UPPER}])")

    if 0.9 <= g6.ratio < 1.2:
        cell.notes.append(f"Near-miss 6m ({g6.ratio:.2f}x B&H)")

    if cell.symbol == "ETHUSDT":
        cell.notes.append("ETH hard filter")
        if prior_cell and prior_cell.metrics:
            btc_g6 = next(m for m in prior_cell.metrics if m.window == "6m" and m.mode == "gate")
            if btc_g6.trades > 0 and g6.trades == 0:
                cell.retention_notes = "ETH RETENTION FAIL: 0 ETH trades vs BTC trades"
            elif btc_g6.trades > 0 and g6.trades < max(5, btc_g6.trades // 4):
                cell.retention_notes = f"ETH RETENTION WARN: ETH n={g6.trades} < 25% of BTC n={btc_g6.trades}"
            else:
                cell.retention_notes = f"OK (ETH n={g6.trades} vs BTC n={btc_g6.trades})"
    elif cell.symbol == "SOLUSDT":
        cell.notes.append("SOL hard filter")
        if prior_cell and prior_cell.metrics:
            eth_g6 = next(m for m in prior_cell.metrics if m.window == "6m" and m.mode == "gate")
            if eth_g6.trades > 0 and g6.trades == 0:
                cell.retention_notes = "SOL RETENTION FAIL: 0 SOL trades vs ETH trades"
            elif eth_g6.trades > 0 and g6.trades < max(5, eth_g6.trades // 4):
                cell.retention_notes = f"SOL RETENTION WARN: SOL n={g6.trades} < 25% of ETH n={eth_g6.trades}"
            else:
                cell.retention_notes = f"OK (SOL n={g6.trades} vs ETH n={eth_g6.trades})"
    elif cell.symbol == "BNBUSDT":
        cell.notes.append("BNB hard filter")
        if prior_cell and prior_cell.metrics:
            sol_g6 = next(m for m in prior_cell.metrics if m.window == "6m" and m.mode == "gate")
            cell.retention_notes = f"OK (BNB n={g6.trades} vs SOL n={sol_g6.trades})"

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
        f"6m={cell.gate_6m}({g6.ratio:.3f}x){tiny_tag} ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [btc_smoke={cell.btc_smoke}, eth_smoke={cell.eth_smoke}, sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}, retention={cell.retention_notes}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: pee-ttf-zero-cross
# ---------------------------------------------------------------------------

def run_ttf_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "pee-ttf-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, PeeTtfParams]] = [
        ("mode_a|(L15)", PeeTtfParams(mode="mode_a", length=15)),
        ("mode_a|(L10)", PeeTtfParams(mode="mode_a", length=10)),
        ("mode_a|(L20)", PeeTtfParams(mode="mode_a", length=20)),
        ("mode_b|(L15)", PeeTtfParams(mode="mode_b", length=15)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_ttf_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_ttf_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_ttf_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_ttf_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            eth_smoke_str = "Y" if eth_ok else f"FAIL: {eth_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                eth_smoke=eth_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not eth_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, eth={eth_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = ttf_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                prior_cell = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: hannula-pfe-zero-cross
# ---------------------------------------------------------------------------

def run_pfe_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "hannula-pfe-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, HannulaPfeParams]] = [
        ("mode_a|(p10,s5)", HannulaPfeParams(mode="mode_a", period=10, smooth=5)),
        ("mode_a|(p8,s3)", HannulaPfeParams(mode="mode_a", period=8, smooth=3)),
        ("mode_a|(p14,s8)", HannulaPfeParams(mode="mode_a", period=14, smooth=8)),
        ("mode_b|(p10,s5)", HannulaPfeParams(mode="mode_b", period=10, smooth=5)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_pfe_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_pfe_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_pfe_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_pfe_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            eth_smoke_str = "Y" if eth_ok else f"FAIL: {eth_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                eth_smoke=eth_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not eth_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, eth={eth_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = pfe_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                prior_cell = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: absolute-strength-hist-zero
# ---------------------------------------------------------------------------

def run_ash_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "absolute-strength-hist-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, AbsoluteStrengthHistParams]] = [
        ("mode_a|(len9,sm2)", AbsoluteStrengthHistParams(mode="mode_a", length=9, smooth=2)),
        ("mode_a|(len7,sm1)", AbsoluteStrengthHistParams(mode="mode_a", length=7, smooth=1)),
        ("mode_a|(len14,sm3)", AbsoluteStrengthHistParams(mode="mode_a", length=14, smooth=3)),
        ("mode_b|(len9,sm2)", AbsoluteStrengthHistParams(mode="mode_b", length=9, smooth=2)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_ash_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_ash_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_ash_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_ash_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            eth_smoke_str = "Y" if eth_ok else f"FAIL: {eth_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                eth_smoke=eth_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not eth_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, eth={eth_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = ash_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                prior_cell = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: leibfarth-apz-break-flip
# ---------------------------------------------------------------------------

def run_apz_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "leibfarth-apz-break-flip"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, LeibfarthApzParams]] = [
        ("mode_a|(p20,b1.4)", LeibfarthApzParams(mode="mode_a", period=20, band_pct=1.4)),
        ("mode_a|(p14,b1.2)", LeibfarthApzParams(mode="mode_a", period=14, band_pct=1.2)),
        ("mode_a|(p30,b1.8)", LeibfarthApzParams(mode="mode_a", period=30, band_pct=1.8)),
        ("mode_b|(p20,b1.4)", LeibfarthApzParams(mode="mode_b", period=20, band_pct=1.4)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_apz_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_apz_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_apz_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_apz_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            eth_smoke_str = "Y" if eth_ok else f"FAIL: {eth_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                eth_smoke=eth_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not eth_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, eth={eth_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = apz_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                prior_cell = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 5: nadaraya-rq-estimate-cross
# ---------------------------------------------------------------------------

def run_rq_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "nadaraya-rq-estimate-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, NadarayaRqParams]] = [
        ("mode_a|(lb8,a8)", NadarayaRqParams(mode="mode_a", lookback=8, alpha=8.0)),
        ("mode_a|(lb5,a1)", NadarayaRqParams(mode="mode_a", lookback=5, alpha=1.0)),
        ("mode_a|(lb14,a25)", NadarayaRqParams(mode="mode_a", lookback=14, alpha=25.0)),
        ("mode_b|(lb8,a8)", NadarayaRqParams(mode="mode_b", lookback=8, alpha=8.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_rq_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_rq_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_rq_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_rq_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            eth_smoke_str = "Y" if eth_ok else f"FAIL: {eth_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                eth_smoke=eth_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not eth_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, eth={eth_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = rq_signals(bars, p)
                cell.metrics, cell.tiny_n_kill, cell.thin_n_flag = _eval_windows(
                    symbol, sid, bars, buys, sells, stops
                )
                prior_cell = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior_cell)
            except Exception as exc:
                cell.error = str(exc)
            results.append(cell)
            _print_cell(cell)

    return results


def run_strategy_cells(
    strategy_id: str,
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    if strategy_id == "pee-ttf-zero-cross":
        return run_ttf_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "hannula-pfe-zero-cross":
        return run_pfe_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "absolute-strength-hist-zero":
        return run_ash_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "leibfarth-apz-break-flip":
        return run_apz_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "nadaraya-rq-estimate-cross":
        return run_rq_cells(symbol, bars_by_tf, active_keys, prior_results)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


# ---------------------------------------------------------------------------
# Master Sweep Runner (Ladder: BTC -> ETH -> SOL -> BNB)
# ---------------------------------------------------------------------------

def run_stage14_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Stop-ladder tracking: cells that pass BTC -> ETH -> SOL -> BNB
    active_keys: set[str] | None = None
    prior_results_by_key: dict[str, CellResult] = {}

    for symbol in symbols:
        print(f"\n{'='*70}\n[stage14-dual-sol-bnb-v1] Evaluating Symbol: {symbol}\n{'='*70}", flush=True)

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
                "pee-ttf-zero-cross": ["mode_a|(L15)", "mode_a|(L10)", "mode_a|(L20)", "mode_b|(L15)"],
                "hannula-pfe-zero-cross": ["mode_a|(p10,s5)", "mode_a|(p8,s3)", "mode_a|(p14,s8)", "mode_b|(p10,s5)"],
                "absolute-strength-hist-zero": ["mode_a|(len9,sm2)", "mode_a|(len7,sm1)", "mode_a|(len14,sm3)", "mode_b|(len9,sm2)"],
                "leibfarth-apz-break-flip": ["mode_a|(p20,b1.4)", "mode_a|(p14,b1.2)", "mode_a|(p30,b1.8)", "mode_b|(p20,b1.4)"],
                "nadaraya-rq-estimate-cross": ["mode_a|(lb8,a8)", "mode_a|(lb5,a1)", "mode_a|(lb14,a25)", "mode_b|(lb8,a8)"],
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
                            btc_smoke="Y",
                            eth_smoke="Y",
                            sol_smoke="Y",
                            bnb_smoke="Y",
                            retention_notes="—",
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
                            prior_results=prior_results_by_key if symbol != "BTCUSDT" else None,
                        )
                        sym_results.extend(res)
                        all_results.extend(res)

        # Update prior results for next ladder step
        prior_results_by_key = {f"{r.strategy_id}@{r.tf}@{r.mode_params}": r for r in sym_results if not r.skipped and not r.error}

        # Stop-ladder filtering: only cells with gate_6m == "PASS" advance to next symbol
        passed_cells = [
            r for r in sym_results
            if not r.skipped and not r.error and r.gate_6m == "PASS"
        ]
        next_active: set[str] = {f"{r.strategy_id}@{r.tf}@{r.mode_params}" for r in passed_cells}

        print(f"\n[{symbol}] Evaluation Summary: Scored={len(sym_results)}, PASS_6m={len(passed_cells)}", flush=True)
        for r in passed_cells:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            print(f"  -> PROMOTED: {r.strategy_id} @ {r.tf} {r.mode_params} (6m={g6.return_pct:.2f}%, {g6.ratio:.3f}x B&H, btc_smoke={r.btc_smoke}, eth_smoke={r.eth_smoke}, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, retention={r.retention_notes})", flush=True)

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

    pass_6m_md = f"**{r.gate_6m}**" if r.gate_6m == "PASS" else r.gate_6m
    pass_full_md = f"**{r.gate_full}**" if r.gate_full == "PASS" else r.gate_full

    note_str = "; ".join(r.notes) if r.notes else "—"

    md_cols = [
        f"`{r.symbol}`",
        f"`{r.strategy_id}`",
        f"`{r.tf}`",
        f"`{r.mode_params}`",
        f"`{r.btc_smoke}`",
        f"`{r.eth_smoke}`",
        f"`{r.sol_smoke}`",
        f"`{r.bnb_smoke}`",
        f"`{r.retention_notes}`",
        str(g6.trades) if g6 else "—",
        f"{g6.win_rate_pct:.1f}%" if g6 else "—",
        f"{g6.return_pct:+.2f}%" if g6 else "—",
        f"{g6.bh_return_pct:+.2f}%" if g6 else "—",
        f"{g6.ratio:.3f}×" if g6 else "—",
        pass_6m_md,
        str(gf.trades) if gf else "—",
        f"{gf.win_rate_pct:.1f}%" if gf else "—",
        f"{gf.return_pct:+.2f}%" if gf else "—",
        f"{gf.bh_return_pct:+.2f}%" if gf else "—",
        f"{gf.ratio:.3f}×" if gf else "—",
        pass_full_md,
        f"{o6.return_pct:+.2f}%" if o6 else "—",
        f"{of.return_pct:+.2f}%" if of else "—",
        note_str,
    ]

    csv_cols = [
        r.symbol,
        r.strategy_id,
        r.tf,
        r.mode_params,
        r.btc_smoke,
        r.eth_smoke,
        r.sol_smoke,
        r.bnb_smoke,
        r.retention_notes,
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

    md_path = output_dir / "stage14-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage14-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage14-dual-sol-bnb-v1 scoreboard (BTC->ETH portability PRIMARY + BNB-portable SECONDARY)",
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
        "- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).",
        "- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).",
        "- **ETH Portability (CRITICAL):** Stage 13 wipe lesson (REI cleared BTC 1.530x then wiped ETH -1.201x). BTC->ETH portability is primary.",
        "- **BNB-portable SECONDARY:** After BTC+ETH+SOL clear, run `bnb_smoke` before declaring BNB fail; stresses BNB-after-BTC+ETH+SOL kill conditions.",
        "- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-13 IDs, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Super Passband/RWI/Reverse EMA/PGO, no Roofing, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Pee TTF (`pee-ttf-zero-cross`):** Trend Trigger Factor. L=15 preferred; L=10, L=20. Mode A TTF x 0; Mode B +-100 reclaim.",
        "- **Hannula PFE (`hannula-pfe-zero-cross`):** Polarized Fractal Efficiency. (10,5) preferred; (8,3), (14,8). Mode A PFE x 0; Mode B quality hold (pfe > 20).",
        "- **Absolute Strength Histogram (`absolute-strength-hist-zero`):** ASH RSI-method SMA internals. (9,2) preferred; (7,1), (14,3). Mode A ASH x 0; Mode B ash > 0 quality.",
        "- **Leibfarth APZ (`leibfarth-apz-break-flip`):** Adaptive Price Zone double-EMA band break-flip. (20,1.4) preferred; (14,1.2), (30,1.8). Mode A close x up break, exit close x dn; Mode B fade reclaim.",
        "- **Nadaraya RQ (`nadaraya-rq-estimate-cross`):** Causal Nadaraya-Watson Rational Quadratic Kernel. (8,8) preferred; (5,1), (14,25). Mode A close x yhat; Mode B close x yhat + slope.",
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
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}) [btc_smoke={r.btc_smoke}, eth_smoke={r.eth_smoke}, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, retention={r.retention_notes}]: 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f}x wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f}x n={gf.trades}"
            )

    lines.append("")
    lines.append("## All Scored Cells by Strategy")
    lines.append("")

    headers = [
        "Symbol", "Strategy ID", "TF", "Params", "BTC Smoke", "ETH Smoke", "SOL Smoke", "BNB Smoke", "Retention",
        "n (6m)", "WR (6m)", "Ret (6m)", "B&H (6m)", "Ratio (6m)", "PASS_6m",
        "n (full)", "WR (full)", "Ret (full)", "B&H (full)", "Ratio (full)", "PASS_full",
        "Ops Ret (6m)", "Ops Ret (full)", "Notes",
    ]

    for sid in STRATEGY_IDS:
        lines.append(f"### `{sid}`")
        lines.append("")
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("|" + "|".join(["---"] * len(headers)) + "|")

        sid_results = [r for r in results if r.strategy_id == sid]
        for r in sid_results:
            md_cols, _ = _row_to_cols(r)
            lines.append("| " + " | ".join(md_cols) + " |")
        lines.append("")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # CSV
    csv_rows: list[list[str]] = [headers]
    for r in results:
        _, csv_cols = _row_to_cols(r)
        csv_rows.append(csv_cols)

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
