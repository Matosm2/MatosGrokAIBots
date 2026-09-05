"""Markdown metrics for jewel-strength-hold-v1 Path B replays (dual sizing + windows)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from backtest.jewel_replay.engine import ReplayResult
from backtest.metrics import max_drawdown_pct

# Gate uses Mode A (100% equity) return vs B&H; Mode B is ops sizing only.
# WR / n are informational only (not pass/fail legs).
MODE_A_PCT = 100.0
MODE_B_PCT = 2.5
GATE_BH_MULTIPLIER = 1.2
# Legacy informational threshold (not used for PASS/FAIL).
GATE_WR_MIN = 60.0


def evaluate_gate(
    mode_a_return_pct: float,
    buy_hold_return_pct: float,
) -> tuple[bool, str]:
    """
    Gate: Mode-A MTM return ≥ GATE_BH_MULTIPLIER × B&H (same window).

    When B&H > 0:
      PASS iff mode_a >= 1.2 * buy_hold; ratio = mode_a / buy_hold (display).
    When B&H ≤ 0:
      Ratio is undefined for a "≥ 1.2×" multiple (non-positive denominator).
      Policy: PASS only if Mode-A > 0 (absolute positive while B&H flat/down);
      ratio display = "n/a".
    """
    if buy_hold_return_pct <= 0:
        return mode_a_return_pct > 0, "n/a"
    ratio = mode_a_return_pct / buy_hold_return_pct
    passed = mode_a_return_pct >= GATE_BH_MULTIPLIER * buy_hold_return_pct
    return passed, f"{ratio:.3f}"


def _open_long_from_trades(result: ReplayResult) -> bool:
    """Detect open long: more entries than exits in chronological process order."""
    # Trades list only contains closed trades. Infer open if equity path suggests
    # inventory: compare final MTM to cash-only after last exit using last close.
    # Practical approach: scan whether last signal left a position — engine does not
    # expose qty. Use: if any trade entry_bar > all exit_bars... trades are closed
    # only, so check whether final_equity implies leftover coins:
    # After all closed trades, cash = initial + sum(pnl). If final_equity != that
    # cash (within float eps), open MTM leg remains.
    closed_pnl = sum(t.pnl for t in result.trades)
    cash_if_flat = result.initial_equity + closed_pnl
    return abs(result.final_equity - cash_if_flat) > 1e-6


@dataclass
class DualModeRow:
    """One symbol/variant/window with Mode A (gate) + Mode B (ops)."""

    symbol: str
    variant: str
    window_label: str
    mode_a: ReplayResult
    mode_b: ReplayResult
    source_csv: str = ""
    prep_notes: list[str] | None = None

    def summarize(self) -> dict[str, float | int | str | bool]:
        a = summarize(self.mode_a)
        b = summarize(self.mode_b)
        n = int(a["trades"])
        wr = float(a["win_rate_pct"])
        ret_a = float(a["return_pct"])  # MTM / equity curve return
        bh = float(a["buy_hold_return_pct"])
        gate_pass, ratio_display = evaluate_gate(ret_a, bh)
        wr_display = "n/a" if n == 0 else f"{wr:.1f}%"
        return {
            "symbol": self.symbol,
            "variant": self.variant,
            "window": self.window_label,
            "trades": n,
            "win_rate_pct": wr,
            "win_rate_display": wr_display,
            "mode_a_return_pct": ret_a,
            "mode_a_closed_return_pct": float(a["closed_return_pct"]),
            "mode_b_return_pct": float(b["return_pct"]),
            "mode_b_closed_return_pct": float(b["closed_return_pct"]),
            "buy_hold_return_pct": bh,
            "mode_a_bh_ratio": ratio_display,
            "mode_a_max_dd_pct": float(a["max_drawdown_pct"]),
            "mode_b_max_dd_pct": float(b["max_drawdown_pct"]),
            "mode_a_open_long": bool(a["ends_open_long"]),
            "mode_b_open_long": bool(b["ends_open_long"]),
            "gate_pass": gate_pass,
            "gate_label": "PASS" if gate_pass else "FAIL",
            "return_basis": "MTM/equity (includes unrealised if open long)",
        }


def summarize(result: ReplayResult) -> dict[str, float | int | str | bool]:
    trades = result.trades
    n = len(trades)
    wins = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl <= 0]
    total_pnl = sum(t.pnl for t in trades)
    # MTM / equity-curve return (gate metric) — includes unrealised open leg
    ret = (
        (result.final_equity / result.initial_equity - 1.0) * 100.0
        if result.initial_equity
        else 0.0
    )
    # Closed-trade PnL return vs initial (not compounded path; excludes unrealised)
    closed_ret = (
        (total_pnl / result.initial_equity) * 100.0 if result.initial_equity else 0.0
    )
    wr = (len(wins) / n * 100.0) if n else 0.0
    ends_open = _open_long_from_trades(result)
    # WR informational only; gate is Mode-A ≥ 1.2× B&H (see evaluate_gate).
    gate_wr_ok = n > 0 and wr >= GATE_WR_MIN  # informational, not pass/fail
    gate_pass, ratio_display = evaluate_gate(ret, result.buy_hold_return_pct)
    gate_bh_ok = gate_pass  # alias: beat-multiple vs B&H
    return {
        "variant": result.variant,
        "trades": n,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": wr,
        "win_rate_display": "n/a" if n == 0 else f"{wr:.2f}%",
        "return_pct": ret,
        "closed_return_pct": closed_ret,
        "buy_hold_return_pct": result.buy_hold_return_pct,
        "vs_buy_hold_pp": ret - result.buy_hold_return_pct,
        "mode_a_bh_ratio": ratio_display,
        "max_drawdown_pct": max_drawdown_pct(result.equity_curve),
        "total_pnl": total_pnl,
        "buy_qty_pct": result.buy_qty_pct,
        "ends_open_long": ends_open,
        "gate_wr_ok": gate_wr_ok,
        "gate_bh_ok": gate_bh_ok,
        "gate_pass": gate_pass,
    }


def _fmt_block(m: dict[str, float | int | str | bool]) -> list[str]:
    return [
        f"| Trades (closed) | {m['trades']} |",
        f"| Wins / Losses | {m['wins']} / {m['losses']} |",
        f"| Win rate (closed) | {m['win_rate_display']} |",
        f"| Strategy return (MTM/equity) | {float(m['return_pct']):.2f}% |",
        f"| Closed-trade PnL / initial | {float(m['closed_return_pct']):.2f}% |",
        f"| Ends open long | {'yes' if m['ends_open_long'] else 'no'} |",
        f"| Buy & hold return | {float(m['buy_hold_return_pct']):.2f}% |",
        f"| vs buy & hold (pp, MTM) | {float(m['vs_buy_hold_pp']):+.2f} |",
        f"| Max drawdown | {float(m['max_drawdown_pct']):.2f}% |",
        f"| Total closed PnL (USDT) | {float(m['total_pnl']):.2f} |",
        f"| Size (buy_qty_pct) | {float(m['buy_qty_pct']):g}% |",
        f"| Mode-A / B&H ratio | {m.get('mode_a_bh_ratio', 'n/a')} |",
        f"| Gate Mode-A ≥ {GATE_BH_MULTIPLIER:g}× B&H (MTM) | "
        f"{'PASS' if m['gate_pass'] else 'FAIL'} |",
        f"| WR ≥{GATE_WR_MIN:g}% (info only) | "
        f"{'yes' if m['gate_wr_ok'] else 'no'} |",
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
        f"- Gate before paper: **Mode-A MTM ≥ {GATE_BH_MULTIPLIER:g}× B&H** "
        f"(WR informational only; Mode A = {MODE_A_PCT:g}% equity; "
        f"Mode B = {MODE_B_PCT:g}% ops). If B&H≤0: PASS only if Mode-A>0; ratio n/a.",
        "- **Return basis for gate:** MTM/equity curve (includes unrealised if open long). "
        "Closed-trade PnL/initial reported separately.",
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
    prep_notes: list[str] | None = None,
) -> Path:
    """
    Dual-sizing gate report: full and/or 6m tables.

    Columns: n | WR | Mode-A | Mode-B | B&H | Mode-A/B&H | PASS/FAIL
    PASS iff Mode-A MTM ≥ 1.2× B&H (WR informational).
    If B&H≤0: PASS only if Mode-A>0; ratio n/a.
    WR shown as n/a when n==0 (not 0%).
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
        f"- **PASS** iff `Mode-A MTM/equity ≥ {GATE_BH_MULTIPLIER:g} × B&H` "
        "(same window). **WR is informational only** (not a pass/fail leg).",
        "- **B&H ≤ 0:** PASS only if Mode-A > 0; Mode-A/B&H ratio shown as **n/a** "
        "(multiple undefined for non-positive B&H).",
        "- **Return basis:** Mode-A/B columns are **MTM/equity** (include unrealised "
        "open long). Closed-trade PnL/initial is in Detail. WR is closed-trades only; "
        "**n/a** when n=0 (not 0%).",
        "",
        "## Data",
        "",
    ]
    for s in sources:
        lines.append(f"- `{s}`")
    if prep_notes:
        lines.append("")
        lines.append("### Sample prep (Claude caveats)")
        lines.append("")
        for note in prep_notes:
            lines.append(f"- {note}")
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
            "| Symbol | Variant | n | WR | Mode-A MTM | Mode-B (ops) MTM | B&H | "
            "Mode-A/B&H | Closed-A / init | Open long | PASS/FAIL |"
        )
        lines.append(
            "|--------|---------|---|----|------------|------------------|-----|"
            "-----------|----------------|-----------|-----------|"
        )
        for row in wrows:
            m = row.summarize()
            open_flag = "yes" if m["mode_a_open_long"] else "no"
            lines.append(
                f"| {m['symbol']} | {m['variant']} | {m['trades']} | "
                f"{m['win_rate_display']} | "
                f"{float(m['mode_a_return_pct']):+.2f}% | "
                f"{float(m['mode_b_return_pct']):+.2f}% | "
                f"{float(m['buy_hold_return_pct']):+.2f}% | "
                f"{m['mode_a_bh_ratio']} | "
                f"{float(m['mode_a_closed_return_pct']):+.2f}% | "
                f"{open_flag} | "
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
            f"(n={m['trades']}, WR={m['win_rate_display']} info, "
            f"Mode-A MTM {float(m['mode_a_return_pct']):+.2f}% / "
            f"B&H {float(m['buy_hold_return_pct']):+.2f}% = "
            f"ratio {m['mode_a_bh_ratio']}; "
            f"need ≥{GATE_BH_MULTIPLIER:g}× when B&H>0; "
            f"closed-A/init {float(m['mode_a_closed_return_pct']):+.2f}%)"
        )
        lines.append(
            f"- Open long at window end (Mode A): "
            f"{'yes — MTM includes unrealised' if m['mode_a_open_long'] else 'no'}"
        )
        lines.append(
            f"- Mode-A max DD {float(m['mode_a_max_dd_pct']):.2f}%; "
            f"Mode-B max DD {float(m['mode_b_max_dd_pct']):.2f}%"
        )
        lines.append(
            f"- Wins/Losses (closed, Mode A): {a['wins']} / {a['losses']}"
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
        f"- Mode A = {MODE_A_PCT:g}% equity (gate: MTM ≥ {GATE_BH_MULTIPLIER:g}× B&H); "
        f"Mode B = {MODE_B_PCT:g}% equity (ops)."
    )
    lines.append(
        "- Closed-trade WR uses completed exits only (informational); WR=n/a when n=0."
    )
    lines.append(
        "- If B&H≤0: PASS only if Mode-A>0; Mode-A/B&H ratio = n/a."
    )
    lines.append(
        "- Dropped last open/partial daily bar; full sample starts 2017-12-31 "
        "(jewel_high warm-up)."
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
