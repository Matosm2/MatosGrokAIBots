"""Binance USDT-M fundingRate fetch + cache (signal only; Spot fills elsewhere).

Uses www.binance.com/fapi host (fapi.binance.com is geo-blocked from some regions).
If fetch fails → raise FundingFetchError (callers mark ERROR cell; never invent rates).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import DEFAULT_CACHE_DIR

FUNDING_CACHE_DIR = DEFAULT_CACHE_DIR / "funding"
FUNDING_URL = "https://www.binance.com/fapi/v1/fundingRate"
# Fallback hosts tried in order if primary fails.
FUNDING_URLS: tuple[str, ...] = (
    "https://www.binance.com/fapi/v1/fundingRate",
    "https://fapi.binance.com/fapi/v1/fundingRate",
)


class FundingFetchError(RuntimeError):
    """Raised when Binance USDT-M fundingRate cannot be retrieved."""


@dataclass(frozen=True)
class FundingPrint:
    time_ms: int
    rate: float  # Binance decimal (0.001 == 0.10%)


def _cache_path(symbol: str) -> Path:
    return FUNDING_CACHE_DIR / f"{symbol.upper()}_fundingRate.jsonl"


def _meta_path(symbol: str) -> Path:
    return FUNDING_CACHE_DIR / f"{symbol.upper()}_fundingRate.meta.json"


def _http_get_json(url: str, timeout: float = 30.0) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "MatosGrokAIBots-pathb/fresh-wave-v9"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    data = json.loads(raw)
    if not isinstance(data, list):
        raise FundingFetchError(f"unexpected funding payload type: {type(data).__name__}")
    return data


def fetch_funding_rate_history(
    symbol: str = "BTCUSDT",
    *,
    start_ms: int,
    end_ms: int | None = None,
    limit: int = 1000,
    sleep_s: float = 0.15,
) -> list[FundingPrint]:
    """Paginate Binance USDT-M fundingRate. Raises FundingFetchError on hard failure."""
    end_ms = end_ms or int(datetime.now(timezone.utc).timestamp() * 1000)
    sym = symbol.upper()
    out: list[FundingPrint] = []
    cursor = start_ms
    last_err: Exception | None = None

    while cursor < end_ms:
        batch: list[dict] | None = None
        for base in FUNDING_URLS:
            url = f"{base}?symbol={sym}&startTime={cursor}&endTime={end_ms}&limit={limit}"
            try:
                batch = _http_get_json(url)
                last_err = None
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
                last_err = exc
                continue
            except FundingFetchError as exc:
                last_err = exc
                continue
        if batch is None:
            raise FundingFetchError(
                f"fundingRate fetch blocked/failed for {sym}: {last_err!r}"
            )
        if not batch:
            break
        for row in batch:
            try:
                t = int(row["fundingTime"])
                r = float(row["fundingRate"])
            except (KeyError, TypeError, ValueError) as exc:
                raise FundingFetchError(f"bad funding row: {row!r}") from exc
            out.append(FundingPrint(time_ms=t, rate=r))
        last_t = int(batch[-1]["fundingTime"])
        if len(batch) < limit:
            break
        nxt = last_t + 1
        if nxt <= cursor:
            break
        cursor = nxt
        time.sleep(sleep_s)

    # Dedupe + sort
    seen: set[int] = set()
    uniq: list[FundingPrint] = []
    for p in sorted(out, key=lambda x: x.time_ms):
        if p.time_ms in seen:
            continue
        seen.add(p.time_ms)
        uniq.append(p)
    return uniq


def load_or_fetch_funding(
    symbol: str = "BTCUSDT",
    *,
    years: float = 2.5,
    refresh: bool = False,
) -> list[FundingPrint]:
    """Load cached funding prints or fetch (~years lookback). Never invents rates."""
    FUNDING_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(symbol)
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    start_ms = int(now_ms - years * 365.25 * 24 * 3600 * 1000)

    if path.exists() and not refresh:
        rows: list[FundingPrint] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            rows.append(FundingPrint(time_ms=int(obj["t"]), rate=float(obj["r"])))
        if rows and rows[0].time_ms <= start_ms + 7 * 86_400_000:
            # Cache covers roughly the requested window (allow 7d slack at start)
            return [p for p in rows if p.time_ms >= start_ms]

    prints = fetch_funding_rate_history(symbol, start_ms=start_ms, end_ms=now_ms)
    if not prints:
        raise FundingFetchError(f"empty fundingRate series for {symbol}")

    with path.open("w", encoding="utf-8") as fh:
        for p in prints:
            fh.write(json.dumps({"t": p.time_ms, "r": p.rate}) + "\n")
    _meta_path(symbol).write_text(
        json.dumps(
            {
                "symbol": symbol.upper(),
                "prints": len(prints),
                "start_ms": prints[0].time_ms,
                "end_ms": prints[-1].time_ms,
                "source": FUNDING_URL,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return prints
