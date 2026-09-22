"""dorsey-relvol-midline-fifty-v1 — Dorsey Relative Volatility Index midline-50 cross.

LOCKED ENCODE ORDER #3 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage9 wiped PSY (up-close count) and RMI (m-bar Wilder).
  Dorsey Relative Volatility Index is RSI-shaped but feeds standard deviation assigned by up/down
  direction — volatility-direction polarity.
  CRITICAL: NEVER label as Relative Vigor Index (RVI is (close-open)/(high-low) vigor, burned).
  != RSI, != RVI-vigor, != PSY/RMI, != Stoch.
  Midline-50 is the documented bias line; dense on 1H.
  Close/HL portable; identical (stdevLen, avgLen) on SOL+BNB.

Formula (refined):
  sH = stdev(high, stdevLen); sL = stdev(low, stdevLen)
  uH = high > high[1] ? sH : 0; uL = low > low[1] ? sL : 0
  rviH = 100 * rma(uH, avgLen) / rma(sH, avgLen)
  rviL = 100 * rma(uL, avgLen) / rma(sL, avgLen)
  rvi = (rviH + rviL) / 2.0
  Defaults stdevLen=10, avgLen=14.

Mode A (primary / dense midline cross):
  long: ta.crossover(rvi, 50)
  exit: ta.crossunder(rvi, 50) or ATR stop.

Mode B (secondary classic extremes):
  long: ta.crossover(rvi, 60)
  exit: ta.crossunder(rvi, 40) or ATR stop.

sol_smoke:
  Kill if: Relative Vigor formula; RSI labeled RelVol; 15m stdevLen=3 spam; ER/AO/PGO/ADX graft.
  Prefer Mode A (10, 14), 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class.

bnb_smoke:
  Kill if: different (stdevLen, avgLen) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: Relative Vigor; RSI primary; Stoch; PSY/RMI; ConnorsRSI; ER-gate; AO/ROC/WMA/PGO; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, dorsey_relative_volatility_index

STRATEGY_ID = "dorsey-relvol-midline-fifty-v1"


@dataclass(frozen=True)
class DorseyRelVolParams:
    mode: str = "mode_a"  # "mode_a" (cross > 50) | "mode_b" (cross > 60, exit < 40)
    stdev_len: int = 10
    avg_len: int = 14
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: DorseyRelVolParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.stdev_len <= 3:
        return False, "sol_smoke: 15m stdev_len<=3 forbidden (spam)"
    if (params.stdev_len, params.avg_len) not in {(10, 14), (8, 14), (14, 14), (10, 10)}:
        return False, f"sol_smoke: (stdev,avg)=({params.stdev_len},{params.avg_len}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DorseyRelVolParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.stdev_len <= 1 or params.avg_len <= 0:
        return False, "bnb_smoke: stdev_len must be > 1 and avg_len > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DorseyRelVolParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for dorsey-relvol-midline-fifty-v1."""
    params = params or DorseyRelVolParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    rvi_vals = dorsey_relative_volatility_index(
        highs, lows, closes, stdev_len=params.stdev_len, avg_len=params.avg_len
    )

    fifties: list[float | None] = [50.0] * n
    sixties: list[float | None] = [60.0] * n
    forties: list[float | None] = [40.0] * n

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

        # Update trailing stop if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False
            if params.mode == "mode_a":
                # Exit on crossunder 50
                if crossunder(rvi_vals, fifties, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit on crossunder 40
                if crossunder(rvi_vals, forties, i):
                    exit_signal = True

            # Stop hit check
            if stop_level is not None and c < stop_level:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0
                stop_level = None
                continue

        # Check entries if flat
        if not in_pos and i > 0:
            enter_signal = False
            if params.mode == "mode_a":
                # Mode A: crossover(rvi, 50)
                if crossover(rvi_vals, fifties, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(rvi, 60)
                if crossover(rvi_vals, sixties, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
