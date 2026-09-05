"""Markdown report writer for ema-rsi-trend-v1.1 backtests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.engine import BacktestResult
from backtest.metrics import Metrics, combine_results, summarize


def _ts(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _regime_flag(bars: list[Bar]) -> str:
    if len(bars) < 100:
        return "Insufficient bars to classify regime."
    n = len(bars)
    mid = n // 2
    first_ret = bars[mid].close / bars[0].close - 1.0
    second_ret = bars[-1].close / bars[mid].close - 1.0
    total = bars[-1].close / bars[0].close - 1.0
    parts = []
    if abs(total) < 0.15:
        parts.append("overall range-ish (±15%)")
    elif total > 0:
        parts.append("overall bullish window")
    else:
        parts.append("overall bearish window")
    if first_ret > 0.1 and second_ret > 0.1:
        parts.append("both halves up — single-regime bull risk")
    elif first_ret < -0.1 and second_ret < -0.1:
        parts.append("both halves down — single-regime bear risk")
    elif (first_ret > 0) != (second_ret > 0):
        parts.append("halves disagree — mixed regimes (good)")
    else:
        parts.append("mildly same-direction halves")
    return "; ".join(parts)


def _fmt_metrics(m: Metrics) -> list[str]:
    pf = m.profit_factor
    pf_s = "inf" if pf == float("inf") else f"{pf:.2f}"
    return [
        f"| Trades | {m.trades} |",
        f"| Wins / Losses | {m.wins} / {m.losses} |",
        f"| Win rate | {m.win_rate_pct:.2f}% |",
        f"| Expectancy (USDT/trade) | {m.expectancy_usdt:.4f} |",
        f"| Expectancy (%/trade) | {m.expectancy_pct:.4f}% |",
        f"| Total PnL (USDT) | {m.total_pnl:.2f} |",
        f"| Strategy return | {m.return_pct:.2f}% |",
        f"| Buy & hold return | {m.buy_hold_return_pct:.2f}% |",
        f"| vs buy & hold (pp) | {m.vs_buy_hold_pp:+.2f} |",
        f"| Max drawdown | {m.max_drawdown_pct:.2f}% |",
        f"| Avg win / avg loss | {m.avg_win:.4f} / {m.avg_loss:.4f} |",
        f"| Profit factor | {pf_s} |",
        f"| Avg bars held (1H) | {m.avg_bars_held:.1f} (~{m.avg_bars_held:.1f}h) |",
    ]


def write_results_markdown(
    *,
    results: list[BacktestResult],
    bars_by_symbol: dict[str, list[Bar]],
    path: Path,
    years: float,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []
    lines.append("# Offline backtest: ema-rsi-trend-v1.1")
    lines.append("")
    lines.append(f"_Generated: {now}_")
    lines.append("")
    lines.append("## Strategy (must-match checklist)")
    lines.append("")
    lines.append("1. **Bar-close only, no lookahead** — fills and signals at bar close.")
    lines.append(
        "2. **Pine v1.1:** EMA20/50 cross + RSI≥50 + close≥EMA50 buy; "
        "sell EMA crossunder OR RSI cross under 40; cooldown 6; BTC+ETH; no hard stop."
    )
    fee = results[0].fee_rate if results else 0.001
    slip = results[0].slippage_rate if results else 0.0005
    lines.append(
        f"3. **Fees/slippage:** fee **{fee * 100:.2f}% per side** "
        f"(Pine `commission_value=0.1`); slippage **{slip * 100:.3f}%** adverse vs close."
    )
    lines.append("4. **Sell = full close** (not 2.5% clips).")
    lines.append(
        "5. **Buy 2.5% equity**; max pos 12% / max 4 opens apply to live bot — "
        "per-symbol offline book has ≤1 open; **daily halt not modeled**."
    )
    lines.append("6. **Spot long-only** — do not conflate with failed futures v1.")
    lines.append(
        "7. Report includes trades, win%, expectancy, vs buy-hold, max DD, hold time; "
        "regime flags below."
    )
    lines.append("")
    lines.append("## Data")
    lines.append("")
    lines.append("- Source: Binance Spot public `/api/v3/klines` (1h)")
    lines.append(f"- Requested lookback: ~{years} years")
    lines.append(f"- Symbols: {', '.join(r.symbol for r in results)}")
    for r in results:
        bars = bars_by_symbol.get(r.symbol, [])
        if bars:
            lines.append(
                f"- **{r.symbol}:** {len(bars)} bars, "
                f"{_ts(bars[0].open_time_ms)} → {_ts(bars[-1].open_time_ms)}"
            )
            lines.append(f"  - Regime note: {_regime_flag(bars)}")
    lines.append("")
    lines.append("## Sizing & costs")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append("| Initial equity (per symbol book) | 10_000 USDT |")
    lines.append("| Buy size | 2.5% of equity |")
    lines.append("| Sell | 100% of open long |")
    lines.append(f"| Fee per side | {fee * 100:.2f}% |")
    lines.append(f"| Slippage per side | {slip * 100:.3f}% adverse |")
    lines.append("| Hard stop | none (v1.1) |")
    lines.append("| Daily loss halt | **not modeled** |")
    lines.append("")

    for r in results:
        m = summarize(r)
        lines.append(f"## {r.symbol}")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.extend(_fmt_metrics(m))
        lines.append("")
        if r.trades:
            lines.append("<details><summary>Trades (first/last 10)</summary>")
            lines.append("")
            lines.append(
                "| # | Entry (UTC) | Exit (UTC) | Entry | Exit | PnL | PnL% | Bars |"
            )
            lines.append("|---|-------------|------------|-------|------|-----|------|------|")
            show = r.trades if len(r.trades) <= 20 else (r.trades[:10] + r.trades[-10:])
            for i, t in enumerate(show, 1):
                idx = i if len(r.trades) <= 20 else (
                    i if i <= 10 else len(r.trades) - (len(show) - i)
                )
                lines.append(
                    f"| {idx} | {_ts(t.entry_time_ms)} | {_ts(t.exit_time_ms)} | "
                    f"{t.entry_price:.4f} | {t.exit_price:.4f} | "
                    f"{t.pnl:.4f} | {t.pnl_pct:.2f}% | {t.bars_held} |"
                )
            if len(r.trades) > 20:
                lines.append("")
                lines.append(f"_… {len(r.trades) - 20} trades omitted …_")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    if len(results) > 1:
        _, cm = combine_results(results)
        lines.append("## COMBINED (trade-pool + mean per-symbol return)")
        lines.append("")
        lines.append(
            "Independent per-symbol books (each started at 10k). "
            "Expectancy/win% from pooled trades; return = mean of per-symbol returns; "
            "max DD = worst per-symbol DD."
        )
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.extend(_fmt_metrics(cm))
        lines.append("")

    lines.append("## Caveats")
    lines.append("")
    for r in results[:1]:
        for n in r.notes:
            lines.append(f"- {n}")
    lines.append(
        "- Single-regime windows: see per-symbol regime notes; do not overfit to one bull run."
    )
    lines.append("- Cache under `backtest/cache/` is gitignored; re-fetch on demand.")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
