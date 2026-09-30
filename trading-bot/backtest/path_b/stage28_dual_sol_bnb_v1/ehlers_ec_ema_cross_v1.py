"""ehlers-ec-ema-cross — Ehlers-Way Zero-Lag Error-Correcting EC x EMA cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage27 VR 0.698x regress + pack BTC 0/32 + Stage26 FVE dense 1.055x FAIL LEAD —
  need published denser trend impulse that can push BTC past FVE's under-1.2x neighborhood
  without cloning Qstick/Klinger/Envelopes/VR or ZLEMA stage4.
  EC (Ehlers & Way, S&C / MESA ZeroLag.pdf; Sacred Traders; Wealth-Lab TASC Nov 2010):
    alpha = 2 / (Length + 1)
    ema = alpha * close + (1 - alpha) * ema[1]
    Gain search in [-GainLimit/10 .. +GainLimit/10] min |close - EC|
    EC = alpha * (ema + BestGain * (close - EC[1])) + (1 - alpha) * EC[1]
  Mode A:
    long crossover(ec, ema)
    exit crossunder(ec, ema)
  Mode B:
    require 100.0 * LeastError / close > Thresh — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (Length=20, GainLimit=50, Thresh=0) Mode A.
  != ZLEMA / != EDCF filt*lag / != Ultimate Smoother / != PMA.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20 (FVE 1.055x / VR 0.698x rhyme);
  Kill Length/Gain inflate until n collapses; Kill ZLEMA/EDCF/US labeled EC.
  Prefer Mode A (20, 50, 0), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill ZLEMA labeled EC. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill Length retuned only on SOL;
  15m spam; stage12-27 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: ZLEMA/EDCF/US/PMA labeled EC; Qstick/Klinger/Envelopes/VR grafts;
request.security; stage12-27 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_ec

STRATEGY_ID = "ehlers-ec-ema-cross"


@dataclass(frozen=True)
class EhlersEcParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    length: int = 20              # 12, 20, 32
    gain_limit: int = 50          # 22, 50
    thresh: float = 0.0           # 0.0, 0.5, 0.75
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: EhlersEcParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {12, 20, 32}:
        return False, f"btc_smoke: length={params.length} not in {{12, 20, 32}}"
    if params.gain_limit not in {22, 50}:
        return False, f"btc_smoke: gain_limit={params.gain_limit} not in {{22, 50}}"
    if params.thresh not in {0.0, 0.5, 0.75}:
        return False, f"btc_smoke: thresh={params.thresh} not in {{0.0, 0.5, 0.75}}"
    return True, "PASS"


def validate_eth_smoke(params: EhlersEcParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.length not in {12, 20, 32} or params.gain_limit not in {22, 50}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: EhlersEcParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.length not in {12, 20, 32} or params.gain_limit not in {22, 50}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersEcParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.length not in {12, 20, 32} or params.gain_limit not in {22, 50}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersEcParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-ec-ema-cross."""
    params = params or EhlersEcParams()
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
    ec_vals, ema_vals, err_pcts = ehlers_ec(closes, params.length, params.gain_limit)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        crossover_ec_ema = crossover(ec_vals, ema_vals, i)
        crossunder_ec_ema = crossunder(ec_vals, ema_vals, i)

        if params.mode == "mode_a":
            entry_cond = crossover_ec_ema
            exit_cond = crossunder_ec_ema
        elif params.mode == "mode_b":
            err_ok = (err_pcts[i] is not None) and (err_pcts[i] > params.thresh)
            entry_cond = crossover_ec_ema and err_ok
            exit_cond = crossunder_ec_ema
        else:
            entry_cond = crossover_ec_ema
            exit_cond = crossunder_ec_ema

        # Check ATR stop if enabled and in position
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
