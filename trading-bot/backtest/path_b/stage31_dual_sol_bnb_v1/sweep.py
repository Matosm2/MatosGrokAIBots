"""stage31-dual-sol-bnb-v1 harness: Sweep and score strategies (BTC, ETH, SOL, BNB independently).

LOCKED ENCODE ORDER (4 strategies):
1. apirine-sdo-zero-cross
2. ehlers-madh-zero-cross
3. premier-stochastic-osc-zero
4. apirine-tradj-ema-cross

NEW GATE (Nuno 2026-09-22 + Mid-Encode Patch):
  PER-COIN GATE:
  - Score BTC / ETH / SOL / BNB independently.
  - Coin PASS (paper-eligible) iff Mode-A >= 1.2x B&H on that coin AND denser sample n >= 40.
  - Thin n < 40 -> ineligible for paper even if x >= 1.2 (flag THIN clearly).
  - Multiple strategies OK — best eligible per coin.
  - Do NOT kill a seat only because it fails another coin.
  - Full-ladder no longer required for paper.
  - Score all four coins even if BTC fails.
  - Prefer dense BTC lead when ranking / sweep priority, but per-coin scoring is authoritative.
  - LIVE still NO. Hold open draft PR.
  - Track B Hard Ban: no CK / QQE / MAMA / Wilder-VS.

Full(~2y) Mode-A + ops 2.5% sizing reported for operational visibility.
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
from backtest.path_b.stage31_dual_sol_bnb_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.apirine_sdo_zero_cross_v1 import (
    ApirineSdoParams,
    compute_signals as sdo_signals,
    validate_bnb_smoke as validate_sdo_bnb_smoke,
    validate_btc_smoke as validate_sdo_btc_smoke,
    validate_eth_smoke as validate_sdo_eth_smoke,
    validate_sol_smoke as validate_sdo_sol_smoke,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.ehlers_madh_zero_cross_v1 import (
    EhlersMadhParams,
    compute_signals as madh_signals,
    validate_bnb_smoke as validate_madh_bnb_smoke,
    validate_btc_smoke as validate_madh_btc_smoke,
    validate_eth_smoke as validate_madh_eth_smoke,
    validate_sol_smoke as validate_madh_sol_smoke,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.premier_stochastic_osc_zero_v1 import (
    PremierStochParams,
    compute_signals as pso_signals,
    validate_bnb_smoke as validate_pso_bnb_smoke,
    validate_btc_smoke as validate_pso_btc_smoke,
    validate_eth_smoke as validate_pso_eth_smoke,
    validate_sol_smoke as validate_pso_sol_smoke,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.apirine_tradj_ema_cross_v1 import (
    ApirineTradjEmaParams,
    compute_signals as tradj_signals,
    validate_bnb_smoke as validate_tradj_bnb_smoke,
    validate_btc_smoke as validate_tradj_btc_smoke,
    validate_eth_smoke as validate_tradj_eth_smoke,
    validate_sol_smoke as validate_tradj_sol_smoke,
)

GATE_MULT = 1.2
DENSER_N_FLOOR = 40  # Mid-encode patch: Coin PASS iff Mode-A >= 1.2x B&H on that coin AND n >= 40
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
    pass_coin: str = "N"  # Y / N per new gate: x >= 1.2 AND n >= 40
    thin_flag: str = "—"  # THIN if x >= 1.2 but n < 40
    btc_smoke: str = "Y"
    eth_smoke: str = "Y"
    sol_smoke: str = "Y"
    bnb_smoke: str = "Y"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
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


def _gate_label(symbol: str, trades: int, ret: float, bh: float, window: str) -> tuple[str, str, str]:
    """Return (gate_6m_label, pass_coin_label, thin_flag_label)."""
    ratio = _ratio(ret, bh)
    if trades == 0:
        return "FAIL", "N", "—"

    ratio_ok = ratio >= GATE_MULT
    dense_ok = trades >= DENSER_N_FLOOR

    if window == "6m":
        if ratio_ok and dense_ok:
            return "PASS", "Y", "—"
        elif ratio_ok and not dense_ok:
            return "FAIL", "N", "THIN"
        else:
            return "FAIL", "N", "—"

    return ("PASS" if ratio_ok else "FAIL"), "—", "—"


def _eval_windows(
    symbol: str,
    sid: str,
    bars: list[Bar],
    buys: list[bool],
    sells: list[bool],
    stops: list[float | None],
) -> tuple[list[WindowModeMetrics], str, str]:
    out: list[WindowModeMetrics] = []
    cell_pass_coin = "N"
    cell_thin_flag = "—"

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
                gate_lbl, p_coin, th_flag = _gate_label(symbol, n_trades, ret_pct, bh_pct, win_label)
                if win_label == "6m":
                    cell_pass_coin = p_coin
                    cell_thin_flag = th_flag

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

    return out, cell_pass_coin, cell_thin_flag


def _finish(cell: CellResult, pass_coin: str, thin_flag: str) -> CellResult:
    g6 = next((m for m in cell.metrics if m.window == "6m" and m.mode == "gate"), None)
    gf = next((m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
    if not g6:
        cell.gate_6m = "FAIL"
        cell.pass_coin = "N"
        return cell

    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate if gf else "FAIL"
    cell.pass_coin = pass_coin
    cell.thin_flag = thin_flag

    if thin_flag == "THIN":
        cell.notes.append(f"THIN-N (Mode-A 6m n={g6.trades} < {DENSER_N_FLOOR}; ineligible for paper even though x={g6.ratio:.2f} >= {GATE_MULT})")
    elif pass_coin == "Y":
        cell.notes.append(f"PASS_coin (Mode-A 6m x={g6.ratio:.2f} >= {GATE_MULT} AND n={g6.trades} >= {DENSER_N_FLOOR})")

    return cell


def _print_cell(cell: CellResult) -> None:
    if cell.error:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> ERROR: {cell.error}", flush=True)
        return
    g6 = next((m for m in cell.metrics if m.window == "6m" and m.mode == "gate"), None)
    gf = next((m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
    if not g6 or not gf:
        print(f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> NO METRICS", flush=True)
        return
    pass_tag = f" [PASS_COIN={cell.pass_coin}]" if cell.pass_coin == "Y" else ""
    thin_tag = f" [{cell.thin_flag}]" if cell.thin_flag == "THIN" else ""
    print(
        f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> "
        f"6m={cell.gate_6m}({g6.ratio:.3f}x){pass_tag}{thin_tag} ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: apirine-sdo-zero-cross
# ---------------------------------------------------------------------------

def run_apirine_sdo_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
) -> list[CellResult]:
    sid = "apirine-sdo-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Mode A default (14, 100, 3); sweep n in {8, 14, 20, 40}, lb in {50, 100, 200}, pds in {3, 5, 6}
    param_grid: list[tuple[str, ApirineSdoParams]] = [
        ("mode_a|(n14,lb100,pds3)", ApirineSdoParams(mode="mode_a", n=14, lb=100, pds=3)),
        ("mode_a|(n8,lb50,pds3)", ApirineSdoParams(mode="mode_a", n=8, lb=50, pds=3)),
        ("mode_a|(n14,lb50,pds3)", ApirineSdoParams(mode="mode_a", n=14, lb=50, pds=3)),
        ("mode_a|(n20,lb100,pds5)", ApirineSdoParams(mode="mode_a", n=20, lb=100, pds=5)),
        ("mode_a|(n40,lb200,pds6)", ApirineSdoParams(mode="mode_a", n=40, lb=200, pds=6)),
        ("mode_b|(n14,lb100,pds3,rising)", ApirineSdoParams(mode="mode_b", n=14, lb=100, pds=3, rising_req=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf, [])
        if not bars:
            continue
        for desc, params in param_grid:
            btc_ok, btc_r = validate_sdo_btc_smoke(params, tf)
            eth_ok, eth_r = validate_sdo_eth_smoke(params, tf)
            sol_ok, sol_r = validate_sdo_sol_smoke(params, tf)
            bnb_ok, bnb_r = validate_sdo_bnb_smoke(params, tf)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke="Y" if btc_ok else f"FAIL: {btc_r}",
                eth_smoke="Y" if eth_ok else f"FAIL: {eth_r}",
                sol_smoke="Y" if sol_ok else f"FAIL: {sol_r}",
                bnb_smoke="Y" if bnb_ok else f"FAIL: {bnb_r}",
            )

            try:
                buys, sells, stops = sdo_signals(bars, params)
                metrics, p_coin, th_flag = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell = _finish(cell, p_coin, th_flag)
            except Exception as e:
                cell.error = str(e)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: ehlers-madh-zero-cross
# ---------------------------------------------------------------------------

def run_ehlers_madh_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
) -> list[CellResult]:
    sid = "ehlers-madh-zero-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Mode A default (8, 27); sweep Short in {6, 8, 10}, Dom in {20, 27, 34}
    param_grid: list[tuple[str, EhlersMadhParams]] = [
        ("mode_a|(s8,dom27)", EhlersMadhParams(mode="mode_a", short_length=8, dominant_cycle=27)),
        ("mode_a|(s6,dom20)", EhlersMadhParams(mode="mode_a", short_length=6, dominant_cycle=20)),
        ("mode_a|(s8,dom20)", EhlersMadhParams(mode="mode_a", short_length=8, dominant_cycle=20)),
        ("mode_a|(s10,dom34)", EhlersMadhParams(mode="mode_a", short_length=10, dominant_cycle=34)),
        ("mode_b|(s8,dom27,rising)", EhlersMadhParams(mode="mode_b", short_length=8, dominant_cycle=27, rising_req=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf, [])
        if not bars:
            continue
        for desc, params in param_grid:
            btc_ok, btc_r = validate_madh_btc_smoke(params, tf)
            eth_ok, eth_r = validate_madh_eth_smoke(params, tf)
            sol_ok, sol_r = validate_madh_sol_smoke(params, tf)
            bnb_ok, bnb_r = validate_madh_bnb_smoke(params, tf)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke="Y" if btc_ok else f"FAIL: {btc_r}",
                eth_smoke="Y" if eth_ok else f"FAIL: {eth_r}",
                sol_smoke="Y" if sol_ok else f"FAIL: {sol_r}",
                bnb_smoke="Y" if bnb_ok else f"FAIL: {bnb_r}",
            )

            try:
                buys, sells, stops = madh_signals(bars, params)
                metrics, p_coin, th_flag = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell = _finish(cell, p_coin, th_flag)
            except Exception as e:
                cell.error = str(e)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: premier-stochastic-osc-zero
# ---------------------------------------------------------------------------

def run_premier_stoch_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
) -> list[CellResult]:
    sid = "premier-stochastic-osc-zero"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Mode A default (8, 5); sweep Period in {5, 8, 14}, Smooth in {3, 5, 8}
    param_grid: list[tuple[str, PremierStochParams]] = [
        ("mode_a|(per8,sm5)", PremierStochParams(mode="mode_a", period=8, smooth=5)),
        ("mode_a|(per5,sm3)", PremierStochParams(mode="mode_a", period=5, smooth=3)),
        ("mode_a|(per8,sm3)", PremierStochParams(mode="mode_a", period=8, smooth=3)),
        ("mode_a|(per14,sm8)", PremierStochParams(mode="mode_a", period=14, smooth=8)),
        ("mode_b|(per8,sm5,dip-0.2)", PremierStochParams(mode="mode_b", period=8, smooth=5)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf, [])
        if not bars:
            continue
        for desc, params in param_grid:
            btc_ok, btc_r = validate_pso_btc_smoke(params, tf)
            eth_ok, eth_r = validate_pso_eth_smoke(params, tf)
            sol_ok, sol_r = validate_pso_sol_smoke(params, tf)
            bnb_ok, bnb_r = validate_pso_bnb_smoke(params, tf)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke="Y" if btc_ok else f"FAIL: {btc_r}",
                eth_smoke="Y" if eth_ok else f"FAIL: {eth_r}",
                sol_smoke="Y" if sol_ok else f"FAIL: {sol_r}",
                bnb_smoke="Y" if bnb_ok else f"FAIL: {bnb_r}",
            )

            try:
                buys, sells, stops = pso_signals(bars, params)
                metrics, p_coin, th_flag = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell = _finish(cell, p_coin, th_flag)
            except Exception as e:
                cell.error = str(e)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 4: apirine-tradj-ema-cross
# ---------------------------------------------------------------------------

def run_apirine_tradj_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
) -> list[CellResult]:
    sid = "apirine-tradj-ema-cross"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Mode A default (20, 20, 5); sweep Periods in {10, 20, 40}, Pds in {10, 20, 40}, Mltp in {5, 8, 10}
    param_grid: list[tuple[str, ApirineTradjEmaParams]] = [
        ("mode_a|(p20,pds20,m5)", ApirineTradjEmaParams(mode="mode_a", periods=20, pds=20, mltp=5.0)),
        ("mode_a|(p10,pds10,m5)", ApirineTradjEmaParams(mode="mode_a", periods=10, pds=10, mltp=5.0)),
        ("mode_a|(p20,pds10,m8)", ApirineTradjEmaParams(mode="mode_a", periods=20, pds=10, mltp=8.0)),
        ("mode_a|(p40,pds40,m10)", ApirineTradjEmaParams(mode="mode_a", periods=40, pds=40, mltp=10.0)),
        ("mode_b|(p20,pds20,m5,close_gate)", ApirineTradjEmaParams(mode="mode_b", periods=20, pds=20, mltp=5.0, close_gate=True)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf, [])
        if not bars:
            continue
        for desc, params in param_grid:
            btc_ok, btc_r = validate_tradj_btc_smoke(params, tf)
            eth_ok, eth_r = validate_tradj_eth_smoke(params, tf)
            sol_ok, sol_r = validate_tradj_sol_smoke(params, tf)
            bnb_ok, bnb_r = validate_tradj_bnb_smoke(params, tf)

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                btc_smoke="Y" if btc_ok else f"FAIL: {btc_r}",
                eth_smoke="Y" if eth_ok else f"FAIL: {eth_r}",
                sol_smoke="Y" if sol_ok else f"FAIL: {sol_r}",
                bnb_smoke="Y" if bnb_ok else f"FAIL: {bnb_r}",
            )

            try:
                buys, sells, stops = tradj_signals(bars, params)
                metrics, p_coin, th_flag = _eval_windows(symbol, sid, bars, buys, sells, stops)
                cell.metrics = metrics
                cell = _finish(cell, p_coin, th_flag)
            except Exception as e:
                cell.error = str(e)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Main Runner: Independent Per-Coin Execution
# ---------------------------------------------------------------------------

def run_stage31_dual_sol_bnb_v1(
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
    years: float = 2.5,
    refresh: bool = False,
) -> list[CellResult]:
    """Execute all 4 strategies independently across BTC/ETH/SOL/BNB."""
    print("=" * 80)
    print(f"RUNNING {RESEARCH_ID} (Path B Track 1)")
    print(f"NEW PER-COIN GATE: Mode-A 6m >= {GATE_MULT}x B&H on that coin AND denser n >= {DENSER_N_FLOOR}")
    print("Thin n < 40 = ineligible for paper (flagged THIN)")
    print("All coins scored independently — no ladder prune")
    print(f"Symbols: {symbols} | Years: {years:g}")
    print("=" * 80, flush=True)

    all_results: list[CellResult] = []

    for sym in symbols:
        print(f"\n--- Loading and materializing {sym} 1h & 4h ---", flush=True)
        data = materialize_symbol(sym, tfs=("1h", "4h"), years=years, refresh=refresh)
        bars_by_tf = {"1h": data.get("1h", []), "4h": data.get("4h", [])}

        print(f"\n>>> Scoring Strategy 1: apirine-sdo-zero-cross on {sym} <<<", flush=True)
        res_sdo = run_apirine_sdo_cells(sym, bars_by_tf)
        all_results.extend(res_sdo)

        print(f"\n>>> Scoring Strategy 2: ehlers-madh-zero-cross on {sym} <<<", flush=True)
        res_madh = run_ehlers_madh_cells(sym, bars_by_tf)
        all_results.extend(res_madh)

        print(f"\n>>> Scoring Strategy 3: premier-stochastic-osc-zero on {sym} <<<", flush=True)
        res_pso = run_premier_stoch_cells(sym, bars_by_tf)
        all_results.extend(res_pso)

        print(f"\n>>> Scoring Strategy 4: apirine-tradj-ema-cross on {sym} <<<", flush=True)
        res_tradj = run_apirine_tradj_cells(sym, bars_by_tf)
        all_results.extend(res_tradj)

    return all_results


def write_scoreboard(
    results: list[CellResult],
    out_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Write markdown and CSV scoreboard for stage31-dual-sol-bnb-v1."""
    out_dir = out_dir or RESULTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / f"{RESEARCH_ID}-scoreboard.md"
    csv_path = out_dir / f"{RESEARCH_ID}-scoreboard.csv"

    csv_rows = []
    for r in results:
        g6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "gate"), None)
        gf = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"), None)
        o6 = next((m for m in r.metrics if m.window == "6m" and m.mode == "ops"), None)
        of = next((m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"), None)

        csv_rows.append({
            "strategy_id": r.strategy_id,
            "coin": r.symbol,
            "tf": r.tf,
            "mode_params": r.mode_params,
            "n": g6.trades if g6 else 0,
            "wr_pct": f"{g6.win_rate_pct:.1f}" if g6 else "—",
            "mode_a_ret_pct": f"{g6.return_pct:.2f}" if g6 else "—",
            "bh_ret_pct": f"{g6.bh_return_pct:.2f}" if g6 else "—",
            "x_bh": f"{g6.ratio:.3f}" if g6 else "—",
            "pass_coin": r.pass_coin,
            "thin_flag": r.thin_flag,
            "max_dd_6m_pct": f"{g6.max_drawdown_pct:.2f}" if g6 else "—",
            "gate_full": r.gate_full,
            "ret_full_pct": f"{gf.return_pct:.2f}" if gf else "—",
            "bh_full_pct": f"{gf.bh_return_pct:.2f}" if gf else "—",
            "x_bh_full": f"{gf.ratio:.3f}" if gf else "—",
            "n_full": gf.trades if gf else 0,
            "wr_full_pct": f"{gf.win_rate_pct:.1f}" if gf else "—",
            "max_dd_full_pct": f"{gf.max_drawdown_pct:.2f}" if gf else "—",
            "ops_ret_6m_pct": f"{o6.return_pct:.2f}" if o6 else "—",
            "ops_ret_full_pct": f"{of.return_pct:.2f}" if of else "—",
            "btc_smoke": r.btc_smoke,
            "eth_smoke": r.eth_smoke,
            "sol_smoke": r.sol_smoke,
            "bnb_smoke": r.bnb_smoke,
            "notes": "; ".join(r.notes) if r.notes else "—",
        })

    fieldnames = [
        "strategy_id", "coin", "tf", "mode_params", "n", "wr_pct",
        "mode_a_ret_pct", "bh_ret_pct", "x_bh", "pass_coin", "thin_flag",
        "max_dd_6m_pct", "gate_full", "ret_full_pct", "bh_full_pct", "x_bh_full",
        "n_full", "wr_full_pct", "max_dd_full_pct", "ops_ret_6m_pct", "ops_ret_full_pct",
        "btc_smoke", "eth_smoke", "sol_smoke", "bnb_smoke", "notes",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    # Markdown generation
    pass_coin_list = [r for r in results if r.pass_coin == "Y"]
    thin_list = [r for r in results if r.thin_flag == "THIN"]

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        f"# {RESEARCH_ID} — Scoreboard (Independent Per-Coin Gate)",
        "",
        f"- Generated: {now_str}",
        f"- Research ID: `{RESEARCH_ID}` (Track 1 Path B)",
        f"- NEW PER-COIN GATE (Nuno 2026-09-22 + Mid-Encode Patch):",
        f"  - Mode-A 6m Return >= {GATE_MULT}x Buy & Hold on that coin AND denser sample n >= {DENSER_N_FLOOR}.",
        f"  - Thin n < {DENSER_N_FLOOR} -> Ineligible for paper even if x >= {GATE_MULT} (flagged THIN).",
        f"  - BTC, ETH, SOL, BNB scored independently — no seat killed solely for failing another coin.",
        f"- Fees / Slip: {FEE*100:.2f}% / side fee + {SLIP*100:.2f}% adverse slippage",
        f"- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)",
        f"- Strategy Encode Order (exactly 4):",
        f"  1. `apirine-sdo-zero-cross`",
        f"  2. `ehlers-madh-zero-cross`",
        f"  3. `premier-stochastic-osc-zero`",
        f"  4. `apirine-tradj-ema-cross`",
        f"- Track B Hard Ban: Honored (no CK / QQE / MAMA / Wilder-VS)",
        "",
        "## Executive Summary",
        f"- Total Scored Cells: {len([r for r in results if not r.skipped])} / {len(results)}",
        f"- Coin PASS (Paper-Eligible, x >= {GATE_MULT} & n >= {DENSER_N_FLOOR}): {len(pass_coin_list)}",
        f"- Thin Leaders (x >= {GATE_MULT} but n < {DENSER_N_FLOOR}, Ineligible): {len(thin_list)}",
        "",
        "## Per-Coin PASS List (Paper-Eligible)",
    ]

    if pass_coin_list:
        lines.append("| Coin | Strategy ID | TF | Mode/Params | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | Notes |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in pass_coin_list:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | {r.mode_params} | "
                f"{g6.return_pct:.2f}% | {g6.bh_return_pct:.2f}% | {g6.ratio:.3f}x | {g6.trades} | {g6.win_rate_pct:.1f}% | {'; '.join(r.notes)} |"
            )
    else:
        lines.append(f"- *None. Zero candidates met the per-coin gate (x >= {GATE_MULT}x B&H AND n >= {DENSER_N_FLOOR}).*")

    lines.extend([
        "",
        "## THIN Leaders (x >= 1.2x B&H but n < 40 — Ineligible for Paper)",
    ])

    if thin_list:
        lines.append("| Coin | Strategy ID | TF | Mode/Params | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | Notes |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in thin_list:
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            lines.append(
                f"| {r.symbol} | `{r.strategy_id}` | {r.tf} | {r.mode_params} | "
                f"{g6.return_pct:.2f}% | {g6.bh_return_pct:.2f}% | {g6.ratio:.3f}x | {g6.trades} | {g6.win_rate_pct:.1f}% | {'; '.join(r.notes)} |"
            )
    else:
        lines.append("- *None.*")

    lines.extend([
        "",
        "## Full Per-Coin Scoreboard",
        "",
        "| Strategy ID | Coin | TF | Mode/Params | n | WR% | Mode-A Ret% | B&H% | xB&H | PASS_coin | THIN | MaxDD% | Full Ret% | Full B&H% | Full xB&H | Full n | Ops 6m% | Ops Full% | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
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
            f"| `{r.strategy_id}` | {r.symbol} | {r.tf} | {r.mode_params} | "
            f"{n_6m} | {wr_6m} | {ret_6m} | {bh_6m} | {ratio_6m} | **{r.pass_coin}** | {r.thin_flag} | {dd_6m} | "
            f"{ret_full} | {bh_full} | {ratio_full} | {n_full} | "
            f"{ops_6m} | {ops_full} | {notes_str} |"
        )

    lines.append("")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return md_path, csv_path
