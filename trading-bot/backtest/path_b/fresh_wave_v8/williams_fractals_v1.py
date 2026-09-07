"""williams-fractals-v1 — Fractals-only breakout (no Alligator / Donchian)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "williams-fractals-v1"


@dataclass(frozen=True)
class WilliamsFractalsParams:
    # Classic 5-bar Williams fractal (2 bars each side of center).
    wings: int = 2


def compute_raw(
    bars: list[Bar],
    params: WilliamsFractalsParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Confirmed 5-bar fractal (center known only after `wings` bars — no look-ahead).
    Entry: close > last confirmed up-fractal high.
    Exit: close < last confirmed down-fractal low.
    Forbidden: Alligator SMAs, Donchian(N), RSI/CCI grafts.
    """
    params = params or WilliamsFractalsParams()
    wings = params.wings
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0 or wings < 1:
        return raw_long, raw_exit

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    last_up: float | None = None
    last_down: float | None = None

    for i in range(n):
        # Confirm fractal whose center is i - wings (needs wings bars after center).
        c = i - wings
        if c >= wings:
            # Up fractal: center high strictly greater than wings bars each side.
            h_c = highs[c]
            up_ok = True
            for k in range(1, wings + 1):
                if highs[c - k] >= h_c or highs[c + k] >= h_c:
                    up_ok = False
                    break
            if up_ok:
                last_up = h_c

            lo_c = lows[c]
            dn_ok = True
            for k in range(1, wings + 1):
                if lows[c - k] <= lo_c or lows[c + k] <= lo_c:
                    dn_ok = False
                    break
            if dn_ok:
                last_down = lo_c

        if last_up is not None and closes[i] > last_up:
            raw_long[i] = True
        if last_down is not None and closes[i] < last_down:
            raw_exit[i] = True

    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: WilliamsFractalsParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
