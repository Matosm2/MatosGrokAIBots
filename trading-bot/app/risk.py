"""Risk management rules applied before order placement."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from app.config import Settings
from app.models import RiskDecision, Side, TradingViewAlert

logger = logging.getLogger(__name__)


@dataclass
class PortfolioState:
    """Tracks open positions and daily PnL for risk checks."""

    equity_usdt: float
    open_positions: dict[str, float] = field(default_factory=dict)  # symbol -> qty
    daily_realized_pnl_usdt: float = 0.0
    day: date = field(default_factory=lambda: datetime.now(timezone.utc).date())
    prices: dict[str, float] = field(default_factory=dict)  # last known mid

    def reset_day_if_needed(self) -> None:
        today = datetime.now(timezone.utc).date()
        if today != self.day:
            self.day = today
            self.daily_realized_pnl_usdt = 0.0

    @property
    def open_count(self) -> int:
        return sum(1 for q in self.open_positions.values() if abs(q) > 1e-12)

    @property
    def daily_pnl_pct(self) -> float:
        if self.equity_usdt <= 0:
            return 0.0
        return (self.daily_realized_pnl_usdt / self.equity_usdt) * 100.0


def resolve_price(alert: TradingViewAlert, state: PortfolioState) -> float | None:
    if alert.price and alert.price > 0:
        return alert.price
    return state.prices.get(alert.symbol)


def size_order(
    alert: TradingViewAlert,
    settings: Settings,
    state: PortfolioState,
    price: float,
) -> tuple[float, float]:
    """
    Return (qty, notional_usdt).
    Prefer explicit qty; else qty_pct of equity; else RISK_PER_TRADE_PCT of equity.
    """
    if alert.qty is not None:
        qty = float(alert.qty)
        return qty, qty * price

    pct = alert.qty_pct if alert.qty_pct is not None else settings.risk_per_trade_pct
    notional = state.equity_usdt * (pct / 100.0)
    # Cap by max position
    max_notional = state.equity_usdt * (settings.max_position_pct / 100.0)
    notional = min(notional, max_notional)
    qty = notional / price if price > 0 else 0.0
    return qty, notional


def check_risk(
    alert: TradingViewAlert,
    settings: Settings,
    state: PortfolioState,
) -> RiskDecision:
    """Apply balanced risk rules; return allow/deny with sized quantity."""
    state.reset_day_if_needed()

    symbol = alert.symbol
    if symbol not in settings.allowed_symbol_set:
        return RiskDecision(
            allowed=False,
            reason=f"Symbol {symbol} not in ALLOWED_SYMBOLS",
        )

    price = resolve_price(alert, state)
    if price is None or price <= 0:
        return RiskDecision(
            allowed=False,
            reason="Missing price: include price in alert or wait for market data",
        )

    # Daily loss circuit breaker
    if state.daily_pnl_pct <= -abs(settings.max_daily_loss_pct):
        return RiskDecision(
            allowed=False,
            reason=(
                f"Daily loss limit hit ({state.daily_pnl_pct:.2f}% "
                f"<= -{settings.max_daily_loss_pct}%)"
            ),
        )

    qty, notional = size_order(alert, settings, state, price)
    if qty <= 0 or notional <= 0:
        return RiskDecision(allowed=False, reason="Computed quantity is zero")

    # Max position % of equity
    max_notional = state.equity_usdt * (settings.max_position_pct / 100.0)
    existing_qty = state.open_positions.get(symbol, 0.0)
    if alert.side == Side.BUY:
        projected_notional = (existing_qty + qty) * price
        if projected_notional > max_notional + 1e-9:
            # Trim to remaining room
            room = max(0.0, max_notional - existing_qty * price)
            if room <= 0:
                return RiskDecision(
                    allowed=False,
                    reason=f"Max position {settings.max_position_pct}% of equity reached for {symbol}",
                )
            qty = room / price
            notional = qty * price

        # New position slot
        if existing_qty <= 1e-12 and state.open_count >= settings.max_open_positions:
            return RiskDecision(
                allowed=False,
                reason=f"Max open positions ({settings.max_open_positions}) reached",
            )
    else:  # SELL
        if existing_qty <= 1e-12:
            # Allow sell signals that close nothing as reject (spot: no short by default)
            return RiskDecision(
                allowed=False,
                reason=f"No open long position in {symbol} to sell",
            )
        qty = min(qty, existing_qty)
        notional = qty * price

    # Per-trade risk cap on notional
    per_trade_cap = state.equity_usdt * (settings.risk_per_trade_pct / 100.0)
    # Only enforce when sizing via pct defaults; absolute qty still capped by max_position
    if alert.qty is None and notional > per_trade_cap + 1e-9:
        notional = per_trade_cap
        qty = notional / price

    return RiskDecision(
        allowed=True,
        reason="ok",
        sized_qty=round(qty, 8),
        notional_usdt=round(notional, 4),
    )


def apply_fill(
    state: PortfolioState,
    symbol: str,
    side: Side,
    qty: float,
    price: float,
) -> None:
    """Update portfolio after a (paper or live) fill."""
    state.prices[symbol] = price
    current = state.open_positions.get(symbol, 0.0)
    if side == Side.BUY:
        state.open_positions[symbol] = current + qty
    else:
        new_qty = current - qty
        # Realized PnL approximation: mark vs last price already in state
        # Use simple: no cost basis tracking beyond equity adjust
        state.daily_realized_pnl_usdt += 0.0  # placeholder; equity mark-to-market elsewhere
        if new_qty <= 1e-12:
            state.open_positions.pop(symbol, None)
        else:
            state.open_positions[symbol] = new_qty
