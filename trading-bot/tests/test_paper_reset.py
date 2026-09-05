"""Paper-only portfolio reset endpoint."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret-paper-reset-xyz")
    monkeypatch.setenv("TRADING_MODE", "paper")
    monkeypatch.setenv("PAPER_EQUITY_USDT", "1000")
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    # Reload settings/app
    from app.config import get_settings
    get_settings.cache_clear()
    from app.main import app
    with TestClient(app) as c:
        yield c
    get_settings.cache_clear()


def test_paper_reset_sets_equity(client, tmp_path):
    # Simulate stale 10k book
    from app.deps import get_portfolio, get_executor
    state = get_portfolio()
    state.equity_usdt = 10004.0
    state.cash_usdt = 10004.0
    state.open_positions["BTCUSDT"] = 0.01
    state.avg_entry["BTCUSDT"] = 60000.0
    exe = get_executor()
    if exe.store:
        exe.store.save("portfolio.json", state.to_dict())

    r = client.post("/paper/reset", headers={"X-Webhook-Secret": "test-secret-paper-reset-xyz"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["equity_usdt"] == 1000.0
    assert body["open_positions"] == 0
    state2 = get_portfolio()
    assert state2.equity_usdt == 1000.0
    assert state2.open_count == 0
    saved = (tmp_path / "portfolio.json").read_text()
    assert "1000" in saved


def test_paper_reset_requires_auth(client):
    r = client.post("/paper/reset")
    assert r.status_code == 401
