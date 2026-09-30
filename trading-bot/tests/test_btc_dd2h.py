"""btc-dd2h target-style paper book: allowlist, fees, and no live path."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.binance_client import BinanceClient
from app.config import Settings
from app.executor import TradeExecutor
from app.idempotency import IdempotencyStore
from app.models import OrderStatus, TradingViewAlert
from app.risk import PortfolioState
from app.target_book import FEE_RATE, START_EQUITY_USDT


def _settings(**overrides: object) -> Settings:
    base: dict[str, object] = dict(
        trading_mode="paper",
        webhook_secret="test-secret",
        risk_per_trade_pct=2.5,
        max_position_pct=12.0,
        max_open_positions=4,
        max_daily_loss_pct=5.0,
        allowed_symbols="BTCUSDT,ETHUSDT",
        allowed_strategies="btc-dd2h",
        paper_equity_usdt=10_000.0,
        data_dir="",
    )
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _executor(settings: Settings | None = None) -> TradeExecutor:
    settings = settings or _settings()
    state = PortfolioState(
        equity_usdt=10_000,
        prices={"BTCUSDT": 50_000.0, "ETHUSDT": 3_000.0},
    )
    return TradeExecutor(settings, state, IdempotencyStore(), binance=None)


def _alert(target: str, alert_id: str, **overrides: object) -> TradingViewAlert:
    payload: dict[str, object] = dict(
        symbol="BTCUSDT",
        target=target,
        price=50_000,
        alert_id=alert_id,
        strategy_id="btc-dd2h",
    )
    payload.update(overrides)
    return TradingViewAlert(**payload)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_happy_path_long_short_flat_separate_book():
    ex = _executor()
    main_cash = ex.state.cash_usdt

    long_resp = await ex.handle_alert(_alert("long", "dd-long"))
    assert long_resp.ok
    assert long_resp.status == OrderStatus.PAPER
    assert long_resp.trade is not None
    assert long_resp.trade.side.value == "buy"
    assert long_resp.trade.qty == pytest.approx(0.02)

    book = ex.state.strategy_books["btc-dd2h"]
    fee = 0.02 * 50_000 * FEE_RATE
    assert fee == pytest.approx(0.55)
    assert book.qty == pytest.approx(0.02)
    assert book.fees_usdt == pytest.approx(fee)
    assert book.equity_usdt == pytest.approx(START_EQUITY_USDT - fee)
    # 1x: position notional equals pre-trade equity, not a larger multiple.
    assert abs(book.qty * 50_000) == pytest.approx(START_EQUITY_USDT)
    # Separate from the spot book.
    assert ex.state.open_positions == {}
    assert ex.state.cash_usdt == pytest.approx(main_cash)

    equity_before_flip = book.equity_usdt
    short_resp = await ex.handle_alert(_alert("short", "dd-short"))
    assert short_resp.ok
    assert short_resp.trade is not None
    assert short_resp.trade.side.value == "sell"
    assert book.qty < 0
    assert abs(book.qty) * 50_000 == pytest.approx(equity_before_flip)
    assert ex.state.open_positions == {}

    flat_resp = await ex.handle_alert(_alert("flat", "dd-flat"))
    assert flat_resp.ok
    assert book.qty == pytest.approx(0.0)
    assert book.avg_entry is None
    assert ex.state.open_positions == {}


@pytest.mark.asyncio
async def test_short_from_flat_uses_full_equity():
    ex = _executor()
    resp = await ex.handle_alert(_alert("short", "dd-short-flat"))
    assert resp.ok
    book = ex.state.strategy_books["btc-dd2h"]
    assert book.qty == pytest.approx(-0.02)
    assert book.equity_usdt == pytest.approx(START_EQUITY_USDT - 0.55)
    assert abs(book.qty) * 50_000 == pytest.approx(START_EQUITY_USDT)


@pytest.mark.asyncio
async def test_side_word_long_is_target():
    ex = _executor()
    alert = TradingViewAlert(
        symbol="BTCUSDT",
        side="long",
        price=50_000,
        alert_id="dd-side-long",
        strategy_id="btc-dd2h",
    )
    resp = await ex.handle_alert(alert)
    assert resp.ok
    assert ex.state.strategy_books["btc-dd2h"].qty > 0


@pytest.mark.asyncio
async def test_legacy_alert_rejected_when_not_in_allowlist():
    ex = _executor(_settings(allowed_strategies=""))
    alert = TradingViewAlert(
        symbol="BTCUSDT",
        side="buy",
        price=50_000,
        alert_id="legacy-bostian",
        strategy_id="bostian-iii-sma-zero",
    )
    resp = await ex.handle_alert(alert)
    assert not resp.ok
    assert resp.status == OrderStatus.REJECTED
    assert resp.message
    assert "ALLOWED_STRATEGIES" in resp.message
    assert "btc-dd2h" not in ex.state.strategy_books
    assert ex.state.open_positions == {}


@pytest.mark.asyncio
async def test_empty_allowlist_rejects_btc_dd2h():
    ex = _executor(_settings(allowed_strategies=""))
    resp = await ex.handle_alert(_alert("long", "dd-closed"))
    assert not resp.ok
    assert "ALLOWED_STRATEGIES" in (resp.message or "")
    assert ex.state.strategy_books == {}


@pytest.mark.asyncio
async def test_allowlist_does_not_admit_legacy_seat():
    ex = _executor(_settings(allowed_strategies="btc-dd2h"))
    alert = TradingViewAlert(
        symbol="ETHUSDT",
        side="buy",
        price=3_000,
        alert_id="legacy-accdist",
        strategy_id="accdist-sma-cross-v1",
    )
    resp = await ex.handle_alert(alert)
    assert not resp.ok
    assert "ALLOWED_STRATEGIES" in (resp.message or "")
    assert ex.state.open_positions == {}


@pytest.mark.asyncio
async def test_spot_buy_rejected_for_btc_dd2h():
    ex = _executor()
    alert = TradingViewAlert(
        symbol="BTCUSDT",
        side="buy",
        price=50_000,
        alert_id="dd-spot-buy",
        strategy_id="btc-dd2h",
    )
    resp = await ex.handle_alert(alert)
    assert not resp.ok
    assert "target" in (resp.message or "")
    assert ex.state.strategy_books == {}
    assert ex.state.open_positions == {}


@pytest.mark.asyncio
async def test_live_mode_never_places_btc_dd2h():
    settings = _settings(
        trading_mode="live",
        webhook_secret="strong-live-secret-not-default",
        binance_api_key="k",
        binance_api_secret="s",
        allowed_strategies="btc-dd2h",
    )
    state = PortfolioState(equity_usdt=10_000, prices={"BTCUSDT": 50_000.0})
    binance = BinanceClient(settings)
    binance.get_account_balances = AsyncMock(return_value={"USDT": 10_000.0})  # type: ignore[method-assign]
    binance.place_market_order = AsyncMock(return_value={"orderId": 1})  # type: ignore[method-assign]
    ex = TradeExecutor(settings, state, IdempotencyStore(), binance=binance)

    resp = await ex.handle_alert(_alert("long", "dd-live"))
    assert not resp.ok
    assert "paper-only" in (resp.message or "")
    binance.place_market_order.assert_not_called()
    binance.get_account_balances.assert_not_called()
    assert state.strategy_books == {}
    assert state.open_positions == {}


@pytest.mark.asyncio
async def test_wrong_symbol_rejected():
    ex = _executor()
    resp = await ex.handle_alert(
        _alert("long", "dd-eth", symbol="ETHUSDT", price=3_000)
    )
    assert not resp.ok
    assert "BTCUSDT" in (resp.message or "")
    assert ex.state.strategy_books == {}


def test_allowed_strategies_default_empty():
    settings = Settings(trading_mode="paper", webhook_secret="change-me", data_dir="")
    assert settings.allowed_strategy_set == set()


def test_book_persists_separately_from_spot_portfolio():
    ex_state = PortfolioState(equity_usdt=10_000, cash_usdt=10_000)
    from app.target_book import new_btc_dd2h_book

    book = new_btc_dd2h_book()
    ex_state.strategy_books["btc-dd2h"] = book
    restored = PortfolioState.from_dict(ex_state.to_dict())
    assert restored.equity_usdt == pytest.approx(10_000)
    assert restored.strategy_books["btc-dd2h"].cash_usdt == pytest.approx(1_000)
    assert "btc-dd2h" not in restored.open_positions
