"""roc-zero-cross-v1 — Rate of Change zero-line cross.

LOCKED ENCODE ORDER #3 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Pure momentum oscillator: ROC = 100 * (close / close[N] - 1).
  StockCharts centerline cross identifies trend polarity.
  Short N (9/12/14/21) -> very dense zero-touches on 1H majors — anti-pattern to stage7 ER sparse gate.
  Distinct from burned dual-mom (cross-sectional ranking), KST (multi-ROC composite),
  TRIX (triple-EMA ROC), Coppock.
  Close-only -> identical N on SOL+BNB.

Formula:
  roc = 100.0 * (close / close[N] - 1.0)
  N in {9, 12, 14, 21}; prefer 12 (ChartSchool default).

Mode A (primary / centerline):
  long: ta.crossover(roc, 0)
  exit: ta.crossunder(roc, 0) or ATR stop.

Mode B (secondary — oversold reclaim):
  long: ta.crossover(roc, -ext) where ext in {5, 8, 10}; default ext=8.
  exit: ta.crossunder(roc, 0) or ATR stop.

sol_smoke:
  Kill if: KST/TRIX/Coppock substitute; dual-mom rank; SMA200 filter; 15m N=3 spam.
  Prefer Mode A N=12, 1H+.
  Retention: SOL n after ETH should stay dense; if ROC stuck positive through dumps without exit cross, kill.

bnb_smoke:
  Kill if: different N than SOL; Mode B extremes-only shorts ungated; no ATR.
  Prefer identical N; long-only; ATR exit.

Forbidden: dual-mom ranking; KST; TRIX; Coppock; SMA200 graft; RSI; ER-gate; ROC-of-ROC.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, roc

STRATEGY_ID = "roc-zero-cross-v1"


@dataclass(frozen=True)
class RocZeroCrossParams:
    mode: str = "mode_a"  # "mode_a" (zero crossover) | "mode_b" (oversold reclaim: cross > -ext)
    length: int = 12
    oversold_ext: float = 8.0  # ext in {5, 8, 10} for mode_b
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: RocZeroCrossParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 3:
        return False, "sol_smoke: 15m N<=3 forbidden (spam)"
    if params.length not in {9, 12, 14, 21}:
        return False, f"sol_smoke: N={params.length} not in locked set {{9, 12, 14, 21}}"
    return True, "PASS"


def validate_bnb_smoke(params: RocZeroCrossParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: RocZeroCrossParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for roc-zero-cross-v1."""
    params = params or RocZeroCrossParams()
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
    roc_vals = roc(closes, params.length)

    zeros: list[float | None] = [0.0] * n
    neg_ext_levels: list[float | None] = [-params.oversold_ext] * n

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
            if crossunder(roc_vals, zeros, i):
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
                # Mode A: crossover(roc, 0)
                if crossover(roc_vals, zeros, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(roc, -ext)
                if crossover(roc_vals, neg_ext_levels, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
