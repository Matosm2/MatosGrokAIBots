"""absolute-strength-hist-zero — Absolute Strength Histogram zero-cross (RSI-method, SMA).

LOCKED ENCODE ORDER #3 (BTC->ETH PORTABILITY PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage8 burned ROC/AO; stage13 wiped PZO/TMO and deferred ASH for RSI/STOCH naming.
  ASH RSI-method decomposes close-change into absolute bulls/bears then light double-average —
  encode ASH = SmthBulls - SmthBears x 0, != Wilder RSI, != Stoch %K, != CMO-zero, != TMO, != PZO.
  Prefer SMA internals (not WMA) to avoid stage8 WMA-dual burn rhyme.
  Close-only -> identical (length, smooth) on BTC/ETH/SOL/BNB.

Formula:
  d = close - close[1]
  bulls = 0.5 * (|d| + d)
  bears = 0.5 * (|d| - d)
  avgB = sma(bulls, length)
  avgS = sma(bears, length)
  smB = sma(avgB, smooth)
  smS = sma(avgS, smooth)
  ash = smB - smS
  Prefer length=9, smooth=2.

Mode A (BTC->ETH-PRIMARY):
  long: crossover(ash, 0)
  exit: crossunder(ash, 0) or ATR stop.

Mode B (BNB quiet / quality hold):
  long: crossover(ash, 0) and ash > 0 quality hold / smB > smS
  exit: crossunder(ash, 0) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if length/smooth raised into stage12-damp; Kill if Wilder RSI substitute; Kill if TMO/PZO graft.
  Prefer Mode A (9,2), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears then ETH wipes (stage13 REI pattern); Kill if params retuned only on ETH; Kill if RSI OB/OS replace zero-cross.
  Prefer identical (9,2) on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if RSI/Stoch/CMO/TMO labeled ASH; 15m length=3; stage12-13.
  Retention check: after ETH, SOL n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (length,smooth) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: Wilder RSI; Stoch; CMO-zero; TMO/PZO/REI; WMA dual-price; stage12 duals; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import absolute_strength_hist, atr, crossover, crossunder

STRATEGY_ID = "absolute-strength-hist-zero"


@dataclass(frozen=True)
class AbsoluteStrengthHistParams:
    mode: str = "mode_a"  # "mode_a" (ash cross 0) | "mode_b" (ash cross 0 and ash > 0 quality)
    length: int = 9
    smooth: int = 2
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: AbsoluteStrengthHistParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.smooth > 10 or params.length > 30:
        return False, f"btc_smoke: params ({params.length},{params.smooth}) enter stage12-damp"
    if params.length not in {7, 9, 14} or params.smooth not in {1, 2, 3}:
        return False, f"btc_smoke: ({params.length},{params.smooth}) not in locked sweep grid"
    return True, "PASS"


def validate_eth_smoke(params: AbsoluteStrengthHistParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.length not in {7, 9, 14} or params.smooth not in {1, 2, 3}:
        return False, f"eth_smoke: ({params.length},{params.smooth}) retuned away from locked grid"
    return True, "PASS"


def validate_sol_smoke(params: AbsoluteStrengthHistParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 3:
        return False, "sol_smoke: 15m length<=3 forbidden (spam)"
    if params.length not in {7, 9, 14} or params.smooth not in {1, 2, 3}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: AbsoluteStrengthHistParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.length <= 0 or params.smooth <= 0:
        return False, "bnb_smoke: length and smooth must be > 0"
    if params.smooth > 10:
        return False, "bnb_smoke: smooth too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: AbsoluteStrengthHistParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for absolute-strength-hist-zero."""
    params = params or AbsoluteStrengthHistParams()
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
    ash = absolute_strength_hist(closes, length=params.length, smooth=params.smooth)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(ash, zero_line, i)
        cross_dn = crossunder(ash, zero_line, i)

        ash_val = ash[i] if ash[i] is not None else 0.0

        if params.mode == "mode_b":
            entry_cond = cross_up and ash_val > 0.0
        else:
            entry_cond = cross_up

        if not in_pos:
            if entry_cond:
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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
