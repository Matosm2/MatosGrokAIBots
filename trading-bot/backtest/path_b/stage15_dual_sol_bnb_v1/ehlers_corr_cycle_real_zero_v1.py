"""ehlers-corr-cycle-real-zero — Ehlers Correlation Cycle Real zero-cross.

LOCKED ENCODE ORDER #3 (BNB-SURVIVAL CRITICAL + CORRELATION CYCLE REAL-ZERO).
Thesis:
  Stage5 burned CTI (Pearson price x ramp threshold dual).
  Ehlers Correlation Cycle (TASC Jun 2020) correlates price with cosine (Real) and -sine (Imag) basis functions —
  Mode A locks Real zero-cross for dense BTC/ETH trade count;
  Mode B optionally requires state != 0 (angle-stable trend regime, threshold=9 deg) to damp quieter BNB cycle chatter —
  identical (period, threshold) across all coins.
  != CTI, != Cyber Cycle, != Roofing/SS.

Formula:
  Real = Pearson corr(close[0..P-1], cos(2*pi*i / P))
  Imag = Pearson corr(close[0..P-1], -sin(2*pi*i / P))
  Angle = atan2(-Imag, Real) in degrees
  dAngle = Angle[t] - Angle[t-1] (wrapped to [-180, 180])
  state = +1 if abs(dAngle) < Threshold and Real > 0 else (-1 if abs(dAngle) < Threshold and Real < 0 else 0)
  Prefer period=20, threshold=9.

Mode A (BTC->ETH-PRIMARY dense zero — prefer first):
  long: crossover(real, 0)
  exit: crossunder(real, 0) or ATR stop.

Mode B (BNB-quiet / state trend-gate):
  long: crossover(real, 0) and state != 0 (or state == +1)
  exit: crossunder(real, 0) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if period/threshold inflate until Real n collapses; Kill if Mode B forced while Mode A BTC healthy; Kill CTI/SS graft.
  Prefer Mode A period=20, 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears >=1.2x then ETH wipes; Kill period/threshold retuned only on ETH; Kill CTI dual-thr substitute.
  Prefer identical (20, 9) on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if CTI/CyberCycle/Roofing labeled CCY-Real; 15m period=5 spam; stage12-14.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (period, threshold); Mode B shorts ungated; Mode B only on BNB; no ATR.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs params != SOL.

Forbidden: CTI ramp; CyberCycle/Roofing/SS; TTF/PFE/ASH/APZ/Nadaraya; Imag-only as Mode A first-pass; stage12-13; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_corr_cycle

STRATEGY_ID = "ehlers-corr-cycle-real-zero"


@dataclass(frozen=True)
class CorrCycleParams:
    mode: str = "mode_a"  # "mode_a" (real cross 0) | "mode_b" (real cross 0 and state != 0)
    period: int = 20
    threshold: float = 9.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: CorrCycleParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period > 35:
        return False, f"btc_smoke: period={params.period} > 35 collapses BTC n"
    if params.period not in {14, 20, 28}:
        return False, f"btc_smoke: period={params.period} not in locked set {{14, 20, 28}}"
    if params.threshold not in {6.0, 9.0, 12.0}:
        return False, f"btc_smoke: threshold={params.threshold} not in locked set {{6, 9, 12}}"
    return True, "PASS"


def validate_eth_smoke(params: CorrCycleParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.period not in {14, 20, 28} or params.threshold not in {6.0, 9.0, 12.0}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: CorrCycleParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period <= 5:
        return False, "sol_smoke: 15m period<=5 forbidden (spam)"
    if params.period not in {14, 20, 28} or params.threshold not in {6.0, 9.0, 12.0}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: CorrCycleParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.period <= 0 or params.threshold <= 0.0:
        return False, "bnb_smoke: invalid parameters"
    if params.period > 35:
        return False, "bnb_smoke: period too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: CorrCycleParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-corr-cycle-real-zero."""
    params = params or CorrCycleParams()
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
    real, _, _, state = ehlers_corr_cycle(closes, period=params.period, threshold=params.threshold)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(real, zero_line, i)
        cross_dn = crossunder(real, zero_line, i)

        if params.mode == "mode_b":
            # Mode B: require state != 0 (trend mode)
            entry_cond = cross_up and (state[i] != 0)
        else:
            entry_cond = cross_up

        if not in_pos:
            if entry_cond:
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
