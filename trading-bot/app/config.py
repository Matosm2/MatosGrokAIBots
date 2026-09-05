"""Application configuration with balanced risk defaults."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Secrets that must never be used in live mode
_INSECURE_WEBHOOK_DEFAULTS = frozenset(
    {
        "",
        "change-me",
        "change-me-to-a-long-random-string",
        "YOUR_WEBHOOK_SECRET",
        "test-secret",
    }
)


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

    # Persist portfolio + idempotency under this directory (empty = memory only)
    data_dir: str = "data"

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

    @model_validator(mode="after")
    def fail_closed_live_default_secret(self) -> Settings:
        """Refuse live trading with a default / insecure webhook secret."""
        if self.trading_mode == "live":
            secret = (self.webhook_secret or "").strip()
            if secret.lower() in {s.lower() for s in _INSECURE_WEBHOOK_DEFAULTS}:
                raise ValueError(
                    "WEBHOOK_SECRET is insecure/default; refuse live trading "
                    "(fail-closed). Set a long random secret before TRADING_MODE=live."
                )
            if not self.binance_api_key or not self.binance_api_secret:
                raise ValueError(
                    "BINANCE_API_KEY/SECRET required when TRADING_MODE=live"
                )
        return self

    @property
    def allowed_symbol_set(self) -> set[str]:
        return {s.strip().upper() for s in self.allowed_symbols.split(",") if s.strip()}

    @property
    def is_paper(self) -> bool:
        return self.trading_mode != "live"

    @property
    def insecure_webhook_secret(self) -> bool:
        secret = (self.webhook_secret or "").strip()
        return secret.lower() in {s.lower() for s in _INSECURE_WEBHOOK_DEFAULTS}


@lru_cache
def get_settings() -> Settings:
    return Settings()
