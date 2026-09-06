"""williams-r-mr-v1 — Williams %R(14) OS→recovery mean-reversion."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, williams_r
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "williams-r-mr-v1"


@dataclass(frozen=True)
class WilliamsRParams:
    length: int = 14
    entry_level: float = -80.0
    exit_level: float = -20.0


def compute_raw(
    bars: list[Bar],
    params: WilliamsRParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(%R, −80).
    Exit: crossunder(%R, −20).
    """
    params = params or WilliamsRParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    series = williams_r(highs, lows, closes, params.length)
    n = len(bars)
    level_entry: list[float | None] = [params.entry_level] * n
    level_exit: list[float | None] = [params.exit_level] * n
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if series[i] is None:
            continue
        raw_long[i] = crossover(series, level_entry, i)
        raw_exit[i] = crossunder(series, level_exit, i)
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: WilliamsRParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
