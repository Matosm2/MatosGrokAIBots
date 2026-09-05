"""Tests for dashboard login session cookie and HTML routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.dashboard import COOKIE_NAME, LOGIN_RATE_LIMIT_MAX, get_login_rate_limiter, session_token
from app.main import app


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
    get_login_rate_limiter().reset()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    get_login_rate_limiter().reset()


def test_dashboard_shows_login_without_cookie(client: TestClient):
    r = client.get("/dashboard")
    assert r.status_code == 200
    assert "Webhook secret" in r.text
    assert "Sign in" in r.text


def test_dashboard_login_rejects_bad_secret(client: TestClient):
    r = client.post("/dashboard/login", data={"secret": "wrong"}, follow_redirects=False)
    assert r.status_code == 401
    assert "Invalid webhook secret" in r.text
    assert COOKIE_NAME not in r.cookies


def test_dashboard_login_sets_cookie_and_shows_data(client: TestClient):
    r = client.post(
        "/dashboard/login",
        data={"secret": "unit-test-secret-not-default"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers.get("location") == "/dashboard"
    assert COOKIE_NAME in r.cookies
    token = r.cookies[COOKIE_NAME]
    assert token == session_token("unit-test-secret-not-default")

    dash = client.get("/dashboard")
    assert dash.status_code == 200
    assert "Equity" in dash.text
    assert "paper" in dash.text.lower()
    assert "Trade log" in dash.text
    assert "Open positions" in dash.text
    assert "Last alert" in dash.text
    assert "unit-test-secret-not-default" not in dash.text


def test_dashboard_logout_clears_session(client: TestClient):
    client.post("/dashboard/login", data={"secret": "unit-test-secret-not-default"})
    assert "Equity" in client.get("/dashboard").text

    out = client.post("/dashboard/logout", follow_redirects=False)
    assert out.status_code == 303
    again = client.get("/dashboard")
    assert "Sign in" in again.text


def test_dashboard_rejects_forged_cookie(client: TestClient):
    client.cookies.set(COOKIE_NAME, "deadbeef" * 8)
    r = client.get("/dashboard")
    assert r.status_code == 200
    assert "Sign in" in r.text


def _set_cookie_header(response) -> str | None:
    """Return Set-Cookie header value for dashboard_session if present."""
    # httpx/starlette may expose multiple set-cookie headers
    for key, value in response.headers.multi_items():
        if key.lower() == "set-cookie" and value.startswith(f"{COOKIE_NAME}="):
            return value
    raw = response.headers.get("set-cookie")
    if raw and raw.startswith(f"{COOKIE_NAME}="):
        return raw
    return None


def test_dashboard_login_secure_cookie_with_forwarded_proto(client: TestClient):
    """ProxyHeadersMiddleware + X-Forwarded-Proto=https => Secure cookie (Railway)."""
    r = client.post(
        "/dashboard/login",
        data={"secret": "unit-test-secret-not-default"},
        headers={"X-Forwarded-Proto": "https", "X-Forwarded-For": "203.0.113.10"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    set_cookie = _set_cookie_header(r)
    assert set_cookie is not None
    assert "secure" in set_cookie.lower()


def test_dashboard_login_rate_limited(client: TestClient):
    for _ in range(LOGIN_RATE_LIMIT_MAX):
        r = client.post("/dashboard/login", data={"secret": "wrong"}, follow_redirects=False)
        assert r.status_code == 401
    blocked = client.post("/dashboard/login", data={"secret": "wrong"}, follow_redirects=False)
    assert blocked.status_code == 429
    assert "Too many login attempts" in blocked.text
    # Even a correct secret is blocked while limited
    still = client.post(
        "/dashboard/login",
        data={"secret": "unit-test-secret-not-default"},
        follow_redirects=False,
    )
    assert still.status_code == 429
