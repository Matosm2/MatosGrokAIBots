"""asi-dual-break-v1 — Price + ASI dual level break.

Indicators:
  Wilder's Accumulative Swing Index (ASI) = cumsum(SI).
  T-proxy:
    Family 1 (ATR multiple): T = atr_mult * ATR(atr_len), default atr_mult=1.0, atr_len=14
    Family 2 (% of close): T = pct * close[i-1]

Entry Long:
  Closed bar: close > highest(high, N)[1] AND ASI > highest(ASI, N)[1]
Entry Short:
  Mirror (deferred to second pass; long-only first pass).
Exit:
  Opposite dual break (close < lowest(low, N)[1] AND ASI < lowest(ASI, N)[1])
  or optional ATR trail.

≠ Donchian-naked primary; ≠ Divergence-only discretionary; ≠ RSI/ADX grafts.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import accumulative_swing_index, atr

STRATEGY_ID = "asi-dual-break-v1"


@dataclass(frozen=True)
class AsiDualBreakParams:
    n: int = 20  # lookback N in {10, 20, 55}
    proxy_family: str = "atr"  # "atr" | "pct"
    atr_mult: float = 1.0  # in {0.5, 1.0, 1.5, 2.0}
    atr_len: int = 14
    pct_close: float = 0.02  # in {0.01, 0.02, 0.03}
    atr_trail_mult: float = 0.0  # 0.0 = opposite dual break; >0 = ATR trail stop


def compute_signals(
    bars: list[Bar],
    params: AsiDualBreakParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for asi-dual-break-v1."""
    params = params or AsiDualBreakParams()
    num_bars = len(bars)
    buys = [False] * num_bars
    sells = [False] * num_bars
    stops: list[float | None] = [None] * num_bars
    if num_bars == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    # Compute T proxy per bar
    if params.proxy_family.lower() == "pct":
        t_limit: list[float | None] = [None] * num_bars
        for i in range(1, num_bars):
            t_limit[i] = closes[i - 1] * params.pct_close
    else:
        atr_vals = atr(highs, lows, closes, params.atr_len)
        t_limit = [
            (a * params.atr_mult if a is not None else None)
            for a in atr_vals
        ]

    asi_vals = accumulative_swing_index(opens, highs, lows, closes, t_limit)

    atr_trail_vals: list[float | None] = [None] * num_bars
    if params.atr_trail_mult > 0.0:
        atr_trail_vals = atr(highs, lows, closes, params.atr_len)

    lookback = params.n
    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(num_bars):
        # We need at least lookback prior bars: i - lookback >= 0
        if i < lookback + 1:
            continue

        # Prior N bars: [i - lookback : i]
        prior_highs = highs[i - lookback : i]
        prior_lows = lows[i - lookback : i]
        prior_asis = asi_vals[i - lookback : i]

        hh_prior = max(prior_highs)
        ll_prior = min(prior_lows)
        asi_hh_prior = max(prior_asis)
        asi_ll_prior = min(prior_asis)

        dual_break_up = (closes[i] > hh_prior) and (asi_vals[i] > asi_hh_prior)
        dual_break_down = (closes[i] < ll_prior) and (asi_vals[i] < asi_ll_prior)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, closes[i])

            exit_hit = False
            if dual_break_down:
                exit_hit = True
            elif params.atr_trail_mult > 0.0 and atr_trail_vals[i] is not None:
                trail_stop = highest_since_entry - atr_trail_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if closes[i] < stop_level:
                    exit_hit = True

            if exit_hit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if dual_break_up:
            buys[i] = True
            in_pos = True
            highest_since_entry = closes[i]
            if params.atr_trail_mult > 0.0 and atr_trail_vals[i] is not None:
                stop_level = closes[i] - atr_trail_vals[i] * params.atr_trail_mult
                stops[i] = stop_level
            else:
                stop_level = None

    return buys, sells, stops
