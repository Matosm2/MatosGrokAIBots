"""stage20-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (ALL 5):
1. vpci-zero-cross
2. bw-mfi-green-fade-flip
3. demand-index-zero
4. kalman-estimate-cross
5. ravi-threshold-dir

Design Bias:
  BNB-survival CRITICAL after 3-coin clear (stage14 TTF + stage19 HHLL rhyme).
  Prefer denser n >> 9 (>> HHLL n=8). Keep BTC->ETH->SOL portability.
  EXIT HHLL/STARC/VZO/NVI/FDI.
  Identical dual params across BTC/ETH/SOL/BNB (never BNB-only Length/Mode B).
  bnb_smoke CRITICAL + btc_smoke + eth_smoke + sol_smoke.
  Tiny-n: BTC n <= 5 FAIL; flag n approx 9 (6..10).
Stop-ladder: BTC -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).
LEAD gate: last-6m Mode-A return >= 1.2x buy-and-hold (same window) AND n > 5 on BTC. WR info.
Full(~2y) Mode-A + ops 2.5% sizing.
Costs: 0.1%/side + 5 bps adverse slip. Closed-bar only; pyramiding 0.
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
from backtest.path_b.stage20_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.vpci_zero_cross_v1 import (
    VpciParams,
    compute_signals as vpci_signals,
    validate_bnb_smoke as validate_vpci_bnb_smoke,
    validate_btc_smoke as validate_vpci_btc_smoke,
    validate_eth_smoke as validate_vpci_eth_smoke,
    validate_sol_smoke as validate_vpci_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.bw_mfi_green_fade_flip_v1 import (
    BwMfiParams,
    compute_signals as bw_mfi_signals,
    validate_bnb_smoke as validate_bw_mfi_bnb_smoke,
    validate_btc_smoke as validate_bw_mfi_btc_smoke,
    validate_eth_smoke as validate_bw_mfi_eth_smoke,
    validate_sol_smoke as validate_bw_mfi_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.demand_index_zero_v1 import (
    DemandIndexParams,
    compute_signals as demand_index_signals,
    validate_bnb_smoke as validate_demand_index_bnb_smoke,
    validate_btc_smoke as validate_demand_index_btc_smoke,
    validate_eth_smoke as validate_demand_index_eth_smoke,
    validate_sol_smoke as validate_demand_index_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.kalman_estimate_cross_v1 import (
    KalmanParams,
    compute_signals as kalman_signals,
    validate_bnb_smoke as validate_kalman_bnb_smoke,
    validate_btc_smoke as validate_kalman_btc_smoke,
    validate_eth_smoke as validate_kalman_eth_smoke,
    validate_sol_smoke as validate_kalman_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.ravi_threshold_dir_v1 import (
    RaviParams,
    compute_signals as ravi_signals,
    validate_bnb_smoke as validate_ravi_bnb_smoke,
    validate_btc_smoke as validate_ravi_btc_smoke,
    validate_eth_smoke as validate_ravi_eth_smoke,
    validate_sol_smoke as validate_ravi_sol_smoke,
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
    retention_notes: str = "—"  # Retention diagnostic
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    tiny_n_kill: bool = False
    thin_n_flag: bool = False
    notes: list[str] = field(default_factory=list)
    skipped: bool = False
    error: str | None = None


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
    sid: str,
    bars: list[Bar],
    buys: list[bool],
    sells: list[bool],
    stops: list[float | None],
) -> tuple[list[WindowModeMetrics], bool, bool]:
    out: list[WindowModeMetrics] = []
    cell_tiny_kill = False
    cell_thin_flag = False

    for win_label, months in WINDOWS:
        start_ms = _window_start_ms(months)
        masked_buys = _mask_buys_before(buys, bars, start_ms)

        for mode_name, size_pct in SIZING:
            raw_res = run_long_only(
                symbol=symbol,
                strategy_id=sid,
                bars=bars,
                buys=masked_buys,
                sells=sells,
                stop_prices=stops,
                initial_equity=INITIAL,
                buy_qty_pct=size_pct,
                fee_rate=FEE,
                slippage_rate=SLIP,
                window_label=win_label,
            )
            sliced = slice_result_to_window(raw_res, bars, start_ms, window_label=win_label)
            m = summarize_path_b(sliced)

            ret_pct = float(m["return_pct"])
            bh_pct = float(m["buy_hold_return_pct"])
            ratio = _ratio(ret_pct, bh_pct)
            n_trades = int(m["trades"])

            gate_lbl = "—"
            if mode_name == "gate":
                gate_lbl, tiny_k, thin_f = _gate_label(symbol, n_trades, ret_pct, bh_pct, win_label)
                if win_label == "6m":
                    cell_tiny_kill = tiny_k
                    cell_thin_flag = thin_f

            wmm = WindowModeMetrics(
                window=win_label,
                mode=mode_name,
                size_pct=size_pct,
                return_pct=ret_pct,
                bh_return_pct=bh_pct,
                ratio=ratio,
                win_rate_pct=float(m["win_rate_pct"]),
                trades=n_trades,
                wins=int(m["wins"]),
                losses=int(m["losses"]),
                max_drawdown_pct=float(m["max_drawdown_pct"]),
                gate=gate_lbl,
            )
            out.append(wmm)

    return out, cell_tiny_kill, cell_thin_flag


def _finish(cell: CellResult, prior_cell: CellResult | None = None) -> CellResult:
    g6 = next((m for m in cell.metrics if m.window == "6m" and m.mode == "gate"), None)
    gf = next((m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
    if not g6:
        cell.gate_6m = "FAIL"
        return cell

    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate if gf else "FAIL"

    if cell.tiny_n_kill:
        cell.notes.append(f"TINY-N KILL (BTC 6m n={g6.trades} <= {TINY_N_THRESHOLD})")
    if cell.thin_n_flag:
        cell.notes.append(f"THIN-N FLAG (BTC 6m n={g6.trades} in thin band [{THIN_N_LOWER}..{THIN_N_UPPER}])")

    if 0.9 <= g6.ratio < 1.2:
        cell.notes.append(f"Near-miss 6m ({g6.ratio:.2f}x B&H)")

    if cell.symbol == "ETHUSDT":
        cell.notes.append("ETH hard filter (BTC->ETH portability check)")
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
        cell.notes.append("BNB hard filter (BNB-survival CRITICAL)")
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
# Strategy 1: vpci-zero-cross
# ---------------------------------------------------------------------------

def run_vpci_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "vpci-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, VpciParams]] = [
        ("mode_a|(s5,l20)", VpciParams(mode="mode_a", short_len=5, long_len=20)),
        ("mode_a|(s8,l20)", VpciParams(mode="mode_a", short_len=8, long_len=20)),
        ("mode_a|(s5,l25)", VpciParams(mode="mode_a", short_len=5, long_len=25)),
        ("mode_b|(s5,l20,sig10)", VpciParams(mode="mode_b", short_len=5, long_len=20, sig_len=10)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_vpci_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_vpci_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_vpci_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_vpci_bnb_smoke(p, tf)
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
                buys, sells, stops = vpci_signals(bars, p)
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
# Strategy 2: bw-mfi-green-fade-flip
# ---------------------------------------------------------------------------

def run_bw_mfi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "bw-mfi-green-fade-flip"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, BwMfiParams]] = [
        ("mode_a|(conf1)", BwMfiParams(mode="mode_a", confirm_bars=1, exit_on_fade=True)),
        ("mode_a|(conf2)", BwMfiParams(mode="mode_a", confirm_bars=2, exit_on_fade=True)),
        ("mode_a|(conf3)", BwMfiParams(mode="mode_a", confirm_bars=3, exit_on_fade=True)),
        ("mode_b|(conf1,notgreen)", BwMfiParams(mode="mode_b", confirm_bars=1, exit_on_fade=False)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_bw_mfi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_bw_mfi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_bw_mfi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_bw_mfi_bnb_smoke(p, tf)
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
                buys, sells, stops = bw_mfi_signals(bars, p)
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
# Strategy 3: demand-index-zero
# ---------------------------------------------------------------------------

def run_demand_index_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "demand-index-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, DemandIndexParams]] = [
        ("mode_a|(bs10,sm10)", DemandIndexParams(mode="mode_a", n_bs=10, n_smooth=10)),
        ("mode_a|(bs8,sm5)", DemandIndexParams(mode="mode_a", n_bs=8, n_smooth=5)),
        ("mode_a|(bs14,sm14)", DemandIndexParams(mode="mode_a", n_bs=14, n_smooth=14)),
        ("mode_b|(bs10,sm10,hold1)", DemandIndexParams(mode="mode_b", n_bs=10, n_smooth=10, hold_bars=1, band_level=5.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_demand_index_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_demand_index_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_demand_index_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_demand_index_bnb_smoke(p, tf)
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
                buys, sells, stops = demand_index_signals(bars, p)
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
# Strategy 4: kalman-estimate-cross
# ---------------------------------------------------------------------------

def run_kalman_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "kalman-estimate-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, KalmanParams]] = [
        ("mode_a|(len20,r0.01,q0.1)", KalmanParams(mode="mode_a", length=20, r=0.01, q=0.1)),
        ("mode_a|(len14,r0.01,q0.05)", KalmanParams(mode="mode_a", length=14, r=0.01, q=0.05)),
        ("mode_a|(len30,r0.02,q0.1)", KalmanParams(mode="mode_a", length=30, r=0.02, q=0.1)),
        ("mode_b|(len20,r0.01,q0.1,slope3)", KalmanParams(mode="mode_b", length=20, r=0.01, q=0.1, slope_len=3)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_kalman_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_kalman_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_kalman_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_kalman_bnb_smoke(p, tf)
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
                buys, sells, stops = kalman_signals(bars, p)
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
# Strategy 5: ravi-threshold-dir
# ---------------------------------------------------------------------------

def run_ravi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ravi-threshold-dir"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, RaviParams]] = [
        ("mode_a|(s7,l65,thr3.0,dir3)", RaviParams(mode="mode_a", short_len=7, long_len=65, thr=3.0, dir_len=3)),
        ("mode_a|(s7,l40,thr3.0,dir3)", RaviParams(mode="mode_a", short_len=7, long_len=40, thr=3.0, dir_len=3)),
        ("mode_a|(s5,l40,thr2.0,dir1)", RaviParams(mode="mode_a", short_len=5, long_len=40, thr=2.0, dir_len=1)),
        ("mode_b|(s7,l65,thr4.0,dir5)", RaviParams(mode="mode_b", short_len=7, long_len=65, thr=4.0, dir_len=5)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_ravi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_ravi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_ravi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_ravi_bnb_smoke(p, tf)
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
                buys, sells, stops = ravi_signals(bars, p)
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
# Master Ladder Runner (BTC -> ETH -> SOL -> BNB)
# ---------------------------------------------------------------------------

def run_stage20_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []
    tfs = ("1h", "4h")

    active_keys: set[str] | None = None
    prior_results_by_key: dict[str, CellResult] = {}

    for s_idx, symbol in enumerate(symbols):
        print(f"\n{'='*70}\n[stage20-dual-sol-bnb-v1] Evaluating Symbol: {symbol} (LADDER STEP {s_idx + 1}/4)\n{'='*70}", flush=True)

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
                "vpci-zero-cross": ["mode_a|(s5,l20)", "mode_a|(s8,l20)", "mode_a|(s5,l25)", "mode_b|(s5,l20,sig10)"],
                "bw-mfi-green-fade-flip": ["mode_a|(conf1)", "mode_a|(conf2)", "mode_a|(conf3)", "mode_b|(conf1,notgreen)"],
                "demand-index-zero": ["mode_a|(bs10,sm10)", "mode_a|(bs8,sm5)", "mode_a|(bs14,sm14)", "mode_b|(bs10,sm10,hold1)"],
                "kalman-estimate-cross": ["mode_a|(len20,r0.01,q0.1)", "mode_a|(len14,r0.01,q0.05)", "mode_a|(len30,r0.02,q0.1)", "mode_b|(len20,r0.01,q0.1,slope3)"],
                "ravi-threshold-dir": ["mode_a|(s7,l65,thr3.0,dir3)", "mode_a|(s7,l40,thr3.0,dir3)", "mode_a|(s5,l40,thr2.0,dir1)", "mode_b|(s7,l65,thr4.0,dir5)"],
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

            if active_keys is None or any(k.startswith(f"{sid}@") for k in active_keys):
                bars = _get_bars()
                if sid == "vpci-zero-cross":
                    res = run_vpci_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "bw-mfi-green-fade-flip":
                    res = run_bw_mfi_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "demand-index-zero":
                    res = run_demand_index_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "kalman-estimate-cross":
                    res = run_kalman_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "ravi-threshold-dir":
                    res = run_ravi_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
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

        print(f"\n[{symbol}] Evaluation Summary: Scored={len([r for r in sym_results if not r.skipped])}, PASS_6m={len(passed_cells)}", flush=True)
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

    note_str = "; ".join(r.notes) if r.notes else "—"
    if r.skipped:
        g6_trades = "—"
        g6_wr = "—"
        g6_ret = "—"
        g6_bh = "—"
        g6_ratio = "—"
        gf_trades = "—"
        gf_wr = "—"
        gf_ret = "—"
        gf_bh = "—"
        gf_ratio = "—"
        o6_ret = "—"
        of_ret = "—"
    elif r.error:
        note_str = f"ERROR: {r.error}"
        g6_trades = "—"
        g6_wr = "—"
        g6_ret = "—"
        g6_bh = "—"
        g6_ratio = "—"
        gf_trades = "—"
        gf_wr = "—"
        gf_ret = "—"
        gf_bh = "—"
        gf_ratio = "—"
        o6_ret = "—"
        of_ret = "—"
    else:
        g6_trades = str(g6.trades) if g6 else "—"
        g6_wr = f"{g6.win_rate_pct:.1f}%" if g6 else "—"
        g6_ret = f"{g6.return_pct:.2f}%" if g6 else "—"
        g6_bh = f"{g6.bh_return_pct:.2f}%" if g6 else "—"
        g6_ratio = f"{g6.ratio:.3f}x" if g6 else "—"

        gf_trades = str(gf.trades) if gf else "—"
        gf_wr = f"{gf.win_rate_pct:.1f}%" if gf else "—"
        gf_ret = f"{gf.return_pct:.2f}%" if gf else "—"
        gf_bh = f"{gf.bh_return_pct:.2f}%" if gf else "—"
        gf_ratio = f"{gf.ratio:.3f}x" if gf else "—"

        o6_ret = f"{o6.return_pct:.2f}%" if o6 else "—"
        of_ret = f"{of.return_pct:.2f}%" if of else "—"

    md_cols = [
        r.symbol,
        f"`{r.strategy_id}`",
        r.tf,
        f"`{r.mode_params}`",
        r.btc_smoke,
        r.eth_smoke,
        r.sol_smoke,
        r.bnb_smoke,
        r.retention_notes,
        g6_trades,
        g6_wr,
        g6_ret,
        g6_bh,
        g6_ratio,
        f"**{r.gate_6m}**" if r.gate_6m == "PASS" else r.gate_6m,
        gf_trades,
        gf_wr,
        gf_ret,
        gf_bh,
        gf_ratio,
        f"**{r.gate_full}**" if r.gate_full == "PASS" else r.gate_full,
        o6_ret,
        of_ret,
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
        f"{g6.return_pct:.2f}" if g6 else "",
        f"{g6.bh_return_pct:.2f}" if g6 else "",
        f"{g6.ratio:.4f}" if g6 else "",
        r.gate_6m,
        str(gf.trades) if gf else "",
        f"{gf.win_rate_pct:.2f}" if gf else "",
        f"{gf.return_pct:.2f}" if gf else "",
        f"{gf.bh_return_pct:.2f}" if gf else "",
        f"{gf.ratio:.4f}" if gf else "",
        r.gate_full,
        f"{o6.return_pct:.2f}" if o6 else "",
        f"{of.return_pct:.2f}" if of else "",
        note_str,
    ]

    return md_cols, csv_cols


def write_scoreboard(
    results: list[CellResult],
    output_dir: Path = RESULTS_DIR,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / "stage20-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage20-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage20-dual-sol-bnb-v1 scoreboard (BNB-survival CRITICAL after 3-coin clear + Denser n >> 9)",
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
        "- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD — TTF/HHLL choke).",
        "- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).",
        "- **BNB-Survival Bias:** Designed to survive quieter BNB without quiet wipe (stage14 TTF and stage19 HHLL rhyme).",
        "- **BTC LEAD & Density:** Keep dense trades (n >> 9) without over-damp collapse (stage12/15/18) or ETH wipe (stage13/17).",
        "- **SOL & BNB Retention:** Multi-dozen participation on SOL and quiet-wipe protection on BNB.",
        "- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke (CRITICAL) logged; retention_notes checked across ladder.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-19 IDs, no DPO/PPO/VHF/FOSC/PO, no HA/MDI/DSS/III/PMA, no BandPass/HP/3LB/SI/Kagi, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no HHLL/STARC/VZO/NVI/FDI, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Volume Price Confirmation Indicator (`vpci-zero-cross`):** Dormeier VPCI x 0. (5,20) preferred; (8,20), (5,25). Mode A VPCI x 0; Mode B sig=10. != VZO / != III / != CMF / != OBV.",
        "- **Bill Williams MFI Green/Fade Flip (`bw-mfi-green-fade-flip`):** Green+dir edge entry / Fade exit. confirmBars=1 preferred; confirmBars=2, confirmBars=3. Mode A Green+bull edge / Fade exit; Mode B not green exit. != AO / != Money Flow Index.",
        "- **James Sibbet Demand Index (`demand-index-zero`):** Sierra Chart locked DI x 0. (10,10) preferred; (8,5), (14,14). Mode A DI x 0; Mode B hold > +5. != VZO / != Bostian III.",
        "- **Simple 1D Kalman Filter (`kalman-estimate-cross`):** close x recursive estimate cross. (20,0.01,0.1) preferred; (14,0.01,0.05), (30,0.02,0.1). Mode A close x est; Mode B slope gate. != Nadaraya / != PMA / != SuperSmoother.",
        "- **Chande RAVI Threshold x Dir (`ravi-threshold-dir`):** RAVI > thr x close dir. (7,65,3.0,3) preferred; (7,40,3.0,3), (5,40,2.0,1). Mode A rising edge; Mode B thr=4.0 dir=5. != dual-MA cross / != VHF / != FDI.",
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

    lines.extend([
        "",
        "## Ladder Promotion Rules",
        "",
        "1. **BTC:** Evaluated on all 40 cells (5 strategies × 2 TFs × 4 parameter sets).",
        "2. **ETH:** Evaluated ONLY on cells with `PASS_6m == PASS` on BTC. Pruned cells marked skipped (N/A).",
        "3. **SOL:** Evaluated ONLY on cells with `PASS_6m == PASS` on ETH.",
        "4. **BNB:** Evaluated ONLY on cells with `PASS_6m == PASS` on SOL.",
        "",
        "## Scoreboard Table",
        "",
        "| Symbol | Strategy ID | TF | Params | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Retention | 6m Trades | 6m WR% | 6m Ret% | 6m B&H% | 6m xB&H | 6m Gate | Full Trades | Full WR% | Full Ret% | Full B&H% | Full xB&H | Full Gate | 6m Ops% | Full Ops% | Notes |",
        "|--------|-------------|----|--------|-----------|-----------|-----------|-----------|-----------|-----------|--------|---------|---------|---------|---------|-------------|----------|-----------|-----------|-----------|-----------|---------|-----------|-------|",
    ])

    csv_rows: list[list[str]] = [
        [
            "symbol",
            "strategy_id",
            "tf",
            "mode_params",
            "btc_smoke",
            "eth_smoke",
            "sol_smoke",
            "bnb_smoke",
            "retention_notes",
            "gate_6m_trades",
            "gate_6m_wr_pct",
            "gate_6m_ret_pct",
            "gate_6m_bh_ret_pct",
            "gate_6m_ratio",
            "gate_6m_label",
            "gate_full_trades",
            "gate_full_wr_pct",
            "gate_full_ret_pct",
            "gate_full_bh_ret_pct",
            "gate_full_ratio",
            "gate_full_label",
            "ops_6m_ret_pct",
            "ops_full_ret_pct",
            "notes",
        ]
    ]

    for r in results:
        md_cols, csv_cols = _row_to_cols(r)
        lines.append("| " + " | ".join(md_cols) + " |")
        csv_rows.append(csv_cols)

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
