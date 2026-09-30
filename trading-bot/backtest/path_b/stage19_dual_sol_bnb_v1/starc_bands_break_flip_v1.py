"""starc-bands-break-flip — Stoller Average Range Channel bands break-flip.

LOCKED ENCODE ORDER #2 (BTC LEAD PRIMARY).
Thesis:
  Stage18 mid-cycle oscillators never left BTC; Keltner/BB/Donchian burned as primaries.
  STARC (Manning Stoller) = SMA +/- k * ATR.
  Center is strictly SMA (classic 6), != Keltner EMA, != Bollinger SMA +/- sigma.
  Mode A: close breakout above upper band -> long; cross under lower band -> exit.
  Intended BTC-clearing range expansion polarity without volume-flow III.
  Identical (smaLen, atrLen, k) on all four coins.
  != Keltner (EMA center).
  != Bollinger Bands (stdev bands).
  != Donchian Channels (HH/LL channel).
  != AccelBands (stage9).

Mode A (BTC-LEAD PRIMARY — prefer):
  long: crossover(close, upper)
  exit: crossunder(close, lower)

Mode B (BNB quiet / chatter):
  larger k / longer smaLen or exit on mid SMA — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill k/smaLen/atrLen inflate until breaks collapse;
  Kill Mode A BTC 0 / chop; Kill Keltner/BB/Donchian substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A (6,15,2), 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill params retuned only on ETH; Kill Keltner/BB/III labeled STARC.
  Prefer identical (6,15,2); ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m smaLen=3 k=1; stage12-18 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different (smaLen,atrLen,k); Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: Keltner/BB/Donchian labeled STARC; BB-squeeze; AccelBands; III/volume; stage12-18 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, starc_bands

STRATEGY_ID = "starc-bands-break-flip"


@dataclass(frozen=True)
class StarcParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    sma_len: int = 6
    atr_len: int = 15
    k: float = 2.0
    exit_on_mid: bool = False
    atr_trail_mult: float = 0.0


def validate_btc_smoke(params: StarcParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.sma_len not in {5, 6, 10}:
        return False, f"btc_smoke: sma_len={params.sma_len} not in locked sweep {{5, 6, 10}}"
    if params.atr_len not in {10, 15}:
        return False, f"btc_smoke: atr_len={params.atr_len} not in locked sweep {{10, 15}}"
    if params.k not in {1.5, 2.0, 2.5}:
        return False, f"btc_smoke: k={params.k} not in locked sweep {{1.5, 2.0, 2.5}}"
    if params.k > 3.5:
        return False, f"btc_smoke: k={params.k} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: StarcParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.sma_len not in {5, 6, 10} or params.atr_len not in {10, 15} or params.k not in {1.5, 2.0, 2.5}:
        return False, "eth_smoke: parameters retuned away from locked sweep"
    return True, "PASS"


def validate_sol_smoke(params: StarcParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and (params.sma_len <= 3 or params.k <= 1.0):
        return False, "sol_smoke: 15m smaLen<=3 or k<=1 forbidden (spam)"
    if params.sma_len not in {5, 6, 10} or params.atr_len not in {10, 15} or params.k not in {1.5, 2.0, 2.5}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: StarcParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.sma_len not in {5, 6, 10} or params.atr_len not in {10, 15} or params.k not in {1.5, 2.0, 2.5}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: StarcParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for starc-bands-break-flip."""
    params = params or StarcParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    upper, mid, lower = starc_bands(
        highs=highs,
        lows=lows,
        closes=closes,
        sma_len=params.sma_len,
        atr_len=params.atr_len,
        k=params.k,
    )
    atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(closes, upper, i)
        cross_dn_lower = crossunder(closes, lower, i)
        cross_dn_mid = crossunder(closes, mid, i)

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

            exit_band = cross_dn_mid if params.exit_on_mid else cross_dn_lower
            if stop_hit or exit_band:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
