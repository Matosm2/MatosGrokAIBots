"""mass-index-bulge-v1 — Dorsey Mass Index bulge reversal + EMA9 slope."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import ema, mass_index
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "mass-index-bulge-v1"


@dataclass(frozen=True)
class MassIndexBulgeParams:
    sum_length: int = 25
    ema_length: int = 9
    side_ema: int = 9
    bulge_high: float = 27.0
    bulge_low: float = 26.5


def compute_raw(
    bars: list[Bar],
    params: MassIndexBulgeParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Setup: MI rises above bulge_high then falls below bulge_low (reversal bulge).
    Long only when EMA(side_ema) slope is up. Exit when EMA slope flips down.
    """
    params = params or MassIndexBulgeParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    mi = mass_index(highs, lows, params.ema_length, params.sum_length)
    side = ema(closes, params.side_ema)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    seen_above = False
    for i in range(n):
        v = mi[i]
        if v is not None and v > params.bulge_high:
            seen_above = True
        slope_up = (
            side[i] is not None
            and i > 0
            and side[i - 1] is not None
            and side[i] > side[i - 1]  # type: ignore[operator]
        )
        slope_down = (
            side[i] is not None
            and i > 0
            and side[i - 1] is not None
            and side[i] < side[i - 1]  # type: ignore[operator]
        )
        if (
            seen_above
            and v is not None
            and v < params.bulge_low
            and slope_up
        ):
            raw_long[i] = True
            seen_above = False  # consume bulge setup
        if slope_down:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: MassIndexBulgeParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
