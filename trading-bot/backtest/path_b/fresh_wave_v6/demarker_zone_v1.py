"""demarker-zone-v1 — DeM zone-exit (NO RSI graft)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import demarker
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "demarker-zone-v1"


@dataclass(frozen=True)
class DemarkerZoneParams:
    length: int = 14
    low_level: float = 0.30
    high_level: float = 0.70
    mid_level: float = 0.50


def compute_raw(
    bars: list[Bar],
    params: DemarkerZoneParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: was ≤ low_level then cross back > low_level.
    Exit: reach high_level OR reclaim mid_level from below.
    """
    params = params or DemarkerZoneParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    series = demarker(highs, lows, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(1, n):
        cur, prev = series[i], series[i - 1]
        if cur is None or prev is None:
            continue
        if prev <= params.low_level and cur > params.low_level:
            raw_long[i] = True
        if cur >= params.high_level:
            raw_exit[i] = True
        elif prev < params.mid_level and cur >= params.mid_level:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: DemarkerZoneParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
