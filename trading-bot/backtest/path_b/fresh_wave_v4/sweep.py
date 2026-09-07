"""fresh-wave-v4 harness: Fisher×16 + Coppock×2 + ORB×1 (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. No remakes of prior families.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v4 import (
    COARSE_FIRST_TFS,
    COPPOCK_TFS,
    ORB_TF_LABEL,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.fresh_wave_v4.coppock_curve_v1 import (
    compute_signals as coppock_signals,
)
from backtest.path_b.fresh_wave_v4.ehlers_fisher_v1 import (
    compute_signals as fisher_signals,
)
from backtest.path_b.fresh_wave_v4.session_orb_v1 import (
    compute_signals as orb_signals,
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
    skipped: bool = False  # N/A cell


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
    if strategy_id == "ehlers-fisher-v1":
        buys, sells = fisher_signals(bars)
        return buys, sells, None
    if strategy_id == "coppock-curve-v1":
        buys, sells = coppock_signals(bars)
        return buys, sells, None
    if strategy_id == "session-orb-v1":
        buys, sells, stops = orb_signals(bars)
        return buys, sells, stops
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


def _na_cell(strategy_id: str, tf: str, reason: str) -> CellResult:
    return CellResult(
        strategy_id=strategy_id,
        tf=tf,
        gate_6m="N/A",
        gate_full="N/A",
        skipped=True,
        notes=[reason],
    )


def run_cell(strategy_id: str, tf: str, btc: dict[str, list[Bar]]) -> CellResult:
    cell = CellResult(strategy_id=strategy_id, tf=tf)
    try:
        # ORB always consumes 5m bars regardless of label
        if strategy_id == "session-orb-v1":
            bars = btc["5m"]
        else:
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


def run_fresh_wave_v4(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
) -> list[CellResult]:
    tfs = tfs or COARSE_FIRST_TFS
    need = list(dict.fromkeys([*tfs, *SWEEP_TFS, "5m", "1d", "2d"]))
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    results: list[CellResult] = []

    # 1) Ehlers Fisher — full TF spray
    for tf in tfs:
        sid = "ehlers-fisher-v1"
        print(f"[fresh-wave-v4] {sid} @ {tf} ...", flush=True)
        cell = run_cell(sid, tf, btc)
        _print_cell(cell)
        results.append(cell)

    # 2) Coppock — 1d/2d only; N/A elsewhere
    for tf in SWEEP_TFS:
        sid = "coppock-curve-v1"
        if tf not in COPPOCK_TFS:
            cell = _na_cell(sid, tf, "Coppock frozen to 1d/2d only (kick)")
            print(f"[fresh-wave-v4] {sid} @ {tf} -> N/A", flush=True)
            results.append(cell)
            continue
        print(f"[fresh-wave-v4] {sid} @ {tf} ...", flush=True)
        cell = run_cell(sid, tf, btc)
        _print_cell(cell)
        results.append(cell)

    # 3) Session ORB — one primary BTC cell from 5m
    sid = "session-orb-v1"
    print(f"[fresh-wave-v4] {sid} @ {ORB_TF_LABEL} (5m UTC midnight OR) ...", flush=True)
    cell = run_cell(sid, ORB_TF_LABEL, btc)
    _print_cell(cell)
    results.append(cell)

    return results


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
        f"  -> 6m={cell.gate_6m}({g6.ratio:.3f}) n={g6.trades} | "
        f"full={cell.gate_full}({gf.ratio:.3f}) n={gf.trades}",
        flush=True,
    )


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
    path = path or (RESULTS_DIR / "fresh-wave-v4-scoreboard.md")
    by: dict[tuple[str, str], CellResult] = {(r.strategy_id, r.tf): r for r in results}
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes of prior families.**",
        "",
        "## Scoring",
        "",
        f"- **LEAD gate:** 6m Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_6m`",
        f"- **Also:** full(~2y) Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_full` (informational)",
        f"- Costs: 0.10%/side fee + 5 bps slip; Mode-A **{GATE_SIZE_PCT:.0f}%** + Mode-B ops **{OPS_SIZE_PCT}%** (ops not scored)",
        "- Symbol: BTCUSDT only. Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot. Single-TF (no HTF filter).",
        "- Params frozen (no spray): Fisher len10 Fish×Trigger prior Fish<0; Coppock ROC14+11/WMA10 (1d/2d only); UTC midnight OR 30m, skip OR>2×ATR14, vol filter OFF, one trade/session.",
        "- Cell scope: Fisher = 16 TF; Coppock = 1d+2d (N/A elsewhere); ORB = one primary `orb-utc` cell from 5m.",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **ehlers-fisher-v1** — Ehlers Fisher len **10** on HL2. Enter crossover(Fish, Trigger) AND prior Fish < 0; exit crossunder(Fish, Trigger).",
        "2. **coppock-curve-v1** — Coppock = WMA(**10**, ROC(**14**)+ROC(**11**)). Enter trough-turn while <0 OR crossover(0) after ≥10 bars below 0; exit turn-down while >0 OR crossunder(0). **1d/2d only.**",
        "3. **session-orb-v1** — UTC midnight OR first **30m** from **5m** bars. Enter close > OR high after window; exit target 1× OR height, opposite OR edge (stop), or 23:59 UTC flat. Skip if OR height > **2×ATR(14)** on OR close bar. One trade/session. Vol filter OFF.",
        "",
        "## Scoreboard LEAD 6m PASS/FAIL_6m (ratio)",
        "",
    ]
    header = "| strategy \\ tf | " + " | ".join(SWEEP_TFS) + " |"
    sep = "|" + "|".join(["---"] * (len(SWEEP_TFS) + 1)) + "|"
    lines.append(header)
    lines.append(sep)

    # Fisher row across 16 TFs
    cells = []
    for tf in SWEEP_TFS:
        r = by.get(("ehlers-fisher-v1", tf))
        if r is None or r.error:
            cells.append("ERR" if r and r.error else "—")
            continue
        if r.skipped:
            cells.append("N/A")
            continue
        g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
        cells.append(_gate_cell(r.gate_6m, g.ratio))
    lines.append("| ehlers-fisher-v1 | " + " | ".join(cells) + " |")

    # Coppock row
    cells = []
    for tf in SWEEP_TFS:
        r = by.get(("coppock-curve-v1", tf))
        if r is None:
            cells.append("—")
            continue
        if r.skipped or r.gate_6m == "N/A":
            cells.append("N/A")
            continue
        if r.error:
            cells.append("ERR")
            continue
        g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
        cells.append(_gate_cell(r.gate_6m, g.ratio))
    lines.append("| coppock-curve-v1 | " + " | ".join(cells) + " |")

    # ORB: N/A across spray (primary cell below)
    lines.append(
        "| session-orb-v1 | "
        + " | ".join(["N/A"] * len(SWEEP_TFS))
        + " |"
    )
    lines.append("")
    lines.append(
        f"_`session-orb-v1` primary cell is `{ORB_TF_LABEL}` (5m→UTC midnight OR), "
        "not a 16-TF spray — see ORB section below._"
    )
    lines.append("")

    lines.append("## Scoreboard full(~2y) PASS/FAIL_full (ratio)")
    lines.append("")
    lines.append(header)
    lines.append(sep)
    cells = []
    for tf in SWEEP_TFS:
        r = by.get(("ehlers-fisher-v1", tf))
        if r is None or r.error:
            cells.append("ERR" if r and r.error else "—")
            continue
        g = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
        cells.append(_gate_cell(r.gate_full, g.ratio))
    lines.append("| ehlers-fisher-v1 | " + " | ".join(cells) + " |")
    cells = []
    for tf in SWEEP_TFS:
        r = by.get(("coppock-curve-v1", tf))
        if r is None or r.skipped or r.gate_full == "N/A":
            cells.append("N/A")
            continue
        if r.error:
            cells.append("ERR")
            continue
        g = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
        cells.append(_gate_cell(r.gate_full, g.ratio))
    lines.append("| coppock-curve-v1 | " + " | ".join(cells) + " |")
    lines.append(
        "| session-orb-v1 | "
        + " | ".join(["N/A"] * len(SWEEP_TFS))
        + " |"
    )
    lines.append("")

    lines.append("## Combined (6m LEAD | full)")
    lines.append("")
    lines.append(header)
    lines.append(sep)
    for sid in ("ehlers-fisher-v1", "coppock-curve-v1"):
        cells = []
        for tf in SWEEP_TFS:
            r = by.get((sid, tf))
            if r is None:
                cells.append("—")
                continue
            if r.skipped or r.gate_6m == "N/A":
                cells.append("N/A")
                continue
            if r.error:
                cells.append("ERR")
                continue
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
            cells.append(
                f"{r.gate_6m[0]}{g6.ratio:.2f}|{r.gate_full[0]}{gf.ratio:.2f}"
            )
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append(
        "| session-orb-v1 | "
        + " | ".join(["N/A"] * len(SWEEP_TFS))
        + " |"
    )
    lines.append("")
    lines.append("_Legend: P=PASS F=FAIL; `P6m|Pfull` compact ratios._")
    lines.append("")

    # ORB primary
    lines.append("## session-orb-v1 primary cell (BTCUSDT)")
    lines.append("")
    orb = by.get(("session-orb-v1", ORB_TF_LABEL))
    if orb is None:
        lines.append("_missing_")
    elif orb.error:
        lines.append(f"ERROR: {orb.error}")
    else:
        g6 = next(m for m in orb.metrics if m.window == "6m" and m.mode == "gate")
        gf = next(
            m for m in orb.metrics if m.window == "full(~2y)" and m.mode == "gate"
        )
        o6 = next(m for m in orb.metrics if m.window == "6m" and m.mode == "ops")
        of = next(
            m for m in orb.metrics if m.window == "full(~2y)" and m.mode == "ops"
        )
        lines.append(
            f"- `{orb.strategy_id}` @ `{orb.tf}`: **6m={orb.gate_6m}** "
            f"ret={g6.return_pct:.2f}% bh={g6.bh_return_pct:.2f}% "
            f"ratio={g6.ratio:.3f} wr={g6.win_rate_pct:.1f}% n={g6.trades} | "
            f"full={orb.gate_full} ratio={gf.ratio:.3f} n={gf.trades} | "
            f"ops_6m={o6.return_pct:.2f}% ops_full={of.return_pct:.2f}%"
        )
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
        if r.skipped:
            lines.append(
                f"| {r.strategy_id} | {r.tf} | N/A | — | — | — | — | — | "
                f"N/A | — | — | — | — | — | — | — | {'; '.join(r.notes)} |"
            )
            continue
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
            "- No param spray / SMA200/RSI/BB/ST grafts. Excluded: owned, v1, v2, v3 IDs, Jewel/Hub, Black Skull, research rejects (Stoch, Keltner, MACD-hist div, Inverse Fisher-RSI, HA hybrids, ATR-squeeze).",
            "- No OOS (ETH/SOL/BNB) in this PR — parent runs after BTC PASS_6m.",
            "- Hold prior PRs #15–#21 unmerged; this PR is additive fresh-wave-v4 only.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
