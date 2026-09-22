"""hma-dual-cross-v1 — Hull Moving Average Dual Cross (low lag).

LOCKED ENCODE ORDER #2 (DUAL-SURVIVAL: SOL + BNB lean).
Thesis:
  HMA = WMA(2 * WMA(n/2) - WMA(n), round(sqrt(n)))
  Low-lag smoother designed to retain SOL trend density after ETH pass better than
  stage5 CTI lag (~L/2) or VIDYA flatten.
  Dual HMA cross is majors-portable (close-only), dense enough for SOL 1H-4H trades,
  and identical on BNB without volume-shape dependence.
  Explicitly distinct from ALMA, T3, ZLEMA, KAMA, SuperSmoother.

Mode A (primary):
  fast = HMA(Lf)
  slow = HMA(Ls)
  Long entry: ta.crossover(fast, slow)
  Exit: ta.crossunder(fast, slow) or ATR stop.
  (Lf, Ls) in {(9, 16), (10, 30), (16, 36)}.

Mode B (secondary):
  close x HMA(Ls) — only if Mode A SOL under-fires.

sol_smoke:
  Kill if: ZLEMA/ALMA/T3 substitute; 15m length soup; EMA ribbon.
  Prefer Mode A (9,16) or (10,30), 1H+.
  Retention check: SOL trade density after ETH must stay roughly >= ETH density (same params);
  if HMA dual goes silent on SOL while ETH traded -> kill.

bnb_smoke:
  Kill if: per-coin length retune; Lf<=5; no ATR (when stop enabled).
  Prefer identical (Lf, Ls); long-only.

Forbidden: ALMA, T3, ZLEMA, KAMA, SuperSmoother, EMA ribbon, SMA200, RSI graft.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, hma

STRATEGY_ID = "hma-dual-cross-v1"


@dataclass(frozen=True)
class HmaParams:
    mode: str = "mode_a"  # "mode_a" (dual HMA) | "mode_b" (close x HMA)
    fast_len: int = 9
    slow_len: int = 16
    hma_b_len: int = 30
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: HmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m length soup forbidden"
    if params.mode == "mode_a" and (params.fast_len, params.slow_len) not in {
        (9, 16),
        (10, 30),
        (16, 36),
    }:
        return False, f"sol_smoke: (Lf, Ls)=({params.fast_len}, {params.slow_len}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: HmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.fast_len <= 5:
        return False, "bnb_smoke: Lf<=5 forbidden (noise/spam)"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: HmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for hma-dual-cross-v1."""
    params = params or HmaParams()
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
        fast_series = hma(closes, params.fast_len)
        slow_series = hma(closes, params.slow_len)
    else:
        fast_series = [float(c) for c in closes]
        slow_series = hma(closes, params.hma_b_len)

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
