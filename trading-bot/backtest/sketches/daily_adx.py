"""daily-adx-trend-hold-v1 — Daily ADX trend hold (research sketch)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import adx_di, ema
from backtest.sketches.engine import apply_position_gate


@dataclass(frozen=True)
class DailyAdxParams:
    ema_fast: int = 50
    ema_slow: int = 200
    adx_len: int = 14
    adx_entry_min: float = 25.0
    adx_exit_max: float = 20.0


def compute_raw(
    bars: list[Bar],
    params: DailyAdxParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry (flat): EMA50 > EMA200 AND ADX14 >= 25 AND +DI > -DI
    Exit (in pos): -DI > +DI OR ADX < 20 OR close < EMA200
    """
    params = params or DailyAdxParams()
    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    ef = ema(closes, params.ema_fast)
    es = ema(closes, params.ema_slow)
    plus_di, minus_di, adx = adx_di(highs, lows, closes, params.adx_len)

    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if (
            ef[i] is None
            or es[i] is None
            or adx[i] is None
            or plus_di[i] is None
            or minus_di[i] is None
        ):
            continue
        raw_long[i] = (
            ef[i] > es[i]
            and adx[i] >= params.adx_entry_min
            and plus_di[i] > minus_di[i]
        )
        raw_exit[i] = (
            minus_di[i] > plus_di[i]
            or adx[i] < params.adx_exit_max
            or closes[i] < es[i]
        )
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: DailyAdxParams | None = None,
) -> tuple[list[bool], list[bool]]:
    raw_long, raw_exit = compute_raw(bars, params)
    return apply_position_gate(raw_long, raw_exit)


STRATEGY_ID = "daily-adx-trend-hold-v1"
INTERVAL = "1d"
