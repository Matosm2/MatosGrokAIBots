"""ravi-threshold-dir — Chande RAVI threshold x close direction.

LOCKED ENCODE ORDER #5.
Thesis:
  Stage18 VHF x dir = 0 BTC; stage19 FDI x dir = 0 BTC.
  RAVI (Tushar Chande, Beyond Technical Analysis):
    ravi = abs(100 * (sma(close, short) - sma(close, long)) / sma(close, long))
    bull = close > close[dir_len]
    long_cond = ravi > thr and bull
  Mode A:
    enter on rising edge of long_cond (long_cond and not long_cond[1])
    exit on not long_cond
  Prefer (7, 65, 3.0, 3); if n thin on 1H prefer long=40 identical.
  Mode B: slightly higher thr / longer dir_len — only if Mode A over-whips;
  identical params.
  != dual-MA-cross / != VHF / != FDI / != ADX.

btc_smoke:
  Kill thr/long tighten until entries collapse;
  Kill Mode A BTC 0 / chop; Kill dual-MA-cross / ADX/VHF/FDI substitute.
  Prefer Mode A (7,65,3,3) or (7,40,3,3), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x;
  Kill thr/long retuned only on ETH; Kill direction-blind RAVI or VHF/FDI/III labeled this seat.
  Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x;
  15m short=3 thr=1 spam; stage12-19 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL: Kill 3-coin clear then BNB quiet wipe;
  Kill (short,long,thr,dir_len) retuned only on BNB; Kill Mode B only on BNB;
  HHLL graft; ungated shorts; no ATR.
  Prefer identical; long-only; ATR. If thr too low / dir_len=1 chatters ->
  raise thr/dir_len everywhere, else kill.

Forbidden: SMA fast x slow cross labeled RAVI; ADX/VHF/FDI/TII labeled RAVI;
direction-blind RAVI-alone; request.security; stage12-19 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, ravi

STRATEGY_ID = "ravi-threshold-dir"


@dataclass(frozen=True)
class RaviParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    short_len: int = 7
    long_len: int = 65
    thr: float = 3.0
    dir_len: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: RaviParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.short_len not in {5, 7}:
        return False, f"btc_smoke: short_len={params.short_len} not in locked sweep {{5, 7}}"
    if params.long_len not in {40, 65}:
        return False, f"btc_smoke: long_len={params.long_len} not in locked sweep {{40, 65}}"
    if params.thr not in {2.0, 3.0, 4.0}:
        return False, f"btc_smoke: thr={params.thr} not in locked sweep {{2.0, 3.0, 4.0}}"
    if params.dir_len not in {1, 3, 5}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in locked sweep {{1, 3, 5}}"
    if params.long_len > 100 or params.thr > 6.0:
        return False, "btc_smoke: parameters collapse BTC entries"
    return True, "PASS"


def validate_eth_smoke(params: RaviParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if (
        params.short_len not in {5, 7}
        or params.long_len not in {40, 65}
        or params.thr not in {2.0, 3.0, 4.0}
        or params.dir_len not in {1, 3, 5}
    ):
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: RaviParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and (params.short_len <= 3 or params.thr <= 1.0):
        return False, "sol_smoke: 15m short_len<=3 thr<=1.0 forbidden (spam)"
    if (
        params.short_len not in {5, 7}
        or params.long_len not in {40, 65}
        or params.thr not in {2.0, 3.0, 4.0}
        or params.dir_len not in {1, 3, 5}
    ):
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: RaviParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if (
        params.short_len not in {5, 7}
        or params.long_len not in {40, 65}
        or params.thr not in {2.0, 3.0, 4.0}
        or params.dir_len not in {1, 3, 5}
    ):
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: RaviParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ravi-threshold-dir."""
    params = params or RaviParams()
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
    ravi_vals = ravi(closes, short_len=params.short_len, long_len=params.long_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(params.dir_len, n):
        c = closes[i]
        h = highs[i]

        r_val = ravi_vals[i]
        r_prev = ravi_vals[i - 1]

        bull = c > closes[i - params.dir_len]
        prev_bull = closes[i - 1] > closes[i - 1 - params.dir_len] if (i - 1 >= params.dir_len) else False

        long_cond = (r_val is not None) and (r_val > params.thr) and bull
        prev_long_cond = (r_prev is not None) and (r_prev > params.thr) and prev_bull

        rising_edge = long_cond and not prev_long_cond

        entry_trigger = rising_edge

        if not in_pos:
            if entry_trigger:
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

            exit_cond = not long_cond
            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
