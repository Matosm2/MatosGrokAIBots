"""cci-mr-v1 — CCI(20, 0.015) mean-reversion from deep oversold."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import cci, crossover, crossunder
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "cci-mr-v1"


@dataclass(frozen=True)
class CciParams:
    length: int = 20
    constant: float = 0.015
    entry_level: float = -100.0
    exit_level: float = 100.0


def compute_raw(
    bars: list[Bar],
    params: CciParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(CCI, −100).
    Exit: crossunder(CCI, +100).
    """
    params = params or CciParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    series = cci(highs, lows, closes, params.length, params.constant)
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
    params: CciParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
