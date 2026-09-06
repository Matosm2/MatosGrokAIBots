"""Markdown reports + gate tables for Path B (dual sizing).

Gate (Mode A only): n>0 AND Mode-A return ≥ 1.2 × B&H (same window).
WR is informational — does not drive PASS/FAIL.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from backtest.metrics import max_drawdown_pct
from backtest.path_b.engine import SketchResult

GATE_SIZE_PCT = 100.0
OPS_SIZE_PCT = 2.5
GATE_BH_MULT = 1.2


def summarize_path_b(result: SketchResult) -> dict:
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
    ratio = (ret / bh) if bh != 0 else (float("inf") if ret > 0 else 0.0)
    gate_bh_ok = ret >= GATE_BH_MULT * bh
    gate = n > 0 and gate_bh_ok
    return {
        "trades": n,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": wr,
        "return_pct": ret,
        "buy_hold_return_pct": bh,
        "ret_bh_ratio": ratio,
        "max_drawdown_pct": max_drawdown_pct(result.equity_curve),
        "total_pnl": total_pnl,
        "expectancy_usdt": (total_pnl / n) if n else 0.0,
        "avg_bars_held": (sum(t.bars_held for t in trades) / n) if n else 0.0,
        "gate_pass": gate,
        "gate_bh_ok": gate_bh_ok,
        "buy_qty_pct": result.buy_qty_pct,
    }


def write_strategy_report(
    *,
    strategy_id: str,
    rules_md: list[str],
    results_by_window_mode: dict[str, dict[str, list[SketchResult]]],
    path: Path,
    extra_notes: list[str] | None = None,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        f"# Offline backtest: {strategy_id}",
        "",
        f"_Generated: {now}_",
        "",
        "**RESEARCH ONLY — not enabled for paper/live. Hard-stop on FAIL (no paper/alerts/webhook).**",
        "",
        "## Rules",
        "",
    ]
    for r in rules_md:
        lines.append(f"- {r}")
    lines.extend(
        [
            "",
            "## Common costs / sizing",
            "",
            "| Parameter | Value |",
            "|-----------|-------|",
            "| Fee | 0.10% / side |",
            "| Slippage | 5 bps adverse vs close |",
            f"| Size Mode A (**gate**) | **{GATE_SIZE_PCT:.0f}% equity when in** (PASS/FAIL uses this only) |",
            f"| Size Mode B (**ops**) | **{OPS_SIZE_PCT}% equity** (report only) |",
            "| Close | full position |",
            "| Mode | spot long-only, bar-close, no lookahead |",
            "| Data | Binance Spot OHLCV via **ccxt** (owned cache) |",
            "",
            "## Gate table (mandatory 6m Mode-A lead)",
            "",
            f"PASS iff **n>0** AND **Mode-A return ≥ {GATE_BH_MULT} × B&H** (same window). "
            "WR informational only. Mode B = —.",
            "",
            "| Strategy | Symbol | Mode | Size | 6m WR | 6m Mode-A ret | 6m B&H | ret/B&H | PASS/FAIL |",
            "|----------|--------|------|------|-------|---------------|--------|---------|-----------|",
        ]
    )
    six = results_by_window_mode.get("6m", {})
    gate_results = six.get("gate", [])
    ops_by_sym = {r.symbol: r for r in six.get("ops", [])}
    for r in gate_results:
        mg = summarize_path_b(r)
        gate_label = "PASS" if mg["gate_pass"] else "FAIL"
        ratio_s = (
            f"{mg['ret_bh_ratio']:.3f}"
            if mg["ret_bh_ratio"] not in (float("inf"), float("-inf"))
            else "n/a"
        )
        lines.append(
            f"| {strategy_id} | {r.symbol} | A (gate) | {GATE_SIZE_PCT:.0f}% | "
            f"{mg['win_rate_pct']:.2f}% | {mg['return_pct']:+.2f}% | "
            f"{mg['buy_hold_return_pct']:+.2f}% | {ratio_s} | **{gate_label}** |"
        )
        ops = ops_by_sym.get(r.symbol)
        if ops is not None:
            mo = summarize_path_b(ops)
            lines.append(
                f"| {strategy_id} | {r.symbol} | B (ops) | {OPS_SIZE_PCT}% | "
                f"{mo['win_rate_pct']:.2f}% | {mo['return_pct']:+.2f}% | "
                f"{mo['buy_hold_return_pct']:+.2f}% | — | — |"
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
                m = summarize_path_b(res)
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
                        f"Bars: {len(res.timestamps_ms)} "
                        f"({t0:%Y-%m-%d} → {t1:%Y-%m-%d} UTC)"
                    )
                    lines.append("")
                lines.append("| Metric | Value |")
                lines.append("|--------|-------|")
                lines.append(f"| Size | {res.buy_qty_pct:g}% equity |")
                lines.append(f"| Trades | {m['trades']} |")
                lines.append(f"| Wins / Losses | {m['wins']} / {m['losses']} |")
                lines.append(f"| Win rate (info) | {m['win_rate_pct']:.2f}% |")
                lines.append(f"| Strategy return | {m['return_pct']:+.2f}% |")
                lines.append(f"| Buy & hold | {m['buy_hold_return_pct']:+.2f}% |")
                ratio_s = (
                    f"{m['ret_bh_ratio']:.3f}"
                    if m["ret_bh_ratio"] not in (float("inf"), float("-inf"))
                    else "n/a"
                )
                lines.append(f"| ret / B&H | {ratio_s} |")
                lines.append(f"| Max drawdown | {m['max_drawdown_pct']:.2f}% |")
                lines.append(f"| Expectancy (USDT) | {m['expectancy_usdt']:.4f} |")
                lines.append(f"| Avg bars held | {m['avg_bars_held']:.1f} |")
                if mode_name.startswith("A"):
                    gate = "PASS" if m["gate_pass"] else "FAIL"
                    lines.append(
                        f"| Gate (ret ≥ {GATE_BH_MULT}×B&H on 100%) | **{gate}** |"
                    )
                    if not m["gate_pass"]:
                        lines.append("| Promotion | **HARD-STOP** — no paper/alerts/webhook |")
                else:
                    lines.append("| Gate | — (ops only; not scored) |")
                lines.append("")
                if m["trades"] == 0 and mode_name.startswith("A"):
                    lines.append(
                        "_No trades in this window — Gate = FAIL / hard-stop._"
                    )
                    lines.append("")
                if res.trades and mode_name.startswith("A"):
                    lines.append("<details><summary>Trades (first/last 8)</summary>")
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
                        idx = (
                            i
                            if len(res.trades) <= 16
                            else (i if i <= 8 else len(res.trades) - (len(show) - i))
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
    lines.append("- Warmup on longer history; entries only inside each window.")
    lines.append("- Thresholds fixed a priori — **not tuned on the 6m window**.")
    lines.append("- Gate PASS/FAIL only on Mode A (100%-when-in); Mode B ops parallel.")
    lines.append("- Does not change live/paper bot defaults.")
    lines.append("- Fresh Path B IDs — not Jewel / open-proxy / ADX-RSI-EMA-MTF / #13.")
    if extra_notes:
        for n in extra_notes:
            lines.append(f"- {n}")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_batch_summary(
    *,
    rows: list[dict],
    path: Path,
) -> Path:
    """rows: strategy_id, symbol, wr, gate_ret, ops_ret, bh, ratio, trades, gate"""
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Path B research — 6m Mode-A gate summary",
        "",
        f"_Generated: {now}_",
        "",
        f"PASS iff n>0 AND **Mode-A return ≥ {GATE_BH_MULT} × B&H**. WR informational.",
        "FAIL ⇒ hard-stop promotion (no paper/alerts/webhook).",
        "",
        "| Strategy | Symbol | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |",
        "|----------|--------|--------|-------|------------|-----|---------|---------|-----------|",
    ]
    for r in rows:
        ratio_s = (
            f"{r['ratio']:.3f}"
            if r.get("ratio") not in (None, float("inf"), float("-inf"))
            else "n/a"
        )
        lines.append(
            f"| {r['strategy_id']} | {r['symbol']} | {r['trades']} | "
            f"{r['wr']:.2f}% | {r['gate_ret']:+.2f}% | {r['bh']:+.2f}% | "
            f"{ratio_s} | {r['ops_ret']:+.2f}% | **{r['gate']}** |"
        )
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
