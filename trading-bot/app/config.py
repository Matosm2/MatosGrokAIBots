"""Application configuration with balanced risk defaults."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Binance credentials (never invent; leave empty for paper mode)
    binance_api_key: str = ""
    binance_api_secret: str = ""
    binance_base_url: str = "https://api.binance.com"

    # Webhook auth
    webhook_secret: str = "change-me"

    # Trading mode
    trading_mode: Literal["paper", "live"] = "paper"
    default_quote: str = "USDT"

    # Risk defaults (balanced)
    risk_per_trade_pct: float = Field(default=2.5, ge=0.1, le=100)
    max_position_pct: float = Field(default=12.0, ge=0.1, le=100)
    max_open_positions: int = Field(default=4, ge=1, le=50)
    max_daily_loss_pct: float = Field(default=5.0, ge=0.1, le=100)

    allowed_symbols: str = "BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT"

    # Paper equity baseline (USDT)
    paper_equity_usdt: float = 10_000.0

    # Idempotency TTL (seconds)
    idempotency_ttl_seconds: int = 86_400

    # App
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    @field_validator("trading_mode", mode="before")
    @classmethod
    def normalize_mode(cls, v: object) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v  # type: ignore[return-value]

    @property
    def allowed_symbol_set(self) -> set[str]:
        return {s.strip().upper() for s in self.allowed_symbols.split(",") if s.strip()}

    @property
    def is_paper(self) -> bool:
        return self.trading_mode != "live"


@lru_cache
def get_settings() -> Settings:
    return Settings()
