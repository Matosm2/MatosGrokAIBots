"""stage29-dual-sol-bnb-v1 harness: Sweep and score strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (4 strategies):
1. katsanos-stiffness-threshold
2. cpr-range-break-accept
3. varadi-dvs-stretch-midline
4. historical-volatility-ratio-expand-dir

Design Bias:
  BTC LEAD PRIMARY CRITICAL — clear past Vervoort 0.832x / FVE 1.055x to >= 1.20 without over-damp.
  Keep ETH denser n >> 9 secondary once BTC clears.
  SOL-after + BNB-survival tertiary.
  EXIT stage28 ECxEMA / Vervoort ZL-HAxTyp / ZL-FIR / DV2.
  Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
  btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
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
from backtest.path_b.stage29_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.katsanos_stiffness_threshold_v1 import (
    KatsanosStiffnessParams,
    compute_signals as stiffness_signals,
    validate_bnb_smoke as validate_stiffness_bnb_smoke,
    validate_btc_smoke as validate_stiffness_btc_smoke,
    validate_eth_smoke as validate_stiffness_eth_smoke,
    validate_sol_smoke as validate_stiffness_sol_smoke,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.cpr_range_break_accept_v1 import (
    CprRangeParams,
    compute_signals as cpr_signals,
    validate_bnb_smoke as validate_cpr_bnb_smoke,
    validate_btc_smoke as validate_cpr_btc_smoke,
    validate_eth_smoke as validate_cpr_eth_smoke,
    validate_sol_smoke as validate_cpr_sol_smoke,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.varadi_dvs_stretch_midline_v1 import (
    VaradiDvsParams,
    compute_signals as dvs_signals,
    validate_bnb_smoke as validate_dvs_bnb_smoke,
    validate_btc_smoke as validate_dvs_btc_smoke,
    validate_eth_smoke as validate_dvs_eth_smoke,
    validate_sol_smoke as validate_dvs_sol_smoke,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.historical_volatility_ratio_expand_dir_v1 import (
    HvrExpandDirParams,
    compute_signals as hvr_signals,
    validate_bnb_smoke as validate_hvr_bnb_smoke,
    validate_btc_smoke as validate_hvr_btc_smoke,
    validate_eth_smoke as validate_hvr_eth_smoke,
    validate_sol_smoke as validate_hvr_sol_smoke,
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
    retention_notes: str = "—"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    tiny_n_kill: bool = False
    thin_n_flag: bool = False
    notes: list[str] = field(default_factory=list)
    skipped: bool = False
    error: str | None = None


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc)
    target_dt = now.timestamp() - (months * 30.4375 * 86400)
    return int(target_dt * 1000)


def _mask_buys_before(buys: list[bool], bars: list[Bar], start_ms: int) -> list[bool]:
    masked = list(buys)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            masked[i] = False
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

    if cell.symbol == "BTCUSDT":
        cell.notes.append("BTC LEAD PRIMARY CRITICAL")
    elif cell.symbol == "ETHUSDT":
        cell.notes.append("ETH secondary (eth_smoke; denser n >> 9)")
        if prior_cell and prior_cell.metrics:
            btc_g6 = next(m for m in prior_cell.metrics if m.window == "6m" and m.mode == "gate")
            if btc_g6.trades > 0 and g6.trades == 0:
                cell.retention_notes = "ETH RETENTION FAIL: 0 ETH trades vs BTC trades"
            elif btc_g6.trades > 0 and g6.trades < max(5, btc_g6.trades // 4):
                cell.retention_notes = f"ETH RETENTION WARN: ETH n={g6.trades} < 25% of BTC n={btc_g6.trades}"
            else:
                cell.retention_notes = f"OK (ETH n={g6.trades} vs BTC n={btc_g6.trades})"
    elif cell.symbol == "SOLUSDT":
        cell.notes.append("SOL hard filter (sol_smoke)")
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


def _make_pruned_cell(
    symbol: str,
    sid: str,
    tf: str,
    desc: str,
    prune_reason: str = "Pruned by stop-ladder",
) -> CellResult:
    prior_coin = "BTC" if symbol == "ETHUSDT" else ("ETH" if symbol == "SOLUSDT" else "SOL")
    return CellResult(
        symbol=symbol,
        strategy_id=sid,
        tf=tf,
        mode_params=desc,
        gate_6m="FAIL",
        gate_full="FAIL",
        btc_smoke="Y",
        eth_smoke="Y",
        sol_smoke="Y",
        bnb_smoke="Y",
        retention_notes="—",
        metrics=[],
        notes=[f"{prune_reason} ({prior_coin} PASS_6m required)"],
        skipped=True,
    )


def _print_cell(cell: CellResult) -> None:
    if cell.skipped:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> PRUNED ({'; '.join(cell.notes)})", flush=True)
        return
    if cell.error:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> ERROR: {cell.error}", flush=True)
        return
    g6 = next((m for m in cell.metrics if m.window == "6m" and m.mode == "gate"), None)
    gf = next((m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
    if not g6 or not gf:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> NO METRICS", flush=True)
        return
    tiny_tag = " [TINY-N KILL]" if cell.tiny_n_kill else (" [THIN-N]" if cell.thin_n_flag else "")
    print(
        f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> "
        f"6m={cell.gate_6m}({g6.ratio:.3f}x){tiny_tag} ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [btc_smoke={cell.btc_smoke}, eth_smoke={cell.eth_smoke}, sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}, retention={cell.retention_notes}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: katsanos-stiffness-threshold
# ---------------------------------------------------------------------------

def run_katsanos_stiffness_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "katsanos-stiffness-threshold"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, KatsanosStiffnessParams]] = [
        ("mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50)", KatsanosStiffnessParams(mode="mode_a", mab=100, period=60, nstd=0.2, sm=3, buy_thr=90.0, sell_thr=50.0)),
        ("mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50)", KatsanosStiffnessParams(mode="mode_a", mab=50, period=40, nstd=0.2, sm=3, buy_thr=90.0, sell_thr=50.0)),
        ("mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50)", KatsanosStiffnessParams(mode="mode_a", mab=100, period=80, nstd=0.2, sm=3, buy_thr=90.0, sell_thr=50.0)),
        ("mode_b|(mab100,p60,buy95,sell50)", KatsanosStiffnessParams(mode="mode_b", mab=100, period=60, nstd=0.2, sm=3, buy_thr=95.0, sell_thr=50.0, rising_req=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                pruned = _make_pruned_cell(symbol, sid, tf, desc)
                _print_cell(pruned)
                results.append(pruned)
                continue

            btc_ok, btc_msg = validate_stiffness_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_stiffness_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_stiffness_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_stiffness_bnb_smoke(p, tf)
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

            try:
                buys, sells, stops = stiffness_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f
                prior = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: cpr-range-break-accept
# ---------------------------------------------------------------------------

def run_cpr_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "cpr-range-break-accept"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, CprRangeParams]] = [
        ("mode_a|(N24)", CprRangeParams(mode="mode_a", n=24)),
        ("mode_a|(N12)", CprRangeParams(mode="mode_a", n=12)),
        ("mode_a|(N48)", CprRangeParams(mode="mode_a", n=48)),
        ("mode_b|(N24,narrow0.002)", CprRangeParams(mode="mode_b", n=24, narrow_pct=0.002)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                pruned = _make_pruned_cell(symbol, sid, tf, desc)
                _print_cell(pruned)
                results.append(pruned)
                continue

            btc_ok, btc_msg = validate_cpr_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_cpr_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_cpr_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_cpr_bnb_smoke(p, tf)
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

            try:
                buys, sells, stops = cpr_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f
                prior = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: varadi-dvs-stretch-midline
# ---------------------------------------------------------------------------

def run_dvs_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "varadi-dvs-stretch-midline"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, VaradiDvsParams]] = [
        ("mode_a|(sum20,rank100,mid50)", VaradiDvsParams(mode="mode_a", sum_len=20, rank_len=100, mid=50.0)),
        ("mode_a|(sum10,rank63,mid50)", VaradiDvsParams(mode="mode_a", sum_len=10, rank_len=63, mid=50.0)),
        ("mode_a|(sum40,rank126,mid50)", VaradiDvsParams(mode="mode_a", sum_len=40, rank_len=126, mid=50.0)),
        ("mode_b|(sum20,rank100,rec40_exit50)", VaradiDvsParams(mode="mode_b", sum_len=20, rank_len=100, entry_thr_b=40.0, mid=50.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                pruned = _make_pruned_cell(symbol, sid, tf, desc)
                _print_cell(pruned)
                results.append(pruned)
                continue

            btc_ok, btc_msg = validate_dvs_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_dvs_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_dvs_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_dvs_bnb_smoke(p, tf)
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

            try:
                buys, sells, stops = dvs_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f
                prior = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: historical-volatility-ratio-expand-dir
# ---------------------------------------------------------------------------

def run_hvr_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "historical-volatility-ratio-expand-dir"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, HvrExpandDirParams]] = [
        ("mode_a|(s10,l100,exp0.5,dir5)", HvrExpandDirParams(mode="mode_a", short_len=10, long_len=100, expand_thr=0.5, dir_len=5)),
        ("mode_a|(s6,l50,exp0.4,dir3)", HvrExpandDirParams(mode="mode_a", short_len=6, long_len=50, expand_thr=0.4, dir_len=3)),
        ("mode_a|(s14,l100,exp0.6,dir8)", HvrExpandDirParams(mode="mode_a", short_len=14, long_len=100, expand_thr=0.6, dir_len=8)),
        ("mode_b|(s10,l100,exp0.5,dir5,comp0.5)", HvrExpandDirParams(mode="mode_b", short_len=10, long_len=100, expand_thr=0.5, dir_len=5, comp_thr=0.5)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                pruned = _make_pruned_cell(symbol, sid, tf, desc)
                _print_cell(pruned)
                results.append(pruned)
                continue

            btc_ok, btc_msg = validate_hvr_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_hvr_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_hvr_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_hvr_bnb_smoke(p, tf)
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

            try:
                buys, sells, stops = hvr_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f
                prior = prior_results.get(cell_key) if prior_results else None
                cell = _finish(cell, prior)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Stop-Ladder Orchestration
# ---------------------------------------------------------------------------

def run_stage29_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []
    active_keys: set[str] | None = None
    prior_results_by_key: dict[str, CellResult] = {}

    for stage_idx, symbol in enumerate(symbols):
        print(f"\n{'='*70}\n[stage29-dual-sol-bnb-v1] STAGE {stage_idx+1}/{len(symbols)}: {symbol}\n{'='*70}", flush=True)

        print(f"Loading data for {symbol} (1h, 4h, {years}y)...", flush=True)
        res = materialize_symbol(symbol=symbol, tfs=("1h", "4h"), years=years, refresh=refresh)
        bars_by_tf: dict[str, list[Bar]] = {
            "1h": res["1h"],
            "4h": res["4h"],
        }
        for tf in ("1h", "4h"):
            print(f"Loaded {len(bars_by_tf[tf])} bars for {symbol} @ {tf}", flush=True)

        stage_cells: list[CellResult] = []

        # 1. katsanos-stiffness-threshold
        stage_cells.extend(run_katsanos_stiffness_cells(symbol, bars_by_tf, active_keys, prior_results_by_key))

        # 2. cpr-range-break-accept
        stage_cells.extend(run_cpr_cells(symbol, bars_by_tf, active_keys, prior_results_by_key))

        # 3. varadi-dvs-stretch-midline
        stage_cells.extend(run_dvs_cells(symbol, bars_by_tf, active_keys, prior_results_by_key))

        # 4. historical-volatility-ratio-expand-dir
        stage_cells.extend(run_hvr_cells(symbol, bars_by_tf, active_keys, prior_results_by_key))

        all_results.extend(stage_cells)

        passed_this_stage = [
            c for c in stage_cells
            if not c.skipped and not c.error and c.gate_6m == "PASS"
        ]

        print(
            f"\n[stage29-dual-sol-bnb-v1] {symbol} STAGE SUMMARY: "
            f"{len(passed_this_stage)}/{len([c for c in stage_cells if not c.skipped])} passed 6m gate.",
            flush=True,
        )

        active_keys = {
            f"{c.strategy_id}@{c.tf}@{c.mode_params}"
            for c in passed_this_stage
        }
        prior_results_by_key = {
            f"{c.strategy_id}@{c.tf}@{c.mode_params}": c
            for c in stage_cells
            if not c.skipped
        }

        if not active_keys and stage_idx < len(symbols) - 1:
            print(
                f"[stage29-dual-sol-bnb-v1] No strategy passed {symbol} 6m gate. "
                f"Subsequent coins will be marked PRUNED in scoreboard.",
                flush=True,
            )

    return all_results


def write_scoreboard(results: list[CellResult]) -> tuple[Path, Path]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / f"{RESEARCH_ID}-scoreboard.csv"
    md_path = RESULTS_DIR / f"{RESEARCH_ID}-scoreboard.md"

    csv_rows: list[dict[str, str]] = []
    for r in results:
        g6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "gate"), None)
        gf = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
        o6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "ops"), None)
        of = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"), None)

        csv_rows.append({
            "symbol": r.symbol,
            "strategy_id": r.strategy_id,
            "tf": r.tf,
            "mode_params": r.mode_params,
            "gate_6m": r.gate_6m,
            "gate_full": r.gate_full,
            "ret_6m_pct": f"{g6.return_pct:.2f}" if g6 else "—",
            "bh_6m_pct": f"{g6.bh_return_pct:.2f}" if g6 else "—",
            "ratio_6m": f"{g6.ratio:.3f}" if g6 else "—",
            "n_6m": str(g6.trades) if g6 else "—",
            "wr_6m_pct": f"{g6.win_rate_pct:.1f}" if g6 else "—",
            "max_dd_6m_pct": f"{g6.max_drawdown_pct:.2f}" if g6 else "—",
            "ret_full_pct": f"{gf.return_pct:.2f}" if gf else "—",
            "bh_full_pct": f"{gf.bh_return_pct:.2f}" if gf else "—",
            "ratio_full": f"{gf.ratio:.3f}" if gf else "—",
            "n_full": str(gf.trades) if gf else "—",
            "wr_full_pct": f"{gf.win_rate_pct:.1f}" if gf else "—",
            "max_dd_full_pct": f"{gf.max_drawdown_pct:.2f}" if gf else "—",
            "ops_ret_6m_pct": f"{o6.return_pct:.2f}" if o6 else "—",
            "ops_ret_full_pct": f"{of.return_pct:.2f}" if of else "—",
            "btc_smoke": r.btc_smoke,
            "eth_smoke": r.eth_smoke,
            "sol_smoke": r.sol_smoke,
            "bnb_smoke": r.bnb_smoke,
            "retention_notes": r.retention_notes,
            "notes": "; ".join(r.notes) if r.notes else "—",
        })

    fieldnames = [
        "symbol", "strategy_id", "tf", "mode_params", "gate_6m", "gate_full",
        "ret_6m_pct", "bh_6m_pct", "ratio_6m", "n_6m", "wr_6m_pct", "max_dd_6m_pct",
        "ret_full_pct", "bh_full_pct", "ratio_full", "n_full", "wr_full_pct", "max_dd_full_pct",
        "ops_ret_6m_pct", "ops_ret_full_pct",
        "btc_smoke", "eth_smoke", "sol_smoke", "bnb_smoke", "retention_notes", "notes",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    # Markdown generation
    pass_6m_list = [
        r for r in results
        if not r.skipped and not r.error and r.gate_6m == "PASS"
    ]
    full_ladder_passes = []
    passed_symbols_by_candidate: dict[str, list[str]] = {}
    for r in results:
        if r.gate_6m == "PASS":
            cand = f"{r.strategy_id}@{r.tf}@{r.mode_params}"
            passed_symbols_by_candidate.setdefault(cand, []).append(r.symbol)

    for cand, syms in passed_symbols_by_candidate.items():
        if len(syms) == len(DEFAULT_SYMBOLS):
            full_ladder_passes.append(cand)

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        f"# {RESEARCH_ID} — Scoreboard",
        "",
        f"- Generated: {now_str}",
        f"- Research ID: `{RESEARCH_ID}` (Track 1 Path B)",
        f"- Stop-Ladder: `BTCUSDT -> ETHUSDT (HARD) -> SOLUSDT (HARD) -> BNBUSDT (HARD)`",
        f"- Gate Rule: Last 6m Mode-A Return >= {GATE_MULT}x Buy & Hold, n > {TINY_N_THRESHOLD} (tiny-n kill threshold)",
        f"- Fees / Slip: {FEE*100:.2f}% / side fee + {SLIP*100:.2f}% adverse slippage",
        f"- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)",
        f"- Strategy Encode Order (exactly 4):",
        f"  1. `katsanos-stiffness-threshold`",
        f"  2. `cpr-range-break-accept`",
        f"  3. `varadi-dvs-stretch-midline`",
        f"  4. `historical-volatility-ratio-expand-dir`",
        "",
        "## Executive Summary",
        f"- Total Scored Cells: {len([r for r in results if not r.skipped])} / {len(results)}",
        f"- Pruned / Skipped by Stop-Ladder: {len([r for r in results if r.skipped])}",
        f"- Candidates Passing 6m Gate on at least 1 symbol: {len(pass_6m_list)}",
        f"- Full 4-Coin Ladder Complete Passes: {len(full_ladder_passes)}",
        "",
        "## PASS_6m Promoted Candidates",
    ]

    if pass_6m_list:
        lines.append("| Symbol | Strategy ID | TF | Mode/Params | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | Notes |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in pass_6m_list:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | {r.mode_params} | "
                f"{g6.return_pct:.2f}% | {g6.bh_return_pct:.2f}% | {g6.ratio:.3f}x | {g6.trades} | {g6.win_rate_pct:.1f}% | {'; '.join(r.notes)} |"
            )
    else:
        lines.append("- *None. Zero candidates met the 6m >= 1.2x B&H hurdle with n > 5.*")

    lines.extend([
        "",
        "## Full Stop-Ladder Scoreboard",
        "",
        "| Symbol | Strategy ID | TF | Mode/Params | 6m Gate | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | 6m MaxDD% | Full Gate | Full Ret% | Full B&H% | Full xB&H | Full n | Ops 6m% | Ops Full% | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Retention Notes | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])

    for r in results:
        g6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "gate"), None)
        gf = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
        o6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "ops"), None)
        of = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"), None)

        ret_6m = f"{g6.return_pct:.2f}%" if g6 else "—"
        bh_6m = f"{g6.bh_return_pct:.2f}%" if g6 else "—"
        ratio_6m = f"{g6.ratio:.3f}x" if g6 else "—"
        n_6m = str(g6.trades) if g6 else "—"
        wr_6m = f"{g6.win_rate_pct:.1f}%" if g6 else "—"
        dd_6m = f"{g6.max_drawdown_pct:.2f}%" if g6 else "—"

        ret_full = f"{gf.return_pct:.2f}%" if gf else "—"
        bh_full = f"{gf.bh_return_pct:.2f}%" if gf else "—"
        ratio_full = f"{gf.ratio:.3f}x" if gf else "—"
        n_full = str(gf.trades) if gf else "—"

        ops_6m = f"{o6.return_pct:.2f}%" if o6 else "—"
        ops_full = f"{of.return_pct:.2f}%" if of else "—"

        notes_str = "; ".join(r.notes) if r.notes else "—"

        lines.append(
            f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | {r.mode_params} | "
            f"**{r.gate_6m}** | {ret_6m} | {bh_6m} | {ratio_6m} | {n_6m} | {wr_6m} | {dd_6m} | "
            f"{r.gate_full} | {ret_full} | {bh_full} | {ratio_full} | {n_full} | "
            f"{ops_6m} | {ops_full} | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | "
            f"{r.retention_notes} | {notes_str} |"
        )

    lines.append("")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return md_path, csv_path
