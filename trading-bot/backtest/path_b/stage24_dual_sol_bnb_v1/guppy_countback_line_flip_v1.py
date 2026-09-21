"""guppy-countback-line-flip — Guppy Count Back Line close×CBL SAR flip.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage23 BTC PASS 0/32; closest Chande-Kroll ~1.194x near-miss — need published
  non-ATR count-back SAR that can clear dense BTC >= 1.2x without cloning
  Wilder VS / Chande-Kroll / SuperTrend / PSAR.
  Guppy CBL (Daryl Guppy):
    From most recent significant HH: count back 3 successively lower lows -> cblLong
    (ratchet: never lower existing cblLong).
    From most recent significant LL: count back 3 successively higher highs -> cblShort
    (ratchet: never raise existing cblShort).
  Mode A:
    long crossover(close, cblShort)
    exit crossunder(close, cblLong)
  Mode B:
    require min bars since CBL update >= kConfirm, or optional ATR exit mult in {1.5, 2.0};
    identical params across all four coins.
  Prefer countDepth=3 Mode A.
  != Wilder VS (factor*ATR) / != Chande-Kroll (two-stage ATR) / != SuperTrend / != PSAR.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x;
  Kill countDepth inflated / over-confirm until n collapses;
  Kill SuperTrend/Wilder/CK/PSAR labeled CBL. Prefer Mode A countDepth=3, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill params retuned only on SOL;
  15m spam; stage12-23 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill countDepth retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: SuperTrend/Chandelier/Wilder-VS/Chande-Kroll/PSAR labeled CBL;
request.security; stage12-23 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, guppy_cbl

STRATEGY_ID = "guppy-countback-line-flip"


@dataclass(frozen=True)
class GuppyCblParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    count_depth: int = 3        # 3 (locked)
    atr_trail_mult: float = 0.0 # 0.0 (off), 1.5, 2.0
    atr_len: int = 14
    k_confirm: int = 0          # Mode B min bars since CBL update (e.g. 2)


def validate_btc_smoke(params: GuppyCblParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.count_depth != 3:
        return False, f"btc_smoke: count_depth={params.count_depth} != 3 (locked published)"
    if params.atr_trail_mult not in {0.0, 1.5, 2.0}:
        return False, f"btc_smoke: atr_trail_mult={params.atr_trail_mult} not in {{0.0, 1.5, 2.0}}"
    return True, "PASS"


def validate_eth_smoke(params: GuppyCblParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.count_depth != 3 or params.atr_trail_mult not in {0.0, 1.5, 2.0}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: GuppyCblParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.count_depth != 3 or params.atr_trail_mult not in {0.0, 1.5, 2.0}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: GuppyCblParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.count_depth != 3 or params.atr_trail_mult not in {0.0, 1.5, 2.0}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: GuppyCblParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for guppy-countback-line-flip."""
    params = params or GuppyCblParams()
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
    cbl_long, cbl_short = guppy_cbl(highs, lows, closes, params.count_depth)

    in_pos = False
    highest_since_entry = 0.0

    # Track bars since cbl_short changed for Mode B
    bars_since_update = 0
    prev_cbl_short: float | None = None

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        cur_cbl_s = cbl_short[i]
        prev_cbl_s = cbl_short[i - 1]
        cur_cbl_l = cbl_long[i]
        prev_cbl_l = cbl_long[i - 1]

        if cur_cbl_s != prev_cbl_short:
            bars_since_update = 0
            prev_cbl_short = cur_cbl_s
        else:
            bars_since_update += 1

        if not in_pos:
            # Entry: crossover(close, cblShort)
            if cur_cbl_s is not None:
                cross_up = (prev_cbl_s is not None and cp <= prev_cbl_s and c > cur_cbl_s) or (prev_cbl_s is None and c > cur_cbl_s)
                if cross_up:
                    can_enter = True
                    if params.mode == "mode_b" and params.k_confirm > 0:
                        if bars_since_update < params.k_confirm:
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

            # Exit: crossunder(close, cblLong)
            cross_exit = False
            if cur_cbl_l is not None:
                cross_exit = (prev_cbl_l is not None and cp >= prev_cbl_l and c < cur_cbl_l) or (prev_cbl_l is None and c < cur_cbl_l)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
