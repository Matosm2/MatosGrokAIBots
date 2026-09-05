"""Jewel Slow/High strength-hold signal logic (no RSI/Stoch proxy)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Variant(str, Enum):
    V_ZONE = "V-zone"
    V_WIDE = "V-wide"


@dataclass(frozen=True)
class JewelParams:
    slow_enter: float = 70.0
    high_enter: float = 80.0
    slow_exit: float = 70.0
    high_exit: float = 80.0
    atr_len: int = 14
    atr_mult: float = 3.0
    variant: Variant = Variant.V_ZONE


@dataclass
class SignalSeries:
    entry_a: list[bool]
    entry_b: list[bool]
    raw_long: list[bool]
    zone_exit: list[bool]
    atr: list[float | None]


def crossover_level(series: list[float | None], level: float, i: int) -> bool:
    """Pine-like ta.crossover(series, level)."""
    if i < 1:
        return False
    cur, prev = series[i], series[i - 1]
    if cur is None or prev is None:
        return False
    return prev <= level and cur > level


def true_range(high: float, low: float, prev_close: float | None) -> float:
    if prev_close is None:
        return high - low
    return max(high - low, abs(high - prev_close), abs(low - prev_close))


def atr_wilder(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int,
) -> list[float | None]:
    """Wilder ATR matching Pine ta.atr."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    trs: list[float] = []
    for i in range(n):
        prev_c = closes[i - 1] if i > 0 else None
        trs.append(true_range(highs[i], lows[i], prev_c))
    # First ATR at index length-1 = SMA of first `length` TRs (Pine)
    seed = sum(trs[:length]) / length
    out[length - 1] = seed
    prev = seed
    for i in range(length, n):
        prev = (prev * (length - 1) + trs[i]) / length
        out[i] = prev
    return out


def compute_signals(
    *,
    highs: list[float],
    lows: list[float],
    closes: list[float],
    slow: list[float | None],
    high_j: list[float | None],
    params: JewelParams | None = None,
) -> SignalSeries:
    """Raw entry/exit flags from Jewel Slow/High (+ ATR series for V-wide)."""
    params = params or JewelParams()
    n = len(closes)
    if not (len(highs) == len(lows) == len(slow) == len(high_j) == n):
        raise ValueError("OHLCV and Slow/High series must be equal length")

    atr = atr_wilder(highs, lows, closes, params.atr_len)
    entry_a = [False] * n
    entry_b = [False] * n
    raw_long = [False] * n
    zone_exit = [False] * n

    for i in range(n):
        a = crossover_level(slow, params.slow_enter, i)
        b = crossover_level(high_j, params.high_enter, i) and (
            slow[i] is not None and slow[i] >= params.slow_enter
        )
        entry_a[i] = a
        entry_b[i] = b
        raw_long[i] = a or b
        s, h = slow[i], high_j[i]
        zone_exit[i] = (
            s is not None
            and h is not None
            and s < params.slow_exit
            and h <= params.high_exit
        )

    return SignalSeries(
        entry_a=entry_a,
        entry_b=entry_b,
        raw_long=raw_long,
        zone_exit=zone_exit,
        atr=atr,
    )
