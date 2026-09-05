"""Fetch and cache public Binance Spot OHLCV (no auth).

Uses data-api.binance.vision (works from restricted regions where api.binance.com may 451).
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import httpx

BINANCE_KLINES = "https://data-api.binance.vision/api/v3/klines"
DEFAULT_CACHE_DIR = Path(__file__).resolve().parent / "cache"


@dataclass(frozen=True)
class Bar:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time_ms: int

    @property
    def open_time(self) -> datetime:
        return datetime.fromtimestamp(self.open_time_ms / 1000, tz=timezone.utc)


def _cache_path(cache_dir: Path, symbol: str, interval: str) -> Path:
    return cache_dir / f"{symbol}_{interval}.csv"


def _meta_path(cache_dir: Path, symbol: str, interval: str) -> Path:
    return cache_dir / f"{symbol}_{interval}.meta.json"


def bars_to_csv(path: Path, bars: list[Bar]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            ["open_time_ms", "open", "high", "low", "close", "volume", "close_time_ms"]
        )
        for b in bars:
            w.writerow(
                [
                    b.open_time_ms,
                    b.open,
                    b.high,
                    b.low,
                    b.close,
                    b.volume,
                    b.close_time_ms,
                ]
            )


def bars_from_csv(path: Path) -> list[Bar]:
    bars: list[Bar] = []
    with path.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            bars.append(
                Bar(
                    open_time_ms=int(row["open_time_ms"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                    close_time_ms=int(row["close_time_ms"]),
                )
            )
    return bars


def fetch_klines(
    symbol: str,
    interval: str = "1h",
    *,
    start_ms: int | None = None,
    end_ms: int | None = None,
    limit: int = 1000,
    client: httpx.Client | None = None,
) -> list[Bar]:
    """Paginate Binance public klines until end or no more data."""
    own = client is None
    client = client or httpx.Client(timeout=30.0)
    bars: list[Bar] = []
    cursor = start_ms
    try:
        while True:
            params: dict[str, str | int] = {
                "symbol": symbol.upper(),
                "interval": interval,
                "limit": min(limit, 1000),
            }
            if cursor is not None:
                params["startTime"] = cursor
            if end_ms is not None:
                params["endTime"] = end_ms
            resp = client.get(BINANCE_KLINES, params=params)
            resp.raise_for_status()
            rows = resp.json()
            if not rows:
                break
            for row in rows:
                bars.append(
                    Bar(
                        open_time_ms=int(row[0]),
                        open=float(row[1]),
                        high=float(row[2]),
                        low=float(row[3]),
                        close=float(row[4]),
                        volume=float(row[5]),
                        close_time_ms=int(row[6]),
                    )
                )
            last_open = int(rows[-1][0])
            # next page starts after last open
            next_cursor = last_open + 1
            if cursor is not None and next_cursor <= cursor:
                break
            cursor = next_cursor
            if len(rows) < min(limit, 1000):
                break
            if end_ms is not None and last_open >= end_ms:
                break
            time.sleep(0.05)  # be polite
    finally:
        if own:
            client.close()

    # de-dupe by open_time
    seen: dict[int, Bar] = {}
    for b in bars:
        seen[b.open_time_ms] = b
    return [seen[k] for k in sorted(seen)]


def load_or_fetch(
    symbol: str,
    interval: str = "1h",
    *,
    years: float = 2.0,
    cache_dir: Path | None = None,
    refresh: bool = False,
) -> list[Bar]:
    """
    Load cached CSV or fetch ~`years` of history ending now.
    Cache under backtest/cache/ (gitignored when large).
    """
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    path = _cache_path(cache_dir, symbol, interval)
    meta_p = _meta_path(cache_dir, symbol, interval)

    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    start_ms = now_ms - int(years * 365.25 * 24 * 3600 * 1000)

    if path.exists() and not refresh:
        bars = bars_from_csv(path)
        if bars and bars[0].open_time_ms <= start_ms + 7 * 24 * 3600 * 1000:
            # extend if stale (missing recent bars)
            last = bars[-1].open_time_ms
            if now_ms - last > 2 * 3600 * 1000:
                extra = fetch_klines(symbol, interval, start_ms=last + 1, end_ms=now_ms)
                if extra:
                    by_t = {b.open_time_ms: b for b in bars}
                    for b in extra:
                        by_t[b.open_time_ms] = b
                    bars = [by_t[k] for k in sorted(by_t)]
                    bars_to_csv(path, bars)
                    meta_p.write_text(
                        json.dumps(
                            {
                                "symbol": symbol,
                                "interval": interval,
                                "bars": len(bars),
                                "fetched_at": datetime.now(timezone.utc).isoformat(),
                            },
                            indent=2,
                        )
                    )
            return bars

    bars = fetch_klines(symbol, interval, start_ms=start_ms, end_ms=now_ms)
    bars_to_csv(path, bars)
    meta_p.write_text(
        json.dumps(
            {
                "symbol": symbol,
                "interval": interval,
                "bars": len(bars),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
    )
    return bars
