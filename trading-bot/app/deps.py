"""Shared FastAPI dependencies and auth helpers."""

from __future__ import annotations

import secrets
from typing import Optional

from fastapi import Depends, Header, HTTPException

from app.config import Settings, get_settings
from app.executor import TradeExecutor
from app.risk import PortfolioState

# App-scoped singletons (set in lifespan in main.py)
_state: Optional[PortfolioState] = None
_executor: Optional[TradeExecutor] = None


def set_runtime(state: PortfolioState, executor: TradeExecutor) -> None:
    global _state, _executor
    _state = state
    _executor = executor


def clear_runtime() -> None:
    global _state, _executor
    _state = None
    _executor = None


def get_executor() -> TradeExecutor:
    if _executor is None:
        raise RuntimeError("Executor not initialized")
    return _executor


def get_portfolio() -> PortfolioState:
    if _state is None:
        raise RuntimeError("Portfolio not initialized")
    return _state


def secrets_equal(provided: Optional[str], expected: Optional[str]) -> bool:
    """Length-safe constant-time compare for webhook secrets.

    ``secrets.compare_digest`` on bytes raises ValueError when lengths differ;
    always return False instead of 500ing the request.
    """
    if not provided or not expected:
        return False
    try:
        return secrets.compare_digest(
            provided.encode("utf-8"),
            expected.encode("utf-8"),
        )
    except (TypeError, ValueError):
        return False


def require_webhook_auth(
    settings: Settings = Depends(get_settings),
    x_webhook_secret: Optional[str] = Header(default=None),
) -> None:
    """Auth gate for private endpoints (/health, /trades)."""
    if not secrets_equal(x_webhook_secret, settings.webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid or missing webhook secret")
