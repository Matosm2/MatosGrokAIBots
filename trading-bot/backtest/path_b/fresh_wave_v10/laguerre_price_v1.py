"""laguerre-price-v1 — Ehlers Laguerre filter γ=0.8 on close. Forbidden Laguerre RSI / EMA×RSI."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, laguerre_filter
from backtest.path_b.engine import apply_position_gate
from backtest.path_b.fresh_wave_v10 import LAGUERRE_GAMMA

STRATEGY_ID = "laguerre-price-v1"


@dataclass(frozen=True)
class LaguerrePriceParams:
    gamma: float = LAGUERRE_GAMMA


def compute_raw(
    bars: list[Bar],
    params: LaguerrePriceParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: close crossover above Laguerre filter.
    Exit: close crossunder below Laguerre filter.
    Price Laguerre only — not Laguerre RSI; no EMA×RSI stack.
    """
    params = params or LaguerrePriceParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit

    closes = [b.close for b in bars]
    filt = laguerre_filter(closes, gamma=params.gamma)
    close_opt: list[float | None] = list(closes)
    for i in range(n):
        if filt[i] is None:
            continue
        if crossover(close_opt, filt, i):
            raw_long[i] = True
        if crossunder(close_opt, filt, i):
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: LaguerrePriceParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
