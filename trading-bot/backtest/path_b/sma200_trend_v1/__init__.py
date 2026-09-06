"""sma200-trend-v1 — Daily SMA200 cross-above trend (Path B research)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import sma

STRATEGY_ID = "sma200-trend-v1"
INTERVAL = "1d"


@dataclass(frozen=True)
class Sma200Params:
    length: int = 200


def compute_signals(
    bars: list[Bar],
    params: Sma200Params | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry while flat: close crosses above SMA(200), OR first bar with
    close > SMA200 after becoming flat (re-entry / window-start case).
    Exit: close < SMA(200).
    NOT always-long-while-above without a cross/re-entry rule.
    Pyramiding 0.
    """
    params = params or Sma200Params()
    closes = [b.close for b in bars]
    s = sma(closes, params.length)
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    in_pos = False
    for i in range(n):
        if s[i] is None:
            continue
        above = closes[i] > s[i]
        below = closes[i] < s[i]
        if in_pos:
            if below:
                sells[i] = True
                in_pos = False
            continue
        # flat: entry on cross above, or first usable bar already above
        crossed = False
        if i > 0 and s[i - 1] is not None:
            crossed = closes[i - 1] <= s[i - 1] and closes[i] > s[i]
        first_ready_above = above and (i == 0 or s[i - 1] is None)
        # after flat: prior bar was at/below SMA (includes just-exited on prior bar)
        after_flat_above = False
        if above and i > 0 and s[i - 1] is not None:
            after_flat_above = closes[i - 1] <= s[i - 1]
        if crossed or first_ready_above or after_flat_above:
            buys[i] = True
            in_pos = True
    return buys, sells


def compute_raw(
    bars: list[Bar],
    params: Sma200Params | None = None,
) -> tuple[list[bool], list[bool]]:
    """Raw flags without position gate (for tests)."""
    params = params or Sma200Params()
    closes = [b.close for b in bars]
    s = sma(closes, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if s[i] is None:
            continue
        raw_exit[i] = closes[i] < s[i]
        if i > 0 and s[i - 1] is not None:
            raw_long[i] = closes[i - 1] <= s[i - 1] and closes[i] > s[i]
        elif closes[i] > s[i]:
            raw_long[i] = True
    return raw_long, raw_exit
