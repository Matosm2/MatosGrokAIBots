"""rmi-midline-fifty-cross-v1 — Relative Momentum Index midline-50 cross.

LOCKED ENCODE ORDER #4 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Altman (TASC 1993) RMI replaces RSI's 1-bar change with m-bar momentum (m >= 3)
  then Wilder-smooths ups/downs over n. Midline-50 polarity is dense on 1H.
  Distinct from burned EMA/RSI (must lock m >= 3 — RMI(n,1) == RSI(n)),
  != CMO-zero, != ConnorsRSI.
  Close-only; identical (n,m) on SOL+BNB.

Formula:
  mom = close - close[m]
  u = math.max(mom, 0.0); d = math.max(-mom, 0.0)
  U = ta.rma(u, n); D = ta.rma(d, n); guard (U + D) > 0.
  rmi = 100.0 * U / (U + D)
  (n,m) in {(14,3),(20,5),(21,5)}; default (20,5). Hard forbid m=1.

Mode A (primary / midline):
  long: ta.crossover(rmi, 50)
  exit: ta.crossunder(rmi, 50) or ATR stop.

Mode B (secondary OS reclaim):
  long: ta.crossover(rmi, 30)
  exit: ta.crossunder(rmi, 50) or crossunder(rmi, 30) or ATR stop.

sol_smoke:
  Kill if: m=1 RSI clone; ConnorsRSI/CMO; 15m n=5 m=1 spam; ER/AO/PGO graft.
  Prefer Mode A (20,5), 1H+.
  Retention: after ETH, SOL n must stay multi-dozen-class.

bnb_smoke:
  Kill if: different (n,m) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only.

Forbidden: RSI primary; CMO-zero; ConnorsRSI; StochRSI; ER-gate; m=1.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, relative_momentum_index

STRATEGY_ID = "rmi-midline-fifty-cross-v1"


@dataclass(frozen=True)
class RmiMidlineParams:
    mode: str = "mode_a"  # "mode_a" (crossover 50) | "mode_b" (crossover 30, exit < 50)
    length: int = 20
    momentum: int = 5  # HARD m >= 3
    oversold_level: float = 30.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: RmiMidlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if params.momentum < 3:
        return False, f"sol_smoke: m={params.momentum} < 3 strictly forbidden (RSI clone)"
    if tf == "15m" and params.length <= 5 and params.momentum <= 1:
        return False, "sol_smoke: 15m n<=5 m<=1 spam forbidden"
    if (params.length, params.momentum) not in {(14, 3), (20, 5), (21, 5)}:
        return False, f"sol_smoke: (n,m)=({params.length},{params.momentum}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: RmiMidlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.momentum < 3:
        return False, f"bnb_smoke: m={params.momentum} < 3 strictly forbidden (RSI clone)"
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: RmiMidlineParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for rmi-midline-fifty-cross-v1."""
    params = params or RmiMidlineParams()
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
    rmi_vals = relative_momentum_index(closes, params.length, params.momentum)

    fifties: list[float | None] = [50.0] * n
    thirties: list[float | None] = [params.oversold_level] * n

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
                if crossunder(rmi_vals, fifties, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit on crossunder 50 or crossunder 30
                if crossunder(rmi_vals, fifties, i) or crossunder(rmi_vals, thirties, i):
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
                # Mode A: crossover(rmi, 50)
                if crossover(rmi_vals, fifties, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(rmi, 30)
                if crossover(rmi_vals, thirties, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
