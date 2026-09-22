"""stage19-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (ALL 5):
1. hhll-structure-flip
2. starc-bands-break-flip
3. vzo-zero-cross
4. nvi-ema-cross
5. fdi-low-trend-dir

Design Bias:
  BTC LEAD PRIMARY without over-damp (stage12/15/18 rhyme: denser mid-cycle seats never left BTC).
  Keep denser n >> 9 + ETH portability + SOL-after-BTC+ETH + BNB-after-3-coin.
  Identical dual params across BTC/ETH/SOL/BNB.
  btc_smoke (CRITICAL: kill 0 BTC / over-damp) + eth_smoke + sol_smoke + bnb_smoke.
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
from backtest.path_b.stage19_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.hhll_structure_flip_v1 import (
    HhllParams,
    compute_signals as hhll_signals,
    validate_bnb_smoke as validate_hhll_bnb_smoke,
    validate_btc_smoke as validate_hhll_btc_smoke,
    validate_eth_smoke as validate_hhll_eth_smoke,
    validate_sol_smoke as validate_hhll_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.starc_bands_break_flip_v1 import (
    StarcParams,
    compute_signals as starc_signals,
    validate_bnb_smoke as validate_starc_bnb_smoke,
    validate_btc_smoke as validate_starc_btc_smoke,
    validate_eth_smoke as validate_starc_eth_smoke,
    validate_sol_smoke as validate_starc_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.vzo_zero_cross_v1 import (
    VzoParams,
    compute_signals as vzo_signals,
    validate_bnb_smoke as validate_vzo_bnb_smoke,
    validate_btc_smoke as validate_vzo_btc_smoke,
    validate_eth_smoke as validate_vzo_eth_smoke,
    validate_sol_smoke as validate_vzo_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.nvi_ema_cross_v1 import (
    NviParams,
    compute_signals as nvi_signals,
    validate_bnb_smoke as validate_nvi_bnb_smoke,
    validate_btc_smoke as validate_nvi_btc_smoke,
    validate_eth_smoke as validate_nvi_eth_smoke,
    validate_sol_smoke as validate_nvi_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.fdi_low_trend_dir_v1 import (
    FdiParams,
    compute_signals as fdi_signals,
    validate_bnb_smoke as validate_fdi_bnb_smoke,
    validate_btc_smoke as validate_fdi_btc_smoke,
    validate_eth_smoke as validate_fdi_eth_smoke,
    validate_sol_smoke as validate_fdi_sol_smoke,
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
# Strategy 1: hhll-structure-flip
# ---------------------------------------------------------------------------

def run_hhll_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "hhll-structure-flip"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, HhllParams]] = [
        ("mode_a|(lb3)", HhllParams(mode="mode_a", lb=3)),
        ("mode_a|(lb2)", HhllParams(mode="mode_a", lb=2)),
        ("mode_a|(lb5)", HhllParams(mode="mode_a", lb=5)),
        ("mode_b|(lb3,bos)", HhllParams(mode="mode_b", lb=3, bos_entry=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_hhll_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_hhll_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_hhll_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_hhll_bnb_smoke(p, tf)
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
                buys, sells, stops = hhll_signals(bars, p)
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
# Strategy 2: starc-bands-break-flip
# ---------------------------------------------------------------------------

def run_starc_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "starc-bands-break-flip"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, StarcParams]] = [
        ("mode_a|(sma6,atr15,k2.0)", StarcParams(mode="mode_a", sma_len=6, atr_len=15, k=2.0)),
        ("mode_a|(sma5,atr10,k1.5)", StarcParams(mode="mode_a", sma_len=5, atr_len=10, k=1.5)),
        ("mode_a|(sma10,atr15,k2.5)", StarcParams(mode="mode_a", sma_len=10, atr_len=15, k=2.5)),
        ("mode_b|(sma6,atr15,k2.0,midexit)", StarcParams(mode="mode_b", sma_len=6, atr_len=15, k=2.0, exit_on_mid=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_starc_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_starc_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_starc_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_starc_bnb_smoke(p, tf)
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
                buys, sells, stops = starc_signals(bars, p)
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
# Strategy 3: vzo-zero-cross
# ---------------------------------------------------------------------------

def run_vzo_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "vzo-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, VzoParams]] = [
        ("mode_a|(len14)", VzoParams(mode="mode_a", length=14)),
        ("mode_a|(len10)", VzoParams(mode="mode_a", length=10)),
        ("mode_a|(len21)", VzoParams(mode="mode_a", length=21)),
        ("mode_b|(len14,hold1)", VzoParams(mode="mode_b", length=14, hold_bars=1)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_vzo_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_vzo_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_vzo_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_vzo_bnb_smoke(p, tf)
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
                buys, sells, stops = vzo_signals(bars, p)
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
# Strategy 4: nvi-ema-cross
# ---------------------------------------------------------------------------

def run_nvi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "nvi-ema-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, NviParams]] = [
        ("mode_a|(sig50)", NviParams(mode="mode_a", sig_len=50)),
        ("mode_a|(sig21)", NviParams(mode="mode_a", sig_len=21)),
        ("mode_a|(sig100)", NviParams(mode="mode_a", sig_len=100)),
        ("mode_b|(sig50,trail1.5)", NviParams(mode="mode_b", sig_len=50, atr_trail_mult=1.5)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_nvi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_nvi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_nvi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_nvi_bnb_smoke(p, tf)
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
                buys, sells, stops = nvi_signals(bars, p)
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
# Strategy 5: fdi-low-trend-dir
# ---------------------------------------------------------------------------

def run_fdi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "fdi-low-trend-dir"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, FdiParams]] = [
        ("mode_a|(n30,thr1.50,dir3)", FdiParams(mode="mode_a", n=30, thr=1.50, dir_len=3)),
        ("mode_a|(n20,thr1.40,dir1)", FdiParams(mode="mode_a", n=20, thr=1.40, dir_len=1)),
        ("mode_a|(n30,thr1.55,dir5)", FdiParams(mode="mode_a", n=30, thr=1.55, dir_len=5)),
        ("mode_b|(n30,thr1.45,dir3)", FdiParams(mode="mode_b", n=30, thr=1.45, dir_len=3)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_fdi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_fdi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_fdi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_fdi_bnb_smoke(p, tf)
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
                buys, sells, stops = fdi_signals(bars, p)
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

def run_stage19_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    all_results: list[CellResult] = []
    tfs = ("1h", "4h")

    active_keys: set[str] | None = None
    prior_results_by_key: dict[str, CellResult] = {}

    for s_idx, symbol in enumerate(symbols):
        print(f"\n{'='*70}\n[stage19-dual-sol-bnb-v1] Evaluating Symbol: {symbol} (LADDER STEP {s_idx + 1}/4)\n{'='*70}", flush=True)

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
                "hhll-structure-flip": ["mode_a|(lb3)", "mode_a|(lb2)", "mode_a|(lb5)", "mode_b|(lb3,bos)"],
                "starc-bands-break-flip": ["mode_a|(sma6,atr15,k2.0)", "mode_a|(sma5,atr10,k1.5)", "mode_a|(sma10,atr15,k2.5)", "mode_b|(sma6,atr15,k2.0,midexit)"],
                "vzo-zero-cross": ["mode_a|(len14)", "mode_a|(len10)", "mode_a|(len21)", "mode_b|(len14,hold1)"],
                "nvi-ema-cross": ["mode_a|(sig50)", "mode_a|(sig21)", "mode_a|(sig100)", "mode_b|(sig50,trail1.5)"],
                "fdi-low-trend-dir": ["mode_a|(n30,thr1.50,dir3)", "mode_a|(n20,thr1.40,dir1)", "mode_a|(n30,thr1.55,dir5)", "mode_b|(n30,thr1.45,dir3)"],
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
                if sid == "hhll-structure-flip":
                    res = run_hhll_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "starc-bands-break-flip":
                    res = run_starc_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "vzo-zero-cross":
                    res = run_vzo_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "nvi-ema-cross":
                    res = run_nvi_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
                    sym_results.extend(res)
                    all_results.extend(res)
                elif sid == "fdi-low-trend-dir":
                    res = run_fdi_cells(symbol, bars, active_keys=active_keys, prior_results=prior_results_by_key)
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

    md_cols = [
        r.symbol,
        r.strategy_id,
        r.tf,
        r.mode_params,
        r.btc_smoke,
        r.eth_smoke,
        r.sol_smoke,
        r.bnb_smoke,
        r.retention_notes,
        str(g6.trades) if g6 else "—",
        f"{g6.win_rate_pct:.1f}%" if g6 else "—",
        f"{g6.return_pct:+.2f}%" if g6 else "—",
        f"{g6.bh_return_pct:+.2f}%" if g6 else "—",
        f"{g6.ratio:.3f}x" if g6 else "—",
        f"**{r.gate_6m}**",
        str(gf.trades) if gf else "—",
        f"{gf.win_rate_pct:.1f}%" if gf else "—",
        f"{gf.return_pct:+.2f}%" if gf else "—",
        f"{gf.bh_return_pct:+.2f}%" if gf else "—",
        f"{gf.ratio:.3f}x" if gf else "—",
        r.gate_full,
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

    md_path = output_dir / "stage19-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage19-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage19-dual-sol-bnb-v1 scoreboard (BTC LEAD PRIMARY without over-damp + Denser n >> 9)",
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
        "- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).",
        "- **BTC LEAD PRIMARY Bias:** Designed to clear dense BTC first without stage12/15/18 over-damp or mid-cycle chop wipe.",
        "- **BTC LEAD & Density:** Keep dense trades without over-damp collapse (stage12/15/18) or ETH wipe (stage13/17).",
        "- **SOL & BNB Retention:** Multi-dozen participation on SOL and quiet-wipe protection on BNB.",
        "- **Mandatory Smoke & Retention Tests:** btc_smoke (CRITICAL), eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-18 IDs, no DPO/PPO/VHF/FOSC/PO, no HA/MDI/DSS/III/PMA, no BandPass/HP/3LB/SI/Kagi, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Higher-High / Lower-Low Structure Flip (`hhll-structure-flip`):** confirmed pivot HH/HL structure polarity. lb=3 preferred; lb=2, lb=5. Mode A bullStruct edge; Mode B BOS entry. != Kagi, != 3LB, != ZigZag look-ahead.",
        "- **STARC Bands Break Flip (`starc-bands-break-flip`):** Stoller SMA +/- k*ATR break-flip. (6,15,2.0) preferred; (5,10,1.5), (10,15,2.5). Mode A close x upper/lower; Mode B mid-exit. != Keltner (EMA center), != BB, != Donchian.",
        "- **Volume Zone Oscillator (`vzo-zero-cross`):** Khalil signed-volume EMA ratio x 0. len=14 preferred; len=10, len=21. Mode A VZO x 0; Mode B hold > +5. != PZO (price), != Bostian III, != CMF/OBV.",
        "- **Negative Volume Index (`nvi-ema-cross`):** Fosback NVI x EMA signal cross. sigLen=50 on 1H preferred; sigLen=21, sigLen=100. Mode A NVI x EMA; Mode B ATR trail. != OBV, != PVI.",
        "- **Fractal Dimension Index Low Trend (`fdi-low-trend-dir`):** Matulich-corrected Sevcik FDI < thr x close direction. (30,1.50,3) preferred; (20,1.40,1), (30,1.55,5). Mode A rising edge; Mode B thr=1.45. != FRAMA, != CHOP, != VHF.",
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

    # Summary section
    total_cells = len(results)
    btc_cells = [r for r in results if r.symbol == "BTCUSDT"]
    eth_cells = [r for r in results if r.symbol == "ETHUSDT" and not r.skipped]
    sol_cells = [r for r in results if r.symbol == "SOLUSDT" and not r.skipped]
    bnb_cells = [r for r in results if r.symbol == "BNBUSDT" and not r.skipped]

    btc_pass = [r for r in btc_cells if r.gate_6m == "PASS"]
    eth_pass = [r for r in eth_cells if r.gate_6m == "PASS"]
    sol_pass = [r for r in sol_cells if r.gate_6m == "PASS"]
    bnb_pass = [r for r in bnb_cells if r.gate_6m == "PASS"]

    lines.extend([
        "",
        "## Ladder Progression Summary",
        "",
        f"- **BTCUSDT:** {len(btc_cells)} scored, **{len(btc_pass)} PASS** ({len(btc_cells) - len(btc_pass)} failed/pruned)",
        f"- **ETHUSDT:** {len(eth_cells)} scored, **{len(eth_pass)} PASS** ({len(eth_cells) - len(eth_pass)} failed/pruned)",
        f"- **SOLUSDT:** {len(sol_cells)} scored, **{len(sol_pass)} PASS** ({len(sol_cells) - len(sol_pass)} failed/pruned)",
        f"- **BNBUSDT:** {len(bnb_cells)} scored, **{len(bnb_pass)} PASS** ({len(bnb_cells) - len(bnb_pass)} failed/pruned)",
        "",
        f"**Full 4-Coin Ladder Survivors:** {len(bnb_pass)}",
        "",
        "## Smoke & Retention Diagnostic Summary",
        "",
        f"- `btc_smoke` Failures: {sum(1 for r in results if r.btc_smoke.startswith('FAIL'))}",
        f"- `eth_smoke` Failures: {sum(1 for r in results if r.eth_smoke.startswith('FAIL'))}",
        f"- `sol_smoke` Failures: {sum(1 for r in results if r.sol_smoke.startswith('FAIL'))}",
        f"- `bnb_smoke` Failures: {sum(1 for r in results if r.bnb_smoke.startswith('FAIL'))}",
        f"- `tiny_n_kill` Activations (BTC n <= {TINY_N_THRESHOLD}): {sum(1 for r in btc_cells if r.tiny_n_kill)}",
        f"- `thin_n_flag` Warnings (BTC n in [{THIN_N_LOWER}..{THIN_N_UPPER}]): {sum(1 for r in btc_cells if r.thin_n_flag)}",
        "",
    ])

    md_path.write_text("\n".join(lines), encoding="utf-8")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
