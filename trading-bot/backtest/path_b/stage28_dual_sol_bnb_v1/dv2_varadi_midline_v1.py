"""dv2-varadi-midline — Varadi DV2 percent-rank midline reclaim.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage15 seated DVI then EXIT 0-BTC; stage15 reject deferred DV2 mean-reversion.
  DV2 is distinct: percent-rank of average of today/yesterday Close/(High+Low) (CSS Analytics).
  Trend-port mid-reclaim — not classic DV2<10 fade.
  r = close / (high + low)
  dv_raw = (r + r[1]) / 2
  dv2 = 100 * percentrank(dv_raw, rankLen)
  Mode A:
    long crossover(dv2, 50)
    exit crossunder(dv2, 50)
  Mode B:
    reclaim through 40 exit at 50 — only if Mode A under-fires;
    identical params across all four coins (still not fade-short primary).
  Prefer rankLen=100, mid=50 Mode A.
  != DVI (magnitude+stretch) / != RSI2 / != PSY / != IMI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill rankLen inflate/spam; Kill DVI/RSI2/PSY labeled DV2; Kill Mode B fade-shorts forced.
  Prefer Mode A rankLen=100 mid-50, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill rankLen retuned only on SOL;
  stage12-27 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR.

Forbidden: DVI magnitude+stretch / RSI2 / PSY / IMI labeled DV2; SMA200 graft;
stage12-27 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, dv2_varadi

STRATEGY_ID = "dv2-varadi-midline"


@dataclass(frozen=True)
class Dv2VaradiParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    rank_len: int = 100           # 63, 100, 126, 252
    mid: float = 50.0             # 50.0
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: Dv2VaradiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.rank_len not in {63, 100, 126, 252}:
        return False, f"btc_smoke: rank_len={params.rank_len} not in {{63, 100, 126, 252}}"
    return True, "PASS"


def validate_eth_smoke(params: Dv2VaradiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.rank_len not in {63, 100, 126, 252}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: Dv2VaradiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.rank_len not in {63, 100, 126, 252}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: Dv2VaradiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.rank_len not in {63, 100, 126, 252}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: Dv2VaradiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for dv2-varadi-midline."""
    params = params or Dv2VaradiParams()
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
    dv2_vals, _ = dv2_varadi(highs, lows, closes, params.rank_len)

    mid_vals: list[float | None] = [params.mid] * count
    mid40_vals: list[float | None] = [40.0] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        crossover_mid = crossover(dv2_vals, mid_vals, i)
        crossunder_mid = crossunder(dv2_vals, mid_vals, i)

        if params.mode == "mode_a":
            entry_cond = crossover_mid
            exit_cond = crossunder_mid
        elif params.mode == "mode_b":
            # Reclaim through 40, exit at 50 crossunder
            crossover_40 = crossover(dv2_vals, mid40_vals, i)
            entry_cond = crossover_40
            exit_cond = crossunder_mid
        else:
            entry_cond = crossover_mid
            exit_cond = crossunder_mid

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
