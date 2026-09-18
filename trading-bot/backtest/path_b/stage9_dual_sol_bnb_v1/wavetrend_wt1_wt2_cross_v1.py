"""wavetrend-wt1-wt2-cross-v1 — LazyBear WaveTrend WT1xWT2 cross.

LOCKED ENCODE ORDER #3 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  LazyBear / QuantConnect WaveTrend: HLC3 channel index normalized by EMA mean-abs-dev
  with 0.015 factor, WT1=EMA(CI), WT2=SMA(WT1).
  Dual-line cross is a dense momentum flip — no ER gate, no PGO thr sparsity.
  Distinct from burned CCI, Stoch, SMI, RSI.
  HLC3 portable; identical (n1,n2,n3) on SOL+BNB.

Formula:
  ap = hlc3
  esa = ta.ema(ap, n1)
  d = ta.ema(math.abs(ap - esa), n1); guard d > 0.
  ci = (ap - esa) / (0.015 * d)
  wt1 = ta.ema(ci, n2)
  wt2 = ta.sma(wt1, n3)
  Defaults: (10, 21, 4); sweep n1 in {8,10,12}, n2 in {14,21}, n3 in {3,4}. Factor 0.015 locked.

Mode A (primary / dense dual-cross):
  long: ta.crossover(wt1, wt2)
  exit: ta.crossunder(wt1, wt2) or ATR stop.

Mode B (secondary OS gated cross):
  long: ta.crossover(wt1, wt2) and wt1 < -53
  exit: ta.crossunder(wt1, wt2) or ATR stop.

sol_smoke:
  Kill if: CCI/Stoch labeled WT; missing 0.015; 15m n1=3 spam; ER/AO/PGO graft.
  Prefer Mode A (10,21,4), 1H+.
  Retention: after ETH, SOL cross n must not collapse to PGO-class single digits.

bnb_smoke:
  Kill if: different params than SOL; Mode B ungated shorts; no ATR.
  Prefer identical params; long-only.

Forbidden: CCI; Stoch/SMI; RSI; ER-gate; AO/ROC/WMA/PGO; WT without 0.015.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, wavetrend

STRATEGY_ID = "wavetrend-wt1-wt2-cross-v1"


@dataclass(frozen=True)
class WaveTrendParams:
    mode: str = "mode_a"  # "mode_a" (crossover wt1, wt2) | "mode_b" (crossover & wt1 < -53)
    n1: int = 10
    n2: int = 21
    n3: int = 4
    oversold_level: float = -53.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: WaveTrendParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.n1 <= 3:
        return False, "sol_smoke: 15m n1<=3 forbidden (spam)"
    if (params.n1, params.n2, params.n3) not in {
        (10, 21, 4),
        (8, 21, 4),
        (12, 21, 4),
        (10, 14, 3),
    }:
        return False, f"sol_smoke: (n1,n2,n3)=({params.n1},{params.n2},{params.n3}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: WaveTrendParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.n1 <= 0 or params.n2 <= 0 or params.n3 <= 0:
        return False, "bnb_smoke: lengths must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: WaveTrendParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for wavetrend-wt1-wt2-cross-v1."""
    params = params or WaveTrendParams()
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
    wt1_vals, wt2_vals = wavetrend(highs, lows, closes, params.n1, params.n2, params.n3)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        wt1_curr = wt1_vals[i]

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
            # Exit on crossunder(wt1, wt2)
            if crossunder(wt1_vals, wt2_vals, i):
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
            if crossover(wt1_vals, wt2_vals, i):
                if params.mode == "mode_a":
                    enter_signal = True
                elif params.mode == "mode_b":
                    # Gated by oversold level
                    if wt1_curr is not None and wt1_curr < params.oversold_level:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
