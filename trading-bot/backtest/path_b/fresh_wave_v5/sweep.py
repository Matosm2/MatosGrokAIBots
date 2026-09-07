"""fresh-wave-v5 harness: Elder pairs + CMF/LinReg/MFI/UO sprays (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. Part B parked. No burned grafts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v5 import (
    CMF_PERIODS,
    CMF_PRIMARY_PERIOD,
    COARSE_FIRST_TFS,
    ELDER_PAIRS,
    FI_EMA_LENGTHS,
    PREFERRED_4H_1D,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.fresh_wave_v5.cmf_flow_v1 import (
    CmfFlowParams,
    compute_signals as cmf_signals,
)
from backtest.path_b.fresh_wave_v5.elder_triple_screen_fi_v1 import (
    ElderTripleScreenParams,
    compute_signals as elder_signals,
)
from backtest.path_b.fresh_wave_v5.linreg_r2_v1 import (
    LinregR2Params,
    compute_signals as linreg_signals,
)
from backtest.path_b.fresh_wave_v5.mfi_only_v1 import (
    MfiOnlyParams,
    compute_signals as mfi_signals,
)
from backtest.path_b.fresh_wave_v5.ultimate_oscillator_v1 import (
    UltimateOscParams,
    compute_signals as uo_signals,
)
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b

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
    strategy_id: str
    tf: str  # display / cell key (may include variant labels)
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
                "BTCUSDT",
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
        print(f"  -> N/A ({'; '.join(cell.notes)})", flush=True)
        return
    if cell.error:
        print(f"  -> ERROR {cell.error}", flush=True)
        return
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    print(
        f"  -> 6m={cell.gate_6m}({g6.ratio:.3f}) n={g6.trades} wr={g6.win_rate_pct:.1f}% | "
        f"full={cell.gate_full}({gf.ratio:.3f}) n={gf.trades}",
        flush=True,
    )


def run_elder_cells(btc: dict[str, list[Bar]]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "elder-triple-screen-fi-v1"
    for entry_tf, tide_tf in ELDER_PAIRS:
        for fi_ema in FI_EMA_LENGTHS:
            label = f"{entry_tf}/{tide_tf}|fi{fi_ema}"
            print(f"[fresh-wave-v5] {sid} @ {label} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=label)
            try:
                buys, sells, stops = elder_signals(
                    btc[entry_tf],
                    btc[tide_tf],
                    entry_tf,
                    tide_tf,
                    ElderTripleScreenParams(fi_ema=fi_ema),
                )
                cell.metrics = _eval_windows(sid, btc[entry_tf], buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_cmf_cells(
    btc: dict[str, list[Bar]], tfs: tuple[str, ...]
) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "cmf-flow-v1"
    # Mode-A primary period across TFs, then other periods as labeled, then Mode-B
    for mode, channel_n in (("A", 20), ("B", 20), ("B", 55)):
        if mode == "A":
            periods = CMF_PERIODS  # labeled sweep; 21 is primary
        else:
            periods = (CMF_PRIMARY_PERIOD,)  # Mode-B primary period only
        for period in periods:
            for tf in tfs:
                tag = f"{tf}|p{period}|{mode}"
                if mode == "B":
                    tag += f"|n{channel_n}"
                # Skip duplicate Mode-A non-primary on fine TFs if we want — run all
                print(f"[fresh-wave-v5] {sid} @ {tag} ...", flush=True)
                cell = CellResult(strategy_id=sid, tf=tag)
                try:
                    buys, sells = cmf_signals(
                        btc[tf],
                        CmfFlowParams(period=period, mode=mode, channel_n=channel_n),
                    )
                    cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                    _finish(cell)
                except Exception as exc:  # noqa: BLE001
                    cell.error = repr(exc)
                    cell.gate_6m = "ERROR"
                    cell.gate_full = "ERROR"
                _print_cell(cell)
                results.append(cell)
    return results


def run_linreg_cells(
    btc: dict[str, list[Bar]], tfs: tuple[str, ...]
) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "linreg-r2-v1"
    configs: list[tuple[int, float, str]] = [
        (20, 0.7, "A"),  # primary
        (20, 0.8, "A"),
        (50, 0.7, "A"),
        (100, 0.7, "A"),
        (20, 0.7, "B"),
    ]
    for length, r2_gate, mode in configs:
        for tf in tfs:
            tag = f"{tf}|L{length}|r{r2_gate}|{mode}"
            print(f"[fresh-wave-v5] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = linreg_signals(
                    btc[tf],
                    LinregR2Params(length=length, r2_gate=r2_gate, mode=mode),
                )
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_mfi_cells(
    btc: dict[str, list[Bar]], tfs: tuple[str, ...]
) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "mfi-only-v1"
    configs: list[tuple[int, float, float]] = [
        (14, 20.0, 80.0),  # primary
        (10, 20.0, 80.0),
        (20, 20.0, 80.0),
        (14, 15.0, 85.0),
    ]
    for length, lo, hi in configs:
        for tf in tfs:
            tag = f"{tf}|{length}|{int(lo)}/{int(hi)}"
            print(f"[fresh-wave-v5] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = mfi_signals(
                    btc[tf],
                    MfiOnlyParams(length=length, low_level=lo, high_level=hi),
                )
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_uo_cells(
    btc: dict[str, list[Bar]], tfs: tuple[str, ...]
) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "ultimate-oscillator-v1"
    configs: list[tuple[int, int, int, str]] = [
        (7, 14, 28, "classic"),  # primary
        (7, 14, 28, "B"),
        (5, 10, 20, "classic"),
        (10, 20, 40, "classic"),
    ]
    for short, mid, long, mode in configs:
        for tf in tfs:
            tag = f"{tf}|{short},{mid},{long}|{mode}"
            print(f"[fresh-wave-v5] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = uo_signals(
                    btc[tf],
                    UltimateOscParams(short=short, mid=mid, long=long, mode=mode),
                )
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_fresh_wave_v5(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
    prefer_4h_1d: bool = False,
    skip_mode_b: bool = False,
) -> list[CellResult]:
    tfs = tfs or COARSE_FIRST_TFS
    if prefer_4h_1d:
        tfs = tuple(t for t in COARSE_FIRST_TFS if t in set(PREFERRED_4H_1D) or t in ("2d",))
        # kick: prefer 4h–1d; include 2d as coarse
        tfs = tuple(dict.fromkeys([*(PREFERRED_4H_1D), "2d"]))
    need = list(dict.fromkeys([*tfs, *SWEEP_TFS, "5m", "1d", "2d", "1w", "4h"]))
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    results: list[CellResult] = []

    # Priority 1: Elder pair cells
    results.extend(run_elder_cells(btc))

    # Priority 2/3: other four — Mode-A-ish first via function order
    results.extend(run_cmf_cells(btc, tfs))
    results.extend(run_linreg_cells(btc, tfs))
    results.extend(run_mfi_cells(btc, tfs))
    results.extend(run_uo_cells(btc, tfs))

    if skip_mode_b:
        results = [
            r
            for r in results
            if "|B" not in r.tf and "|B|" not in r.tf and not r.tf.endswith("|B")
        ]
    return results


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


def write_scoreboard(results: list[CellResult], path: Path | None = None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "fresh-wave-v5-scoreboard.md")
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts. Part B parked.**",
        "",
        "## Scoring",
        "",
        f"- **LEAD gate:** 6m Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_6m` (≥1 trade). WR informational.",
        f"- **Also:** full(~2y) Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_full` (informational)",
        f"- Costs: 0.10%/side fee + 5 bps slip; Mode-A **{GATE_SIZE_PCT:.0f}%** + Mode-B ops **{OPS_SIZE_PCT}%** (ops not scored)",
        "- Symbol: BTCUSDT only (no ETH OOS in this PR). Agg: 5m→sub-daily; 1d native; 2d=2×1d; 1w=7×1d.",
        "- Elder: paired TFs only `(4h,1d)`, `(1d,1w)`; FI EMA primary **2** (+13 labeled).",
        "- CMF primary period **21** (sweep 14/20/21/30 labeled); Mode A zero-cross before Mode B channel.",
        "- LinReg primary L=20 R²=0.7 Mode A; MFI 14 @20/80; UO 7/14/28 classic (+ Mode-B cross 30).",
        "- `chandelier-exit` ATR22×3 = helper/tests only (not a primary seat).",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **elder-triple-screen-fi-v1** — Tide MACD-hist rising; EMA(FI,2)<0; buy-stop prior high cancel ~2 bars; exit tide flip / FI>0.",
        "2. **cmf-flow-v1** — Mode A: CMF cross >0; Mode B: close > N-bar high & CMF>0; exit opposite.",
        "3. **linreg-r2-v1** — Mode A: close>+2σ & slope>0 & R²≥gate; Mode B: fade ≤−2σ; exit mid/opposite.",
        "4. **mfi-only-v1** — MFI was ≤20 then cross >20; exit ≥80 or mid-50. **No RSI graft.**",
        "5. **ultimate-oscillator-v1** — Classic bull-div + interim UO break; Mode-B cross 30; exit ≥70 or >50 then <45.",
        "",
        "## PASS_6m cells (LEAD)",
        "",
    ]
    six_pass = [r for r in results if r.gate_6m == "PASS"]
    if not six_pass:
        lines.append("_none_")
    else:
        for r in six_pass:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f} n={gf.trades}"
            )
    lines.append("")
    lines.append("## PASS_full cells (informational; not LEAD)")
    lines.append("")
    full_pass = [r for r in results if r.gate_full == "PASS"]
    if not full_pass:
        lines.append("_none_")
    else:
        for r in full_pass:
            g = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: full ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | 6m={r.gate_6m}"
            )
    lines.append("")

    # Compact LEAD tables by family (primary-ish rows)
    lines.append("## LEAD 6m by family (all scored cells)")
    lines.append("")
    for sid in STRATEGY_IDS:
        fam = [r for r in results if r.strategy_id == sid]
        if not fam:
            continue
        lines.append(f"### {sid}")
        lines.append("")
        lines.append(
            "| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | "
            "full | full_ratio | full_n | ops_6m% | ops_full% | error |"
        )
        lines.append(
            "|------|----|---------|--------|----------|--------|------|"
            "------|------------|--------|---------|-----------|-------|"
        )
        for r in fam:
            if r.skipped:
                lines.append(
                    f"| {r.tf} | N/A | — | — | — | — | — | N/A | — | — | — | — | "
                    f"{'; '.join(r.notes)} |"
                )
                continue
            if r.error:
                lines.append(
                    f"| {r.tf} | ERROR | — | — | — | — | — | ERROR | — | — | — | — | "
                    f"{r.error} |"
                )
                continue
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            o6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
            of = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops")
            lines.append(
                f"| {r.tf} | {_gate_cell(r.gate_6m, g6.ratio)} | {g6.return_pct:.2f} | "
                f"{g6.bh_return_pct:.2f} | {g6.ratio:.3f} | {g6.win_rate_pct:.1f} | {g6.trades} | "
                f"{_gate_cell(r.gate_full, gf.ratio)} | {gf.ratio:.3f} | {gf.trades} | "
                f"{o6.return_pct:.2f} | {of.return_pct:.2f} |  |"
            )
        lines.append("")

    lines.extend(
        [
            "## Caveats",
            "",
            "- LEAD = 6m Mode-A sizing only. full(~2y) context only.",
            "- Strategy Mode A/B (CMF/LinReg/UO) ≠ sizing Mode-B ops 2.5%.",
            "- No param retune on 6m after freeze. No Part B mid-board adds.",
            "- Hold prior PRs #15–#22 unmerged; this PR is additive fresh-wave-v5 only.",
            "- No OOS (ETH/SOL/BNB) in this PR.",
            "",
            f"## IDs frozen: {', '.join(STRATEGY_IDS)}",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
