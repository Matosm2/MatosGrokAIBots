"""fresh-wave-v1 harness: 5 strategies × 16 TFs = 80 cells (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. No prior failed families.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave import RESEARCH_ID, STRATEGY_IDS
from backtest.path_b.fresh_wave.connors_rsi_mr_v1 import compute_signals as crsi_signals
from backtest.path_b.fresh_wave.ha_streak_trend_v1 import compute_signals as ha_signals
from backtest.path_b.fresh_wave.ichimoku_cloud_trend_v1 import (
    compute_signals as ichi_signals,
)
from backtest.path_b.fresh_wave.nr7_breakout_v1 import compute_signals as nr7_signals
from backtest.path_b.fresh_wave.obv_ema_trend_v1 import compute_signals as obv_signals
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS, ordered_tfs
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b

GATE_MULT = 1.2
FEE = 0.001
SLIP = 0.0005
INITIAL = 10_000.0
RESULTS_DIR = Path(__file__).resolve().parent / "results"

SIZING = (("gate", GATE_SIZE_PCT), ("ops", OPS_SIZE_PCT))
# LEAD = 6m; also report full(~2y)
WINDOWS: tuple[tuple[str, float], ...] = (("6m", 6.0), ("full(~2y)", 24.0))


@dataclass
class WindowModeMetrics:
    window: str
    mode: str  # gate | ops
    size_pct: float
    return_pct: float = 0.0
    bh_return_pct: float = 0.0
    ratio: float = 0.0
    win_rate_pct: float = 0.0
    trades: int = 0
    wins: int = 0
    losses: int = 0
    max_drawdown_pct: float = 0.0
    gate: str = "—"  # PASS | FAIL | — (ops)


@dataclass
class CellResult:
    strategy_id: str
    tf: str
    gate_6m: str = "FAIL"  # LEAD
    gate_full: str = "FAIL"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    error: str = ""


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


def _signals_for(
    strategy_id: str, bars: list[Bar]
) -> tuple[list[bool], list[bool], list[float | None] | None]:
    if strategy_id == "connors-rsi-mr-v1":
        buys, sells = crsi_signals(bars)
        return buys, sells, None
    if strategy_id == "nr7-breakout-v1":
        buys, sells, stops = nr7_signals(bars)
        return buys, sells, stops
    if strategy_id == "ichimoku-cloud-trend-v1":
        buys, sells = ichi_signals(bars)
        return buys, sells, None
    if strategy_id == "ha-streak-trend-v1":
        buys, sells = ha_signals(bars)
        return buys, sells, None
    if strategy_id == "obv-ema-trend-v1":
        buys, sells = obv_signals(bars)
        return buys, sells, None
    raise ValueError(f"unknown strategy {strategy_id}")


def _eval_windows(
    strategy_id: str,
    tf: str,
    bars: list[Bar],
    buys_full: list[bool],
    sells_full: list[bool],
    stop_prices: list[float | None] | None,
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


def run_cell(strategy_id: str, tf: str, btc: dict[str, list[Bar]]) -> CellResult:
    cell = CellResult(strategy_id=strategy_id, tf=tf)
    try:
        bars = btc[tf]
        buys, sells, stops = _signals_for(strategy_id, bars)
        cell.metrics = _eval_windows(strategy_id, tf, bars, buys, sells, stops)
        g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
        gf = next(
            m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"
        )
        cell.gate_6m = g6.gate
        cell.gate_full = gf.gate
    except Exception as exc:  # noqa: BLE001
        cell.error = repr(exc)
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"
    return cell


def run_fresh_wave(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
) -> list[CellResult]:
    tfs = tfs or ordered_tfs()
    need = list(dict.fromkeys([*tfs, *SWEEP_TFS]))
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    results: list[CellResult] = []
    for tf in tfs:
        for sid in STRATEGY_IDS:
            print(f"[fresh-wave] {sid} @ {tf} ...", flush=True)
            cell = run_cell(sid, tf, btc)
            if cell.error:
                print(f"  -> ERROR {cell.error}", flush=True)
            else:
                g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
                gf = next(
                    m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"
                )
                print(
                    f"  -> 6m={cell.gate_6m}({g6.ratio:.3f}) n={g6.trades} | "
                    f"full={cell.gate_full}({gf.ratio:.3f}) n={gf.trades}",
                    flush=True,
                )
            results.append(cell)
    return results


def _gate_cell(gate: str, ratio: float) -> str:
    if gate == "PASS":
        return f"PASS({ratio:.2f})"
    if gate == "FAIL":
        return f"FAIL({ratio:.2f})"
    if gate == "ERROR":
        return "ERR"
    return "—"


def write_scoreboard(results: list[CellResult], path: Path | None = None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "fresh-wave-v1-scoreboard.md")
    by: dict[tuple[str, str], CellResult] = {(r.strategy_id, r.tf): r for r in results}
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude. No Jewel. No prior failed families.**",
        "",
        "## Scoring",
        "",
        f"- **LEAD gate:** 6m Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_6m`",
        f"- **Also:** full(~2y) Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_full` (informational)",
        f"- Costs: 0.10%/side fee + 5 bps slip; Mode-A **{GATE_SIZE_PCT:.0f}%** + Mode-B ops **{OPS_SIZE_PCT}%** (ops not scored)",
        "- Symbol: BTCUSDT only. Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.",
        "- Params frozen (no spray): CRSI(3,2,100); NR7/ATR14×2/10-bar; Ichimoku 9/26/52; HA streak=3; OBV EMA20 + close EMA50.",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **connors-rsi-mr-v1** — Classic **CRSI(3,2,100)** = mean of RSI(close,3), RSI(streak,2), PercentRank(ROC1,100). Enter CRSI<10; exit CRSI>90 OR hold≥5 bars.",
        "2. **nr7-breakout-v1** — NR7 = narrowest H-L of last 7 bars. Enter when close > that NR7 high. Exit: ±2×ATR(14) from entry (stop via engine; target via signal) OR after 10 bars (bar-close; reference mid=(NR7.H+NR7.L)/2).",
        "3. **ichimoku-cloud-trend-v1** — Classic **9/26/52**, displacement 26 (cloud at i from i-26; no lookahead). Enter TK cross up AND close > cloud top; exit close < cloud bottom OR TK cross down.",
        "4. **ha-streak-trend-v1** — Enter after 3 consecutive HA bull bars (HA close>HA open); exit on first HA bear bar.",
        "5. **obv-ema-trend-v1** — Enter OBV cross above EMA20(OBV) AND close > EMA50; exit OBV cross below EMA20(OBV).",
        "",
        "## Scoreboard LEAD 6m PASS/FAIL_6m (ratio)",
        "",
    ]
    header = "| strategy \\ tf | " + " | ".join(SWEEP_TFS) + " |"
    sep = "|" + "|".join(["---"] * (len(SWEEP_TFS) + 1)) + "|"
    lines.append(header)
    lines.append(sep)
    for sid in STRATEGY_IDS:
        cells = []
        for tf in SWEEP_TFS:
            r = by.get((sid, tf))
            if r is None or r.error:
                cells.append("ERR" if r and r.error else "—")
                continue
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            cells.append(_gate_cell(r.gate_6m, g.ratio))
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")

    lines.append("## Scoreboard full(~2y) PASS/FAIL_full (ratio)")
    lines.append("")
    lines.append(header)
    lines.append(sep)
    for sid in STRATEGY_IDS:
        cells = []
        for tf in SWEEP_TFS:
            r = by.get((sid, tf))
            if r is None or r.error:
                cells.append("ERR" if r and r.error else "—")
                continue
            g = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
            cells.append(_gate_cell(r.gate_full, g.ratio))
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")

    lines.append("## Combined (6m LEAD | full)")
    lines.append("")
    lines.append(header)
    lines.append(sep)
    for sid in STRATEGY_IDS:
        cells = []
        for tf in SWEEP_TFS:
            r = by.get((sid, tf))
            if r is None or r.error:
                cells.append("ERR" if r and r.error else "—")
                continue
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
            cells.append(f"{r.gate_6m[0]}{g6.ratio:.2f}|{r.gate_full[0]}{gf.ratio:.2f}")
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("_Legend: P=PASS F=FAIL; `P6m|Pfull` compact ratios._")
    lines.append("")

    lines.append("## PASS_6m cells (LEAD)")
    lines.append("")
    six_pass = [r for r in results if r.gate_6m == "PASS"]
    if not six_pass:
        lines.append("_none_")
    else:
        for r in six_pass:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
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
            g = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: full ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | 6m={r.gate_6m}"
            )
    lines.append("")

    lines.append("## Cell detail (Mode-A gate; both windows)")
    lines.append("")
    lines.append(
        "| strategy | tf | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | "
        "full | full_ret% | full_bh% | full_ratio | full_wr% | full_n | "
        "ops_6m% | ops_full% | error |"
    )
    lines.append(
        "|----------|----|----|---------|--------|----------|--------|------|"
        "------|-----------|----------|------------|----------|--------|"
        "---------|-----------|-------|"
    )
    for r in results:
        if r.error:
            lines.append(
                f"| {r.strategy_id} | {r.tf} | ERROR | — | — | — | — | — | "
                f"ERROR | — | — | — | — | — | — | — | {r.error} |"
            )
            continue
        g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
        gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
        o6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
        of = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops")
        lines.append(
            f"| {r.strategy_id} | {r.tf} | {r.gate_6m} | {g6.return_pct:.2f} | "
            f"{g6.bh_return_pct:.2f} | {g6.ratio:.3f} | {g6.win_rate_pct:.1f} | {g6.trades} | "
            f"{r.gate_full} | {gf.return_pct:.2f} | {gf.bh_return_pct:.2f} | {gf.ratio:.3f} | "
            f"{gf.win_rate_pct:.1f} | {gf.trades} | {o6.return_pct:.2f} | {of.return_pct:.2f} |  |"
        )
    lines.append("")
    lines.extend(
        [
            "## Caveats",
            "",
            "- LEAD = 6m Mode-A only. full(~2y) is reported for context, not paper clearance.",
            "- Mode-B ops 2.5% is parallel / informational only.",
            "- No param spray. No ema-rsi / openproxy / bb-squeeze / kama / dual-mom / sma200 / supertrend in this wave.",
            "- Hold PRs #15–#17 unmerged; this PR is additive fresh-wave-v1 only.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
