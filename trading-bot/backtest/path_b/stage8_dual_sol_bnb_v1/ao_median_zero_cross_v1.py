"""ao-median-zero-cross-v1 — Bill Williams Awesome Oscillator zero-cross.

LOCKED ENCODE ORDER #1 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage7 failed on sparse coincidence (ER>thr ∩ SMA cross -> n≈2) and parked unused Ehlers/RWI.
  AO is a dense momentum histogram: SMA of HL2 (not close) fast - slow, unbound around zero.
  Zero-line cross is Williams' two-bar signal — fires whenever short median momentum flips vs long.
  Expected BTC/ETH 1H–4H trade density far above stage7 ER.
  Distinct from burned Fractals / Gann HiLo; no Alligator SMMA stack.
  Close+HL portable; identical (fast, slow) on SOL+BNB.
  Explicitly != stage6 adaptive dual-MA (FRAMA/HMA/McGinley) and != ER-gated SMA.

Formula:
  med = (high + low) / 2
  ao = ta.sma(med, Af) - ta.sma(med, As)
  (Af, As) in {(5, 34), (5, 21), (8, 34)}; default (5, 34).

Mode A (primary):
  long: ta.crossover(ao, 0)
  exit: ta.crossunder(ao, 0) or ATR stop.

Mode B (secondary denser — Williams saucer above zero):
  long: ao[2] > ao[1] and ao > ao[1] and ao > 0
  exit: ta.crossunder(ao, 0) or ATR stop.

sol_smoke:
  Kill if: Fractals/Alligator; close-SMA dual as AO; 15m Af=3; ER/ADX graft.
  Prefer Mode A (5,34), 1H+.
  Retention: SOL n multi-dozen-class after ETH.

bnb_smoke:
  Kill if: different (Af,As); Mode B ungated shorts; no ATR.
  Prefer identical; long-only.

Forbidden: Fractals, Alligator, Gann HiLo, ER-gate, ADX, RSI, FRAMA/HMA/McGinley, close-SMA labeled AO.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, awesome_oscillator, crossover, crossunder

STRATEGY_ID = "ao-median-zero-cross-v1"


@dataclass(frozen=True)
class AoMedianParams:
    mode: str = "mode_a"  # "mode_a" (zero-cross) | "mode_b" (saucer above zero)
    fast_len: int = 5
    slow_len: int = 34
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: AoMedianParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.fast_len <= 3:
        return False, "sol_smoke: 15m Af<=3 forbidden (spam)"
    if (params.fast_len, params.slow_len) not in {(5, 34), (5, 21), (8, 34)}:
        return False, f"sol_smoke: (Af, As)=({params.fast_len}, {params.slow_len}) not in locked set"
    if params.fast_len >= params.slow_len:
        return False, "sol_smoke: fast_len >= slow_len invalid"
    return True, "PASS"


def validate_bnb_smoke(params: AoMedianParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.fast_len >= params.slow_len:
        return False, "bnb_smoke: fast_len >= slow_len invalid"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: AoMedianParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ao-median-zero-cross-v1."""
    params = params or AoMedianParams()
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
    ao_vals = awesome_oscillator(highs, lows, params.fast_len, params.slow_len)
    zeros: list[float | None] = [0.0] * n

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

        # Check exit conditions first
        if in_pos:
            exit_signal = False
            # Exit on crossunder 0
            if crossunder(ao_vals, zeros, i):
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

        # Check entry conditions if flat
        if not in_pos and i > 0:
            enter_signal = False
            if params.mode == "mode_a":
                # Mode A: crossover(ao, 0)
                if crossover(ao_vals, zeros, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: Williams saucer above zero: ao[2] > ao[1] and ao[0] > ao[1] and ao[0] > 0
                if i >= 2:
                    ao2 = ao_vals[i - 2]
                    ao1 = ao_vals[i - 1]
                    ao0 = ao_vals[i]
                    if (
                        ao2 is not None
                        and ao1 is not None
                        and ao0 is not None
                        and ao2 > ao1
                        and ao0 > ao1
                        and ao0 > 0.0
                    ):
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
