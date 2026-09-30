"""ehlers-convolution-zero — Ehlers Convolution fold-correlation.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage25 NHNL thin-n ETH fail + DSP 0-BTC — need published fold-correlation series
  denser than NHNL without cloning CorrCycle/BandPass/DSP EXIT.
  Convolution (John Ehlers, Cycle Analytics for Traders pp. 170-174):
    prefilter price via HighPass and SuperSmoother;
    fold two equal-length segments about candidate turn (half = Lookback // 2);
    compute normalized Pearson correlation of the folded halves;
    peak correlation approx lookback/2 lag marks turns.
  Mode A:
    long crossover(conv, thr)
    exit crossunder(conv, thr) or peak-fade (conv < conv[1] and conv[1] >= conv[2] and conv[1] > thr)
  Mode B:
    require conv > conv[1] rising on entry — only if Mode A over-whips;
    identical params across all four coins.
  Prefer Lookback=18, thr=0.05 Mode A.
  != CorrCycle / != Spearman / != BandPass / != DSP / != CyberCycle / != EBSW.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill Lookback inflate until n collapses;
  Kill CorrCycle/BandPass/DSP substitute. Prefer Mode A (18, 0.05), 1H+.

eth_smoke:
  CRITICAL: Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill CorrCycle/BandPass labeled Convolution.
  Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill Lookback retuned only on SOL;
  15m spam; stage12-25 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: CorrCycle/Spearman/BandPass/DSP/CyberCycle/EBSW labeled Convolution;
Roofing/Autocorr-Periodogram primary; request.security; stage12-25 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, ehlers_convolution

STRATEGY_ID = "ehlers-convolution-zero"


@dataclass(frozen=True)
class EhlersConvolutionParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    lookback: int = 18            # 13, 18, 26, 39
    thr: float = 0.05             # 0.0, 0.05, 0.10
    exit_peak_fade: bool = True   # crossunder thr or peak-fade
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: EhlersConvolutionParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.lookback not in {13, 18, 26, 39}:
        return False, f"btc_smoke: lookback={params.lookback} not in {{13, 18, 26, 39}}"
    if params.thr not in {0.0, 0.05, 0.10}:
        return False, f"btc_smoke: thr={params.thr} not in {{0.0, 0.05, 0.10}}"
    return True, "PASS"


def validate_eth_smoke(params: EhlersConvolutionParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC PRIMARY CRITICAL)."""
    if params.lookback not in {13, 18, 26, 39} or params.thr not in {0.0, 0.05, 0.10}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: EhlersConvolutionParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.lookback not in {13, 18, 26, 39} or params.thr not in {0.0, 0.05, 0.10}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersConvolutionParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.lookback not in {13, 18, 26, 39} or params.thr not in {0.0, 0.05, 0.10}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersConvolutionParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-convolution-zero."""
    params = params or EhlersConvolutionParams()
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
    conv_vals = ehlers_convolution(closes, lookback=params.lookback)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(2, count):
        c = closes[i]
        h = highs[i]
        cur_conv = conv_vals[i]
        prev_conv = conv_vals[i - 1]
        prev2_conv = conv_vals[i - 2]

        if cur_conv is None or prev_conv is None:
            continue

        co_thr = (prev_conv <= params.thr) and (cur_conv > params.thr)
        cu_thr = (prev_conv >= params.thr) and (cur_conv < params.thr)

        peak_fade = False
        if params.exit_peak_fade and prev2_conv is not None:
            peak_fade = (cur_conv < prev_conv) and (prev_conv >= prev2_conv) and (prev_conv > params.thr)

        # Long entry logic
        if not in_pos:
            entry_cond = co_thr
            if params.mode == "mode_b":
                entry_cond = entry_cond and (cur_conv > prev_conv)

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

            exit_cond = cu_thr or peak_fade or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
