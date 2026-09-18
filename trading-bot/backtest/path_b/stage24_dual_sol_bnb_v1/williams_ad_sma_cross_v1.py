"""williams-ad-sma-cross — Williams Accumulation/Distribution WAD × SMA cross.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage23 0-BTC / 1.194x near-miss; Stage-22 VFI cleared BTC->ETH — need
  price-only accumulation impulse without cloning AccDist/ASI/CLV/VFI/OBV.
  Williams AD (WAD):
    cumulative; if C > C[1]: WAD += C - min(L, C[1])
    if C < C[1]: WAD += C - max(H, C[1])
    else unchanged — No volume.
    sig = ta.sma(wad, m)
  Mode A:
    long crossover(wad, sig)
    exit crossunder(wad, sig)
  Mode B:
    require wad > wad[1] rising — only if Mode A over-whips;
    identical params across all four coins.
  Prefer m=21 Mode A.
  != AccDist (CLV*vol) / != ASI / != CLV / != OBV / != VFI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x;
  Kill m inflate until n collapses;
  Kill AccDist/ASI/CLV/OBV/VFI labeled WAD. Prefer Mode A m=21, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill m retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill m retuned only on SOL;
  AccDist/VFI graft; stage12-23 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill m retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: AccDist/CLV*vol/ASI/OBV/VFI labeled WAD; volume graft into WAD;
request.security; stage12-23 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, williams_ad

STRATEGY_ID = "williams-ad-sma-cross"


@dataclass(frozen=True)
class WilliamsAdParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    m: int = 21                 # 14, 21, 34
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: WilliamsAdParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.m not in {14, 21, 34}:
        return False, f"btc_smoke: m={params.m} not in {{14, 21, 34}}"
    return True, "PASS"


def validate_eth_smoke(params: WilliamsAdParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.m not in {14, 21, 34}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: WilliamsAdParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.m not in {14, 21, 34}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: WilliamsAdParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.m not in {14, 21, 34}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: WilliamsAdParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for williams-ad-sma-cross."""
    params = params or WilliamsAdParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    wad_vals, sig_vals = williams_ad(highs, lows, closes, params.m)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_wad = wad_vals[i]
        prev_wad = wad_vals[i - 1]
        cur_sig = sig_vals[i]
        prev_sig = sig_vals[i - 1]

        if not in_pos:
            # Entry: crossover(wad, sig)
            if (
                cur_wad is not None
                and prev_wad is not None
                and cur_sig is not None
                and prev_sig is not None
            ):
                cross_up = (prev_wad <= prev_sig) and (cur_wad > cur_sig)
                if cross_up:
                    can_enter = True
                    if params.mode == "mode_b":
                        if cur_wad <= prev_wad:
                            can_enter = False
                    if can_enter:
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

            # Exit: crossunder(wad, sig)
            cross_exit = False
            if (
                cur_wad is not None
                and prev_wad is not None
                and cur_sig is not None
                and prev_sig is not None
            ):
                cross_exit = (prev_wad >= prev_sig) and (cur_wad < cur_sig)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
