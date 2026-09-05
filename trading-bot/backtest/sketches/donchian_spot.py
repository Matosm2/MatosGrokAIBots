"""donchian-20-10-spot-v1 — Daily Donchian breakout (research sketch)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.sketches.engine import apply_position_gate


@dataclass(frozen=True)
class DonchianParams:
    entry_lookback: int = 20
    exit_lookback: int = 10


def _prior_highest_high(highs: list[float], i: int, lookback: int) -> float | None:
    """Highest high of the prior `lookback` bars excluding bar i (classic Donchian)."""
    if i < lookback:
        return None
    return max(highs[i - lookback : i])


def _prior_lowest_low(lows: list[float], i: int, lookback: int) -> float | None:
    """Lowest low of the prior `lookback` bars excluding bar i."""
    if i < lookback:
        return None
    return min(lows[i - lookback : i])


def compute_raw(
    bars: list[Bar],
    params: DonchianParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: close > highest high of the prior 20 bars (excluding current).
           Equivalent to classic close > Donchian upper band built on prior highs.
    Exit:  close < lowest low of the prior 10 bars (excluding current).
    """
    params = params or DonchianParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        up = _prior_highest_high(highs, i, params.entry_lookback)
        lo = _prior_lowest_low(lows, i, params.exit_lookback)
        if up is not None:
            raw_long[i] = closes[i] > up
        if lo is not None:
            raw_exit[i] = closes[i] < lo
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: DonchianParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))


STRATEGY_ID = "donchian-20-10-spot-v1"
INTERVAL = "1d"
