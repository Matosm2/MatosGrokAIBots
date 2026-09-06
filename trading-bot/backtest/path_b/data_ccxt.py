"""Owned Binance Spot OHLCV via ccxt (no TV/Claude CSV).

Uses data-api.binance.vision (ccxt urls override) so restricted regions work.
Caches to backtest/cache/ in the same CSV schema as backtest.data.
Falls back to backtest.data.fetch_klines if ccxt cannot load markets.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import ccxt

from backtest.data import (
    DEFAULT_CACHE_DIR,
    Bar,
    bars_from_csv,
    bars_to_csv,
    fetch_klines,
)

def _cache_path(cache_dir: Path, symbol: str, interval: str) -> Path:
    return cache_dir / f"{symbol}_{interval}.csv"


def _meta_path(cache_dir: Path, symbol: str, interval: str) -> Path:
    return cache_dir / f"{symbol}_{interval}.meta.json"


def _exchange() -> ccxt.binance:
    """Binance Spot via data-api.binance.vision (451-safe)."""
    ex = ccxt.binance(
        {
            "enableRateLimit": True,
            "options": {"defaultType": "spot"},
        }
    )
    # Restricted-location workaround (same host as backtest.data)
    vision = "https://data-api.binance.vision"
    ex.urls["api"] = {
        "public": f"{vision}/api/v3",
        "private": f"{vision}/api/v3",
        "v1": f"{vision}/api/v1",
        "v3": f"{vision}/api/v3",
        "publicUrl": f"{vision}/api/v3",
    }
    # Newer ccxt uses nested sapi/etc — patch hostname
    try:
        ex.hostname = "data-api.binance.vision"
    except Exception:
        pass
    return ex


def _to_market(symbol: str) -> str:
    s = symbol.upper()
    if "/" in s:
        return s
    if s.endswith("USDT"):
        return f"{s[:-4]}/USDT"
    return s


def fetch_ohlcv_ccxt(
    symbol: str,
    timeframe: str = "1d",
    *,
    start_ms: int | None = None,
    end_ms: int | None = None,
    limit: int = 1000,
) -> list[Bar]:
    """Paginate Binance Spot OHLCV through ccxt (vision host)."""
    market = _to_market(symbol)
    try:
        ex = _exchange()
        # Avoid full exchangeInfo when possible — set markets manually for BTC/ETH
        if market in ("BTC/USDT", "ETH/USDT"):
            base = market.split("/")[0]
            mkt = {
                "id": f"{base}USDT",
                "symbol": market,
                "base": base,
                "quote": "USDT",
                "baseId": base,
                "quoteId": "USDT",
                "active": True,
                "spot": True,
                "swap": False,
                "future": False,
                "option": False,
                "type": "spot",
                "spot": True,
                "margin": False,
                "contract": False,
                "inverse": False,
                "linear": None,
                "precision": {"amount": 8, "price": 8, "cost": 8},
                "limits": {"amount": {}, "price": {}, "cost": {}},
                "info": {},
                "percentage": True,
                "tierBased": False,
            }
            ex.markets = {market: mkt}
            ex.markets_by_id = {f"{base}USDT": [mkt]}
            ex.symbols = [market]
            ex.ids = [f"{base}USDT"]
        since = start_ms
        bars: list[Bar] = []
        while True:
            batch = ex.fetch_ohlcv(
                market, timeframe=timeframe, since=since, limit=limit
            )
            if not batch:
                break
            for row in batch:
                ts, o, h, l, c, v = row
                if end_ms is not None and int(ts) > end_ms:
                    continue
                bars.append(
                    Bar(
                        open_time_ms=int(ts),
                        open=float(o),
                        high=float(h),
                        low=float(l),
                        close=float(c),
                        volume=float(v),
                        close_time_ms=int(ts) + 1,
                    )
                )
            last_ts = int(batch[-1][0])
            next_since = last_ts + 1
            if since is not None and next_since <= since:
                break
            since = next_since
            if len(batch) < limit:
                break
            if end_ms is not None and last_ts >= end_ms:
                break
        seen: dict[int, Bar] = {}
        for b in bars:
            if end_ms is not None and b.open_time_ms > end_ms:
                continue
            seen[b.open_time_ms] = b
        out = [seen[k] for k in sorted(seen)]
        if out:
            return out
    except Exception as exc:  # noqa: BLE001
        print(f"[data_ccxt] ccxt path failed ({exc!r}); fallback fetch_klines", flush=True)

    # Fallback: owned httpx Binance vision klines (same source family)
    sym = symbol.upper().replace("/", "")
    return fetch_klines(sym, timeframe, start_ms=start_ms, end_ms=end_ms, limit=limit)


def load_or_fetch_ccxt(
    symbol: str,
    interval: str = "1d",
    *,
    years: float = 2.5,
    cache_dir: Path | None = None,
    refresh: bool = False,
) -> list[Bar]:
    """Load cache or fetch ~years of Binance Spot via ccxt (vision)."""
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    sym = symbol.upper().replace("/", "")
    path = _cache_path(cache_dir, sym, interval)
    meta_p = _meta_path(cache_dir, sym, interval)
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    start_ms = now_ms - int(years * 365.25 * 24 * 3600 * 1000)

    if path.exists() and not refresh:
        bars = bars_from_csv(path)
        if bars and bars[0].open_time_ms <= start_ms + 7 * 24 * 3600 * 1000:
            last = bars[-1].open_time_ms
            if now_ms - last > 2 * 3600 * 1000:
                extra = fetch_ohlcv_ccxt(
                    sym, interval, start_ms=last + 1, end_ms=now_ms
                )
                if extra:
                    by_t = {b.open_time_ms: b for b in bars}
                    for b in extra:
                        by_t[b.open_time_ms] = b
                    bars = [by_t[k] for k in sorted(by_t)]
                    bars_to_csv(path, bars)
                    meta_p.write_text(
                        json.dumps(
                            {
                                "symbol": sym,
                                "interval": interval,
                                "bars": len(bars),
                                "source": "ccxt:binance/vision",
                                "fetched_at": datetime.now(timezone.utc).isoformat(),
                            },
                            indent=2,
                        )
                    )
            return bars

    bars = fetch_ohlcv_ccxt(sym, interval, start_ms=start_ms, end_ms=now_ms)
    bars_to_csv(path, bars)
    meta_p.write_text(
        json.dumps(
            {
                "symbol": sym,
                "interval": interval,
                "bars": len(bars),
                "source": "ccxt:binance/vision",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
    )
    return bars
