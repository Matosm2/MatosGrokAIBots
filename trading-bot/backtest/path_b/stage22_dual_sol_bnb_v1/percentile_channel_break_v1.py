"""percentile-channel-break — Empirical percentile / quantile channel close break.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage21 vol-expansion x dir + bar-pattern = BTC PASS 0/32.
  Need impulse channel-break that can clear BTC >= 1.2x first
  without expansion x dir / candle-polarity / Ulcer.
  Percentile channel:
    up = ta.percentile_nearest_rank(high, len, pHi)
    dn = ta.percentile_nearest_rank(low, len, pLo)
  Mode A:
    long crossover(close, up)
    exit crossunder(close, dn)
  Mode B:
    require width percentrank(up - dn, wLen) > wMin — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (50, 90, 10) Mode A.
  != Donchian exact HH/LL / != HHLL / != BB / != Keltner / != STARC.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill len inflate until n collapses;
  Kill Donchian exact HH/LL / HHLL substitute. Prefer Mode A (50,90,10), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m len=10; stage12-21 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill len/pHi retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: Donchian(highest/lowest) labeled percentile; HHLL/pivot BOS labeled quantile;
BB/STARC/Keltner grafts; request.security; stage12-21 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, percentile_channel, percentrank

STRATEGY_ID = "percentile-channel-break"


@dataclass(frozen=True)
class PercentileChannelParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    length: int = 50       # 50, 70
    p_hi: float = 90.0     # 90.0, 95.0
    p_lo: float = 10.0     # 5.0, 10.0
    w_len: int = 200
    w_min: float = 50.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: PercentileChannelParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {50, 70}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{50, 70}}"
    if params.p_hi not in {90.0, 95.0}:
        return False, f"btc_smoke: p_hi={params.p_hi} not in locked sweep {{90.0, 95.0}}"
    if params.p_lo not in {5.0, 10.0}:
        return False, f"btc_smoke: p_lo={params.p_lo} not in locked sweep {{5.0, 10.0}}"
    if params.length > 100:
        return False, f"btc_smoke: length={params.length} collapses BTC n (over-damp)"
    return True, "PASS"


def validate_eth_smoke(params: PercentileChannelParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.length not in {50, 70} or params.p_hi not in {90.0, 95.0} or params.p_lo not in {5.0, 10.0}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: PercentileChannelParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.length <= 10:
        return False, "sol_smoke: 15m length<=10 forbidden (spam)"
    if params.length not in {50, 70} or params.p_hi not in {90.0, 95.0} or params.p_lo not in {5.0, 10.0}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: PercentileChannelParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.length not in {50, 70} or params.p_hi not in {90.0, 95.0} or params.p_lo not in {5.0, 10.0}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PercentileChannelParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for percentile-channel-break."""
    params = params or PercentileChannelParams()
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
    up_vals, dn_vals = percentile_channel(
        highs, lows, length=params.length, p_hi=params.p_hi, p_lo=params.p_lo
    )

    # Optional width percentrank for Mode B
    width_pr: list[float | None] = [None] * n
    if params.mode == "mode_b":
        widths: list[float | None] = [None] * n
        for i in range(n):
            u = up_vals[i]
            d = dn_vals[i]
            if u is not None and d is not None:
                widths[i] = u - d
        width_pr = percentrank(widths, params.w_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        up_cur = up_vals[i]
        up_prev = up_vals[i - 1]
        dn_cur = dn_vals[i]
        dn_prev = dn_vals[i - 1]

        if not in_pos:
            # crossover(close, up)
            if up_cur is not None and up_prev is not None:
                breakout = (cp <= up_prev) and (c > up_cur)
                if params.mode == "mode_b":
                    wpr = width_pr[i]
                    if wpr is None or wpr <= params.w_min:
                        breakout = False
                if breakout:
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

            # exit crossunder(close, dn)
            cross_down = False
            if dn_cur is not None and dn_prev is not None:
                cross_down = (cp >= dn_prev) and (c < dn_cur)

            exit_trigger = stop_hit or cross_down
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
