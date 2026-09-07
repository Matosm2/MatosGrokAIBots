"""adx-dmi-trend-v1 — Wilder DI flip with ADX strength gate."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import adx_di, crossover
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "adx-dmi-trend-v1"


@dataclass(frozen=True)
class AdxDmiParams:
    length: int = 14
    adx_min: float = 25.0


def compute_raw(
    bars: list[Bar],
    params: AdxDmiParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(+DI, −DI) AND ADX > 25.
    Exit: crossover(−DI, +DI).
    """
    params = params or AdxDmiParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    plus_di, minus_di, adx = adx_di(highs, lows, closes, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if plus_di[i] is None or minus_di[i] is None:
            continue
        cross_up = crossover(plus_di, minus_di, i)
        cross_dn = crossover(minus_di, plus_di, i)
        adx_ok = adx[i] is not None and adx[i] > params.adx_min  # type: ignore[operator]
        raw_long[i] = cross_up and adx_ok
        raw_exit[i] = cross_dn
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: AdxDmiParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
