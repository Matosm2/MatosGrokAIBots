"""Order execution: paper (default) and live Binance Spot."""

from __future__ import annotations

import logging
from collections import deque
from typing import Deque, Optional

from app.binance_client import BinanceClient
from app.config import Settings
from app.idempotency import IdempotencyStore
from app.logging_config import log_event
from app.models import (
    OrderStatus,
    Side,
    TradeRecord,
    TradingViewAlert,
    WebhookResponse,
)
from app.risk import PortfolioState, apply_fill, check_risk

logger = logging.getLogger(__name__)


class TradeExecutor:
    def __init__(
        self,
        settings: Settings,
        state: PortfolioState,
        idempotency: IdempotencyStore,
        binance: Optional[BinanceClient] = None,
    ) -> None:
        self.settings = settings
        self.state = state
        self.idempotency = idempotency
        self.binance = binance
        self.recent: Deque[TradeRecord] = deque(maxlen=200)

    def _find_trade(self, trade_id: str) -> Optional[TradeRecord]:
        for t in self.recent:
            if t.id == trade_id:
                return t
        return None

    async def handle_alert(self, alert: TradingViewAlert) -> WebhookResponse:
        assert alert.alert_id is not None

        # Idempotency: duplicate alerts
        prior = self.idempotency.seen(alert.alert_id)
        if prior:
            existing = self._find_trade(prior)
            log_event(
                logger,
                "duplicate_alert",
                alert_id=alert.alert_id,
                trade_id=prior,
            )
            return WebhookResponse(
                ok=True,
                status=OrderStatus.DUPLICATE,
                trade=existing,
                message=f"Duplicate alert_id={alert.alert_id}; returning prior trade",
            )

        decision = check_risk(alert, self.settings, self.state)
        if not decision.allowed:
            trade = TradeRecord(
                alert_id=alert.alert_id,
                symbol=alert.symbol,
                side=alert.side,
                qty=0.0,
                price=alert.price,
                status=OrderStatus.REJECTED,
                mode=self.settings.trading_mode,
                strategy_id=alert.strategy_id,
                reason=decision.reason,
            )
            self.idempotency.mark(alert.alert_id, trade.id)
            self.recent.appendleft(trade)
            log_event(
                logger,
                "risk_rejected",
                alert_id=alert.alert_id,
                symbol=alert.symbol,
                reason=decision.reason,
            )
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=decision.reason,
            )

        qty = decision.sized_qty or 0.0
        price = alert.price or self.state.prices.get(alert.symbol)
        assert price is not None

        if self.settings.is_paper:
            return await self._paper_execute(alert, qty, price, decision.notional_usdt)
        return await self._live_execute(alert, qty, price, decision.notional_usdt)

    async def _paper_execute(
        self,
        alert: TradingViewAlert,
        qty: float,
        price: float,
        notional: float | None,
    ) -> WebhookResponse:
        trade = TradeRecord(
            alert_id=alert.alert_id or "",
            symbol=alert.symbol,
            side=alert.side,
            qty=qty,
            price=price,
            notional_usdt=notional,
            status=OrderStatus.PAPER,
            mode="paper",
            strategy_id=alert.strategy_id,
            reason="Paper/dry-run: order logged, not sent to Binance",
        )
        self.idempotency.mark(alert.alert_id or trade.id, trade.id)
        apply_fill(self.state, alert.symbol, alert.side, qty, price)
        self.recent.appendleft(trade)
        log_event(
            logger,
            "paper_order",
            alert_id=alert.alert_id,
            symbol=alert.symbol,
            side=alert.side.value,
            qty=qty,
            price=price,
            notional=notional,
            strategy_id=alert.strategy_id or "",
        )
        return WebhookResponse(
            ok=True,
            status=OrderStatus.PAPER,
            trade=trade,
            message="Paper order recorded",
        )

    async def _live_execute(
        self,
        alert: TradingViewAlert,
        qty: float,
        price: float,
        notional: float | None,
    ) -> WebhookResponse:
        if self.binance is None:
            trade = TradeRecord(
                alert_id=alert.alert_id or "",
                symbol=alert.symbol,
                side=alert.side,
                qty=qty,
                price=price,
                notional_usdt=notional,
                status=OrderStatus.REJECTED,
                mode="live",
                strategy_id=alert.strategy_id,
                reason="Binance client not configured",
            )
            self.idempotency.mark(alert.alert_id or trade.id, trade.id)
            self.recent.appendleft(trade)
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=trade.reason or "",
            )

        try:
            result = await self.binance.place_market_order(
                symbol=alert.symbol,
                side=alert.side.value,
                quantity=qty,
            )
            order_id = str(result.get("orderId", ""))
            fill_price = price
            fills = result.get("fills") or []
            if fills:
                fill_price = float(fills[0].get("price", price))
            trade = TradeRecord(
                alert_id=alert.alert_id or "",
                symbol=alert.symbol,
                side=alert.side,
                qty=qty,
                price=fill_price,
                notional_usdt=notional,
                status=OrderStatus.FILLED,
                mode="live",
                strategy_id=alert.strategy_id,
                binance_order_id=order_id,
            )
            apply_fill(self.state, alert.symbol, alert.side, qty, fill_price)
            self.idempotency.mark(alert.alert_id or trade.id, trade.id)
            self.recent.appendleft(trade)
            log_event(
                logger,
                "live_order_filled",
                alert_id=alert.alert_id,
                symbol=alert.symbol,
                side=alert.side.value,
                qty=qty,
                order_id=order_id,
            )
            return WebhookResponse(
                ok=True,
                status=OrderStatus.FILLED,
                trade=trade,
                message="Live order placed",
            )
        except Exception as exc:  # noqa: BLE001
            trade = TradeRecord(
                alert_id=alert.alert_id or "",
                symbol=alert.symbol,
                side=alert.side,
                qty=qty,
                price=price,
                notional_usdt=notional,
                status=OrderStatus.REJECTED,
                mode="live",
                strategy_id=alert.strategy_id,
                reason=str(exc),
            )
            self.idempotency.mark(alert.alert_id or trade.id, trade.id)
            self.recent.appendleft(trade)
            log_event(
                logger,
                "live_order_failed",
                alert_id=alert.alert_id,
                error=str(exc),
            )
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=str(exc),
            )
