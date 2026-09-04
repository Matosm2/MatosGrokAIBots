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


class TradingViewAlert(BaseModel):
    """Incoming TradingView webhook JSON schema."""

    symbol: str = Field(..., description="Trading pair, e.g. BTCUSDT")
    side: Side
    qty: Optional[float] = Field(default=None, gt=0, description="Absolute quantity")
    qty_pct: Optional[float] = Field(
        default=None, gt=0, le=100, description="% of equity to risk/allocate"
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
    def normalize_symbol(cls, v: str) -> str:
        return v.strip().upper().replace("/", "").replace("-", "")

    @field_validator("side", mode="before")
    @classmethod
    def normalize_side(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @model_validator(mode="after")
    def require_qty_or_pct(self) -> TradingViewAlert:
        if self.qty is None and self.qty_pct is None:
            # Default: use risk_per_trade_pct from settings at execution time
            pass
        if self.qty is not None and self.qty_pct is not None:
            raise ValueError("Provide either qty or qty_pct, not both")
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


class WebhookResponse(BaseModel):
    ok: bool
    status: OrderStatus
    trade: Optional[TradeRecord] = None
    message: str = ""
