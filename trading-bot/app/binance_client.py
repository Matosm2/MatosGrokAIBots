"""Binance Spot REST client (httpx). Live orders only when TRADING_MODE=live."""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from typing import Any
from urllib.parse import urlencode

import httpx

from app.config import Settings

logger = logging.getLogger(__name__)


class BinanceClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.binance_base_url,
            timeout=15.0,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    def _sign(self, params: dict[str, Any]) -> str:
        query = urlencode(params)
        return hmac.new(
            self.settings.binance_api_secret.encode(),
            query.encode(),
            hashlib.sha256,
        ).hexdigest()

    async def ping(self) -> bool:
        r = await self._client.get("/api/v3/ping")
        return r.status_code == 200

    async def get_price(self, symbol: str) -> float:
        r = await self._client.get("/api/v3/ticker/price", params={"symbol": symbol})
        r.raise_for_status()
        return float(r.json()["price"])

    async def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
    ) -> dict[str, Any]:
        """Place a Spot MARKET order. Requires live credentials."""
        if self.settings.is_paper:
            raise RuntimeError("Refusing live order while TRADING_MODE=paper")
        if not self.settings.binance_api_key or not self.settings.binance_api_secret:
            raise RuntimeError("BINANCE_API_KEY/SECRET required for live trading")

        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "quantity": f"{quantity:.8f}".rstrip("0").rstrip("."),
            "timestamp": int(time.time() * 1000),
        }
        params["signature"] = self._sign(params)
        headers = {"X-MBX-APIKEY": self.settings.binance_api_key}
        r = await self._client.post("/api/v3/order", params=params, headers=headers)
        r.raise_for_status()
        return r.json()
