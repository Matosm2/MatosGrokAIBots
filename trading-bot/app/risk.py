"""Risk management rules applied before order placement."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any

from app.config import Settings
from app.models import RiskDecision, Side, TradingViewAlert

logger = logging.getLogger(__name__)


@dataclass
class PortfolioState:
    """Tracks open positions, cost basis, equity, and daily PnL for risk checks."""

    equity_usdt: float
    cash_usdt: float | None = None  # paper cash; defaults to equity at init
    open_positions: dict[str, float] = field(default_factory=dict)  # symbol -> qty
    avg_entry: dict[str, float] = field(default_factory=dict)  # symbol -> avg cost
    daily_realized_pnl_usdt: float = 0.0
    day_start_equity_usdt: float | None = None
    day: date = field(default_factory=lambda: datetime.now(timezone.utc).date())
    prices: dict[str, float] = field(default_factory=dict)  # last known mid

    def __post_init__(self) -> None:
        if self.cash_usdt is None:
            self.cash_usdt = float(self.equity_usdt)
        if self.day_start_equity_usdt is None:
            self.day_start_equity_usdt = float(self.equity_usdt)

    def reset_day_if_needed(self) -> None:
        today = datetime.now(timezone.utc).date()
        if today != self.day:
            self.day = today
            self.daily_realized_pnl_usdt = 0.0
            self.mark_equity()
            self.day_start_equity_usdt = float(self.equity_usdt)

    @property
    def open_count(self) -> int:
        return sum(1 for q in self.open_positions.values() if abs(q) > 1e-12)

    @property
    def daily_pnl_pct(self) -> float:
        base = self.day_start_equity_usdt or self.equity_usdt
        if base <= 0:
            return 0.0
        return (self.daily_realized_pnl_usdt / base) * 100.0

    def mark_equity(self) -> float:
        """Recompute equity = cash + mark-to-market of open positions."""
        cash = self.cash_usdt if self.cash_usdt is not None else 0.0
        mtm = 0.0
        for sym, qty in self.open_positions.items():
            px = self.prices.get(sym)
            if px is not None and qty > 0:
                mtm += qty * px
        self.equity_usdt = cash + mtm
        return self.equity_usdt

    def to_dict(self) -> dict[str, Any]:
        return {
            "equity_usdt": self.equity_usdt,
            "cash_usdt": self.cash_usdt,
            "open_positions": dict(self.open_positions),
            "avg_entry": dict(self.avg_entry),
            "daily_realized_pnl_usdt": self.daily_realized_pnl_usdt,
            "day_start_equity_usdt": self.day_start_equity_usdt,
            "day": self.day.isoformat(),
            "prices": dict(self.prices),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PortfolioState:
        day_raw = data.get("day")
        day = (
            date.fromisoformat(day_raw)
            if isinstance(day_raw, str)
            else datetime.now(timezone.utc).date()
        )
        dse = data.get("day_start_equity_usdt")
        return cls(
            equity_usdt=float(data.get("equity_usdt", 0)),
            cash_usdt=float(data["cash_usdt"]) if data.get("cash_usdt") is not None else None,
            open_positions={k: float(v) for k, v in (data.get("open_positions") or {}).items()},
            avg_entry={k: float(v) for k, v in (data.get("avg_entry") or {}).items()},
            daily_realized_pnl_usdt=float(data.get("daily_realized_pnl_usdt", 0)),
            day_start_equity_usdt=float(dse) if dse is not None else None,
            day=day,
            prices={k: float(v) for k, v in (data.get("prices") or {}).items()},
        )


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
    Return (qty, notional_usdt) before risk caps.

    Prefer close_all (sells); else explicit qty; else qty_pct of equity;
    else RISK_PER_TRADE_PCT of equity.
    """
    if alert.close_all and alert.side == Side.SELL:
        qty = float(state.open_positions.get(alert.symbol, 0.0))
        return qty, qty * price

    if alert.qty is not None:
        qty = float(alert.qty)
        return qty, qty * price

    pct = alert.qty_pct if alert.qty_pct is not None else settings.risk_per_trade_pct
    notional = state.equity_usdt * (pct / 100.0)
    qty = notional / price if price > 0 else 0.0
    return qty, notional


