"""Markdown reports + gate table for research sketches."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from backtest.metrics import max_drawdown_pct
from backtest.sketches.engine import SketchResult


def summarize_sketch(result: SketchResult) -> dict:
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
    bh = result.buy_hold_return_pct
    gate_wr = wr >= 60.0
    gate_bh = ret > bh
    gate = gate_wr and gate_bh and n > 0
    return {
        "trades": n,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": wr,
        "return_pct": ret,
        "buy_hold_return_pct": bh,
        "max_drawdown_pct": max_drawdown_pct(result.equity_curve),
        "total_pnl": total_pnl,
        "expectancy_usdt": (total_pnl / n) if n else 0.0,
        "avg_bars_held": (sum(t.bars_held for t in trades) / n) if n else 0.0,
        "gate_pass": gate,
        "gate_wr_ok": gate_wr,
        "gate_bh_ok": gate_bh,
    }


def write_strategy_report(
    *,
    strategy_id: str,
    rules_md: list[str],
    results_by_window: dict[str, list[SketchResult]],
    path: Path,
) -> Path:
    """
    results_by_window: e.g. {"6m": [btc, eth], "2y": [btc, eth]}
    Mandatory gate table uses 6m rows.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []
    lines.append(f"# Offline backtest: {strategy_id}")
    lines.append("")
    lines.append(f"_Generated: {now}_")
    lines.append("")
    lines.append("**RESEARCH ONLY — not enabled for paper/live.**")
    lines.append("")
    lines.append("## Rules")
    lines.append("")
    for r in rules_md:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## Common costs / sizing")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append("| Fee | 0.10% / side |")
    lines.append("| Slippage | 5 bps adverse vs close |")
    lines.append("| Size | 2.5% equity |")
    lines.append("| Close | full position |")
    lines.append("| Mode | spot long-only, bar-close, no lookahead |")
    lines.append("")

    # Mandatory 6m gate table
    six = results_by_window.get("6m", [])
    lines.append("## Gate table (mandatory 6m)")
    lines.append("")
    lines.append("PASS only if **WR ≥ 60%** AND **strategy return > buy&hold** (and ≥1 trade).")
    lines.append("")
    lines.append("| Strategy | Symbol | 6m WR | 6m return | 6m B&H | PASS/FAIL |")
    lines.append("|----------|--------|-------|-----------|--------|-----------|")
    for r in six:
        m = summarize_sketch(r)
        gate = "PASS" if m["gate_pass"] else "FAIL"
        lines.append(
            f"| {strategy_id} | {r.symbol} | {m['win_rate_pct']:.2f}% | "
            f"{m['return_pct']:+.2f}% | {m['buy_hold_return_pct']:+.2f}% | **{gate}** |"
        )
    lines.append("")

    for window, results in results_by_window.items():
        lines.append(f"## Window: {window}")
        lines.append("")
        for r in results:
            m = summarize_sketch(r)
            lines.append(f"### {r.symbol} ({window})")
            lines.append("")
            if r.timestamps_ms:
                t0 = datetime.fromtimestamp(r.timestamps_ms[0] / 1000, tz=timezone.utc)
                t1 = datetime.fromtimestamp(r.timestamps_ms[-1] / 1000, tz=timezone.utc)
                lines.append(
                    f"Bars in window equity path: {len(r.timestamps_ms)} "
                    f"({t0:%Y-%m-%d} → {t1:%Y-%m-%d} UTC)"
                )
                lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Trades | {m['trades']} |")
            lines.append(f"| Wins / Losses | {m['wins']} / {m['losses']} |")
            lines.append(f"| Win rate | {m['win_rate_pct']:.2f}% |")
            lines.append(f"| Strategy return | {m['return_pct']:+.2f}% |")
            lines.append(f"| Buy & hold | {m['buy_hold_return_pct']:+.2f}% |")
            lines.append(f"| Max drawdown | {m['max_drawdown_pct']:.2f}% |")
            lines.append(f"| Expectancy (USDT) | {m['expectancy_usdt']:.4f} |")
            lines.append(f"| Avg bars held | {m['avg_bars_held']:.1f} |")
            gate = "PASS" if m["gate_pass"] else "FAIL"
            lines.append(f"| Gate (WR≥60% & ret>B&H) | **{gate}** |")
            lines.append("")
            if m["trades"] == 0:
                lines.append(
                    "_No trades in this window — entry filters never fired "
                    "(e.g. daily EMA50≤EMA200 for ADX/HTF bias). Gate = FAIL._"
                )
                lines.append("")
            if r.trades:
                lines.append("<details><summary>Trades (first/last 8)</summary>")
                lines.append("")
                lines.append(
                    "| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |"
                )
                lines.append(
                    "|---|-----------|----------|-------|------|-----|---|------|-----|"
                )
                show = r.trades if len(r.trades) <= 16 else (r.trades[:8] + r.trades[-8:])
                for i, t in enumerate(show, 1):
                    idx = i if len(r.trades) <= 16 else (
                        i if i <= 8 else len(r.trades) - (len(show) - i)
                    )
                    te = datetime.fromtimestamp(t.entry_time_ms / 1000, tz=timezone.utc)
                    tx = datetime.fromtimestamp(t.exit_time_ms / 1000, tz=timezone.utc)
                    lines.append(
                        f"| {idx} | {te:%Y-%m-%d %H:%M} | {tx:%Y-%m-%d %H:%M} | "
                        f"{t.entry_price:.4f} | {t.exit_price:.4f} | "
                        f"{t.pnl:.4f} | {t.pnl_pct:.2f}% | {t.bars_held} | {t.exit_reason} |"
                    )
                lines.append("")
                lines.append("</details>")
                lines.append("")

    lines.append("## Caveats")
    lines.append("")
    lines.append("- Warmup indicators computed on longer history; entries only inside each window.")
    lines.append("- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.")
    lines.append("- Single-path sample; do not overfit to one bull/bear window.")
    lines.append("- Not related to Jewel Pine or ema-rsi paper webhook wiring.")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_summary_gate_table(
    *,
    rows: list[dict],
    path: Path,
) -> Path:
    """rows: strategy_id, symbol, wr, ret, bh, pass"""
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Research sketches — 6m gate summary",
        "",
        f"_Generated: {now}_",
        "",
        "PASS only if WR ≥ 60% AND return > B&H.",
        "",
        "| Strategy | Symbol | 6m WR | 6m return | 6m B&H | PASS/FAIL |",
        "|----------|--------|-------|-----------|--------|-----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['strategy_id']} | {r['symbol']} | {r['wr']:.2f}% | "
            f"{r['ret']:+.2f}% | {r['bh']:+.2f}% | **{r['gate']}** |"
        )
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
