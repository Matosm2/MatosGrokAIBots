"""frama-fast-slow-cross-v1 — Ehlers Fractal Adaptive Moving Average Dual Cross.

LOCKED ENCODE ORDER #1 (DUAL-SURVIVAL: SOL + BNB lean).
Thesis:
  FRAMA sets exponential smoothing alpha dynamically from the fractal dimension (FD)
  of price ranges over split halves of lookback window N (even), not Kaufman ER (burned KAMA)
  and not Chande CMO (|CMO| VIDYA that cleared ETH then died on SOL).
  When SOL trends (smooth path -> low FD -> alpha increases), FRAMA accelerates and dual-cross
  stays with the trend leg — enabling SOL edge retention after ETH pass.
  Identical OHLC construction applies to BNB without venue volume quirks.

Formula (MESA / Ehlers S&C Oct 2005):
  N even: window split into halves (half = N // 2).
  N1 = (max(highs[first_half]) - min(lows[first_half])) / half
  N2 = (max(highs[second_half]) - min(lows[second_half])) / half
  N3 = (max(highs[full_window]) - min(lows[full_window])) / N
  FD = (log(N1 + N2) - log(N3)) / log(2.0), clamped to [1.0, 2.0]
  alpha = exp(-4.6 * (FD - 1.0)), clamped to [0.01, 1.0]
  FRAMA[t] = alpha * close[t] + (1 - alpha) * FRAMA[t-1]

Mode A (primary):
  fast = FRAMA(Nf)
  slow = FRAMA(Ns)
  Long entry: ta.crossover(fast, slow)
  Exit: ta.crossunder(fast, slow) or ATR stop.
  (Nf, Ns) in {(16, 32), (10, 20), (12, 24)} — N even.

Mode B (secondary):
  close x FRAMA(N) — only if Mode A SOL under-trades.

sol_smoke:
  Kill if: KAMA/ER alpha; VIDYA/CMO alpha; SuperTrend graft; Mode B-only on 15m;
  odd N without even halves. Prefer Mode A (16,32) or (10,20), 1H+.
  Retention: after ETH pass, SOL Mode-A trade count / trend-leg capture must not collapse vs ETH;
  if FRAMA flat during SOL impulse -> kill (over-smooth).

bnb_smoke:
  Kill if: retune N per coin; Nf=6 on 1H (spam); no ATR exit (when exit enabled).
  Prefer identical lengths; long-only first.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, frama

STRATEGY_ID = "frama-fast-slow-cross-v1"


@dataclass(frozen=True)
class FramaParams:
    mode: str = "mode_a"  # "mode_a" (dual FRAMA) | "mode_b" (close x FRAMA)
    fast_len: int = 16
    slow_len: int = 32
    frama_b_len: int = 20
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: FramaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.mode == "mode_b":
        return False, "sol_smoke: Mode B-only on 15m forbidden"
    if params.fast_len % 2 != 0 or params.slow_len % 2 != 0:
        return False, "sol_smoke: odd N without even-window halves forbidden"
    if params.mode == "mode_a" and (params.fast_len, params.slow_len) not in {
        (16, 32),
        (10, 20),
        (12, 24),
    }:
        return False, f"sol_smoke: (Nf, Ns)=({params.fast_len}, {params.slow_len}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: FramaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if tf == "1h" and params.fast_len <= 6:
        return False, "bnb_smoke: Nf<=6 on 1H forbidden (spam)"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: FramaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for frama-fast-slow-cross-v1."""
    params = params or FramaParams()
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

    if params.mode == "mode_a":
        fast_series = frama(highs, lows, closes, params.fast_len)
        slow_series = frama(highs, lows, closes, params.slow_len)
    else:
        fast_series = [float(c) for c in closes]
        slow_series = frama(highs, lows, closes, params.frama_b_len)

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
            if crossunder(fast_series, slow_series, i):
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
        if not in_pos and i > 0 and slow_series[i] is not None and slow_series[i - 1] is not None:
            enter_signal = False
            if crossover(fast_series, slow_series, i):
                enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
