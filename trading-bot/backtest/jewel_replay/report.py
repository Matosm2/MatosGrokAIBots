"""Markdown metrics for jewel-strength-hold-v1 Path B replays."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from backtest.jewel_replay.engine import ReplayResult
from backtest.metrics import max_drawdown_pct


def summarize(result: ReplayResult) -> dict[str, float | int | str]:
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
        "gate_wr_ok": wr >= 60.0,
        "gate_bh_ok": ret > result.buy_hold_return_pct,
    }


def _fmt_block(m: dict[str, float | int | str]) -> list[str]:
    return [
        f"| Trades | {m['trades']} |",
        f"| Wins / Losses | {m['wins']} / {m['losses']} |",
        f"| Win rate | {float(m['win_rate_pct']):.2f}% |",
        f"| Strategy return | {float(m['return_pct']):.2f}% |",
        f"| Buy & hold return | {float(m['buy_hold_return_pct']):.2f}% |",
        f"| vs buy & hold (pp) | {float(m['vs_buy_hold_pp']):+.2f} |",
        f"| Max drawdown | {float(m['max_drawdown_pct']):.2f}% |",
        f"| Total PnL (USDT) | {float(m['total_pnl']):.2f} |",
        f"| Gate WR ≥60% | {'PASS' if m['gate_wr_ok'] else 'FAIL'} |",
        f"| Gate beat B&H | {'PASS' if m['gate_bh_ok'] else 'FAIL'} |",
    ]


def write_replay_markdown(
    *,
    results: list[ReplayResult],
    path: Path,
    source_csv: str,
) -> Path:
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
        "- Costs: 0.10%/side + ≥5 bps slip; size 2.5% equity",
        "- Gate before paper: **≥60% WR** and **beat buy&hold**",
        "",
        f"## Data",
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
            f"slip {r0.slippage_rate * 100:.3f}%; buy {r0.buy_qty_pct}%"
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