def check_risk(
    alert: TradingViewAlert,
    settings: Settings,
    state: PortfolioState,
) -> RiskDecision:
    """Apply balanced risk rules; return allow/deny with sized quantity."""
    state.reset_day_if_needed()
    state.mark_equity()

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

    # Daily loss circuit breaker: block new buys/opens only; SELL/closes still allowed
    daily_halt = state.daily_pnl_pct <= -abs(settings.max_daily_loss_pct)
    if daily_halt and alert.side == Side.BUY:
        return RiskDecision(
            allowed=False,
            reason=(
                f"Daily loss limit hit ({state.daily_pnl_pct:.2f}% "
                f"<= -{settings.max_daily_loss_pct}%); buys halted, sells still allowed"
            ),
        )

    qty, notional = size_order(alert, settings, state, price)
    if qty <= 0 or notional <= 0:
        return RiskDecision(allowed=False, reason="Computed quantity is zero")

    trimmed: str | None = None
    max_notional = state.equity_usdt * (settings.max_position_pct / 100.0)
    per_trade_cap = state.equity_usdt * (settings.risk_per_trade_pct / 100.0)
    existing_qty = state.open_positions.get(symbol, 0.0)

    if alert.side == Side.BUY:
        # Absolute qty (and pct sizing) must respect RISK_PER_TRADE_PCT — trim, don't bypass
        if notional > per_trade_cap + 1e-9:
            notional = per_trade_cap
            qty = notional / price
            trimmed = "trimmed_to_risk_per_trade"
            logger.info(
                "trimmed_to_risk_per_trade symbol=%s notional_cap=%.4f",
                symbol,
                per_trade_cap,
            )

        # Then MAX_POSITION_PCT (including existing)
        projected_notional = (existing_qty + qty) * price
        if projected_notional > max_notional + 1e-9:
            room = max(0.0, max_notional - existing_qty * price)
            if room <= 0:
                return RiskDecision(
                    allowed=False,
                    reason=(
                        f"Max position {settings.max_position_pct}% of equity "
                        f"reached for {symbol}"
                    ),
                )
            qty = room / price
            notional = qty * price
            trimmed = trimmed or "trimmed_to_max_position"

        if existing_qty <= 1e-12 and state.open_count >= settings.max_open_positions:
            return RiskDecision(
                allowed=False,
                reason=f"Max open positions ({settings.max_open_positions}) reached",
            )
    else:  # SELL
        if existing_qty <= 1e-12:
            return RiskDecision(
                allowed=False,
                reason=f"No open long position in {symbol} to sell",
            )
        # No-naked-short: allow full exit via min(qty, open_qty).
        # Do NOT apply RISK_PER_TRADE_PCT on sells (qty_pct 12 / close_all / absolute).
        # PRIORITY: post-size RISK_PER_TRADE_PCT must never truncate sells when qty is None.
        qty = min(qty, existing_qty)
        notional = qty * price

    return RiskDecision(
        allowed=True,
        reason="ok",
        sized_qty=round(qty, 8),
        notional_usdt=round(notional, 4),
        trimmed=trimmed,
    )


def apply_fill(
    state: PortfolioState,
    symbol: str,
    side: Side,
    qty: float,
    price: float,
) -> float:
    """
    Update portfolio after a (paper or live) fill.

    Returns realized PnL for this fill (0 on buys; non-zero on sells/closes).
    """
    state.prices[symbol] = price
    current = state.open_positions.get(symbol, 0.0)
    avg = state.avg_entry.get(symbol, price)
    realized = 0.0

    if side == Side.BUY:
        new_qty = current + qty
        if new_qty > 1e-12:
            # Weighted average entry
            state.avg_entry[symbol] = ((avg * current) + (price * qty)) / new_qty
        state.open_positions[symbol] = new_qty
        if state.cash_usdt is not None:
            state.cash_usdt -= qty * price
    else:
        sell_qty = min(qty, current)
        realized = (price - avg) * sell_qty
        state.daily_realized_pnl_usdt += realized
        if state.cash_usdt is not None:
            state.cash_usdt += sell_qty * price
        new_qty = current - sell_qty
        if new_qty <= 1e-12:
            state.open_positions.pop(symbol, None)
            state.avg_entry.pop(symbol, None)
        else:
            state.open_positions[symbol] = new_qty

    state.mark_equity()
    return realized
