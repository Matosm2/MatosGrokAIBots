"""Pydantic models for webhook payloads and trade records."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PAPER = "paper"
    FILLED = "filled"
    DUPLICATE = "duplicate"


# Common TradingView / exchange ticker prefixes to strip → BTCUSDT-style
_EXCHANGE_PREFIXES = (
    "BINANCE:",
    "BINANCE.US:",
    "BYBIT:",
    "COINBASE:",
    "KRAKEN:",
    "OKX:",
    "KUCOIN:",
)


def normalize_symbol(raw: str) -> str:
    """Normalize ticker: strip exchange prefix, slashes/hyphens → BTCUSDT."""
    v = raw.strip().upper()
    for prefix in _EXCHANGE_PREFIXES:
        if v.startswith(prefix):
            v = v[len(prefix) :]
            break
    # Also strip generic EXCHANGE: if still present
    if ":" in v:
        v = v.split(":", 1)[-1]
    return v.replace("/", "").replace("-", "").replace(" ", "")


class TradingViewAlert(BaseModel):
    """Incoming TradingView webhook JSON schema."""

    symbol: str = Field(..., description="Trading pair, e.g. BTCUSDT")
    side: Side
    qty: Optional[float] = Field(default=None, gt=0, description="Absolute quantity")
    qty_pct: Optional[float] = Field(
        default=None, gt=0, le=100, description="% of equity to risk/allocate"
    )
    close_all: bool = Field(
        default=False,
        description="SELL only: close entire open long (ignores qty/qty_pct sizing)",
    )
    strategy_id: Optional[str] = Field(default=None, max_length=128)
    price: Optional[float] = Field(default=None, gt=0)
    alert_id: Optional[str] = Field(
        default=None,
        description="Client-supplied idempotency key; auto-generated if missing",
    )
    secret: Optional[str] = Field(default=None, description="Optional inline secret")
    timestamp: Optional[datetime] = None
    extra: dict[str, Any] = Field(default_factory=dict)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol_field(cls, v: str) -> str:
        return normalize_symbol(v)

    @field_validator("side", mode="before")
    @classmethod
    def normalize_side(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @model_validator(mode="after")
    def require_qty_or_pct(self) -> TradingViewAlert:
        if self.qty is not None and self.qty_pct is not None:
            raise ValueError("Provide either qty or qty_pct, not both")
        if self.close_all and self.side != Side.SELL:
            raise ValueError("close_all is only valid on sell")
        if self.alert_id is None:
            object.__setattr__(
                self,
                "alert_id",
                f"tv-{uuid4().hex[:16]}",
            )
        return self


class RiskDecision(BaseModel):
    allowed: bool
    reason: str = ""
    sized_qty: Optional[float] = None
    notional_usdt: Optional[float] = None
    trimmed: Optional[str] = None  # e.g. trimmed_to_risk_per_trade


class TradeRecord(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    alert_id: str
    symbol: str
    side: Side
    qty: float
    price: Optional[float] = None
    notional_usdt: Optional[float] = None
    status: OrderStatus
    mode: str
    strategy_id: Optional[str] = None
    reason: Optional[str] = None
    binance_order_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthResponse(BaseModel):
    status: str
    trading_mode: str
    allowed_symbols: list[str]
    open_positions: int
    daily_pnl_pct: float
    equity_usdt: Optional[float] = None


class WebhookResponse(BaseModel):
    ok: bool
    status: OrderStatus
    trade: Optional[TradeRecord] = None
    message: str = ""
