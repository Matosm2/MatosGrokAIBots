"""forecast-oscillator-zero — Forecast Oscillator (FOSC) zero-cross.

LOCKED ENCODE ORDER #4 (BTC LEAD + ETH-PORTABLE PRIMARY).
Thesis:
  Stage17 PMA (predict x trigger WMA construction) 0 BTC; LinReg primary burned.
  Forecast Oscillator is a named %-deviation of close vs prior Time Series Forecast:
    fosc = 100 * (close - tsf[1]) / close
    tsf = lrc + lrs
  Mode A = FOSC x 0 cross — price-vs-forecast polarity intended denser and ETH-portable
  without free LinReg channel-break / slope-zero primary and without PMA 7/7/4.
  Close-only -> identical length across all four coins.
  != LinReg channel break (burned).
  != LinReg-slope-zero primary.
  != PMA 7/7/4 (stage17).
  != NetLead (stage11).

Formula:
  lrc = linreg(close, len, 0)
  lrs = lrc - linreg(close, len, 1)
  tsf = lrc + lrs
  fosc = 100 * (close - tsf[1]) / close
  Prefer len = 14. Mode A FOSC x 0.

Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer):
  long: crossover(fosc, 0)
  exit: crossunder(fosc, 0)

Mode B (BNB quiet):
  fosc vs sma(fosc, sigLen) — only if Mode A over-whips; identical (len, sigLen).

btc_smoke:
  BTC-LEAD CRITICAL: Kill len inflate until n collapses;
  Kill LinReg-channel / PMA / NetLead substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A len=14, 1H+.

eth_smoke:
  BTC->ETH PRIMARY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill len retuned only on ETH; Kill LinReg-channel / III / PMA labeled FOSC.
  Prefer identical len=14; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  Kill LinReg-channel labeled FOSC; 15m len=3; stage12-17 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different len; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: LinReg channel-break / close x linreg as primary; LinReg slope x 0 primary; PMA 7/7/4; NetLead; stage12-17.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, forecast_oscillator, sma

STRATEGY_ID = "forecast-oscillator-zero"


@dataclass(frozen=True)
class FoscParams:
    mode: str = "mode_a"  # "mode_a" (fosc x 0) | "mode_b" (fosc x sma(fosc, sigLen))
    length: int = 14
    sig_len: int = 5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: FoscParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {10, 14, 21}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{10, 14, 21}}"
    if params.length > 50:
        return False, f"btc_smoke: length={params.length} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: FoscParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PRIMARY CRITICAL)."""
    if params.length not in {10, 14, 21}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: FoscParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.length <= 3:
        return False, "sol_smoke: 15m length<=3 forbidden (spam)"
    if params.length not in {10, 14, 21}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: FoscParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.length not in {10, 14, 21}:
        return False, "bnb_smoke: params not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: FoscParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for forecast-oscillator-zero."""
    params = params or FoscParams()
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
    fosc_vals, _ = forecast_oscillator(closes, length=params.length)

    ref_line: list[float | None]
    if params.mode == "mode_b":
        # Mode B: fosc vs sma(fosc, sig_len)
        fosc_clean = [0.0 if v is None else v for v in fosc_vals]
        ref_line = sma(fosc_clean, params.sig_len)
    else:
        ref_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(fosc_vals, ref_line, i)
        cross_dn = crossunder(fosc_vals, ref_line, i)

        if not in_pos:
            if cross_up:
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
