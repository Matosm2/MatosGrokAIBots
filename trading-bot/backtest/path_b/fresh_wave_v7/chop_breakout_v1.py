"""chop-breakout-v1 — CHOP(14) regime gate + structure break (NOT Donchian-branded)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import choppiness_index
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "chop-breakout-v1"


@dataclass(frozen=True)
class ChopBreakoutParams:
    chop_length: int = 14
    trend_max: float = 38.2  # allow breakouts only when CHOP < this
    halt_min: float = 61.8  # exit / halt when CHOP > this
    break_n: int = 20  # prior N-bar high for entry
    exit_n: int = 10  # prior N-bar low for exit


def compute_raw(
    bars: list[Bar],
    params: ChopBreakoutParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: close > prior break_n high AND CHOP < 38.2. No ADX co-gate.
    Exit: close < prior exit_n low OR CHOP > 61.8.
    """
    params = params or ChopBreakoutParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    chop = choppiness_index(highs, lows, closes, params.chop_length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    bn = params.break_n
    en = params.exit_n
    for i in range(n):
        ch = chop[i]
        if ch is None:
            continue
        if i >= bn and ch < params.trend_max:
            prior_high = max(highs[i - bn : i])
            if closes[i] > prior_high:
                raw_long[i] = True
        if ch > params.halt_min:
            raw_exit[i] = True
        elif i >= en:
            prior_low = min(lows[i - en : i])
            if closes[i] < prior_low:
                raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ChopBreakoutParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
