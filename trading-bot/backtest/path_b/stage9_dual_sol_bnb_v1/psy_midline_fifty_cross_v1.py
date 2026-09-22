"""psy-midline-fifty-cross-v1 — Psychological Line midline-50 cross.

LOCKED ENCODE ORDER #1 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage8 wiped AO/ROC/WMA (0 BTC) and parked thin PGO (n=9).
  PSY is a count-frequency oscillator: share of bars with close > close[1] over N
  discrete steps of 100/N, no ATR/SMA dual/path-efficiency gate.
  Midline-50 polarity flips whenever up-close majority flips — expected BTC/ETH 1H–4H n
  far above ER coincidence and PGO thr-n=9.
  Distinct from burned RSI (Wilder gains), ConnorsRSI, Stoch.
  Close-only -> identical N on SOL+BNB.

Formula:
  up = close > close[1] ? 1.0 : 0.0
  psy = 100.0 * ta.sma(up, N)
  N in {10, 12, 13, 20}; prefer 12 (conventional East-Asian default).

Mode A (primary / midline polarity):
  long: ta.crossover(psy, 50)
  exit: ta.crossunder(psy, 50) or ATR stop.

Mode B (secondary denser OS reclaim):
  long: ta.crossover(psy, 25)
  exit: ta.crossunder(psy, 50) or ATR stop.

sol_smoke:
  Kill if: RSI/Stoch grafted; 15m N=5 spam; ER/AO/PGO graft.
  Prefer Mode A N=12, 1H+.
  Retention: after ETH pass, SOL Mode-A n must remain multi-dozen-class on 6m 1H.

bnb_smoke:
  Kill if: different N than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only.

Forbidden: RSI, ConnorsRSI, Stoch, AO/ROC/PGO, request.security, m=1 RMI labeled PSY.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, psychological_line

STRATEGY_ID = "psy-midline-fifty-cross-v1"


@dataclass(frozen=True)
class PsyMidlineParams:
    mode: str = "mode_a"  # "mode_a" (cross > 50) | "mode_b" (cross > 25, exit < 50)
    length: int = 12
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: PsyMidlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m N<=5 forbidden (spam)"
    if params.length not in {10, 12, 13, 20}:
        return False, f"sol_smoke: N={params.length} not in locked set {{10, 12, 13, 20}}"
    return True, "PASS"


def validate_bnb_smoke(params: PsyMidlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PsyMidlineParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for psy-midline-fifty-cross-v1."""
    params = params or PsyMidlineParams()
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
    psy_vals = psychological_line(closes, params.length)

    fifties: list[float | None] = [50.0] * n
    twenty_fives: list[float | None] = [25.0] * n

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
            # Exit on crossunder 50
            if crossunder(psy_vals, fifties, i):
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
                # Mode A: crossover(psy, 50)
                if crossover(psy_vals, fifties, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(psy, 25)
                if crossover(psy_vals, twenty_fives, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
