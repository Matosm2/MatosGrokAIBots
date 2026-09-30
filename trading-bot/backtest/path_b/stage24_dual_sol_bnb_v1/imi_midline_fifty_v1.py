"""imi-midline-fifty — Intraday Momentum Index body RSI ×50 midline.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage23 0-BTC / 1.194x near-miss — need body-based impulse oscillator that
  can clear BTC without cloning stage9/10 midline IDs or raw RSI.
  IMI (Tushar Chande):
    up = max(close - open, 0)
    dn = max(open - close, 0)
    imi = 100 * sum(up, n) / (sum(up, n) + sum(dn, n)) (denom0 -> 50.0)
  Mode A:
    long crossover(imi, 50)
    exit crossunder(imi, 50)
  Mode B:
    require imi > 55 — only if Mode A over-whips;
    identical params across all four coins. Never PSY/RMI/TII/RSI graft.
  Prefer n=14 Mode A.
  != PSY (% of up closes) / != RMI (momentum RSI) / != TII / != raw RSI / != QQE.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x;
  Kill n inflate until n collapses;
  Kill PSY/RMI/TII/raw-RSI/QQE labeled IMI. Prefer Mode A n=14, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill n retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill n retuned only on SOL;
  15m n=3; stage12-23 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill n retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: PSY/RMI/TII/raw-RSI/QQE labeled IMI;
request.security; stage12-23 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, imi

STRATEGY_ID = "imi-midline-fifty"


@dataclass(frozen=True)
class ImiParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    n: int = 14                 # 10, 14, 21
    thr: float = 50.0           # 50.0
    entry_thr: float = 55.0     # Mode B entry thr
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ImiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {10, 14, 21}:
        return False, f"btc_smoke: n={params.n} not in {{10, 14, 21}}"
    return True, "PASS"


def validate_eth_smoke(params: ImiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.n not in {10, 14, 21}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ImiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {10, 14, 21}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ImiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.n not in {10, 14, 21}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ImiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for imi-midline-fifty."""
    params = params or ImiParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    imi_vals = imi(opens, closes, params.n)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_imi = imi_vals[i]
        prev_imi = imi_vals[i - 1]

        if not in_pos:
            # Entry: crossover(imi, thr)
            if cur_imi is not None and prev_imi is not None:
                cross_up = (prev_imi <= params.thr) and (cur_imi > params.thr)
                if cross_up:
                    can_enter = True
                    if params.mode == "mode_b":
                        if cur_imi < params.entry_thr:
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

            # Exit: crossunder(imi, thr)
            cross_exit = False
            if cur_imi is not None and prev_imi is not None:
                cross_exit = (prev_imi >= params.thr) and (cur_imi < params.thr)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
