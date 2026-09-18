"""dss-bressert-trigger-cross — Double Smoothed Stochastic (DSS Bressert) x Trigger Cross.

LOCKED ENCODE ORDER #3 (BTC LEAD + SOL DENSE PRIMARY).
Thesis:
  Stage16 structure/cycle seats failed SOL after BTC+ETH.
  DSS Bressert (Blau / Bressert) is a double-smoothed stochastic of a stochastic:
  EMA-smooth raw %K, then stochastic-of-that, then EMA again.
  Used as DSS x Trigger crossover, not raw Stoch K/D.
  Intended denser majors+SOL polarity with identical (PDS, EMAlen, TriggerLen).
  != raw Stoch primary.
  != SMI.
  != TMO Main zero.
  != stage10 Dorsey RelVol / Relative Volatility Index midline.

Formula:
  pre = ema(stoch(close, high, low, PDS), EMAlen)
  dss = ema(stoch(pre, pre, pre, PDS), EMAlen)
  trig = ema(dss, TriggerLen)
  Prefer (10, 9, 5).

Mode A (BTC-LEAD + SOL-dense — prefer):
  long: crossover(dss, trig)
  exit: crossunder(dss, trig)

Mode B (BNB quiet / 20-80 band):
  long: crossover(dss, trig) and dss < 20
  exit: crossunder(dss, trig) or dss > 80

btc_smoke:
  BTC-LEAD CRITICAL: Kill if PDS/EMA inflated until BTC n collapses;
  Kill if raw Stoch substitute;
  Kill if Mode B 20/80 forced while Mode A BTC healthy. Prefer Mode A (10, 9, 5), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill BTC-clear->ETH-wipe;
  Kill params retuned only on ETH; Kill Stoch K/D graft.
  Prefer identical (10, 9, 5); ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill if BTC+ETH clear then SOL under 1.2x;
  Kill Stoch/SMI/TMO labeled DSS; 15m PDS=3 spam; stage12-16 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different PDS/EMA/Trigger; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR exit.

Forbidden: Raw Stoch K/D; SMI/TMO; Dorsey RelVol / Rel Volatility Index;
BandPass/HP/3LB/SI/Kagi; stage12-16.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, dss_bressert

STRATEGY_ID = "dss-bressert-trigger-cross"


@dataclass(frozen=True)
class DssBressertParams:
    mode: str = "mode_a"  # "mode_a" (dss x trig) | "mode_b" (dss < 20 cross / dss > 80 exit)
    pds: int = 10
    ema_len: int = 9
    trigger_len: int = 5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: DssBressertParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.pds not in {8, 10, 14}:
        return False, f"btc_smoke: pds={params.pds} not in locked set {{8, 10, 14}}"
    if params.trigger_len not in {3, 5}:
        return False, f"btc_smoke: trigger_len={params.trigger_len} not in locked set {{3, 5}}"
    if params.ema_len != 9:
        return False, f"btc_smoke: ema_len={params.ema_len} != 9 locked"
    if params.pds > 20:
        return False, f"btc_smoke: pds={params.pds} > 20 collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: DssBressertParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH CRITICAL)."""
    if params.pds not in {8, 10, 14} or params.trigger_len not in {3, 5} or params.ema_len != 9:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: DssBressertParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.pds <= 3:
        return False, "sol_smoke: 15m pds<=3 forbidden (spam)"
    if params.pds not in {8, 10, 14} or params.trigger_len not in {3, 5} or params.ema_len != 9:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DssBressertParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.pds not in {8, 10, 14} or params.trigger_len not in {3, 5} or params.ema_len != 9:
        return False, "bnb_smoke: params retuned away from locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DssBressertParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for dss-bressert-trigger-cross."""
    params = params or DssBressertParams()
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
    dss, trig = dss_bressert(
        highs, lows, closes,
        pds=params.pds,
        ema_len=params.ema_len,
        trigger_len=params.trigger_len,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(dss, trig, i)
        cross_dn = crossunder(dss, trig, i)

        if params.mode == "mode_b":
            # Mode B: cross while dss < 20; exit when dss > 80 or crossunder
            dss_val = dss[i]
            if dss_val is None or dss_val >= 20.0:
                cross_up = False
            if dss_val is not None and dss_val > 80.0:
                cross_dn = True

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
