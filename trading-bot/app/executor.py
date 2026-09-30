"""Order execution: paper (default) and live Binance Spot."""

from __future__ import annotations

import asyncio
import logging
from collections import deque
from typing import TYPE_CHECKING, Deque, Optional

from app.binance_client import BinanceClient
from app.config import Settings
from app.idempotency import ConcurrentClaimError, IdempotencyStore
from app.logging_config import log_event
from app.models import (
    OrderStatus,
    Side,
    TargetPosition,
    TradeRecord,
    TradingViewAlert,
    WebhookResponse,
)
from app.risk import PortfolioState, apply_fill, check_risk, check_strategy_allowlist, resolve_price
from app.target_book import (
    PAPER_ONLY_REASON,
    STRATEGY_ID as BTC_DD2H_ID,
    SYMBOL as BTC_DD2H_SYMBOL,
    SYMBOL_REASON,
    TARGET_REQUIRED_REASON,
    TargetFill,
    apply_target,
    new_btc_dd2h_book,
)

if TYPE_CHECKING:
    from app.persistence import JsonStore

logger = logging.getLogger(__name__)


class TradeExecutor:
    def __init__(
        self,
        settings: Settings,
        state: PortfolioState,
        idempotency: IdempotencyStore,
        binance: Optional[BinanceClient] = None,
        store: Optional["JsonStore"] = None,
    ) -> None:
        self.settings = settings
        self.state = state
        self.idempotency = idempotency
        self.binance = binance
        self.store = store
        self.recent: Deque[TradeRecord] = deque(maxlen=200)
        self._lock = asyncio.Lock()

    def _find_trade(self, trade_id: str) -> Optional[TradeRecord]:
        for t in self.recent:
            if t.id == trade_id:
                return t
        return None

    def _record_side(self, alert: TradingViewAlert) -> Side:
        if alert.side is not None:
            return alert.side
        if alert.target == TargetPosition.LONG:
            return Side.BUY
        return Side.SELL

    def _record_reject(
        self,
        alert: TradingViewAlert,
        alert_id: str,
        reason: str,
    ) -> WebhookResponse:
        trade = TradeRecord(
            alert_id=alert_id,
            symbol=alert.symbol,
            side=self._record_side(alert),
            qty=0.0,
            price=alert.price,
            status=OrderStatus.REJECTED,
            mode=self.settings.trading_mode,
            strategy_id=alert.strategy_id,
            reason=reason,
        )
        self.idempotency.commit(alert_id, trade.id)
        self.recent.appendleft(trade)
        self._persist_portfolio()
        log_event(
            logger,
            "risk_rejected",
            alert_id=alert_id,
            symbol=alert.symbol,
            reason=reason,
        )
        return WebhookResponse(
            ok=False,
            status=OrderStatus.REJECTED,
            trade=trade,
            message=reason,
        )

    def _persist_portfolio(self) -> None:
        if not self.store or not self.store.enabled:
            return
        self.store.save("portfolio.json", self.state.to_dict())

    async def _sync_live_equity(self) -> None:
        """Refresh equity/cash from Binance free balances (live only)."""
        if self.settings.is_paper or self.binance is None:
            return
        try:
            balances = await self.binance.get_account_balances()
        except Exception as exc:  # noqa: BLE001
            log_event(logger, "live_balance_sync_failed", error=str(exc))
            return

        quote = self.settings.default_quote.upper()
        cash = float(balances.get(quote, 0.0))
        # Mark open base assets at last known prices; prefer balance free qty
        mtm = 0.0
        for symbol, qty in list(self.state.open_positions.items()):
            base = symbol[: -len(quote)] if symbol.endswith(quote) else symbol
            free_base = balances.get(base.upper())
            if free_base is not None:
                self.state.open_positions[symbol] = free_base
                qty = free_base
            px = self.state.prices.get(symbol)
            if px is None and qty > 0:
                try:
                    px = await self.binance.get_price(symbol)
                    self.state.prices[symbol] = px
                except Exception:  # noqa: BLE001
                    continue
            if px is not None and qty > 0:
                mtm += qty * px
        self.state.cash_usdt = cash
        self.state.equity_usdt = cash + mtm
        log_event(
            logger,
            "live_balance_synced",
            cash=cash,
            equity=self.state.equity_usdt,
            open_positions=self.state.open_count,
        )

    async def handle_alert(self, alert: TradingViewAlert) -> WebhookResponse:
        assert alert.alert_id is not None
        alert_id = alert.alert_id

        async with self._lock:
            try:
                prior = self.idempotency.claim(alert_id)
            except ConcurrentClaimError:
                log_event(logger, "concurrent_alert", alert_id=alert_id)
                return WebhookResponse(
                    ok=True,
                    status=OrderStatus.DUPLICATE,
                    trade=None,
                    message=f"alert_id={alert_id} already in flight",
                )

            if prior:
                existing = self._find_trade(prior)
                log_event(
                    logger,
                    "duplicate_alert",
                    alert_id=alert_id,
                    trade_id=prior,
                )
                return WebhookResponse(
                    ok=True,
                    status=OrderStatus.DUPLICATE,
                    trade=existing,
                    message=f"Duplicate alert_id={alert_id}; returning prior trade",
                )

            blocked = check_strategy_allowlist(alert, self.settings)
            if blocked is not None:
                return self._record_reject(alert, alert_id, blocked.reason)

            if (alert.strategy_id or "").strip() == BTC_DD2H_ID:
                try:
                    return await self._handle_btc_dd2h(alert, alert_id)
                except Exception:
                    self.idempotency.abort(alert_id)
                    raise

            if alert.side is None:
                return self._record_reject(
                    alert,
                    alert_id,
                    "target long/short/flat is only valid for btc-dd2h",
                )

            # Live: sync balances before sizing (do not use PAPER_EQUITY_USDT)
            if not self.settings.is_paper:
                await self._sync_live_equity()

            decision = check_risk(alert, self.settings, self.state)
            if not decision.allowed:
                # Risk rejects are definitive for this alert_id — commit so retries
                # don't re-spam; failed live orders use abort instead.
                return self._record_reject(alert, alert_id, decision.reason)

            qty = decision.sized_qty or 0.0
            price = alert.price or self.state.prices.get(alert.symbol)
            assert price is not None

            try:
                if self.settings.is_paper:
                    return await self._paper_execute(
                        alert, qty, price, decision.notional_usdt, decision.trimmed
                    )
                return await self._live_execute(
                    alert, qty, price, decision.notional_usdt, decision.trimmed
                )
            except Exception:
                self.idempotency.abort(alert_id)
                raise

    async def _handle_btc_dd2h(
        self,
        alert: TradingViewAlert,
        alert_id: str,
    ) -> WebhookResponse:
        """Paper book only. Never calls Binance, even if TRADING_MODE=live."""
        if not self.settings.is_paper:
            return self._record_reject(alert, alert_id, PAPER_ONLY_REASON)
        if alert.target is None:
            return self._record_reject(alert, alert_id, TARGET_REQUIRED_REASON)
        if alert.symbol != BTC_DD2H_SYMBOL:
            return self._record_reject(alert, alert_id, SYMBOL_REASON)
        if alert.symbol not in self.settings.allowed_symbol_set:
            return self._record_reject(
                alert,
                alert_id,
                f"Symbol {alert.symbol} not in ALLOWED_SYMBOLS",
            )

        price = resolve_price(alert, self.state)
        if price is None or price <= 0:
            return self._record_reject(
                alert,
                alert_id,
                "Missing price: include price in alert or wait for market data",
            )

        book = self.state.strategy_books.get(BTC_DD2H_ID)
        if book is None:
            book = new_btc_dd2h_book()
        marked = book.cash_usdt + book.qty * price
        if alert.target != TargetPosition.FLAT and marked <= 0:
            return self._record_reject(
                alert,
                alert_id,
                "btc-dd2h book equity is not positive",
            )

        fill: TargetFill = apply_target(book, alert.target.value, price)
        if fill.already:
            return self._record_reject(
                alert,
                alert_id,
                f"btc-dd2h already at target {fill.target}",
            )

        self.state.strategy_books[BTC_DD2H_ID] = book
        self.state.prices[alert.symbol] = price
        reason = (
            f"target={fill.target}; fee={fill.fee_usdt:.4f} USDT; "
            f"book equity={book.equity_usdt:.4f}; paper-only"
        )
        trade = TradeRecord(
            alert_id=alert_id,
            symbol=alert.symbol,
            side=fill.side,
            qty=round(fill.qty, 8),
            price=price,
            notional_usdt=round(fill.notional_usdt, 4),
            status=OrderStatus.PAPER,
            mode="paper",
            strategy_id=BTC_DD2H_ID,
            reason=reason,
        )
        self.idempotency.commit(alert_id, trade.id)
        self.recent.appendleft(trade)
        self._persist_portfolio()
        log_event(
            logger,
            "paper_target_order",
            alert_id=alert_id,
            symbol=alert.symbol,
            side=fill.side.value,
            target=fill.target,
            qty=trade.qty,
            price=price,
            fee=fill.fee_usdt,
            strategy_id=BTC_DD2H_ID,
            book_equity=book.equity_usdt,
            book_qty=book.qty,
        )
        return WebhookResponse(
            ok=True,
            status=OrderStatus.PAPER,
            trade=trade,
            message="Paper target recorded",
        )

    async def _paper_execute(
        self,
        alert: TradingViewAlert,
        qty: float,
        price: float,
        notional: float | None,
        trimmed: str | None = None,
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
            reason="Paper/dry-run: order logged, not sent to Binance"
            + (f"; {trimmed}" if trimmed else ""),
        )
        apply_fill(self.state, alert.symbol, alert.side, qty, price)
        self.idempotency.commit(alert.alert_id or trade.id, trade.id)
        self.recent.appendleft(trade)
        self._persist_portfolio()
        log_event(
            logger,
            "paper_order",
            alert_id=alert.alert_id,
            symbol=alert.symbol,
            side=alert.side.value,
            qty=qty,
            price=price,
            notional=notional,
            trimmed=trimmed or "",
            strategy_id=alert.strategy_id or "",
            equity=self.state.equity_usdt,
            daily_pnl=self.state.daily_realized_pnl_usdt,
        )
        return WebhookResponse(
            ok=True,
            status=OrderStatus.PAPER,
            trade=trade,
            message="Paper order recorded"
            + (f" ({trimmed})" if trimmed else ""),
        )

    async def _live_execute(
        self,
        alert: TradingViewAlert,
        qty: float,
        price: float,
        notional: float | None,
        trimmed: str | None = None,
    ) -> WebhookResponse:
        alert_id = alert.alert_id or ""
        if self.binance is None:
            trade = TradeRecord(
                alert_id=alert_id,
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
            # Config failure — abort so operator can fix and retry same alert_id
            self.idempotency.abort(alert_id)
            self.recent.appendleft(trade)
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=trade.reason or "",
            )

        # LOT_SIZE / minNotional before sending
        try:
            adj = await self.binance.adjust_quantity(alert.symbol, qty, price)
        except Exception as exc:  # noqa: BLE001
            trade = TradeRecord(
                alert_id=alert_id,
                symbol=alert.symbol,
                side=alert.side,
                qty=qty,
                price=price,
                notional_usdt=notional,
                status=OrderStatus.REJECTED,
                mode="live",
                strategy_id=alert.strategy_id,
                reason=f"exchange filter error: {exc}",
            )
            self.idempotency.abort(alert_id)
            self.recent.appendleft(trade)
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=trade.reason or "",
            )

        if adj <= 0:
            trade = TradeRecord(
                alert_id=alert_id,
                symbol=alert.symbol,
                side=alert.side,
                qty=qty,
                price=price,
                notional_usdt=notional,
                status=OrderStatus.REJECTED,
                mode="live",
                strategy_id=alert.strategy_id,
                reason="Quantity fails LOT_SIZE/minNotional after rounding",
            )
            self.idempotency.abort(alert_id)
            self.recent.appendleft(trade)
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=trade.reason or "",
            )
        qty = adj
        notional = qty * price

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
                # Weighted average fill if multiple
                total_qty = 0.0
                total_px = 0.0
                for f in fills:
                    fq = float(f.get("qty", 0) or 0)
                    fp = float(f.get("price", price))
                    total_qty += fq
                    total_px += fq * fp
                if total_qty > 0:
                    fill_price = total_px / total_qty
            trade = TradeRecord(
                alert_id=alert_id,
                symbol=alert.symbol,
                side=alert.side,
                qty=qty,
                price=fill_price,
                notional_usdt=round(qty * fill_price, 4),
                status=OrderStatus.FILLED,
                mode="live",
                strategy_id=alert.strategy_id,
                binance_order_id=order_id,
                reason=trimmed,
            )
            apply_fill(self.state, alert.symbol, alert.side, qty, fill_price)
            self.idempotency.commit(alert_id, trade.id)
            self.recent.appendleft(trade)
            self._persist_portfolio()
            log_event(
                logger,
                "live_order_filled",
                alert_id=alert_id,
                symbol=alert.symbol,
                side=alert.side.value,
                qty=qty,
                order_id=order_id,
                trimmed=trimmed or "",
            )
            return WebhookResponse(
                ok=True,
                status=OrderStatus.FILLED,
                trade=trade,
                message="Live order placed",
            )
        except Exception as exc:  # noqa: BLE001
            trade = TradeRecord(
                alert_id=alert_id,
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
            # Do NOT mark idempotent on failed live orders — allow retry
            self.idempotency.abort(alert_id)
            self.recent.appendleft(trade)
            log_event(
                logger,
                "live_order_failed",
                alert_id=alert_id,
                error=str(exc),
            )
            return WebhookResponse(
                ok=False,
                status=OrderStatus.REJECTED,
                trade=trade,
                message=str(exc),
            )
