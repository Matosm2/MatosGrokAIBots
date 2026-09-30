"""Stage 23 Chande Kroll Optimize v1 package.

Track B OPTIMIZE — single ID: chande-kroll-stop-flip
Two-stage ATR corridor stop-flip:
  atr = ta.atr(p)
  highStop = ta.highest(high, p) - x * atr
  lowStop = ta.lowest(low, p) + x * atr
  stopShort = ta.highest(highStop, q)
  stopLong = ta.lowest(lowStop, q)

Mode A: crossover(close, stopShort) long; exit crossunder(close, stopLong).
Mode B: width (stopShort - stopLong) percentrank > wMin.
"""

from backtest.path_b.stage23_chande_kroll_optimize_v1.indicators import (
    chande_kroll_stops,
    percent_rank,
    true_range,
    wilder_atr,
)
from backtest.path_b.stage23_chande_kroll_optimize_v1.signals import (
    ChandeKrollParams,
    ChandeKrollSignals,
    compute_chande_kroll_signals,
)

__all__ = [
    "ChandeKrollParams",
    "ChandeKrollSignals",
    "chande_kroll_stops",
    "compute_chande_kroll_signals",
    "percent_rank",
    "true_range",
    "wilder_atr",
]
