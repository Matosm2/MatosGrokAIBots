"""elder-safezone-trail-flip — Elder SafeZone adverse-penetration trail flip.

LOCKED ENCODE ORDER #4.
Thesis:
  Swap for Dual Differentiator (which is a DC period measurer, not tradeable*0).
  Elder SafeZone (Alexander Elder, Come Into My Trading Room pp. 173-180):
    hl2 = (high + low) / 2
    ema = ta.ema(hl2, emaLen)
    up = ema > ema[3] (uptrend context)
    penDown = max(low[1] - low, 0.0)
    AvgPen = mean of positive penetrations over N
    rawStop = low[1] - k * AvgPen
    longStop = max(rawStop, rawStop[1], rawStop[2], rawStop[3]) (ratchet)
  Mode A:
    long when up and (crossover(close, longStop) or rising-edge(close > longStop and up))
    exit crossunder(close, longStop)
  Mode B:
    require up for confirmBars in {2, 3} — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (emaLen=22, N=10, k=2.5) Mode A.
  != Wilder VS (ATR*factor SAR) / != Chande-Kroll (two-stage ATR corridor) /
  != Guppy CBL / != SuperTrend / != Chandelier / != PSAR.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill N/k inflate until n collapses;
  Kill Wilder-VS/CK/CBL/SuperTrend labeled SafeZone. Prefer Mode A (22, 10, 2.5), 1H+.

eth_smoke:
  CRITICAL: Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill ATR-SAR labeled SafeZone.
  Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill N/k retuned only on SOL;
  15m spam; SuperTrend graft; stage12-25 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: Wilder-VS/Chande-Kroll/CBL/SuperTrend/Chandelier/PSAR labeled SafeZone;
custom var-trail on low/high as exit graft without flip signal;
Dual Differentiator period labeled SafeZone; request.security; stage12-25 grafts;
SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, elder_safezone

STRATEGY_ID = "elder-safezone-trail-flip"


@dataclass(frozen=True)
class ElderSafeZoneParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    ema_len: int = 22             # 14, 22, 30
    n: int = 10                   # 8, 10, 15
    k: float = 2.5                # 2.0, 2.5, 3.0
    confirm_bars: int = 2         # for mode_b
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: ElderSafeZoneParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.ema_len not in {14, 22, 30}:
        return False, f"btc_smoke: ema_len={params.ema_len} not in {{14, 22, 30}}"
    if params.n not in {8, 10, 15}:
        return False, f"btc_smoke: n={params.n} not in {{8, 10, 15}}"
    if params.k not in {2.0, 2.5, 3.0}:
        return False, f"btc_smoke: k={params.k} not in {{2.0, 2.5, 3.0}}"
    return True, "PASS"


def validate_eth_smoke(params: ElderSafeZoneParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC PRIMARY CRITICAL)."""
    if (
        params.ema_len not in {14, 22, 30}
        or params.n not in {8, 10, 15}
        or params.k not in {2.0, 2.5, 3.0}
    ):
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ElderSafeZoneParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if (
        params.ema_len not in {14, 22, 30}
        or params.n not in {8, 10, 15}
        or params.k not in {2.0, 2.5, 3.0}
    ):
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ElderSafeZoneParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if (
        params.ema_len not in {14, 22, 30}
        or params.n not in {8, 10, 15}
        or params.k not in {2.0, 2.5, 3.0}
    ):
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ElderSafeZoneParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for elder-safezone-trail-flip."""
    params = params or ElderSafeZoneParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    long_stops, up_series = elder_safezone(
        highs, lows, closes,
        ema_len=params.ema_len,
        n=params.n,
        k=params.k,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        stop_val = long_stops[i]
        prev_stop = long_stops[i - 1]

        if stop_val is None or prev_stop is None:
            continue

        co_stop = (closes[i - 1] <= prev_stop) and (c > stop_val)
        cu_stop = (closes[i - 1] >= prev_stop) and (c < stop_val)
        c_below_stop = c < stop_val

        is_up = up_series[i]
        if params.mode == "mode_b":
            # Require up for confirm_bars
            c_bars = params.confirm_bars
            start_b = max(0, i - c_bars + 1)
            is_up = is_up and all(up_series[j] for j in range(start_b, i + 1))

        # Rising edge of (close > stop and is_up)
        prev_cond = (closes[i - 1] > prev_stop) and up_series[i - 1]
        cur_cond = (c > stop_val) and is_up
        rising_edge = cur_cond and not prev_cond

        # Long entry logic
        if not in_pos:
            entry_cond = (co_stop and is_up) or rising_edge

            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                # Use SafeZone long_stop as initial stop
                active_stop = stop_val
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    atr_stop = c - params.atr_trail_mult * atr_vals[i]
                    active_stop = max(active_stop, atr_stop)
                stops[i] = active_stop
        else:
            if h > highest_since_entry:
                highest_since_entry = h

            # SafeZone ratchet stop tracking
            active_stop = stop_val
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                atr_stop = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                active_stop = max(active_stop, atr_stop)
            stops[i] = active_stop

            exit_cond = cu_stop or c_below_stop
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
