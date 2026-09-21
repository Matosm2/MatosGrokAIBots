"""Data loading and resampling utilities for Stage-23 Chande Kroll optimize."""

from __future__ import annotations

from pathlib import Path

from backtest.data import DEFAULT_CACHE_DIR, Bar, load_or_fetch


def get_bars_for_timeframe(
    symbol: str,
    interval: str = "1h",
    *,
    years: float = 2.0,
    cache_dir: Path | None = None,
    refresh: bool = False,
) -> list[Bar]:
    """Fetch or load bars for symbol and interval (supports '1h' and '4h')."""
    return load_or_fetch(
        symbol,
        interval,
        years=years,
        cache_dir=cache_dir or DEFAULT_CACHE_DIR,
        refresh=refresh,
    )


def filter_last_months(bars: list[Bar], months: float = 6.0) -> list[Bar]:
    """Filter bars to the most recent `months` window (~30.4375 days/month)."""
    if not bars:
        return []
    end_ms = bars[-1].close_time_ms
    start_ms = end_ms - int(months * 30.4375 * 24 * 3600 * 1000)
    return [b for b in bars if b.open_time_ms >= start_ms]
