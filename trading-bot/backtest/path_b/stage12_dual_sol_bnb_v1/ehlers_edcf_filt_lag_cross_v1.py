"""ehlers-edcf-filt-lag-cross-v1 — Ehlers Distance Coefficient Filter filt × filt[lag] cross.

LOCKED ENCODE ORDER #2 (BNB-SURVIVAL-CRITICAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage11 wiped NetLead×EMA; stage10 wiped DEMA; stage5 parked SuperSmoother dual. Ehlers Distance
  Coefficient Filter is a nonlinear FIR: coefficients = sum of squared price distances inside the
  window, then weighted average — != IIR SuperSmoother, != DEMA=2*EMA - EMA^2, != NetLead
  lead-recursion, != WMA fixed weights.
  Mode A locks filt x filt[lag] (not price x filt) so quieter BNB does not spam every SMA-like touch
  when the filter degenerates flat — BNB-survival-CRITICAL.
  hl2/close-only -> identical Length+lag on SOL+BNB.

Formula:
  price = (high + low) / 2
  For count = 0 .. Length - 1:
    coef[count] = sum_{k=1 .. Length-1} (price[count] - price[count + k])^2
  filt = sum(coef * price) / sum(coef) (fallback price if sum(coef) == 0)
  Defaults: Length=15, lag=2.

Mode A (BNB-critical lag-cross — prefer first):
  long: crossover(filt, filt[lag])
  exit: crossunder(filt, filt[lag]) or ATR stop.

Mode B (secondary density):
  long: crossover(price, filt)
  exit: crossunder(price, filt) or ATR stop.
  (only if Mode A under-fires on BTC; still identical params across coins).

sol_smoke:
  Kill if: SuperSmoother/DEMA/NetLead labeled EDCF; 15m Length=5 spam; ER/AO/PGO graft;
  Mode B forced while Mode A BTC n already dense. Prefer Mode A (15, 2), 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class.

bnb_smoke:
  BNB-after-SOL kill (CRITICAL): different (Length, lag) than SOL; switching to Mode B only on BNB
  while SOL stays Mode A; no ATR; volume graft. Prefer identical params; long-only; ATR exit.

Forbidden: SuperSmoother/DEMA/NetLead/WMA/HMA/ZLEMA substitute; ER-gate; AO/ROC/PGO;
Pee TDI/TrendScore/GMMA/VQI; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_edcf

STRATEGY_ID = "ehlers-edcf-filt-lag-cross-v1"


@dataclass(frozen=True)
class EhlersEdcfParams:
    mode: str = "mode_a"  # "mode_a" (filt cross filt[lag]) | "mode_b" (price cross filt)
    length: int = 15
    lag: int = 2
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: EhlersEdcfParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m Length<=5 forbidden (spam)"
    if (params.length, params.lag) not in {(15, 2), (10, 2), (20, 2), (15, 3)}:
        return False, f"sol_smoke: (Length,lag)=({params.length},{params.lag}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersEdcfParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after SOL)."""
    if params.length <= 1 or params.lag <= 0:
        return False, "bnb_smoke: Length > 1 and lag > 0 required"
    if params.length > 50 or params.lag > 10:
        return False, "bnb_smoke: Length or lag too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersEdcfParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-edcf-filt-lag-cross-v1."""
    params = params or EhlersEdcfParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    prices = [(h + l) / 2.0 for h, l in zip(highs, lows, strict=False)]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    filt = ehlers_edcf(highs, lows, length=params.length)

    # Shifted filt by lag
    filt_lag: list[float | None] = [None] * n
    lag = params.lag
    for i in range(lag, n):
        filt_lag[i] = filt[i - lag]

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_b":
            cross_up = crossover(prices, filt, i)
            cross_dn = crossunder(prices, filt, i)
        else:
            cross_up = crossover(filt, filt_lag, i)
            cross_dn = crossunder(filt, filt_lag, i)

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
