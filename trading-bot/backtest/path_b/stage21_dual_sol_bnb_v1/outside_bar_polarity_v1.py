"""outside-bar-polarity — Outside bar range-engulf polarity.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage20 confirmation oscillators 0 BTC chop.
  Need dense candle impulse polarity that can fire on BTC expansion bars.
  Outside bar:
    outside = high > high[1] and low < low[1]
    mid = low + midFrac * (high - low)  (default 0.5 -> (high+low)/2)
    bullOut = outside and close > mid
    bearOut = outside and close < mid
  Mode A = long rising-edge of bullOut; exit bearOut or (outside and close <= mid).
  Mode B = require close > high[1] follow-through.
  Prefer raw Mode A.
  != Heikin-Ashi / != HHLL pivot BOS / != body-engulfing.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill confirmBars inflate until n collapses;
  Kill HA/HHLL/body-engulf substitute. Prefer Mode A raw bullOut, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill midFrac retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m outside spam; stage12-20 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe / micro-outside chatter;
  Kill confirmBars retuned only on BNB; Mode B only on BNB. Prefer identical; long-only; ATR.

Forbidden: HA bias labeled outside; HHLL/pivot BOS labeled outside;
body-engulfing as primary; Donchian/NR7 grafts; request.security; stage12-20 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, outside_bar

STRATEGY_ID = "outside-bar-polarity"


@dataclass(frozen=True)
class OutsideBarParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    mid_frac: float = 0.5  # 0.5 or 0.6
    confirm_bars: int = 1  # 1 or 2
    require_follow_through: bool = False  # Mode B: close > high[1]
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: OutsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.mid_frac not in {0.5, 0.6}:
        return False, f"btc_smoke: mid_frac={params.mid_frac} not in locked sweep {{0.5, 0.6}}"
    if params.confirm_bars not in {1, 2}:
        return False, f"btc_smoke: confirm_bars={params.confirm_bars} not in locked sweep {{1, 2}}"
    if params.confirm_bars > 3:
        return False, f"btc_smoke: confirm_bars={params.confirm_bars} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: OutsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.mid_frac not in {0.5, 0.6} or params.confirm_bars not in {1, 2}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: OutsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.confirm_bars <= 0:
        return False, "sol_smoke: 15m spam forbidden"
    if params.mid_frac not in {0.5, 0.6} or params.confirm_bars not in {1, 2}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: OutsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.mid_frac not in {0.5, 0.6} or params.confirm_bars not in {1, 2}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: OutsideBarParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for outside-bar-polarity."""
    params = params or OutsideBarParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    outside, bull_out, bear_out = outside_bar(highs, lows, closes, mid_frac=params.mid_frac)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]
        l = lows[i]

        mid = l + params.mid_frac * (h - l)

        # Entry trigger
        if params.confirm_bars == 1:
            rising_edge = bull_out[i] and not bull_out[i - 1]
        else:
            # confirm_bars == 2
            rising_edge = i >= 2 and bull_out[i] and bull_out[i - 1] and not bull_out[i - 2]

        if params.mode == "mode_b" or params.require_follow_through:
            rising_edge = rising_edge and (c > highs[i - 1])

        # Exit condition: bearOut or (outside and close <= mid)
        exit_cond = bear_out[i] or (outside[i] and c <= mid)

        if not in_pos:
            if rising_edge:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * float(atr_vals[i])
        else:
            highest_since_entry = max(highest_since_entry, h)
            stop_hit = False

            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                new_stop = highest_since_entry - params.atr_trail_mult * float(atr_vals[i])
                prev_stop = stops[i - 1]
                if prev_stop is not None and new_stop < prev_stop:
                    new_stop = prev_stop
                stops[i] = new_stop
                if lows[i] <= new_stop:
                    stop_hit = True

            exit_trigger = stop_hit or exit_cond
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
