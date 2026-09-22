"""mad-channel-break-rvol-v1 — Median / MAD Channel Breakout + Light RVOL.

LOCKED ENCODE ORDER #3 (DUAL-SURVIVAL: SOL + BNB).
Thesis:
  Replaces Bollinger Bands' mean +/- k*stdev with median +/- k*(1.4826 * MAD).
  The Median Absolute Deviation (MAD) is a high-breakdown robust statistic (asymptotic breakdown point 50%),
  making it resilient against SOL wick outliers and BNB thin-print spikes that artificially balloon classical stdev.
  Light RVOL >= kr on the breakout bar ensures volume participation without stage4 RVOL-structure primary.

Formula:
  med = median(close, N)
  mad_val = median(|close - med|, N)
  madSigma = 1.4826 * mad_val
  upper = med + k * madSigma
  lower = med - k * madSigma
  N in {20, 34}; k in {1.5, 2.0, 2.5} (prefer 2.0)

Mode A (primary):
  Long: close > upper and prior close <= upper (closed-bar break only; NOT wick-only).
  Gated by light RVOL: volume / ta.sma(volume, 20) >= kr (kr in {1.0, 1.2}; ON by default).

Mode B (secondary):
  Mean-revert fade (secondary).

Exit:
  Close back through med (Mode A) or opposite band; ATR trail stop.

Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, mad_channel, rvol

STRATEGY_ID = "mad-channel-break-rvol-v1"


@dataclass(frozen=True)
class MadChannelParams:
    mode: str = "mode_a"  # "mode_a" (breakout) | "mode_b" (mean-revert fade)
    channel_n: int = 20
    k_mult: float = 2.0
    rvol_k: float = 1.0  # Light RVOL gate (1.0 or 1.2)
    vol_len: int = 20
    rvol_filter: bool = True
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: MadChannelParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if params.channel_n < 15:
        return False, "sol_smoke: N < 15 on 1H (too noisy)"
    if params.mode != "mode_a":
        return False, "sol_smoke: Mode B first forbidden (prefer Mode A)"
    return True, "PASS"


def validate_bnb_smoke(params: MadChannelParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if tf == "15m" and not params.rvol_filter:
        return False, "bnb_smoke: RVOL off and 15m"
    if params.k_mult < 1.2:
        return False, "bnb_smoke: k < 1.2 (too tight)"
    if params.mode != "mode_a":
        return False, "bnb_smoke: Mode B fade forbidden on BNB"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: MadChannelParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for mad-channel-break-rvol-v1."""
    params = params or MadChannelParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]

    med_vals, upper_vals, lower_vals = mad_channel(closes, params.channel_n, params.k_mult)
    rvol_vals = rvol(vols, params.vol_len)
    atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        m = med_vals[i]
        u = upper_vals[i]
        l = lower_vals[i]
        rv = rvol_vals[i]

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

            if params.mode == "mode_a":
                # Exit when close drops back below rolling median
                if m is not None and c < m:
                    exit_signal = True
            elif params.mode == "mode_b":
                # Fade exit when price reaches median or upper
                if m is not None and c >= m:
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
        if not in_pos and i > 0 and u is not None and l is not None:
            rvol_ok = (not params.rvol_filter) or (rv is not None and rv >= params.rvol_k)
            enter_signal = False

            if params.mode == "mode_a":
                # Closed-bar break beyond upper band (close > upper after prior close <= upper)
                prev_c = closes[i - 1]
                prev_u = upper_vals[i - 1]
                if prev_u is not None and prev_c <= prev_u and c > u and rvol_ok:
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mean-revert fade: touch below lower then close back inside
                prev_c = closes[i - 1]
                prev_l = lower_vals[i - 1]
                if prev_l is not None and prev_c < prev_l and c >= l and rvol_ok:
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
