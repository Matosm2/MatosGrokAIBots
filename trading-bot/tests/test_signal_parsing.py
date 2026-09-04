"""Unit tests for TradingView signal parsing/validation."""

import pytest
from pydantic import ValidationError

from app.models import Side, TradingViewAlert


def test_parse_minimal_buy():
    alert = TradingViewAlert(symbol="btcusdt", side="BUY")
    assert alert.symbol == "BTCUSDT"
    assert alert.side == Side.BUY
    assert alert.alert_id is not None
    assert alert.qty is None
    assert alert.qty_pct is None


def test_parse_with_qty():
    alert = TradingViewAlert(symbol="ETH/USDT", side="sell", qty=0.5, strategy_id="rsi-cross")
    assert alert.symbol == "ETHUSDT"
    assert alert.side == Side.SELL
    assert alert.qty == 0.5
    assert alert.strategy_id == "rsi-cross"


def test_parse_with_qty_pct():
    alert = TradingViewAlert(symbol="SOLUSDT", side="buy", qty_pct=2.5)
    assert alert.qty_pct == 2.5


def test_reject_both_qty_and_pct():
    with pytest.raises(ValidationError):
        TradingViewAlert(symbol="BTCUSDT", side="buy", qty=0.01, qty_pct=5)


def test_reject_invalid_side():
    with pytest.raises(ValidationError):
        TradingViewAlert(symbol="BTCUSDT", side="hold")


def test_reject_negative_qty():
    with pytest.raises(ValidationError):
        TradingViewAlert(symbol="BTCUSDT", side="buy", qty=-1)


def test_normalize_hyphen_symbol():
    alert = TradingViewAlert(symbol="bnb-usdt", side="buy")
    assert alert.symbol == "BNBUSDT"


def test_alert_id_preserved():
    alert = TradingViewAlert(symbol="BTCUSDT", side="buy", alert_id="tv-fixed-123")
    assert alert.alert_id == "tv-fixed-123"
