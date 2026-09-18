"""dema-fast-slow-cross-v1 — Mulloy Double Exponential Moving Average fast×slow cross.

LOCKED ENCODE ORDER #5 (OPTIONAL LAST — DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage8 wiped WMA dual (0 BTC); stage6 wiped HMA/FRAMA/McGinley; EMA/RSI dual-mom burned.
  Mulloy DEMA = 2*EMA - EMA(EMA) is a lag-reduced single-series MA, not WMA weights,
  not Hull WMAsqrt, not Ehlers ZLEMA.
  Fast×slow DEMA cross is a dense dual-line event on 1H majors — identical (Lf, Ls) on SOL+BNB.
  Seat is encoded last (5th) per directive.
  != EMA dual, != WMA, != HMA, != ZLEMA.

Formula:
  dema(src, n) = 2 * ema(src, n) - ema(ema(src, n), n)
  fast = dema(close, Lf); slow = dema(close, Ls)
  (Lf, Ls) in {(10,30), (5,35), (8,21), (12,26)}; prefer (10,30) or (5,35).

Mode A (primary / dense fast×slow cross):
  long: ta.crossover(fast, slow)
  exit: ta.crossunder(fast, slow) or ATR stop.

Mode B (secondary price×DEMA):
  long: ta.crossover(close, slow)
  exit: ta.crossunder(close, slow) or ATR stop.

sol_smoke:
  Kill if: EMA/WMA/HMA/ZLEMA substitute; 15m (3,8) spam; ER/AO/PGO graft.
  Prefer Mode A (10,30), 1H+.
  Retention check: after ETH, if SOL n is huge with poor structure, try (10,30).

bnb_smoke:
  Kill if: different (Lf, Ls) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: plain EMA dual labeled DEMA; WMA dual; HMA; ZLEMA; TEMA; FRAMA/McGinley; SMA200;
           ER-gate; AO/ROC/PGO; PSY/RMI/Disparity/WT/AccelBands; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, dema

STRATEGY_ID = "dema-fast-slow-cross-v1"


@dataclass(frozen=True)
class DemaCrossParams:
    mode: str = "mode_a"  # "mode_a" (fast x slow) | "mode_b" (close x slow)
    fast_len: int = 10
    slow_len: int = 30
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: DemaCrossParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and (params.fast_len <= 3 or params.slow_len <= 8):
        return False, "sol_smoke: 15m (fast<=3, slow<=8) forbidden (spam)"
    if (params.fast_len, params.slow_len) not in {(10, 30), (5, 35), (8, 21), (12, 26)}:
        return False, f"sol_smoke: (fast,slow)=({params.fast_len},{params.slow_len}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DemaCrossParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.fast_len <= 0 or params.slow_len <= 0:
        return False, "bnb_smoke: fast_len and slow_len must be > 0"
    if params.fast_len >= params.slow_len:
        return False, "bnb_smoke: fast_len must be less than slow_len"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DemaCrossParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for dema-fast-slow-cross-v1."""
    params = params or DemaCrossParams()
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
    fast_dema = dema(closes, length=params.fast_len)
    slow_dema = dema(closes, length=params.slow_len)

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
                # Exit on crossunder(fast, slow)
                if crossunder(fast_dema, slow_dema, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit on crossunder(close, slow)
                cl_list: list[float | None] = [closes[i]]
                sl_list: list[float | None] = [slow_dema[i]]
                if i > 0 and slow_dema[i - 1] is not None and slow_dema[i] is not None:
                    if closes[i - 1] >= slow_dema[i - 1] and closes[i] < slow_dema[i]:
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
                # Mode A: crossover(fast, slow)
                if crossover(fast_dema, slow_dema, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(close, slow)
                if slow_dema[i - 1] is not None and slow_dema[i] is not None:
                    if closes[i - 1] <= slow_dema[i - 1] and closes[i] > slow_dema[i]:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
