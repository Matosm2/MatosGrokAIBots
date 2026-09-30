"""vwma-sma-cross-v1 — Volume-Weighted MA × Simple MA Crossover.

LOCKED SPEC:
Indicators:
  ta.vwma(close, len_v) + ta.sma(close, len_s).
  Prefer same-length first (classic VWMA vs SMA state) or fast VWMA × slow SMA.
  Lengths sweep: {10, 20, 34, 50}; pairs: (10, 20), (20, 50).

Entry Mode A (primary):
  Long: ta.crossover(vwma, sma) (closed-bar).
  (Lead is long-only first pass).

Entry Mode B (state filter):
  Long while vwma > sma and close > vwma and close > sma (fewer flips).
  Mode A first for n.

Exit:
  Opposite cross (ta.crossunder(vwma, sma) / vwma < sma); or optional ATR trail stop.

≠ VWAP / AVWAP ± sigma bands; ≠ ALMA; ≠ EMA ribbon; ≠ OBV/CMF grafts.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, sma, vwma

STRATEGY_ID = "vwma-sma-cross-v1"


@dataclass(frozen=True)
class VwmaSmaParams:
    vwma_len: int = 20
    sma_len: int = 20
    mode: str = "mode_a"  # "mode_a" (crossover) | "mode_b" (state filter: vwma > sma & close > both)
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: VwmaSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vwma-sma-cross-v1."""
    params = params or VwmaSmaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    vols = [b.volume for b in bars]

    vwma_vals = vwma(closes, vols, params.vwma_len)
    sma_vals = sma(closes, params.sma_len)

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    mode = params.mode.lower()
    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        v = vwma_vals[i]
        s = sma_vals[i]
        if v is None or s is None:
            continue

        c = closes[i]

        if mode == "mode_a":
            entry_sig = crossover(vwma_vals, sma_vals, i)
            exit_sig = crossunder(vwma_vals, sma_vals, i)
        else:  # mode_b
            # Enter when condition becomes true: vwma > sma and close > both
            prev_v = vwma_vals[i - 1] if i > 0 else None
            prev_s = sma_vals[i - 1] if i > 0 else None
            prev_c = closes[i - 1] if i > 0 else 0.0
            cond_now = v > s and c > v and c > s
            cond_prev = prev_v is not None and prev_s is not None and prev_v > prev_s and prev_c > prev_v and prev_c > prev_s
            entry_sig = cond_now and not cond_prev
            exit_sig = v < s or c < min(v, s)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, c)

            hit_exit = False
            if exit_sig:
                hit_exit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if c < stop_level:
                    hit_exit = True

            if hit_exit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if entry_sig:
            buys[i] = True
            in_pos = True
            highest_since_entry = c
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = c - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level
            else:
                stop_level = None

    return buys, sells, stops
