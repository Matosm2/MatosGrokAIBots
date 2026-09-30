"""stage22-dual-sol-bnb-v1 harness: Sweep and score strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (4 strategies):
1. percentile-channel-break
2. zscore-threshold-hold
3. anchored-vwap-swing-flip
4. katsanos-vfi-zero-cross (PRIORITY KILL IF BTC CHOP like stage20 volume)

Design Bias:
  BTC LEAD PRIMARY without over-damp (stage12/15/18/20/21 rhyme).
  Prefer denser n >> 9. Keep ETH/SOL/BNB lessons.
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
from backtest.path_b.stage22_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.percentile_channel_break_v1 import (
    PercentileChannelParams,
    compute_signals as percentile_signals,
    validate_bnb_smoke as validate_percentile_bnb_smoke,
    validate_btc_smoke as validate_percentile_btc_smoke,
    validate_eth_smoke as validate_percentile_eth_smoke,
    validate_sol_smoke as validate_percentile_sol_smoke,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.zscore_threshold_hold_v1 import (
    ZscoreParams,
    compute_signals as zscore_signals,
    validate_bnb_smoke as validate_zscore_bnb_smoke,
    validate_btc_smoke as validate_zscore_btc_smoke,
    validate_eth_smoke as validate_zscore_eth_smoke,
    validate_sol_smoke as validate_zscore_sol_smoke,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.anchored_vwap_swing_flip_v1 import (
    AnchoredVwapParams,
    compute_signals as vwap_signals,
    validate_bnb_smoke as validate_vwap_bnb_smoke,
    validate_btc_smoke as validate_vwap_btc_smoke,
    validate_eth_smoke as validate_vwap_eth_smoke,
    validate_sol_smoke as validate_vwap_sol_smoke,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.katsanos_vfi_zero_cross_v1 import (
    VfiParams,
    compute_signals as vfi_signals,
    validate_bnb_smoke as validate_vfi_bnb_smoke,
    validate_btc_smoke as validate_vfi_btc_smoke,
    validate_eth_smoke as validate_vfi_eth_smoke,
    validate_sol_smoke as validate_vfi_sol_smoke,
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


def _make_pruned_cell(symbol: str, sid: str, tf: str, desc: str) -> CellResult:
    prior_sym = "BTC" if symbol == "ETHUSDT" else ("ETH" if symbol == "SOLUSDT" else "SOL")
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
        skipped=True,
        notes=[f"Pruned by stop-ladder ({prior_sym} PASS_6m required)"],
    )


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
# Strategy 1: percentile-channel-break
# ---------------------------------------------------------------------------

def run_percentile_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "percentile-channel-break"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, PercentileChannelParams]] = [
        ("mode_a|(len50,p90,p10)", PercentileChannelParams(mode="mode_a", length=50, p_hi=90.0, p_lo=10.0)),
        ("mode_a|(len70,p90,p10)", PercentileChannelParams(mode="mode_a", length=70, p_hi=90.0, p_lo=10.0)),
        ("mode_a|(len50,p95,p5)", PercentileChannelParams(mode="mode_a", length=50, p_hi=95.0, p_lo=5.0)),
        ("mode_b|(len50,p90,p10,wpr50)", PercentileChannelParams(mode="mode_b", length=50, p_hi=90.0, p_lo=10.0)),
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

            btc_ok, btc_msg = validate_percentile_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_percentile_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_percentile_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_percentile_bnb_smoke(p, tf)
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
                cell.notes.append(f"Smoke check failed: btc={btc_msg}, eth={eth_msg}, sol={sol_msg}, bnb={bnb_msg}")
                _print_cell(cell)
                results.append(cell)
                continue

            buys, sells, stops = percentile_signals(bars, p)
            prior_cell = prior_results.get(cell_key) if prior_results else None
            metrics, tiny_k, thin_f = _eval_windows(
                symbol=symbol,
                sid=sid,
                bars=bars,
                buys=buys,
                sells=sells,
                stops=stops,
            )
            cell.metrics = metrics
            cell.tiny_n_kill = tiny_k
            cell.thin_n_flag = thin_f
            finished = _finish(cell, prior_cell)
            _print_cell(finished)
            results.append(finished)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: zscore-threshold-hold
# ---------------------------------------------------------------------------

def run_zscore_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "zscore-threshold-hold"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, ZscoreParams]] = [
        ("mode_a|(len20,thr1.0,exit0.0)", ZscoreParams(mode="mode_a", length=20, thr=1.0, exit_thr=0.0)),
        ("mode_a|(len30,thr1.0,exit0.0)", ZscoreParams(mode="mode_a", length=30, thr=1.0, exit_thr=0.0)),
        ("mode_a|(len20,thr1.5,exit0.5)", ZscoreParams(mode="mode_a", length=20, thr=1.5, exit_thr=0.5)),
        ("mode_b|(len20,thr1.0,exit0.0,rising)", ZscoreParams(mode="mode_b", length=20, thr=1.0, exit_thr=0.0)),
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

            btc_ok, btc_msg = validate_zscore_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_zscore_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_zscore_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_zscore_bnb_smoke(p, tf)
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
                cell.notes.append(f"Smoke check failed: btc={btc_msg}, eth={eth_msg}, sol={sol_msg}, bnb={bnb_msg}")
                _print_cell(cell)
                results.append(cell)
                continue

            buys, sells, stops = zscore_signals(bars, p)
            prior_cell = prior_results.get(cell_key) if prior_results else None
            metrics, tiny_k, thin_f = _eval_windows(
                symbol=symbol,
                sid=sid,
                bars=bars,
                buys=buys,
                sells=sells,
                stops=stops,
            )
            cell.metrics = metrics
            cell.tiny_n_kill = tiny_k
            cell.thin_n_flag = thin_f
            finished = _finish(cell, prior_cell)
            _print_cell(finished)
            results.append(finished)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: anchored-vwap-swing-flip
# ---------------------------------------------------------------------------

def run_vwap_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "anchored-vwap-swing-flip"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, AnchoredVwapParams]] = [
        ("mode_a|(pivot5,5,age0)", AnchoredVwapParams(mode="mode_a", pivot_l=5, pivot_r=5, min_age=0)),
        ("mode_a|(pivot8,8,age0)", AnchoredVwapParams(mode="mode_a", pivot_l=8, pivot_r=8, min_age=0)),
        ("mode_a|(pivot5,5,age3)", AnchoredVwapParams(mode="mode_a", pivot_l=5, pivot_r=5, min_age=3)),
        ("mode_b|(pivot5,5,age3,gate)", AnchoredVwapParams(mode="mode_b", pivot_l=5, pivot_r=5, min_age=3)),
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

            btc_ok, btc_msg = validate_vwap_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_vwap_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_vwap_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_vwap_bnb_smoke(p, tf)
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
                cell.notes.append(f"Smoke check failed: btc={btc_msg}, eth={eth_msg}, sol={sol_msg}, bnb={bnb_msg}")
                _print_cell(cell)
                results.append(cell)
                continue

            buys, sells, stops = vwap_signals(bars, p)
            prior_cell = prior_results.get(cell_key) if prior_results else None
            metrics, tiny_k, thin_f = _eval_windows(
                symbol=symbol,
                sid=sid,
                bars=bars,
                buys=buys,
                sells=sells,
                stops=stops,
            )
            cell.metrics = metrics
            cell.tiny_n_kill = tiny_k
            cell.thin_n_flag = thin_f
            finished = _finish(cell, prior_cell)
            _print_cell(finished)
            results.append(finished)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: katsanos-vfi-zero-cross
# ---------------------------------------------------------------------------

def run_vfi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "katsanos-vfi-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, VfiParams]] = [
        ("mode_a|(per80,c0.1,vc2.5,sm3)", VfiParams(mode="mode_a", period=80, coef=0.1, vcoef=2.5, smooth=3)),
        ("mode_a|(per50,c0.1,vc2.5,sm3)", VfiParams(mode="mode_a", period=50, coef=0.1, vcoef=2.5, smooth=3)),
        ("mode_a|(per80,c0.2,vc2.5,sm3)", VfiParams(mode="mode_a", period=80, coef=0.2, vcoef=2.5, smooth=3)),
        ("mode_b|(per80,c0.1,vc2.5,sm3,sig10)", VfiParams(mode="mode_b", period=80, coef=0.1, vcoef=2.5, smooth=3, sig_len=10)),
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

            btc_ok, btc_msg = validate_vfi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_vfi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_vfi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_vfi_bnb_smoke(p, tf)
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
                cell.notes.append(f"Smoke check failed: btc={btc_msg}, eth={eth_msg}, sol={sol_msg}, bnb={bnb_msg}")
                _print_cell(cell)
                results.append(cell)
                continue

            buys, sells, stops = vfi_signals(bars, p)
            prior_cell = prior_results.get(cell_key) if prior_results else None
            metrics, tiny_k, thin_f = _eval_windows(
                symbol=symbol,
                sid=sid,
                bars=bars,
                buys=buys,
                sells=sells,
                stops=stops,
            )
            cell.metrics = metrics
            cell.tiny_n_kill = tiny_k
            cell.thin_n_flag = thin_f
            finished = _finish(cell, prior_cell)
            _print_cell(finished)
            results.append(finished)

    return results


# ---------------------------------------------------------------------------
# Main Ladder Runner: BTC -> ETH -> SOL -> BNB
# ---------------------------------------------------------------------------

def run_stage22_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
    vfi_dropped: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []
    needed_tfs = ("1h", "4h")

    # Step 1: Pre-fetch & materialize data
    bars_by_symbol_and_tf: dict[str, dict[str, list[Bar]]] = {}
    for sym in symbols:
        print(f"\n[stage22-dual-sol-bnb-v1] Materializing OHLCV for {sym} (1h, 4h)...", flush=True)
        bars_by_symbol_and_tf[sym] = materialize_symbol(sym, tfs=needed_tfs, years=years, refresh=refresh)

    # Active cell keys for ladder filtering: None at start (all candidates run on BTC)
    active_keys: set[str] | None = None
    prior_results_by_key: dict[str, CellResult] = {}

    all_defined_keys: list[tuple[str, str, str]] = []
    for tf in ("1h", "4h"):
        for desc in [
            "mode_a|(len50,p90,p10)", "mode_a|(len70,p90,p10)", "mode_a|(len50,p95,p5)", "mode_b|(len50,p90,p10,wpr50)"
        ]:
            all_defined_keys.append(("percentile-channel-break", tf, desc))
        for desc in [
            "mode_a|(len20,thr1.0,exit0.0)", "mode_a|(len30,thr1.0,exit0.0)", "mode_a|(len20,thr1.5,exit0.5)", "mode_b|(len20,thr1.0,exit0.0,rising)"
        ]:
            all_defined_keys.append(("zscore-threshold-hold", tf, desc))
        for desc in [
            "mode_a|(pivot5,5,age0)", "mode_a|(pivot8,8,age0)", "mode_a|(pivot5,5,age3)", "mode_b|(pivot5,5,age3,gate)"
        ]:
            all_defined_keys.append(("anchored-vwap-swing-flip", tf, desc))
        if not vfi_dropped:
            for desc in [
                "mode_a|(per80,c0.1,vc2.5,sm3)", "mode_a|(per50,c0.1,vc2.5,sm3)", "mode_a|(per80,c0.2,vc2.5,sm3)", "mode_b|(per80,c0.1,vc2.5,sm3,sig10)"
            ]:
                all_defined_keys.append(("katsanos-vfi-zero-cross", tf, desc))

    for sym_idx, symbol in enumerate(symbols):
        print(f"\n{'='*70}\n[stage22-dual-sol-bnb-v1] RUNNING LADDER STEP {sym_idx+1}/{len(symbols)}: {symbol}\n{'='*70}", flush=True)
        bars = bars_by_symbol_and_tf[symbol]
        sym_results: list[CellResult] = []

        if active_keys is not None and len(active_keys) == 0:
            print(f"[{symbol}] Ladder stopped: 0 active cells promoted from previous step. Recording all as pruned.", flush=True)
            for sid, tf, desc in all_defined_keys:
                if vfi_dropped and sid == "katsanos-vfi-zero-cross":
                    continue
                pruned_cell = _make_pruned_cell(symbol, sid, tf, desc)
                sym_results.append(pruned_cell)
                all_results.append(pruned_cell)
        else:
            # 1. Percentile Channel Break
            res = run_percentile_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
            sym_results.extend(res)
            all_results.extend(res)

            # 2. Z-Score Threshold Hold
            res = run_zscore_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
            sym_results.extend(res)
            all_results.extend(res)

            # 3. Anchored VWAP Swing Flip
            res = run_vwap_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
            sym_results.extend(res)
            all_results.extend(res)

            # 4. Katsanos VFI Zero Cross (if not dropped)
            if not vfi_dropped:
                res = run_vfi_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
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

def write_scoreboard(results: list[CellResult], vfi_dropped: bool = False, vfi_reason: str = "") -> tuple[Path, Path]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = RESULTS_DIR / "stage22-dual-sol-bnb-v1-scoreboard.md"
    csv_path = RESULTS_DIR / "stage22-dual-sol-bnb-v1-scoreboard.csv"

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
        "btc_smoke", "eth_smoke", "sol_smoke", "bnb_smoke", "retention_notes", "notes"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    # Markdown format
    md_lines: list[str] = [
        f"# Scoreboard: {RESEARCH_ID}",
        "",
        f"**Date (UTC):** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        "**Track:** Track 1 Path B (Track 2 Discord OFF-LIMITS)",
        "**Status:** RESEARCH / OPTIMISE ONLY — LIVE frozen",
        "**Design bias:** BTC LEAD PRIMARY without over-damp (stage12/15/18/20/21 rhyme). Denser n >> 9. Stop-ladder: BTC -> ETH -> SOL -> BNB.",
    ]
    if vfi_dropped:
        md_lines.append(f"**VFI Early-Kill Execution:** Strategy 4 (`katsanos-vfi-zero-cross`) DROPPED during/after BTC smoke. Reason: {vfi_reason}")
    else:
        md_lines.append("**VFI Early-Kill Execution:** Strategy 4 (`katsanos-vfi-zero-cross`) RETAINED.")

    md_lines.extend([
        "",
        "## Summary",
        "",
        f"- Total Scored Cells: {len([r for r in results if not r.skipped])}",
        f"- Total Skipped / Pruned Cells: {len([r for r in results if r.skipped])}",
        f"- BTC PASS_6m: {len([r for r in results if r.symbol == 'BTCUSDT' and r.gate_6m == 'PASS'])} / {len([r for r in results if r.symbol == 'BTCUSDT'])}",
        f"- ETH PASS_6m: {len([r for r in results if r.symbol == 'ETHUSDT' and r.gate_6m == 'PASS'])} / {len([r for r in results if r.symbol == 'ETHUSDT' and not r.skipped])}",
        f"- SOL PASS_6m: {len([r for r in results if r.symbol == 'SOLUSDT' and r.gate_6m == 'PASS'])} / {len([r for r in results if r.symbol == 'SOLUSDT' and not r.skipped])}",
        f"- BNB PASS_6m: {len([r for r in results if r.symbol == 'BNBUSDT' and r.gate_6m == 'PASS'])} / {len([r for r in results if r.symbol == 'BNBUSDT' and not r.skipped])}",
        "",
        "## Full Results Table",
        "",
        "| Symbol | Strategy ID | TF | Mode/Params | 6m Gate | 6m Ret | 6m B&H | xB&H | 6m n | 6m WR | Full Gate | Full Ret | Full xB&H | Ops 6m | Ops Full | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Notes |",
        "|--------|-------------|----|-------------|---------|--------|--------|------|------|------|-----------|----------|-----------|--------|----------|-----------|-----------|-----------|-----------|-------|",
    ])

    for r in results:
        g6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "gate"), None)
        gf = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
        o6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "ops"), None)
        of = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"), None)

        if r.skipped:
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | {'; '.join(r.notes)} |"
            )
        elif r.error:
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | ERROR | — | — | — | — | — | ERROR | — | — | — | — | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | {r.error} |"
            )
        else:
            assert g6 is not None and gf is not None and o6 is not None and of is not None
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | **{r.gate_6m}** | {g6.return_pct:.2f}% | {g6.bh_return_pct:.2f}% | {g6.ratio:.3f}x | {g6.trades} | {g6.win_rate_pct:.1f}% | {r.gate_full} | {gf.return_pct:.2f}% | {gf.ratio:.3f}x | {o6.return_pct:.2f}% | {of.return_pct:.2f}% | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | {'; '.join(r.notes)} |"
            )

    md_lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    return md_path, csv_path
