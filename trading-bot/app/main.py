"""TradingView → Binance Spot FastAPI service."""

from __future__ import annotations

import logging
import secrets
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
from app.persistence import JsonStore
from app.risk import PortfolioState

logger = logging.getLogger(__name__)

# App-scoped singletons (set in lifespan)
_state: Optional[PortfolioState] = None
_executor: Optional[TradeExecutor] = None
_binance: Optional[BinanceClient] = None
_store: Optional[JsonStore] = None


def get_executor() -> TradeExecutor:
    if _executor is None:
        raise RuntimeError("Executor not initialized")
    return _executor


def get_portfolio() -> PortfolioState:
    if _state is None:
        raise RuntimeError("Portfolio not initialized")
    return _state


def require_webhook_auth(
    settings: Settings = Depends(get_settings),
    x_webhook_secret: Optional[str] = Header(default=None),
) -> None:
    """Auth gate for private endpoints (/health, /trades)."""
    provided = x_webhook_secret or ""
    expected = settings.webhook_secret or ""
    if not expected or not secrets.compare_digest(provided, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing webhook secret")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global _state, _executor, _binance, _store
    settings = get_settings()
    setup_logging(settings.log_level)

    data_dir = (settings.data_dir or "").strip()
    _store = JsonStore(data_dir) if data_dir else JsonStore("")

    # Load persisted portfolio or start from paper equity
    loaded = _store.load("portfolio.json", default=None) if _store.enabled else None
    if isinstance(loaded, dict) and loaded:
        _state = PortfolioState.from_dict(loaded)
        log_event(logger, "portfolio_loaded", equity=_state.equity_usdt)
    else:
        _state = PortfolioState(equity_usdt=settings.paper_equity_usdt)

    # Seed default prices for paper so alerts without price still work in tests/demo
    _state.prices.setdefault("BTCUSDT", 60_000.0)
    _state.prices.setdefault("ETHUSDT", 3_000.0)
    _state.prices.setdefault("SOLUSDT", 150.0)
    _state.prices.setdefault("BNBUSDT", 500.0)
    _state.mark_equity()

    idem = IdempotencyStore(
        ttl_seconds=settings.idempotency_ttl_seconds,
        store=_store if _store.enabled else None,
    )
    _binance = BinanceClient(settings)
    _executor = TradeExecutor(
        settings, _state, idem, _binance, store=_store if _store.enabled else None
    )
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
            "live mode will refuse to start until you set a strong secret."
        )
    yield
    if _binance:
        await _binance.aclose()
    log_event(logger, "shutdown")


app = FastAPI(
    title="TradingView → Binance Bot",
    version="1.1.0",
    description="Webhook bridge from TradingView alerts to Binance Spot (paper by default).",
    lifespan=lifespan,
)


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
    header_ok = (
        bool(x_webhook_secret)
        and secrets.compare_digest(x_webhook_secret, settings.webhook_secret)
    )
    body_ok = (
        bool(alert.secret)
        and secrets.compare_digest(alert.secret, settings.webhook_secret)
    )
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
