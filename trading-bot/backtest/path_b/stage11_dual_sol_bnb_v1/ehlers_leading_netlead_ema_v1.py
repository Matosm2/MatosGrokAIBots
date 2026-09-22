"""ehlers-leading-netlead-ema-v1 — Ehlers Leading Indicator NetLead x EMA dual-line cross.

LOCKED ENCODE ORDER #3 (BNB-SURVIVAL-FIRST + DENSITY: SOL + BNB survival).
Thesis:
  Stage10 wiped DEMA dual; stage7 parked Reverse EMA; ITrend/Laguerre burned.
  Ehlers Leading Indicator builds a lead from price-EMA difference added back to price,
  then EMA-smooths to NetLead, plotted vs a short EMA of hl2 — lag-reduced dual-line
  != ITrend trigger, != Reverse EMA trendxcycle, != DEMA=2*EMA - EMA^2.
  NetLead x EMA cross is dense on 1H; hl2-only -> BNB-portable identical (a1, a2).

Formula:
  price = (high + low) / 2
  Lead = 2 * price + (a1 - 2) * price[1] + (1 - a1) * Lead[1]
  NetLead = a2 * Lead + (1 - a2) * NetLead[1]
  EMA = 0.5 * price + 0.5 * EMA[1]
  Prefer a1=0.25, a2=0.50.

Mode A (primary / dense cross):
  long: crossover(NetLead, EMA)
  exit: crossunder(NetLead, EMA) or ATR stop.

Mode B (secondary / NetLead rising):
  long: crossover(NetLead, NetLead[1]) and NetLead > EMA
  exit: crossunder(NetLead, EMA) or ATR stop.

sol_smoke:
  Kill if: DEMA/ITrend/ReverseEMA labeled ELI; 15m alpha spam; ER/AO/PGO graft; Keltner as entry gate.
  Prefer Mode A (0.25, 0.50), 1H+.
  Retention check: after ETH, if SOL n huge with poor structure, try a1=0.20 same Mode A before family fail.

bnb_smoke:
  Kill if: different (a1, a2) than SOL; per-coin alpha retune after SOL clear; ungated shorts; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: ITrend; ReverseEMA; Laguerre; DEMA/TEMA/ZLEMA; ER-gate; AO/ROC/WMA/PGO; TII/TCF; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_leading_indicator

STRATEGY_ID = "ehlers-leading-netlead-ema-v1"


@dataclass(frozen=True)
class EhlersLeadingParams:
    mode: str = "mode_a"  # "mode_a" (crossover(netLead, ema)) | "mode_b" (netLead rising and netLead > ema)
    a1: float = 0.25
    a2: float = 0.50
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: EhlersLeadingParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and (params.a1 > 0.4 or params.a2 > 0.6):
        return False, "sol_smoke: 15m alpha spam forbidden"
    if (params.a1, params.a2) not in {(0.25, 0.50), (0.20, 0.50), (0.25, 0.33), (0.33, 0.50)}:
        return False, f"sol_smoke: (a1,a2)=({params.a1},{params.a2}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersLeadingParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.a1 <= 0.0 or params.a1 >= 1.0 or params.a2 <= 0.0 or params.a2 >= 1.0:
        return False, "bnb_smoke: alpha values must be in (0, 1)"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersLeadingParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-leading-netlead-ema-v1."""
    params = params or EhlersLeadingParams()
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
    net_lead, ema_vals = ehlers_leading_indicator(highs, lows, a1=params.a1, a2=params.a2)

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
            # Exit on netLead crossunder ema
            if crossunder(net_lead, ema_vals, i):
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
            if params.mode == "mode_a":
                if crossover(net_lead, ema_vals, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: netLead rising (netLead[i] > netLead[i-1] and netLead[i-1] <= netLead[i-2]) and netLead > ema
                nl_curr = net_lead[i]
                nl_prev = net_lead[i - 1]
                nl_prev2 = net_lead[i - 2]
                em_curr = ema_vals[i]
                if (
                    nl_curr is not None
                    and nl_prev is not None
                    and nl_prev2 is not None
                    and em_curr is not None
                ):
                    if nl_curr > nl_prev and nl_prev <= nl_prev2 and nl_curr > em_curr:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
