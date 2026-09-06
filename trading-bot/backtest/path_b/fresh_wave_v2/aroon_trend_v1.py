"""aroon-trend-v1 — Aroon(25) Up/Down crossover with strength gate."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import aroon, crossover
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "aroon-trend-v1"


@dataclass(frozen=True)
class AroonParams:
    length: int = 25
    strength: float = 70.0


def compute_raw(
    bars: list[Bar],
    params: AroonParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(AroonUp, AroonDown) AND AroonUp ≥ 70.
    Exit: crossover(AroonDown, AroonUp).
    """
    params = params or AroonParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    up, down = aroon(highs, lows, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if up[i] is None or down[i] is None:
            continue
        cross_up = crossover(up, down, i)
        cross_dn = crossover(down, up, i)
        raw_long[i] = cross_up and up[i] >= params.strength  # type: ignore[operator]
        raw_exit[i] = cross_dn
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: AroonParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
