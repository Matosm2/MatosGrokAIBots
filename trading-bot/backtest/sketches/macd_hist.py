"""macd-hist-regime-v1 — Daily MACD histogram regime (research sketch)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, ema, macd
from backtest.sketches.engine import apply_position_gate


@dataclass(frozen=True)
class MacdHistParams:
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    ema_filter: int = 100


def compute_raw(
    bars: list[Bar],
    params: MacdHistParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: MACD histogram crosses above 0 AND close > EMA100
    Exit: histogram crosses below 0
    """
    params = params or MacdHistParams()
    closes = [b.close for b in bars]
    _line, _sig, hist = macd(
        closes, params.macd_fast, params.macd_slow, params.macd_signal
    )
    e100 = ema(closes, params.ema_filter)
    zero: list[float | None] = [0.0] * len(closes)

    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if hist[i] is None or e100[i] is None:
            continue
        up = crossover(hist, zero, i)
        dn = crossunder(hist, zero, i)
        raw_long[i] = up and closes[i] > e100[i]
        raw_exit[i] = dn
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: MacdHistParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))


STRATEGY_ID = "macd-hist-regime-v1"
INTERVAL = "1d"
