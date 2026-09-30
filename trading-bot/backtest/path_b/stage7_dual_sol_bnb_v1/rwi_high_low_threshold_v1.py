"""rwi-high-low-threshold-v1 — Mike Poulos Random Walk Index long/short dual-horizon.

LOCKED ENCODE ORDER #3 (DUAL-SURVIVAL: SOL + BNB survival).
Thesis:
  Statistical displacement vs random-walk noise, not a moving average and not stage5 ATR%ile rank.
  RWI High/Low = max over lookbacks i of (range displacement) / (ATR_i * sqrt(i)).
  Readings > 1 claim trend exceeds random walk.
  Poulos dual-horizon rules: long when long-term RWI High > 1 and short-term RWI Low peaks above 1
  (pullback-in-uptrend class).
  Distinct from Donchian/SuperTrend/ADX burns and ATR%ile primary.
  OHLC portable; identical (S, L) on SOL+BNB.

Formula (Michael Poulos):
  For each i in [2, period]:
    RWI_High(i) = (High - Low[i]) / (ATR(i) * sqrt(i))
    RWI_Low(i) = (High[i] - Low) / (ATR(i) * sqrt(i))
  max across i.

Mode A (primary / Poulos):
  rwiH_L = max RWI_High(i) for i <= L
  rwiL_S = max RWI_Low(i) for i <= S
  long when rwiH_L > thr and rwiL_S > thr and rwiL_S > rwiL_S[1] (ST Low peak confirm)
  exit when rwiH_L < thr or rwiL_L > rwiH_L or ATR stop.
  (S, L) in {(5, 40), (7, 64), (8, 48)}. thr = 1.0 first.

Mode B (secondary denser):
  long while rwiH_L > thr and rwiH_L > rwiL_L — denser secondary.

sol_smoke:
  Kill if: ATR%ile percentile grafted as entry; Donchian/SuperTrend substitute; S=2 on 15m.
  Prefer Mode A (7,64) or (5,40), 1H+.
  Retention check: SOL must produce ST Low peaks during LT uptrend after ETH.

bnb_smoke:
  Kill if: per-coin (S, L) retune; thr lowered only on BNB; no ATR.
  Prefer identical params; long-only.

Forbidden: ATR%ile-primary, SuperTrend, Donchian, ADX, FRAMA, HMA, McGinley.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, rwi_high_low

STRATEGY_ID = "rwi-high-low-threshold-v1"


@dataclass(frozen=True)
class RwiParams:
    mode: str = "mode_a"  # "mode_a" (Poulos dual horizon) | "mode_b" (LT high > 1 & LT high > LT low)
    short_len: int = 7
    long_len: int = 64
    threshold: float = 1.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: RwiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.short_len <= 2:
        return False, "sol_smoke: 15m S<=2 forbidden (spam)"
    if (params.short_len, params.long_len) not in {(5, 40), (7, 64), (8, 48)}:
        return False, f"sol_smoke: (S, L)=({params.short_len}, {params.long_len}) not in locked set"
    if params.threshold not in {1.0, 1.2}:
        return False, f"sol_smoke: thr={params.threshold} not in locked set {{1.0, 1.2}}"
    if params.short_len >= params.long_len:
        return False, "sol_smoke: short_len must be strictly < long_len"
    return True, "PASS"


def validate_bnb_smoke(params: RwiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.short_len >= params.long_len:
        return False, "bnb_smoke: short_len >= long_len invalid"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: RwiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for rwi-high-low-threshold-v1."""
    params = params or RwiParams()
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

    # Compute short horizon RWI
    _, rwi_l_s = rwi_high_low(highs, lows, closes, max_lookback=params.short_len)
    # Compute long horizon RWI
    rwi_h_l, rwi_l_l = rwi_high_low(highs, lows, closes, max_lookback=params.long_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    thr = params.threshold

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
            # Exit when rwiH_L < thr or rwiL_L > rwiH_L
            hl = rwi_h_l[i]
            ll = rwi_l_l[i]
            if hl is not None and hl < thr:
                exit_signal = True
            elif hl is not None and ll is not None and ll > hl:
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
            hl = rwi_h_l[i]
            ll = rwi_l_l[i]
            ls = rwi_l_s[i]
            ls_prev = rwi_l_s[i - 1]

            if params.mode == "mode_a":
                # Long when rwiH_L > thr and rwiL_S > thr and rwiL_S > rwiL_S[1]
                if (
                    hl is not None
                    and hl > thr
                    and ls is not None
                    and ls > thr
                    and ls_prev is not None
                    and ls > ls_prev
                ):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Long while rwiH_L > thr and rwiH_L > rwiL_L
                if hl is not None and hl > thr and ll is not None and hl > ll:
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
