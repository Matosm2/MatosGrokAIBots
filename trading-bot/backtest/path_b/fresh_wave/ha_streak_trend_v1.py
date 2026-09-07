"""ha-streak-trend-v1 — Heikin-Ashi 3-bull streak entry / first bear exit."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import heikin_ashi
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "ha-streak-trend-v1"


@dataclass(frozen=True)
class HaStreakParams:
    bull_streak: int = 3


def compute_raw(
    bars: list[Bar],
    params: HaStreakParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    HA bull bar: HA close > HA open; HA bear: HA close < HA open.
    Entry: after `bull_streak` consecutive HA bull bars (signal on the Nth bull).
    Exit: first HA bear bar.
    """
    params = params or HaStreakParams()
    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    ha_o, _ha_h, _ha_l, ha_c = heikin_ashi(opens, highs, lows, closes)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    streak = 0
    for i in range(n):
        bull = ha_c[i] > ha_o[i]
        bear = ha_c[i] < ha_o[i]
        if bull:
            streak += 1
        else:
            streak = 0
        raw_long[i] = streak >= params.bull_streak
        raw_exit[i] = bear
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: HaStreakParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
