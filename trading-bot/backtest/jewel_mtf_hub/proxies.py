"""Open public-indicator proxies for jewel-mtf-hub-regime-v1 (open-proxy edition).

Honest names only — ADX/DI regime, RSI(14) strength, EMA21/55 ribbon.
Frozen thresholds (do not retune on the 6m window):
  ADX_MIN=20, RSI_ENTER=60, RSI_EXIT=50, EMA_FAST=21, EMA_SLOW=55.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.indicators import adx_di, crossover, ema, rsi

# Frozen — do not tune on 6m evaluation window
ADX_LEN = 14
ADX_MIN = 20.0
RSI_LEN = 14
RSI_ENTER = 60.0
RSI_EXIT = 50.0
EMA_FAST = 21
EMA_SLOW = 55


@dataclass(frozen=True)
class RegimeSeries:
    plus_di: list[float | None]
    minus_di: list[float | None]
    adx: list[float | None]
    regime: list[int | None]  # +1 / -1 / 0; None while indicators warming
    flip_to_green: list[bool]
    leave_green: list[bool]


def compute_regime(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    *,
    length: int = ADX_LEN,
    adx_min: float = ADX_MIN,
) -> RegimeSeries:
    """
    regime = +1 when +DI > −DI AND ADX >= adx_min
    regime = −1 when −DI > +DI AND ADX >= adx_min
    regime = 0 otherwise (incl. ties when ADX >= min)
    Warmup bars: regime None; flip/leave False.
    """
    plus_di, minus_di, adx = adx_di(highs, lows, closes, length)
    n = len(closes)
    regime: list[int | None] = [None] * n
    for i in range(n):
        if plus_di[i] is None or minus_di[i] is None or adx[i] is None:
            continue
        if adx[i] >= adx_min:
            if plus_di[i] > minus_di[i]:
                regime[i] = 1
            elif minus_di[i] > plus_di[i]:
                regime[i] = -1
            else:
                regime[i] = 0
        else:
            regime[i] = 0

    flip = [False] * n
    leave = [False] * n
    for i in range(1, n):
        prev, cur = regime[i - 1], regime[i]
        if prev is None or cur is None:
            continue
        # Flip→green: prior ≤ 0 and current = +1
        if prev <= 0 and cur == 1:
            flip[i] = True
        # Leave green: prior = +1 and current ≠ +1
        if prev == 1 and cur != 1:
            leave[i] = True
    return RegimeSeries(
        plus_di=plus_di,
        minus_di=minus_di,
        adx=adx,
        regime=regime,
        flip_to_green=flip,
        leave_green=leave,
    )


@dataclass(frozen=True)
class StrengthSeries:
    rsi: list[float | None]
    enter_cross: list[bool]  # crossover(RSI, 60) at bar close
    exit_below: list[bool]  # RSI < 50


def compute_strength(
    closes: list[float],
    *,
    length: int = RSI_LEN,
    enter: float = RSI_ENTER,
    exit_lvl: float = RSI_EXIT,
) -> StrengthSeries:
    """RSI(14) strength proxy: enter on cross above 60; exit when RSI < 50."""
    r = rsi(closes, length)
    n = len(closes)
    level_enter: list[float | None] = [enter] * n
    enter_cross = [crossover(r, level_enter, i) for i in range(n)]
    exit_below = [(r[i] is not None and r[i] < exit_lvl) for i in range(n)]
    return StrengthSeries(rsi=r, enter_cross=enter_cross, exit_below=exit_below)


@dataclass(frozen=True)
class RibbonSeries:
    ema_fast: list[float | None]
    ema_slow: list[float | None]
    ribbon_low: list[float | None]
    ribbon_high: list[float | None]
    close_cross_ema_fast: list[bool]


def compute_ribbon(
    closes: list[float],
    *,
    fast: int = EMA_FAST,
    slow: int = EMA_SLOW,
) -> RibbonSeries:
    """EMA21 / EMA55 ribbon; ribbon_low=min, ribbon_high=max; close×EMA21."""
    ef = ema(closes, fast)
    es = ema(closes, slow)
    n = len(closes)
    r_low: list[float | None] = [None] * n
    r_high: list[float | None] = [None] * n
    for i in range(n):
        if ef[i] is None or es[i] is None:
            continue
        r_low[i] = min(ef[i], es[i])
        r_high[i] = max(ef[i], es[i])
    close_series: list[float | None] = list(closes)
    cross = [crossover(close_series, ef, i) for i in range(n)]
    return RibbonSeries(
        ema_fast=ef,
        ema_slow=es,
        ribbon_low=r_low,
        ribbon_high=r_high,
        close_cross_ema_fast=cross,
    )
