"""Unit tests for risk checks."""

from app.config import Settings
from app.models import Side, TradingViewAlert
from app.risk import PortfolioState, apply_fill, check_risk


def _settings(**overrides) -> Settings:
    base = dict(
        trading_mode="paper",
        risk_per_trade_pct=2.5,
        max_position_pct=12.0,
        max_open_positions=4,
        max_daily_loss_pct=5.0,
        allowed_symbols="BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT",
        paper_equity_usdt=10_000.0,
        data_dir="",
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


def test_daily_loss_circuit_breaker_blocks_buy():
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


def test_daily_loss_halt_allows_sell():
    """HIGH: daily-loss halt must still allow SELL/closes."""
    settings = _settings(max_daily_loss_pct=5.0)
    state = PortfolioState(
        equity_usdt=10_000,
        cash_usdt=4_000,
        open_positions={"BTCUSDT": 0.1},
        avg_entry={"BTCUSDT": 50_000},
        daily_realized_pnl_usdt=-600,
        prices={"BTCUSDT": 50_000},
    )
    alert = TradingViewAlert(
        symbol="BTCUSDT", side="sell", qty_pct=12, price=50_000, alert_id="halt-sell"
    )
    d = check_risk(alert, settings, state)
    assert d.allowed, d.reason
    assert d.sized_qty is not None and d.sized_qty > 0


def test_buy_absolute_qty_trimmed_to_risk_per_trade():
    """MEDIUM: BUY absolute qty capped by RISK_PER_TRADE_PCT then MAX_POSITION_PCT."""
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000, prices={"ETHUSDT": 2_000})
    # 1.0 ETH @ 2000 = 2000 USDT = 20% equity → trim to 2.5% = 250
    alert = TradingViewAlert(symbol="ETHUSDT", side="buy", qty=1.0, price=2_000)
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert d.trimmed == "trimmed_to_risk_per_trade"
    assert abs((d.notional_usdt or 0) - 250.0) < 1e-3


def test_explicit_qty_under_risk_cap_respected():
    settings = _settings()
    state = PortfolioState(equity_usdt=10_000, prices={"ETHUSDT": 2_000})
    # 0.1 ETH @ 2000 = 200 USDT = 2% < 2.5%
    alert = TradingViewAlert(symbol="ETHUSDT", side="buy", qty=0.1, price=2_000)
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert d.sized_qty == 0.1
    assert d.trimmed is None


def test_max_position_pct_caps():
    settings = _settings(max_position_pct=12.0, risk_per_trade_pct=50.0)
    state = PortfolioState(equity_usdt=10_000, prices={"BTCUSDT": 50_000})
    # qty_pct 50 would be 5k but risk trim first to 50%, then max position 12% = 1200
    alert = TradingViewAlert(symbol="BTCUSDT", side="buy", qty_pct=50, price=50_000)
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert d.notional_usdt is not None
    assert d.notional_usdt <= 1200.0 + 1e-6


def test_sell_qty_pct_12_not_truncated_by_risk_per_trade():
    """
    PRIORITY BUG regression: SELL qty_pct 12 must NOT be truncated by
    post-size RISK_PER_TRADE_PCT when alert.qty is None.
    """
    settings = _settings(risk_per_trade_pct=2.5, max_position_pct=12.0)
    # Open long worth ~12% of equity so qty_pct 12 can fully exit
    open_qty = 0.024  # 0.024 * 50_000 = 1_200 = 12% of 10k
    state = PortfolioState(
        equity_usdt=10_000,
        cash_usdt=8_800,
        open_positions={"BTCUSDT": open_qty},
        avg_entry={"BTCUSDT": 50_000},
        prices={"BTCUSDT": 50_000},
    )
    alert = TradingViewAlert(
        symbol="BTCUSDT",
        side="sell",
        qty_pct=12,
        price=50_000,
        alert_id="sell-12-pct",
    )
    d = check_risk(alert, settings, state)
    assert d.allowed, d.reason
    assert d.sized_qty is not None
    # Must be ~0.024 (12%), NOT ~0.005 (2.5% risk cap)
    assert abs(d.sized_qty - open_qty) < 1e-9, (
        f"SELL qty_pct 12 truncated to {d.sized_qty}; expected {open_qty} "
        "(RISK_PER_TRADE_PCT must not apply to sells)"
    )
    assert abs((d.notional_usdt or 0) - 1_200.0) < 1e-3
    assert d.trimmed is None


def test_sell_close_all_full_exit():
    settings = _settings()
    state = PortfolioState(
        equity_usdt=10_000,
        cash_usdt=5_000,
        open_positions={"BTCUSDT": 0.1},
        avg_entry={"BTCUSDT": 50_000},
        prices={"BTCUSDT": 50_000},
    )
    alert = TradingViewAlert(
        symbol="BTCUSDT", side="sell", close_all=True, price=55_000, alert_id="ca"
    )
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert abs((d.sized_qty or 0) - 0.1) < 1e-12


def test_sell_no_naked_short_caps_to_open():
    settings = _settings()
    state = PortfolioState(
        equity_usdt=10_000,
        open_positions={"BTCUSDT": 0.01},
        avg_entry={"BTCUSDT": 50_000},
        prices={"BTCUSDT": 50_000},
    )
    alert = TradingViewAlert(
        symbol="BTCUSDT", side="sell", qty=1.0, price=50_000, alert_id="naked"
    )
    d = check_risk(alert, settings, state)
    assert d.allowed
    assert abs((d.sized_qty or 0) - 0.01) < 1e-12


def test_apply_fill_real_daily_realized_pnl():
    """HIGH: apply_fill must record real realized PnL, not += 0.0."""
    state = PortfolioState(
        equity_usdt=10_000,
        cash_usdt=5_000,
        open_positions={"BTCUSDT": 0.1},
        avg_entry={"BTCUSDT": 50_000},
        prices={"BTCUSDT": 50_000},
    )
    realized = apply_fill(state, "BTCUSDT", Side.SELL, 0.1, 55_000)
    assert abs(realized - 500.0) < 1e-6  # (55k-50k)*0.1
    assert abs(state.daily_realized_pnl_usdt - 500.0) < 1e-6
    assert "BTCUSDT" not in state.open_positions
    assert state.cash_usdt is not None and state.cash_usdt > 5_000
