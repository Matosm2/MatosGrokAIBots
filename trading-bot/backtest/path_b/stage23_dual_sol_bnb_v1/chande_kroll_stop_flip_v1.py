"""chande-kroll-stop-flip — Chande Kroll Stop two-stage ATR corridor flip.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage22 SOL 0.922x after BTC->ETH — need second published ATR-stop family
  distinct from Wilder VS / SuperTrend / Chandelier for SOL-portable flips with
  denser corridor participation.
  Chande Kroll Stop:
    highStop = highest(high, p) - x * atr(p)
    lowStop = lowest(low, p) + x * atr(p)
    stopShort = highest(highStop, q)
    stopLong = lowest(lowStop, q)
  Mode A:
    long crossover(close, stopShort)
    exit crossunder(close, stopLong)
  Mode B:
    require (stopShort - stopLong) percentrank > wMin — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (10, 1.0, 9) Mode A.
  != Chandelier (single HH - ATR) / != SuperTrend (HL2 ratchet) / != Wilder VS.

btc_smoke:
  Kill Mode A BTC 0/chop; Kill p/x/q inflate until n collapses;
  Kill Chandelier/SuperTrend/Wilder-VS labeled Chande Kroll. Prefer Mode A (10,1.0,9), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  CRITICAL: Kill BTC+ETH clear then SOL under 1.2x; Kill p/x/q retuned only on SOL;
  Chandelier graft; 15m p=3; stage12-22 grafts.
  Prefer denser n >> 9. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill p/x/q retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: Chandelier/SuperTrend/Wilder-VS/PSAR labeled Chande Kroll;
request.security; stage12-22 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, percentrank, chande_kroll_stop

STRATEGY_ID = "chande-kroll-stop-flip"


@dataclass(frozen=True)
class ChandeKrollParams:
    mode: str = "mode_a"    # "mode_a" | "mode_b"
    p: int = 10             # 10, 14
    x: float = 1.0          # 1.0, 1.5
    q: int = 9              # 9, 14
    w_len: int = 50
    w_min: float = 50.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ChandeKrollParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.p not in {10, 14}:
        return False, f"btc_smoke: p={params.p} not in locked sweep {{10, 14}}"
    if params.x not in {1.0, 1.5}:
        return False, f"btc_smoke: x={params.x} not in locked sweep {{1.0, 1.5}}"
    if params.q not in {9, 14}:
        return False, f"btc_smoke: q={params.q} not in locked sweep {{9, 14}}"
    if params.p > 30 or params.q > 30:
        return False, "btc_smoke: p/q inflate until BTC n collapses"
    return True, "PASS"


def validate_eth_smoke(params: ChandeKrollParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.p not in {10, 14} or params.x not in {1.0, 1.5} or params.q not in {9, 14}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ChandeKrollParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH PRIMARY CRITICAL)."""
    if tf == "15m" and params.p <= 3:
        return False, "sol_smoke: 15m p<=3 forbidden (spam)"
    if params.p not in {10, 14} or params.x not in {1.0, 1.5} or params.q not in {9, 14}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ChandeKrollParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.p not in {10, 14} or params.x not in {1.0, 1.5} or params.q not in {9, 14}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ChandeKrollParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for chande-kroll-stop-flip."""
    params = params or ChandeKrollParams()
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
    stop_short, stop_long = chande_kroll_stop(
        highs, lows, closes, p=params.p, x=params.x, q=params.q
    )

    width_pr: list[float | None] = [None] * n
    if params.mode == "mode_b":
        widths: list[float | None] = [None] * n
        for i in range(n):
            ss = stop_short[i]
            sl = stop_long[i]
            if ss is not None and sl is not None:
                widths[i] = ss - sl
        width_pr = percentrank(widths, params.w_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        ss_cur = stop_short[i]
        ss_prev = stop_short[i - 1]
        sl_cur = stop_long[i]
        sl_prev = stop_long[i - 1]

        if not in_pos:
            # crossover(close, stopShort)
            if ss_cur is not None and ss_prev is not None:
                breakout = (cp <= ss_prev) and (c > ss_cur)
                if breakout:
                    can_enter = True
                    if params.mode == "mode_b":
                        wpr = width_pr[i]
                        if wpr is None or wpr <= params.w_min:
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

            # exit crossunder(close, stopLong)
            cross_exit = False
            if sl_cur is not None and sl_prev is not None:
                cross_exit = (cp >= sl_prev) and (c < sl_cur)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
