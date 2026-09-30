"""leibfarth-apz-break-flip — Leibfarth Adaptive Price Zone break-flip.

LOCKED ENCODE ORDER #4 (BTC->ETH PORTABILITY PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage9 burned AccelBands; stage13 wiped Donovan Range Filter; Keltner/SuperTrend/Donchian burned.
  Leibfarth APZ builds bands from double-smoothed EMA of close +- BandPct * double-smoothed EMA of (H-L) —
  != ATR-Keltner, != SuperTrend mid, != Donchian extremes, != Range Filter, != AccelBands.
  Mode A locks band-break trend flip (long when close crosses above upper; exit/flip when close crosses below lower)
  for responsive majors structure — BTC->ETH clearing without REI overlap tricks.
  Forbidden: ADX>30 graft (ADX burned). Identical (period, BandPct) on all four coins.

Formula:
  ds = ema(ema(close, period), period)
  dsg = ema(ema(high - low, period), period)
  up = ds + BandPct * dsg
  dn = ds - BandPct * dsg
  Prefer period=20, BandPct=1.4.

Mode A (BTC->ETH-PRIMARY break-flip):
  long: crossover(close, up)
  exit: crossunder(close, dn) or ATR stop.

Mode B (BNB quiet / article-fade):
  long: crossunder(close, dn) reclaim back inside (crossunder close, dn then close > dn)
  exit: crossover(close, up) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if period/BandPct inflated until flips collapse; Kill if ADX gate; Kill if dual-MA cross replace; Kill if stage12 damp.
  Prefer Mode A (20, 1.4), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears then ETH wipes (stage13 REI pattern); Kill if period/BandPct retuned only on ETH; Kill if Keltner ATR substitute.
  Prefer identical (20, 1.4) on ETH; ETH flip n multi-dozen.

sol_smoke:
  Kill if Keltner/SuperTrend/RF/AccelBands labeled APZ; 15m period=5; ADX/ER/stage12-13.
  Retention check: after ETH, SOL flip n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (period,BandPct) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: ADX; Keltner/SuperTrend/Donchian/RF/AccelBands labeled APZ; REI/PZO/TMO/CLV; stage12 FIR/Gaussian; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, leibfarth_apz

STRATEGY_ID = "leibfarth-apz-break-flip"


@dataclass(frozen=True)
class LeibfarthApzParams:
    mode: str = "mode_a"  # "mode_a" (breakout close x up, exit close x dn) | "mode_b" (fade reclaim)
    period: int = 20
    band_pct: float = 1.4
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: LeibfarthApzParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period > 50 or params.band_pct > 3.0:
        return False, f"btc_smoke: ({params.period},{params.band_pct}) inflated, collapses flip n"
    if params.period not in {14, 20, 30} or params.band_pct not in {1.2, 1.4, 1.8}:
        return False, f"btc_smoke: ({params.period},{params.band_pct}) not in locked sweep grid"
    return True, "PASS"


def validate_eth_smoke(params: LeibfarthApzParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.period not in {14, 20, 30} or params.band_pct not in {1.2, 1.4, 1.8}:
        return False, f"eth_smoke: ({params.period},{params.band_pct}) retuned away from locked grid"
    return True, "PASS"


def validate_sol_smoke(params: LeibfarthApzParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period <= 5:
        return False, "sol_smoke: 15m period<=5 forbidden (spam)"
    if params.period not in {14, 20, 30} or params.band_pct not in {1.2, 1.4, 1.8}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: LeibfarthApzParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.period <= 0 or params.band_pct <= 0:
        return False, "bnb_smoke: period and band_pct must be > 0"
    if params.period > 50:
        return False, "bnb_smoke: period too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: LeibfarthApzParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for leibfarth-apz-break-flip."""
    params = params or LeibfarthApzParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    _, _, up, dn = leibfarth_apz(highs, lows, closes, period=params.period, band_pct=params.band_pct)

    in_pos = False
    highest_since_entry = 0.0

    close_series = [float(c) for c in closes]

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_a":
            # Breakout flip: long on close crossing above upper band, exit on close crossing below lower band
            cross_up = crossover(close_series, up, i)
            cross_dn = crossunder(close_series, dn, i)
            entry_cond = cross_up
            exit_cond = cross_dn
        else:  # mode_b: fade reclaim of lower band
            cross_dn_lower = crossunder(close_series, dn, i)
            reclaim_up_lower = crossover(close_series, dn, i)
            entry_cond = reclaim_up_lower
            exit_cond = crossover(close_series, up, i)

        if not in_pos:
            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * float(atr_vals[i])
        else:
            highest_since_entry = max(highest_since_entry, h)
            stop_hit = False

            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                new_stop = highest_since_entry - params.atr_trail_mult * float(atr_vals[i])
                prev_stop = stops[i - 1]
                if prev_stop is not None and new_stop < prev_stop:
                    new_stop = prev_stop
                stops[i] = new_stop
                if lows[i] <= new_stop:
                    stop_hit = True

            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
