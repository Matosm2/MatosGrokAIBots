"""historical-volatility-ratio-expand-dir — Historical Volatility Ratio (HV short / HV long) expand x dir.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage27 Schwager VR∩Donchian 0.698x EXIT + Stage21 Parkinson HV expansion x dir 0-BTC EXIT —
  need distinct published HV ratio of log-return stdevs (not Japanese True-Range VR; not Parkinson ln(H/L) RMS).
  HVR (TC2000 / Sierra / public HV literature):
    lr = ln(Close / Close[1])
    hvS = stdev(lr, shortLen)
    hvL = stdev(lr, longLen)
    hvr = hvS / hvL
  Mode A:
    long crossover(hvr, ExpandThr) and close > close[dirLen]
    exit crossunder(hvr, ExpandThr) or close < close[dirLen]
  Mode B:
    require prior compression hvr[1] < CompThr (e.g. 0.5) before expand — only if Mode A over-whips;
    identical params across all four coins.
  Prefer short=10, long=100, ExpandThr=0.5, dirLen=5 Mode A.
  != Schwager VR / != Parkinson / != Chaikin / != ATR-ratio.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill ExpandThr inflate until n collapses; Kill Schwager-VR / Parkinson / Chaikin / ATR-ratio labeled HVR.
  Prefer Mode A (10, 100, 0.5, 5), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill Parkinson labeled HVR. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill params retuned only on SOL;
  Parkinson graft; stage12-28 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill Mode B only on BNB.
  Prefer identical; long-only; ATR exit.

Forbidden: Schwager VR∩Donchian / Parkinson ln(H/L)×dir / Chaikin / ATR-ratio labeled HVR;
request.security; stage12-28 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, historical_volatility_ratio

STRATEGY_ID = "historical-volatility-ratio-expand-dir"


@dataclass(frozen=True)
class HvrExpandDirParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    short_len: int = 10           # 6, 10, 14
    long_len: int = 100           # 50, 100
    expand_thr: float = 0.5       # 0.4, 0.5, 0.6
    dir_len: int = 5              # 3, 5, 8
    comp_thr: float = 0.5         # 0.5 for Mode B prior compression
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: HvrExpandDirParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.short_len not in {6, 10, 14}:
        return False, f"btc_smoke: short_len={params.short_len} not in {{6, 10, 14}}"
    if params.long_len not in {50, 100}:
        return False, f"btc_smoke: long_len={params.long_len} not in {{50, 100}}"
    if params.expand_thr not in {0.4, 0.5, 0.6}:
        return False, f"btc_smoke: expand_thr={params.expand_thr} not in {{0.4, 0.5, 0.6}}"
    if params.dir_len not in {3, 5, 8}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in {{3, 5, 8}}"
    return True, "PASS"


def validate_eth_smoke(params: HvrExpandDirParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.short_len not in {6, 10, 14} or params.long_len not in {50, 100}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: HvrExpandDirParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.short_len not in {6, 10, 14} or params.long_len not in {50, 100}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: HvrExpandDirParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.short_len not in {6, 10, 14} or params.long_len not in {50, 100}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: HvrExpandDirParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for historical-volatility-ratio-expand-dir."""
    params = params or HvrExpandDirParams()
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
    hvr, hvs, hvl = historical_volatility_ratio(
        closes,
        short_len=params.short_len,
        long_len=params.long_len,
    )

    thr_series = [params.expand_thr] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up_hvr = crossover(hvr, thr_series, i)
        cross_dn_hvr = crossunder(hvr, thr_series, i)

        dir_ok = False
        if i >= params.dir_len:
            dir_ok = closes[i] > closes[i - params.dir_len]

        if params.mode == "mode_a":
            entry_cond = cross_up_hvr and dir_ok
            exit_cond = cross_dn_hvr or not dir_ok
        elif params.mode == "mode_b":
            # Require prior compression: hvr[1] < comp_thr
            prior_comp = (hvr[i - 1] is not None) and (hvr[i - 1] < params.comp_thr)
            entry_cond = cross_up_hvr and dir_ok and prior_comp
            exit_cond = cross_dn_hvr or not dir_ok
        else:
            entry_cond = cross_up_hvr and dir_ok
            exit_cond = cross_dn_hvr or not dir_ok

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
