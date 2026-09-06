"""Markdown report for jewel-mtf-hub-regime-v1 open-proxy edition."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from backtest.jewel_mtf_hub.engine import RunResult
from backtest.metrics import max_drawdown_pct

# Lead gate: last-6-month Mode-A return ≥ 1.2 × buy-and-hold (same window)
GATE_MULT = 1.2


def summarize(result: RunResult) -> dict:
    trades = result.trades
    n = len(trades)
    wins = [t for t in trades if t.pnl > 0]
    ret = (
        (result.final_equity / result.initial_equity - 1.0) * 100.0
        if result.initial_equity
        else 0.0
    )
    wr = (len(wins) / n * 100.0) if n else 0.0
    bh = result.buy_hold_return_pct
    ratio = (ret / bh) if bh != 0 else float("nan")
    gate_ok = ret >= GATE_MULT * bh and n > 0
    return {
        "variant": result.variant,
        "mode": result.mode,
        "window": result.window_label,
        "trades": n,
        "wins": len(wins),
        "losses": n - len(wins),
        "win_rate_pct": wr,
        "return_pct": ret,
        "buy_hold_return_pct": bh,
        "ratio_vs_bh": ratio,
        "max_drawdown_pct": max_drawdown_pct(result.equity_curve),
        "gate_ok": gate_ok,
        "gate_label": "PASS" if gate_ok else "FAIL",
    }


def write_report(
    *,
    rows: list[RunResult],
    path: Path,
    symbol: str,
    data_notes: list[str],
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# jewel-mtf-hub-regime-v1 — open-proxy edition",
        "",
        f"_Generated: {now}_",
        "",
        "**RESEARCH ONLY — not paper / alerts / webhook.**",
        "",
        "Public-indicator proxies only (ADX/DI, RSI, EMA). Not Jewel. Not Hub.",
        "",
        "## Frozen proxies",
        "",
        "| Proxy | Definition |",
        "|-------|------------|",
        "| Regime | ADX(14), +DI(14), −DI(14) Wilder; +1 if +DI>−DI and ADX≥20; "
        "−1 if −DI>+DI and ADX≥20; else 0 |",
        "| Flip→green | prior regime ≤ 0 and current = +1 |",
        "| Leave green | prior = +1 and current ≠ +1 |",
        "| Strength | RSI(14); enter crossover(RSI, 60); exit RSI < 50 |",
        "| Ribbon | EMA21 / EMA55; ribbon_low=min, ribbon_high=max; "
        "M1 also allows close×EMA21 while green (default ON) |",
        "| HTF join | HTF state only when htf bar fully closed "
        "(htf_close ≤ ltf_close) — reuse PR #12 join |",
        "| 2D bars | Pair consecutive 1D bars index-wise; drop trailing orphan |",
        "",
        "## Matrix (long-only spot)",
        "",
        "| ID | Rule |",
        "|----|------|",
        "| M1 | TF=2D: entry flip→green OR (green AND close×EMA21); exit leave green |",
        "| M2 | HTF=1D regime=+1, LTF=4H: entry 4H flip→green while 1D=+1; "
        "exit 1D leave green |",
        "| M3 | TF=2D: entry RSI cross 60; exit RSI < 50 |",
        "| M4 | HTF=1D RSI≥60, LTF=4H: entry 4H RSI cross 60 while 1D≥60; "
        "exit 1D RSI < 50 |",
        "",
        "## Costs / sizing",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
        "| Fee | 0.10% / side |",
        "| Slippage | 5 bps adverse vs close |",
        "| Mode-A | 100% equity when in |",
        "| Mode-B | 2.5% equity (ops-parallel; live/paper defaults unchanged) |",
        "| Fills | bar-close |",
        f"| Symbol | {symbol} |",
        "",
        "## Data",
        "",
    ]
    for n in data_notes:
        lines.append(f"- {n}")
    lines.append("")

    # Gate table — 6m Mode-A lead
    lines.append("## Gate table (lead: 6m Mode-A ≥ 1.2 × B&H)")
    lines.append("")
    lines.append(
        "PASS if Mode-A return ≥ **1.2 ×** buy-and-hold over the same 6m window "
        "and ≥1 trade. WR is informational. On FAIL: hard-stop promotion "
        "(no paper/alerts/webhook)."
    )
    lines.append("")
    lines.append(
        "| Variant | Mode | Window | Return | B&H | Ratio | WR | Trades | Gate |"
    )
    lines.append(
        "|---------|------|--------|--------|-----|-------|----|--------|------|"
    )

    six_a = [
        r
        for r in rows
        if r.window_label == "6m" and r.mode == "Mode-A"
    ]
    for r in sorted(six_a, key=lambda x: x.variant):
        m = summarize(r)
        ratio_s = (
            f"{m['ratio_vs_bh']:.2f}×"
            if m["ratio_vs_bh"] == m["ratio_vs_bh"]
            else "n/a"
        )
        lines.append(
            f"| {m['variant']} | {m['mode']} | {m['window']} | "
            f"{m['return_pct']:+.2f}% | {m['buy_hold_return_pct']:+.2f}% | "
            f"{ratio_s} | {m['win_rate_pct']:.1f}% | {m['trades']} | "
            f"**{m['gate_label']}** |"
        )
    lines.append("")

    # Full dual-size tables
    for window in ("6m", "full"):
        lines.append(f"## Results — {window}")
        lines.append("")
        lines.append(
            "| Variant | Mode | Return | B&H | Ratio | WR | Trades | MaxDD | Gate* |"
        )
        lines.append(
            "|---------|------|--------|-----|-------|----|--------|-------|-------|"
        )
        block = [r for r in rows if r.window_label == window]
        for r in sorted(block, key=lambda x: (x.variant, x.mode)):
            m = summarize(r)
            ratio_s = (
                f"{m['ratio_vs_bh']:.2f}×"
                if m["ratio_vs_bh"] == m["ratio_vs_bh"]
                else "n/a"
            )
            # Gate criterion always Mode-A vs 1.2× BH; Mode-B shows informational
            gate = m["gate_label"] if r.mode == "Mode-A" else "—"
            lines.append(
                f"| {m['variant']} | {m['mode']} | {m['return_pct']:+.2f}% | "
                f"{m['buy_hold_return_pct']:+.2f}% | {ratio_s} | "
                f"{m['win_rate_pct']:.1f}% | {m['trades']} | "
                f"{m['max_drawdown_pct']:.2f}% | {gate} |"
            )
        lines.append("")
        lines.append(
            "_\\* Gate column applies the 1.2× B&H rule to Mode-A only "
            "(lead decision on 6m)._"
        )
        lines.append("")

    # Per-variant detail
    for variant in ("M1", "M2", "M3", "M4"):
        lines.append(f"## Detail — {variant}")
        lines.append("")
        subset = [r for r in rows if r.variant == variant]
        if not subset:
            lines.append("_No results._")
            lines.append("")
            continue
        for r in subset:
            m = summarize(r)
            lines.append(f"### {variant} / {r.mode} / {r.window_label}")
            lines.append("")
            if r.timestamps_ms:
                t0 = datetime.fromtimestamp(
                    r.timestamps_ms[0] / 1000, tz=timezone.utc
                )
                t1 = datetime.fromtimestamp(
                    r.timestamps_ms[-1] / 1000, tz=timezone.utc
                )
                lines.append(
                    f"Bars: {len(r.timestamps_ms)} ({t0:%Y-%m-%d} → {t1:%Y-%m-%d} UTC)"
                )
                lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Trades | {m['trades']} |")
            lines.append(f"| Win rate | {m['win_rate_pct']:.2f}% |")
            lines.append(f"| Return | {m['return_pct']:+.2f}% |")
            lines.append(f"| Buy & hold | {m['buy_hold_return_pct']:+.2f}% |")
            ratio_s = (
                f"{m['ratio_vs_bh']:.3f}×"
                if m["ratio_vs_bh"] == m["ratio_vs_bh"]
                else "n/a"
            )
            lines.append(f"| Ratio vs B&H | {ratio_s} |")
            lines.append(f"| Max drawdown | {m['max_drawdown_pct']:.2f}% |")
            if r.mode == "Mode-A":
                lines.append(f"| Gate (≥1.2× B&H) | **{m['gate_label']}** |")
            lines.append("")

    lines.append("## Caveats")
    lines.append("")
    lines.append("- Thresholds frozen; not tuned on the 6m evaluation window.")
    lines.append("- Warmup indicators on full history; window books start flat.")
    lines.append("- Single-path BTCUSDT sample; do not over-generalize.")
    lines.append(
        "- On FAIL vs 1.2× B&H gate: hard-stop promotion — no paper/alerts/webhook."
    )
    lines.append(
        "- Research folder id `jewel-mtf-hub-regime-v1` is archival naming only; "
        "series are open ADX/RSI/EMA proxies."
    )
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
