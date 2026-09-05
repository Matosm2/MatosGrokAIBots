"""supertrend-atr-v1 — Daily SuperTrend ATR(10)×3 flip (Path B research)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import supertrend
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "supertrend-atr-v1"
INTERVAL = "1d"


@dataclass(frozen=True)
class SupertrendParams:
    atr_len: int = 10
    mult: float = 3.0


def compute_raw(
    bars: list[Bar],
    params: SupertrendParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """Entry on flip to bullish (+1); exit on flip to bearish (-1). Long-only."""
    params = params or SupertrendParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    _st, direction = supertrend(highs, lows, closes, params.atr_len, params.mult)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        d = direction[i]
        if d is None:
            continue
        prev = direction[i - 1] if i > 0 else None
        if d == 1 and (prev is None or prev == -1):
            raw_long[i] = True
        if d == -1:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: SupertrendParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
