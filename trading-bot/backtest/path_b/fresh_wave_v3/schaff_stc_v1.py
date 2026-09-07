"""schaff-stc-v1 — Schaff Trend Cycle(23,50,10) 25/75 cycle turns."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, schaff_stc
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "schaff-stc-v1"


@dataclass(frozen=True)
class SchaffStcParams:
    fast_length: int = 23
    slow_length: int = 50
    cycle_length: int = 10
    entry_level: float = 25.0
    exit_level: float = 75.0


def compute_raw(
    bars: list[Bar],
    params: SchaffStcParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(STC, 25).
    Exit: crossunder(STC, 75).
    """
    params = params or SchaffStcParams()
    closes = [b.close for b in bars]
    series = schaff_stc(
        closes,
        params.fast_length,
        params.slow_length,
        params.cycle_length,
    )
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
    params: SchaffStcParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
