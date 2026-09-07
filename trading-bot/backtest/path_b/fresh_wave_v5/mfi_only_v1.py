"""mfi-only-v1 — Money Flow Index zone-exit (NO RSI graft)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import mfi
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "mfi-only-v1"


@dataclass(frozen=True)
class MfiOnlyParams:
    length: int = 14
    low_level: float = 20.0
    high_level: float = 80.0
    mid_level: float = 50.0


def compute_raw(
    bars: list[Bar],
    params: MfiOnlyParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: was ≤ low_level then cross back > low_level.
    Exit: reach high_level OR reclaim mid_level from below after being long
          (opposite extreme or mid-50).
    """
    params = params or MfiOnlyParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    series = mfi(highs, lows, closes, volumes, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(1, n):
        cur, prev = series[i], series[i - 1]
        if cur is None or prev is None:
            continue
        # Cross back above low after having been at/below low
        if prev <= params.low_level and cur > params.low_level:
            raw_long[i] = True
        # Opposite extreme or mid
        if cur >= params.high_level:
            raw_exit[i] = True
        elif prev < params.mid_level and cur >= params.mid_level:
            raw_exit[i] = True
        elif cur <= params.low_level:
            # Re-enter OS zone while long → optional soft exit; kick: opposite extreme or mid
            pass
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: MfiOnlyParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
