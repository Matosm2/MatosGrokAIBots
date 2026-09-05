"""TradingView → Binance Spot FastAPI service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.binance_client import BinanceClient
from app.config import Settings, get_settings
from app.dashboard import router as dashboard_router
from app.deps import (
    clear_runtime,
    get_executor,
    get_portfolio,
    require_webhook_auth,
    secrets_equal,
    set_runtime,
)
from app.executor import TradeExecutor
from app.idempotency import IdempotencyStore
from app.logging_config import log_event, setup_logging
from app.models import HealthResponse, TradeRecord, TradingViewAlert, WebhookResponse
from app.persistence import JsonStore
from app.risk import PortfolioState

logger = logging.getLogger(__name__)

# Re-export for tests / callers that imported from app.main
__all__ = [
    "app",
    "create_app",
    "secrets_equal",
    "get_executor",
    "get_portfolio",
    "require_webhook_auth",
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    setup_logging(settings.log_level)

    data_dir = (settings.data_dir or "").strip()
    store = JsonStore(data_dir) if data_dir else JsonStore("")

    # Load persisted portfolio or start from paper equity
    loaded = store.load("portfolio.json", default=None) if store.enabled else None
    if isinstance(loaded, dict) and loaded:
        state = PortfolioState.from_dict(loaded)
        log_event(logger, "portfolio_loaded", equity=state.equity_usdt)
    else:
        state = PortfolioState(equity_usdt=settings.paper_equity_usdt)

    # Seed default prices for paper so alerts without price still work in tests/demo
    state.prices.setdefault("BTCUSDT", 60_000.0)
    state.prices.setdefault("ETHUSDT", 3_000.0)
    state.prices.setdefault("SOLUSDT", 150.0)
    state.prices.setdefault("BNBUSDT", 500.0)
    state.mark_equity()

    idem = IdempotencyStore(
        ttl_seconds=settings.idempotency_ttl_seconds,
        store=store if store.enabled else None,
    )
    binance = BinanceClient(settings)
    executor = TradeExecutor(
        settings, state, idem, binance, store=store if store.enabled else None
    )
    set_runtime(state, executor)
    log_event(
        logger,
        "startup",
        trading_mode=settings.trading_mode,
        allowed_symbols=",".join(sorted(settings.allowed_symbol_set)),
        data_dir=data_dir or "(memory)",
        insecure_webhook=settings.insecure_webhook_secret,
    )
    if settings.insecure_webhook_secret and settings.is_paper:
        logger.warning(
            "WEBHOOK_SECRET is a default/insecure value — fine for local paper; "
            "live mode and durable deploy (absolute DATA_DIR or "
            "PAPER_REQUIRE_STRONG_SECRET) refuse to start until you set a strong secret."
        )
    try:
        yield
    finally:
        await binance.aclose()
        clear_runtime()
        log_event(logger, "shutdown")


app = FastAPI(
    title="TradingView → Binance Bot",
    version="1.2.0",
    description="Webhook bridge from TradingView alerts to Binance Spot (paper by default).",
    lifespan=lifespan,
)
# Trust X-Forwarded-Proto / X-Forwarded-For from Railway (and similar) TLS terminators
# so dashboard session cookies get Secure= correctly when the app sees http upstream.
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.include_router(dashboard_router)


@app.get("/livez")
async def livez() -> dict[str, str]:
    """Unauthenticated liveness probe for Docker/K8s healthchecks."""
    return {"status": "ok"}


@app.get("/health", response_model=HealthResponse)
async def health(
    settings: Settings = Depends(get_settings),
    state: PortfolioState = Depends(get_portfolio),
    _: None = Depends(require_webhook_auth),
) -> HealthResponse:
    state.reset_day_if_needed()
    state.mark_equity()
    return HealthResponse(
        status="ok",
        trading_mode=settings.trading_mode,
        allowed_symbols=sorted(settings.allowed_symbol_set),
        open_positions=state.open_count,
        daily_pnl_pct=round(state.daily_pnl_pct, 4),
        equity_usdt=round(state.equity_usdt, 4),
    )


@app.get("/trades", response_model=list[TradeRecord])
async def recent_trades(
    limit: int = 50,
    executor: TradeExecutor = Depends(get_executor),
    _: None = Depends(require_webhook_auth),
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
    header_ok = secrets_equal(x_webhook_secret, settings.webhook_secret)
    body_ok = secrets_equal(alert.secret, settings.webhook_secret)
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
