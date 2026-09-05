"""Simple long-only bar-close backtest engine (spot)."""

from __future__ import annotations

from dataclasses import dataclass, field

from backtest.data import Bar
from backtest.signals import StrategyParams, apply_position_and_cooldown, compute_indicators


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
    pnl_pct: float  # vs entry cost (notional + entry fee)
    fee_paid: float
    bars_held: int

    @property
    def win(self) -> bool:
        return self.pnl > 0


@dataclass
class BacktestResult:
    symbol: str
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)  # after each bar
    timestamps_ms: list[int] = field(default_factory=list)
    initial_equity: float = 10_000.0
    final_equity: float = 10_000.0
    buy_hold_return_pct: float = 0.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005
    buy_qty_pct: float = 2.5
    params: StrategyParams = field(default_factory=StrategyParams)
    notes: list[str] = field(default_factory=list)


def run_backtest(
    symbol: str,
    bars: list[Bar],
    *,
    params: StrategyParams | None = None,
    initial_equity: float = 10_000.0,
    buy_qty_pct: float = 2.5,
    fee_rate: float = 0.001,
    slippage_rate: float = 0.0005,
    close_entire: bool = True,
) -> BacktestResult:
    """
    Process signals on bar close only (no lookahead).

    Buy: allocate buy_qty_pct% of *current equity* to the long (cash permitting).
    Sell: close entire position (spot long-only; not 2.5% clips).

    fee_rate: fraction per side (0.001 = 0.1%, matching Pine commission_value).
    slippage_rate: adverse fill vs bar close (0.0005 = 5 bps) applied to fill price.
    Fills at close * (1±slippage); fees on notional at fill price.
    """
    _ = close_entire  # always full close in this engine
    params = params or StrategyParams()
    closes = [b.close for b in bars]
    frame = compute_indicators(closes, params)
    buys, sells = apply_position_and_cooldown(frame, params)

    cash = initial_equity
    qty = 0.0
    entry_price = 0.0
    entry_bar = -1
    entry_notional = 0.0
    fees_on_trade = 0.0
    trades: list[Trade] = []
    equity_curve: list[float] = []
    timestamps: list[int] = []

    notes = [
        "Bar-close fills only; indicators use closed bars (no lookahead).",
        f"Fee {fee_rate * 100:.2f}% per side; slippage {slippage_rate * 100:.3f}% "
        "adverse vs close (buy higher / sell lower).",
        "Sell closes 100% of open long (not RISK_PER_TRADE_PCT clips).",
        "Daily loss halt (MAX_DAILY_LOSS_PCT) not modeled in this offline engine.",
        "Spot long-only — not related to any failed futures v1 experiment.",
        "Max position 12% / max 4 opens: single-symbol run has ≤1 open; "
        "multi-symbol portfolio constraints not enforced across independent books.",
    ]

    for i, bar in enumerate(bars):
        if buys[i] and qty == 0.0:
            equity = cash  # flat
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

        elif sells[i] and qty > 0.0:
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
                )
            )
            qty = 0.0
            entry_price = 0.0
            entry_bar = -1
            entry_notional = 0.0
            fees_on_trade = 0.0

        mtm = cash + qty * bar.close
        equity_curve.append(mtm)
        timestamps.append(bar.open_time_ms)

    final = equity_curve[-1] if equity_curve else initial_equity
    if bars:
        bh = (bars[-1].close / bars[0].close - 1.0) * 100.0
    else:
        bh = 0.0

    return BacktestResult(
        symbol=symbol,
        trades=trades,
        equity_curve=equity_curve,
        timestamps_ms=timestamps,
        initial_equity=initial_equity,
        final_equity=final,
        buy_hold_return_pct=bh,
        fee_rate=fee_rate,
        slippage_rate=slippage_rate,
        buy_qty_pct=buy_qty_pct,
        params=params,
        notes=notes,
    )
