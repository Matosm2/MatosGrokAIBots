"""Unit tests for risk checks."""

from app.config import Settings
from app.models import Side, TradingViewAlert
from app.risk import PortfolioState, check_risk


def _settings(**overrides) -> Settings:
    base = dict(
        trading_mode="paper",
        risk_per_trade_pct=2.5,
        max_position_pct=12.0,
        max_open_positions=4,
        max_daily_loss_pct=5.0,
        allowed_symbols="BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT",
        paper_equity_usdt=10_000.0,
    )
    base.update(overrides)
    return Settings(**base)


def test_rejects_disallowed_symbol():
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000, prices={"XRPUSDT": 0.5})
    alert = TradingViewAlert(symbol="XRPUSDT", side="buy", price=0.5)
    d = check_risk(alert, settings, state)
    assert not d.allowed
    assert "ALLOWED_SYMBOLS" in d.reason


def test_rejects_missing_price():
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000)
    alert = TradingViewAlert(symbol="BTCUSDT", side="buy")
    d = check_risk(alert, settings, state)
    assert not d.allowed
    assert "price" in d.reason.lower()


def test_allows_buy_with_default_risk_pct():
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000, prices={"BTCUSDT": 50_000})
    alert = TradingViewAlert(symbol="BTCUSDT", side="buy", price=50_000)
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert d.sized_qty is not None
    # 2.5% of 10k = 250 USDT / 50000 = 0.005 BTC
    assert abs(d.sized_qty - 0.005) < 1e-9
    assert abs((d.notional_usdt or 0) - 250.0) < 1e-6


def test_max_open_positions():
    settings = _settings(max_open_positions=2)
    state = PortfolioState(
        equity_usdt=10_000,
        open_positions={"BTCUSDT": 0.01, "ETHUSDT": 0.5},
        prices={"BTCUSDT": 50_000, "ETHUSDT": 3_000, "SOLUSDT": 100},
    )
    alert = TradingViewAlert(symbol="SOLUSDT", side="buy", price=100)
    d = check_risk(alert, settings, state)
    assert not d.allowed
    assert "Max open positions" in d.reason


def test_sell_without_position_rejected():
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000, prices={"BTCUSDT": 50_000})
    alert = TradingViewAlert(symbol="BTCUSDT", side="sell", price=50_000)
    d = check_risk(alert, settings, state)
    assert not d.allowed
    assert "No open long" in d.reason


def test_daily_loss_circuit_breaker():
    settings = _settings(max_daily_loss_pct=5.0)
    state = PortfolioState(
        equity_usdt=10_000,
        daily_realized_pnl_usdt=-600,  # -6%
        prices={"BTCUSDT": 50_000},
    )
    alert = TradingViewAlert(symbol="BTCUSDT", side="buy", price=50_000)
    d = check_risk(alert, settings, state)
    assert not d.allowed
    assert "Daily loss" in d.reason


def test_explicit_qty_respected():
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000, prices={"ETHUSDT": 2_000})
    alert = TradingViewAlert(symbol="ETHUSDT", side="buy", qty=0.1, price=2_000)
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert d.sized_qty == 0.1


def test_max_position_pct_caps():
    settings = _settings(max_position_pct=12.0, risk_per_trade_pct=50.0)
    state = PortfolioState(equity_usdt=10_000, prices={"BTCUSDT": 50_000})
    # qty_pct 50 would be 5k but max position is 12% = 1200
    alert = TradingViewAlert(symbol="BTCUSDT", side="buy", qty_pct=50, price=50_000)
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert d.notional_usdt is not None
    assert d.notional_usdt <= 1200.0 + 1e-6
