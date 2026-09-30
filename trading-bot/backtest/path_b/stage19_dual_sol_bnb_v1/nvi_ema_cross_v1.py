"""nvi-ema-cross — Negative Volume Index x EMA signal cross.

LOCKED ENCODE ORDER #4 (BTC LEAD PRIMARY).
Thesis:
  Stage18 never left BTC. NVI (Dysart / Fosback) accumulates price changes
  strictly on down-volume bars:
    var nvi = 1000.0
    nvi := volume < volume[1] ? nvi * (close / close[1]) : nvi (multiplicative Fosback)
    sig = ema(nvi, sigLen)
  Mode A = NVI x EMA signal cross.
  Intended BTC-clearing cumulative smart-money polarity with responsive 1H signal length.
  != OBV (accumulates on all volume bars).
  != PVI (positive volume index).
  != CMF / III (stage17).
  Identical sigLen across all four coins.

Mode A (BTC-LEAD PRIMARY — prefer):
  long: crossover(nvi, sig)
  exit: crossunder(nvi, sig)

Mode B (BNB quiet / chatter):
  longer sigLen or ATR trail — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill sigLen->255-on-1H until n collapses;
  Kill Mode A BTC 0 / chop; Kill OBV/III substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A sigLen=50, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill sigLen retuned only on ETH; Kill OBV/III/PZO labeled NVI.
  Prefer identical sigLen=50; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m sigLen=5; stage12-18 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different sigLen; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: OBV labeled NVI; PVI primary; III/CMF; stage12-18 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, nvi

STRATEGY_ID = "nvi-ema-cross"


@dataclass(frozen=True)
class NviParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    sig_len: int = 50
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: NviParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.sig_len not in {21, 50, 100}:
        return False, f"btc_smoke: sig_len={params.sig_len} not in locked sweep {{21, 50, 100}}"
    if params.sig_len > 200:
        return False, f"btc_smoke: sig_len={params.sig_len} collapses BTC n on 1H"
    return True, "PASS"


def validate_eth_smoke(params: NviParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.sig_len not in {21, 50, 100}:
        return False, f"eth_smoke: sig_len={params.sig_len} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: NviParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.sig_len <= 5:
        return False, "sol_smoke: 15m sigLen<=5 forbidden (spam)"
    if params.sig_len not in {21, 50, 100}:
        return False, "sol_smoke: sig_len not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: NviParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.sig_len not in {21, 50, 100}:
        return False, "bnb_smoke: sig_len not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: NviParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for nvi-ema-cross."""
    params = params or NviParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    nvi_vals, sig_vals = nvi(closes, volumes, sig_len=params.sig_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(nvi_vals, sig_vals, i)
        cross_dn = crossunder(nvi_vals, sig_vals, i)

        entry_trigger = cross_up

        if not in_pos:
            if entry_trigger:
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
