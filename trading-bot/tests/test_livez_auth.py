"""Tests for /livez, auth-gated /health, and length-safe secret compare."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app, secrets_equal


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    settings = Settings(
        trading_mode="paper",
        webhook_secret="unit-test-secret-not-default",
        risk_per_trade_pct=2.5,
        max_position_pct=12.0,
        max_open_positions=4,
        max_daily_loss_pct=5.0,
        allowed_symbols="BTCUSDT,ETHUSDT",
        paper_equity_usdt=10_000.0,
        data_dir="",
    )
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_livez_public_no_auth(client: TestClient):
    r = client.get("/livez")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_health_requires_secret(client: TestClient):
    assert client.get("/health").status_code == 401
    bad = client.get("/health", headers={"X-Webhook-Secret": "wrong"})
    assert bad.status_code == 401
    ok = client.get(
        "/health", headers={"X-Webhook-Secret": "unit-test-secret-not-default"}
    )
    assert ok.status_code == 200
    assert ok.json()["status"] == "ok"
    assert ok.json()["trading_mode"] == "paper"


def test_secrets_equal_length_safe():
    assert secrets_equal("abc", "abc") is True
    assert secrets_equal("abc", "abd") is False
    assert secrets_equal("short", "much-longer-secret") is False
    assert secrets_equal("", "x") is False
    assert secrets_equal(None, "x") is False
    assert secrets_equal("x", None) is False
    assert secrets_equal(None, None) is False
