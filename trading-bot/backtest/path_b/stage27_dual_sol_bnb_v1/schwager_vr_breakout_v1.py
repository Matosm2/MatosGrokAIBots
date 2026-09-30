"""schwager-vr-breakout — Jack Schwager Volatility Ratio + structure breakout.

LOCKED ENCODE ORDER #4.
Thesis:
  SWAP note: parent prompt's "volume ratio / up-down volume" misread of parked VR+breakout —
  scout-wave4 locked Jack Schwager Volatility Ratio + directional breakout
  (not Japanese up/down Volume Ratio).
  Stage26 FVE under-1.2x + stage21 naked vol-expansion x dir 0 BTC —
  need published VR > thr cap structure break distinct from continuous vol x dir EXIT.
  VR (Schwager / Incredible Charts / Wickra):
    tr = max(H-L, |H-C[1]|, |L-C[1]|)
    emaPrior = ema(tr[1], n) (current bar excluded from denom)
    vr = tr / emaPrior
    priorHigh = highest(high, M)[1]
    priorLow = lowest(low, M)[1]
  Mode A:
    long when vr > thr and crossover(close, priorHigh)
    exit crossunder(close, priorLow) or crossunder(close, sma(close, M))
  Mode B:
    require vr > thr confirmed on entry — only if Mode A over-whips;
    identical across all four.
  Prefer (n=14, thr=2.0, M=20) Mode A; if n thin try (14, 1.5, 10) identical all four.
  != Japanese Volume Ratio / != ATR-ratio x dir alone / != naked Donchian / != BB-squeeze.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill thr/M inflate until n <= 9 thin; Kill JP-VR / ATR-ratio x dir / naked Donchian substitute.
  Prefer Mode A (14, 2.0, 20) or (14, 1.5, 10), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill vol-expansion x dir labeled VR-breakout.
  Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill thr/M retuned only on SOL;
  15m M=3 spam; Donchian graft without VR; stage12-26 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill thr lowered only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: Japanese Volume Ratio; ATR-ratio x dir alone;
Chaikin/Parkinson x dir without structure; naked Donchian; BB-squeeze;
request.security; stage12-26 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, highest, lowest, schwager_volatility_ratio, sma

STRATEGY_ID = "schwager-vr-breakout"


@dataclass(frozen=True)
class SchwagerVrParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    n: int = 14                   # 10, 14, 20 (VR lookback)
    thr: float = 2.0              # 1.5, 2.0, 2.5
    m: int = 20                   # 10, 20 (structure lookback)
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: SchwagerVrParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {10, 14, 20}:
        return False, f"btc_smoke: n={params.n} not in {{10, 14, 20}}"
    if params.thr not in {1.5, 2.0, 2.5}:
        return False, f"btc_smoke: thr={params.thr} not in {{1.5, 2.0, 2.5}}"
    if params.m not in {10, 20}:
        return False, f"btc_smoke: m={params.m} not in {{10, 20}}"
    return True, "PASS"


def validate_eth_smoke(params: SchwagerVrParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.n not in {10, 14, 20} or params.thr not in {1.5, 2.0, 2.5} or params.m not in {10, 20}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: SchwagerVrParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {10, 14, 20} or params.thr not in {1.5, 2.0, 2.5} or params.m not in {10, 20}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: SchwagerVrParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.n not in {10, 14, 20} or params.thr not in {1.5, 2.0, 2.5} or params.m not in {10, 20}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: SchwagerVrParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for schwager-vr-breakout."""
    params = params or SchwagerVrParams()
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
    vr_vals, _ = schwager_volatility_ratio(highs, lows, closes, n=params.n)
    prior_highs = highest(highs, params.m)
    prior_lows = lowest(lows, params.m)
    sma_mid = sma(closes, params.m)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        vr_cur = vr_vals[i]
        c_cur = closes[i]
        c_prev = closes[i - 1]

        # Structure bounds shifted by 1 bar: highest(high, M)[1]
        ph_prev = prior_highs[i - 1]
        pl_prev = prior_lows[i - 1]
        m_cur = sma_mid[i]
        m_prev = sma_mid[i - 1]

        if vr_cur is None or ph_prev is None or pl_prev is None:
            continue

        crossover_high = c_prev <= ph_prev and c_cur > ph_prev
        crossunder_low = c_prev >= pl_prev and c_cur < pl_prev
        crossunder_sma = m_cur is not None and m_prev is not None and c_prev >= m_prev and c_cur < m_cur

        vr_pass = vr_cur > params.thr

        if params.mode == "mode_a":
            entry_cond = vr_pass and crossover_high
            exit_cond = crossunder_low or crossunder_sma
        elif params.mode == "mode_b":
            # Mode B: vr > thr and confirm bar condition
            vr_prev = vr_vals[i - 1]
            vr_confirm = vr_pass and (vr_prev is not None and vr_prev > params.thr)
            entry_cond = vr_confirm and crossover_high
            exit_cond = crossunder_low or crossunder_sma
        else:
            entry_cond = vr_pass and crossover_high
            exit_cond = crossunder_low or crossunder_sma

        # ATR trailing check
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
