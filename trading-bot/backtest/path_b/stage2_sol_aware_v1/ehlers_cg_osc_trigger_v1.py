"""ehlers-cg-osc-trigger-v1 — Ehlers Center-of-Gravity (CG) Oscillator x Trigger Cross.

LOCKED SPEC:
Formula:
  Price = hl2 = (high + low) / 2
  Length default 10 (sweep in {8, 10, 14, 20})
  CG = - sum_{i=0}^{Length-1} ((1 + i) * Price[t - i]) / sum_{i=0}^{Length-1} Price[t - i]
  Trigger = CG[1] (1-bar delayed trigger)
  Document FIR: Center of gravity weighted average FIR filter.

Entry Mode A (primary):
  Long: ta.crossover(CG, Trigger)
  (Lead is long-only first pass).

Entry Mode B (optional filter):
  Long: Mode A + CG > 0 filter.

Exit:
  Opposite cross (ta.crossunder(CG, Trigger)); or optional ATR trail stop.

≠ Cyber Cycle; ≠ Fisher; ≠ RSI/SMA200; ≠ ASI dual-break adjacency.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_cg

STRATEGY_ID = "ehlers-cg-osc-trigger-v1"


@dataclass(frozen=True)
class EhlersCgParams:
    length: int = 10  # {8, 10, 14, 20}
    mode: str = "mode_a"  # "mode_a" (crossover) | "mode_b" (crossover + CG > 0)
    atr_trail_mult: float = 0.0  # 0.0 = opposite cross only; >0 = ATR trail stop
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: EhlersCgParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-cg-osc-trigger-v1."""
    params = params or EhlersCgParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    # Price = hl2
    hl2_prices = [(b.high + b.low) / 2.0 for b in bars]
    cg, trigger = ehlers_cg(hl2_prices, params.length)

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
        if cg[i] is None or trigger[i] is None:
            continue

        cross_up = crossover(cg, trigger, i)
        cross_down = crossunder(cg, trigger, i)

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
            cond = True
            if params.mode.lower() == "mode_b":
                cond = cg[i] is not None and cg[i] > 0.0

            if cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = bars[i].close
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = bars[i].close - atr_vals[i] * params.atr_trail_mult
                    stops[i] = stop_level
                else:
                    stop_level = None

    return buys, sells, stops
