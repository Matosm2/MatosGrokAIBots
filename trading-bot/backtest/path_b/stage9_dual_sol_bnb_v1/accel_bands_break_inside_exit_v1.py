"""accel-bands-break-inside-exit-v1 — Acceleration Bands break upper + inside exit.

LOCKED ENCODE ORDER #5 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Price Headley bands: SMA of highs/lows scaled by each bar's own (H-L)/(H+L) factor (* k).
  Breakout when close outside upper band; exit when close returns inside.
  Distinct from burned Keltner (ATR offset), BB-squeeze (stddev), Donchian (raw extremes),
  ATR%ile-primary, Chandelier.
  Mode A uses single closed-bar outside for density. Mode B uses two consecutive closes.
  Identical (N, k) on SOL+BNB; OHLC portable.

Formula:
  rng = (high - low) / (high + low); guard high + low > 0.
  upSrc = high * (1.0 + k * rng)
  dnSrc = low * (1.0 - k * rng)
  upper = ta.sma(upSrc, N)
  lower = ta.sma(dnSrc, N)
  mid = ta.sma(close, N)
  N in {14, 20, 30}; k in {3.0, 4.0}; prefer N=20 k=4.

Mode A (primary / density-first single close):
  long: close > upper and close[1] <= upper[1]
  exit: close < upper (or close <= mid) or ATR stop.

Mode B (secondary classic two-bar):
  long: close > upper and close[1] > upper[1]
  exit: close < upper or ATR stop.

sol_smoke:
  Kill if: Keltner/BB/Donchian substitute; ATR%ile graft; 15m N=5 spam; ER/AO/PGO graft.
  Prefer Mode A N=20 k=4, 1H+.
  Retention: after ETH, if SOL n collapses to single digits, try Mode A before kill (same params, not per-coin).

bnb_smoke:
  Kill if: different (N,k) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only.

Forbidden: Keltner; BB-squeeze; Donchian; ATR%ile; Chandelier-primary; ER-gate; AO/ROC/WMA/PGO.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import acceleration_bands, atr

STRATEGY_ID = "accel-bands-break-inside-exit-v1"


@dataclass(frozen=True)
class AccelBandsParams:
    mode: str = "mode_a"  # "mode_a" (1-bar close > upper) | "mode_b" (2-bar close > upper)
    length: int = 20
    k: float = 4.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: AccelBandsParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m N<=5 forbidden (spam)"
    if params.length not in {14, 20, 30}:
        return False, f"sol_smoke: N={params.length} not in locked set {{14, 20, 30}}"
    if params.k not in {3.0, 4.0}:
        return False, f"sol_smoke: k={params.k} not in locked set {{3.0, 4.0}}"
    return True, "PASS"


def validate_bnb_smoke(params: AccelBandsParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    if params.k <= 0:
        return False, "bnb_smoke: k must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: AccelBandsParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for accel-bands-break-inside-exit-v1."""
    params = params or AccelBandsParams()
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
    upper_vals, lower_vals, mid_vals = acceleration_bands(
        highs, lows, closes, params.length, params.k
    )

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        up_curr = upper_vals[i]

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
            # Exit when close falls back inside (close < upper)
            if up_curr is not None and c < up_curr:
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
        if not in_pos and i > 1:
            enter_signal = False
            up_prev = upper_vals[i - 1]
            c_prev = closes[i - 1]

            if up_curr is not None and up_prev is not None:
                if params.mode == "mode_a":
                    # Mode A: close > upper and close[1] <= upper[1]
                    if c > up_curr and c_prev <= up_prev:
                        enter_signal = True
                elif params.mode == "mode_b":
                    # Mode B: close > upper and close[1] > upper[1]
                    if c > up_curr and c_prev > up_prev:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
