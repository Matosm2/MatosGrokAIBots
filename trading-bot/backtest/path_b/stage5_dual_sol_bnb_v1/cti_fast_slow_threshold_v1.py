"""cti-fast-slow-threshold-v1 — Ehlers Correlation Trend Indicator Fast Onset + Slow Failure.

LOCKED ENCODE ORDER #1 (DUAL-SURVIVAL: SOL + BNB).
Thesis:
  CTI computes the Pearson correlation of close price vs an ideal rising straight line over length L.
  Because CTI is inherently bounded in [-1.0, +1.0], it provides an identical, normalized scale
  across BTC, ETH, SOL, and BNB without venue-volume quirks or arbitrary amplitude scaling.
  Fast CTI crossing above buyTh marks trend onset; slow CTI crossing below sellTh marks trend failure.

Formula:
  For count = 0..L-1: X = close[count], Y = -count (or chronological X_i = close, Y_i = i)
  Corr = (L*Sxy - Sx*Sy) / sqrt((L*Sxx - Sx^2) * (L*Syy - Sy^2))

Mode A (primary):
  Long: ta.crossover(ctiFast, buyTh)
  Exit/flat: ta.crossunder(ctiSlow, sellTh)
  Defaults: fastL=20, slowL=40, buyTh=0.5, sellTh=0.0

Mode B (denser):
  Long while ctiFast > 0; exit when ctiFast < 0.

Optional dead-bar filter:
  Skip bar if (high - low) / close < atr_pct_floor (default 0.001).

Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, cti

STRATEGY_ID = "cti-fast-slow-threshold-v1"


@dataclass(frozen=True)
class CtiParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    fast_len: int = 20
    slow_len: int = 40
    buy_th: float = 0.5
    sell_th: float = 0.0
    atr_pct_floor: float = 0.001  # min (high - low) / close
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: CtiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.mode == "mode_b":
        return False, "sol_smoke: Mode B ungated on 15m (spam)"
    if params.fast_len <= 10 and params.atr_pct_floor <= 0:
        return False, "sol_smoke: L=10 without dead-bar skip"
    return True, "PASS"


def validate_bnb_smoke(params: CtiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if tf == "4h" and params.slow_len >= 60:
        return False, "bnb_smoke: slowL >= 60 on 4H (too sparse for 6m)"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: CtiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for cti-fast-slow-threshold-v1."""
    params = params or CtiParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    cti_fast = cti(closes, params.fast_len)
    cti_slow = cti(closes, params.slow_len)
    atr_vals = atr(highs, lows, closes, params.atr_len)

    buy_th_series: list[float | None] = [params.buy_th] * n
    sell_th_series: list[float | None] = [params.sell_th] * n
    zero_series: list[float | None] = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        l = lows[i]

        # Dead bar check
        rng_pct = (h - l) / c if c > 0 else 0.0
        is_dead_bar = rng_pct < params.atr_pct_floor

        # Trailing stop update if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False

            if params.mode == "mode_a":
                # Exit when slow CTI crosses below sell threshold
                if crossunder(cti_slow, sell_th_series, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit when fast CTI drops below zero
                if cti_fast[i] is not None and cti_fast[i] < 0.0:
                    exit_signal = True

            # Stop hit check
            if stop_level is not None and c < stop_level:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0
                stop_level = None
                continue

        # Check entries if flat
        if not in_pos and not is_dead_bar:
            enter_signal = False

            if params.mode == "mode_a":
                if crossover(cti_fast, buy_th_series, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                if cti_fast[i] is not None and cti_fast[i] > 0.0:
                    # Enter on crossover into positive or initial positive
                    prev_val = cti_fast[i - 1] if i > 0 else None
                    if prev_val is None or prev_val <= 0.0:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
