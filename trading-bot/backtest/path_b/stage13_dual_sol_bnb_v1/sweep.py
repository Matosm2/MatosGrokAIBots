"""stage13-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (ALL 5 — include optional #5):
1. demark-rei-zero-cross-v1
2. khalil-pzo-zero-cross-v1
3. mobius-tmo-main-zero-v1
4. donovan-range-filter-flip-v1
5. clv-sma-zero-cross-v1

Design Bias: BTC-clearing PRIMARY + BNB-portable SECONDARY. Dual SOL+BNB identical params.
TINY-N POLICY (critical): BTC Mode-A n <= 5 on 6m -> FAIL that cell even if xB&H >= 1.2; flag n approx 9 (6..10) as thin.
Mandatory btc_smoke + sol_smoke + bnb_smoke per strategy: log FAIL reasons; fail smoke -> disqualify cell.
BNB-smoke stresses BNB-after-BTC+SOL kill conditions; run bnb_smoke before declaring BNB fail.
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
from backtest.path_b.stage13_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.clv_sma_zero_cross_v1 import (
    ClvSmaParams,
    compute_signals as clv_signals,
    validate_bnb_smoke as validate_clv_bnb_smoke,
    validate_btc_smoke as validate_clv_btc_smoke,
    validate_sol_smoke as validate_clv_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.demark_rei_zero_cross_v1 import (
    DemarkReiParams,
    compute_signals as rei_signals,
    validate_bnb_smoke as validate_rei_bnb_smoke,
    validate_btc_smoke as validate_rei_btc_smoke,
    validate_sol_smoke as validate_rei_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.donovan_range_filter_flip_v1 import (
    DonovanRangeFilterParams,
    compute_signals as rf_signals,
    validate_bnb_smoke as validate_rf_bnb_smoke,
    validate_btc_smoke as validate_rf_btc_smoke,
    validate_sol_smoke as validate_rf_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.khalil_pzo_zero_cross_v1 import (
    KhalilPzoParams,
    compute_signals as pzo_signals,
    validate_bnb_smoke as validate_pzo_bnb_smoke,
    validate_btc_smoke as validate_pzo_btc_smoke,
    validate_sol_smoke as validate_pzo_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.mobius_tmo_main_zero_v1 import (
    MobiusTmoParams,
    compute_signals as tmo_signals,
    validate_bnb_smoke as validate_tmo_bnb_smoke,
    validate_btc_smoke as validate_tmo_btc_smoke,
    validate_sol_smoke as validate_tmo_sol_smoke,
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
        cell.notes.append(f"THIN-N FLAG (BTC 6m n={g6.trades} in thin band [{THIN_N_LOWER}..{THIN_N_UPPER}])")

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
            elif eth_g6.trades > 0 and g6.trades < max(5, eth_g6.trades // 4):
                cell.sol_retention_note = f"RETENTION WARN: SOL n={g6.trades} < 25% of ETH n={eth_g6.trades}"
            else:
                cell.sol_retention_note = f"OK (SOL n={g6.trades} vs ETH n={eth_g6.trades})"
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
        f"6m={cell.gate_6m}({g6.ratio:.3f}x){tiny_tag} ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [btc_smoke={cell.btc_smoke}, sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}, sol_retention={cell.sol_retention_note}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: demark-rei-zero-cross-v1
# ---------------------------------------------------------------------------


def run_rei_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "demark-rei-zero-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, DemarkReiParams]] = [
        ("mode_a|(L8)", DemarkReiParams(mode="mode_a", length=8)),
        ("mode_a|(L5)", DemarkReiParams(mode="mode_a", length=5)),
        ("mode_a|(L13)", DemarkReiParams(mode="mode_a", length=13)),
        ("mode_b|(L8)", DemarkReiParams(mode="mode_b", length=8)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_rei_btc_smoke(p, tf)
            sol_ok, sol_msg = validate_rei_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_rei_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = rei_signals(bars, p)
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
# Strategy 2: khalil-pzo-zero-cross-v1
# ---------------------------------------------------------------------------


def run_pzo_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "khalil-pzo-zero-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, KhalilPzoParams]] = [
        ("mode_a|(n14)", KhalilPzoParams(mode="mode_a", n_len=14)),
        ("mode_a|(n10)", KhalilPzoParams(mode="mode_a", n_len=10)),
        ("mode_a|(n20)", KhalilPzoParams(mode="mode_a", n_len=20)),
        ("mode_b|(n14,pzo0)", KhalilPzoParams(mode="mode_b", n_len=14)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_pzo_btc_smoke(p, tf)
            sol_ok, sol_msg = validate_pzo_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_pzo_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = pzo_signals(bars, p)
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
# Strategy 3: mobius-tmo-main-zero-v1
# ---------------------------------------------------------------------------


def run_tmo_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "mobius-tmo-main-zero-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, MobiusTmoParams]] = [
        ("mode_a|(len14,c5,s3)", MobiusTmoParams(mode="mode_a", length=14, calc_length=5, smooth_length=3)),
        ("mode_a|(len10,c5,s3)", MobiusTmoParams(mode="mode_a", length=10, calc_length=5, smooth_length=3)),
        ("mode_a|(len21,c5,s3)", MobiusTmoParams(mode="mode_a", length=21, calc_length=5, smooth_length=3)),
        ("mode_b|(len14,c5,s3)", MobiusTmoParams(mode="mode_b", length=14, calc_length=5, smooth_length=3)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_tmo_btc_smoke(p, tf)
            sol_ok, sol_msg = validate_tmo_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_tmo_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = tmo_signals(bars, p)
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
# Strategy 4: donovan-range-filter-flip-v1
# ---------------------------------------------------------------------------


def run_rf_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "donovan-range-filter-flip-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, DonovanRangeFilterParams]] = [
        ("mode_a|(p20,m1.618)", DonovanRangeFilterParams(mode="mode_a", period=20, mult=1.618)),
        ("mode_a|(p14,m1.618)", DonovanRangeFilterParams(mode="mode_a", period=14, mult=1.618)),
        ("mode_a|(p20,m2.0)", DonovanRangeFilterParams(mode="mode_a", period=20, mult=2.0)),
        ("mode_b|(p20,m1.618)", DonovanRangeFilterParams(mode="mode_b", period=20, mult=1.618)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_rf_btc_smoke(p, tf)
            sol_ok, sol_msg = validate_rf_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_rf_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = rf_signals(bars, p)
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
# Strategy 5: clv-sma-zero-cross-v1
# ---------------------------------------------------------------------------


def run_clv_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "clv-sma-zero-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, ClvSmaParams]] = [
        ("mode_a|(N14)", ClvSmaParams(mode="mode_a", n_len=14)),
        ("mode_a|(N8)", ClvSmaParams(mode="mode_a", n_len=8)),
        ("mode_a|(N21)", ClvSmaParams(mode="mode_a", n_len=21)),
        ("mode_b|(N14)", ClvSmaParams(mode="mode_b", n_len=14)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_clv_btc_smoke(p, tf)
            sol_ok, sol_msg = validate_clv_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_clv_bnb_smoke(p, tf)
            btc_smoke_str = "Y" if btc_ok else f"FAIL: {btc_msg}"
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke=btc_smoke_str,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            if not btc_ok or not sol_ok or not bnb_ok:
                cell.gate_6m = "FAIL"
                cell.notes.append(f"Disqualified by smoke: btc={btc_smoke_str}, sol={sol_smoke_str}, bnb={bnb_smoke_str}")
                results.append(cell)
                _print_cell(cell)
                continue

            try:
                buys, sells, stops = clv_signals(bars, p)
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


def run_strategy_cells(
    strategy_id: str,
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    if strategy_id == "demark-rei-zero-cross-v1":
        return run_rei_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "khalil-pzo-zero-cross-v1":
        return run_pzo_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "mobius-tmo-main-zero-v1":
        return run_tmo_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "donovan-range-filter-flip-v1":
        return run_rf_cells(symbol, bars_by_tf, active_keys, eth_results)
    elif strategy_id == "clv-sma-zero-cross-v1":
        return run_clv_cells(symbol, bars_by_tf, active_keys, eth_results)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


# ---------------------------------------------------------------------------
# Master Sweep Runner (Ladder: BTC -> ETH -> SOL -> BNB)
# ---------------------------------------------------------------------------


def run_stage13_dual_sol_bnb_v1(
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
        print(f"\n{'='*70}\n[stage13-dual-sol-bnb-v1] Evaluating Symbol: {symbol}\n{'='*70}", flush=True)

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
                "demark-rei-zero-cross-v1": ["mode_a|(L8)", "mode_a|(L5)", "mode_a|(L13)", "mode_b|(L8)"],
                "khalil-pzo-zero-cross-v1": ["mode_a|(n14)", "mode_a|(n10)", "mode_a|(n20)", "mode_b|(n14,pzo0)"],
                "mobius-tmo-main-zero-v1": ["mode_a|(len14,c5,s3)", "mode_a|(len10,c5,s3)", "mode_a|(len21,c5,s3)", "mode_b|(len14,c5,s3)"],
                "donovan-range-filter-flip-v1": ["mode_a|(p20,m1.618)", "mode_a|(p14,m1.618)", "mode_a|(p20,m2.0)", "mode_b|(p20,m1.618)"],
                "clv-sma-zero-cross-v1": ["mode_a|(N14)", "mode_a|(N8)", "mode_a|(N21)", "mode_b|(N14)"],
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
            print(f"  -> PROMOTED: {r.strategy_id} @ {r.tf} {r.mode_params} (6m={g6.return_pct:.2f}%, {g6.ratio:.3f}x B&H, btc_smoke={r.btc_smoke}, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, sol_retention={r.sol_retention_note})", flush=True)

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
        f"`{r.sol_smoke}`",
        f"`{r.bnb_smoke}`",
        f"`{r.sol_retention_note}`",
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

    md_path = output_dir / "stage13-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage13-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage13-dual-sol-bnb-v1 scoreboard (BTC-clearing PRIMARY + BNB-portable SECONDARY)",
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
        "- **BNB-portable SECONDARY:** After BTC+SOL clear, run `bnb_smoke` before declaring BNB fail; stresses BNB-after-BTC+SOL kill conditions.",
        "- **Mandatory Smoke & Retention Tests:** btc_smoke, sol_smoke, and bnb_smoke logged; sol_retention_note checked post-ETH.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-12 IDs, no CSI/PMO/Gaussian/US damp, no Super Passband/RWI/Reverse EMA/PGO, no Roofing, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **DeMark REI (`demark-rei-zero-cross-v1`):** DeMark Range Expansion Index. L=8 preferred; L=5, L=13. Mode A REI x 0; Mode B ±60 reclaim.",
        "- **Khalil PZO (`khalil-pzo-zero-cross-v1`):** Price Zone Oscillator. n=14 preferred; n=10, n=20. Mode A PZO x 0; Mode B pzo > 0 quality.",
        "- **Mobius TMO (`mobius-tmo-main-zero-v1`):** True Momentum Oscillator. (14,5,3) preferred; (10,5,3), (21,5,3). Mode A Main x 0; Mode B main > 0 quality. (NO Main x Signal).",
        "- **Donovan Range Filter (`donovan-range-filter-flip-v1`):** DW Range Filter. (20,1.618) preferred; (14,1.618), (20,2.0). Mode A dir flip +1/-1; Mode B src > filt.",
        "- **CLV SMA (`clv-sma-zero-cross-v1`):** Close Location Value SMA. N=14 preferred; N=8, N=21. Mode A CLVS x 0; Mode B clvs > 0 quality. Volume-free.",
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
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}) [btc_smoke={r.btc_smoke}, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, sol_retention={r.sol_retention_note}]: 6m ret={g.return_pct:.2f}% "
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
            "btc_smoke",
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

    # Group by strategy
    for sid in STRATEGY_IDS:
        sid_results = [r for r in results if r.strategy_id == sid]
        if not sid_results:
            continue
        lines.append(f"### `{sid}`")
        lines.append("")
        lines.append(
            "| Symbol | Strategy ID | TF | Params | BTC Smoke | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |"
        )
        lines.append(
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
        )
        for r in sid_results:
            md_cols, csv_cols = _row_to_cols(r)
            lines.append("| " + " | ".join(md_cols) + " |")
            csv_rows.append(csv_cols)
        lines.append("")

    # Write Markdown
    md_path.write_text("\n".join(lines), encoding="utf-8")

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
