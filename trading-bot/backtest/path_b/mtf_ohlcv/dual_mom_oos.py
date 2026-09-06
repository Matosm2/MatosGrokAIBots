"""dual-mom-btc-eth-v1 OOS @ 1d + 2d — research-only (Path B / owned-tf-sweep).

Scope: ONLY dual-mom-btc-eth-v1 at 1D and 2D (frozen lookback=20).
Does NOT rerun ema-rsi / sma200 ETH OOS (see owned-tf-sweep-v1-eth-oos).

Gate (both windows): Mode-A ≥ 1.2× **50/50 BTC+ETH B&H** (dual-mom rule).
ETH-only / BTC-only B&H are informational framing only — never the gate.
Costs: 0.1%/side + 5 bps; Mode-A 100%; Mode-B ops 2.5% parallel (not scored).
Not paper/live. No param spray.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.dual_mom_btc_eth_v1 import align_bars, run_dual_mom
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.longwin import (
    WINDOWS,
    SIZING,
    WindowModeMetrics,
    _gate_label,
    _ratio,
    _window_start_ms,
)
from backtest.path_b.mtf_ohlcv.sweep import DM_PARAMS, FEE, GATE_MULT, INITIAL, SLIP
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b

RESEARCH_ID = "owned-tf-sweep-v1-dual-mom-oos"
STRATEGY_ID = "dual-mom-btc-eth-v1"
# Longwin PASS_longwin dual-mom cells only (frozen TF; no spray)
DUAL_MOM_OOS_TFS: tuple[str, ...] = ("1d", "2d")
RESULTS_DIR = Path(__file__).resolve().parent / "results"


@dataclass
class BhFraming:
    """B&H framings on a window — gate uses bh_50_50 only."""

    window: str
    bh_50_50_pct: float = 0.0
    bh_btc_only_pct: float = 0.0
    bh_eth_only_pct: float = 0.0


@dataclass
class DualMomOosCell:
    strategy_id: str = STRATEGY_ID
    tf: str = ""
    gate_full: str = "FAIL"
    gate_6m: str = "FAIL"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    bh_framing: list[BhFraming] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    error: str = ""


def _window_bh_framing(
    btc_bars: list[Bar],
    eth_bars: list[Bar],
    *,
    window_label: str,
    window_start_ms: int,
) -> BhFraming:
    btc, eth = align_bars(btc_bars, eth_bars)
    win_btc = [b for b in btc if b.open_time_ms >= window_start_ms]
    win_eth = [e for e in eth if e.open_time_ms >= window_start_ms]
    # re-align after window filter (same open times)
    win_btc, win_eth = align_bars(win_btc, win_eth)
    if not win_btc or not win_eth:
        return BhFraming(window=window_label)
    r_btc = win_btc[-1].close / win_btc[0].close - 1.0
    r_eth = win_eth[-1].close / win_eth[0].close - 1.0
    bh_50 = ((1 + r_btc) * 0.5 + (1 + r_eth) * 0.5 - 1.0) * 100.0
    return BhFraming(
        window=window_label,
        bh_50_50_pct=bh_50,
        bh_btc_only_pct=r_btc * 100.0,
        bh_eth_only_pct=r_eth * 100.0,
    )


def _eval_dual_mom_cell(
    tf: str,
    btc_bars: list[Bar],
    eth_bars: list[Bar],
) -> DualMomOosCell:
    cell = DualMomOosCell(tf=tf)
    cell.notes.append(
        "Gate = Mode-A vs 50/50 BTC+ETH B&H (dual-mom rule). "
        "ETH-only / BTC-only B&H are framing only — not the gate."
    )
    metrics: list[WindowModeMetrics] = []
    framing: list[BhFraming] = []
    for label, months in WINDOWS:
        start = _window_start_ms(months)
        framing.append(
            _window_bh_framing(
                btc_bars, eth_bars, window_label=label, window_start_ms=start
            )
        )
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
            bh = float(dm.buy_hold_return_pct)  # primary 50/50
            ratio = _ratio(ret, bh)
            gate = _gate_label(int(m["trades"]), ret, bh) if mode_name == "gate" else "—"
            metrics.append(
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
                f"  {STRATEGY_ID}@{tf} {label} [{mode_name} {buy_pct:g}%]: "
                f"n={m['trades']} wr={m['win_rate_pct']:.1f}% "
                f"ret={ret:+.2f}% bh50/50={bh:+.2f}% "
                f"btcBH={dm.btc_only_bh_return_pct:+.2f}% "
                f"ratio={ratio:.3f} [{gate}]",
                flush=True,
            )
    cell.metrics = metrics
    cell.bh_framing = framing
    g_full = next(
        (m for m in metrics if m.window == "full(~2y)" and m.mode == "gate"), None
    )
    g_6m = next((m for m in metrics if m.window == "6m" and m.mode == "gate"), None)
    cell.gate_full = g_full.gate if g_full else "FAIL"
    cell.gate_6m = g_6m.gate if g_6m else "FAIL"
    return cell


def run_dual_mom_oos(
    *, years: float = 2.5, refresh: bool = False
) -> list[DualMomOosCell]:
    tfs = DUAL_MOM_OOS_TFS
    print(
        f"[dual-mom-oos] materialize BTC+ETH for {tfs} (years={years}) ...",
        flush=True,
    )
    btc = materialize_symbol("BTCUSDT", tfs=tfs, years=years, refresh=refresh)
    eth = materialize_symbol("ETHUSDT", tfs=tfs, years=years, refresh=refresh)
    results: list[DualMomOosCell] = []
    for tf in tfs:
        print(f"[dual-mom-oos] {STRATEGY_ID} @ {tf} ...", flush=True)
        try:
            if tf not in btc or tf not in eth:
                cell = DualMomOosCell(tf=tf, error=f"missing bars for {tf}")
                cell.gate_full = "ERROR"
                cell.gate_6m = "ERROR"
            else:
                cell = _eval_dual_mom_cell(tf, btc[tf], eth[tf])
        except Exception as exc:  # noqa: BLE001
            cell = DualMomOosCell(tf=tf, error=repr(exc))
            cell.gate_full = "ERROR"
            cell.gate_6m = "ERROR"
            print(f"  ERROR {exc!r}", flush=True)
        results.append(cell)
    return results


def write_dual_mom_oos_report(
    results: list[DualMomOosCell], path: Path | None = None
) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "owned-tf-sweep-v1-dual-mom-oos.md")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        f"# {RESEARCH_ID}",
        "",
        f"_Generated: {now}_",
        "",
        "**RESEARCH ONLY — dual-mom-btc-eth-v1 @ 1d + 2d. Not paper/live. No param spray.**",
        "",
        "## Scope",
        "",
        f"- Strategy: **`{STRATEGY_ID}`** only (lookback **{DM_PARAMS.lookback}** bars, frozen)",
        f"- TFs: **{', '.join(f'`{t}`' for t in DUAL_MOM_OOS_TFS)}** "
        "(longwin PASS_longwin dual-mom cells; no other TFs)",
        "- Parent harness: `path_b/mtf_ohlcv` + `run_dual_mom` (same as owned-tf-sweep-v1-longwin)",
        f"- Costs: **0.10%/side** fee + **5 bps** slip",
        f"- Mode-A gate size: **{GATE_SIZE_PCT:.0f}%** equity; Mode-B ops: **{OPS_SIZE_PCT}%** "
        "(parallel, not scored)",
        f"- Gate (both windows): Mode-A ≥ **{GATE_MULT}× 50/50 BTC+ETH B&H** "
        "(dual-mom gate rule)",
        "- **Out of scope:** ema-rsi / sma200 / openproxy ETH OOS (PR #16) — not rerun",
        "",
        "## ETH B&H framing (read this)",
        "",
        "- **Primary / gate benchmark = 50/50 BTC+ETH buy-and-hold** on the same window.",
        "  This is the dual-mom standing rule (same as owned-tf-sweep / longwin).",
        "- **NOT gated vs ETH-only B&H.** Unlike single-asset ETH OOS (`owned-tf-sweep-v1-eth-oos`),",
        "  dual-mom rotates between BTC and ETH (or flat), so ETH-only B&H is the wrong yardstick.",
        "- BTC-only and ETH-only B&H are reported below as **informational framing only**",
        "  so readers can compare the 50/50 gate denominator to single-asset paths.",
        "- Strategy already consumes ETHUSDT (paired with BTCUSDT); this is not an",
        "  “apply BTC params to ETH” OOS — it is a focused dual-mom report at the two",
        "  longwin-PASS TFs.",
        "",
        "## PASS/FAIL table (Mode-A vs 50/50)",
        "",
        "| TF | full(~2y) gate | Mode-A % | 50/50 B&H % | ratio | trades | WR % | "
        "6m gate | Mode-A % | 50/50 B&H % | ratio | trades | WR % |",
        "|----|----------------|----------|-------------|-------|--------|------|"
        "---------|----------|-------------|-------|--------|------|",
    ]
    for cell in results:
        if cell.error:
            lines.append(
                f"| {cell.tf} | **ERROR** | — | — | — | — | — | **ERROR** | — | — | — | — | — |"
            )
            continue
        gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
        g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
        lines.append(
            f"| `{cell.tf}` | **{cell.gate_full}** | {gf.return_pct:+.2f} | "
            f"{gf.bh_return_pct:+.2f} | {gf.ratio:.3f} | {gf.trades} | {gf.win_rate_pct:.1f} | "
            f"**{cell.gate_6m}** | {g6.return_pct:+.2f} | {g6.bh_return_pct:+.2f} | "
            f"{g6.ratio:.3f} | {g6.trades} | {g6.win_rate_pct:.1f} |"
        )
    lines.extend(
        [
            "",
            "## B&H framing by window (informational)",
            "",
            "| TF | Window | 50/50 B&H % (gate denom) | BTC-only B&H % | ETH-only B&H % |",
            "|----|--------|--------------------------|----------------|----------------|",
        ]
    )
    for cell in results:
        if cell.error:
            lines.append(f"| {cell.tf} | — | — | — | — |")
            continue
        for fr in cell.bh_framing:
            lines.append(
                f"| `{cell.tf}` | {fr.window} | {fr.bh_50_50_pct:+.2f} | "
                f"{fr.bh_btc_only_pct:+.2f} | {fr.bh_eth_only_pct:+.2f} |"
            )
    lines.extend(["", "## Cell detail (Mode-A + ops)", ""])
    for cell in results:
        lines.append(
            f"### `{STRATEGY_ID}` @ `{cell.tf}` — "
            f"full **{cell.gate_full}** / 6m **{cell.gate_6m}**"
        )
        lines.append("")
        if cell.error:
            lines.append(f"ERROR: `{cell.error}`")
            lines.append("")
            continue
        for note in cell.notes:
            lines.append(f"- _{note}_")
        lines.append("")
        lines.append(
            "| Window | Mode | Size | Trades | W/L | WR | Ret | 50/50 B&H | ratio | MDD | Gate |"
        )
        lines.append(
            "|--------|------|------|--------|-----|----|-----|-----------|-------|-----|------|"
        )
        for m in cell.metrics:
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
            "- Frozen dual-mom lookback=20; same costs / Mode-A 100% as Path B.",
            "- Agg: 1d native cache; 2d = 2×1d UTC bucket (mtf_ohlcv).",
            "- full(~2y) and 6m both gated vs 50/50; neither uses ETH-only B&H.",
            "- Not wired to paper / alerts / webhook. Hold merges.",
            "- Reuses longwin dual-mom logic; numbers should match "
            "`owned-tf-sweep-v1-longwin-scoreboard.md` dual-mom @ 1d/2d rows.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
