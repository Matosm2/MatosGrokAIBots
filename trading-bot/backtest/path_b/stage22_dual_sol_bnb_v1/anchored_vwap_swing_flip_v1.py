"""anchored-vwap-swing-flip — Event-anchored VWAP from confirmed swing low close flip.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage21 0 BTC; session VWAP+-sigma burned.
  Need event-anchored fair-value reclaim that can clear BTC
  without HHLL multi-pivot BOS state as the signal.
  AVWAP from confirmed pivot low:
    pl = ta.pivotlow(low, L, R)
    on confirmed pl: reset cumTPV/cumV from anchor
    each bar: avwap = cumTPV / cumV with tp = hlc3
  Mode A:
    long crossover(close, avwap)
    exit crossunder(close, avwap)
    Signal is AVWAP cross, NOT HHLL state.
  Mode B:
    require bars-since-anchor >= minAge before signals — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (5, 5) Mode A, minAge=0.
  != session VWAP+-sigma / != HHLL-state / != VWMA x SMA.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill pivot inflate until n collapses;
  Kill session VWAP+-sigma / HHLL-state substitute. Prefer Mode A (5,5), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill pivots retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m L=1; stage12-21 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill pivots retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR.

Forbidden: session VWAP+-sigma labeled AVWAP; HHLL/BOS state as primary signal;
request.security; stage12-21 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import anchored_vwap_pivot_low, atr

STRATEGY_ID = "anchored-vwap-swing-flip"


@dataclass(frozen=True)
class AnchoredVwapParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    pivot_l: int = 5      # 5, 8
    pivot_r: int = 5      # 5, 8
    min_age: int = 0      # 0, 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: AnchoredVwapParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.pivot_l not in {5, 8} or params.pivot_r not in {5, 8}:
        return False, f"btc_smoke: pivots=({params.pivot_l},{params.pivot_r}) not in locked sweep {{5, 8}}"
    if params.min_age not in {0, 3}:
        return False, f"btc_smoke: min_age={params.min_age} not in locked sweep {{0, 3}}"
    if params.pivot_l > 15 or params.pivot_r > 15:
        return False, "btc_smoke: pivots collapse BTC n (over-damp)"
    return True, "PASS"


def validate_eth_smoke(params: AnchoredVwapParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.pivot_l not in {5, 8} or params.pivot_r not in {5, 8} or params.min_age not in {0, 3}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: AnchoredVwapParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and (params.pivot_l <= 1 or params.pivot_r <= 1):
        return False, "sol_smoke: 15m L<=1 forbidden (spam)"
    if params.pivot_l not in {5, 8} or params.pivot_r not in {5, 8} or params.min_age not in {0, 3}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: AnchoredVwapParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.pivot_l not in {5, 8} or params.pivot_r not in {5, 8} or params.min_age not in {0, 3}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: AnchoredVwapParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for anchored-vwap-swing-flip."""
    params = params or AnchoredVwapParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    avwap_vals, bars_since_anchor = anchored_vwap_pivot_low(
        highs, lows, closes, volumes, pivot_left=params.pivot_l, pivot_right=params.pivot_r
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        av_cur = avwap_vals[i]
        av_prev = avwap_vals[i - 1]
        age = bars_since_anchor[i]

        if not in_pos:
            # crossover(close, avwap)
            if av_cur is not None and av_prev is not None:
                cross_up = (cp <= av_prev) and (c > av_cur)
                if params.mode == "mode_b" or params.min_age > 0:
                    if age < params.min_age:
                        cross_up = False
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

            # exit crossunder(close, avwap)
            cross_down = False
            if av_cur is not None and av_prev is not None:
                cross_down = (cp >= av_prev) and (c < av_cur)

            exit_trigger = stop_hit or cross_down
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
