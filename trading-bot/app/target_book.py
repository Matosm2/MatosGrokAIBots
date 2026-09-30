"""Separate paper book for target-style strategies (long / short / flat).

btc-dd2h is the only seat. It never shares the spot long-only portfolio and
never places a live order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.models import Side

STRATEGY_ID = "btc-dd2h"
SYMBOL = "BTCUSDT"
START_EQUITY_USDT = 1_000.0
EQUITY_FRACTION = 1.0  # 100% of book equity
LEVERAGE = 1.0
FEE_RATE = 0.00055  # 0.055%
FEE_PCT = 0.055

PAPER_ONLY_REASON = "btc-dd2h is paper-only; live execution is disabled"
TARGET_REQUIRED_REASON = (
    "btc-dd2h requires target long, short, or flat (not spot buy/sell)"
)
SYMBOL_REASON = "btc-dd2h allows BTCUSDT only"


@dataclass
class StrategyBook:
    """Signed paper position for one strategy. Positive qty is long."""

    strategy_id: str
    symbol: str
    cash_usdt: float
    qty: float = 0.0
    avg_entry: Optional[float] = None
    equity_usdt: float = 0.0
    realized_pnl_usdt: float = 0.0
    fees_usdt: float = 0.0

    def __post_init__(self) -> None:
        if self.equity_usdt == 0.0 and self.qty == 0.0:
            self.equity_usdt = float(self.cash_usdt)

    def mark(self, price: float) -> float:
        self.equity_usdt = float(self.cash_usdt) + float(self.qty) * float(price)
        return self.equity_usdt

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "symbol": self.symbol,
            "cash_usdt": self.cash_usdt,
            "qty": self.qty,
            "avg_entry": self.avg_entry,
            "equity_usdt": self.equity_usdt,
            "realized_pnl_usdt": self.realized_pnl_usdt,
            "fees_usdt": self.fees_usdt,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StrategyBook:
        avg = data.get("avg_entry")
        return cls(
            strategy_id=str(data.get("strategy_id") or STRATEGY_ID),
            symbol=str(data.get("symbol") or SYMBOL),
            cash_usdt=float(data.get("cash_usdt", START_EQUITY_USDT)),
            qty=float(data.get("qty", 0.0)),
            avg_entry=float(avg) if avg is not None else None,
            equity_usdt=float(data.get("equity_usdt", data.get("cash_usdt", START_EQUITY_USDT))),
            realized_pnl_usdt=float(data.get("realized_pnl_usdt", 0.0)),
            fees_usdt=float(data.get("fees_usdt", 0.0)),
        )


@dataclass(frozen=True)
class TargetFill:
    side: Side
    qty: float
    price: float
    notional_usdt: float
    fee_usdt: float
    realized_pnl_usdt: float
    target: str
    already: bool = False


def new_btc_dd2h_book() -> StrategyBook:
    return StrategyBook(
        strategy_id=STRATEGY_ID,
        symbol=SYMBOL,
        cash_usdt=START_EQUITY_USDT,
        equity_usdt=START_EQUITY_USDT,
    )


def desired_qty(equity_usdt: float, price: float, target: str) -> float:
    """Signed quantity for 100% of equity at 1x. Flat is zero."""
    if target == "flat":
        return 0.0
    if price <= 0 or equity_usdt <= 0:
        return 0.0
    mag = (equity_usdt * EQUITY_FRACTION * LEVERAGE) / price
    if target == "short":
        return -mag
    return mag


def _realized(qty: float, avg: Optional[float], delta: float, price: float) -> float:
    if abs(qty) <= 1e-12 or avg is None:
        return 0.0
    if qty > 0 and delta < 0:
        closed = min(qty, -delta)
        return (price - avg) * closed
    if qty < 0 and delta > 0:
        closed = min(-qty, delta)
        return (avg - price) * closed
    return 0.0


def _new_avg(
    qty: float,
    avg: Optional[float],
    price: float,
    new_qty: float,
) -> Optional[float]:
    if abs(new_qty) <= 1e-12:
        return None
    flipped = qty > 0 and new_qty < 0 or qty < 0 and new_qty > 0
    if abs(qty) <= 1e-12 or avg is None or flipped:
        return price
    if abs(new_qty) < abs(qty) - 1e-12:
        return avg
    old_abs = abs(qty)
    add_abs = abs(new_qty) - old_abs
    return (avg * old_abs + price * add_abs) / abs(new_qty)


def apply_target(book: StrategyBook, target: str, price: float) -> TargetFill:
    """Move the book to target. Fee is charged on the traded notional."""
    book.mark(price)
    equity = book.equity_usdt
    desired = desired_qty(equity, price, target)
    delta = desired - book.qty
    side = Side.BUY if delta > 0 else Side.SELL
    if abs(delta) <= 1e-12:
        return TargetFill(
            side=side if target != "long" else Side.BUY,
            qty=0.0,
            price=price,
            notional_usdt=0.0,
            fee_usdt=0.0,
            realized_pnl_usdt=0.0,
            target=target,
            already=True,
        )

    notional = abs(delta) * price
    fee = notional * FEE_RATE
    realized = _realized(book.qty, book.avg_entry, delta, price)
    new_qty = book.qty + delta
    book.avg_entry = _new_avg(book.qty, book.avg_entry, price, new_qty)
    if abs(new_qty) <= 1e-12:
        book.qty = 0.0
        book.avg_entry = None
    else:
        book.qty = new_qty
    book.cash_usdt -= delta * price
    book.cash_usdt -= fee
    book.fees_usdt += fee
    book.realized_pnl_usdt += realized
    book.mark(price)
    return TargetFill(
        side=Side.BUY if delta > 0 else Side.SELL,
        qty=abs(delta),
        price=price,
        notional_usdt=notional,
        fee_usdt=fee,
        realized_pnl_usdt=realized,
        target=target,
        already=False,
    )
