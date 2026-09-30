"""arms-vama-dual-cross — Richard Arms Volume Adjusted Moving Average dual crossover.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage29 wipe + need published volume-aware impulse denser than DVS mid-reclaim
  without cloning stage3 VWMAxSMA, stage28 Vervoort dual-ZL TEMA, or EC cost-chop.
  VAMA (Richard W. Arms Jr.; Fidelity / NeuroShell):
    AvgVol = rolling SMA(volume, SampleN) (causal)
    VolInc = AvgVol * 0.67
    Arms walk-back VAMA(fast) and VAMA(slow) on close.
  Forbidden: ta.vwma labeled VAMA.
  Mode A:
    long crossover(vamaFast, vamaSlow)
    exit crossunder(vamaFast, vamaSlow)
  Mode B:
    require close > vamaSlow on entry — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (fast=8, slow=55, SampleN=100) Mode A.
  != VWMA / != Vervoort / != EC.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill lengths inflate until n collapses; Kill VWMA/Vervoort/EC labeled VAMA;
  Kill non-causal full-chart AvgVol. Prefer Mode A (8, 55, 100), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill VWMA labeled VAMA. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill fastLen retuned only on SOL;
  Kill 15m spam; stage12-29 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Kill Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: VWMA / Vervoort / EC labeled VAMA; Track-B four; stage12-29.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import arms_vama, atr, crossover, crossunder

STRATEGY_ID = "arms-vama-dual-cross"


@dataclass(frozen=True)
class ArmsVamaParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    fast_len: int = 8             # 5, 8, 13
    slow_len: int = 55            # 34, 55, 89
    sample_n: int = 100           # 50, 100, 200
    factor: float = 0.67          # 0.67
    trend_req: bool = False       # Mode B option: close > vamaSlow
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: ArmsVamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.fast_len not in {5, 8, 13}:
        return False, f"btc_smoke: fast_len={params.fast_len} not in {{5, 8, 13}}"
    if params.slow_len not in {34, 55, 89}:
        return False, f"btc_smoke: slow_len={params.slow_len} not in {{34, 55, 89}}"
    if params.sample_n not in {50, 100, 200}:
        return False, f"btc_smoke: sample_n={params.sample_n} not in {{50, 100, 200}}"
    return True, "PASS"


def validate_eth_smoke(params: ArmsVamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.fast_len not in {5, 8, 13} or params.slow_len not in {34, 55, 89} or params.sample_n not in {50, 100, 200}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ArmsVamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.fast_len not in {5, 8, 13} or params.slow_len not in {34, 55, 89} or params.sample_n not in {50, 100, 200}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ArmsVamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.fast_len not in {5, 8, 13} or params.slow_len not in {34, 55, 89} or params.sample_n not in {50, 100, 200}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ArmsVamaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for arms-vama-dual-cross."""
    params = params or ArmsVamaParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    vama_fast, vama_slow = arms_vama(
        closes=closes,
        volumes=volumes,
        fast_len=params.fast_len,
        slow_len=params.slow_len,
        sample_n=params.sample_n,
        factor=params.factor,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(vama_fast, vama_slow, i)
        cross_dn = crossunder(vama_fast, vama_slow, i)

        trend_ok = (
            vama_slow[i] is not None
            and closes[i] > vama_slow[i]
        )

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and (trend_ok if params.trend_req else True)
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
