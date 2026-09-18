"""stage15-dual-sol-bnb-v1 harness: Sweep and score five strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (ALL 5 — include optional #5):
1. ehlers-spearman-rank-zero
2. ehlers-uo2025-hpdiff-zero
3. ehlers-corr-cycle-real-zero
4. ehlers-net-myrsi-zero
5. varadi-dvi-midline-cross

Design Bias:
  BNB-survival CRITICAL after 3-coin clear (stage14 TTF lesson) +
  keep BTC->ETH portability (don't regress to stage13) +
  denser n >> 9 (TTF seats were thin n=6-8). Dual identical params.
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
from backtest.path_b.stage15_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_spearman_rank_zero_v1 import (
    SpearmanRankParams,
    compute_signals as spearman_signals,
    validate_bnb_smoke as validate_spearman_bnb_smoke,
    validate_btc_smoke as validate_spearman_btc_smoke,
    validate_eth_smoke as validate_spearman_eth_smoke,
    validate_sol_smoke as validate_spearman_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_uo2025_hpdiff_zero_v1 import (
    Uo2025Params,
    compute_signals as uo2025_signals,
    validate_bnb_smoke as validate_uo2025_bnb_smoke,
    validate_btc_smoke as validate_uo2025_btc_smoke,
    validate_eth_smoke as validate_uo2025_eth_smoke,
    validate_sol_smoke as validate_uo2025_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_corr_cycle_real_zero_v1 import (
    CorrCycleParams,
    compute_signals as corr_cycle_signals,
    validate_bnb_smoke as validate_corr_cycle_bnb_smoke,
    validate_btc_smoke as validate_corr_cycle_btc_smoke,
    validate_eth_smoke as validate_corr_cycle_eth_smoke,
    validate_sol_smoke as validate_corr_cycle_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_net_myrsi_zero_v1 import (
    NetMyRsiParams,
    compute_signals as net_myrsi_signals,
    validate_bnb_smoke as validate_net_myrsi_bnb_smoke,
    validate_btc_smoke as validate_net_myrsi_btc_smoke,
    validate_eth_smoke as validate_net_myrsi_eth_smoke,
    validate_sol_smoke as validate_net_myrsi_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.varadi_dvi_midline_cross_v1 import (
    VaradiDviParams,
    compute_signals as dvi_signals,
    validate_bnb_smoke as validate_dvi_bnb_smoke,
    validate_btc_smoke as validate_dvi_btc_smoke,
    validate_eth_smoke as validate_dvi_eth_smoke,
    validate_sol_smoke as validate_dvi_sol_smoke,
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
# Strategy 1: ehlers-spearman-rank-zero
# ---------------------------------------------------------------------------

def run_spearman_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-spearman-rank-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, SpearmanRankParams]] = [
        ("mode_a|(L20)", SpearmanRankParams(mode="mode_a", length=20)),
        ("mode_a|(L14)", SpearmanRankParams(mode="mode_a", length=14)),
        ("mode_a|(L28)", SpearmanRankParams(mode="mode_a", length=28)),
        ("mode_b|(L20)", SpearmanRankParams(mode="mode_b", length=20)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_spearman_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_spearman_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_spearman_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_spearman_bnb_smoke(p, tf)
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
                buys, sells, stops = spearman_signals(bars, p)
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
# Strategy 2: ehlers-uo2025-hpdiff-zero
# ---------------------------------------------------------------------------

def run_uo2025_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-uo2025-hpdiff-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, Uo2025Params]] = [
        ("mode_a|(p20,bw2.0)", Uo2025Params(mode="mode_a", band_edge=20, bandwidth=2.0)),
        ("mode_a|(p14,bw2.0)", Uo2025Params(mode="mode_a", band_edge=14, bandwidth=2.0)),
        ("mode_a|(p28,bw2.0)", Uo2025Params(mode="mode_a", band_edge=28, bandwidth=2.0)),
        ("mode_b|(p20,bw2.0)", Uo2025Params(mode="mode_b", band_edge=20, bandwidth=2.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_uo2025_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_uo2025_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_uo2025_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_uo2025_bnb_smoke(p, tf)
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
                buys, sells, stops = uo2025_signals(bars, p)
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
# Strategy 3: ehlers-corr-cycle-real-zero
# ---------------------------------------------------------------------------

def run_corr_cycle_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-corr-cycle-real-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, CorrCycleParams]] = [
        ("mode_a|(p20,th9)", CorrCycleParams(mode="mode_a", period=20, threshold=9.0)),
        ("mode_a|(p14,th9)", CorrCycleParams(mode="mode_a", period=14, threshold=9.0)),
        ("mode_a|(p28,th9)", CorrCycleParams(mode="mode_a", period=28, threshold=9.0)),
        ("mode_b|(p20,th9)", CorrCycleParams(mode="mode_b", period=20, threshold=9.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_corr_cycle_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_corr_cycle_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_corr_cycle_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_corr_cycle_bnb_smoke(p, tf)
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
                buys, sells, stops = corr_cycle_signals(bars, p)
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
# Strategy 4: ehlers-net-myrsi-zero
# ---------------------------------------------------------------------------

def run_net_myrsi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "ehlers-net-myrsi-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, NetMyRsiParams]] = [
        ("mode_a|(rsi14,net14)", NetMyRsiParams(mode="mode_a", rsi_length=14, net_length=14)),
        ("mode_a|(rsi10,net14)", NetMyRsiParams(mode="mode_a", rsi_length=10, net_length=14)),
        ("mode_a|(rsi20,net14)", NetMyRsiParams(mode="mode_a", rsi_length=20, net_length=14)),
        ("mode_b|(rsi14,net14)", NetMyRsiParams(mode="mode_b", rsi_length=14, net_length=14)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_net_myrsi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_net_myrsi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_net_myrsi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_net_myrsi_bnb_smoke(p, tf)
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
                buys, sells, stops = net_myrsi_signals(bars, p)
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
# Strategy 5: varadi-dvi-midline-cross (Optional 5th)
# ---------------------------------------------------------------------------

def run_dvi_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    prior_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "varadi-dvi-midline-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    param_grid: list[tuple[str, VaradiDviParams]] = [
        ("mode_a|(n168,w0.8)", VaradiDviParams(mode="mode_a", n=168, mag_weight=0.8, str_weight=0.2)),
        ("mode_a|(n100,w0.8)", VaradiDviParams(mode="mode_a", n=100, mag_weight=0.8, str_weight=0.2)),
        ("mode_a|(n252,w0.8)", VaradiDviParams(mode="mode_a", n=252, mag_weight=0.8, str_weight=0.2)),
        ("mode_b|(n168,w0.8)", VaradiDviParams(mode="mode_b", n=168, mag_weight=0.8, str_weight=0.2)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            btc_ok, btc_msg = validate_dvi_btc_smoke(p, tf)
            eth_ok, eth_msg = validate_dvi_eth_smoke(p, tf)
            sol_ok, sol_msg = validate_dvi_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_dvi_bnb_smoke(p, tf)
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
                buys, sells, stops = dvi_signals(bars, p)
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
    if strategy_id == "ehlers-spearman-rank-zero":
        return run_spearman_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "ehlers-uo2025-hpdiff-zero":
        return run_uo2025_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "ehlers-corr-cycle-real-zero":
        return run_corr_cycle_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "ehlers-net-myrsi-zero":
        return run_net_myrsi_cells(symbol, bars_by_tf, active_keys, prior_results)
    elif strategy_id == "varadi-dvi-midline-cross":
        return run_dvi_cells(symbol, bars_by_tf, active_keys, prior_results)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


# ---------------------------------------------------------------------------
# Master Sweep Runner (Ladder: BTC -> ETH -> SOL -> BNB)
# ---------------------------------------------------------------------------

def run_stage15_dual_sol_bnb_v1(
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
        print(f"\n{'='*70}\n[stage15-dual-sol-bnb-v1] Evaluating Symbol: {symbol}\n{'='*70}", flush=True)

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
                "ehlers-spearman-rank-zero": ["mode_a|(L20)", "mode_a|(L14)", "mode_a|(L28)", "mode_b|(L20)"],
                "ehlers-uo2025-hpdiff-zero": ["mode_a|(p20,bw2.0)", "mode_a|(p14,bw2.0)", "mode_a|(p28,bw2.0)", "mode_b|(p20,bw2.0)"],
                "ehlers-corr-cycle-real-zero": ["mode_a|(p20,th9)", "mode_a|(p14,th9)", "mode_a|(p28,th9)", "mode_b|(p20,th9)"],
                "ehlers-net-myrsi-zero": ["mode_a|(rsi14,net14)", "mode_a|(rsi10,net14)", "mode_a|(rsi20,net14)", "mode_b|(rsi14,net14)"],
                "varadi-dvi-midline-cross": ["mode_a|(n168,w0.8)", "mode_a|(n100,w0.8)", "mode_a|(n252,w0.8)", "mode_b|(n168,w0.8)"],
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

    md_path = output_dir / "stage15-dual-sol-bnb-v1-scoreboard.md"
    csv_path = output_dir / "stage15-dual-sol-bnb-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage15-dual-sol-bnb-v1 scoreboard (BNB-survival CRITICAL + BTC->ETH portability PRESERVED)",
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
        "- **BNB-Survival (CRITICAL):** Stage 14 wipe lesson (TTF cleared BTC->ETH->SOL then wiped BNB 0.093x). BNB survival after 3-coin clear is critical.",
        "- **BTC->ETH Portability:** Keep portability without regressing to stage13 choke.",
        "- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-14 IDs, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Spearman Rank (`ehlers-spearman-rank-zero`):** Rank correlation rho vs time rank. L=20 preferred; L=14, L=28. Mode A rho x 0; Mode B quality rho > 0.2.",
        "- **Ultimate Oscillator 2025 (`ehlers-uo2025-hpdiff-zero`):** Dual-HighPass / RMS. (20,2.0) preferred; (14,2.0), (28,2.0). Mode A uo x 0; Mode B uo > 0.5 quality.",
        "- **Correlation Cycle Real (`ehlers-corr-cycle-real-zero`):** Cosine corr Real x 0. (20,9) preferred; (14,9), (28,9). Mode A Real x 0; Mode B Real x 0 AND state != 0.",
        "- **NET MyRSI (`ehlers-net-myrsi-zero`):** Kendall NET on MyRSI. (14,14) preferred; (10,14), (20,14). Mode A NET x 0; Mode B NET > 0.2 quality.",
        "- **Varadi DVI (`varadi-dvi-midline-cross`):** DV Intermediate Oscillator percent-rank composite. (168,0.8) preferred; (100,0.8), (252,0.8). Mode A DVI x 0.5; Mode B DVI > 0.55 / stretch.",
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
