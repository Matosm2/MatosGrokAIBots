"""mobius-tmo-main-zero-v1 — Mobius True Momentum Oscillator Main-line zero-cross.

LOCKED ENCODE ORDER #3 (BTC-CLEARING PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage8 burned ROC/AO; stage12 wiped PMO×signal. Mobius TMO builds a discrete vote =
  sum(sign(close vs open[i])) over Length, then light double-EMA -> Main.
  Encode class is Main zero-cross, != raw ROC, != AO median SMA, != PSY up-close share midline-50,
  != PMO×signal dual-line. Light calcLength=5 / smoothLength=3 keeps BTC responsive (anti-stage12 over-smooth).
  Close+open OHLC -> identical (length, calc, smooth) on SOL+BNB.
  Do NOT use Main×Signal as Mode A (PMO-class EXIT).

Formula:
  vote = sum(close > open[i] ? 1 : close < open[i] ? -1 : 0) over length
  ema1 = ema(vote, calcLength)
  main = ema(ema1, smoothLength)
  Prefer (14, 5, 3).

Mode A (BTC-PRIMARY):
  long: crossover(main, 0)
  exit: crossunder(main, 0) or ATR stop.

Mode B (BNB quiet):
  long: crossover(main, 0) and main > 0
  exit: crossunder(main, 0) or main < 0 or ATR stop.
  (identical params across coins). Not Main×Signal.

btc_smoke:
  BTC-LEAD CRITICAL: Kill if smooth/calc raised into stage12-damp territory until BTC n collapses;
  Kill if Mode A becomes Main×Signal (PMO EXIT clone); Kill if HTF security agg. Prefer Mode A (14,5,3), 1H+.

sol_smoke:
  Kill if: ROC/AO/PMO labeled TMO; 15m length=3 spam; ER/stage12 graft. Retention check: after ETH, SOL n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+SOL: different (length,calc,smooth) than SOL; Main×Signal only on BNB; no ATR; volume graft.
  Prefer identical params; long-only; ATR exit.

Forbidden: ROC/AO/PSY/PMO×signal labeled TMO; HTF request.security; stage12 duals; ER-gate.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, mobius_tmo

STRATEGY_ID = "mobius-tmo-main-zero-v1"


@dataclass(frozen=True)
class MobiusTmoParams:
    mode: str = "mode_a"  # "mode_a" (main cross 0) | "mode_b" (main cross 0 and main > 0)
    length: int = 14
    calc_length: int = 5
    smooth_length: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: MobiusTmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.calc_length > 10 or params.smooth_length > 10:
        return False, "btc_smoke: calc/smooth length too large (stage12 over-smooth damp)"
    if params.length not in {10, 14, 21}:
        return False, f"btc_smoke: length={params.length} not in locked set {{10, 14, 21}}"
    return True, "PASS"


def validate_sol_smoke(params: MobiusTmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 3:
        return False, "sol_smoke: 15m length<=3 forbidden (spam)"
    if params.length not in {10, 14, 21}:
        return False, f"sol_smoke: length={params.length} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: MobiusTmoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+SOL)."""
    if params.length <= 0 or params.calc_length <= 0 or params.smooth_length <= 0:
        return False, "bnb_smoke: lengths must be > 0"
    if params.length > 50:
        return False, "bnb_smoke: length too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: MobiusTmoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for mobius-tmo-main-zero-v1."""
    params = params or MobiusTmoParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    main_series, _ = mobius_tmo(
        opens,
        closes,
        length=params.length,
        calc_length=params.calc_length,
        smooth_length=params.smooth_length,
    )

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        curr_main = main_series[i]
        cross_up = crossover(main_series, zero_line, i)
        cross_dn = crossunder(main_series, zero_line, i)

        if not in_pos:
            entry_cond = cross_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_main is not None and curr_main > 0.0)

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

            exit_cond = cross_dn
            if params.mode == "mode_b":
                exit_cond = exit_cond or (curr_main is not None and curr_main < 0.0)

            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
