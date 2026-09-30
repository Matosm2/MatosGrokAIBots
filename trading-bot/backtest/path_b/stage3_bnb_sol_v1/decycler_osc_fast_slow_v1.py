"""decycler-osc-fast-slow-v1 — Ehlers Decycler Oscillator Fast × Slow Crossover.

LOCKED SPEC:
Indicators:
  Ehlers Decycler Oscillator pair (John F. Ehlers, TASC Sep 2015 "Decyclers").
  Fast(P_fast, K=1.2) × Slow(P_slow, K=1.0).
  Pairs: (100, 125), (50, 63), (40, 50).

Entry Mode A (primary):
  Long: fast osc crosses above slow osc (ta.crossover).
  (Lead is long-only first pass).

Entry Mode B (direction filter):
  Mode A + fast > 0 for longs. Mode A first for n.

Exit:
  Opposite cross (fast osc crosses below slow osc); or optional ATR trail stop.

≠ Roofing; ≠ CG; ≠ Cyber Cycle; ≠ MESA Sine; ≠ Fisher-on-decycler.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_decycler_oscillator

STRATEGY_ID = "decycler-osc-fast-slow-v1"


@dataclass(frozen=True)
class DecyclerOscParams:
    p_fast: int = 100
    p_slow: int = 125
    k_fast: float = 1.2
    k_slow: float = 1.0
    mode: str = "mode_a"  # "mode_a" (crossover) | "mode_b" (crossover + fast > 0)
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: DecyclerOscParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for decycler-osc-fast-slow-v1."""
    params = params or DecyclerOscParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    fast_osc = ehlers_decycler_oscillator(closes, hp_period=params.p_fast, k=params.k_fast)
    slow_osc = ehlers_decycler_oscillator(closes, hp_period=params.p_slow, k=params.k_slow)

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    mode = params.mode.lower()
    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if fast_osc[i] is None or slow_osc[i] is None:
            continue

        cross_up = crossover(fast_osc, slow_osc, i)
        cross_down = crossunder(fast_osc, slow_osc, i)

        if mode == "mode_b" and cross_up:
            if fast_osc[i] is None or fast_osc[i] <= 0.0:
                cross_up = False

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
