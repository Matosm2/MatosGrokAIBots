"""swenlin-pmo-signal-cross-v1 — Swenlin DecisionPoint PMO × signal-line cross.

LOCKED ENCODE ORDER #5 (OPTIONAL 5th — BNB-SURVIVAL-CRITICAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage8 burned ROC zero-cross primary; dual-mom/MACD adjacency skipped prior cycles.
  Swenlin PMO is 1-bar %ROC double-smoothed with custom alpha=2/period (not 2/(period+1))
  then EMA signal — encode class is PMO x signal, != raw ROC zero, != MACD (EMA - EMA),
  != AO median. Double custom-smooth + signal is intentionally quieter than ROC-zero —
  BNB-survival-CRITICAL seat if briefs 1-4 need a portable momentum dual-line.
  Close-only -> identical (s1, s2, sigLen).

Formula:
  roc1 = (close / close[1] - 1.0) * 100.0
  customSmooth(x, L): prior + (x - prior) * (2.0 / L)
  sm1 = customSmooth(roc1, s1)
  pmo = customSmooth(10.0 * sm1, s2)
  sig = ema(pmo, sigLen)
  Defaults: s1=35, s2=20, sigLen=10.

Mode A:
  long: crossover(pmo, sig)
  exit: crossunder(pmo, sig) or ATR stop.

Mode B (BNB quiet):
  long: crossover(pmo, sig) and pmo > 0
  exit: crossunder(pmo, sig) or ATR stop.
  (identical Mode across coins).

sol_smoke:
  Kill if: ROC-zero labeled PMO; MACD formula used; 15m s1=5 spam; ER/AO/PGO graft.
  Prefer Mode A (35, 20, 10), 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class.

bnb_smoke:
  BNB-after-SOL kill (CRITICAL): different (s1, s2, sigLen) than SOL; Mode B only on BNB;
  no ATR; per-coin retune. Prefer identical params; long-only; ATR exit.
  Kill if BNB needs longer s1 than SOL.

Forbidden: raw ROC zero primary; MACD/APO/PPO substitute; AO; WMA dual; ER-gate;
Pee TDI/TrendScore/GMMA/VQI; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, swenlin_pmo

STRATEGY_ID = "swenlin-pmo-signal-cross-v1"


@dataclass(frozen=True)
class SwenlinPmoParams:
    mode: str = "mode_a"  # "mode_a" (pmo cross sig) | "mode_b" (pmo cross sig and pmo > 0)
    s1: int = 35
    s2: int = 20
    sig_len: int = 10
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: SwenlinPmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.s1 <= 5:
        return False, "sol_smoke: 15m s1<=5 forbidden (spam)"
    if (params.s1, params.s2, params.sig_len) not in {
        (35, 20, 10),
        (25, 20, 10),
        (35, 15, 10),
        (35, 20, 8),
    }:
        return False, f"sol_smoke: (s1,s2,sigLen)=({params.s1},{params.s2},{params.sig_len}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: SwenlinPmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after SOL)."""
    if params.s1 <= 0 or params.s2 <= 0 or params.sig_len <= 0:
        return False, "bnb_smoke: lengths must be > 0"
    if params.s1 > 100 or params.s2 > 100 or params.sig_len > 50:
        return False, "bnb_smoke: lengths too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: SwenlinPmoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for swenlin-pmo-signal-cross-v1."""
    params = params or SwenlinPmoParams()
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
    pmo, sig = swenlin_pmo(
        closes,
        s1=params.s1,
        s2=params.s2,
        sig_len=params.sig_len,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]
        curr_pmo = pmo[i]

        cross_up = crossover(pmo, sig, i)
        cross_dn = crossunder(pmo, sig, i)

        if not in_pos:
            entry_cond = cross_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_pmo is not None and curr_pmo > 0.0)

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
