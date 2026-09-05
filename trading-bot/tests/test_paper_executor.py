"""Unit tests for paper executor and idempotency."""

import pytest

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
    # Position only increased once
    qty = executor.state.open_positions["ETHUSDT"]
    assert abs(qty - first.trade.qty) < 1e-9


@pytest.mark.asyncio
async def test_paper_sell_after_buy(executor: TradeExecutor):
    buy = TradingViewAlert(
        symbol="BTCUSDT", side="buy", qty=0.01, price=60_000, alert_id="b1"
    )
    await executor.handle_alert(buy)
    sell = TradingViewAlert(
        symbol="BTCUSDT", side="sell", qty=0.01, price=61_000, alert_id="s1"
    )
    resp = await executor.handle_alert(sell)
    assert resp.ok
    assert resp.status == OrderStatus.PAPER
    assert "BTCUSDT" not in executor.state.open_positions


@pytest.mark.asyncio
async def test_risk_reject_recorded(executor: TradeExecutor):
    alert = TradingViewAlert(
        symbol="DOGEUSDT", side="buy", price=0.1, alert_id="bad-sym"
    )
    resp = await executor.handle_alert(alert)
    assert not resp.ok
    assert resp.status == OrderStatus.REJECTED
    assert len(executor.recent) == 1
