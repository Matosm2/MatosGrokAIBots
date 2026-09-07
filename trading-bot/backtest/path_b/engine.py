"""Generic spot long-only bar-close engine for Path B research."""

from __future__ import annotations

from dataclasses import dataclass, field

from backtest.data import Bar


@dataclass
class Trade:
    symbol: str
    entry_bar: int
    exit_bar: int
    entry_time_ms: int
    exit_time_ms: int
    entry_price: float
    exit_price: float
    qty: float
    notional_entry: float
    pnl: float
    pnl_pct: float
    fee_paid: float
    bars_held: int
    exit_reason: str = "signal"


@dataclass
class SketchResult:
    symbol: str
    strategy_id: str
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    timestamps_ms: list[int] = field(default_factory=list)
    initial_equity: float = 10_000.0
    final_equity: float = 10_000.0
    buy_hold_return_pct: float = 0.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005
    buy_qty_pct: float = 2.5
    window_label: str = ""
    notes: list[str] = field(default_factory=list)


def run_long_only(
    symbol: str,
    strategy_id: str,
    bars: list[Bar],
    buys: list[bool],
    sells: list[bool],
    *,
    stop_prices: list[float | None] | None = None,
    initial_equity: float = 10_000.0,
    buy_qty_pct: float = 2.5,
    fee_rate: float = 0.001,
    slippage_rate: float = 0.0005,
    window_label: str = "",
    notes: list[str] | None = None,
) -> SketchResult:
    """
    Bar-close fills; optional stop checked on close (close < stop => exit).
    stop_prices[i] is the active stop level while in a trade (same value each bar),
    or None when flat / unused. Engine freezes stop at entry from stop_prices[entry].
    """
    assert len(buys) == len(bars) == len(sells)
    cash = initial_equity
    qty = 0.0
    entry_price = 0.0
    entry_bar = -1
    entry_notional = 0.0
    fees_on_trade = 0.0
    stop_level: float | None = None
    trades: list[Trade] = []
    equity_curve: list[float] = []
    timestamps: list[int] = []

    default_notes = [
        f"strategy_id={strategy_id} — RESEARCH sketch; not wired to paper/live.",
        "Bar-close fills only; indicators on closed bars (no lookahead).",
        f"Fee {fee_rate * 100:.2f}%/side; slippage {slippage_rate * 100:.3f}% adverse; "
        f"size {buy_qty_pct}% equity; full close; spot long-only.",
    ]

    for i, bar in enumerate(bars):
        if qty > 0.0:
            stop_hit = stop_level is not None and bar.close < stop_level
            sig_exit = sells[i]
            if stop_hit or sig_exit:
                fill = bar.close * (1.0 - slippage_rate)
                proceeds = qty * fill
                fee = proceeds * fee_rate
                cash += proceeds - fee
                cost = entry_notional + fees_on_trade
                pnl = (proceeds - fee) - cost
                pnl_pct = (pnl / cost) * 100.0 if cost else 0.0
                reason = "stop" if stop_hit and not sig_exit else (
                    "signal+stop" if stop_hit and sig_exit else "signal"
                )
                trades.append(
                    Trade(
                        symbol=symbol,
                        entry_bar=entry_bar,
                        exit_bar=i,
                        entry_time_ms=bars[entry_bar].open_time_ms,
                        exit_time_ms=bar.open_time_ms,
                        entry_price=entry_price,
                        exit_price=fill,
                        qty=qty,
                        notional_entry=entry_notional,
                        pnl=pnl,
                        pnl_pct=pnl_pct,
                        fee_paid=fees_on_trade + fee,
                        bars_held=i - entry_bar,
                        exit_reason=reason,
                    )
                )
                qty = 0.0
                entry_price = 0.0
                entry_bar = -1
                entry_notional = 0.0
                fees_on_trade = 0.0
                stop_level = None

        if buys[i] and qty == 0.0:
            equity = cash
            notional = equity * (buy_qty_pct / 100.0)
            if notional > cash:
                notional = cash
            fill = bar.close * (1.0 + slippage_rate)
            if notional > 0 and fill > 0:
                fee = notional * fee_rate
                spend = notional + fee
                if spend > cash:
                    notional = cash / (1.0 + fee_rate)
                    fee = notional * fee_rate
                    spend = notional + fee
                qty = notional / fill
                cash -= spend
                entry_price = fill
                entry_bar = i
                entry_notional = notional
                fees_on_trade = fee
                if stop_prices is not None and stop_prices[i] is not None:
                    stop_level = stop_prices[i]

        mtm = cash + qty * bar.close
        equity_curve.append(mtm)
        timestamps.append(bar.open_time_ms)

    # Force-close any open long on last bar (honest window PnL / trade count)
    if qty > 0.0 and bars:
        i = len(bars) - 1
        bar = bars[i]
        fill = bar.close * (1.0 - slippage_rate)
        proceeds = qty * fill
        fee = proceeds * fee_rate
        cash += proceeds - fee
        cost = entry_notional + fees_on_trade
        pnl = (proceeds - fee) - cost
        pnl_pct = (pnl / cost) * 100.0 if cost else 0.0
        trades.append(
            Trade(
                symbol=symbol,
                entry_bar=entry_bar,
                exit_bar=i,
                entry_time_ms=bars[entry_bar].open_time_ms,
                exit_time_ms=bar.open_time_ms,
                entry_price=entry_price,
                exit_price=fill,
                qty=qty,
                notional_entry=entry_notional,
                pnl=pnl,
                pnl_pct=pnl_pct,
                fee_paid=fees_on_trade + fee,
                bars_held=i - entry_bar,
                exit_reason="eod",
            )
        )
        qty = 0.0
        equity_curve[-1] = cash

    final = equity_curve[-1] if equity_curve else initial_equity
    if bars:
        bh = (bars[-1].close / bars[0].close - 1.0) * 100.0
    else:
        bh = 0.0

    return SketchResult(
        symbol=symbol,
        strategy_id=strategy_id,
        trades=trades,
        equity_curve=equity_curve,
        timestamps_ms=timestamps,
        initial_equity=initial_equity,
        final_equity=final,
        buy_hold_return_pct=bh,
        fee_rate=fee_rate,
        slippage_rate=slippage_rate,
        buy_qty_pct=buy_qty_pct,
        window_label=window_label,
        notes=(notes or []) + default_notes,
    )


