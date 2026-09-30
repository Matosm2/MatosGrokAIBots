"""blau-dti-zero-cross — Blau Directional Trend Index (DTI) zero crossover.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage29 DVS 1.093x near-miss under-1.20 + Stiffness/CPR under + HVR BTC FAIL —
  need published dense directional impulse != MR mid-reclaim / stiffness / CPR / HVR / Track-B ATR-corridor.
  DTI (William Blau, "Momentum, Direction, and Divergence"; MQL5 Blau_DTI / Blau_HLM):
    HMU = max(High - High[q-1], 0)
    LMD = max(Low[q-1] - Low, 0)
    HLM = HMU - LMD
    DTI = 100 * EMA3(HLM) / EMA3(|HLM|) periods (r, s, u).
  Mode A:
    long crossover(dti, 0)
    exit crossunder(dti, 0)
  Mode B:
    require dti > dti[1] rising on entry — only if Mode A over-whips;
    identical params across all four coins — still not +/-25 fade primary.
  Prefer (q=2, r=20, s=5, u=3) Mode A.
  != ADX / != TSI / != Blau CSI / != Blau MDI / != RAVI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20 (DVS 1.093x rhyme);
  Kill r/s/u inflate until n collapses; Kill ADX/TSI/CSI/MDI labeled DTI; Kill Track-B grafts.
  Prefer Mode A (2, 20, 5, 3), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill params retuned only on SOL;
  15m spam; stage12-29 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: ADX/TSI/Blau-CSI/MDI labeled DTI; Stiffness/CPR/DVS/HVR; Track-B four; stage12-29.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, blau_dti, crossover, crossunder

STRATEGY_ID = "blau-dti-zero-cross"


@dataclass(frozen=True)
class BlauDtiParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    q: int = 2                    # 1, 2, 3
    r: int = 20                   # 10, 20, 32
    s: int = 5                    # 3, 5
    u: int = 3                    # 1, 3
    rising_req: bool = False      # Mode B option
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: BlauDtiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.q not in {1, 2, 3}:
        return False, f"btc_smoke: q={params.q} not in {{1, 2, 3}}"
    if params.r not in {10, 20, 32}:
        return False, f"btc_smoke: r={params.r} not in {{10, 20, 32}}"
    if params.s not in {3, 5}:
        return False, f"btc_smoke: s={params.s} not in {{3, 5}}"
    if params.u not in {1, 3}:
        return False, f"btc_smoke: u={params.u} not in {{1, 3}}"
    return True, "PASS"


def validate_eth_smoke(params: BlauDtiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.q not in {1, 2, 3} or params.r not in {10, 20, 32} or params.s not in {3, 5} or params.u not in {1, 3}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: BlauDtiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.q not in {1, 2, 3} or params.r not in {10, 20, 32} or params.s not in {3, 5} or params.u not in {1, 3}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: BlauDtiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.q not in {1, 2, 3} or params.r not in {10, 20, 32} or params.s not in {3, 5} or params.u not in {1, 3}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: BlauDtiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for blau-dti-zero-cross."""
    params = params or BlauDtiParams()
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
    dti, _, _ = blau_dti(
        highs=highs,
        lows=lows,
        q=params.q,
        r=params.r,
        s=params.s,
        u=params.u,
    )

    zero_line = [0.0] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(dti, zero_line, i)
        cross_dn = crossunder(dti, zero_line, i)

        rising = (
            dti[i] is not None
            and dti[i - 1] is not None
            and dti[i] > dti[i - 1]
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
