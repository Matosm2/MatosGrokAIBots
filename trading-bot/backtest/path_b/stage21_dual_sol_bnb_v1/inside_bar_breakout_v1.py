"""inside-bar-breakout — Inside bar mother-bar high/low close breakout.

LOCKED ENCODE ORDER #5.
Thesis:
  Stage20 0 BTC. Need compression -> impulse structure that can clear BTC
  without HHLL multi-pivot BOS or long Donchian.
  Inside bar:
    inside = high < high[1] and low > low[1]
    On inside: arm motherH = high[1], motherL = low[1], armed = cancelBars
    Each bar if armed > 0: armed -= 1
  Mode A:
    long when armed > 0 and close > motherH and not (close[1] > motherH)
    exit close < motherL or arm expire / opposite bear break
    Clear arm after fill.
  Mode B:
    require mother range >= k * ta.atr(atrLen) (skip tiny mothers) — only if
    Mode A over-whips; identical params across all four coins.
  Prefer cancelBars=5 Mode A.
  != HHLL / != Donchian-long / != NR7 / != Heikin-Ashi.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill cancelBars/k tighten until n collapses;
  Kill HHLL/Donchian/NR7/HA substitute. Prefer Mode A cancelBars=5, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill cancelBars retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m cancelBars=1; stage12-20 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe / failed-break churn;
  Kill cancelBars/k retuned only on BNB; Mode B only on BNB.
  Prefer identical; long-only; ATR.

Forbidden: HHLL/pivot BOS labeled inside-break; Donchian(N>=20) labeled mother;
NR7 labeled inside; HA bias; request.security; stage12-20 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, inside_bar

STRATEGY_ID = "inside-bar-breakout"


@dataclass(frozen=True)
class InsideBarParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    cancel_bars: int = 5  # 3, 5, 8
    k: float = 0.0  # 0.0 (raw) or 0.5 (Mode B ATR filter)
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: InsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.cancel_bars not in {3, 5, 8}:
        return False, f"btc_smoke: cancel_bars={params.cancel_bars} not in locked sweep {{3, 5, 8}}"
    if params.k not in {0.0, 0.5}:
        return False, f"btc_smoke: k={params.k} not in locked sweep {{0.0, 0.5}}"
    if params.cancel_bars > 15:
        return False, f"btc_smoke: cancel_bars={params.cancel_bars} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: InsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.cancel_bars not in {3, 5, 8} or params.k not in {0.0, 0.5}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: InsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.cancel_bars <= 1:
        return False, "sol_smoke: 15m cancel_bars<=1 forbidden (spam)"
    if params.cancel_bars not in {3, 5, 8} or params.k not in {0.0, 0.5}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: InsideBarParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.cancel_bars not in {3, 5, 8} or params.k not in {0.0, 0.5}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: InsideBarParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for inside-bar-breakout."""
    params = params or InsideBarParams()
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
    insides = inside_bar(highs, lows)

    in_pos = False
    highest_since_entry = 0.0
    armed = 0
    mother_h = 0.0
    mother_l = 0.0

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        # Check inside bar to arm / rearm mother range
        if insides[i]:
            m_h = highs[i - 1]
            m_l = lows[i - 1]
            m_range = m_h - m_l
            qualifies = True
            if (params.mode == "mode_b" or params.k > 0.0) and atr_vals[i] is not None:
                qualifies = bool(m_range >= params.k * float(atr_vals[i]))
            if qualifies:
                mother_h = m_h
                mother_l = m_l
                armed = params.cancel_bars

        if not in_pos:
            # Entry condition: armed > 0 and close breaks above mother_h on rising edge
            breakout = (armed > 0) and (c > mother_h) and not (cp > mother_h)
            if breakout:
                buys[i] = True
                in_pos = True
                armed = 0  # Clear arm after fill
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * float(atr_vals[i])
            else:
                if armed > 0:
                    armed -= 1
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

            # Exit on close < mother_l (break failure) or ATR stop hit
            fail_exit = c < mother_l
            exit_trigger = stop_hit or fail_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
