"""owned-tf-sweep-v1-longwin: 10×16 BTC cells with LEAD full(~2y) + 6m gates.

LEAD gate: full available history (~2y) Mode-A ≥ 1.2× B&H → PASS/FAIL_longwin.
Also report 6m Mode-A ratio + PASS/FAIL_6m (standing rule; longwin PASS ≠ paper).
dual-mom: vs 50/50 B&H both windows. WR + n trades both windows.
Costs: 0.1%/side + 5 bps; Mode-A 100% + Mode-B ops 2.5% (ops informational).
Same frozen params / agg / HTF map as owned-tf-sweep-v1. No ETH OOS. No param spray.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.bb_squeeze_breakout_v1 import compute_signals as bb_signals
from backtest.path_b.dual_mom_btc_eth_v1 import DualMomParams, run_dual_mom
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.kama_er_trend_v1 import compute_signals as kama_signals
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.openproxy_signals import (
    signals_m1,
    signals_m2,
    signals_m3,
    signals_m4,
)
from backtest.path_b.mtf_ohlcv.sweep import (
    DM_PARAMS,
    EMA_PARAMS,
    FEE,
    GATE_MULT,
    INITIAL,
    SLIP,
    SMA_PARAMS,
    STRATEGY_IDS,
)
from backtest.path_b.mtf_ohlcv.timeframes import (
    M2_M4_HTF,
    SWEEP_TFS,
    htf_for,
    ordered_tfs,
)
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b
from backtest.path_b.sma200_trend_v1 import compute_signals as sma_signals
from backtest.path_b.supertrend_atr_v1 import compute_signals as st_signals
from backtest.signals import apply_position_and_cooldown, compute_indicators

RESEARCH_ID = "owned-tf-sweep-v1-longwin"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

SIZING = (("gate", GATE_SIZE_PCT), ("ops", OPS_SIZE_PCT))
# LEAD = full(~2y); also report 6m. months≈ calendar months via 30.4375d.
WINDOWS: tuple[tuple[str, float], ...] = (("full(~2y)", 24.0), ("6m", 6.0))


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
class LongwinCell:
    strategy_id: str
    tf: str
    gate_longwin: str = "FAIL"  # LEAD
    gate_6m: str = "FAIL"
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


def _ema_signals(bars: list[Bar]) -> tuple[list[bool], list[bool]]:
    closes = [b.close for b in bars]
    frame = compute_indicators(closes, EMA_PARAMS)
    return apply_position_and_cooldown(frame, EMA_PARAMS)


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
    strategy_id: str,
    tf: str,
    btc: dict[str, list[Bar]],
) -> tuple[list[Bar], list[bool], list[bool], list[float | None] | None]:
    bars = btc[tf]
    if strategy_id == "ema-rsi-trend-v1.1":
        buys, sells = _ema_signals(bars)
        return bars, buys, sells, None
    if strategy_id == "openproxy-M1":
        fr = signals_m1(bars, tf)
        return fr.bars, fr.buys, fr.sells, None
    if strategy_id == "openproxy-M3":
        fr = signals_m3(bars, tf)
        return fr.bars, fr.buys, fr.sells, None
    if strategy_id == "openproxy-M2":
        fr = signals_m2(bars, btc[htf_for(tf)], tf)
        return fr.bars, fr.buys, fr.sells, None
    if strategy_id == "openproxy-M4":
        fr = signals_m4(bars, btc[htf_for(tf)], tf)
        return fr.bars, fr.buys, fr.sells, None
    if strategy_id == "bb-squeeze-breakout-v1":
        buys, sells, stops = bb_signals(bars)
        return bars, buys, sells, stops
    if strategy_id == "kama-er-trend-v1":
        buys, sells = kama_signals(bars)
        return bars, buys, sells, None
    if strategy_id == "sma200-trend-v1":
        buys, sells = sma_signals(bars, SMA_PARAMS)
        return bars, buys, sells, None
    if strategy_id == "supertrend-atr-v1":
        buys, sells = st_signals(bars)
        return bars, buys, sells, None
    raise ValueError(f"unknown long-only strategy {strategy_id}")


def _eval_long_only_windows(
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


def _eval_dual_mom_windows(
    tf: str,
    btc_bars: list[Bar],
    eth_bars: list[Bar],
) -> list[WindowModeMetrics]:
    out: list[WindowModeMetrics] = []
    for label, months in WINDOWS:
        start = _window_start_ms(months)
        for mode_name, buy_pct in SIZING:
            dm = run_dual_mom(
                btc_bars,
                eth_bars,
                params=DM_PARAMS,
                initial_equity=INITIAL,
                buy_qty_pct=buy_pct,
                fee_rate=FEE,
                slippage_rate=SLIP,
                window_label=label,
                window_start_ms=start,
            )
            sketch = dm.as_sketch()
            m = summarize_path_b(sketch)
            ret = float(m["return_pct"])
            bh = float(dm.buy_hold_return_pct)  # 50/50 on window
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


def run_cell(
    strategy_id: str,
    tf: str,
    btc: dict[str, list[Bar]],
    eth: dict[str, list[Bar]] | None,
) -> LongwinCell:
    cell = LongwinCell(strategy_id=strategy_id, tf=tf)
    try:
        if strategy_id == "dual-mom-btc-eth-v1":
            if eth is None or tf not in eth:
                cell.error = "ETH bars missing for dual-mom"
                cell.gate_longwin = "ERROR"
                cell.gate_6m = "ERROR"
                return cell
            cell.metrics = _eval_dual_mom_windows(tf, btc[tf], eth[tf])
            cell.notes.append("dual-mom gate vs 50/50 BTC+ETH B&H both windows")
        else:
            bars, buys, sells, stops = _signals_for(strategy_id, tf, btc)
            cell.metrics = _eval_long_only_windows(
                strategy_id, tf, bars, buys, sells, stops
            )

        g_full = next(
            (m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"),
            None,
        )
        g_6m = next(
            (m for m in cell.metrics if m.window == "6m" and m.mode == "gate"),
            None,
        )
        cell.gate_longwin = g_full.gate if g_full else "FAIL"
        cell.gate_6m = g_6m.gate if g_6m else "FAIL"
    except Exception as exc:  # noqa: BLE001
        cell.error = repr(exc)
        cell.gate_longwin = "ERROR"
        cell.gate_6m = "ERROR"
    return cell


def run_longwin_sweep(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
) -> list[LongwinCell]:
    tfs = tfs or ordered_tfs()
    need: list[str] = []
    for tf in ordered_tfs():
        if tf in tfs or tf in M2_M4_HTF.values():
            if tf not in need:
                need.append(tf)
    for tf in tfs:
        h = M2_M4_HTF[tf]
        if h not in need:
            need.append(h)
    if "1w" not in need:
        need.append("1w")
    for tf in tfs:
        if tf not in need:
            need.append(tf)

    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    eth = materialize_symbol("ETHUSDT", tfs=tuple(tfs), years=years, refresh=refresh)

    results: list[LongwinCell] = []
    for tf in tfs:
        for sid in STRATEGY_IDS:
            print(f"[longwin] {sid} @ {tf} ...", flush=True)
            cell = run_cell(sid, tf, btc, eth)
            g_full = next(
                (m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate"),
                None,
            )
            g_6m = next(
                (m for m in cell.metrics if m.window == "6m" and m.mode == "gate"),
                None,
            )
            if cell.error:
                print(f"  -> ERROR {cell.error}", flush=True)
            else:
                assert g_full and g_6m
                print(
                    f"  -> longwin={cell.gate_longwin}({g_full.ratio:.3f}) "
                    f"n={g_full.trades} wr={g_full.win_rate_pct:.1f}% | "
                    f"6m={cell.gate_6m}({g_6m.ratio:.3f}) "
                    f"n={g_6m.trades} wr={g_6m.win_rate_pct:.1f}%",
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


def write_longwin_scoreboard(
    results: list[LongwinCell], path: Path | None = None
) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "owned-tf-sweep-v1-longwin-scoreboard.md")
    by: dict[tuple[str, str], LongwinCell] = {
        (r.strategy_id, r.tf): r for r in results
    }
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — longwin LEAD ≠ paper clearance. No ETH OOS in this PR.**",
        "",
        "## Scoring",
        "",
        f"- **LEAD gate:** full(~2y) Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_longwin`",
        f"- **Also:** 6m Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_6m` (standing rule unchanged)",
        "- dual-mom: vs **50/50** BTC+ETH B&H both windows",
        "- WR + n trades both windows (informational)",
        f"- Costs: 0.10%/side fee + 5 bps slip; Mode-A **{GATE_SIZE_PCT:.0f}%** + Mode-B ops **{OPS_SIZE_PCT}%** (ops not scored)",
        "- Symbol: BTCUSDT (ETH only for dual-mom). Hold #14 BB params. Same HTF/agg as owned-tf-sweep-v1.",
        "",
        "## M2/M4 HTF map (frozen)",
        "",
        "| LTF | HTF |",
        "|-----|-----|",
    ]
    for ltf, htf in M2_M4_HTF.items():
        lines.append(f"| {ltf} | {htf} |")
    lines.append("")

    # LEAD scoreboard
    lines.append("## Scoreboard LEAD full(~2y) PASS/FAIL_longwin (ratio)")
    lines.append("")
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
            g = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            cells.append(_gate_cell(r.gate_longwin, g.ratio))
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")

    # 6m scoreboard
    lines.append("## Scoreboard 6m PASS/FAIL_6m (ratio)")
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
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            cells.append(_gate_cell(r.gate_6m, g.ratio))
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")

    # Combined compact
    lines.append("## Combined (longwin | 6m)")
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
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            cells.append(
                f"{r.gate_longwin[0]}{gf.ratio:.2f}|{r.gate_6m[0]}{g6.ratio:.2f}"
            )
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("_Legend: P=PASS F=FAIL; `Plw|P6m` compact ratios._")
    lines.append("")

    # PASS lists
    lines.append("## PASS_longwin cells (LEAD)")
    lines.append("")
    lw_pass = [r for r in results if r.gate_longwin == "PASS"]
    if not lw_pass:
        lines.append("_none_")
    else:
        for r in lw_pass:
            g = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: longwin ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | 6m={r.gate_6m} ratio={g6.ratio:.3f} n={g6.trades}"
            )
    lines.append("")

    lines.append("## PASS_6m cells (informational; not LEAD)")
    lines.append("")
    six_pass = [r for r in results if r.gate_6m == "PASS"]
    if not six_pass:
        lines.append("_none_")
    else:
        for r in six_pass:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | longwin={r.gate_longwin}"
            )
    lines.append("")

    # Detail table Mode-A both windows
    lines.append("## Cell detail (Mode-A gate; both windows)")
    lines.append("")
    lines.append(
        "| strategy | tf | longwin | lw_ret% | lw_bh% | lw_ratio | lw_wr% | lw_n | "
        "6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | ops_lw% | ops_6m% | error |"
    )
    lines.append(
        "|----------|----|---------|---------|--------|----------|--------|------|"
        "----|---------|--------|----------|--------|------|---------|---------|-------|"
    )
    for r in results:
        if r.error:
            lines.append(
                f"| {r.strategy_id} | {r.tf} | ERROR | — | — | — | — | — | "
                f"ERROR | — | — | — | — | — | — | — | {r.error} |"
            )
            continue
        gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
        g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
        of = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops")
        o6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
        lines.append(
            f"| {r.strategy_id} | {r.tf} | {r.gate_longwin} | {gf.return_pct:.2f} | "
            f"{gf.bh_return_pct:.2f} | {gf.ratio:.3f} | {gf.win_rate_pct:.1f} | {gf.trades} | "
            f"{r.gate_6m} | {g6.return_pct:.2f} | {g6.bh_return_pct:.2f} | {g6.ratio:.3f} | "
            f"{g6.win_rate_pct:.1f} | {g6.trades} | {of.return_pct:.2f} | {o6.return_pct:.2f} |  |"
        )
    lines.append("")
    lines.extend(
        [
            "## Caveats",
            "",
            "- LEAD = full(~2y) Mode-A only. longwin PASS ≠ paper clearance (6m standing rule still applies for paper).",
            "- Mode-B ops 2.5% is parallel / informational only.",
            "- ETH OOS: **not this PR** — only later on longwin PASS cells after CoS.",
            "- No Claude. No Jewel invite. No param spray. Hold #15/#16 unmerged.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
