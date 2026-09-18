"""vzo-zero-cross — Volume Zone Oscillator zero-cross.

LOCKED ENCODE ORDER #3 (BTC LEAD PRIMARY).
Thesis:
  Stage18 mid-cycle oscillators = 0 BTC. Historical BTC clearers carried volume-polarity energy.
  VZO (Walid Khalil) is signed-volume EMA ratio:
    signedVol = close > close[1] ? volume : (close < close[1] ? -volume : 0)
    vp = ema(signedVol, len)
    tv = ema(volume, len)
    vzo = 100 * vp / tv
  Mode A = VZO x 0 cross.
  Intended to clear dense BTC first without stage18 over-damp.
  != PZO (Khalil price sibling signs price change, stage13).
  != Bostian III / Intraday Intensity SMA-zero (stage17).
  != CMF / OBV.
  Identical len across all four coins.

Mode A (BTC-LEAD PRIMARY — prefer):
  long: crossover(vzo, 0)
  exit: crossunder(vzo, 0)

Mode B (BNB quiet / chatter):
  hold above +5 / below -5 N bars — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill len inflate until n collapses;
  Kill Mode A BTC 0 / chop; Kill PZO/III/CMF labeled VZO;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A len=14, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill len retuned only on ETH; Kill III/PZO labeled VZO.
  Prefer identical len=14; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m len=5; stage12-18 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different len; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: PZO labeled VZO; III / Intraday Intensity; CMF/OBV; stage12-18 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, vzo

STRATEGY_ID = "vzo-zero-cross"


@dataclass(frozen=True)
class VzoParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    length: int = 14
    hold_bars: int = 0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: VzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {10, 14, 21}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{10, 14, 21}}"
    if params.length > 40:
        return False, f"btc_smoke: length={params.length} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: VzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.length not in {10, 14, 21}:
        return False, f"eth_smoke: length={params.length} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m length<=5 forbidden (spam)"
    if params.length not in {10, 14, 21}:
        return False, "sol_smoke: length not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: VzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.length not in {10, 14, 21}:
        return False, "bnb_smoke: length not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VzoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vzo-zero-cross."""
    params = params or VzoParams()
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
    vzo_vals = vzo(closes, volumes, length=params.length)
    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    bars_since_cross = 999

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(vzo_vals, zero_line, i)
        cross_dn = crossunder(vzo_vals, zero_line, i)

        if cross_up:
            bars_since_cross = 0
        else:
            bars_since_cross += 1

        entry_trigger = False
        if params.mode == "mode_b" and params.hold_bars > 0:
            val = vzo_vals[i]
            if bars_since_cross == params.hold_bars and val is not None and val > 5.0:
                entry_trigger = True
        else:
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
