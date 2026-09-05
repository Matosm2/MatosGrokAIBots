"""Binance Spot REST client (httpx). Live orders only when TRADING_MODE=live."""

from __future__ import annotations

import hashlib
import hmac
import logging
import math
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from app.config import Settings

logger = logging.getLogger(__name__)


@dataclass
class SymbolFilters:
    step_size: float
    min_qty: float
    min_notional: float


def floor_to_step(qty: float, step: float) -> float:
    """Round quantity down to LOT_SIZE stepSize."""
    if step <= 0:
        return qty
    precision = max(0, int(round(-math.log10(step)))) if step < 1 else 0
    floored = math.floor(qty / step + 1e-15) * step
    return float(f"{floored:.{precision}f}")


class BinanceClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.binance_base_url,
            timeout=15.0,
        )
        self._filters: dict[str, SymbolFilters] = {}

    async def aclose(self) -> None:
        await self._client.aclose()

    @staticmethod
    def round_step(qty: float, step: float) -> float:
        return floor_to_step(qty, step)

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

    async def get_exchange_filters(self, symbol: str) -> SymbolFilters:
        if symbol in self._filters:
            return self._filters[symbol]
        r = await self._client.get("/api/v3/exchangeInfo", params={"symbol": symbol})
        r.raise_for_status()
        data = r.json()
        symbols = data.get("symbols") or []
        if not symbols:
            raise RuntimeError(f"No exchangeInfo for {symbol}")
        step = 0.00001
        min_qty = 0.0
        min_notional = 0.0
        for f in symbols[0].get("filters") or []:
            ftype = f.get("filterType")
            if ftype == "LOT_SIZE":
                step = float(f.get("stepSize", step))
                min_qty = float(f.get("minQty", 0))
            elif ftype in ("MIN_NOTIONAL", "NOTIONAL"):
                raw = f.get("minNotional", f.get("notional", 0))
                min_notional = float(raw or 0)
        filt = SymbolFilters(step_size=step, min_qty=min_qty, min_notional=min_notional)
        self._filters[symbol] = filt
        return filt

    def apply_lot_filters(
        self,
        qty: float,
        price: float,
        filt: SymbolFilters,
    ) -> float:
        """Floor qty to stepSize; raise if below minQty / minNotional."""
        adj = floor_to_step(qty, filt.step_size)
        if adj < filt.min_qty - 1e-15:
            raise ValueError(
                f"Quantity {adj} below LOT_SIZE minQty {filt.min_qty}"
            )
        notional = adj * price
        if filt.min_notional > 0 and notional + 1e-9 < filt.min_notional:
            raise ValueError(
                f"Notional {notional:.4f} below minNotional {filt.min_notional}"
            )
        return adj

    async def adjust_quantity(self, symbol: str, qty: float, price: float) -> float:
        """Fetch LOT_SIZE/minNotional filters and return exchange-legal qty."""
        filt = await self.get_exchange_filters(symbol)
        return self.apply_lot_filters(qty, price, filt)

    async def get_account_balances(self) -> dict[str, float]:
        """Return free balances keyed by asset (e.g. USDT, BTC)."""
        if not self.settings.binance_api_key or not self.settings.binance_api_secret:
            raise RuntimeError("BINANCE_API_KEY/SECRET required for account sync")
        params: dict[str, Any] = {"timestamp": int(time.time() * 1000)}
        params["signature"] = self._sign(params)
        headers = {"X-MBX-APIKEY": self.settings.binance_api_key}
        r = await self._client.get("/api/v3/account", params=params, headers=headers)
        r.raise_for_status()
        out: dict[str, float] = {}
        for bal in r.json().get("balances") or []:
            free = float(bal.get("free", 0))
            if free > 0:
                out[bal["asset"]] = free
        return out

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
