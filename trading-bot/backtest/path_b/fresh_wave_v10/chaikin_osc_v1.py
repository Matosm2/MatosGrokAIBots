"""chaikin-osc-v1 — EMA3−EMA10 of ADL zero-cross. Forbidden CMF/OBV/MFI twin."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import chaikin_oscillator, crossover, crossunder
from backtest.path_b.engine import apply_position_gate
from backtest.path_b.fresh_wave_v10 import CHAIKIN_FAST, CHAIKIN_SLOW

STRATEGY_ID = "chaikin-osc-v1"


@dataclass(frozen=True)
class ChaikinOscParams:
    fast: int = CHAIKIN_FAST
    slow: int = CHAIKIN_SLOW


def compute_raw(
    bars: list[Bar],
    params: ChaikinOscParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(ChaikinOsc, 0).
    Exit: crossunder(ChaikinOsc, 0).
    Chaikin Osc = EMA(3,ADL)−EMA(10,ADL) — not windowed CMF, not OBV, not MFI.
    """
    params = params or ChaikinOscParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    osc = chaikin_oscillator(
        highs, lows, closes, volumes, fast=params.fast, slow=params.slow
    )
    zero: list[float | None] = [0.0] * n
    for i in range(n):
        if osc[i] is None:
            continue
        if crossover(osc, zero, i):
            raw_long[i] = True
        if crossunder(osc, zero, i):
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ChaikinOscParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
