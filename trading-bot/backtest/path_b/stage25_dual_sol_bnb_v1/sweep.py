"""stage25-dual-sol-bnb-v1 harness: Sweep and score strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (4 strategies):
1. ehlers-dsp-zero-cross
2. nhnl-oscillator-zero
3. volume-roc-dir
4. elder-thermometer-cool-dir

Design Bias:
  BTC LEAD PRIMARY — push past Chande-Kroll ~1.194x / Kirshenbaum ~1.113x without over-damp.
  Denser n >> 9. Keep ETH/SOL/BNB lessons.
  EXIT stage24 Guppy-CBL / Kirshenbaum / IMI / Williams-AD.
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
from backtest.path_b.stage25_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.ehlers_dsp_zero_cross_v1 import (
    EhlersDspParams,
    compute_signals as dsp_signals,
    validate_bnb_smoke as validate_dsp_bnb_smoke,
    validate_btc_smoke as validate_dsp_btc_smoke,
    validate_eth_smoke as validate_dsp_eth_smoke,
    validate_sol_smoke as validate_dsp_sol_smoke,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.nhnl_oscillator_zero_v1 import (
    NhnlParams,
    compute_signals as nhnl_signals,
    validate_bnb_smoke as validate_nhnl_bnb_smoke,
    validate_btc_smoke as validate_nhnl_btc_smoke,
    validate_eth_smoke as validate_nhnl_eth_smoke,
    validate_sol_smoke as validate_nhnl_sol_smoke,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.volume_roc_dir_v1 import (
    VolumeRocParams,
    compute_signals as vroc_signals,
    validate_bnb_smoke as validate_vroc_bnb_smoke,
    validate_btc_smoke as validate_vroc_btc_smoke,
    validate_eth_smoke as validate_vroc_eth_smoke,
    validate_sol_smoke as validate_vroc_sol_smoke,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.elder_thermometer_cool_dir_v1 import (
    ElderThermometerParams,
    compute_signals as thermo_signals,
    validate_bnb_smoke as validate_thermo_bnb_smoke,
    validate_btc_smoke as validate_thermo_btc_smoke,
    validate_eth_smoke as validate_thermo_eth_smoke,
    validate_sol_smoke as validate_thermo_sol_smoke,
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
# Strategy 1: ehlers-dsp-zero-cross
# ---------------------------------------------------------------------------

def run_dsp_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-dsp-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, EhlersDspParams]] = [
        ("mode_a|(len7)", EhlersDspParams(mode="mode_a", length=7)),
        ("mode_a|(len5)", EhlersDspParams(mode="mode_a", length=5)),
        ("mode_a|(len9)", EhlersDspParams(mode="mode_a", length=9)),
        ("mode_a|(len14)", EhlersDspParams(mode="mode_a", length=14)),
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

            btc_ok, btc_msg = validate_dsp_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_dsp_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_dsp_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_dsp_bnb_smoke(p, tf)
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
                buys, sells, stops = dsp_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f

                prior_cell = prior_results.get(cell_key) if prior_results else None
                _finish(cell, prior_cell)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: nhnl-oscillator-zero
# ---------------------------------------------------------------------------

def run_nhnl_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "nhnl-oscillator-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, NhnlParams]] = [
        ("mode_a|(L20,W10)", NhnlParams(mode="mode_a", l=20, w=10)),
        ("mode_a|(L14,W5)", NhnlParams(mode="mode_a", l=14, w=5)),
        ("mode_a|(L20,W14)", NhnlParams(mode="mode_a", l=20, w=14)),
        ("mode_a|(L30,W10)", NhnlParams(mode="mode_a", l=30, w=10)),
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

            btc_ok, btc_msg = validate_nhnl_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_nhnl_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_nhnl_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_nhnl_bnb_smoke(p, tf)
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
                buys, sells, stops = nhnl_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f

                prior_cell = prior_results.get(cell_key) if prior_results else None
                _finish(cell, prior_cell)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: volume-roc-dir
# ---------------------------------------------------------------------------

def run_vroc_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "volume-roc-dir"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, VolumeRocParams]] = [
        ("mode_a|(n14,dir1)", VolumeRocParams(mode="mode_a", n=14, dir_len=1)),
        ("mode_a|(n10,dir1)", VolumeRocParams(mode="mode_a", n=10, dir_len=1)),
        ("mode_a|(n20,dir1)", VolumeRocParams(mode="mode_a", n=20, dir_len=1)),
        ("mode_a|(n14,dir3)", VolumeRocParams(mode="mode_a", n=14, dir_len=3)),
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

            btc_ok, btc_msg = validate_vroc_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_vroc_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_vroc_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_vroc_bnb_smoke(p, tf)
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
                buys, sells, stops = vroc_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f

                prior_cell = prior_results.get(cell_key) if prior_results else None
                _finish(cell, prior_cell)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: elder-thermometer-cool-dir
# ---------------------------------------------------------------------------

def run_thermo_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "elder-thermometer-cool-dir"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, ElderThermometerParams]] = [
        ("mode_a|(ema22,k3.0)", ElderThermometerParams(mode="mode_a", ema_len=22, k=3.0, dir_len=1)),
        ("mode_a|(ema14,k3.0)", ElderThermometerParams(mode="mode_a", ema_len=14, k=3.0, dir_len=1)),
        ("mode_a|(ema20,k2.5)", ElderThermometerParams(mode="mode_a", ema_len=20, k=2.5, dir_len=1)),
        ("mode_a|(ema22,k3.5)", ElderThermometerParams(mode="mode_a", ema_len=22, k=3.5, dir_len=1)),
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

            btc_ok, btc_msg = validate_thermo_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_thermo_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_thermo_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_thermo_bnb_smoke(p, tf)
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
                buys, sells, stops = thermo_signals(bars, p)
                metrics, tiny_k, thin_f = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell.tiny_n_kill = tiny_k
                cell.thin_n_flag = thin_f

                prior_cell = prior_results.get(cell_key) if prior_results else None
                _finish(cell, prior_cell)
            except Exception as e:
                cell.error = str(e)
                cell.gate_6m = "FAIL"
                cell.gate_full = "FAIL"

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Full Ladder Orchestrator
# ---------------------------------------------------------------------------

def run_stage25_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []

    print(f"\n{'='*70}\n[stage25-dual-sol-bnb-v1] Materializing OHLCV data for {symbols} ({years}y)...\n{'='*70}", flush=True)
    bars_by_symbol_and_tf: dict[str, dict[str, list[Bar]]] = {}
    needed_tfs = ("1h", "4h")
    for s in symbols:
        bars_by_symbol_and_tf[s] = materialize_symbol(s, tfs=needed_tfs, years=years, refresh=refresh)
        print(f"  -> {s}: 1h bars={len(bars_by_symbol_and_tf[s]['1h'])}, 4h bars={len(bars_by_symbol_and_tf[s]['4h'])}", flush=True)

    active_keys: set[str] | None = None  # None for BTC (all evaluated); pruned thereafter
    prior_results_by_key: dict[str, CellResult] = {}

    for stage_idx, symbol in enumerate(symbols):
        print(f"\n{'-'*70}\n[stage25-dual-sol-bnb-v1] Ladder Stage {stage_idx+1}/4: {symbol}\n{'-'*70}", flush=True)

        bars_by_tf = bars_by_symbol_and_tf[symbol]

        s1_cells = run_dsp_cells(symbol, bars_by_tf, active_keys, prior_results_by_key)
        s2_cells = run_nhnl_cells(symbol, bars_by_tf, active_keys, prior_results_by_key)
        s3_cells = run_vroc_cells(symbol, bars_by_tf, active_keys, prior_results_by_key)
        s4_cells = run_thermo_cells(symbol, bars_by_tf, active_keys, prior_results_by_key)

        stage_cells = s1_cells + s2_cells + s3_cells + s4_cells
        all_results.extend(stage_cells)

        # Evaluate passes to filter the ladder for next coin
        passed_this_stage = [
            c for c in stage_cells
            if not c.skipped and not c.error and c.gate_6m == "PASS"
        ]
        print(
            f"\n[stage25-dual-sol-bnb-v1] {symbol} Stage Summary: "
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
                f"[stage25-dual-sol-bnb-v1] No strategy passed {symbol} 6m gate. "
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

    md_lines: list[str] = [
        f"# Scoreboard: {RESEARCH_ID}",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Status:** Research / Optimise Only — LIVE FROZEN.",
        f"**Design Bias:** BTC LEAD PRIMARY — push past Chande-Kroll ~1.194x / Kirshenbaum ~1.113x without over-damp. Denser n >> 9. Keep ETH/SOL/BNB lessons. EXIT stage24 Guppy-CBL / Kirshenbaum / IMI / Williams-AD. Identical dual params.",
        "",
        "## Summary",
        f"- Total Scored Cells: {len([r for r in results if not r.skipped])}",
        f"- Total Pruned/Skipped Cells: {len([r for r in results if r.skipped])}",
        f"- Total PASS_6m: {len(pass_6m_list)}",
        "",
        "## PASS_6m Promoted Candidates",
    ]

    if not pass_6m_list:
        md_lines.append("*None. All candidates failed to clear >= 1.2x B&H on 6m or were pruned by ladder.*")
    else:
        md_lines.append("| Symbol | Strategy | TF | Mode/Params | 6m Ret% | 6m B&H% | xB&H | n_6m | WR% | MaxDD% | Smoke / Retention |")
        md_lines.append("|--------|----------|----|-------------|---------|---------|------|------|-----|--------|-------------------|")
        for r in pass_6m_list:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | "
                f"{g6.return_pct:.2f}% | {g6.bh_return_pct:.2f}% | {g6.ratio:.3f}x | {g6.trades} | "
                f"{g6.win_rate_pct:.1f}% | {g6.max_drawdown_pct:.2f}% | {r.retention_notes} |"
            )

    md_lines.extend([
        "",
        "## Full Ladder Results",
        "",
        "| Symbol | Strategy | TF | Mode/Params | 6m Gate | 6m Ret% | xB&H | n_6m | Full Ret% | xB&H Full | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Notes |",
        "|--------|----------|----|-------------|---------|---------|------|------|-----------|-----------|-----------|-----------|-----------|-----------|-------|",
    ])

    for r in results:
        if r.skipped:
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | "
                f"PRUNED | — | — | — | — | — | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | {'; '.join(r.notes)} |"
            )
        elif r.error:
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | "
                f"ERROR | — | — | — | — | — | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | Error: {r.error} |"
            )
        else:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            md_lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | `{r.mode_params}` | "
                f"{r.gate_6m} | {g6.return_pct:.2f}% | {g6.ratio:.3f}x | {g6.trades} | "
                f"{gf.return_pct:.2f}% | {gf.ratio:.3f}x | {r.btc_smoke} | {r.eth_smoke} | {r.sol_smoke} | {r.bnb_smoke} | {'; '.join(r.notes) if r.notes else '—'} |"
            )

    md_lines.extend([
        "",
        "## Notes & Methodology",
        "- **Harness:** Path B event-driven closed-bar backtest (`process_orders_on_close = True`).",
        "- **Fees / Slippage:** 0.10% fee per side + 5 bps adverse slippage.",
        "- **Gate Sizing:** Mode A Gate uses 100% equity; Ops uses 2.5% equity.",
        f"- **LEAD Criteria:** 6m Mode-A return >= {GATE_MULT}x Buy & Hold return AND n > {TINY_N_THRESHOLD} on BTC.",
        f"- **Tiny-n Policy:** BTC Mode-A n <= {TINY_N_THRESHOLD} triggers an immediate TINY-N KILL.",
        f"- **Thin-n Flag:** BTC Mode-A n in [{THIN_N_LOWER}..{THIN_N_UPPER}] flagged as THIN-N.",
        "- **Dual Survival:** Identical parameter set tested across BTC -> ETH -> SOL -> BNB ladder; never retuned per coin.",
        "- **Status:** RESEARCH / OPTIMISE ONLY — LIVE FROZEN.",
    ])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    return md_path, csv_path
