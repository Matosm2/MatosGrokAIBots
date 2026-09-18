"""tcf-plus-sign-flip-v1 — Trend Continuation Factor +TCF sign flip.

LOCKED ENCODE ORDER #4 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage8 wiped AO/ROC; ADX/DMI burned.
  Pee TCF builds recursive continuation factors from 1-bar changes then sums
  (+Change - -CF) / (-Change - +CF) over N — directional continuation polarity.
  != ADX/DMI, != AO, != ROC.
  Mode A: long while +TCF > 0 (enter on crossover 0); dense sign flips on 1H.
  Identical N on SOL+BNB.

Formula:
  Change = close - close[1]
  plusChange = max(Change, 0)
  minusChange = max(-Change, 0)
  plusCF = plusChange == 0 ? 0 : plusChange + plusCF[1]
  minusCF = minusChange == 0 ? 0 : minusChange + minusCF[1]
  plusTCF = sum(plusChange - minusCF, N)
  minusTCF = sum(minusChange - plusCF, N)
  N in {20, 25, 35}; prefer 35.

Mode A (primary / dense +TCF zero flip):
  long: ta.crossover(plusTCF, 0)
  exit: ta.crossunder(plusTCF, 0) or when minusTCF > 0 or ATR stop.

Mode B (secondary cross form):
  long: ta.crossover(plusTCF, minusTCF) and plusTCF > 0
  exit: ta.crossunder(plusTCF, minusTCF) or ATR stop.

sol_smoke:
  Kill if: ADX labeled TCF; AO/ROC substitute; 15m N=5 spam; ER/PGO graft.
  Prefer Mode A N=35, 1H+.
  Retention check: after ETH, if SOL n collapses, try N=25 same Mode A before kill.

bnb_smoke:
  Kill if: different N than SOL; Mode B shorts ungated; no ATR.
  Prefer identical N; long-only; ATR exit.

Forbidden: ADX/DMI; AO/ROC/WMA/PGO; ER-gate; PSY/RMI/Disparity/WT; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, trend_continuation_factor

STRATEGY_ID = "tcf-plus-sign-flip-v1"


@dataclass(frozen=True)
class TcfSignFlipParams:
    mode: str = "mode_a"  # "mode_a" (cross > 0) | "mode_b" (cross > minusTCF and plusTCF > 0)
    length: int = 35
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: TcfSignFlipParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m N<=5 forbidden (spam)"
    if params.length not in {20, 25, 35}:
        return False, f"sol_smoke: N={params.length} not in locked set {{20, 25, 35}}"
    return True, "PASS"


def validate_bnb_smoke(params: TcfSignFlipParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: TcfSignFlipParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for tcf-plus-sign-flip-v1."""
    params = params or TcfSignFlipParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    plus_tcf, minus_tcf = trend_continuation_factor(closes, length=params.length)

    zeros: list[float | None] = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

        # Update trailing stop if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False
            if params.mode == "mode_a":
                # Exit on crossunder 0 or when minusTCF > 0
                if crossunder(plus_tcf, zeros, i):
                    exit_signal = True
                elif minus_tcf[i] is not None and minus_tcf[i] > 0.0:
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit on crossunder(plusTCF, minusTCF)
                if crossunder(plus_tcf, minus_tcf, i):
                    exit_signal = True

            # Stop hit check
            if stop_level is not None and c < stop_level:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0
                stop_level = None
                continue

        # Check entries if flat
        if not in_pos and i > 0:
            enter_signal = False
            if params.mode == "mode_a":
                # Mode A: crossover(plusTCF, 0)
                if crossover(plus_tcf, zeros, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(plusTCF, minusTCF) and plusTCF > 0
                if crossover(plus_tcf, minus_tcf, i):
                    pt = plus_tcf[i]
                    if pt is not None and pt > 0.0:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
