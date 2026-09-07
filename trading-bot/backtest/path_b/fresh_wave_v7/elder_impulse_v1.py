"""elder-impulse-v1 — Elder Impulse (EMA13 + MACD-hist); NO FI; buy-stop when not Red."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import ema, macd_hist
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "elder-impulse-v1"

# Impulse colors
GREEN = 1
RED = -1
BLUE = 0


@dataclass(frozen=True)
class ElderImpulseParams:
    ema_length: int = 13
    cancel_bars: int = 2
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9


def _impulse_colors(
    closes: list[float], params: ElderImpulseParams
) -> list[int | None]:
    """Green=both↑; Red=both↓; else Blue. None while indicators warming."""
    n = len(closes)
    e = ema(closes, params.ema_length)
    _m, _s, hist = macd_hist(
        closes, params.macd_fast, params.macd_slow, params.macd_signal
    )
    colors: list[int | None] = [None] * n
    for i in range(1, n):
        e0, e1 = e[i], e[i - 1]
        h0, h1 = hist[i], hist[i - 1]
        if e0 is None or e1 is None or h0 is None or h1 is None:
            continue
        ema_up = e0 > e1
        ema_dn = e0 < e1
        hist_up = h0 > h1
        hist_dn = h0 < h1
        if ema_up and hist_up:
            colors[i] = GREEN
        elif ema_dn and hist_dn:
            colors[i] = RED
        else:
            colors[i] = BLUE
    return colors


def compute_raw(
    bars: list[Bar],
    params: ElderImpulseParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry TF only (first pass — no HTF censor).
    When impulse is not Red: arm buy-stop at prior bar high; fill close>=stop
    within cancel_bars; cancel otherwise. NO market-on-green; NO FI.
    Exit: Red bar (opposite impulse).
    """
    params = params or ElderImpulseParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    colors = _impulse_colors(closes, params)

    armed = False
    arm_level = 0.0
    bars_left = 0

    for i in range(n):
        col = colors[i]

        # Exit on Red (opposite impulse)
        if col == RED:
            raw_exit[i] = True
            # Also cancel any pending buy-stop on Red
            if armed:
                armed = False
                bars_left = 0

        if armed:
            bars_left -= 1
            if closes[i] >= arm_level:
                raw_long[i] = True
                armed = False
                bars_left = 0
            elif bars_left <= 0:
                armed = False
            continue

        # Arm buy-stop only when not Red (Green or Blue) — never market on green alone
        if col is not None and col != RED and i >= 1:
            armed = True
            arm_level = highs[i - 1]
            bars_left = params.cancel_bars
            if closes[i] >= arm_level:
                raw_long[i] = True
                armed = False
                bars_left = 0

    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ElderImpulseParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
