"""Fail-closed live config + LOT_SIZE helpers."""

import pytest
from pydantic import ValidationError

from app.binance_client import BinanceClient, floor_to_step
from app.config import Settings


def test_live_rejects_default_webhook_secret():
    with pytest.raises(ValidationError):
        Settings(
            trading_mode="live",
            webhook_secret="change-me",
            binance_api_key="k",
            binance_api_secret="s",
        )


def test_live_rejects_missing_keys():
    with pytest.raises(ValidationError):
        Settings(
            trading_mode="live",
            webhook_secret="strong-live-secret-xyz",
            binance_api_key="",
            binance_api_secret="",
        )


def test_paper_allows_default_secret():
    s = Settings(trading_mode="paper", webhook_secret="change-me", data_dir="")
    assert s.is_paper
    assert s.insecure_webhook_secret


def test_round_step():
    assert floor_to_step(0.01234, 0.001) == pytest.approx(0.012)
    assert floor_to_step(1.999, 0.1) == pytest.approx(1.9)
    assert BinanceClient.round_step(0.01234, 0.001) == pytest.approx(0.012)
