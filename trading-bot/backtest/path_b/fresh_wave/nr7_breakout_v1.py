"""nr7-breakout-v1 — NR7 narrow-range breakout with 2×ATR / 10-bar mid exit."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr

STRATEGY_ID = "nr7-breakout-v1"


@dataclass(frozen=True)
class Nr7Params:
    """
    NR7: bar range (H-L) is the narrowest of the last `nr_lookback` bars (incl. self).
    Entry: after an NR7 forms, first bar with close > that NR7's high (may be same bar).
    Exit:
      (a) stop: close < entry - 2×ATR(14) at entry (engine stop_prices), OR
      (b) target: close >= entry + 2×ATR(14) at entry, OR
      (c) time: bars held ≥ 10 — exit on bar-close; reference level = NR7 mid
          = (NR7.high + NR7.low) / 2 (documented; fill remains bar-close).
    """

    nr_lookback: int = 7
    atr_len: int = 14
    atr_mult: float = 2.0
    max_hold_bars: int = 10


def _is_nr7(highs: list[float], lows: list[float], i: int, lookback: int) -> bool:
    if i + 1 < lookback:
        return False
    ranges = [highs[j] - lows[j] for j in range(i - lookback + 1, i + 1)]
    cur = ranges[-1]
    return cur <= min(ranges)


def compute_signals(
    bars: list[Bar],
    params: Nr7Params | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Returns (buys, sells, stop_prices). stop_prices[i] active while in trade."""
    params = params or Nr7Params()
    n = len(bars)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    atr_s = atr(highs, lows, closes, params.atr_len)

    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n

    pending_nr7_high: float | None = None
    pending_nr7_mid: float | None = None
    in_pos = False
    entry_i = -1
    entry_px = 0.0
    atr_at_entry = 0.0
    stop_level: float | None = None
    target_level = 0.0

    for i in range(n):
        if _is_nr7(highs, lows, i, params.nr_lookback):
            pending_nr7_high = highs[i]
            pending_nr7_mid = (highs[i] + lows[i]) / 2.0

        if in_pos:
            stops[i] = stop_level
            held = i - entry_i
            hit_target = closes[i] >= target_level
            # Engine also checks stop_prices vs close; signal exit for target/time.
            if hit_target or held >= params.max_hold_bars:
                sells[i] = True
                in_pos = False
                entry_i = -1
                stop_level = None
                # keep pending NR7 for re-entry setups
            continue

        # flat: enter on close > pending NR7 high
        a = atr_s[i]
        if (
            pending_nr7_high is not None
            and a is not None
            and closes[i] > pending_nr7_high
        ):
            buys[i] = True
            in_pos = True
            entry_i = i
            entry_px = closes[i]
            atr_at_entry = a
            stop_level = entry_px - params.atr_mult * atr_at_entry
            target_level = entry_px + params.atr_mult * atr_at_entry
            stops[i] = stop_level
            # consume this NR7 setup
            pending_nr7_high = None
            _ = pending_nr7_mid  # documented mid retained until next NR7

    return buys, sells, stops
