"""kalman-estimate-cross — Simple 1D Kalman filter price x estimate cross.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage19 HHLL structure overtraded quiet BNB; FIR/SS duals EXIT'd stage12.
  Kalman (Rudolf E. Kalman 1960; public 1D price ports):
    predict = estimate
    gain = error_est / (error_est + error_meas)
    estimate = prediction + gain * (close - prediction)
    error_est = (1 - gain) * error_est + Q / length
    error_meas = R * length
  Mode A = close x estimate cross.
  Intended quieter-market survival (gain damps noise when error_est low)
  while remaining responsive on majors impulse.
  != Nadaraya-RQ / != Ehlers PMA / != SuperSmoother.

Mode A (prefer (20, 0.01, 0.1)):
  long: crossover(close, estimate)
  exit: crossunder(close, estimate)

Mode B (BNB quiet / chatter):
  require estimate slope estimate > estimate[slope_len] — only if Mode A over-whips;
  identical params.

btc_smoke:
  Kill length/R inflate until n collapses;
  Kill Mode A BTC 0 / chop; Kill Nadaraya/PMA/SS substitute.
  Prefer Mode A (20, 0.01, 0.1), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x;
  Kill (length,R,Q) retuned only on ETH; Kill Nadaraya/PMA labeled Kalman.
  Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x;
  15m length=5 Q=1 spam; stage12-19 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL: Kill 3-coin clear then BNB quiet wipe;
  Kill length/R/Q retuned only on BNB; Kill Mode B only on BNB;
  HHLL graft; ungated shorts; no ATR.
  Prefer identical; long-only; ATR. If estimate hugs price ->
  raise R everywhere or Mode B slope, else kill.

Forbidden: Nadaraya/PMA/SS labeled Kalman; dual Kalman short x long first pass;
request.security; stage12-19 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, kalman_1d

STRATEGY_ID = "kalman-estimate-cross"


@dataclass(frozen=True)
class KalmanParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    length: int = 20
    r: float = 0.01
    q: float = 0.1
    slope_len: int = 0  # Mode B: estimate > estimate[slope_len]
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: KalmanParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {14, 20, 30}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{14, 20, 30}}"
    if params.r not in {0.01, 0.02}:
        return False, f"btc_smoke: r={params.r} not in locked sweep {{0.01, 0.02}}"
    if params.q not in {0.05, 0.1}:
        return False, f"btc_smoke: q={params.q} not in locked sweep {{0.05, 0.1}}"
    if params.length > 50:
        return False, f"btc_smoke: length={params.length} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: KalmanParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if (
        params.length not in {14, 20, 30}
        or params.r not in {0.01, 0.02}
        or params.q not in {0.05, 0.1}
    ):
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: KalmanParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and (params.length <= 5 or params.q >= 1.0):
        return False, "sol_smoke: 15m length<=5 Q>=1.0 forbidden (spam)"
    if (
        params.length not in {14, 20, 30}
        or params.r not in {0.01, 0.02}
        or params.q not in {0.05, 0.1}
    ):
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: KalmanParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if (
        params.length not in {14, 20, 30}
        or params.r not in {0.01, 0.02}
        or params.q not in {0.05, 0.1}
    ):
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KalmanParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for kalman-estimate-cross."""
    params = params or KalmanParams()
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
    estimate = kalman_1d(closes, length=params.length, r=params.r, q=params.q)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(closes, estimate, i)
        cross_dn = crossunder(closes, estimate, i)

        entry_trigger = cross_up
        if params.mode == "mode_b" and params.slope_len > 0:
            if i >= params.slope_len:
                e_now = estimate[i]
                e_prev = estimate[i - params.slope_len]
                slope_ok = (e_now is not None and e_prev is not None and e_now > e_prev)
            else:
                slope_ok = False
            entry_trigger = cross_up and slope_ok

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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
