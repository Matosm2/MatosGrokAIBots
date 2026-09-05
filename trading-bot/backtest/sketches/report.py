"""Markdown reports + gate table for research sketches (dual sizing)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from backtest.metrics import max_drawdown_pct
from backtest.sketches.engine import SketchResult

# Mode A (gate): 100% equity when in — PASS/FAIL uses this only.
# Mode B (ops): 2.5% equity — report only; never drives PASS/FAIL.
GATE_SIZE_PCT = 100.0
OPS_SIZE_PCT = 2.5


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
    # PASS only meaningful for Mode A (100%-when-in); callers must not gate on ops.
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
        "buy_qty_pct": result.buy_qty_pct,
    }


def write_strategy_report(
    *,
    strategy_id: str,
    rules_md: list[str],
    # results_by_window_mode: {"6m": {"gate": [btc, eth], "ops": [btc, eth]}, ...}
    results_by_window_mode: dict[str, dict[str, list[SketchResult]]],
    path: Path,
) -> Path:
    """Write per-strategy markdown with dual sizing (gate 100% / ops 2.5%)."""
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
    lines.append(
        f"| Size Mode A (**gate**) | **{GATE_SIZE_PCT:.0f}% equity when in** "
        "(PASS/FAIL uses this only) |"
    )
    lines.append(
        f"| Size Mode B (**ops**) | **{OPS_SIZE_PCT}% equity** (Balanced realism; report only) |"
    )
    lines.append("| Close | full position |")
    lines.append("| Mode | spot long-only, bar-close, no lookahead |")
    lines.append("")

    six = results_by_window_mode.get("6m", {})
    gate_results = six.get("gate", [])
    ops_by_sym = {r.symbol: r for r in six.get("ops", [])}

    lines.append("## Gate table (mandatory 6m) — both sizing modes")
    lines.append("")
    lines.append(
        "PASS only if **n>0** AND **WR ≥ 60%** AND **strategy return > buy&hold** "
        "on **Mode A (100%-when-in)**. Mode B is ops realism only (PASS/FAIL = —)."
    )
    lines.append("")
    lines.append(
        "| Strategy | Symbol | Mode | Size | 6m WR | 6m return | 6m B&H | PASS/FAIL |"
    )
    lines.append(
        "|----------|--------|------|------|-------|-----------|--------|-----------|"
    )
    for r in gate_results:
        mg = summarize_sketch(r)
        gate_label = "PASS" if mg["gate_pass"] else "FAIL"
        lines.append(
            f"| {strategy_id} | {r.symbol} | A (gate) | {GATE_SIZE_PCT:.0f}% | "
            f"{mg['win_rate_pct']:.2f}% | {mg['return_pct']:+.2f}% | "
            f"{mg['buy_hold_return_pct']:+.2f}% | **{gate_label}** |"
        )
        ops = ops_by_sym.get(r.symbol)
        if ops is not None:
            mo = summarize_sketch(ops)
            lines.append(
                f"| {strategy_id} | {r.symbol} | B (ops) | {OPS_SIZE_PCT}% | "
                f"{mo['win_rate_pct']:.2f}% | {mo['return_pct']:+.2f}% | "
                f"{mo['buy_hold_return_pct']:+.2f}% | — |"
            )
    lines.append("")

    for window, modes in results_by_window_mode.items():
        lines.append(f"## Window: {window}")
        lines.append("")
        gate_list = modes.get("gate", [])
        ops_map = {r.symbol: r for r in modes.get("ops", [])}
        for r in gate_list:
            for mode_name, res in (
                ("A (gate) 100%", r),
                ("B (ops) 2.5%", ops_map.get(r.symbol)),
            ):
                if res is None:
                    continue
                m = summarize_sketch(res)
                lines.append(f"### {res.symbol} ({window}) — {mode_name}")
                lines.append("")
                if res.timestamps_ms:
                    t0 = datetime.fromtimestamp(
                        res.timestamps_ms[0] / 1000, tz=timezone.utc
                    )
                    t1 = datetime.fromtimestamp(
                        res.timestamps_ms[-1] / 1000, tz=timezone.utc
                    )
                    lines.append(
                        f"Bars in window equity path: {len(res.timestamps_ms)} "
                        f"({t0:%Y-%m-%d} → {t1:%Y-%m-%d} UTC)"
                    )
                    lines.append("")
                lines.append("| Metric | Value |")
                lines.append("|--------|-------|")
                lines.append(f"| Size | {res.buy_qty_pct:g}% equity |")
                lines.append(f"| Trades | {m['trades']} |")
                lines.append(f"| Wins / Losses | {m['wins']} / {m['losses']} |")
                lines.append(f"| Win rate | {m['win_rate_pct']:.2f}% |")
                lines.append(f"| Strategy return | {m['return_pct']:+.2f}% |")
                lines.append(f"| Buy & hold | {m['buy_hold_return_pct']:+.2f}% |")
                lines.append(f"| Max drawdown | {m['max_drawdown_pct']:.2f}% |")
                lines.append(f"| Expectancy (USDT) | {m['expectancy_usdt']:.4f} |")
                lines.append(f"| Avg bars held | {m['avg_bars_held']:.1f} |")
                if mode_name.startswith("A"):
                    gate = "PASS" if m["gate_pass"] else "FAIL"
                    lines.append(f"| Gate (WR≥60% & ret>B&H on 100%) | **{gate}** |")
                else:
                    lines.append("| Gate | — (ops only; not scored) |")
                lines.append("")
                if m["trades"] == 0 and mode_name.startswith("A"):
                    lines.append(
                        "_No trades in this window — entry filters never fired. Gate = FAIL._"
                    )
                    lines.append("")
                if res.trades and mode_name.startswith("A"):
                    lines.append("<details><summary>Trades (first/last 8) — gate book</summary>")
                    lines.append("")
                    lines.append(
                        "| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |"
                    )
                    lines.append(
                        "|---|-----------|----------|-------|------|-----|---|------|-----|"
                    )
                    show = (
                        res.trades
                        if len(res.trades) <= 16
                        else (res.trades[:8] + res.trades[-8:])
                    )
                    for i, t in enumerate(show, 1):
                        idx = i if len(res.trades) <= 16 else (
                            i if i <= 8 else len(res.trades) - (len(show) - i)
                        )
                        te = datetime.fromtimestamp(
                            t.entry_time_ms / 1000, tz=timezone.utc
                        )
                        tx = datetime.fromtimestamp(
                            t.exit_time_ms / 1000, tz=timezone.utc
                        )
                        lines.append(
                            f"| {idx} | {te:%Y-%m-%d %H:%M} | {tx:%Y-%m-%d %H:%M} | "
                            f"{t.entry_price:.4f} | {t.exit_price:.4f} | "
                            f"{t.pnl:.4f} | {t.pnl_pct:.2f}% | {t.bars_held} | "
                            f"{t.exit_reason} |"
                        )
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")

    lines.append("## Caveats")
    lines.append("")
    lines.append("- Warmup indicators computed on longer history; entries only inside each window.")
    lines.append("- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.")
    lines.append("- Single-path sample; do not overfit to one bull/bear window.")
    lines.append("- Gate PASS/FAIL is **only** on Mode A (100%-when-in); Mode B is ops parallel.")
    lines.append("- Not related to Jewel Pine or ema-rsi paper webhook wiring.")
    lines.append("- Does not change live/paper bot defaults.")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_summary_gate_table(
    *,
    rows: list[dict],
    path: Path,
) -> Path:
    """
    rows: strategy_id, symbol, wr, gate_ret, ops_ret, bh, gate
    Dual-sizing 6m summary.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Research sketches — 6m gate summary (dual sizing)",
        "",
        f"_Generated: {now}_",
        "",
        "PASS only if n>0 AND WR ≥ 60% AND **Mode A (100%-when-in)** return > B&H.",
        "Mode B (2.5% ops) is reported for realism only.",
        "",
        "| Strategy | Symbol | 6m WR | Gate ret (100%) | Ops ret (2.5%) | 6m B&H | PASS/FAIL |",
        "|----------|--------|-------|-----------------|----------------|--------|-----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['strategy_id']} | {r['symbol']} | {r['wr']:.2f}% | "
            f"{r['gate_ret']:+.2f}% | {r['ops_ret']:+.2f}% | "
            f"{r['bh']:+.2f}% | **{r['gate']}** |"
        )
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
