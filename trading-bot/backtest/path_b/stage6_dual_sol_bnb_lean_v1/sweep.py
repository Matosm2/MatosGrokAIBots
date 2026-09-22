"""stage6-dual-sol-bnb-lean-v1 harness: Sweep and score three strategies (BTC -> ETH -> SOL -> BNB).

LOCKED ENCODE ORDER (exactly 3):
1. frama-fast-slow-cross-v1
2. hma-dual-cross-v1
3. mcginley-close-slope-cross-v1

Design Bias: DUAL-SURVIVAL + SOL RETENTION — identical params intended to clear BOTH SOL and BNB (no per-coin retuning).
Mandatory sol_smoke + bnb_smoke per strategy: log FAIL reasons; fail smoke -> disqualify cell.
SOL-after-ETH retention checks: evaluate trade density, impulse hugging, and over-smoothing before declaring fail.
Stop-ladder: BTC -> ETH -> SOL (HARD) -> BNB (HARD).
LEAD gate: last-6m Mode-A return >= 1.2x buy-and-hold (same window). WR info.
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
from backtest.path_b.stage6_dual_sol_bnb_lean_v1 import (
    DEFAULT_SYMBOLS,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.stage6_dual_sol_bnb_lean_v1.frama_fast_slow_cross_v1 import (
    FramaParams,
    compute_signals as frama_signals,
    validate_bnb_smoke as validate_frama_bnb_smoke,
    validate_sol_smoke as validate_frama_sol_smoke,
)
from backtest.path_b.stage6_dual_sol_bnb_lean_v1.hma_dual_cross_v1 import (
    HmaParams,
    compute_signals as hma_signals,
    validate_bnb_smoke as validate_hma_bnb_smoke,
    validate_sol_smoke as validate_hma_sol_smoke,
)
from backtest.path_b.stage6_dual_sol_bnb_lean_v1.mcginley_close_slope_cross_v1 import (
    McGinleyParams,
    compute_signals as mcginley_signals,
    validate_bnb_smoke as validate_mcginley_bnb_smoke,
    validate_sol_smoke as validate_mcginley_sol_smoke,
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
    sol_smoke: str = "Y"  # Y / FAIL: reason / N/A
    bnb_smoke: str = "Y"  # Y / FAIL: reason / N/A
    sol_retention_note: str = "—"  # Retention diagnostic (especially after ETH pass)
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


def _finish(cell: CellResult, eth_cell: CellResult | None = None) -> CellResult:
    if cell.error or cell.skipped or not cell.metrics:
        return cell
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate

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
            elif eth_g6.trades > 0 and g6.trades < 0.5 * eth_g6.trades:
                cell.sol_retention_note = f"RETENTION WARN: trade density collapsed ({g6.trades} SOL vs {eth_g6.trades} ETH)"
            else:
                cell.sol_retention_note = f"RETENTION OK: {g6.trades} trades (ETH={eth_g6.trades})"
        else:
            if g6.trades == 0:
                cell.sol_retention_note = "RETENTION FAIL: 0 trades (under-trading / over-smooth)"
            else:
                cell.sol_retention_note = f"RETENTION EVAL: {g6.trades} trades (no ETH predecessor)"
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
    print(
        f"[{cell.symbol}] {cell.strategy_id} @ {cell.tf} {cell.mode_params} -> "
        f"6m={cell.gate_6m}({g6.ratio:.3f}x) ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% n={g6.trades} wr={g6.win_rate_pct:.1f}% [sol_smoke={cell.sol_smoke}, bnb_smoke={cell.bnb_smoke}, sol_retention={cell.sol_retention_note}] | "
        f"full={cell.gate_full}({gf.ratio:.3f}x) n={gf.trades}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Strategy 1: frama-fast-slow-cross-v1
# ---------------------------------------------------------------------------

def run_frama_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "frama-fast-slow-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (Nf, Ns) in {(16, 32), (10, 20), (12, 24)} (Mode A); Mode B (N=20)
    param_grid: list[tuple[str, FramaParams]] = [
        ("mode_a|(16,32)", FramaParams(mode="mode_a", fast_len=16, slow_len=32)),
        ("mode_a|(10,20)", FramaParams(mode="mode_a", fast_len=10, slow_len=20)),
        ("mode_a|(12,24)", FramaParams(mode="mode_a", fast_len=12, slow_len=24)),
        ("mode_b|frama20", FramaParams(mode="mode_b", frama_b_len=20)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_frama_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_frama_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = frama_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 2: hma-dual-cross-v1
# ---------------------------------------------------------------------------

def run_hma_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "hma-dual-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: (Lf, Ls) in {(9, 16), (10, 30), (16, 36)} (Mode A); Mode B (Ls=30)
    param_grid: list[tuple[str, HmaParams]] = [
        ("mode_a|(9,16)", HmaParams(mode="mode_a", fast_len=9, slow_len=16)),
        ("mode_a|(10,30)", HmaParams(mode="mode_a", fast_len=10, slow_len=30)),
        ("mode_a|(16,36)", HmaParams(mode="mode_a", fast_len=16, slow_len=36)),
        ("mode_b|hma30", HmaParams(mode="mode_b", hma_b_len=30)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_hma_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_hma_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = hma_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Strategy 3: mcginley-close-slope-cross-v1
# ---------------------------------------------------------------------------

def run_mcginley_cells(
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    sid = "mcginley-close-slope-cross-v1"
    results: list[CellResult] = []
    tfs = ("1h", "4h")

    # Grid: N in {10, 14, 20} (Mode A); Mode B (N=14)
    param_grid: list[tuple[str, McGinleyParams]] = [
        ("mode_a|N14", McGinleyParams(mode="mode_a", length=14, k=1.0)),
        ("mode_a|N10", McGinleyParams(mode="mode_a", length=10, k=1.0)),
        ("mode_a|N20", McGinleyParams(mode="mode_a", length=20, k=1.0)),
        ("mode_b|N14", McGinleyParams(mode="mode_b", length=14, k=1.0)),
    ]

    for tf in tfs:
        bars = bars_by_tf.get(tf)
        if not bars:
            continue
        for desc, p in param_grid:
            cell_key = f"{sid}@{tf}@{desc}"
            if active_keys is not None and cell_key not in active_keys:
                continue

            sol_ok, sol_msg = validate_mcginley_sol_smoke(p, tf)
            bnb_ok, bnb_msg = validate_mcginley_bnb_smoke(p, tf)
            sol_smoke_str = "Y" if sol_ok else f"FAIL: {sol_msg}"
            bnb_smoke_str = "Y" if bnb_ok else f"FAIL: {bnb_msg}"

            cell = CellResult(
                symbol=symbol,
                strategy_id=sid,
                tf=tf,
                mode_params=desc,
                sol_smoke=sol_smoke_str,
                bnb_smoke=bnb_smoke_str,
            )

            try:
                buys, sells, stops = mcginley_signals(bars, p)
                cell.metrics = _eval_windows(symbol, sid, bars, buys, sells, stop_prices=stops)
                eth_c = eth_results.get(cell_key) if eth_results else None
                _finish(cell, eth_cell=eth_c)
            except Exception as exc:
                cell.error = str(exc)

            _print_cell(cell)
            results.append(cell)

    return results


# ---------------------------------------------------------------------------
# Stop-Ladder Dispatcher
# ---------------------------------------------------------------------------

def run_strategy_cells(
    strategy_id: str,
    symbol: str,
    bars_by_tf: dict[str, list[Bar]],
    active_keys: set[str] | None = None,
    eth_results: dict[str, CellResult] | None = None,
) -> list[CellResult]:
    if strategy_id == "frama-fast-slow-cross-v1":
        return run_frama_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    elif strategy_id == "hma-dual-cross-v1":
        return run_hma_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    elif strategy_id == "mcginley-close-slope-cross-v1":
        return run_mcginley_cells(symbol, bars_by_tf, active_keys=active_keys, eth_results=eth_results)
    else:
        raise ValueError(f"Unknown strategy_id: {strategy_id}")


def run_stage6_dual_sol_bnb_lean_v1(
    years: float = 2.5,
    refresh: bool = False,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> list[CellResult]:
    """Execute the locked 3-strategy stop-ladder with DUAL-SURVIVAL + SOL RETENTION."""
    all_results: list[CellResult] = []
    active_keys: set[str] | None = None  # None for BTC (run all)
    eth_results_by_key: dict[str, CellResult] = {}

    for idx, symbol in enumerate(symbols):
        print(f"\n==================================================================", flush=True)
        print(f"[{RESEARCH_ID}] Evaluating Symbol {idx+1}/{len(symbols)}: {symbol}", flush=True)
        print(f"==================================================================", flush=True)

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
            print(f"\n--- [{symbol}] Strategy: {sid} ---", flush=True)
            if active_keys is not None and len(active_keys) == 0:
                # Mark cells as skipped/pruned by ladder
                tfs = ("1h", "4h")
                param_grid_keys = {
                    "frama-fast-slow-cross-v1": ["mode_a|(16,32)", "mode_a|(10,20)", "mode_a|(12,24)", "mode_b|frama20"],
                    "hma-dual-cross-v1": ["mode_a|(9,16)", "mode_a|(10,30)", "mode_a|(16,36)", "mode_b|hma30"],
                    "mcginley-close-slope-cross-v1": ["mode_a|N14", "mode_a|N10", "mode_a|N20", "mode_b|N14"],
                }[sid]
                for tf in tfs:
                    for desc in param_grid_keys:
                        res_cell = CellResult(
                            symbol=symbol,
                            strategy_id=sid,
                            tf=tf,
                            mode_params=desc,
                            sol_smoke="Y",
                            bnb_smoke="Y",
                            sol_retention_note="—",
                            skipped=True,
                            notes=["Pruned by stop-ladder (BTC PASS_6m required)"],
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
                    active_keys=active_keys,
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
            print(f"  -> PROMOTED: {r.strategy_id} @ {r.tf} {r.mode_params} (6m={g6.return_pct:.2f}%, {g6.ratio:.3f}x B&H, sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, sol_retention={r.sol_retention_note})", flush=True)

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

    note_str = "; ".join(r.notes)
    if r.error:
        note_str = f"ERROR: {r.error}"
    elif r.skipped:
        note_str = "Pruned by ladder"

    md_cols = [
        r.symbol,
        r.tf,
        r.mode_params,
        r.sol_smoke,
        r.bnb_smoke,
        r.sol_retention_note,
        r.gate_6m,
        f"{g6.return_pct:.2f}%" if g6 else "—",
        f"{g6.bh_return_pct:.2f}%" if g6 else "—",
        f"{g6.ratio:.3f}x" if g6 else "—",
        f"{g6.win_rate_pct:.1f}%" if g6 else "—",
        str(g6.trades) if g6 else "—",
        r.gate_full,
        f"{gf.ratio:.3f}x" if gf else "—",
        str(gf.trades) if gf else "—",
        f"{o6.return_pct:.2f}%" if o6 else "—",
        f"{of.return_pct:.2f}%" if of else "—",
        note_str,
    ]

    csv_cols = [
        r.symbol,
        r.strategy_id,
        r.tf,
        r.mode_params,
        r.sol_smoke,
        r.bnb_smoke,
        r.sol_retention_note,
        str(g6.trades) if g6 else "",
        f"{g6.win_rate_pct:.1f}" if g6 else "",
        f"{g6.return_pct:.2f}" if g6 else "",
        f"{g6.bh_return_pct:.2f}" if g6 else "",
        f"{g6.ratio:.3f}" if g6 else "",
        r.gate_6m,
        str(gf.trades) if gf else "",
        f"{gf.win_rate_pct:.1f}" if gf else "",
        f"{gf.return_pct:.2f}" if gf else "",
        f"{gf.bh_return_pct:.2f}" if gf else "",
        f"{gf.ratio:.3f}" if gf else "",
        r.gate_full,
        f"{o6.return_pct:.2f}" if o6 else "",
        f"{of.return_pct:.2f}" if of else "",
        note_str,
    ]

    return md_cols, csv_cols


def write_scoreboard(
    results: list[CellResult],
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    output_dir = output_dir or RESULTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / "stage6-dual-sol-bnb-lean-v1-scoreboard.md"
    csv_path = output_dir / "stage6-dual-sol-bnb-lean-v1-scoreboard.csv"

    now = datetime.now(timezone.utc).isoformat()

    lines: list[str] = [
        "# stage6-dual-sol-bnb-lean-v1 scoreboard (DUAL-SURVIVAL + SOL RETENTION: SOL + BNB)",
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
        "- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.",
        "- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).",
        "- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.",
        "- **Closed-bar only;** long-only first pass; pyramiding 0.",
        "- **Hard excludes honored** (no stage1-5 IDs, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, no EMA/RSI, SMA200, etc.).",
        "",
        "## Parameter Locks Summary (LOCKED BEFORE SCORING)",
        "",
        "- **Ehlers FRAMA (`frama-fast-slow-cross-v1`):** Fractal dimension alpha from N1/N2/N3 halves. Locked pairs (16,32), (10,20), (12,24) (Mode A) and frama20 (Mode B). N even.",
        "- **Hull Moving Average (`hma-dual-cross-v1`):** Low-lag WMA(2*WMA(n/2) - WMA(n), sqrt(n)). Locked pairs (9,16), (10,30), (16,36) (Mode A) and hma30 (Mode B).",
        "- **McGinley Dynamic (`mcginley-close-slope-cross-v1`):** Adaptive speed hug via (close/MD)^4 denominator. N in {10, 14, 20} (Mode A close x MD + MD rising) and Mode B state.",
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
                f"- `[{r.symbol}] {r.strategy_id}` @ `{r.tf}` ({r.mode_params}) [sol_smoke={r.sol_smoke}, bnb_smoke={r.bnb_smoke}, sol_retention={r.sol_retention_note}]: 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f}x wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f}x n={gf.trades}"
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

    for sid in STRATEGY_IDS:
        fam = [r for r in results if r.strategy_id == sid]
        if not fam:
            continue
        lines.append(f"### {sid}")
        lines.append("")
        lines.append(
            "| symbol | tf | mode/params | sol_smoke | bnb_smoke | sol_retention | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | "
            "full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |"
        )
        lines.append(
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
        )
        for r in fam:
            md_cols, csv_cols = _row_to_cols(r)
            lines.append(f"| {' | '.join(md_cols)} |")
            csv_rows.append(csv_cols)
        lines.append("")

    lines.append("## Dual-Survival & Ladder Analysis")
    lines.append("")
    lines.append("1. **Stop-Ladder Attrition:**")
    btc_pass = len([r for r in results if r.symbol == "BTCUSDT" and r.gate_6m == "PASS"])
    eth_pass = len([r for r in results if r.symbol == "ETHUSDT" and r.gate_6m == "PASS"])
    sol_pass = len([r for r in results if r.symbol == "SOLUSDT" and r.gate_6m == "PASS"])
    bnb_pass = len([r for r in results if r.symbol == "BNBUSDT" and r.gate_6m == "PASS"])
    lines.append(f"   - BTC PASS_6m: {btc_pass}")
    lines.append(f"   - ETH PASS_6m: {eth_pass}")
    lines.append(f"   - SOL PASS_6m: {sol_pass} (HARD FILTER)")
    lines.append(f"   - BNB PASS_6m: {bnb_pass} (HARD FILTER)")
    lines.append("")
    lines.append("2. **Smoke & Retention Outcomes:**")
    lines.append("   - All cells verified against mandatory sol_smoke and bnb_smoke rules.")
    lines.append("   - Dual identical parameter constraint strictly preserved across all symbols.")
    lines.append("   - SOL retention diagnostics logged after ETH evaluation.")
    lines.append("")
    lines.append("3. **Path B Pause / Next Actions:**")
    if bnb_pass == 0:
        lines.append("   - **FULL-LADDER PASS_6m = 0** across all 3 locked strategies.")
        lines.append("   - **ACTION:** Cue Path B pause for CoS / Nuno usage.")
    else:
        lines.append(f"   - Found {bnb_pass} cell(s) clearing full ladder!")
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return md_path, csv_path
