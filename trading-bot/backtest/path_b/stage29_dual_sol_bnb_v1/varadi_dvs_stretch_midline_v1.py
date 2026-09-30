"""varadi-dvs-stretch-midline — Varadi DVS stretch percent-rank midline reclaim.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage15 seated DVI then EXIT; stage28 seated DV2 then EXIT cost-chop —
  both Varadi family but distinct constructions.
  DVS (CSS Analytics 2009-07-31):
    ds = +1 up / -1 down / 0 flat
    sumDS = sum(ds, sumLen)
    raw = 0.5 * (sumDS + sumDS[1])
    dvs = 100.0 * percentrank(raw, rankLen)
  Mode A:
    long crossover(dvs, 50)
    exit crossunder(dvs, 50)
    Trend-port mid-reclaim — not fade DVS<20.
  Mode B:
    reclaim through 40 exit at 50 — only if Mode A under-fires;
    identical across all four — still not fade-short primary.
  Prefer sumLen=20, rankLen=100, mid=50 Mode A.
  != DVI (composite magnitude+stretch) / != DV2 (close/(high+low)) / != PSY.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill rankLen inflate/spam; Kill DVI/DV2/PSY labeled DVS; Kill Mode B fade-shorts forced.
  Prefer Mode A sumLen=20 rankLen=100 mid-50, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill DV2 labeled DVS. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill rankLen retuned only on SOL;
  DV2 graft; stage12-28 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: DVI / DV2 / PSY labeled DVS; EC/Vervoort/FIR grafts;
request.security; stage12-28 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, varadi_dvs

STRATEGY_ID = "varadi-dvs-stretch-midline"


@dataclass(frozen=True)
class VaradiDvsParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    sum_len: int = 20             # 10, 20, 40
    rank_len: int = 100           # 63, 100, 126, 252
    mid: float = 50.0             # 50.0 (Mode A)
    entry_thr_b: float = 40.0     # 40.0 (Mode B reclaim)
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: VaradiDvsParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.sum_len not in {10, 20, 40}:
        return False, f"btc_smoke: sum_len={params.sum_len} not in {{10, 20, 40}}"
    if params.rank_len not in {63, 100, 126, 252}:
        return False, f"btc_smoke: rank_len={params.rank_len} not in {{63, 100, 126, 252}}"
    return True, "PASS"


def validate_eth_smoke(params: VaradiDvsParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.sum_len not in {10, 20, 40} or params.rank_len not in {63, 100, 126, 252}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VaradiDvsParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.sum_len not in {10, 20, 40} or params.rank_len not in {63, 100, 126, 252}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: VaradiDvsParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.sum_len not in {10, 20, 40} or params.rank_len not in {63, 100, 126, 252}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VaradiDvsParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for varadi-dvs-stretch-midline."""
    params = params or VaradiDvsParams()
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
    dvs_series, raw_series = varadi_dvs(
        closes,
        sum_len=params.sum_len,
        rank_len=params.rank_len,
    )

    mid_series = [params.mid] * count
    mode_b_thr_series = [params.entry_thr_b] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_above_mid = crossover(dvs_series, mid_series, i)
        cross_below_mid = crossunder(dvs_series, mid_series, i)

        if params.mode == "mode_a":
            entry_cond = cross_above_mid
            exit_cond = cross_below_mid
        elif params.mode == "mode_b":
            # Reclaim through 40, exit at 50 crossunder
            cross_above_40 = crossover(dvs_series, mode_b_thr_series, i)
            entry_cond = cross_above_40
            exit_cond = cross_below_mid
        else:
            entry_cond = cross_above_mid
            exit_cond = cross_below_mid

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
