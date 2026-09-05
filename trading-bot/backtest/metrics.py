"""Performance metrics for backtest results."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.engine import BacktestResult, Trade


@dataclass
class Metrics:
    trades: int
    wins: int
    losses: int
    win_rate_pct: float
    expectancy_usdt: float  # avg PnL per trade
    expectancy_pct: float  # avg pnl_pct per trade
    total_pnl: float
    return_pct: float
    max_drawdown_pct: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    buy_hold_return_pct: float
    vs_buy_hold_pp: float  # strategy return - BH return (percentage points)
    avg_bars_held: float


def max_drawdown_pct(equity: list[float]) -> float:
    if not equity:
        return 0.0
    peak = equity[0]
    max_dd = 0.0
    for e in equity:
        if e > peak:
            peak = e
        if peak > 0:
            dd = (peak - e) / peak * 100.0
            if dd > max_dd:
                max_dd = dd
    return max_dd


def summarize(result: BacktestResult) -> Metrics:
    trades = result.trades
    n = len(trades)
    wins_t = [t for t in trades if t.pnl > 0]
    losses_t = [t for t in trades if t.pnl <= 0]
    total_pnl = sum(t.pnl for t in trades)
    ret = (
        (result.final_equity / result.initial_equity - 1.0) * 100.0
        if result.initial_equity
        else 0.0
    )
    avg_win = sum(t.pnl for t in wins_t) / len(wins_t) if wins_t else 0.0
    avg_loss = sum(t.pnl for t in losses_t) / len(losses_t) if losses_t else 0.0
    gross_win = sum(t.pnl for t in wins_t)
    gross_loss = abs(sum(t.pnl for t in losses_t))
    pf = (gross_win / gross_loss) if gross_loss > 0 else (float("inf") if gross_win > 0 else 0.0)
    return Metrics(
        trades=n,
        wins=len(wins_t),
        losses=len(losses_t),
        win_rate_pct=(len(wins_t) / n * 100.0) if n else 0.0,
        expectancy_usdt=(total_pnl / n) if n else 0.0,
        expectancy_pct=(sum(t.pnl_pct for t in trades) / n) if n else 0.0,
        total_pnl=total_pnl,
        return_pct=ret,
        max_drawdown_pct=max_drawdown_pct(result.equity_curve),
        avg_win=avg_win,
        avg_loss=avg_loss,
        profit_factor=pf,
        buy_hold_return_pct=result.buy_hold_return_pct,
        vs_buy_hold_pp=ret - result.buy_hold_return_pct,
        avg_bars_held=(sum(t.bars_held for t in trades) / n) if n else 0.0,
    )


def combine_results(
    results: list[BacktestResult],
    *,
    label: str = "COMBINED",
) -> tuple[BacktestResult, Metrics]:
    """
    Combined metrics from independent per-symbol runs (each started with
    full initial equity). Equity curves are not merged dollar-for-dollar;
    we report trade-pool stats and average return / max of per-symbol DDs.
    """
    all_trades: list[Trade] = []
    for r in results:
        all_trades.extend(r.trades)
    all_trades.sort(key=lambda t: t.entry_time_ms)

    # Synthetic result for summarize: use equal-weight average equity path length
    # For return: mean of per-symbol returns; for DD: max of per-symbol DDs.
    if not results:
        empty = BacktestResult(symbol=label)
        return empty, summarize(empty)

    init = results[0].initial_equity
    avg_final = sum(r.final_equity for r in results) / len(results)
    # Approximate combined equity curve unavailable; stitch average of aligned
    # returns via trade list + use worst DD among symbols for conservatism.
    avg_bh = sum(r.buy_hold_return_pct for r in results) / len(results)
    fee = results[0].fee_rate
    buy_pct = results[0].buy_qty_pct
    params = results[0].params

    # Build a pseudo equity curve from sequential trades on shared capital:
    # start init, apply each trade's pnl in time order (independent symbols
    # approximated as one book). Sizing was per-symbol equity, so this is
    # slightly inconsistent — documented as trade-pool combined.
    cash_eq = init
    curve = [cash_eq]
    for t in all_trades:
        cash_eq += t.pnl
        curve.append(cash_eq)

    combined = BacktestResult(
        symbol=label,
        trades=all_trades,
        equity_curve=curve,
        timestamps_ms=[],
        initial_equity=init,
        final_equity=curve[-1],
        buy_hold_return_pct=avg_bh,
        fee_rate=fee,
        buy_qty_pct=buy_pct,
        params=params,
    )
    m = summarize(combined)
    # Prefer mean of per-symbol strategy returns for "vs BH" narrative
    mean_ret = sum(
        (r.final_equity / r.initial_equity - 1.0) * 100.0 for r in results
    ) / len(results)
    # Override return to mean per-symbol; keep trade-pool expectancy
    m = Metrics(
        trades=m.trades,
        wins=m.wins,
        losses=m.losses,
        win_rate_pct=m.win_rate_pct,
        expectancy_usdt=m.expectancy_usdt,
        expectancy_pct=m.expectancy_pct,
        total_pnl=m.total_pnl,
        return_pct=mean_ret,
        max_drawdown_pct=max(max_drawdown_pct(r.equity_curve) for r in results),
        avg_win=m.avg_win,
        avg_loss=m.avg_loss,
        profit_factor=m.profit_factor,
        buy_hold_return_pct=avg_bh,
        vs_buy_hold_pp=mean_ret - avg_bh,
        avg_bars_held=m.avg_bars_held,
    )
    return combined, m


def regime_windows(result: BacktestResult) -> list[str]:
    """
    Flag coarse calendar-year buy&hold regimes for the symbol window.

    Single-regime windows (strong bull or bear BH) are called out so readers
    do not over-generalize a 2y sample that is mostly one trend.
    """
    from datetime import datetime, timezone

    if not result.timestamps_ms or not result.equity_curve:
        return ["Insufficient data for regime tagging."]

    # Pair close prices from equity path is wrong; use trade timestamps + BH overall.
    # Build year buckets from bar timestamps using first/last close proxy via BH.
    # We approximate yearly BH using trade entry/exit prices when available,
    # else flag using overall BH magnitude.
    flags: list[str] = []
    by_year: dict[int, list[tuple[int, float]]] = {}
    # Reconstruct approximate price path from trades is incomplete; use
    # overall BH and concentration of trades in calendar years.
    years = sorted({datetime.fromtimestamp(ts / 1000, tz=timezone.utc).year for ts in result.timestamps_ms})
    trade_years = [
        datetime.fromtimestamp(t.entry_time_ms / 1000, tz=timezone.utc).year for t in result.trades
    ]
    if not years:
        return flags

    bh = result.buy_hold_return_pct
    if bh >= 80:
        flags.append(
            f"**Single-regime risk ({result.symbol}):** buy&hold **+{bh:.1f}%** over the window "
            f"— sample is dominated by a strong bull; edge vs BH is hard to generalize."
        )
    elif bh <= -40:
        flags.append(
            f"**Single-regime risk ({result.symbol}):** buy&hold **{bh:.1f}%** over the window "
            f"— sample is dominated by a strong bear; defensive stats may not transfer."
        )
    else:
        flags.append(
            f"{result.symbol} overall buy&hold **{bh:+.1f}%** across years {years[0]}–{years[-1]} "
            f"(mixed/moderate; still only one multi-year path)."
        )

    if trade_years:
        from collections import Counter
        c = Counter(trade_years)
        top_y, top_n = c.most_common(1)[0]
        if top_n >= max(3, int(0.6 * len(trade_years))):
            flags.append(
                f"{result.symbol}: **{top_n}/{len(trade_years)}** trades entered in **{top_y}** "
                f"— trade activity concentrated in one calendar year."
            )
    return flags

