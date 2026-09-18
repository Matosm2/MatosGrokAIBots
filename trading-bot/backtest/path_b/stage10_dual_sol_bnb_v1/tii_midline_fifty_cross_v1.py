"""tii-midline-fifty-cross-v1 — Pee Trend Intensity Index midline-50 cross.

LOCKED ENCODE ORDER #1 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage9 wiped PSY/RMI midline-50 (count-up / m-bar Wilder) and Disparity/WT/AccelBands.
  Pee TII measures what share of recent closes sit above a longer SMA (deviation-sum intensity),
  not up-close count (PSY) and not RSI/RMI gains.
  Midline-50 polarity is dense on 1H–4H; classic 80/20 is Mode B (sparser thr).
  Close+SMA portable; identical (major, minor) on SOL+BNB.
  Anti-sparse vs ER/PGO-n=9.
  Distinct from burned PSY/RMI/RSI, != ADX.

Formula:
  ma = ta.sma(close, major)
  sdPos = sum(max(close - ma, 0), minor)
  sdNeg = sum(max(ma - close, 0), minor)
  tii = 100 * sdPos / (sdPos + sdNeg)  guard (sdPos + sdNeg) > 0
  (major, minor) in {(40,20), (60,30), (50,25)}; prefer (60,30) first (Pee default).

Mode A (primary / dense midline):
  long: ta.crossover(tii, 50)
  exit: ta.crossunder(tii, 50) or ATR stop.

Mode B (secondary classic extremes):
  long: ta.crossover(tii, 80)
  exit: ta.crossunder(tii, 50) or crossunder(tii, 20) or ATR stop.

sol_smoke:
  Kill if: RSI/PSY/RMI labeled TII; 15m major=10 spam; ER/AO/PGO graft; Mode B 80-only with single-digit n.
  Prefer Mode A (60,30), 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  Kill if: different (major, minor) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: RSI/PSY/RMI substitute; ADX/DMI graft; SMA200; ER-gate; AO/ROC/WMA/PGO; Disparity/WT; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, trend_intensity_index

STRATEGY_ID = "tii-midline-fifty-cross-v1"


@dataclass(frozen=True)
class TiiMidlineParams:
    mode: str = "mode_a"  # "mode_a" (cross > 50) | "mode_b" (cross > 80, exit < 50)
    major: int = 60
    minor: int = 30
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: TiiMidlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.major <= 10:
        return False, "sol_smoke: 15m major<=10 forbidden (spam)"
    if (params.major, params.minor) not in {(40, 20), (60, 30), (50, 25)}:
        return False, f"sol_smoke: (major,minor)=({params.major},{params.minor}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: TiiMidlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.major <= 0 or params.minor <= 0:
        return False, "bnb_smoke: major and minor must be > 0"
    if params.minor >= params.major:
        return False, "bnb_smoke: minor must be less than major"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: TiiMidlineParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for tii-midline-fifty-cross-v1."""
    params = params or TiiMidlineParams()
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
    tii_vals = trend_intensity_index(closes, major=params.major, minor=params.minor)

    fifties: list[float | None] = [50.0] * n
    eighties: list[float | None] = [80.0] * n

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
            # Exit on crossunder 50
            if crossunder(tii_vals, fifties, i):
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
                # Mode A: crossover(tii, 50)
                if crossover(tii_vals, fifties, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(tii, 80)
                if crossover(tii_vals, eighties, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
