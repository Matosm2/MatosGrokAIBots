"""fresh-wave-v2 OOS stop-ladder on PASS_6m cells (ETH → SOL → BNB).

Strategy stop-ladder (not full 3×3):
1) Run ETH on all three PASS_6m cells (priority order)
2) SOL only on cells that PASS ETH
3) BNB only on cells that PASS SOL

Frozen params/TF from fresh-wave-v2 BTC scoreboard. Gate: 6m Mode-A ≥ 1.2×
that symbol's B&H. Also report full(~2y). No paper, no param spray.
williams-r-mr-v1 + vortex-trend-v1 already hard-stop — not OOS'd.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v2 import RESEARCH_ID
from backtest.path_b.fresh_wave_v2.aroon_trend_v1 import compute_signals as aroon_signals
from backtest.path_b.fresh_wave_v2.cci_mr_v1 import compute_signals as cci_signals
from backtest.path_b.fresh_wave_v2.psar_trend_v1 import compute_signals as psar_signals
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b

OOS_RESEARCH_ID = f"{RESEARCH_ID}-oos-ladder"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# BTC PASS_6m cells — priority order (frozen TF/params); williams/vortex excluded
PASS_6M_CELLS: tuple[tuple[str, str], ...] = (
    ("aroon-trend-v1", "6h"),
    ("psar-trend-v1", "2d"),
    ("cci-mr-v1", "2d"),
)

SYMBOL_LADDER: tuple[str, ...] = ("ETHUSDT", "SOLUSDT", "BNBUSDT")

GATE_MULT = 1.2
FEE = 0.001
SLIP = 0.0005
INITIAL = 10_000.0
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
class LadderCell:
    symbol: str
    strategy_id: str
    tf: str
    gate_6m: str = "FAIL"
    gate_full: str = "FAIL"
    skipped: bool = False
    skip_reason: str = ""
    metrics: list[WindowModeMetrics] = field(default_factory=list)
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
    if strategy_id == "aroon-trend-v1":
        buys, sells = aroon_signals(bars)
        return buys, sells, None
    if strategy_id == "psar-trend-v1":
        buys, sells = psar_signals(bars)
        return buys, sells, None
    if strategy_id == "cci-mr-v1":
        buys, sells = cci_signals(bars)
        return buys, sells, None
    raise ValueError(f"unsupported OOS strategy: {strategy_id}")


def _run_one(
    symbol: str,
    strategy_id: str,
    tf: str,
    bars_by_tf: dict[str, list[Bar]],
) -> LadderCell:
    cell = LadderCell(symbol=symbol, strategy_id=strategy_id, tf=tf)
    try:
        bars = bars_by_tf[tf]
        buys, sells, stops = _signals_for(strategy_id, bars)
        print(f"[oos-ladder] {symbol} {strategy_id} @ {tf} ...", flush=True)
        out: list[WindowModeMetrics] = []
        for label, months in WINDOWS:
            start = _window_start_ms(months)
            buys_w = _mask_buys_before(buys, bars, start)
            for mode_name, buy_pct in SIZING:
                res = run_long_only(
                    symbol,
                    strategy_id,
                    bars,
                    buys_w,
                    sells,
                    stop_prices=stops,
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
                gate = (
                    _gate_label(int(m["trades"]), ret, bh)
                    if mode_name == "gate"
                    else "—"
                )
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
                print(
                    f"  {symbol} {strategy_id}@{tf} {label} [{mode_name}]: "
                    f"n={m['trades']} wr={m['win_rate_pct']:.1f}% "
                    f"ret={ret:+.2f}% bh={bh:+.2f}% ratio={ratio:.3f} [{gate}]",
                    flush=True,
                )
        cell.metrics = out
        g6 = next(m for m in out if m.window == "6m" and m.mode == "gate")
        gf = next(m for m in out if m.window == "full(~2y)" and m.mode == "gate")
        cell.gate_6m = g6.gate
        cell.gate_full = gf.gate
    except Exception as exc:  # noqa: BLE001
        cell.error = repr(exc)
        cell.gate_6m = "ERROR"
        cell.gate_full = "ERROR"
        print(f"  ERROR {exc!r}", flush=True)
    return cell


def run_oos_ladder(*, years: float = 2.5, refresh: bool = False) -> list[LadderCell]:
    """Stop-ladder: ETH all cells → SOL on ETH PASS → BNB on SOL PASS."""
    need_tfs = tuple(dict.fromkeys(tf for _, tf in PASS_6M_CELLS))
    results: list[LadderCell] = []
    passed_prev: set[tuple[str, str]] = set(PASS_6M_CELLS)  # ETH runs all

    for rung, symbol in enumerate(SYMBOL_LADDER):
        if rung == 0:
            candidates = list(PASS_6M_CELLS)
        else:
            candidates = [(s, t) for (s, t) in PASS_6M_CELLS if (s, t) in passed_prev]
            for sid, tf in PASS_6M_CELLS:
                if (sid, tf) not in passed_prev:
                    prev_sym = SYMBOL_LADDER[rung - 1]
                    skip = LadderCell(
                        symbol=symbol,
                        strategy_id=sid,
                        tf=tf,
                        gate_6m="SKIP",
                        gate_full="SKIP",
                        skipped=True,
                        skip_reason=f"prior rung {prev_sym} FAIL/ERROR/SKIP",
                    )
                    results.append(skip)
                    print(
                        f"[oos-ladder] SKIP {symbol} {sid}@{tf} "
                        f"(prior {prev_sym} did not PASS)",
                        flush=True,
                    )

        if not candidates:
            print(f"[oos-ladder] {symbol}: no candidates — ladder stopped", flush=True)
            continue

        data = materialize_symbol(symbol, tfs=need_tfs, years=years, refresh=refresh)
        rung_pass: set[tuple[str, str]] = set()
        for sid, tf in candidates:
            cell = _run_one(symbol, sid, tf, data)
            results.append(cell)
            if cell.gate_6m == "PASS":
                rung_pass.add((sid, tf))
        passed_prev = rung_pass
        print(
            f"[oos-ladder] {symbol} done: "
            f"PASS={[f'{s}@{t}' for s, t in rung_pass] or 'none'}",
            flush=True,
        )
        if not rung_pass and rung < len(SYMBOL_LADDER) - 1:
            for later in SYMBOL_LADDER[rung + 1 :]:
                for sid, tf in PASS_6M_CELLS:
                    results.append(
                        LadderCell(
                            symbol=later,
                            strategy_id=sid,
                            tf=tf,
                            gate_6m="SKIP",
                            gate_full="SKIP",
                            skipped=True,
                            skip_reason=f"ladder stopped: {symbol} had zero PASS",
                        )
                    )
                    print(
                        f"[oos-ladder] SKIP {later} {sid}@{tf} "
                        f"(ladder stopped at {symbol})",
                        flush=True,
                    )
            break

    return results


def write_oos_ladder_report(
    results: list[LadderCell], path: Path | None = None
) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / f"{OOS_RESEARCH_ID}.md")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        f"# {OOS_RESEARCH_ID}",
        "",
        f"_Generated: {now}_",
        "",
        "**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v2 PASS_6m cells. "
        "Not paper/live. No retunes. No Claude.**",
        "",
        "## Scope",
        "",
        f"- Parent: `{RESEARCH_ID}` BTC PASS_6m cells (frozen params / TF / agg)",
        "- Strategy stop-ladder: **ETH all → SOL on ETH PASS → BNB on SOL PASS**",
        f"- Symbols: {' → '.join(SYMBOL_LADDER)}",
        "- Costs: 0.10%/side fee + 5 bps slip",
        f"- Mode-A gate size: **{GATE_SIZE_PCT:.0f}%** equity; Mode-B ops: "
        f"**{OPS_SIZE_PCT}%** (parallel, not scored)",
        f"- Gate: 6m Mode-A return ≥ **{GATE_MULT} × that symbol's B&H** "
        "(same window); also report full(~2y)",
        "- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.",
        "- Params frozen: Aroon(25)+Up≥70; PSAR AF 0.02/0.02/0.2; CCI(20,0.015)",
        "- Hard-stop (not OOS): williams-r-mr-v1, vortex-trend-v1",
        "",
        "## Cells (priority order)",
        "",
    ]
    for i, (sid, tf) in enumerate(PASS_6M_CELLS, 1):
        lines.append(f"{i}. `{sid}` @ `{tf}`")
    lines.append("")

    lines.append("## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)")
    lines.append("")
    lines.append("| Cell | ETHUSDT | SOLUSDT | BNBUSDT |")
    lines.append("|------|---------|---------|---------|")
    by_key = {(r.symbol, r.strategy_id, r.tf): r for r in results}
    for sid, tf in PASS_6M_CELLS:
        cells_txt = []
        for sym in SYMBOL_LADDER:
            r = by_key.get((sym, sid, tf))
            if r is None:
                cells_txt.append("—")
            elif r.skipped:
                cells_txt.append("SKIP")
            elif r.error:
                cells_txt.append("ERROR")
            else:
                g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
                cells_txt.append(f"**{r.gate_6m}**({g.ratio:.2f})")
        lines.append(f"| `{sid}` @ `{tf}` | " + " | ".join(cells_txt) + " |")
    lines.append("")

    for sym in SYMBOL_LADDER:
        lines.append(f"## 6m Mode-A gate — {sym}")
        lines.append("")
        lines.append(
            "| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | "
            "Ops ret | PASS/FAIL |"
        )
        lines.append(
            "|---|----------|----|--------|-------|------------|-----|---------|---------|"
            "-----------|"
        )
        for i, (sid, tf) in enumerate(PASS_6M_CELLS, 1):
            r = by_key.get((sym, sid, tf))
            if r is None:
                lines.append(f"| {i} | {sid} | {tf} | — | — | — | — | — | — | — |")
                continue
            if r.skipped:
                lines.append(
                    f"| {i} | {sid} | {tf} | — | — | — | — | — | — | **SKIP** |"
                )
                continue
            if r.error:
                lines.append(
                    f"| {i} | {sid} | {tf} | — | — | — | — | — | — | **ERROR** |"
                )
                continue
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            o = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
            lines.append(
                f"| {i} | {sid} | {tf} | {g.trades} | {g.win_rate_pct:.2f}% | "
                f"{g.return_pct:+.2f}% | {g.bh_return_pct:+.2f}% | {g.ratio:.3f} | "
                f"{o.return_pct:+.2f}% | **{r.gate_6m}** |"
            )
        lines.append("")

        lines.append(f"## Full window (~2y) Mode-A — {sym} (info)")
        lines.append("")
        lines.append(
            "| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |"
        )
        lines.append(
            "|---|----------|----|--------|----|------------|-----|---------|---------|"
        )
        for i, (sid, tf) in enumerate(PASS_6M_CELLS, 1):
            r = by_key.get((sym, sid, tf))
            if r is None or r.skipped or r.error or not r.metrics:
                status = (
                    "SKIP" if r and r.skipped else ("ERROR" if r and r.error else "—")
                )
                lines.append(
                    f"| {i} | {sid} | {tf} | — | — | — | — | — | {status} |"
                )
                continue
            g = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate"
            )
            o = next(
                m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops"
            )
            lines.append(
                f"| {i} | {sid} | {tf} | {g.trades} | {g.win_rate_pct:.2f}% | "
                f"{g.return_pct:+.2f}% | {g.bh_return_pct:+.2f}% | {g.ratio:.3f} | "
                f"{o.return_pct:+.2f}% |"
            )
        lines.append("")

    lines.append("## Cell detail")
    lines.append("")
    for r in results:
        tag = r.gate_6m
        lines.append(
            f"### `{r.symbol}` · `{r.strategy_id}` @ `{r.tf}` — 6m **{tag}**"
        )
        lines.append("")
        if r.skipped:
            lines.append(f"_Skipped:_ {r.skip_reason}")
            lines.append("")
            continue
        if r.error:
            lines.append(f"ERROR: `{r.error}`")
            lines.append("")
            continue
        lines.append(
            "| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |"
        )
        lines.append(
            "|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|"
        )
        for m in r.metrics:
            lines.append(
                f"| {m.window} | {m.mode} | {m.size_pct:g}% | {m.trades} | "
                f"{m.wins}/{m.losses} | {m.win_rate_pct:.2f}% | {m.return_pct:+.2f}% | "
                f"{m.bh_return_pct:+.2f}% | {m.ratio:.3f} | {m.max_drawdown_pct:.2f}% | "
                f"**{m.gate}** |"
            )
        lines.append("")

    lines.extend(
        [
            "## Caveats",
            "",
            "- Stop-ladder: later symbols only run on cells that PASS the prior rung.",
            "- Frozen params from fresh-wave-v2 — **no retune on alts**.",
            "- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.",
            "- williams-r-mr-v1 + vortex-trend-v1 hard-stopped on BTC — not OOS'd.",
            "- Not wired to paper/alerts/webhook. Hold PR #20 unmerged (push only).",
            "- Same mtf_ohlcv aggregation + fresh_wave_v2 signal code as BTC scoreboard.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
