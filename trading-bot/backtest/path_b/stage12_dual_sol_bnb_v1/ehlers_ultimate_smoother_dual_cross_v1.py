"""ehlers-ultimate-smoother-dual-cross-v1 — Ehlers Ultimate Smoother fast × slow dual-line cross.

LOCKED ENCODE ORDER #3 (BNB-SURVIVAL-CRITICAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage5 parked SuperSmoother dual; stage10 wiped DEMA; stage11 wiped NetLead×EMA.
  Ehlers Ultimate Smoother = AllPass - HighPass (zero lag in passband via cancellation) —
  != SuperSmoother Butterworth IIR, != DEMA, != NetLead, != ZLEMA.
  Fast x slow US cross is dense on 1H; close-only -> BNB-portable identical (Pf, Ps).
  BNB-survival-CRITICAL: dual US periods (not close x US) reduce quieter-BNB micro-whips
  vs raw price touches of a near-zero-lag smoother.

Formula:
  a1 = exp(-1.414 * pi / Period)
  c2 = 2 * a1 * cos(1.414 * pi / Period)
  c3 = -a1^2
  c1 = (1 + c2 - c3) / 4
  US = (1 - c1)*Price + (2*c1 - c2)*Price[1] - (c1 + c3)*Price[2] + c2*US[1] + c3*US[2]
  fast = US(close, Pf); slow = US(close, Ps)
  Defaults: Pf=10, Ps=30.

Mode A:
  long: crossover(fast, slow)
  exit: crossunder(fast, slow) or ATR stop.

Mode B (BNB quiet / quality):
  long: crossover(fast, slow) and close > slow
  exit: crossunder(fast, slow) or ATR stop.
  (identical Mode across coins).

sol_smoke:
  Kill if: SuperSmoother/DEMA/NetLead labeled US; 15m Pf=3 spam; ER/AO/PGO graft.
  Prefer Mode A (10, 30), 1H+.
  Retention check: after ETH, if SOL n huge with poor structure, try (12, 40) same Mode A
  before family fail (still identical params).

bnb_smoke:
  BNB-after-SOL kill (CRITICAL): different (Pf, Ps) than SOL; Mode B only on BNB; no ATR;
  per-coin period retune after SOL clear. Prefer identical params; long-only; ATR exit.
  Kill if BNB needs Ps >> SOL.

Forbidden: SuperSmoother/DEMA/NetLead/ZLEMA/HMA/TEMA substitute; ER-gate; AO/ROC/WMA/PGO;
Pee TDI/TrendScore/GMMA/VQI; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_ultimate_smoother

STRATEGY_ID = "ehlers-ultimate-smoother-dual-cross-v1"


@dataclass(frozen=True)
class EhlersUltimateSmootherParams:
    mode: str = "mode_a"  # "mode_a" (fast cross slow) | "mode_b" (fast cross slow and close > slow)
    period_fast: int = 10
    period_slow: int = 30
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: EhlersUltimateSmootherParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period_fast <= 3:
        return False, "sol_smoke: 15m Pf<=3 forbidden (spam)"
    if (params.period_fast, params.period_slow) not in {(10, 30), (8, 24), (12, 40)}:
        return False, f"sol_smoke: (Pf,Ps)=({params.period_fast},{params.period_slow}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersUltimateSmootherParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after SOL)."""
    if params.period_fast <= 0 or params.period_slow <= 0:
        return False, "bnb_smoke: periods must be > 0"
    if params.period_fast >= params.period_slow:
        return False, "bnb_smoke: period_fast must be < period_slow"
    if params.period_slow > 100:
        return False, "bnb_smoke: period_slow too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersUltimateSmootherParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-ultimate-smoother-dual-cross-v1."""
    params = params or EhlersUltimateSmootherParams()
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
    fast = ehlers_ultimate_smoother(closes, period=params.period_fast)
    slow = ehlers_ultimate_smoother(closes, period=params.period_slow)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]
        curr_slow = slow[i]

        cross_up = crossover(fast, slow, i)
        cross_dn = crossunder(fast, slow, i)

        if not in_pos:
            entry_cond = cross_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_slow is not None and c > curr_slow)

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
