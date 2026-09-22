"""vidya-dual-or-close-cross-v1 — Chande Variable Index Dynamic Average (VIDYA) Dual Cross.

LOCKED ENCODE ORDER #4 (DUAL-SURVIVAL: SOL + BNB).
Thesis:
  Chande VIDYA dynamically adapts its smoothing speed using the Chande Momentum Oscillator (CMO).
  When momentum collapses (|CMO| -> 0), the effective alpha approaches zero and VIDYA flattens,
  preventing whipsaws in choppy markets (BNB benefit). When momentum expands (|CMO| -> 100),
  alpha accelerates up to standard EMA speed (SOL benefit).
  Distinct from burned KAMA (Kaufman ER) and excluded CMO-zero-cross (CMO is only the adaptive speed).

Formula:
  cmo = ta.cmo(close, cmoLen) in [-100, +100]
  F = 2.0 / (emaLen + 1)
  alpha = F * abs(cmo) / 100.0
  vidya[t] = alpha * close[t] + (1 - alpha) * vidya[t-1]

CMO Scale Convention Lock:
  CMO is computed as 100 * (Su - Sd) / (Su + Sd) in [-100, +100].
  Dividing by 100.0 maps absolute momentum to [0.0, 1.0].
  Effective smoothing weight = F * (|CMO| / 100.0) in [0.0, F].

Mode A (primary):
  Fast VIDYA(emaLen=9, cmoLen=12) x slow VIDYA(20, 50).
  Long: ta.crossover(fast, slow).

Mode B:
  close x VIDYA(emaLen=20, cmoLen=9).

Optional slopeMin (mandatory ON for BNB smoke):
  Requires abs(vidya - vidya[1]) / close > slopeMin to prevent entries during flat drift.

Exit:
  Opposite cross; ATR trail stop.

Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, vidya

STRATEGY_ID = "vidya-dual-or-close-cross-v1"


@dataclass(frozen=True)
class VidyaParams:
    mode: str = "mode_a"  # "mode_a" (dual VIDYA) | "mode_b" (close x VIDYA)
    fast_ema_len: int = 9
    fast_cmo_len: int = 12
    slow_ema_len: int = 20
    slow_cmo_len: int = 50
    vidya_b_ema_len: int = 20
    vidya_b_cmo_len: int = 9
    slope_min: float = 0.0003  # slope floor |vidya - vidya[1]| / close
    slope_filter: bool = True  # ON for BNB smoke
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: VidyaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m dual soup forbidden"
    return True, "PASS"


def validate_bnb_smoke(params: VidyaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if not params.slope_filter or params.slope_min <= 0.0:
        return False, "bnb_smoke: slopeMin / flat-trade filter must be ON"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VidyaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vidya-dual-or-close-cross-v1."""
    params = params or VidyaParams()
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
        fast_v = vidya(closes, params.fast_ema_len, params.fast_cmo_len)
        slow_v = vidya(closes, params.slow_ema_len, params.slow_cmo_len)
    else:
        fast_v = [float(c) for c in closes]
        slow_v = vidya(closes, params.vidya_b_ema_len, params.vidya_b_cmo_len)

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
            if crossunder(fast_v, slow_v, i):
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
        if not in_pos and i > 0 and slow_v[i] is not None and slow_v[i - 1] is not None:
            # Slope check on the reference VIDYA line
            ref_v = slow_v
            slope_ok = True
            if params.slope_filter and params.slope_min > 0.0 and c > 0:
                slope_val = abs(ref_v[i] - ref_v[i - 1]) / c  # type: ignore[operator]
                slope_ok = slope_val >= params.slope_min

            enter_signal = False
            if slope_ok and crossover(fast_v, slow_v, i):
                enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
