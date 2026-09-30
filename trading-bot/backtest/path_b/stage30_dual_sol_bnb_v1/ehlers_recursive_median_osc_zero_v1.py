"""ehlers-recursive-median-osc-zero — John Ehlers Recursive Median Oscillator zero crossover.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage29 wipe + need published cycle/impulse oscillator denser than DVS mid-reclaim
  without cloning BandPass / naked two-pole HP / DSP / CorrCycle / RocketRSI.
  RMO (John Ehlers TASC Mar 2018 "Recursive Median Filters"; ProRealCode / MQL5 mladen):
    med = Median(Close, 5)
    alpha1 = (cos(2*pi/LP) + sin(2*pi/LP) - 1.0) / cos(2*pi/LP)
    RM = alpha1 * med + (1 - alpha1) * RM[1]
    alpha2 = (cos(0.707*2*pi/HP) + sin(0.707*2*pi/HP) - 1.0) / cos(0.707*2*pi/HP)
    RMO = (1 - alpha2/2)^2 * (RM - 2*RM[1] + RM[2]) + 2*(1 - alpha2)*RMO[1] - (1 - alpha2)^2 * RMO[2]
  Mode A:
    long crossover(rmo, 0)
    exit crossunder(rmo, 0)
  Mode B:
    require rmo > rmo[1] rising on entry — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (LP=12, HP=30, medLen=5) Mode A.
  != BandPass / != naked-HP-of-price / != DSP / != CorrCycle / != RSI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill HP inflate/spam; Kill BandPass/naked-HP/DSP/CorrCycle labeled RMO;
  Kill Track-B graft. Prefer Mode A (12, 30), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill BandPass labeled RMO. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill LP/HP retuned only on SOL;
  Kill 15m spam; stage12-29 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Kill Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: BandPass / naked-HP-of-price / DSP / CorrCycle / Cyber / EBSW labeled RMO; Track-B four; stage12-29.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_rmo

STRATEGY_ID = "ehlers-recursive-median-osc-zero"


@dataclass(frozen=True)
class EhlersRmoParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    lp: int = 12                  # 8, 12, 16
    hp: int = 30                  # 20, 30, 40
    med_len: int = 5              # 5
    rising_req: bool = False      # Mode B option
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: EhlersRmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.lp not in {8, 12, 16}:
        return False, f"btc_smoke: lp={params.lp} not in {{8, 12, 16}}"
    if params.hp not in {20, 30, 40}:
        return False, f"btc_smoke: hp={params.hp} not in {{20, 30, 40}}"
    if params.med_len != 5:
        return False, f"btc_smoke: med_len={params.med_len} != 5"
    return True, "PASS"


def validate_eth_smoke(params: EhlersRmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.lp not in {8, 12, 16} or params.hp not in {20, 30, 40} or params.med_len != 5:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: EhlersRmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.lp not in {8, 12, 16} or params.hp not in {20, 30, 40} or params.med_len != 5:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersRmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.lp not in {8, 12, 16} or params.hp not in {20, 30, 40} or params.med_len != 5:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersRmoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-recursive-median-osc-zero."""
    params = params or EhlersRmoParams()
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
    rmo, _ = ehlers_rmo(
        closes=closes,
        lp=params.lp,
        hp=params.hp,
        med_len=params.med_len,
    )

    zero_line = [0.0] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(rmo, zero_line, i)
        cross_dn = crossunder(rmo, zero_line, i)

        rising = (
            rmo[i] is not None
            and rmo[i - 1] is not None
            and rmo[i] > rmo[i - 1]
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
