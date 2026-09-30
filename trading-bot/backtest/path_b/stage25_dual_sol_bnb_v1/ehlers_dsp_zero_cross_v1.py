"""ehlers-dsp-zero-cross — Ehlers Detrended Synthetic Price zero-cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage24 BTC PASS 0/32; closest Kirshenbaum ~1.113x / stage23 Chande-Kroll ~1.194x —
  need published cycle-in-phase oscillator that can clear dense BTC >= 1.2x without
  cloning DPO / Decycler / BandPass EXIT.
  DSP (John Ehlers, MESA and Trading Market Cycles pp. 64-70):
    price = (high + low) / 2
    alpha = 2.0 / (Length + 1.0)
    alpha2 = alpha / 2.0
    EMA1 = alpha * price + (1.0 - alpha) * EMA1[1]
    EMA2 = alpha2 * price + (1.0 - alpha2) * EMA2[1]
    DSP = EMA1 - EMA2
  Mode A:
    long crossover(dsp, 0)
    exit crossunder(dsp, 0)
  Mode B:
    require dsp > dsp[1] rising on entry — only if Mode A over-whips;
    identical params across all four coins.
  Prefer Length=7 Mode A.
  != DPO (close - displaced SMA) / != Decycler (HP residual dual) /
  != BandPass (IIR bandpass zero) / != CyberCycle / != EBSW.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x / ~1.113x;
  Kill Length inflate until n collapses;
  Kill DPO/Decycler/BandPass/CyberCycle/EBSW labeled DSP. Prefer Mode A Length=7, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill Length retuned only on SOL;
  15m spam; stage12-24 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill Length retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: DPO/Decycler/BandPass/CyberCycle/EBSW labeled DSP;
request.security; stage12-24 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, ehlers_dsp

STRATEGY_ID = "ehlers-dsp-zero-cross"


@dataclass(frozen=True)
class EhlersDspParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    length: int = 7             # 5, 7, 9, 14
    atr_trail_mult: float = 0.0 # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: EhlersDspParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {5, 7, 9, 14}:
        return False, f"btc_smoke: length={params.length} not in {{5, 7, 9, 14}}"
    return True, "PASS"


def validate_eth_smoke(params: EhlersDspParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.length not in {5, 7, 9, 14}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: EhlersDspParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.length not in {5, 7, 9, 14}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersDspParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.length not in {5, 7, 9, 14}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersDspParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-dsp-zero-cross."""
    params = params or EhlersDspParams()
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
    dsp_vals = ehlers_dsp(highs, lows, params.length)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_dsp = dsp_vals[i]
        prev_dsp = dsp_vals[i - 1]

        if cur_dsp is None or prev_dsp is None:
            continue

        co_zero = (prev_dsp <= 0.0) and (cur_dsp > 0.0)
        cu_zero = (prev_dsp >= 0.0) and (cur_dsp < 0.0)

        # Long entry logic
        if not in_pos:
            entry_cond = co_zero
            if params.mode == "mode_b":
                entry_cond = entry_cond and (cur_dsp > prev_dsp)

            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * atr_vals[i]
        else:
            if h > highest_since_entry:
                highest_since_entry = h

            # ATR trailing stop
            atr_stop_hit = False
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                cur_stop = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                stops[i] = cur_stop
                if c < cur_stop:
                    atr_stop_hit = True

            exit_cond = cu_zero or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
