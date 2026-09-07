"""fresh-wave-v7 harness: RVI / CHOP / Elder Impulse sprays (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. Part B last 3 seats. No paper.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v7 import (
    COARSE_FIRST_TFS,
    PREFERRED_4H_1D,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.fresh_wave_v7.chop_breakout_v1 import (
    ChopBreakoutParams,
    compute_signals as chop_signals,
)
from backtest.path_b.fresh_wave_v7.elder_impulse_v1 import (
    ElderImpulseParams,
    compute_signals as elder_signals,
)
from backtest.path_b.fresh_wave_v7.rvi_signal_v1 import (
    RviSignalParams,
    compute_signals as rvi_signals,
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
    tf: str
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


def _ordered_tfs(tfs: tuple[str, ...], prefer: tuple[str, ...] | None = None) -> tuple[str, ...]:
    """Prefer listed TFs first (still within `tfs`), then remaining coarse-first."""
    if not prefer:
        return tfs
    pref = [t for t in prefer if t in tfs]
    rest = [t for t in tfs if t not in set(pref)]
    return tuple(pref + rest)


def run_rvi_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "rvi-signal-v1"
    order = _ordered_tfs(tfs, PREFERRED_4H_1D + ("2d",))
    for tf in order:
        tag = f"{tf}|rvi10|sig4"
        print(f"[fresh-wave-v7] {sid} @ {tag} ...", flush=True)
        cell = CellResult(strategy_id=sid, tf=tag)
        try:
            buys, sells = rvi_signals(btc[tf], RviSignalParams())
            cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
            _finish(cell)
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            cell.gate_full = "ERROR"
        _print_cell(cell)
        results.append(cell)
    return results


def run_chop_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "chop-breakout-v1"
    # Full 16; primary N=20; labeled N=55 optional
    configs: list[int] = [20, 55]
    for break_n in configs:
        for tf in tfs:
            tag = f"{tf}|chop14|n{break_n}"
            print(f"[fresh-wave-v7] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = chop_signals(
                    btc[tf], ChopBreakoutParams(break_n=break_n)
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


def run_elder_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "elder-impulse-v1"
    order = _ordered_tfs(tfs, PREFERRED_4H_1D + ("2d",))
    for tf in order:
        tag = f"{tf}|ema13|cancel2"
        print(f"[fresh-wave-v7] {sid} @ {tag} ...", flush=True)
        cell = CellResult(strategy_id=sid, tf=tag)
        try:
            buys, sells = elder_signals(btc[tf], ElderImpulseParams())
            cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
            _finish(cell)
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            cell.gate_full = "ERROR"
        _print_cell(cell)
        results.append(cell)
    return results


def run_fresh_wave_v7(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
    prefer_coarse: bool = False,
) -> list[CellResult]:
    tfs = tfs or COARSE_FIRST_TFS
    if prefer_coarse:
        band = {"2d", "1d", "12h", "9h", "7h", "6h", "5h", "4h"}
        tfs = tuple(t for t in COARSE_FIRST_TFS if t in band)
    need = list(dict.fromkeys([*tfs, *SWEEP_TFS, "5m", "1d", "2d"]))
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    results: list[CellResult] = []
    results.extend(run_rvi_cells(btc, tfs))
    results.extend(run_chop_cells(btc, tfs))
    results.extend(run_elder_cells(btc, tfs))
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
    path = path or (RESULTS_DIR / "fresh-wave-v7-scoreboard.md")
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**",
        "",
        "## Scoring",
        "",
        f"- **LEAD gate:** 6m Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_6m` (≥1 trade). WR informational.",
        f"- **Also:** full(~2y) Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_full` (informational)",
        f"- Costs: 0.10%/side fee + 5 bps slip; Mode-A **{GATE_SIZE_PCT:.0f}%** + Mode-B ops **{OPS_SIZE_PCT}%** (ops not scored)",
        "- Symbol: BTCUSDT only (no ETH OOS in this PR). Agg: 5m→sub-daily; 1d native; 2d=2×1d.",
        "- RVI(**10**) Signal(**4**): crossover + RVI>0; exit crossunder or RVI<0; prefer 4h–1d.",
        "- CHOP(**14**)<**38.2** + close>prior **20**-high; exit prior **10**-low or CHOP>**61.8**; full 16; NOT Donchian; no ADX.",
        "- Elder Impulse: EMA(**13**)+MACD-hist Green/Red/Blue; buy-stop prior high when not Red; cancel **2**; NO FI.",
        "- Watchlist (no paper): ema-rsi@9h, schaff@2d. v6 OOS hard-stop held.",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **rvi-signal-v1** — crossover(RVI, Signal) AND RVI>0; exit crossunder or RVI<0.",
        "2. **chop-breakout-v1** — CHOP<38.2 regime + structure break above prior 20-high; exit 10-low or CHOP>61.8.",
        "3. **elder-impulse-v1** — buy-stop prior high when impulse not Red; cancel 2 bars; exit on Red; no market-on-green; no FI.",
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
            "- No param retune on 6m after freeze. Last Part B seats (B6–B8).",
            "- Hold prior PRs #15–#24 unmerged; this PR is additive fresh-wave-v7 only.",
            "- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only.",
            "- Watchlist (no paper): ema-rsi@9h, schaff@2d.",
            "- v6 twiggs ETH OOS hard-stop — do not revive without Strategy OK.",
            "",
            f"## IDs frozen: {', '.join(STRATEGY_IDS)}",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
