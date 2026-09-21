"""wilder-volatility-system-flip — Wilder Volatility System ARC SAR close flip.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage22 SOL under-gate after majors — need published ATR stop-and-reverse
  that can flip with SOL impulse without cloning SuperTrend/Chandelier burns or stage22 channel.
  Wilder Volatility System (New Concepts 1978 pp.23-26):
  atr = ta.atr(n)
  arc = factor * atr
  sarLong = ta.highest(close, n) - arc
  sarShort = ta.lowest(close, n) + arc
  Mode A:
    long crossover(close, sarShort) from flat
    exit crossunder(close, sarLong)
    Long-only first (no forced always-in).
  Mode B:
    require ATR percentrank > thr — only if Mode A over-whips; identical all four.
  Prefer (7, 3.0) Mode A; density alt (9, 2.0) identical-all-four if needed.
  != SuperTrend (HL2 ratchet) / != Chandelier (HH - ATR) / != PSAR.

btc_smoke:
  Kill Mode A BTC 0/chop; Kill n/factor inflate until n collapses;
  Kill SuperTrend/Chandelier/PSAR labeled Wilder VS. Prefer Mode A (7,3.0) or (9,2.0) identical, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill n/factor retuned only on ETH. Prefer identical.

sol_smoke:
  CRITICAL: Kill BTC+ETH clear then SOL under 1.2x; Kill n/factor retuned only on SOL;
  SuperTrend/Chandelier graft; 15m n=3; stage12-22 grafts.
  Prefer denser n >> 9. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill n/factor retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: SuperTrend/Chandelier/PSAR labeled Wilder VS; vol-expansion x dir graft;
request.security; stage12-22 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, percentrank, wilder_volatility_system

STRATEGY_ID = "wilder-volatility-system-flip"


@dataclass(frozen=True)
class WilderVsParams:
    mode: str = "mode_a"    # "mode_a" | "mode_b"
    n: int = 7              # 7, 9
    factor: float = 3.0     # 2.0, 3.0
    atr_pr_len: int = 50
    atr_pr_thr: float = 50.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: WilderVsParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {7, 9}:
        return False, f"btc_smoke: n={params.n} not in locked sweep {{7, 9}}"
    if params.factor not in {2.0, 3.0}:
        return False, f"btc_smoke: factor={params.factor} not in locked sweep {{2.0, 3.0}}"
    if params.n > 20 or params.factor > 5.0:
        return False, "btc_smoke: n/factor inflate until BTC n collapses"
    return True, "PASS"


def validate_eth_smoke(params: WilderVsParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.n not in {7, 9} or params.factor not in {2.0, 3.0}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: WilderVsParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH PRIMARY CRITICAL)."""
    if tf == "15m" and params.n <= 3:
        return False, "sol_smoke: 15m n<=3 forbidden (spam)"
    if params.n not in {7, 9} or params.factor not in {2.0, 3.0}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: WilderVsParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.n not in {7, 9} or params.factor not in {2.0, 3.0}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: WilderVsParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for wilder-volatility-system-flip."""
    params = params or WilderVsParams()
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
    sar_long, sar_short = wilder_volatility_system(
        closes, highs, lows, n=params.n, factor=params.factor
    )

    atr_pr: list[float | None] = [None] * n
    if params.mode == "mode_b":
        atr_pr = percentrank(atr_vals, params.atr_pr_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        s_short_cur = sar_short[i]
        s_short_prev = sar_short[i - 1]
        s_long_cur = sar_long[i]
        s_long_prev = sar_long[i - 1]

        if not in_pos:
            # crossover(close, sarShort) from flat
            if s_short_cur is not None and s_short_prev is not None:
                cross_short = (cp <= s_short_prev) and (c > s_short_cur)
                if cross_short:
                    can_enter = True
                    if params.mode == "mode_b":
                        pr = atr_pr[i]
                        if pr is None or pr <= params.atr_pr_thr:
                            can_enter = False
                    if can_enter:
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

            # exit crossunder(close, sarLong)
            cross_exit = False
            if s_long_cur is not None and s_long_prev is not None:
                cross_exit = (cp >= s_long_prev) and (c < s_long_cur)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
