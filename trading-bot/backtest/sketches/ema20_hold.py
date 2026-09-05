"""close-above-ema20-hold-v1 — Daily close above rising EMA20 (research sketch)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import adx_di, ema
from backtest.sketches.engine import apply_position_gate


@dataclass(frozen=True)
class Ema20HoldParams:
    ema_len: int = 20
    ema_slope_lookback: int = 5
    # Optional ADX filter — OFF by default (adx_min is None / unused).
    adx_len: int = 14
    adx_min: float | None = None  # e.g. 15.0 to enable ADX≥15
    # Explicitly no EMA50>EMA200 filter on this sketch.


def compute_raw(
    bars: list[Bar],
    params: Ema20HoldParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry (flat): close > EMA20 AND EMA20 > EMA20[5]
                 (+ optional ADX ≥ adx_min when adx_min is set)
    Exit (in pos): close < EMA20

    No EMA50>EMA200 requirement.
    """
    params = params or Ema20HoldParams()
    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    e20 = ema(closes, params.ema_len)
    plus_di = minus_di = adx = None
    if params.adx_min is not None:
        plus_di, minus_di, adx = adx_di(highs, lows, closes, params.adx_len)

    n = len(bars)
    lb = params.ema_slope_lookback
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if e20[i] is None:
            continue
        if i >= lb and e20[i - lb] is None:
            continue
        rising = i >= lb and e20[i] is not None and e20[i - lb] is not None and (
            e20[i] > e20[i - lb]
        )
        above = closes[i] > e20[i]
        adx_ok = True
        if params.adx_min is not None:
            assert adx is not None
            if adx[i] is None:
                continue
            adx_ok = adx[i] >= params.adx_min
        raw_long[i] = above and rising and adx_ok
        raw_exit[i] = closes[i] < e20[i]
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: Ema20HoldParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))


STRATEGY_ID = "close-above-ema20-hold-v1"
INTERVAL = "1d"
