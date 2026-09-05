"""Tests for LOT_SIZE rounding and idempotency claim/abort."""

import pytest

from app.binance_client import floor_to_step, SymbolFilters, BinanceClient
from app.config import Settings
from app.idempotency import ConcurrentClaimError, IdempotencyStore
from app.persistence import JsonStore


def test_floor_to_step():
    assert floor_to_step(0.012345, 0.001) == pytest.approx(0.012)
    assert floor_to_step(1.999, 0.1) == pytest.approx(1.9)


def test_apply_lot_filters_min_notional():
    settings = Settings(
        trading_mode="paper",
        webhook_secret="unit-test-secret-not-default",
        data_dir="",
    )
    client = BinanceClient(settings)
    filt = SymbolFilters(step_size=0.001, min_qty=0.001, min_notional=10.0)
    with pytest.raises(ValueError, match="minNotional"):
        client.apply_lot_filters(0.001, 100.0, filt)  # notional 0.1
    adj = client.apply_lot_filters(0.1234, 100.0, filt)
    assert adj == pytest.approx(0.123)


def test_claim_commit_abort(tmp_path):
    store = JsonStore(tmp_path)
    idem = IdempotencyStore(ttl_seconds=60, store=store)
    assert idem.claim("a1") is None
    with pytest.raises(ConcurrentClaimError):
        idem.claim("a1")
    idem.abort("a1")
    assert idem.claim("a1") is None
    idem.commit("a1", "trade-1")
    assert idem.seen("a1") == "trade-1"
    assert idem.claim("a1") == "trade-1"

    # Persist + reload
    idem2 = IdempotencyStore(ttl_seconds=60, store=store)
    assert idem2.seen("a1") == "trade-1"


def test_round_step_classmethod():
    assert BinanceClient.round_step(0.01234, 0.001) == pytest.approx(0.012)
