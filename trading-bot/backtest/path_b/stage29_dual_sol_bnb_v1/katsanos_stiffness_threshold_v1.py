"""katsanos-stiffness-threshold — Katsanos Stiffness (count above buffered MA) threshold cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage28 Vervoort 0.832x under-lead + EC/FIR/DV2 cost-chop 0-BTC + Stage26 FVE dense 1.055x FAIL LEAD —
  need published trend-quality seat != volume-flow FVE/VFI and != dual zero-lag TEMA stall.
  Stiffness (Katsanos TASC Nov 2018; mkatsanos.com; Thinkorswim; Traders Tips Nov 2018):
    ma = SMA(Close, MAB)
    sd = StDev(Close, MAB)
    ma2 = ma - NSTD * sd
    above = Close > ma2 ? 1.0 : 0.0
    stif = 100.0 * Sum(above, Period) / Period
    stiffness = EMA(stif, SM)
  Mode A:
    long crossover(stiffness, BuyThr)
    exit crossunder(stiffness, SellThr)
  Mode B:
    raise BuyThr (e.g. 95) and/or require rising stiffness (stiffness > stiffness[1]) — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (MAB=100, Period=60, NSTD=0.2, SM=3, BuyThr=90, SellThr=50) Mode A.
  != FVE / != VFI / != CHOP / != ADX / != Qstick.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20 (FVE 1.055x / Vervoort 0.832x rhyme);
  Kill MAB/Period inflate until n collapses; Kill FVE/VFI/CHOP/ADX labeled Stiffness.
  Prefer Mode A (100, 60, 0.2, 3, 90, 50), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill FVE labeled Stiffness. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill Period retuned only on SOL;
  15m spam; stage12-28 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: FVE/VFI/CHOP/ADX labeled Stiffness; EC/Vervoort/FIR/DV2 grafts;
request.security; stage12-28 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, katsanos_stiffness

STRATEGY_ID = "katsanos-stiffness-threshold"


@dataclass(frozen=True)
class KatsanosStiffnessParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    mab: int = 100                # 50, 100
    period: int = 60              # 40, 60, 80
    nstd: float = 0.2             # 0.2
    sm: int = 3                   # 3
    buy_thr: float = 90.0         # 75, 90, 95
    sell_thr: float = 50.0        # 40, 50, 60
    rising_req: bool = False      # Mode B option
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: KatsanosStiffnessParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.mab not in {50, 100}:
        return False, f"btc_smoke: mab={params.mab} not in {{50, 100}}"
    if params.period not in {40, 60, 80}:
        return False, f"btc_smoke: period={params.period} not in {{40, 60, 80}}"
    if params.buy_thr not in {75.0, 90.0, 95.0}:
        return False, f"btc_smoke: buy_thr={params.buy_thr} not in {{75, 90, 95}}"
    if params.sell_thr not in {40.0, 50.0, 60.0}:
        return False, f"btc_smoke: sell_thr={params.sell_thr} not in {{40, 50, 60}}"
    return True, "PASS"


def validate_eth_smoke(params: KatsanosStiffnessParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.mab not in {50, 100} or params.period not in {40, 60, 80}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: KatsanosStiffnessParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.mab not in {50, 100} or params.period not in {40, 60, 80}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: KatsanosStiffnessParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.mab not in {50, 100} or params.period not in {40, 60, 80}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KatsanosStiffnessParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for katsanos-stiffness-threshold."""
    params = params or KatsanosStiffnessParams()
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
    stiffness, stif_raw, ma2 = katsanos_stiffness(
        closes,
        mab=params.mab,
        period=params.period,
        nstd=params.nstd,
        sm=params.sm,
    )

    buy_series = [params.buy_thr] * count
    sell_series = [params.sell_thr] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(stiffness, buy_series, i)
        cross_dn = crossunder(stiffness, sell_series, i)

        rising = (
            stiffness[i] is not None
            and stiffness[i - 1] is not None
            and stiffness[i] > stiffness[i - 1]
        )

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and (rising if params.rising_req else True)
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
