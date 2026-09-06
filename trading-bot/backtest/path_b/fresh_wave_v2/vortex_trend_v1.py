"""vortex-trend-v1 — Vortex(14) VI+/VI− trend crossover."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, vortex
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "vortex-trend-v1"


@dataclass(frozen=True)
class VortexParams:
    length: int = 14


def compute_raw(
    bars: list[Bar],
    params: VortexParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(VI+, VI−).
    Exit: crossover(VI−, VI+).
    """
    params = params or VortexParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    vip, vim = vortex(highs, lows, closes, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if vip[i] is None or vim[i] is None:
            continue
        raw_long[i] = crossover(vip, vim, i)
        raw_exit[i] = crossover(vim, vip, i)
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: VortexParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
