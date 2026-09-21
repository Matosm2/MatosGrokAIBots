"""ehlers-madh-zero-cross — Ehlers Moving Average Difference Hann zero-cross.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage30 wipe + need published dense cycle/impulse oscillator with frequent zero flips.
  MADH (John Ehlers TASC Nov 2021; ProRealCode / PineCodersTASC):
    Hann weights: w(i) = 1 - cos(360*i / (L + 1))
    Filt1 = sum(w * Close) / sum(w) over ShortLength
    Filt2 = sum(w * Close) / sum(w) over LongLength = floor(ShortLength + DominantCycle/2)
    MADH = 100 * (Filt1 - Filt2) / Filt2
  Mode A:
    long crossover(madh, 0)
    exit crossunder(madh, 0)
  Mode B:
    require rising confirm madh > madh[1] on entry —
    only if Mode A over-whips; identical across all four.
  Prefer (ShortLength=8, DominantCycle=27) Mode A.
  != MACD / != ZL-FIR*price / != BandPass / != RMO / != PPO.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill Dom inflated until BTC n collapses or Short shortened until spam;
  Kill MACD/ZL-FIR/BandPass/RMO substitute; Kill Track-B graft. Prefer Mode A (8, 27), 1H+.

eth_smoke:
  Kill params retuned only on ETH; Kill MACD labeled MADH. Prefer identical params.

sol_smoke:
  Kill params retuned only on SOL; 15m spam; stage1-30 grafts.

bnb_smoke:
  Kill params retuned only on BNB; Mode B only on BNB; ungated shorts.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_madh

STRATEGY_ID = "ehlers-madh-zero-cross"


@dataclass(frozen=True)
class EhlersMadhParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    short_length: int = 8         # 6, 8, 10
    dominant_cycle: int = 27      # 20, 27, 34
    rising_req: bool = False      # Mode B rising confirm
    atr_trail_mult: float = 0.0   # 0.0 (off)
    atr_len: int = 14


def validate_btc_smoke(params: EhlersMadhParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.short_length not in {6, 8, 10}:
        return False, f"btc_smoke: short_length={params.short_length} not in {{6, 8, 10}}"
    if params.dominant_cycle not in {20, 27, 34}:
        return False, f"btc_smoke: dominant_cycle={params.dominant_cycle} not in {{20, 27, 34}}"
    return True, "PASS"


def validate_eth_smoke(params: EhlersMadhParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation."""
    if params.short_length not in {6, 8, 10} or params.dominant_cycle not in {20, 27, 34}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: EhlersMadhParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.short_length not in {6, 8, 10} or params.dominant_cycle not in {20, 27, 34}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersMadhParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.short_length not in {6, 8, 10} or params.dominant_cycle not in {20, 27, 34}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersMadhParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-madh-zero-cross."""
    params = params or EhlersMadhParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    madh, filt1, filt2 = ehlers_madh(
        closes=closes,
        short_length=params.short_length,
        dominant_cycle=params.dominant_cycle,
    )
    zero_line = [0.0] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(madh, zero_line, i)
        cross_dn = crossunder(madh, zero_line, i)

        m_cur = madh[i]
        m_prev = madh[i - 1]
        rising = (m_cur is not None and m_prev is not None and m_cur > m_prev)

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and (rising or not params.rising_req)
            exit_cond = cross_dn
        else:
            entry_cond = cross_up
            exit_cond = cross_dn

        atr_stop_hit = False
        if in_pos and params.atr_trail_mult > 0.0:
            if highs[i] > highest_since_entry:
                highest_since_entry = highs[i]
            atr_v = atr_vals[i]
            if atr_v is not None:
                stop_level = highest_since_entry - params.atr_trail_mult * atr_v
                stops[i] = stop_level
                if closes[i] < stop_level:
                    atr_stop_hit = True

        if not in_pos:
            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = highs[i]
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = highest_since_entry - params.atr_trail_mult * atr_vals[i]
        else:
            if exit_cond or atr_stop_hit:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0

    return buys, sells, stops
