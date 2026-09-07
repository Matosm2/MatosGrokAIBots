"""gann-hilo-activator-v1 — Krausz HiLo Activator Mode A SAR-style flip (n=3). ≠ PSAR."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import sma
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "gann-hilo-activator-v1"


@dataclass(frozen=True)
class GannHiLoParams:
    length: int = 3


def hilo_activator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 3,
) -> tuple[list[float | None], list[bool | None]]:
    """
    Recursive Krausz HiLo (≠ PSAR AF parabola):
      activator = close > activator[1] ? SMA(low, n) : SMA(high, n)
    Returns (activator, is_long_state) where is_long means close > prior activator.
    """
    n = len(closes)
    ma_h = sma(highs, length)
    ma_l = sma(lows, length)
    act: list[float | None] = [None] * n
    is_long: list[bool | None] = [None] * n
    for i in range(n):
        if ma_h[i] is None or ma_l[i] is None:
            continue
        if i == 0 or act[i - 1] is None:
            # Seed: treat above high-SMA as long, else short.
            if closes[i] > ma_h[i]:
                is_long[i] = True
                act[i] = ma_l[i]
            else:
                is_long[i] = False
                act[i] = ma_h[i]
            continue
        if closes[i] > act[i - 1]:
            is_long[i] = True
            act[i] = ma_l[i]
        else:
            is_long[i] = False
            act[i] = ma_h[i]
    return act, is_long


def compute_raw(
    bars: list[Bar],
    params: GannHiLoParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Mode A SAR-style flip:
      Entry: state flips to long (close flips above prior activator).
      Exit: state flips to short (close flips below prior activator).
    No PSAR AF; no SMA200/RSI grafts.
    """
    params = params or GannHiLoParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    _act, state = hilo_activator(highs, lows, closes, params.length)
    for i in range(1, n):
        s0, s1 = state[i], state[i - 1]
        if s0 is None or s1 is None:
            continue
        if s0 and not s1:
            raw_long[i] = True
        if (not s0) and s1:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: GannHiLoParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
