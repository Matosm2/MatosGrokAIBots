"""Unit tests for paper executor and idempotency."""

from unittest.mock import AsyncMock

import pytest

from app.binance_client import BinanceClient
from app.config import Settings
from app.executor import TradeExecutor
from app.idempotency import IdempotencyStore
from app.models import OrderStatus, Side, TradingViewAlert
from app.risk import PortfolioState


@pytest.fixture
def executor() -> TradeExecutor:
    settings = Settings(
        trading_mode="paper",
        webhook_secret="test-secret",
        risk_per_trade_pct=2.5,
        max_position_pct=12.0,
        max_open_positions=4,
        max_daily_loss_pct=5.0,
        allowed_symbols="BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT",
        paper_equity_usdt=10_000.0,
        data_dir="",
    )
    state = PortfolioState(
        equity_usdt=10_000,
        prices={"BTCUSDT": 60_000.0, "ETHUSDT": 3_000.0},
    )
    return TradeExecutor(settings, state, IdempotencyStore(), binance=None)


@pytest.mark.asyncio
async def test_paper_buy_logs_order(executor: TradeExecutor):
    alert = TradingViewAlert(
        symbol="BTCUSDT",
        side="buy",
        price=60_000,
        alert_id="alert-1",
        strategy_id="test-strat",
    )
    resp = await executor.handle_alert(alert)
    assert resp.ok
    assert resp.status == OrderStatus.PAPER
    assert resp.trade is not None
    assert resp.trade.qty > 0
    assert resp.trade.mode == "paper"
    assert executor.state.open_positions.get("BTCUSDT", 0) > 0
    assert len(executor.recent) == 1


@pytest.mark.asyncio
async def test_duplicate_alert_idempotent(executor: TradeExecutor):
    alert = TradingViewAlert(
        symbol="ETHUSDT",
        side="buy",
        price=3_000,
        alert_id="dup-42",
    )
    first = await executor.handle_alert(alert)
    second = await executor.handle_alert(alert)
    assert first.status == OrderStatus.PAPER
    assert second.status == OrderStatus.DUPLICATE
    assert second.trade is not None
    assert first.trade is not None
    assert second.trade.id == first.trade.id
    qty = executor.state.open_positions["ETHUSDT"]
    assert abs(qty - first.trade.qty) < 1e-9


@pytest.mark.asyncio
async def test_paper_sell_after_buy(executor: TradeExecutor):
    # 0.004 BTC @ 60k = 240 USDT < 2.5% risk cap (250) so not trimmed
    buy = TradingViewAlert(
        symbol="BTCUSDT", side="buy", qty=0.004, price=60_000, alert_id="b1"
    )
    buy_resp = await executor.handle_alert(buy)
    assert buy_resp.ok and buy_resp.trade is not None
    bought = buy_resp.trade.qty
    sell = TradingViewAlert(
        symbol="BTCUSDT", side="sell", qty=bought, price=61_000, alert_id="s1"
    )
    resp = await executor.handle_alert(sell)
    assert resp.ok
    assert resp.status == OrderStatus.PAPER
    assert "BTCUSDT" not in executor.state.open_positions
    # Meaningful paper PnL: (61000-60000)*bought
    expected = (61_000 - 60_000) * bought
    assert abs(executor.state.daily_realized_pnl_usdt - expected) < 1e-6


@pytest.mark.asyncio
async def test_paper_sell_qty_pct_12_full_slice(executor: TradeExecutor):
    """PRIORITY: paper path also must not cap sells to RISK_PER_TRADE_PCT."""
    # Seed a 12% position
    open_qty = 0.02  # 0.02 * 60_000 = 1_200
    executor.state.open_positions["BTCUSDT"] = open_qty
    executor.state.avg_entry["BTCUSDT"] = 60_000
    executor.state.cash_usdt = 8_800
    executor.state.mark_equity()
    sell = TradingViewAlert(
        symbol="BTCUSDT",
        side="sell",
        qty_pct=12,
        price=60_000,
        alert_id="sell-12",
    )
    resp = await executor.handle_alert(sell)
    assert resp.ok
    assert resp.trade is not None
    assert abs(resp.trade.qty - open_qty) < 1e-9


@pytest.mark.asyncio
async def test_risk_reject_recorded(executor: TradeExecutor):
    alert = TradingViewAlert(
        symbol="DOGEUSDT", side="buy", price=0.1, alert_id="bad-sym"
    )
    resp = await executor.handle_alert(alert)
    assert not resp.ok
    assert resp.status == OrderStatus.REJECTED
    assert len(executor.recent) == 1


@pytest.mark.asyncio
async def test_failed_live_order_not_marked_idempotent():
    """HIGH: failed live orders must abort claim so the same alert_id can retry."""
    settings = Settings(
        trading_mode="live",
        webhook_secret="strong-live-secret-not-default",
        binance_api_key="k",
        binance_api_secret="s",
        risk_per_trade_pct=2.5,
        max_position_pct=12.0,
        max_open_positions=4,
        max_daily_loss_pct=5.0,
        allowed_symbols="BTCUSDT",
        paper_equity_usdt=10_000.0,
        data_dir="",
    )
    state = PortfolioState(equity_usdt=10_000, prices={"BTCUSDT": 60_000.0})
    binance = BinanceClient(settings)
    binance.get_account_balances = AsyncMock(return_value={"USDT": 10_000.0})  # type: ignore[method-assign]
    binance.adjust_quantity = AsyncMock(return_value=0.004)  # type: ignore[method-assign]
    binance.place_market_order = AsyncMock(side_effect=RuntimeError("binance down"))  # type: ignore[method-assign]

    ex = TradeExecutor(settings, state, IdempotencyStore(), binance=binance)
    alert = TradingViewAlert(
        symbol="BTCUSDT", side="buy", price=60_000, alert_id="live-fail-1"
    )
    first = await ex.handle_alert(alert)
    assert not first.ok
    assert first.status == OrderStatus.REJECTED
    assert ex.idempotency.seen("live-fail-1") is None

    # Retry should not be DUPLICATE
    second = await ex.handle_alert(alert)
    assert second.status == OrderStatus.REJECTED
    assert second.status != OrderStatus.DUPLICATE
