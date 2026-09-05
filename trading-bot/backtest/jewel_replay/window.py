"""Calendar window filters for Path B jewel CSV replay."""

from __future__ import annotations

import calendar
from datetime import datetime, timezone
from enum import Enum

from backtest.jewel_replay.csv_loader import JewelBar


class WindowMode(str, Enum):
    ALL = "all"
    SIX_M = "6m"
    BOTH = "both"


def months_before(dt: datetime, months: int) -> datetime:
    """Subtract calendar months, clamping day to the target month length."""
    if months < 0:
        raise ValueError("months must be >= 0")
    y, m = dt.year, dt.month - months
    while m <= 0:
        m += 12
        y -= 1
    day = min(dt.day, calendar.monthrange(y, m)[1])
    return dt.replace(year=y, month=m, day=day)


def window_start_ms(*, end_ms: int, months: int = 6) -> int:
    """Inclusive start timestamp (ms) for a trailing calendar-month window."""
    end = datetime.fromtimestamp(end_ms / 1000.0, tz=timezone.utc)
    start = months_before(end, months)
    return int(start.timestamp() * 1000)


def filter_bars_last_months(
    bars: list[JewelBar],
    *,
    months: int = 6,
) -> list[JewelBar]:
    """
    Keep bars whose open_time_ms is on/after (last_bar_time - months).

    Empty input returns empty. Uses the last bar as the window end (not wall clock),
    so offline CSV ends define the sample.
    """
    if not bars:
        return []
    start_ms = window_start_ms(end_ms=bars[-1].open_time_ms, months=months)
    return [b for b in bars if b.open_time_ms >= start_ms]


def resolve_windows(mode: WindowMode | str) -> list[tuple[str, str]]:
    """
    Map CLI --window to ordered (label, kind) pairs.

    kind is 'all' or '6m'. label is the human report header.
    """
    if isinstance(mode, str):
        mode = WindowMode(mode)
    if mode is WindowMode.ALL:
        return [("full", "all")]
    if mode is WindowMode.SIX_M:
        return [("last_6m", "6m")]
    if mode is WindowMode.BOTH:
        return [("full", "all"), ("last_6m", "6m")]
    raise ValueError(f"Unknown window mode: {mode}")


def apply_window(bars: list[JewelBar], kind: str) -> list[JewelBar]:
    if kind == "all":
        return list(bars)
    if kind == "6m":
        return filter_bars_last_months(bars, months=6)
    raise ValueError(f"Unknown window kind: {kind}")
