"""stage2-sol-aware-v1 harness: Sweep and score five strategies (BTCUSDT -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (1->5):
1. pwh-pwl-accept-break-v1
2. ehlers-cg-osc-trigger-v1
3. alma-fast-slow-cross-v1
4. cmo-zero-cross-v1
5. ehlers-roofing-zero-cross-v1

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
from backtest.path_b.stage2_sol_aware_v1 import (
    ALMA_TFS,
    CMO_TFS,
    DEFAULT_SYMBOLS,
    EHLERS_CG_TFS,
    PWH_PWL_TFS,
    RESEARCH_ID,
    ROOFING_TFS,
    STRATEGY_IDS,
)
from backtest.path_b.stage2_sol_aware_v1.alma_fast_slow_cross_v1 import (
    AlmaParams,
    compute_signals as alma_signals,
)
from backtest.path_b.stage2_sol_aware_v1.cmo_zero_cross_v1 import (
    CmoZeroCrossParams,
    compute_signals as cmo_signals,
)
from backtest.path_b.stage2_sol_aware_v1.ehlers_cg_osc_trigger_v1 import (
    EhlersCgParams,
    compute_signals as cg_signals,
)
from backtest.path_b.stage2_sol_aware_v1.ehlers_roofing_zero_cross_v1 import (
    EhlersRoofingParams,
    compute_signals as roofing_signals,
)
from backtest.path_b.stage2_sol_aware_v1.pwh_pwl_accept_break_v1 import (
    PwhPwlParams,
    compute_signals as pwh_pwl_signals,
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


# 1. PWH / PWL Accept Break
def run_pwh_pwl_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "pwh-pwl-accept-break-v1"
    for tf in PWH_PWL_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: Mode A vs B, RVOL k in {0.0 (off), 1.0, 1.5}
        params_sweep = [
            ("mode_a", 0.0, "mode_a|rvol_off"),
            ("mode_a", 1.0, "mode_a|rvol1.0"),
            ("mode_a", 1.5, "mode_a|rvol1.5"),
            ("mode_b", 0.0, "mode_b|rvol_off"),
            ("mode_b", 1.0, "mode_b|rvol1.0"),
            ("mode_b", 1.5, "mode_b|rvol1.5"),
        ]
        for mode, rvol, tag in params_sweep:
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = PwhPwlParams(mode=mode, rvol_k=rvol)
                buys, sells, stops = pwh_pwl_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 2. Ehlers CG Osc Trigger
def run_ehlers_cg_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "ehlers-cg-osc-trigger-v1"
    for tf in EHLERS_CG_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Sweep: Length in {8, 10, 14, 20}, Mode A
        for length in (8, 10, 14, 20):
            tag = f"mode_a|len{length}"
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = EhlersCgParams(length=length, mode="mode_a")
                buys, sells, stops = cg_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


# 3. ALMA Fast x Slow Cross
def run_alma_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "alma-fast-slow-cross-v1"
    for tf in ALMA_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Pairs: (9,21), (20,50), (60,120)
        # Offsets: 0.85, 0.90 (sigma fixed at 6.0)
        for fast_len, slow_len in ((9, 21), (20, 50), (60, 120)):
            for offset in (0.85, 0.90):
                tag = f"mode_a|({fast_len},{slow_len})|off{offset:g}|sig6"
                cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
                try:
                    p = AlmaParams(
                        fast_len=fast_len,
                        slow_len=slow_len,
                        offset=offset,
                        sigma=6.0,
                        mode="mode_a",
                    )
                    buys, sells, stops = alma_signals(bars, p)
                    cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                    _finish(cell)
                except Exception as exc:  # noqa: BLE001
                    cell.error = repr(exc)
                    cell.gate_6m = "ERROR"
                    cell.gate_full = "ERROR"
                _print_cell(cell)
                results.append(cell)
    return results


# 4. CMO Zero Cross
def run_cmo_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "cmo-zero-cross-v1"
    for tf in CMO_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # Length in {14, 20, 25}, Mode A and Mode B
        for length in (14, 20, 25):
            for mode in ("mode_a", "mode_b"):
                tag = f"{mode}|len{length}"
                cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
                try:
                    p = CmoZeroCrossParams(length=length, mode=mode)
                    buys, sells, stops = cmo_signals(bars, p)
                    cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                    _finish(cell)
                except Exception as exc:  # noqa: BLE001
                    cell.error = repr(exc)
                    cell.gate_6m = "ERROR"
                    cell.gate_full = "ERROR"
                _print_cell(cell)
                results.append(cell)
    return results


# 5. Ehlers Roofing Zero Cross
def run_roofing_cells(symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "ehlers-roofing-zero-cross-v1"
    for tf in ROOFING_TFS:
        if tf not in bars_by_tf:
            continue
        bars = bars_by_tf[tf]
        # (hp, ss) in {(48, 10), (40, 10), (80, 40)}, Mode A
        for hp, ss in ((48, 10), (40, 10), (80, 40)):
            tag = f"mode_a|hp{hp}_ss{ss}"
            cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=tag)
            try:
                p = EhlersRoofingParams(hp_period=hp, ss_period=ss, mode="mode_a")
                buys, sells, stops = roofing_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_strategy_on_symbol(strategy_id: str, symbol: str, bars_by_tf: dict[str, list[Bar]]) -> list[CellResult]:
    if strategy_id == "pwh-pwl-accept-break-v1":
        return run_pwh_pwl_cells(symbol, bars_by_tf)
    if strategy_id == "ehlers-cg-osc-trigger-v1":
        return run_ehlers_cg_cells(symbol, bars_by_tf)
    if strategy_id == "alma-fast-slow-cross-v1":
        return run_alma_cells(symbol, bars_by_tf)
    if strategy_id == "cmo-zero-cross-v1":
        return run_cmo_cells(symbol, bars_by_tf)
    if strategy_id == "ehlers-roofing-zero-cross-v1":
        return run_roofing_cells(symbol, bars_by_tf)
    raise ValueError(f"Unknown strategy_id: {strategy_id}")


def _reconstruct_and_eval_cell(
    symbol: str,
    parent_cell: CellResult,
    sym_bars: dict[str, list[Bar]],
) -> CellResult:
    sid = parent_cell.strategy_id
    tf = parent_cell.tf
    params_tag = parent_cell.mode_params
    cell = CellResult(symbol=symbol, strategy_id=sid, tf=tf, mode_params=params_tag)

    if tf not in sym_bars:
        cell.error = f"Missing TF {tf}"
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"
        return cell

    bars = sym_bars[tf]
    try:
        if sid == "pwh-pwl-accept-break-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            rvol = 0.0 if parts[1] == "rvol_off" else float(parts[1].replace("rvol", ""))
            p = PwhPwlParams(mode=mode, rvol_k=rvol)
            buys, sells, stops = pwh_pwl_signals(bars, p)
        elif sid == "ehlers-cg-osc-trigger-v1":
            parts = params_tag.split("|")
            length = int(parts[1].replace("len", ""))
            p = EhlersCgParams(length=length, mode="mode_a")
            buys, sells, stops = cg_signals(bars, p)
        elif sid == "alma-fast-slow-cross-v1":
            parts = params_tag.split("|")
            pair_str = parts[1].strip("()")
            f_len, s_len = [int(x) for x in pair_str.split(",")]
            off = float(parts[2].replace("off", ""))
            p = AlmaParams(fast_len=f_len, slow_len=s_len, offset=off, sigma=6.0, mode="mode_a")
            buys, sells, stops = alma_signals(bars, p)
        elif sid == "cmo-zero-cross-v1":
            parts = params_tag.split("|")
            mode = parts[0]
            length = int(parts[1].replace("len", ""))
            p = CmoZeroCrossParams(length=length, mode=mode)
            buys, sells, stops = cmo_signals(bars, p)
        elif sid == "ehlers-roofing-zero-cross-v1":
            parts = params_tag.split("|")
            hp_ss = parts[1].split("_")
            hp = int(hp_ss[0].replace("hp", ""))
            ss = int(hp_ss[1].replace("ss", ""))
            p = EhlersRoofingParams(hp_period=hp, ss_period=ss, mode="mode_a")
            buys, sells, stops = roofing_signals(bars, p)
        else:
            raise ValueError(f"Unknown sid: {sid}")

        cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stops)
        _finish(cell)
    except Exception as exc:  # noqa: BLE001
        cell.error = repr(exc)
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"

    return cell


def run_stage2_sol_aware_v1(
    *,
    years: float = 2.5,
    refresh: bool = False,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> list[CellResult]:
    """Execute locked encode order (1->5) on BTC first, then stop-ladder ETH -> SOL -> BNB."""
    needed_tfs = tuple(dict.fromkeys([*PWH_PWL_TFS, *EHLERS_CG_TFS, *ALMA_TFS, *CMO_TFS, *ROOFING_TFS, "5m", "1d"]))

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

    # OOS Stop-Ladder: ETH -> SOL (HARD FILTER) -> BNB
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

            cell = _reconstruct_and_eval_cell(oos_sym, parent_cell, sym_bars)
            _print_cell(cell)
            all_results.append(cell)

            if cell.gate_6m == "PASS":
                next_passing_cells.append(parent_cell)
            else:
                ratio_str = "ERR"
                if cell.metrics:
                    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
                    ratio_str = f"{g6.ratio:.3f}x"
                print(f"  [STOP-LADDER] {oos_sym} FAILED ({ratio_str}) for {sid} @ {tf} {params_tag} (Stopped ladder)", flush=True)

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
    md_path = path or (RESULTS_DIR / "stage2-sol-aware-v1-scoreboard.md")
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
        "- **Closed-bar only;** UTC week Monday 00:00–Monday 00:00 for PWH/PWL; long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-reopen-v1 IDs, no cmo-zone-v1 leave-50, no EMA/RSI, SMA200, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **ALMA (`alma-fast-slow-cross-v1`):** Sigma fixed at `6.0`; Offset locked at `{0.85, 0.90}`; Pairs locked at `(9,21)`, `(20,50)`, `(60,120)`. FIR Gaussian weights fallback implemented.",
        "- **Roofing (`ehlers-roofing-zero-cross-v1`):** (hp, ss) locked at `(48,10)` lead, `(40,10)`, `(80,40)`. Documented 2-pole HighPass + 2-pole SuperSmoother IIR.",
        "- **CG Osc (`ehlers-cg-osc-trigger-v1`):** Length in `{8, 10, 14, 20}`, default 10. Center-of-gravity FIR formula with 1-bar delayed trigger.",
        "- **CMO (`cmo-zero-cross-v1`):** Length in `{14, 20, 25}`, default 20. Strictly zero-cross (Mode A) and SMA(9) cross (Mode B). Never leave -50 zone.",
        "- **PWH/PWL (`pwh-pwl-accept-break-v1`):** Prior UTC ISO-week high/low. Mode A accept-break, Mode B break+retest. RVOL k in `{off, 1.0, 1.5}`.",
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
                    "", "", note_str,
                ])
                continue

            if r.error:
                lines.append(
                    f"| {r.symbol} | {r.tf} | {r.mode_params} | ERR | — | — | — | — | — | ERR | — | — | — | — | {r.error} |"
                )
                csv_rows.append([
                    r.symbol, r.strategy_id, r.tf, r.mode_params,
                    "", "", "", "", "", "ERR",
                    "", "", "", "", "", "ERR",
                    "", "", r.error,
                ])
                continue

            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            o6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
            of = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops")

            pass_6m_label = _gate_cell(g6.gate, g6.ratio)
            pass_full_label = _gate_cell(gf.gate, gf.ratio)

            notes_list = list(r.notes)
            if sol_note:
                notes_list.append(sol_note)
            if r.symbol == "SOLUSDT" and 0.9 <= g6.ratio < 1.2:
                notes_list.append("near-miss 0.9-1.2x (FAIL)")

            note_str = "; ".join(notes_list)

            lines.append(
                f"| {r.symbol} | {r.tf} | {r.mode_params} | {pass_6m_label} | {g6.return_pct:.2f} | "
                f"{g6.bh_return_pct:.2f} | {g6.ratio:.3f} | {g6.win_rate_pct:.1f} | {g6.trades} | "
                f"{pass_full_label} | {gf.ratio:.3f} | {gf.trades} | {o6.return_pct:.2f} | "
                f"{of.return_pct:.2f} | {note_str} |"
            )

            csv_rows.append([
                r.symbol,
                r.strategy_id,
                r.tf,
                r.mode_params,
                str(g6.trades),
                f"{g6.win_rate_pct:.2f}",
                f"{g6.return_pct:.2f}",
                f"{g6.bh_return_pct:.2f}",
                f"{g6.ratio:.4f}",
                g6.gate,
                str(gf.trades),
                f"{gf.win_rate_pct:.2f}",
                f"{gf.return_pct:.2f}",
                f"{gf.bh_return_pct:.2f}",
                f"{gf.ratio:.4f}",
                gf.gate,
                f"{o6.return_pct:.2f}",
                f"{of.return_pct:.2f}",
                note_str,
            ])

        lines.append("")

    lines.append("## Summary & Findings")
    lines.append("")
    total_eval = len([r for r in results if not r.skipped and not r.error])
    pass_cnt = len(pass_6m_cells)
    lines.append(f"- Total evaluated cells: {total_eval}")
    lines.append(f"- Total PASS_6m cells: {pass_cnt}")
    sol_cells = [r for r in results if r.symbol == "SOLUSDT"]
    sol_pass = [r for r in sol_cells if r.gate_6m == "PASS"]
    lines.append(f"- SOL evaluated cells: {len(sol_cells)}, SOL PASS_6m cells: {len(sol_pass)}")
    lines.append("- Hard stop rules and gate compliance strictly enforced.")
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
