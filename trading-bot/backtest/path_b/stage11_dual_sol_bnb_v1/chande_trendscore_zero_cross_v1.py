"""chande-trendscore-zero-cross-v1 — Chande TrendScore signed lookback-block zero polarity.

LOCKED ENCODE ORDER #1 (BNB-SURVIVAL-FIRST + DENSITY: SOL + BNB survival).
Thesis:
  Stage10 wiped TII/PSY/RMI/Dorsey midline-50 intensity and TCF sign. Chande TrendScore is a
  discrete signed rating (-10..+10): sum of ten +1/-1 comparisons of today's close vs closes
  11-20 bars ago — direction+strength in one reading, != ADX intensity, != VHF unsigned,
  != SMA-deviation share (TII).
  Zero-cross is dense on 1H; close-only -> majors-liquid portable to quieter BNB with
  identical (start_lag, width). BNB-survival-first: no volume microstructure.

Formula:
  For i = start_lag .. start_lag + width - 1:
    ts += close >= close[i] ? 1.0 : -1.0
  Classic (11, 10) -> -10..+10.

Mode A (primary / dense zero):
  long: crossover(ts, 0)
  exit: crossunder(ts, 0) or ATR stop.

Mode B (BNB-quiet smooth):
  tsE = ema(ts, 5)
  long: crossover(tsE, 0)
  exit: crossunder(tsE, 0) or ATR stop.
  (identical Mode across coins).

sol_smoke:
  Kill if: TII/PSY labeled TrendScore; ADX graft; 15m width=3 spam; ER/AO/PGO graft.
  Prefer Mode A (11, 10), 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  Kill if: different (start_lag, width) than SOL; Mode B only on BNB while SOL Mode A;
  no ATR; volume graft. Prefer identical; long-only; ATR exit.

Forbidden: ADX/DMI/VHF substitute; TII/PSY/RMI midline; TCF; ER-gate; AO/ROC/WMA/PGO; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, chande_trendscore, crossover, crossunder, ema

STRATEGY_ID = "chande-trendscore-zero-cross-v1"


@dataclass(frozen=True)
class ChandeTrendScoreParams:
    mode: str = "mode_a"  # "mode_a" (ts cross 0) | "mode_b" (ema(ts, 5) cross 0)
    start_lag: int = 11
    width: int = 10
    ema_len: int = 5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: ChandeTrendScoreParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.width <= 3:
        return False, "sol_smoke: 15m width<=3 forbidden (spam)"
    if (params.start_lag, params.width) not in {(11, 10), (8, 8), (15, 7)}:
        return False, f"sol_smoke: (start_lag,width)=({params.start_lag},{params.width}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ChandeTrendScoreParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.start_lag <= 0 or params.width <= 0:
        return False, "bnb_smoke: start_lag and width must be > 0"
    if params.width > 30:
        return False, "bnb_smoke: width too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ChandeTrendScoreParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for chande-trendscore-zero-cross-v1."""
    params = params or ChandeTrendScoreParams()
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
    raw_ts = chande_trendscore(closes, start_lag=params.start_lag, width=params.width)

    if params.mode == "mode_b":
        # Mode B: ema(ts, 5)
        # Filter None values to compute EMA
        first_valid = -1
        for i in range(n):
            if raw_ts[i] is not None:
                first_valid = i
                break
        if first_valid != -1:
            valid_ts = [float(raw_ts[i]) for i in range(first_valid, n)]
            inner_ema = ema(valid_ts, params.ema_len)
            ts_series: list[float | None] = [None] * n
            for i, val in enumerate(inner_ema):
                ts_series[first_valid + i] = val
        else:
            ts_series = [None] * n
    else:
        ts_series = raw_ts

    zeroes: list[float | None] = [0.0] * n

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
            if crossunder(ts_series, zeroes, i):
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
            if crossover(ts_series, zeroes, i):
                enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
