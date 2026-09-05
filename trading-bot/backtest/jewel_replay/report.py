"""Markdown metrics for jewel-strength-hold-v1 Path B replays (dual sizing + windows)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from backtest.jewel_replay.engine import ReplayResult
from backtest.metrics import max_drawdown_pct

# Gate uses Mode A (100% equity) return vs B&H; Mode B is ops sizing only.
MODE_A_PCT = 100.0
MODE_B_PCT = 2.5
GATE_WR_MIN = 60.0


@dataclass
class DualModeRow:
    """One symbol/variant/window with Mode A (gate) + Mode B (ops)."""

    symbol: str
    variant: str
    window_label: str
    mode_a: ReplayResult
    mode_b: ReplayResult
    source_csv: str = ""

    def summarize(self) -> dict[str, float | int | str | bool]:
        a = summarize(self.mode_a)
        b = summarize(self.mode_b)
        n = int(a["trades"])
        wr = float(a["win_rate_pct"])
        ret_a = float(a["return_pct"])
        bh = float(a["buy_hold_return_pct"])
        gate_pass = n > 0 and wr >= GATE_WR_MIN and ret_a > bh
        return {
            "symbol": self.symbol,
            "variant": self.variant,
            "window": self.window_label,
            "trades": n,
            "win_rate_pct": wr,
            "mode_a_return_pct": ret_a,
            "mode_b_return_pct": float(b["return_pct"]),
            "buy_hold_return_pct": bh,
            "mode_a_max_dd_pct": float(a["max_drawdown_pct"]),
            "mode_b_max_dd_pct": float(b["max_drawdown_pct"]),
            "gate_pass": gate_pass,
            "gate_label": "PASS" if gate_pass else "FAIL",
        }


def summarize(result: ReplayResult) -> dict[str, float | int | str | bool]:
    trades = result.trades
    n = len(trades)
    wins = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl <= 0]
    total_pnl = sum(t.pnl for t in trades)
    ret = (
        (result.final_equity / result.initial_equity - 1.0) * 100.0
        if result.initial_equity
        else 0.0
    )
    wr = (len(wins) / n * 100.0) if n else 0.0
    gate_wr_ok = n > 0 and wr >= GATE_WR_MIN
    # Legacy single-run gate (Mode A intended): WR + beat B&H
    gate_bh_ok = ret > result.buy_hold_return_pct
    return {
        "variant": result.variant,
        "trades": n,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": wr,
        "return_pct": ret,
        "buy_hold_return_pct": result.buy_hold_return_pct,
        "vs_buy_hold_pp": ret - result.buy_hold_return_pct,
        "max_drawdown_pct": max_drawdown_pct(result.equity_curve),
        "total_pnl": total_pnl,
        "buy_qty_pct": result.buy_qty_pct,
        "gate_wr_ok": gate_wr_ok,
        "gate_bh_ok": gate_bh_ok,
        "gate_pass": gate_wr_ok and gate_bh_ok,
    }


def _fmt_block(m: dict[str, float | int | str | bool]) -> list[str]:
    return [
        f"| Trades | {m['trades']} |",
        f"| Wins / Losses | {m['wins']} / {m['losses']} |",
        f"| Win rate | {float(m['win_rate_pct']):.2f}% |",
        f"| Strategy return | {float(m['return_pct']):.2f}% |",
        f"| Buy & hold return | {float(m['buy_hold_return_pct']):.2f}% |",
        f"| vs buy & hold (pp) | {float(m['vs_buy_hold_pp']):+.2f} |",
        f"| Max drawdown | {float(m['max_drawdown_pct']):.2f}% |",
        f"| Total PnL (USDT) | {float(m['total_pnl']):.2f} |",
        f"| Size (buy_qty_pct) | {float(m['buy_qty_pct']):g}% |",
        f"| Gate WR ≥{GATE_WR_MIN:g}% | {'PASS' if m['gate_wr_ok'] else 'FAIL'} |",
        f"| Gate beat B&H | {'PASS' if m['gate_bh_ok'] else 'FAIL'} |",
    ]


def write_replay_markdown(
    *,
    results: list[ReplayResult],
    path: Path,
    source_csv: str,
) -> Path:
    """Legacy single-sizing report (kept for fixture / one-off Mode B dumps)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# Offline replay: jewel-strength-hold-v1 (RESEARCH)",
        "",
        f"_Generated: {now}_",
        "",
        "## Framing",
        "",
        "- **strategy_id:** `jewel-strength-hold-v1`",
        "- Path B CSV replay — **not** paper/live webhook-enabled",
        "- Spot long-only, bar close, pyramiding 0; Slow/High from CSV only",
        "- Costs: 0.10%/side + ≥5 bps slip",
        f"- Gate before paper: **≥{GATE_WR_MIN:g}% WR** and **Mode-A return > buy&hold** "
        f"(Mode A = {MODE_A_PCT:g}% equity; Mode B = {MODE_B_PCT:g}% ops)",
        "",
        "## Data",
        "",
        f"- Source CSV: `{source_csv}`",
    ]
    if results:
        r0 = results[0]
        if r0.timestamps_ms:
            t0 = datetime.fromtimestamp(r0.timestamps_ms[0] / 1000, tz=timezone.utc)
            t1 = datetime.fromtimestamp(r0.timestamps_ms[-1] / 1000, tz=timezone.utc)
            lines.append(
                f"- Bars: {len(r0.timestamps_ms)}  "
                f"({t0:%Y-%m-%d} → {t1:%Y-%m-%d} UTC)"
            )
        lines.append(f"- Symbol label: {r0.symbol}")
        lines.append(
            f"- Fee {r0.fee_rate * 100:.2f}%/side; "
            f"slip {r0.slippage_rate * 100:.3f}%; buy {r0.buy_qty_pct:g}%"
        )
    lines.append("")

    for r in results:
        m = summarize(r)
        lines.append(f"## {r.symbol} — {r.variant}")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.extend(_fmt_block(m))
        lines.append("")

    lines.append("## Caveats")
    lines.append("")
    if results:
        for n in results[0].notes:
            lines.append(f"- {n}")
    lines.append(
        "- Synthetic or exported Jewel columns required; CI uses fixture only."
    )
    lines.append(
        "- **Repaint / non-realtime risk:** Path B assumes bar-close Slow/High "
        "values as exported. If Jewel plots repaint intrabar or on historical "
        "recalc, offline WR/return can look better than live bar-close fills."
    )
    lines.append(
        "- **Invite-only Jewel:** Slow/High come from an invite-only indicator. "
        "Replay fidelity depends on the same plots Nuno exports from his chart; "
        "this harness cannot reconstruct Jewel without those series."
    )
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_dual_gate_markdown(
    *,
    rows: list[DualModeRow],
    path: Path,
    sources: list[str],
    waiting_for_real_csvs: bool = False,
) -> Path:
    """
    Dual-sizing gate report: full and/or 6m tables.

    Columns: WR | Mode-A return | Mode-B (ops) return | B&H | PASS/FAIL
    PASS only if n>0 AND WR≥60% AND Mode-A return > B&H.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# Path B dual-sizing gate: jewel-strength-hold-v1",
        "",
        f"_Generated: {now}_",
        "",
        "## Framing",
        "",
        "- **strategy_id:** `jewel-strength-hold-v1`",
        "- Path B CSV replay — **not** paper/live webhook-enabled",
        f"- **Mode A (gate):** `buy_qty_pct={MODE_A_PCT:g}` — 100% equity when in; "
        "compared to buy & hold",
        f"- **Mode B (ops):** `buy_qty_pct={MODE_B_PCT:g}` — ops column only",
        "- Costs: 0.10%/side + 5 bps slip; V-zone and V-wide",
        f"- **PASS** iff `n>0` AND `WR ≥ {GATE_WR_MIN:g}%` AND "
        "`Mode-A return > B&H` (same window)",
        "",
        "## Data",
        "",
    ]
    for s in sources:
        lines.append(f"- `{s}`")
    if waiting_for_real_csvs:
        lines.append("")
        lines.append(
            "> **Waiting for real CSVs:** Expected on CM700 at "
            "`C:\\temp\\GrokBOTandclaudToHATrading\\outbox\\jewel-btc-daily.csv` and "
            "`jewel-eth-daily.csv` (also check `/workspace/uploads/jewel*.csv`). "
            "This report may be fixture-only scaffolding until those land."
        )
    lines.append("")

    # Group by window label for tables
    by_window: dict[str, list[DualModeRow]] = {}
    for row in rows:
        by_window.setdefault(row.window_label, []).append(row)

    for wlabel, wrows in by_window.items():
        title = "Full window" if wlabel == "full" else "Last 6 months"
        lines.append(f"## Gate table — {title} (`{wlabel}`)")
        lines.append("")
        lines.append(
            "| Symbol | Variant | n | WR | Mode-A return | Mode-B (ops) | B&H | PASS/FAIL |"
        )
        lines.append(
            "|--------|---------|---|----|---------------|--------------|-----|-----------|"
        )
        for row in wrows:
            m = row.summarize()
            lines.append(
                f"| {m['symbol']} | {m['variant']} | {m['trades']} | "
                f"{float(m['win_rate_pct']):.1f}% | "
                f"{float(m['mode_a_return_pct']):+.2f}% | "
                f"{float(m['mode_b_return_pct']):+.2f}% | "
                f"{float(m['buy_hold_return_pct']):+.2f}% | "
                f"**{m['gate_label']}** |"
            )
        lines.append("")

    # Detail blocks
    lines.append("## Detail")
    lines.append("")
    for row in rows:
        m = row.summarize()
        a = summarize(row.mode_a)
        lines.append(
            f"### {row.symbol} — {row.variant} — {row.window_label}"
        )
        lines.append("")
        if row.mode_a.timestamps_ms:
            t0 = datetime.fromtimestamp(
                row.mode_a.timestamps_ms[0] / 1000, tz=timezone.utc
            )
            t1 = datetime.fromtimestamp(
                row.mode_a.timestamps_ms[-1] / 1000, tz=timezone.utc
            )
            lines.append(
                f"- Bars: {len(row.mode_a.timestamps_ms)} "
                f"({t0:%Y-%m-%d} → {t1:%Y-%m-%d} UTC)"
            )
        if row.source_csv:
            lines.append(f"- Source: `{row.source_csv}`")
        lines.append(
            f"- Gate: **{m['gate_label']}** "
            f"(n={m['trades']}, WR={float(m['win_rate_pct']):.2f}%, "
            f"Mode-A {float(m['mode_a_return_pct']):+.2f}% vs "
            f"B&H {float(m['buy_hold_return_pct']):+.2f}%)"
        )
        lines.append(
            f"- Mode-A max DD {float(m['mode_a_max_dd_pct']):.2f}%; "
            f"Mode-B max DD {float(m['mode_b_max_dd_pct']):.2f}%"
        )
        lines.append(
            f"- Wins/Losses (Mode A): {a['wins']} / {a['losses']}"
        )
        lines.append("")

    lines.append("## Caveats")
    lines.append("")
    lines.append(
        "- strategy_id jewel-strength-hold-v1 — RESEARCH Path B replay."
    )
    lines.append(
        "- Bar-close fills; Jewel Slow/High from CSV (no RSI/Stoch proxy)."
    )
    lines.append(
        f"- Mode A = {MODE_A_PCT:g}% equity (gate vs B&H); "
        f"Mode B = {MODE_B_PCT:g}% equity (ops)."
    )
    lines.append(
        "- V-wide ATR stop uses ATR frozen at entry; threshold vs entry bar close."
    )
    lines.append("- Not wired to paper/live webhooks.")
    lines.append(
        "- **Repaint / non-realtime risk:** Path B assumes bar-close Slow/High "
        "as exported."
    )
    lines.append(
        "- **Invite-only Jewel:** Slow/High from invite-only indicator; harness "
        "cannot reconstruct without exported series."
    )
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
