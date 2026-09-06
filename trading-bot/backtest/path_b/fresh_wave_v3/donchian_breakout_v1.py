"""donchian-breakout-v1 — Turtle S1 channel breakout (entry20 / exit10)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import donchian
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "donchian-breakout-v1"


@dataclass(frozen=True)
class DonchianParams:
    entry_length: int = 20
    exit_length: int = 10


def compute_raw(
    bars: list[Bar],
    params: DonchianParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: close > prior 20-bar high (Donchian upper excl. current).
    Exit: close < prior 10-bar low (Donchian lower excl. current).
    No pyramid (gated).
    """
    params = params or DonchianParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    upper, _ = donchian(highs, lows, params.entry_length)
    _, lower = donchian(highs, lows, params.exit_length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if upper[i] is not None and closes[i] > upper[i]:  # type: ignore[operator]
            raw_long[i] = True
        if lower[i] is not None and closes[i] < lower[i]:  # type: ignore[operator]
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: DonchianParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
