"""TradingView → Binance Spot FastAPI service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.binance_client import BinanceClient
from app.config import Settings, get_settings
from app.executor import TradeExecutor
from app.idempotency import IdempotencyStore
from app.logging_config import log_event, setup_logging
from app.models import HealthResponse, TradeRecord, TradingViewAlert, WebhookResponse
from app.risk import PortfolioState

logger = logging.getLogger(__name__)

# App-scoped singletons (set in lifespan)
_state: Optional[PortfolioState] = None
_executor: Optional[TradeExecutor] = None
_binance: Optional[BinanceClient] = None


def get_executor() -> TradeExecutor:
    if _executor is None:
        raise RuntimeError("Executor not initialized")
    return _executor


def get_portfolio() -> PortfolioState:
    if _state is None:
        raise RuntimeError("Portfolio not initialized")
    return _state


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global _state, _executor, _binance
    settings = get_settings()
    setup_logging(settings.log_level)
    _state = PortfolioState(equity_usdt=settings.paper_equity_usdt)
    # Seed default prices for paper so alerts without price still work in tests/demo
    _state.prices.update(
        {
            "BTCUSDT": 60_000.0,
            "ETHUSDT": 3_000.0,
            "SOLUSDT": 150.0,
            "BNBUSDT": 500.0,
        }
    )
    idem = IdempotencyStore(ttl_seconds=settings.idempotency_ttl_seconds)
    _binance = BinanceClient(settings)
    _executor = TradeExecutor(settings, _state, idem, _binance)
    log_event(
        logger,
        "startup",
        trading_mode=settings.trading_mode,
        allowed_symbols=",".join(sorted(settings.allowed_symbol_set)),
    )
    yield
    if _binance:
        await _binance.aclose()
    log_event(logger, "shutdown")


app = FastAPI(
    title="TradingView → Binance Bot",
    version="1.0.0",
    description="Webhook bridge from TradingView alerts to Binance Spot (paper by default).",
    lifespan=lifespan,
)


def verify_secret(
    request: Request,
    settings: Settings = Depends(get_settings),
    x_webhook_secret: Optional[str] = Header(default=None),
) -> None:
    # Secret may arrive as header or body field (checked later in handler)
    if x_webhook_secret and x_webhook_secret == settings.webhook_secret:
        return
    # Allow missing header; body secret checked in webhook handler
    request.state.header_secret_ok = bool(
        x_webhook_secret and x_webhook_secret == settings.webhook_secret
    )


@app.get("/health", response_model=HealthResponse)
async def health(
    settings: Settings = Depends(get_settings),
    state: PortfolioState = Depends(get_portfolio),
) -> HealthResponse:
    state.reset_day_if_needed()
    return HealthResponse(
        status="ok",
        trading_mode=settings.trading_mode,
        allowed_symbols=sorted(settings.allowed_symbol_set),
        open_positions=state.open_count,
        daily_pnl_pct=round(state.daily_pnl_pct, 4),
    )


@app.get("/trades", response_model=list[TradeRecord])
async def recent_trades(
    limit: int = 50,
    executor: TradeExecutor = Depends(get_executor),
) -> list[TradeRecord]:
    limit = max(1, min(limit, 200))
    return list(executor.recent)[:limit]


@app.post("/webhook/tradingview", response_model=WebhookResponse)
async def tradingview_webhook(
    alert: TradingViewAlert,
    request: Request,
    settings: Settings = Depends(get_settings),
    executor: TradeExecutor = Depends(get_executor),
    x_webhook_secret: Optional[str] = Header(default=None),
) -> WebhookResponse:
    header_ok = x_webhook_secret == settings.webhook_secret if x_webhook_secret else False
    body_ok = alert.secret == settings.webhook_secret if alert.secret else False
    if not (header_ok or body_ok):
        log_event(logger, "auth_failed", path=str(request.url.path))
        raise HTTPException(status_code=401, detail="Invalid or missing webhook secret")

    # Strip secret from further processing logs
    alert.secret = None
    return await executor.handle_alert(alert)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception) -> JSONResponse:
    log_event(logger, "unhandled_error", error=str(exc), path=str(request.url.path))
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def create_app() -> FastAPI:
    """Factory for tests."""
    return app
