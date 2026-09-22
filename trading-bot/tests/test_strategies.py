"""Tests for the Strategy registry and paper seat definitions."""

from __future__ import annotations

from app.models import OrderStatus, Side, TradeRecord
from app.strategy_registry import STRATEGY_REGISTRY, get_active_strategies


def test_locked_paper_seats_exist():
    assert "bostian-iii-sma-zero" in STRATEGY_REGISTRY
    assert "accdist-sma-cross-v1" in STRATEGY_REGISTRY


def test_bostian_seat_spec():
    strat = STRATEGY_REGISTRY["bostian-iii-sma-zero"]
    assert strat.symbol == "BTCUSDT"
    assert strat.timeframe == "4h"
    assert "Bostian" in strat.description or "Intraday Intensity" in strat.description
    assert "sma(iii, 21)" in strat.build
    assert "crossover(iiiS, 0)" in strat.entry_signal
    assert "crossunder(iiiS, 0)" in strat.exit_signal
    assert "0" in strat.entry_rule
    assert "0" in strat.exit_rule


def test_accdist_seat_spec():
    strat = STRATEGY_REGISTRY["accdist-sma-cross-v1"]
    assert strat.symbol == "ETHUSDT"
    assert strat.timeframe == "4h"
    assert "Accumulation/Distribution" in strat.description or "ADL" in strat.description
    assert "ta.sma(adl, 50)" in strat.build
    assert "crossover(adl, sig)" in strat.entry_signal
    assert "crossunder(adl, sig)" in strat.exit_signal
    assert "ADL" in strat.entry_rule or "Accumulation/Distribution" in strat.entry_rule
    assert "ADL" in strat.exit_rule or "Accumulation/Distribution" in strat.exit_rule


def test_get_active_strategies_without_trades():
    strats = get_active_strategies()
    ids = [s.strategy_id for s in strats]
    assert "bostian-iii-sma-zero" in ids
    assert "accdist-sma-cross-v1" in ids


def test_get_active_strategies_with_custom_trade():
    custom_trade = TradeRecord(
        alert_id="tv-123",
        symbol="SOLUSDT",
        side=Side.BUY,
        qty=1.5,
        status=OrderStatus.FILLED,
        mode="paper",
        strategy_id="custom-sol-strategy-v1",
    )
    strats = get_active_strategies([custom_trade])
    ids = [s.strategy_id for s in strats]
    assert "bostian-iii-sma-zero" in ids
    assert "accdist-sma-cross-v1" in ids
    assert "custom-sol-strategy-v1" in ids
