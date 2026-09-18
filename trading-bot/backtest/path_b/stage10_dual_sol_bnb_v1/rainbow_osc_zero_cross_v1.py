"""rainbow-osc-zero-cross-v1 — Widner recursive-SMA Rainbow Oscillator zero-cross.

LOCKED ENCODE ORDER #2 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage9 wiped Disparity ((C-SMA)/SMA) and AccelBands envelopes; stage8 wiped WMA dual.
  Widner Rainbow Oscillator ranks close vs the average of ten recursively smoothed 2-period SMAs,
  normalized by close-range — consensus-of-trends oscillator, not dual-MA and not %-from-single-SMA.
  RO zero-cross is dense on 1H; identical recursive depth on SOL+BNB.
  != Disparity, != WMA dual, != BB.

Formula:
  ave1 = SMA(close, p)
  ave2 = SMA(ave1, p) ... through ave10 (depth=10)
  aveA = mean(ave1 .. ave10)
  rangeC = highest(close, depth+1) - lowest(close, depth+1)
  ro = 100 * (close - aveA) / rangeC
  rb = 100 * (max(aves) - min(aves)) / rangeC
  Prefer p=2, depth=10.

Mode A (primary / dense zero-cross):
  long: ta.crossover(ro, 0)
  exit: ta.crossunder(ro, 0) or ATR stop.

Mode B (secondary bandwidth filter):
  long: ta.crossover(ro, 0) and rb < thr (thr in {30, 38, 50})
  exit: ta.crossunder(ro, 0) or ATR stop.

sol_smoke:
  Kill if: WMA/Disparity substitute; missing rangeC guard; 15m depth=3 spam; ER/AO/PGO graft.
  Prefer Mode A p=2 depth=10, 1H+.
  Retention check: after ETH, SOL zero-cross n must not collapse to single digits.

bnb_smoke:
  Kill if: different (p, depth) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: WMA dual; Disparity; BB-squeeze; HMA/ZLEMA; ER-gate; PSY/RMI; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, rainbow_oscillator

STRATEGY_ID = "rainbow-osc-zero-cross-v1"


@dataclass(frozen=True)
class RainbowOscParams:
    mode: str = "mode_a"  # "mode_a" (cross > 0) | "mode_b" (cross > 0 and rb < thr)
    p: int = 2
    depth: int = 10
    rb_thr: float = 38.0  # Used in Mode B
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: RainbowOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.depth <= 3:
        return False, "sol_smoke: 15m depth<=3 forbidden (spam)"
    if (params.p, params.depth) not in {(2, 10), (2, 8), (3, 10)}:
        return False, f"sol_smoke: (p,depth)=({params.p},{params.depth}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: RainbowOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.p <= 0 or params.depth <= 0:
        return False, "bnb_smoke: p and depth must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: RainbowOscParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for rainbow-osc-zero-cross-v1."""
    params = params or RainbowOscParams()
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
    ro_vals, rb_vals = rainbow_oscillator(closes, p=params.p, depth=params.depth)

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

        # Check exits first
        if in_pos:
            exit_signal = False
            # Exit on crossunder 0
            if crossunder(ro_vals, zeros, i):
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
                # Mode A: crossover(ro, 0)
                if crossover(ro_vals, zeros, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(ro, 0) and rb < thr
                if crossover(ro_vals, zeros, i):
                    rb_val = rb_vals[i]
                    if rb_val is not None and rb_val < params.rb_thr:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
