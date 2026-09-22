"""zscore-threshold-hold — Rolling price z-score threshold hold.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage21 0 BTC on expansion x dir / bar-pattern.
  Need trend-hold polarity that can clear BTC impulse legs
  without candle patterns or vol-expansion.
  Z-score:
    basis = ta.sma(close, len)
    sd = ta.stdev(close, len)
    z = sd == 0 ? 0 : (close - basis) / sd
  Mode A:
    long rising-edge z > thr
    exit z < exitThr (default 0)
  Mode B:
    require z > thr and z > z[1] (rising z) — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (20, 1.0, 0) Mode A.
  != BB-squeeze / != Disparity / != PGO / != MR-fade.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill len/thr inflate until n collapses;
  Kill BB-squeeze / Disparity / PGO / MR-fade substitute. Prefer Mode A (20,1.0,0), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill thr retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m len=5; stage12-21 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill thr/len retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR.

Forbidden: BB-squeeze labeled z; Disparity zero labeled z-hold;
PGO/ATR-denom labeled z; MR fade (long z<-thr) as this ID; request.security; stage12-21 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, rolling_zscore

STRATEGY_ID = "zscore-threshold-hold"


@dataclass(frozen=True)
class ZscoreParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    length: int = 20      # 20, 30
    thr: float = 1.0      # 1.0, 1.5
    exit_thr: float = 0.0 # 0.0, 0.5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ZscoreParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {20, 30}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{20, 30}}"
    if params.thr not in {1.0, 1.5}:
        return False, f"btc_smoke: thr={params.thr} not in locked sweep {{1.0, 1.5}}"
    if params.exit_thr not in {0.0, 0.5}:
        return False, f"btc_smoke: exit_thr={params.exit_thr} not in locked sweep {{0.0, 0.5}}"
    if params.length > 50:
        return False, f"btc_smoke: length={params.length} collapses BTC n (over-damp)"
    return True, "PASS"


def validate_eth_smoke(params: ZscoreParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.length not in {20, 30} or params.thr not in {1.0, 1.5} or params.exit_thr not in {0.0, 0.5}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ZscoreParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m length<=5 forbidden (spam)"
    if params.length not in {20, 30} or params.thr not in {1.0, 1.5} or params.exit_thr not in {0.0, 0.5}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ZscoreParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.length not in {20, 30} or params.thr not in {1.0, 1.5} or params.exit_thr not in {0.0, 0.5}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ZscoreParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for zscore-threshold-hold."""
    params = params or ZscoreParams()
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
    z_vals = rolling_zscore(closes, length=params.length)

    in_pos = False
    highest_since_entry = 0.0
    prev_hold_cond = False

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        z_cur = z_vals[i]
        z_prev = z_vals[i - 1]

        hold_cond = False
        if z_cur is not None:
            if params.mode == "mode_b":
                hold_cond = (z_cur > params.thr) and (z_prev is not None and z_cur > z_prev)
            else:
                hold_cond = z_cur > params.thr

        rising_edge = hold_cond and not prev_hold_cond

        if not in_pos:
            if rising_edge:
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

            # exit when z < exit_thr
            exit_cond = (z_cur is not None) and (z_cur < params.exit_thr)
            exit_trigger = stop_hit or exit_cond
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

        prev_hold_cond = hold_cond

    return buys, sells, stops
