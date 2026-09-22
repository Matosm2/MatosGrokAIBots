"""pgo-threshold-zeroexit-v1 — Pretty Good Oscillator threshold breakout + zero exit.

LOCKED ENCODE ORDER #2 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Unused Mark Johnson oscillator: close displacement from SMA in ATR-equivalent units.
  Continuous line with fixed thresholds, NOT a percentile rank (≠ stage5 ATR%ile-primary)
  and NOT Keltner band overlay (burned).
  Entry on +thr breakout; exit on return to 0 (close back at SMA).
  Short lookbacks (14/21) keep BTC/ETH trade counts dense vs stage7 ER gate.
  Identical (N, thr) on SOL+BNB; OHLC portable.

Formula:
  sma = ta.sma(close, N)
  den = ta.ema(ta.tr(true), N)
  pgo = (close - sma) / den; guard den > 0.
  N in {14, 21, 34}; thr in {2.0, 2.5, 3.0}; prefer N=14 thr=2.5 first.

Mode A (primary / Johnson):
  long: ta.crossover(pgo, thr)
  exit: ta.crossunder(pgo, 0) or pgo <= 0 (zero return) or ATR stop.

Mode B (secondary denser):
  long while pgo > thr * 0.5 and close > sma — only if Mode A under-fires SOL.
  exit: ta.crossunder(pgo, 0) or pgo <= 0 or ATR stop.

sol_smoke:
  Kill if: ATR%ile gate; Keltner/BB substitute; N=89 on 15m; ER graft.
  Prefer Mode A N=14 thr=2.5, 1H+.
  Retention: SOL must still print thr crosses after ETH (try thr=2.5 before kill if thr=3 silent).

bnb_smoke:
  Kill if: per-coin thr/N; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: ATR%ile-primary; Keltner; BB-squeeze; ER-gate; SMA±k·ATR labeled PGO.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, pretty_good_oscillator, sma

STRATEGY_ID = "pgo-threshold-zeroexit-v1"


@dataclass(frozen=True)
class PgoThresholdParams:
    mode: str = "mode_a"  # "mode_a" (thr crossover + zero exit) | "mode_b" (pgo > thr*0.5 & close > sma)
    length: int = 14
    threshold: float = 2.5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: PgoThresholdParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length >= 89:
        return False, "sol_smoke: N>=89 on 15m forbidden (too sparse / wrong TF)"
    if params.length not in {14, 21, 34}:
        return False, f"sol_smoke: N={params.length} not in locked set {{14, 21, 34}}"
    if params.threshold not in {2.0, 2.5, 3.0}:
        return False, f"sol_smoke: thr={params.threshold} not in locked set {{2.0, 2.5, 3.0}}"
    return True, "PASS"


def validate_bnb_smoke(params: PgoThresholdParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.threshold <= 0:
        return False, "bnb_smoke: threshold must be > 0"
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PgoThresholdParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pgo-threshold-zeroexit-v1."""
    params = params or PgoThresholdParams()
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
    pgo_vals = pretty_good_oscillator(highs, lows, closes, params.length)
    sma_vals = sma(closes, params.length)

    thr_levels: list[float | None] = [params.threshold] * n
    zeros: list[float | None] = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        pgo_curr = pgo_vals[i]

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
            # Exit on return to 0: crossunder 0 or pgo <= 0
            if crossunder(pgo_vals, zeros, i) or (pgo_curr is not None and pgo_curr <= 0.0):
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
                # Mode A: crossover(pgo, thr)
                if crossover(pgo_vals, thr_levels, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: pgo > thr * 0.5 and close > sma
                s_val = sma_vals[i]
                if (
                    pgo_curr is not None
                    and s_val is not None
                    and pgo_curr > (params.threshold * 0.5)
                    and c > s_val
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
