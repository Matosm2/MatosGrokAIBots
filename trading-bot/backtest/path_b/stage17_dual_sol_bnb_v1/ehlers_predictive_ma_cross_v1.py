"""ehlers-predictive-ma-cross — Ehlers Predictive Moving Average Predict x Trigger Cross.

LOCKED ENCODE ORDER #5 (BTC LEAD PRIMARY).
Thesis:
  Stage16 structure stalled SOL; stage8 WMA fast x slow burned as free dual.
  Ehlers Predictive MA is a fixed Rocket-Science construction:
  predict = 2 * WMA(src, 7) - WMA(WMA(src, 7), 7)
  trigger = WMA(predict, 4)
  Mode A = predict x trigger cross.
  Low-lag predictive polarity may keep BTC+ETH density and follow SOL impulses better than
  Kagi R-threshold under-flips — without free WMA-length dual retune.
  != stage8 wma-fast-slow-cross.
  != ZLEMA x SMA stage4.

Formula:
  w1 = wma(src, 7)
  w2 = wma(w1, 7)
  predict = 2*w1 - w2
  trigger = wma(predict, 4)
  Prefer close + 7/7/4 locked.

Mode A (BTC-LEAD PRIMARY — prefer):
  long: crossover(predict, trigger)
  exit: crossunder(predict, trigger)

Mode B (BNB quiet / hold filter):
  long: crossover(predict, trigger) and predict > trigger hold 2 bars
  exit: crossunder(predict, trigger)

btc_smoke:
  BTC-LEAD CRITICAL: Kill if lengths inflated into free WMA dual (stage8);
  Kill if ZLEMA/MAMA substitute;
  Kill if Mode B forced while Mode A BTC healthy. Prefer Mode A 7/7/4 close, 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill BTC-clear->ETH-wipe;
  Kill lengths retuned only on ETH; Kill WMA dual graft.
  Prefer identical 7/7/4; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  Kill free WMA dual / ZLEMA labeled PMA; 15m WMA(3) spam; stage12-16 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different lengths; Mode B shorts ungated; no ATR.
  Prefer identical 7/7/4; long-only; ATR exit.

Forbidden: Free WMA fast x slow; ZLEMA x SMA; MAMA/FAMA primary; SuperSmoother;
BandPass/HP/3LB/SI/Kagi; stage12-16.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_predictive_ma

STRATEGY_ID = "ehlers-predictive-ma-cross"


@dataclass(frozen=True)
class PredictiveMaParams:
    mode: str = "mode_a"  # "mode_a" (predict x trig) | "mode_b" (predict x trig hold 2 bars)
    src: str = "close"  # "close" | "hl2"
    wma_len: int = 7
    trigger_len: int = 4
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: PredictiveMaParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.wma_len != 7:
        return False, f"btc_smoke: wma_len={params.wma_len} != 7 (fixed 7/7/4 required)"
    if params.trigger_len not in {3, 4, 5}:
        return False, f"btc_smoke: trigger_len={params.trigger_len} not in locked set {{3, 4, 5}}"
    if params.src not in {"close", "hl2"}:
        return False, f"btc_smoke: src={params.src} not in locked set {{close, hl2}}"
    return True, "PASS"


def validate_eth_smoke(params: PredictiveMaParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH CRITICAL)."""
    if params.wma_len != 7 or params.trigger_len not in {3, 4, 5} or params.src not in {"close", "hl2"}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: PredictiveMaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.wma_len <= 3:
        return False, "sol_smoke: 15m wma_len<=3 forbidden (spam)"
    if params.wma_len != 7 or params.trigger_len not in {3, 4, 5} or params.src not in {"close", "hl2"}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: PredictiveMaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.wma_len != 7 or params.trigger_len not in {3, 4, 5} or params.src not in {"close", "hl2"}:
        return False, "bnb_smoke: params retuned away from locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PredictiveMaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-predictive-ma-cross."""
    params = params or PredictiveMaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    if params.src == "hl2":
        src = [(h + l) / 2.0 for h, l in zip(highs, lows)]
    else:
        src = closes

    atr_vals = atr(highs, lows, closes, params.atr_len)
    predict, trig = ehlers_predictive_ma(
        src,
        wma_len=params.wma_len,
        trigger_len=params.trigger_len,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(predict, trig, i)
        cross_dn = crossunder(predict, trig, i)

        if params.mode == "mode_b":
            # Mode B: require predict > trig for 2 bars (hold filter)
            p_val = predict[i]
            t_val = trig[i]
            p_prev = predict[i - 1]
            t_prev = trig[i - 1]
            if p_val is None or t_val is None or p_prev is None or t_prev is None:
                cross_up = False
            elif not (p_val > t_val and p_prev > t_prev):
                cross_up = False

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
