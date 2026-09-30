"""alma-fast-slow-cross-v1 — ALMA Dual Crossover (Gaussian FIR Moving Average).

LOCKED SPEC:
Indicators:
  Arnaud Legoux Moving Average (ALMA):
  FIR Gaussian filter weights with:
    m = offset * (length - 1)
    s = length / sigma
    weight_i = exp(- (i - m)^2 / (2 * s^2))
  Defaults locked before sweep: offset = 0.85, sigma = 6.0.
  Offset sweep: {0.85, 0.90}.
  Fast / slow length pairs: {(9, 21), (20, 50), (60, 120)}.

Entry Mode A (primary):
  Long: fast ALMA crosses above slow ALMA (crossover).
  (Lead is long-only first pass).

Exit:
  Opposite cross (fast ALMA crosses below slow ALMA); or optional ATR trail stop.

≠ EMA ribbon; ≠ Hull primary; ≠ SMA200 graft; ≠ RSI filter.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import alma, atr, crossover, crossunder

STRATEGY_ID = "alma-fast-slow-cross-v1"


@dataclass(frozen=True)
class AlmaParams:
    fast_len: int = 9
    slow_len: int = 21
    offset: float = 0.85
    sigma: float = 6.0
    mode: str = "mode_a"
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: AlmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for alma-fast-slow-cross-v1."""
    params = params or AlmaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    fast_alma = alma(closes, length=params.fast_len, offset=params.offset, sigma=params.sigma)
    slow_alma = alma(closes, length=params.slow_len, offset=params.offset, sigma=params.sigma)

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if fast_alma[i] is None or slow_alma[i] is None:
            continue

        cross_up = crossover(fast_alma, slow_alma, i)
        cross_down = crossunder(fast_alma, slow_alma, i)

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
