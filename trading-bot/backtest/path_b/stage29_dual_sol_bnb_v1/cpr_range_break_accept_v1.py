"""cpr-range-break-accept — Central Pivot Range (CPR) TC/BC range break-accept.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage28 wipe + need published structure impulse denser than VR 0.698x without cloning
  stage1 classic-floor-pivots-utc R1/S1 set, Camarilla, Woodie, or HHLL BOS.
  CPR (public Ochoa / Groww / Quantzee / StockManiacs):
    Same-TF lookback (no request.security):
      ph = highest(H, N)[1]
      pl = lowest(L, N)[1]
      pc = close[1]
      P = (ph + pl + pc) / 3.0
      BC = (ph + pl) / 2.0
      TC = 2.0 * P - BC
      if TC < BC: swap(TC, BC)
      cprW = TC - BC
  Mode A:
    long crossover(close, TC)
    exit crossunder(close, BC)
  Mode B:
    require narrow CPR (cprW / P < narrowPct) before TC break — only if Mode A over-whips;
    identical params across all four coins.
  Prefer N=24 Mode A.
  != Classic floor R1/S1 (R1=2P-L / S1=2P-H) / != Camarilla / != Woodie / != HHLL BOS.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill N inflate until n collapses; Kill floor-R1/Camarilla/Woodie/HHLL labeled CPR.
  Prefer Mode A N=24, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill classic floor R1 labeled CPR. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill N retuned only on SOL;
  15m spam; stage12-28 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: Classic floor R1/S1 ladder; Camarilla; Woodie; HHLL/BOS;
request.security; stage12-28 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, cpr_range, crossover, crossunder

STRATEGY_ID = "cpr-range-break-accept"


@dataclass(frozen=True)
class CprRangeParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    n: int = 24                   # 12, 24, 48
    narrow_pct: float = 0.002     # 0.001, 0.002, 0.005 for Mode B
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: CprRangeParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {12, 24, 48}:
        return False, f"btc_smoke: n={params.n} not in {{12, 24, 48}}"
    if params.narrow_pct not in {0.001, 0.002, 0.005}:
        return False, f"btc_smoke: narrow_pct={params.narrow_pct} not in {{0.001, 0.002, 0.005}}"
    return True, "PASS"


def validate_eth_smoke(params: CprRangeParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.n not in {12, 24, 48}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: CprRangeParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {12, 24, 48}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: CprRangeParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.n not in {12, 24, 48}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: CprRangeParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for cpr-range-break-accept."""
    params = params or CprRangeParams()
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
    tc, p_series, bc, width_series = cpr_range(highs, lows, closes, n=params.n)

    close_series: list[float | None] = [float(c) for c in closes]

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_above_tc = crossover(close_series, tc, i)
        cross_below_bc = crossunder(close_series, bc, i)

        if params.mode == "mode_a":
            entry_cond = cross_above_tc
            exit_cond = cross_below_bc
        elif params.mode == "mode_b":
            # Narrow CPR condition on prior or current bar
            narrow_ok = False
            p_val = p_series[i]
            w_val = width_series[i]
            if p_val is not None and w_val is not None and p_val > 0:
                narrow_ok = (w_val / p_val) < params.narrow_pct
            entry_cond = cross_above_tc and narrow_ok
            exit_cond = cross_below_bc
        else:
            entry_cond = cross_above_tc
            exit_cond = cross_below_bc

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
