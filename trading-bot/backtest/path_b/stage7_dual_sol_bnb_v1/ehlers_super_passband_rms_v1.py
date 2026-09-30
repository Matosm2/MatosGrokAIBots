"""ehlers-super-passband-rms-v1 — Ehlers Super Passband Filter +/- RMS envelope.

LOCKED ENCODE ORDER #2 (DUAL-SURVIVAL: SOL + BNB survival).
Thesis:
  Unused Ehlers bandpass oscillator (S&C Jul 2016): difference of two fast EMAs with
  alpha = 5 / Period (not ta.ema default alpha = 2/(N+1), not MACD defaults).
  Rejects very low and high frequencies -> oscillator with RMS cyclic envelope triggers.
  Distinct from burned/excluded Roofing, CyberCycle, Decycler, ITrend, SuperSmoother, FRAMA, CG.
  Close-only -> dual SOL+BNB identical (P1, P2, rmsLen).

Formula (S&C Jul 2016):
  a1 = 5.0 / P1; a2 = 5.0 / P2
  c0 = a1 - a2
  c1 = a2*(1-a1) - a1*(1-a2)
  c2 = (1-a1) + (1-a2)
  c3 = (1-a1) * (1-a2)
  PB[t] = c0*close[t] + c1*close[t-1] + c2*PB[t-1] - c3*PB[t-2]
  rms = sqrt(sma(PB^2, rmsLen))

Mode A (primary / article rules):
  long: ta.crossover(pb, -rms)
  exit: ta.crossunder(pb, rms) or ta.crossunder(pb, -rms) or ATR stop.
  (P1, P2) in {(20, 40), (30, 50), (40, 60)} with P1 < P2; rmsLen in {40, 50}.

Mode B (secondary):
  PB zero-cross only — secondary if Mode A under-trades SOL.

sol_smoke:
  Kill if: Roofing substitute; MACD(12,26,9) labeled passband; 15m P1=10.
  Prefer Mode A (40,60) or (30,50), rmsLen=50, 1H+.
  Retention check: SOL Mode-A n after ETH must not go silent.

bnb_smoke:
  Kill if: retune P1/P2 per coin; Mode B-only shorts ungated; no ATR.
  Prefer identical periods; long-only.

Forbidden: Roofing/HP, SuperSmoother, Decycler, ITrend, FRAMA, HMA, McGinley, classic MACD.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_super_passband, rms

STRATEGY_ID = "ehlers-super-passband-rms-v1"


@dataclass(frozen=True)
class SuperPassbandParams:
    mode: str = "mode_a"  # "mode_a" (crossover pb x -rms) | "mode_b" (pb zero-cross)
    p1: int = 40
    p2: int = 60
    rms_len: int = 50
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: SuperPassbandParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.p1 <= 10:
        return False, "sol_smoke: 15m P1<=10 forbidden (spam)"
    if params.p1 >= params.p2:
        return False, "sol_smoke: P1 must be strictly < P2"
    if (params.p1, params.p2) not in {(20, 40), (30, 50), (40, 60)}:
        return False, f"sol_smoke: (P1, P2)=({params.p1}, {params.p2}) not in locked set"
    if params.rms_len not in {40, 50}:
        return False, f"sol_smoke: rmsLen={params.rms_len} not in locked set {{40, 50}}"
    return True, "PASS"


def validate_bnb_smoke(params: SuperPassbandParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.p1 >= params.p2:
        return False, "bnb_smoke: P1 >= P2 invalid"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: SuperPassbandParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-super-passband-rms-v1."""
    params = params or SuperPassbandParams()
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
    pb_vals = ehlers_super_passband(closes, params.p1, params.p2)
    rms_vals = rms(pb_vals, params.rms_len)

    # Calculate neg_rms = -rms
    neg_rms_vals: list[float | None] = [
        (-r if r is not None else None) for r in rms_vals
    ]
    zeros: list[float | None] = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

        # Trailing stop update if in position
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
                # Exit when pb crosses under +rms or pb crosses under -rms
                if crossunder(pb_vals, rms_vals, i) or crossunder(pb_vals, neg_rms_vals, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit on pb crossunder zero
                if crossunder(pb_vals, zeros, i):
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
        if not in_pos and i > 0 and pb_vals[i] is not None:
            enter_signal = False

            if params.mode == "mode_a":
                # Long entry: crossover(pb, -rms)
                if neg_rms_vals[i] is not None and crossover(pb_vals, neg_rms_vals, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Long entry: crossover(pb, 0)
                if crossover(pb_vals, zeros, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
