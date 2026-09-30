"""ehlers-gaussian-fast-slow-cross-v1 — Ehlers N-pole Gaussian Filter fast × slow dual-line cross.

LOCKED ENCODE ORDER #4 (BNB-SURVIVAL-CRITICAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage5 parked SuperSmoother; stage10 wiped DEMA; dual-mom/EMA burned. Ehlers Gaussian Filter is
  cascaded-pole lowpass with alpha from Gaussian beta(omega, N) — != SuperSmoother Butterworth
  coefficients, != DEMA, != plain EMA dual-mom, != NetLead.
  Fast x slow Gaussian (fixed poles) is dense on 1H; close-only -> BNB-portable identical (Pf, Ps, poles).
  BNB-survival-CRITICAL: multipole Gaussian damps high-freq quieter-BNB noise better than 1-pole EMA duals
  that historically wiped.

Formula:
  w = 2 * pi / P
  beta = (1 - cos(w)) / (1.414^(2/N) - 1)
  alpha = -beta + sqrt(beta^2 + 2*beta)
  2-pole recurrence:
    f = alpha^2 * price + 2*(1-alpha)*f[1] - (1-alpha)^2 * f[2]
  4-pole recurrence: binomial expansion.
  fast = gauss(close, Pf, N); slow = gauss(close, Ps, N)
  Defaults: Pf=10, Ps=30, N=2.

Mode A:
  long: crossover(fast, slow)
  exit: crossunder(fast, slow) or ATR stop.

Mode B (BNB quiet):
  N=4 same periods — if Mode A over-whips; identical N+periods across coins.
  long: crossover(fast, slow)
  exit: crossunder(fast, slow) or ATR stop.

sol_smoke:
  Kill if: SuperSmoother/EMA dual labeled Gaussian; 15m Pf=3 spam; ER/AO/PGO graft.
  Prefer Mode A (10, 30, N=2), 1H+.
  Retention check: after ETH, SOL n must not collapse to PGO-class single digits.

bnb_smoke:
  BNB-after-SOL kill (CRITICAL): different (Pf, Ps, N) than SOL; Mode B shorts ungated; no ATR;
  per-coin pole retune. Prefer identical params; long-only; ATR exit.
  Kill if BNB needs N=4 while SOL only survives N=2.

Forbidden: SuperSmoother/DEMA/EMA-dual-mom/NetLead/HMA substitute; ER-gate; AO/ROC/WMA/PGO;
Pee TDI/TrendScore/GMMA/VQI; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_gaussian_filter

STRATEGY_ID = "ehlers-gaussian-fast-slow-cross-v1"


@dataclass(frozen=True)
class EhlersGaussianParams:
    mode: str = "mode_a"  # "mode_a" (N=2) | "mode_b" (N=4)
    period_fast: int = 10
    period_slow: int = 30
    poles: int = 2
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: EhlersGaussianParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period_fast <= 3:
        return False, "sol_smoke: 15m Pf<=3 forbidden (spam)"
    if (params.period_fast, params.period_slow) not in {(10, 30), (8, 24), (12, 40)}:
        return False, f"sol_smoke: (Pf,Ps)=({params.period_fast},{params.period_slow}) not in locked set"
    if params.poles not in (2, 4):
        return False, f"sol_smoke: poles={params.poles} not in {{2, 4}}"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersGaussianParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after SOL)."""
    if params.period_fast <= 0 or params.period_slow <= 0:
        return False, "bnb_smoke: periods must be > 0"
    if params.period_fast >= params.period_slow:
        return False, "bnb_smoke: period_fast must be < period_slow"
    if params.poles not in (2, 4):
        return False, "bnb_smoke: poles must be 2 or 4"
    if params.period_slow > 100:
        return False, "bnb_smoke: period_slow too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersGaussianParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-gaussian-fast-slow-cross-v1."""
    params = params or EhlersGaussianParams()
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
    fast = ehlers_gaussian_filter(closes, period=params.period_fast, poles=params.poles)
    slow = ehlers_gaussian_filter(closes, period=params.period_slow, poles=params.poles)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(fast, slow, i)
        cross_dn = crossunder(fast, slow, i)

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
