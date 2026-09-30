"""heikin-ashi-bias-flip — Heikin-Ashi Bias (HA close vs HA open polarity flip).

LOCKED ENCODE ORDER #1 (BTC LEAD + SOL DENSE PRIMARY).
Thesis:
  Stage16 Kagi cleared BTC+ETH then SOL 0.807x (under 1.2x gate).
  Structure clones (3LB/Kagi) stall under SOL gate.
  Heikin-Ashi bias flip is a candle-transform polarity rule (not continuous-line structure):
  long while HA_close > HA_open; flip/exit when HA_close < HA_open.
  Averaged OHLC path participates denser on impulsive SOL than Yang/Yin reversal-amount stalls,
  staying majors-portable with identical construction.
  != HA-streak (burned: N consecutive same-color required).
  != 3LB/Kagi/Renko structure clones.

Formula:
  HA_Close = (O + H + L + C) / 4
  HA_Open = (HA_Open[1] + HA_Close[1]) / 2 (seed: (O[0] + C[0]) / 2)
  bull = haClose > haOpen
  Recurse on closed OHLC (var) — do NOT switch chart type as data source.

Mode A (BTC-LEAD + SOL-dense — prefer):
  long when bull and not bull[1]; exit when not bull and bull[1]. confirm=1.

Mode B (BNB quiet / SOL chatter):
  require 2 consecutive bull bars to enter / 2 bear bars to exit — only if Mode A over-whips;
  identical confirm (!= HA-streak N>=3 as Mode A).

btc_smoke:
  BTC-LEAD CRITICAL: Kill confirm inflate until flips collapse;
  Kill HA-streak N>=3 as Mode A;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A confirm=1, 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill BTC-clear->ETH-wipe;
  Kill confirm retuned only on ETH; Kill Kagi/3LB substitute.
  Prefer identical; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill if BTC+ETH >=1.2x then SOL under 1.2x;
  Kill Kagi/3LB/Renko labeled HA; 15m spam; stage12-16 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different confirm; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: HA-streak N>=3 Mode A; Kagi/3LB/Renko mislabel; request.security HA TF; stage12-16.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, heikin_ashi_bias

STRATEGY_ID = "heikin-ashi-bias-flip"


@dataclass(frozen=True)
class HeikinAshiParams:
    mode: str = "mode_a"  # "mode_a" (confirm=1) | "mode_b" (confirm=2)
    confirm: int = 1
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: HeikinAshiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.confirm not in {1, 2}:
        return False, f"btc_smoke: confirm={params.confirm} not in locked set {{1, 2}}"
    if params.confirm >= 3:
        return False, f"btc_smoke: confirm={params.confirm} is forbidden HA-streak (N>=3)"
    return True, "PASS"


def validate_eth_smoke(params: HeikinAshiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH CRITICAL)."""
    if params.confirm not in {1, 2}:
        return False, f"eth_smoke: confirm={params.confirm} not in locked set {{1, 2}}"
    if params.confirm >= 3:
        return False, f"eth_smoke: confirm={params.confirm} is forbidden HA-streak (N>=3)"
    return True, "PASS"


def validate_sol_smoke(params: HeikinAshiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden (spam)"
    if params.confirm not in {1, 2}:
        return False, f"sol_smoke: confirm={params.confirm} not in locked set {{1, 2}}"
    return True, "PASS"


def validate_bnb_smoke(params: HeikinAshiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.confirm not in {1, 2}:
        return False, f"bnb_smoke: confirm={params.confirm} not in locked set {{1, 2}}"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: HeikinAshiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for heikin-ashi-bias-flip."""
    params = params or HeikinAshiParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    _, _, bull = heikin_ashi_bias(opens, highs, lows, closes)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.confirm == 1:
            cross_up = bull[i] and not bull[i - 1]
            cross_dn = not bull[i] and bull[i - 1]
        else:  # confirm == 2
            cross_up = bull[i] and bull[i - 1] and (i < 2 or not bull[i - 2])
            cross_dn = not bull[i] and not bull[i - 1] and (i < 2 or bull[i - 2])

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
