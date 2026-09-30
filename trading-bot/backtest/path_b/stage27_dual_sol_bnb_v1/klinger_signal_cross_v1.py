"""klinger-signal-cross — Stephen Klinger Volume Oscillator KVO x signal EMA cross.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage26 FVE dense-under-1.2x — need published volume-force oscillator x signal
  denser / differently constructed than FVE cutoff money-flow, without cloning VFI/VROC/VPCI EXIT.
  KVO (Stephen Klinger; Capital.com / Investopedia / CQG / thinkorswim):
    Full VF from trend x dm/cm
    kvo = ema(vf, fast) - ema(vf, slow)
    sig = ema(kvo, signalLen)
  Mode A:
    long crossover(kvo, sig)
    exit crossunder(kvo, sig)
  Mode B:
    require kvo > 0 on entry — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (34, 55, 13) Mode A.
  != FVE / != VFI / != VROC / != VPCI / != Chaikin Osc / != PVO / != OBV.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill lengths inflate until n collapses; Kill FVE/VFI/VROC/VPCI/PVO labeled Klinger.
  Prefer Mode A (34, 55, 13), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill FVE labeled Klinger. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill lengths retuned only on SOL;
  FVE graft; stage12-26 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: FVE/VFI/VROC/VPCI/ChaikinOsc/PVO/OBV/MACD-of-price labeled Klinger;
request.security; stage12-26 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, klinger_oscillator

STRATEGY_ID = "klinger-signal-cross"


@dataclass(frozen=True)
class KlingerParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    fast: int = 34                # 21, 34, 55
    slow: int = 55                # 34, 55, 89
    signal_len: int = 13          # 9, 13
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: KlingerParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    valid_pairs = {(21, 34), (34, 55), (55, 89)}
    if (params.fast, params.slow) not in valid_pairs:
        return False, f"btc_smoke: (fast,slow)=({params.fast},{params.slow}) not in {valid_pairs}"
    if params.signal_len not in {9, 13}:
        return False, f"btc_smoke: signal_len={params.signal_len} not in {{9, 13}}"
    return True, "PASS"


def validate_eth_smoke(params: KlingerParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    valid_pairs = {(21, 34), (34, 55), (55, 89)}
    if (params.fast, params.slow) not in valid_pairs or params.signal_len not in {9, 13}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: KlingerParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    valid_pairs = {(21, 34), (34, 55), (55, 89)}
    if (params.fast, params.slow) not in valid_pairs or params.signal_len not in {9, 13}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: KlingerParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    valid_pairs = {(21, 34), (34, 55), (55, 89)}
    if (params.fast, params.slow) not in valid_pairs or params.signal_len not in {9, 13}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KlingerParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for klinger-signal-cross."""
    params = params or KlingerParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    kvo_vals, sig_vals = klinger_oscillator(
        highs, lows, closes, volumes,
        fast=params.fast, slow=params.slow, signal_len=params.signal_len,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        k_cur = kvo_vals[i]
        k_prev = kvo_vals[i - 1]
        s_cur = sig_vals[i]
        s_prev = sig_vals[i - 1]

        if k_cur is None or k_prev is None or s_cur is None or s_prev is None:
            continue

        crossover_sig = k_prev <= s_prev and k_cur > s_cur
        crossunder_sig = k_prev >= s_prev and k_cur < s_cur

        if params.mode == "mode_a":
            entry_cond = crossover_sig
            exit_cond = crossunder_sig
        elif params.mode == "mode_b":
            entry_cond = crossover_sig and (k_cur > 0.0)
            exit_cond = crossunder_sig
        else:
            entry_cond = crossover_sig
            exit_cond = crossunder_sig

        # ATR trailing check
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
