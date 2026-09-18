"""ehlers-roofing-zero-cross-v1 — Ehlers Roofing Filter Zero-Line Cross.

LOCKED SPEC:
Formula:
  2-pole HighPass(hp_period) then 2-pole SuperSmoother(ss_period).
  Document IIR coefficients (per John Ehlers, Cycle Analytics for Traders / MESA).
  Locked (hp, ss) parameter pairs:
    Lead default: (48, 10)
    Alternative 1: (40, 10)
    Alternative 2: (80, 40)

Entry Mode A (primary):
  Long: closed-bar roofing filter crosses above 0 (crossover(roofing, 0)).
  (Lead is long-only first pass).

Exit:
  Opposite cross (roofing crosses below 0); or optional ATR trail stop.

≠ MESA Stochastic 20/80; ≠ Cyber Cycle primary; ≠ Fisher-on-roofing; ≠ RSI grafts; ≠ MESA Sine.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_roofing_filter

STRATEGY_ID = "ehlers-roofing-zero-cross-v1"


@dataclass(frozen=True)
class EhlersRoofingParams:
    hp_period: int = 48  # {(48, 10), (40, 10), (80, 40)}
    ss_period: int = 10
    mode: str = "mode_a"
    atr_trail_mult: float = 0.0  # 0.0 = opposite cross only; >0 = ATR trail stop
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: EhlersRoofingParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-roofing-zero-cross-v1."""
    params = params or EhlersRoofingParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    hl2_prices = [(b.high + b.low) / 2.0 for b in bars]
    roofing_vals = ehlers_roofing_filter(hl2_prices, hp_period=params.hp_period, ss_period=params.ss_period)
    zero_line: list[float | None] = [0.0] * n

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if roofing_vals[i] is None:
            continue

        cross_up = crossover(roofing_vals, zero_line, i)
        cross_down = crossunder(roofing_vals, zero_line, i)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, bars[i].close)

            exit_hit = False
            if cross_down:
                exit_hit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if bars[i].close < stop_level:
                    exit_hit = True

            if exit_hit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if cross_up:
            buys[i] = True
            in_pos = True
            highest_since_entry = bars[i].close
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = bars[i].close - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level
            else:
                stop_level = None

    return buys, sells, stops
