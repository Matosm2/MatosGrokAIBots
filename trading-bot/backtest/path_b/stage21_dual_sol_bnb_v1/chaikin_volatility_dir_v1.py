"""chaikin-volatility-dir — Marc Chaikin Volatility expansion x close-direction.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage20 VPCI/BW-MFI/DI/Kalman/RAVI = BTC PASS 0/40 (chop under costs).
  Need impulse vol-expansion polarity that can clear BTC >= 1.2x first
  without volume-confirmation oscillators or estimate-cross.
  Chaikin Volatility:
    hl = high - low
    emaHL = ema(hl, emaLen)
    cv = 100.0 * (emaHL - emaHL[rocLen]) / emaHL[rocLen]
    expand = cv > cv[1]
    bull = close > close[dirLen]
  Mode A = long rising-edge (expand and bull); exit when not.
  Mode B = require (cv > 0 and expand) x bull — only if Mode A over-whips;
  identical params across all four coins.
  Prefer (10, 10, 1) Mode A.
  != ATR%ile / != Mass Index / != VPCI / != ATR-slope-alone.

Mode A (prefer (10,10,1)):
  long: rising-edge of (expand and bull)
  exit: not (expand and bull)

Mode B:
  long: rising-edge of (cv > 0 and expand and bull)
  exit: not (cv > 0 and expand and bull)

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill emaLen inflate until n collapses;
  Kill ATR%ile/Mass/Chandelier labeled Chaikin. Prefer Mode A (10,10,1), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m emaLen=3; stage12-20 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill emaLen retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: ATR%ile/Mass/Chandelier labeled Chaikin; ATR-slope-alone labeled Chaikin;
VPCI/DI grafts; request.security; stage12-20 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, chaikin_volatility

STRATEGY_ID = "chaikin-volatility-dir"


@dataclass(frozen=True)
class ChaikinParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    ema_len: int = 10
    roc_len: int = 10
    dir_len: int = 1
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ChaikinParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.ema_len not in {10, 14}:
        return False, f"btc_smoke: ema_len={params.ema_len} not in locked sweep {{10, 14}}"
    if params.roc_len not in {5, 10}:
        return False, f"btc_smoke: roc_len={params.roc_len} not in locked sweep {{5, 10}}"
    if params.dir_len not in {1, 3}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in locked sweep {{1, 3}}"
    if params.ema_len > 25:
        return False, f"btc_smoke: ema_len={params.ema_len} collapses BTC n (over-damp)"
    return True, "PASS"


def validate_eth_smoke(params: ChaikinParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.ema_len not in {10, 14} or params.roc_len not in {5, 10} or params.dir_len not in {1, 3}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ChaikinParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.ema_len <= 3:
        return False, "sol_smoke: 15m ema_len<=3 forbidden (spam)"
    if params.ema_len not in {10, 14} or params.roc_len not in {5, 10} or params.dir_len not in {1, 3}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ChaikinParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.ema_len not in {10, 14} or params.roc_len not in {5, 10} or params.dir_len not in {1, 3}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ChaikinParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for chaikin-volatility-dir."""
    params = params or ChaikinParams()
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
    cv_vals = chaikin_volatility(highs, lows, ema_len=params.ema_len, roc_len=params.roc_len)

    in_pos = False
    highest_since_entry = 0.0
    prev_long_cond = False

    min_bar = max(1, params.dir_len)

    for i in range(min_bar, n):
        c = closes[i]
        h = highs[i]

        cv_cur = cv_vals[i]
        cv_prev = cv_vals[i - 1]

        if cv_cur is not None and cv_prev is not None:
            expand = cv_cur > cv_prev
            if params.mode == "mode_b":
                expand = expand and (cv_cur > 0.0)
        else:
            expand = False

        c_dir_prev = closes[i - params.dir_len]
        bull = c > c_dir_prev

        long_cond = expand and bull
        rising_edge = long_cond and not prev_long_cond

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

            exit_trigger = stop_hit or (not long_cond)
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

        prev_long_cond = long_cond

    return buys, sells, stops
