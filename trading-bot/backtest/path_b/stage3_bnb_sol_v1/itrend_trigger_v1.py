"""itrend-trigger-v1 — Ehlers Instantaneous Trendline × Trigger Crossover.

LOCKED SPEC:
Indicators:
  Ehlers Instantaneous Trendline and Trigger (simplified Pine form, alpha=0.07 locked first).
  Price = hl2 = (high + low) / 2.
  Trigger = 2 * ITrend - ITrend[2].

Entry Mode A (primary):
  Long: Trigger crosses above ITrend (ta.crossover).
  (Lead is long-only first pass).

Exit:
  Opposite cross (Trigger crosses below ITrend); or optional ATR trail stop.

≠ 2002 MESA-DLL / dominant-cycle adaptive notch form; ≠ SuperTrend; ≠ EMA grafts; ≠ Roofing; ≠ CG.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_itrend_trigger

STRATEGY_ID = "itrend-trigger-v1"


@dataclass(frozen=True)
class ITrendParams:
    alpha: float = 0.07
    mode: str = "mode_a"
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: ITrendParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for itrend-trigger-v1."""
    params = params or ITrendParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    itrend_vals, trigger_vals = ehlers_itrend_trigger(highs, lows, alpha=params.alpha)

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if itrend_vals[i] is None or trigger_vals[i] is None:
            continue

        cross_up = crossover(trigger_vals, itrend_vals, i)
        cross_down = crossunder(trigger_vals, itrend_vals, i)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, closes[i])

            exit_hit = False
            if cross_down:
                exit_hit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if closes[i] < stop_level:
                    exit_hit = True

            if exit_hit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if cross_up:
            buys[i] = True
            in_pos = True
            highest_since_entry = closes[i]
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = closes[i] - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level
            else:
                stop_level = None

    return buys, sells, stops
