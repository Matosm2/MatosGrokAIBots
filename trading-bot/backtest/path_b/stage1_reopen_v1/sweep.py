"""stage1-reopen-v1 harness: Sweep and score five strategies (BTCUSDT -> ETH -> SOL -> BNB).

LEAD gate: last-6m Mode-A return >= 1.2x buy-and-hold (same window). WR informational.
Also report full(~2y) Mode-A + ops 2.5% sizing.
Costs: 0.1%/side + 5 bps (consistent with prior Path B waves).
Closed-bar only; long-only first pass; pyramiding 0.
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
from backtest.path_b.stage1_reopen_v1 import (
    ACCDIST_TFS,
    ASI_TFS,
    DEFAULT_SYMBOLS,
    PDH_PDL_TFS,
    PIVOT_TFS,
    PVT_TFS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage1_reopen_v1.accdist_sma_cross_v1 import (
    AccDistSmaParams,
    compute_signals as accdist_signals,
)
from backtest.path_b.stage1_reopen_v1.asi_dual_break_v1 import (
    AsiDualBreakParams,
    compute_signals as asi_signals,
)
from backtest.path_b.stage1_reopen_v1.classic_floor_pivots_utc_v1 import (
    ClassicFloorPivotsParams,
    compute_signals as pivot_signals,
)
from backtest.path_b.stage1_reopen_v1.pdh_pdl_accept_break_v1 import (
    PdhPdlParams,
    compute_signals as pdh_pdl_signals,
)
from backtest.path_b.stage1_reopen_v1.pvt_ema_cross_v1 import (
    PvtEmaParams,
    compute_signals as pvt_signals,
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


def _finish(cell: CellResult) -> CellResult:
    if cell.error or cell.skipped or not cell.metrics:
        return cell
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate
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
        f"6m={cell.gate_6m}({g6.ratio:.3f}) ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% | "
        f"full={cell.gate_full}({gf.ratio:.3f}) n={gf.trades}",
        flush=True,
    )


# 1. Classic Floor Pivots
def run_pivot_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "classic-floor-pivots-utc-v1"
    for tf in PIVOT_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: Mode A vs B, day vs week (1H only for week per spec), ATR buffer k in {0.0, 0.5, 1.0}
        params_sweep = [
            ("mode_a", "day", 0.0, "mode_a|day|buf0.0"),
            ("mode_a", "day", 0.5, "mode_a|day|buf0.5"),
            ("mode_a", "day", 1.0, "mode_a|day|buf1.0"),
            ("mode_b", "day", 0.0, "mode_b|day|buf0.0"),
            ("mode_b", "day", 0.5, "mode_b|day|buf0.5"),
            ("mode_b", "day", 1.0, "mode_b|day|buf1.0"),
        ]
        if tf == "1h":
            params_sweep.extend([
                ("mode_a", "week", 0.0, "mode_a|week|buf0.0"),
                ("mode_b", "week", 0.0, "mode_b|week|buf0.0"),
            ])

        for mode, period, buf, tag in params_sweep:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = ClassicFloorPivotsParams(mode=mode, period=period, atr_buffer_k=buf)
                buys, sells, stops = pivot_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 2. PDH / PDL Accept Break
def run_pdh_pdl_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "pdh-pdl-accept-break-v1"
    for tf in PDH_PDL_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: Mode A vs B, RVOL k in {0.0, 1.0, 1.5, 2.0}
        params_sweep = [
            ("mode_a", 0.0, "mode_a|rvol_off"),
            ("mode_a", 1.0, "mode_a|rvol1.0"),
            ("mode_a", 1.5, "mode_a|rvol1.5"),
            ("mode_a", 2.0, "mode_a|rvol2.0"),
            ("mode_b", 0.0, "mode_b|rvol_off"),
            ("mode_b", 1.0, "mode_b|rvol1.0"),
            ("mode_b", 1.5, "mode_b|rvol1.5"),
            ("mode_b", 2.0, "mode_b|rvol2.0"),
        ]
        for mode, rvol, tag in params_sweep:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = PdhPdlParams(mode=mode, rvol_k=rvol)
                buys, sells, stops = pdh_pdl_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 3. PVT x EMA Cross
def run_pvt_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "pvt-ema-cross-v1"
    for tf in PVT_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: EMA len in {9, 14, 21, 34}, Mode A (and Mode B optional)
        for ema_len in (9, 14, 21, 34):
            tag = f"mode_a|ema{ema_len}"
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = PvtEmaParams(ema_len=ema_len, mode="mode_a")
                buys, sells, stops = pvt_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 4. AccDist x SMA Cross
def run_accdist_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "accdist-sma-cross-v1"
    for tf in ACCDIST_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: N in {10, 20, 50, 65}, Mode A
        for n_len in (10, 20, 50, 65):
            tag = f"mode_a|sma{n_len}"
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = AccDistSmaParams(sma_len=n_len, mode="mode_a")
                buys, sells, stops = accdist_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 5. ASI Dual Break
def run_asi_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "asi-dual-break-v1"
    for tf in ASI_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep:
        # Lookback N in {10, 20, 55}
        # Family 1: ATR proxy atr_mult in {0.5, 1.0, 1.5, 2.0}
        # Family 2: Pct close proxy in {1%, 2%, 3%}
        for n_val in (10, 20, 55):
            # Family 1 (ATR)
            for mult in (0.5, 1.0, 1.5, 2.0):
                tag = f"N{n_val}|T_atr_{mult:g}x"
                cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
                try:
                    p = AsiDualBreakParams(n=n_val, proxy_family="atr", atr_mult=mult)
                    buys, sells, stops = asi_signals(bars, p)
                    cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                    _finish(cell)
                except Exception as exc:  # noqa: BLE001
                    cell.error = repr(exc)
                    cell.gate_6m = "ERROR"
                    cell.gate_full = "ERROR"
                _print_cell(cell)
                results.append(cell)

            # Family 2 (% close)
            for pct in (0.01, 0.02, 0.03):
                pct_label = f"{int(pct * 100)}%"
                tag = f"N{n_val}|T_pct_{pct_label}"
                cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
                try:
                    p = AsiDualBreakParams(n=n_val, proxy_family="pct", pct_close=pct)
                    buys, sells, stops = asi_signals(bars, p)
                    cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                    _finish(cell)
                except Exception as exc:  # noqa: BLE001
                    cell.error = repr(exc)
                    cell.gate_6m = "ERROR"
                    cell.gate_full = "ERROR"
                _print_cell(cell)
                results.append(cell)
    return results


def run_strategy_on_symbol(
    strategy_id: str,
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
) -> list[CellResult]:
    if strategy_id == "classic-floor-pivots-utc-v1":
        return run_pivot_cells(symbol, bars_by_tf)
    if strategy_id == "pdh-pdl-accept-break-v1":
        return run_pdh_pdl_cells(symbol, bars_by_tf)
    if strategy_id == "pvt-ema-cross-v1":
        return run_pvt_cells(symbol, bars_by_tf)
    if strategy_id == "accdist-sma-cross-v1":
        return run_accdist_cells(symbol, bars_by_tf)
    if strategy_id == "asi-dual-break-v1":
        return run_asi_cells(symbol, bars_by_tf)
    raise ValueError(f"Unknown strategy_id: {strategy_id}")


def run_stage1_reopen_v1(
    *,
    years: float = 2.5,
    refresh: bool = False,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> list[CellResult]:
    """Execute locked encode order (1->5) on BTC first, then stop-ladder ETH -> SOL -> BNB."""
    needed_tfs = tuple(dict.fromkeys([*PIVOT_TFS, *PDH_PDL_TFS, *PVT_TFS, *ACCDIST_TFS, *ASI_TFS, "5m", "1d"]))

    # Step 1: Materialize BTC
    print(f"\n==================== MATERIALIZING BTCUSDT ====================", flush=True)
    btc_bars = materialize_symbol("BTCUSDT", tfs=needed_tfs, years=years, refresh=refresh)

    all_results: list[CellResult] = []

    # Execute BTC across all 5 strategies in locked encode order
    for sid in STRATEGY_IDS:
        print(f"\n==================== SCORING BTC: {sid} ====================", flush=True)
        res = run_strategy_on_symbol(sid, "BTCUSDT", btc_bars)
        all_results.extend(res)

    # Check for PASS_6m cells on BTC
    btc_pass_cells = [r for r in all_results if r.symbol == "BTCUSDT" and r.gate_6m == "PASS"]
    print(f"\n==================== BTC RUN COMPLETE: {len(btc_pass_cells)} PASS_6m CELLS ====================", flush=True)
    for c in btc_pass_cells:
        g6 = next(m for m in c.metrics if m.window == "6m" and m.mode == "gate")
        print(f"  BTC PASS: {c.strategy_id} @ {c.tf} {c.mode_params} ratio={g6.ratio:.3f} n={g6.trades}", flush=True)

    # OOS Stop-Ladder: ETH -> SOL -> BNB
    # If a cell passes BTC, evaluate on ETH. If passes ETH, evaluate on SOL. If passes SOL, evaluate on BNB.
    # SOL is the hard filter.
    ladder_symbols = ("ETHUSDT", "SOLUSDT", "BNBUSDT")
    active_passing_cells = list(btc_pass_cells)

    for oos_sym in ladder_symbols:
        if not active_passing_cells:
            print(f"\n[STOP-LADDER] No active passing cells remaining for {oos_sym}. Stop-ladder terminated.", flush=True)
            break

        print(f"\n==================== MATERIALIZING {oos_sym} ====================", flush=True)
        sym_bars = materialize_symbol(oos_sym, tfs=needed_tfs, years=years, refresh=refresh)

        next_passing_cells = []
        for parent_cell in active_passing_cells:
            sid = parent_cell.strategy_id
            tf = parent_cell.tf
            params_tag = parent_cell.mode_params
            print(f"\n[STOP-LADDER] Evaluating {oos_sym} on {sid} @ {tf} {params_tag} ...", flush=True)

            # Run just this specific cell on the new symbol
            if tf not in sym_bars:
                print(f"  Missing tf {tf} for {oos_sym}", flush=True)
                continue
            bars = sym_bars[tf]
            cell = CellResult(symbol=oos_sym, strategy_id=sid, tf=tf, mode_params=params_tag)
            try:
                # Reconstruct params and run
                if sid == "classic-floor-pivots-utc-v1":
                    parts = params_tag.split("|")
                    mode = parts[0]
                    period = parts[1]
                    buf = float(parts[2].replace("buf", ""))
                    p = ClassicFloorPivotsParams(mode=mode, period=period, atr_buffer_k=buf)
                    buys, sells, stops = pivot_signals(bars, p)
                elif sid == "pdh-pdl-accept-break-v1":
                    parts = params_tag.split("|")
                    mode = parts[0]
                    rvol = 0.0 if parts[1] == "rvol_off" else float(parts[1].replace("rvol", ""))
                    p = PdhPdlParams(mode=mode, rvol_k=rvol)
                    buys, sells, stops = pdh_pdl_signals(bars, p)
                elif sid == "pvt-ema-cross-v1":
                    parts = params_tag.split("|")
                    mode = parts[0]
                    ema_len = int(parts[1].replace("ema", ""))
                    p = PvtEmaParams(ema_len=ema_len, mode=mode)
                    buys, sells, stops = pvt_signals(bars, p)
                elif sid == "accdist-sma-cross-v1":
                    parts = params_tag.split("|")
                    mode = parts[0]
                    sma_len = int(parts[1].replace("sma", ""))
                    p = AccDistSmaParams(sma_len=sma_len, mode=mode)
                    buys, sells, stops = accdist_signals(bars, p)
                elif sid == "asi-dual-break-v1":
                    parts = params_tag.split("|")
                    n_val = int(parts[0].replace("N", ""))
                    t_str = parts[1]
                    if "T_atr_" in t_str:
                        mult = float(t_str.replace("T_atr_", "").replace("x", ""))
                        p = AsiDualBreakParams(n=n_val, proxy_family="atr", atr_mult=mult)
                    else:
                        pct = float(t_str.replace("T_pct_", "").replace("%", "")) / 100.0
                        p = AsiDualBreakParams(n=n_val, proxy_family="pct", pct_close=pct)
                    buys, sells, stops = asi_signals(bars, p)
                else:
                    raise ValueError(f"Unknown sid {sid}")

                cell.metrics = _eval_windows(oos_sym, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"

            _print_cell(cell)
            all_results.append(cell)

            if cell.gate_6m == "PASS":
                next_passing_cells.append(parent_cell)
            else:
                print(f"  [STOP-LADDER] {oos_sym} FAILED for {sid} @ {tf} {params_tag} (Stopped ladder)", flush=True)

        active_passing_cells = next_passing_cells

    return all_results


def _gate_cell(gate: str, ratio: float) -> str:
    if gate == "PASS":
        return f"PASS({ratio:.2f})"
    if gate == "FAIL":
        return f"FAIL({ratio:.2f})"
    if gate == "ERROR":
        return "ERR"
    if gate == "N/A":
        return "N/A"
    return "—"


def write_scoreboard(results: list[CellResult], path: Path | None = None) -> tuple[Path, Path]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = path or (RESULTS_DIR / "stage1-reopen-v1-scoreboard.md")
    csv_path = md_path.with_suffix(".csv")

    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
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
        "- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL is the hard filter**.",
        "- **Closed-bar only;** UTC day 00:00–24:00; long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no EMA/RSI, SMA200, Woodie, Camarilla, VWAP±σ, CMF, OBV, Chaikin Osc, etc.).",
        "",
        "## ASI Limit-Move T-Proxy Locked Specification",
        "",
        "- Crypto has no exchange daily limit move; `T_PROXY.md` locked before ASI runs.",
        "- **Family 1 (ATR proxy):** `T = atr_mult * ATR(14)` with `atr_mult ∈ {0.5, 1.0, 1.5, 2.0}`, baseline `1.0x`.",
        "- **Family 2 (% of close):** `T = pct * close[i-1]` with `pct ∈ {1%, 2%, 3%}`.",
        "- Dual breakout: `close > highest(high, N)[1]` AND `ASI > highest(ASI, N)[1]` with `N ∈ {10, 20, 55}`.",
        "",
        "## PASS_6m cells (LEAD)",
        "",
    ]

    pass_6m_cells = [r for r in results if r.gate_6m == "PASS"]
    if not pass_6m_cells:
        lines.append("_none_")
    else:
        for r in pass_6m_cells:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}): 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f} n={gf.trades}"
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

    for sid in STRATEGY_IDS:
        fam = [r for r in results if r.strategy_id == sid]
        if not fam:
            continue
        lines.append(f"### {sid}")
        lines.append("")
        lines.append(
            "| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | "
            "full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |"
        )
        lines.append(
            "|--------|----|-------------|---------|---------|--------|------|--------|------|"
            "-----------|-----------|--------|---------|-----------|-------|"
        )

        for r in fam:
            sol_note = "SOL filter" if r.symbol == "SOLUSDT" else ""
            if r.skipped:
                note_str = "; ".join(r.notes)
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | N/A | — | — | — | — | — | N/A | — | — | — | — | {note_str} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params,
                    "", "", "", "", "", "N/A",
                    "", "", "", "", "", "N/A",
                    "", "", note_str
                ])
                continue
            if r.error:
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | ERROR | — | — | — | — | — | ERROR | — | — | — | — | {r.error} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params,
                    "", "", "", "", "", "ERROR",
                    "", "", "", "", "", "ERROR",
                    "", "", r.error
                ])
                continue

            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            o6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
            of = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops")

            pass_6m_yn = "Y" if r.gate_6m == "PASS" else "N"
            pass_full_yn = "Y" if r.gate_full == "PASS" else "N"

            lines.append(
                f"| {r.symbol} | {r.tf} | {r.mode_params} | {_gate_cell(r.gate_6m, g6.ratio)} | {g6.return_pct:.2f} | "
                f"{g6.bh_return_pct:.2f} | {g6.ratio:.3f} | {g6.win_rate_pct:.1f} | {g6.trades} | "
                f"{_gate_cell(r.gate_full, gf.ratio)} | {gf.ratio:.3f} | {gf.trades} | "
                f"{o6.return_pct:.2f} | {of.return_pct:.2f} | {sol_note} |"
            )

            csv_rows.append([
                r.symbol,
                r.strategy_id,
                r.tf,
                r.mode_params,
                str(g6.trades),
                f"{g6.win_rate_pct:.1f}",
                f"{g6.return_pct:.2f}",
                f"{g6.bh_return_pct:.2f}",
                f"{g6.ratio:.3f}",
                pass_6m_yn,
                str(gf.trades),
                f"{gf.win_rate_pct:.1f}",
                f"{gf.return_pct:.2f}",
                f"{gf.bh_return_pct:.2f}",
                f"{gf.ratio:.3f}",
                pass_full_yn,
                f"{o6.return_pct:.2f}",
                f"{of.return_pct:.2f}",
                sol_note,
            ])
        lines.append("")

    lines.extend(
        [
            "## Summary & Findings",
            "",
            f"- Total evaluated cells: {len(results)}",
            f"- Total PASS_6m cells: {len(pass_6m_cells)}",
            "- Hard stop rules and gate compliance strictly enforced.",
            "",
        ]
    )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
