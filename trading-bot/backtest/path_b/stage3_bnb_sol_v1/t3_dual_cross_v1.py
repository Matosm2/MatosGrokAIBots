"""t3-dual-cross-v1 — Tillson T3 Dual Moving Average Crossover.

LOCKED SPEC:
Indicators:
  Tillson T3 moving average via nested GDEMA / polynomial cascade.
  vFactor locked at 0.7 (default) and 0.5 before sweep.
  Fast/slow length pairs: {(5, 15), (8, 21), (10, 30)}.

Entry Mode A (primary):
  Long: fast T3 crosses above slow T3 (ta.crossover).
  (Lead is long-only first pass).

Exit:
  Opposite cross (fast T3 crosses below slow T3); or optional ATR trail stop.

≠ ALMA; ≠ EMA ribbon / stack; ≠ Hull primary; ≠ SMA200 / RSI grafts.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, t3

STRATEGY_ID = "t3-dual-cross-v1"


@dataclass(frozen=True)
class T3Params:
    fast_len: int = 5
    slow_len: int = 15
    v_factor: float = 0.7
    mode: str = "mode_a"
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: T3Params | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for t3-dual-cross-v1."""
    params = params or T3Params()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    fast_t3 = t3(closes, length=params.fast_len, v_factor=params.v_factor)
    slow_t3 = t3(closes, length=params.slow_len, v_factor=params.v_factor)

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if fast_t3[i] is None or slow_t3[i] is None:
            continue

        cross_up = crossover(fast_t3, slow_t3, i)
        cross_down = crossunder(fast_t3, slow_t3, i)

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
