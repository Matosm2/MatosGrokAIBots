"""elder-ray-v1 — Bear Power fade under rising EMA13."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import ema
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "elder-ray-v1"


@dataclass(frozen=True)
class ElderRayParams:
    ema_length: int = 13


def compute_raw(
    bars: list[Bar],
    params: ElderRayParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Bull = High − EMA; Bear = Low − EMA.
    Entry: EMA rising AND Bear < 0 AND Bear rising vs prior bar.
    Exit: Bear turns down OR EMA falling.
    """
    params = params or ElderRayParams()
    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    ema_s = ema(closes, params.ema_length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(1, n):
        if ema_s[i] is None or ema_s[i - 1] is None:
            continue
        bear = lows[i] - ema_s[i]  # type: ignore[operator]
        bear_prev = lows[i - 1] - ema_s[i - 1]  # type: ignore[operator]
        ema_rising = ema_s[i] > ema_s[i - 1]  # type: ignore[operator]
        ema_falling = ema_s[i] < ema_s[i - 1]  # type: ignore[operator]
        bear_rising = bear > bear_prev
        bear_turns_down = bear < bear_prev
        raw_long[i] = ema_rising and bear < 0.0 and bear_rising
        raw_exit[i] = bear_turns_down or ema_falling
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ElderRayParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
