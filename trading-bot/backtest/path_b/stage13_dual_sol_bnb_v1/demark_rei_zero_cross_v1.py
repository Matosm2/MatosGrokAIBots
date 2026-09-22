"""demark-rei-zero-cross-v1 — DeMark Range Expansion Index zero-cross (Mode A) / ±60 reclaim (Mode B).

LOCKED ENCODE ORDER #1 (BTC-CLEARING PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage12 wiped CSI/EDCF/US/Gaussian/PMO (0 BTC). TD REI is an arithmetic OHLC range-expansion
  oscillator (-100..+100) with DeMark overlap conditions — != EMA dual-smoother, != FIR-lag,
  != CSI body/range triple-EMA, != ROC, != CMO, != midline-50 intensity.
  Mode A locks REI zero-cross for BTC-clearing density (responsive polarity of strong H/L expansion);
  Mode B = classic DeMark ±60 reclaim only if Mode A over-whips quieter BNB — identical period across coins.

Formula:
  s = (high - high[2]) + (low - low[2])
  v = 1 if ((high[t-2] >= close[t-7] or high[t-2] >= close[t-8] or high[t] >= close[t-5] or high[t] >= close[t-6]) and
           (low[t-2] <= close[t-7] or low[t-2] <= close[t-8] or low[t] <= close[t-5] or low[t] <= close[t-6])) else 0
  num = sum(v * s, L)
  den = sum(abs(high - high[2]) + abs(low - low[2]), L)
  rei = den != 0 ? 100 * num / den : 0
  Prefer L=8.

Mode A (BTC-PRIMARY dense zero — prefer first):
  long: crossover(rei, 0)
  exit: crossunder(rei, 0) or ATR stop.

Mode B (BNB-quiet / DeMark classic ±60 reclaim):
  long: crossover(rei, -60)
  exit: crossunder(rei, 60) or ATR stop.
  (identical L across coins).

btc_smoke:
  Kill if CSI/PMO/Gaussian/US damp grafted; Kill if L >> 13 collapses BTC n; Kill if Mode B forced while Mode A BTC n healthy.
  Prefer Mode A L=8, 1H+.

sol_smoke:
  Kill if: RSI/CMO/ROC/DeMarker labeled REI; 15m L=3 spam; ER/AO/PGO/stage12 graft.
  Prefer Mode A L=8, 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+SOL: different L than SOL; Mode B shorts ungated; no ATR; volume graft.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs L != SOL.

Forbidden: RSI/CMO/ROC/CSI/PMO; ADX; ER-gate; AO/WMA/PGO; stage12 smoother duals; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, demark_rei

STRATEGY_ID = "demark-rei-zero-cross-v1"


@dataclass(frozen=True)
class DemarkReiParams:
    mode: str = "mode_a"  # "mode_a" (rei cross 0) | "mode_b" (rei cross -60, exit crossunder 60)
    length: int = 8
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: DemarkReiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length > 20:
        return False, f"btc_smoke: L={params.length} > 20 collapses BTC n"
    if params.length not in {5, 8, 13}:
        return False, f"btc_smoke: L={params.length} not in locked set {{5, 8, 13}}"
    return True, "PASS"


def validate_sol_smoke(params: DemarkReiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 3:
        return False, "sol_smoke: 15m L<=3 forbidden (spam)"
    if params.length not in {5, 8, 13}:
        return False, f"sol_smoke: L={params.length} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DemarkReiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+SOL)."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    if params.length > 20:
        return False, "bnb_smoke: length too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DemarkReiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for demark-rei-zero-cross-v1."""
    params = params or DemarkReiParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    rei = demark_rei(highs, lows, closes, length=params.length)

    # Threshold constants for crossover/crossunder
    zero_line = [0.0] * n
    neg60_line = [-60.0] * n
    pos60_line = [60.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_a":
            cross_up = crossover(rei, zero_line, i)
            cross_dn = crossunder(rei, zero_line, i)
        else:  # mode_b
            cross_up = crossover(rei, neg60_line, i)
            cross_dn = crossunder(rei, pos60_line, i)

        if not in_pos:
            if cross_up:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * float(atr_vals[i])
        else:
            highest_since_entry = max(highest_since_entry, h)
            stop_hit = False

            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                new_stop = highest_since_entry - params.atr_trail_mult * float(atr_vals[i])
                prev_stop = stops[i - 1]
                if prev_stop is not None and new_stop < prev_stop:
                    new_stop = prev_stop
                stops[i] = new_stop
                if lows[i] <= new_stop:
                    stop_hit = True

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