def slice_result_to_window(
    result: SketchResult,
    bars: list[Bar],
    window_start_ms: int,
    *,
    window_label: str,
) -> SketchResult:
    """Keep trades with entry in window; rebuild equity from window start flat book."""
    # Find first bar index in window
    start_i = 0
    for i, b in enumerate(bars):
        if b.open_time_ms >= window_start_ms:
            start_i = i
            break
    else:
        start_i = len(bars)

    win_bars = bars[start_i:]
    if not win_bars:
        return SketchResult(
            symbol=result.symbol,
            strategy_id=result.strategy_id,
            initial_equity=result.initial_equity,
            final_equity=result.initial_equity,
            fee_rate=result.fee_rate,
            slippage_rate=result.slippage_rate,
            buy_qty_pct=result.buy_qty_pct,
            window_label=window_label,
            notes=result.notes + ["Empty window."],
        )

    # Re-simulate would be ideal; approximate: filter trades entering in window
    # and rebuild equity from initial applying only those trades in order,
    # plus mark-to-market path using bar closes while ignoring pre-window.
    # Better: re-run is caller's job with buys masked. Here we filter + BH on window.
    trades = [t for t in result.trades if t.entry_time_ms >= window_start_ms]
    init = result.initial_equity
    # equity curve over window bars: start init, apply trade pnls when exit in window
    # crude but consistent with independent window books when buys were masked pre-window
    eq = init
    curve: list[float] = []
    # Map exit_bar -> pnl
    pnl_at_exit = {t.exit_bar: t.pnl for t in trades}
    # Also need mtm while open — skip detailed mtm; use stepwise cash+pnl at exits
    # Prefer using original curve sliced and rebased if original was masked correctly.
    if len(result.equity_curve) == len(bars) and start_i < len(result.equity_curve):
        base = result.equity_curve[start_i]
        # If flat at window start, rebase to init
        for e in result.equity_curve[start_i:]:
            curve.append(init + (e - base))
        final = curve[-1] if curve else init
    else:
        for i in range(start_i, len(bars)):
            if i in pnl_at_exit:
                eq += pnl_at_exit[i]
            curve.append(eq)
        final = eq

    bh = (win_bars[-1].close / win_bars[0].close - 1.0) * 100.0
    return SketchResult(
        symbol=result.symbol,
        strategy_id=result.strategy_id,
        trades=trades,
        equity_curve=curve,
        timestamps_ms=[b.open_time_ms for b in win_bars],
        initial_equity=init,
        final_equity=final,
        buy_hold_return_pct=bh,
        fee_rate=result.fee_rate,
        slippage_rate=result.slippage_rate,
        buy_qty_pct=result.buy_qty_pct,
        window_label=window_label,
        notes=result.notes,
    )


def apply_position_gate(
    raw_long: list[bool],
    raw_exit: list[bool],
) -> tuple[list[bool], list[bool]]:
    """Pyramiding 0: buy on first raw_long while flat; sell on raw_exit while long."""
    n = len(raw_long)
    buys = [False] * n
    sells = [False] * n
    in_pos = False
    for i in range(n):
        if not in_pos and raw_long[i]:
            buys[i] = True
            in_pos = True
        elif in_pos and raw_exit[i]:
            sells[i] = True
            in_pos = False
    return buys, sells
