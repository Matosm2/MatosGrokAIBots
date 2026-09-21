"""Chande Kroll Stop indicators matching Pine Script ta.* semantics.

Build definition:
  atr = ta.atr(p)  (Wilder's smoothed ATR, RMA)
  highStop = ta.highest(high, p) - x * atr
  lowStop = ta.lowest(low, p) + x * atr
  stopShort = ta.highest(highStop, q)
  stopLong = ta.lowest(lowStop, q)

Also includes percentrank helper for Mode B:
  percentrank(source, length) = percentage of past length values <= current value
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def true_range(
    highs: list[float], lows: list[float], closes: list[float]
) -> list[float]:
    """Pine ta.tr(true): max(high - low, abs(high - close[1]), abs(low - close[1]))."""
    n = len(highs)
    if n == 0:
        return []
    out = [0.0] * n
    out[0] = highs[0] - lows[0]
    for i in range(1, n):
        h = highs[i]
        l = lows[i]
        c_prev = closes[i - 1]
        out[i] = max(h - l, abs(h - c_prev), abs(l - c_prev))
    return out


def wilder_atr(
    highs: list[float], lows: list[float], closes: list[float], length: int
) -> list[float | None]:
    """Wilder's ATR as in Pine ta.atr(length), using RMA (Wilder's smoothing).

    Warmup: first valid value at index length - 1, equal to SMA of tr[:length].
    Subsequent values: (prev * (length - 1) + tr[i]) / length.
    """
    n = len(highs)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    tr = true_range(highs, lows, closes)
    seed = sum(tr[:length]) / length
    out[length - 1] = seed

    prev = seed
    for i in range(length, n):
        prev = (prev * (length - 1) + tr[i]) / length
        out[i] = prev
    return out


def highest(values: list[float | None], length: int) -> list[float | None]:
    """Rolling highest over past `length` bars (inclusive of current bar).

    Returns None if fewer than `length` valid non-None values are available.
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    for i in range(length - 1, n):
        window = values[i - length + 1 : i + 1]
        if any(v is None for v in window):
            out[i] = None
        else:
            out[i] = max(v for v in window if v is not None)
    return out


def lowest(values: list[float | None], length: int) -> list[float | None]:
    """Rolling lowest over past `length` bars (inclusive of current bar).

    Returns None if fewer than `length` valid non-None values are available.
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    for i in range(length - 1, n):
        window = values[i - length + 1 : i + 1]
        if any(v is None for v in window):
            out[i] = None
        else:
            out[i] = min(v for v in window if v is not None)
    return out


@dataclass(frozen=True)
class ChandeKrollStops:
    atr: list[float | None]
    high_stop: list[float | None]
    low_stop: list[float | None]
    stop_short: list[float | None]
    stop_long: list[float | None]


def chande_kroll_stops(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    *,
    p: int = 10,
    x: float = 1.0,
    q: int = 9,
) -> ChandeKrollStops:
    """Compute Chande Kroll Stop bands.

    Stage 1:
      atr = ta.atr(p)
      highStop = ta.highest(high, p) - x * atr
      lowStop = ta.lowest(low, p) + x * atr
    Stage 2:
      stopShort = ta.highest(highStop, q)
      stopLong = ta.lowest(lowStop, q)

    Note:
      high_stop[i] requires highest(high, p) and atr(p). Both valid from i >= p - 1.
      stop_short[i] requires highest(high_stop, q), so valid from i >= (p - 1) + (q - 1).
    """
    n = len(highs)
    atr = wilder_atr(highs, lows, closes, p)
    highs_boxed: list[float | None] = list(highs)
    lows_boxed: list[float | None] = list(lows)

    hh_p = highest(highs_boxed, p)
    ll_p = lowest(lows_boxed, p)

    high_stop: list[float | None] = [None] * n
    low_stop: list[float | None] = [None] * n

    for i in range(n):
        hh = hh_p[i]
        ll = ll_p[i]
        at = atr[i]
        if hh is not None and at is not None:
            high_stop[i] = hh - x * at
        if ll is not None and at is not None:
            low_stop[i] = ll + x * at

    stop_short = highest(high_stop, q)
    stop_long = lowest(low_stop, q)

    return ChandeKrollStops(
        atr=atr,
        high_stop=high_stop,
        low_stop=low_stop,
        stop_short=stop_short,
        stop_long=stop_long,
    )


def percent_rank(source: list[float | None], length: int) -> list[float | None]:
    """Pine ta.percentrank(source, length):

    Percent of values in the past `length` bars that are less than or equal to current bar.
    Pine definition: 100 * (count of source[k] <= source[0] for k in 0..length) / (length + 1)
    or strictly over past bars (length lookback).
    Standard Pine percentrank formula:
      count = 0
      for k = 0 to length
          if source[k] <= source[0]: count += 1
      percentrank = count / (length + 1) * 100
    """
    n = len(source)
    out: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return out

    for i in range(length, n):
        cur = source[i]
        if cur is None:
            out[i] = None
            continue
        window = source[i - length : i + 1]
        if any(v is None for v in window):
            out[i] = None
            continue
        count = sum(1 for v in window if v is not None and v <= cur)
        out[i] = (count / len(window)) * 100.0
    return out
