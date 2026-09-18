"""wma-fast-slow-cross-v1 — Linear Weighted MA fast×slow cross.

LOCKED ENCODE ORDER #4 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Fixed linear WMA dual-cross remains unused: heavier arithmetic weight on recent bars
  (≠ SMA equal weight, ≠ HMA nested WMAs+sqrt, ≠ ZLEMA lag-remove, ≠ VWMA×SMA volume).
  Dense crossover n on 1H with (9,21)/(10,30) — anti-sparse vs ER.
  Identical (Lf, Ls) on SOL+BNB; close-only portable.

Formula:
  fast = ta.wma(close, Lf); slow = ta.wma(close, Ls)
  Linear arithmetic weights only.
  (Lf, Ls) in {(9, 21), (10, 30), (12, 26), (5, 20)}; prefer (10, 30) or (9, 21).

Mode A (primary):
  long: ta.crossover(fast, slow)
  exit: ta.crossunder(fast, slow) or ATR stop.

Mode B (secondary denser):
  long while close > slow and fast > slow
  exit: ta.crossunder(fast, slow) or ATR stop.

sol_smoke:
  Kill if: HMA/ZLEMA/VWMA substitute; ER/ATR%ile gate; 15m (3,8); Hull disguise.
  Prefer Mode A (10,30)/(9,21), 1H+.
  Retention: after ETH, SOL cross n must not collapse.

bnb_smoke:
  Kill if: different (Lf, Ls); Mode B ungated shorts; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: HMA, ZLEMA, VWMA×SMA, FRAMA, McGinley, ALMA, T3, ER-gate, SMA200, WMA-of-WMA Hull.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, wma

STRATEGY_ID = "wma-fast-slow-cross-v1"


@dataclass(frozen=True)
class WmaCrossParams:
    mode: str = "mode_a"  # "mode_a" (crossover) | "mode_b" (close > slow and fast > slow)
    fast_len: int = 10
    slow_len: int = 30
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: WmaCrossParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and (params.fast_len, params.slow_len) == (3, 8):
        return False, "sol_smoke: 15m (3,8) forbidden (spam)"
    if (params.fast_len, params.slow_len) not in {
        (9, 21),
        (10, 30),
        (12, 26),
        (5, 20),
    }:
        return False, f"sol_smoke: (Lf, Ls)=({params.fast_len}, {params.slow_len}) not in locked set"
    if params.fast_len >= params.slow_len:
        return False, "sol_smoke: fast_len >= slow_len invalid"
    return True, "PASS"


def validate_bnb_smoke(params: WmaCrossParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.fast_len >= params.slow_len:
        return False, "bnb_smoke: fast_len >= slow_len invalid"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: WmaCrossParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for wma-fast-slow-cross-v1."""
    params = params or WmaCrossParams()
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
    fast_vals = wma(closes, params.fast_len)
    slow_vals = wma(closes, params.slow_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        f_val = fast_vals[i]
        s_val = slow_vals[i]

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
            # Exit on crossunder
            if crossunder(fast_vals, slow_vals, i):
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
                if crossover(fast_vals, slow_vals, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: close > slow and fast > slow
                if c is not None and s_val is not None and f_val is not None and c > s_val and f_val > s_val:
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
