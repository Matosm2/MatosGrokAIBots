"""nadaraya-rq-estimate-cross — Causal Nadaraya-Watson Rational Quadratic Kernel estimate cross.

LOCKED ENCODE ORDER #5 (BTC->ETH PORTABILITY PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage12 wiped Gaussian multipole / EDCF FIR; stage2 ALMA; dual-MA banned.
  Causal NW RQ is a kernel-regression endpoint estimate of close (weights decay with lag; no future bars) —
  Mode A = close crossover yhat — != SMA/EMA dual-cross, != Ehlers multipole Gaussian, != ALMA, != EDCF.
  Non-parametric OHLC-close -> identical (lookback, alpha) on BTC/ETH/SOL/BNB.
  Must use causal/non-repainting endpoint (not LuxAlgo two-sided repaint envelope).

Formula:
  w_i = (1 + i^2 / (2 * alpha * lookback^2))^(-alpha)  for i = 0 .. lookback - 1
  yhat = sum(close[i] * w_i) / sum(w_i)
  Prefer lookback=8, alpha=8.

Mode A (BTC->ETH-PRIMARY):
  long: crossover(close, yhat)
  exit: crossunder(close, yhat) or ATR stop.

Mode B (BNB quiet / quality hold):
  long: crossover(close, yhat) and close > yhat (or slope(yhat) > 0)
  exit: crossunder(close, yhat) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if lookback/alpha inflated until n collapses; Kill if repainting two-sided kernel; Kill if Gaussian multipole / EDCF substitute.
  Prefer Mode A (8,8), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears then ETH wipes (stage13 REI pattern); Kill if lookback/alpha retuned only on ETH; Kill if repaint envelope.
  Prefer identical params on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if repaint NW / Gaussian / ALMA / EDCF labeled RQ; 15m lookback=3 spam; stage12-13.
  Retention check: after ETH, SOL n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (lookback,alpha) than SOL; Mode B shorts ungated; no ATR; per-coin retune.
  Prefer identical params; long-only; ATR exit.

Forbidden: Repaint two-sided NW; Ehlers Gaussian multipole; ALMA/EDCF/SMA dual; REI/PZO/TMO/RF/CLV; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, nadaraya_rq

STRATEGY_ID = "nadaraya-rq-estimate-cross"


@dataclass(frozen=True)
class NadarayaRqParams:
    mode: str = "mode_a"  # "mode_a" (close cross yhat) | "mode_b" (close cross yhat + slope quality)
    lookback: int = 8
    alpha: float = 8.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: NadarayaRqParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.lookback > 25:
        return False, f"btc_smoke: lookback={params.lookback} > 25 collapses n (stage12 rhyme)"
    if params.lookback not in {5, 8, 14} or params.alpha not in {1.0, 8.0, 25.0}:
        return False, f"btc_smoke: ({params.lookback},{params.alpha}) not in locked sweep grid"
    return True, "PASS"


def validate_eth_smoke(params: NadarayaRqParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.lookback not in {5, 8, 14} or params.alpha not in {1.0, 8.0, 25.0}:
        return False, f"eth_smoke: ({params.lookback},{params.alpha}) retuned away from locked grid"
    return True, "PASS"


def validate_sol_smoke(params: NadarayaRqParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.lookback <= 3:
        return False, "sol_smoke: 15m lookback<=3 forbidden (spam)"
    if params.lookback not in {5, 8, 14} or params.alpha not in {1.0, 8.0, 25.0}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: NadarayaRqParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.lookback <= 0 or params.alpha <= 0:
        return False, "bnb_smoke: lookback and alpha must be > 0"
    if params.lookback > 25:
        return False, "bnb_smoke: lookback too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: NadarayaRqParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for nadaraya-rq-estimate-cross."""
    params = params or NadarayaRqParams()
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
    yhat = nadaraya_rq(closes, lookback=params.lookback, alpha=params.alpha)

    in_pos = False
    highest_since_entry = 0.0

    close_series = [float(c) for c in closes]

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(close_series, yhat, i)
        cross_dn = crossunder(close_series, yhat, i)

        if params.mode == "mode_b":
            # Quality hold: close cross up and yhat slope > 0
            slope_up = (
                yhat[i] is not None
                and yhat[i - 1] is not None
                and float(yhat[i]) > float(yhat[i - 1])
            )
            entry_cond = cross_up and slope_up
        else:
            entry_cond = cross_up

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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
