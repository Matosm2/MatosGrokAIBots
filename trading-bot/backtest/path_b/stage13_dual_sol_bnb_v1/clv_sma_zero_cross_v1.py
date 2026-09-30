"""clv-sma-zero-cross-v1 — Close Location Value SMA zero-cross (volume-free).

LOCKED ENCODE ORDER #5 (OPTIONAL 5TH ENCODE — BTC-CLEARING PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage1 seated AccDist (CLV * volume cumulative); Chaikin Osc / CMF / OBV burned; stage12 CSI wiped.
  CLV = ((close - low) - (high - close)) / (high - low) = (2*close - high - low) / (high - low) in [-1, +1].
  Measures where close sits in the bar range. Path-B Mode A = SMA(CLV, N) x 0, volume-free so SOL!=BNB
  venue-volume shape is avoided (antithesis of deferred NVI/VZO).
  != AccDist line, != III (x volume), != BoP ((C - O)/(H - L)), != CSI triple-smooth body/range.
  Light SMA(N) keeps BTC responsive. OHLC-only -> identical N on SOL+BNB.

Formula:
  rng = high - low
  clv = rng != 0 ? (2*close - high - low) / rng : 0
  clvs = sma(clv, N)
  Prefer N=14.

Mode A (BTC-PRIMARY):
  long: crossover(clvs, 0)
  exit: crossunder(clvs, 0) or ATR stop.

Mode B (BNB quiet):
  long: crossover(clvs, 0) and clvs > 0
  exit: crossunder(clvs, 0) or clvs < 0 or ATR stop.
  (identical N across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if N raised until BTC n collapses;
  Kill if volume*CLV AccDist reintroduced; Kill if CSI triple-EMA graft.
  Prefer Mode A N=14, 1H+.

sol_smoke:
  Kill if AccDist/CMF/III labeled CLV-SMA; 15m N=3; stage12 grafts. Retention check: after ETH, SOL n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+SOL: different N than SOL; Mode B shorts ungated; no ATR; volume graft.
  Prefer identical params; long-only; ATR exit.

Forbidden: AccDist/CMF/III/OBV/volume; BoP; CSI/PMO; stage12 duals.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, clv_sma, crossover, crossunder

STRATEGY_ID = "clv-sma-zero-cross-v1"


@dataclass(frozen=True)
class ClvSmaParams:
    mode: str = "mode_a"  # "mode_a" (clvs cross 0) | "mode_b" (clvs cross 0 and clvs > 0)
    n_len: int = 14
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ClvSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n_len > 30:
        return False, f"btc_smoke: N={params.n_len} > 30 collapses BTC n"
    if params.n_len not in {8, 14, 21}:
        return False, f"btc_smoke: N={params.n_len} not in locked set {{8, 14, 21}}"
    return True, "PASS"


def validate_sol_smoke(params: ClvSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.n_len <= 3:
        return False, "sol_smoke: 15m N<=3 forbidden (spam)"
    if params.n_len not in {8, 14, 21}:
        return False, f"sol_smoke: N={params.n_len} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ClvSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+SOL)."""
    if params.n_len <= 0:
        return False, "bnb_smoke: n_len must be > 0"
    if params.n_len > 50:
        return False, "bnb_smoke: n_len too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ClvSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for clv-sma-zero-cross-v1."""
    params = params or ClvSmaParams()
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
    clvs = clv_sma(highs, lows, closes, n_len=params.n_len)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        curr_clvs = clvs[i]
        cross_up = crossover(clvs, zero_line, i)
        cross_dn = crossunder(clvs, zero_line, i)

        if not in_pos:
            entry_cond = cross_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_clvs is not None and curr_clvs > 0.0)

            if entry_cond:
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

            exit_cond = cross_dn
            if params.mode == "mode_b":
                exit_cond = exit_cond or (curr_clvs is not None and curr_clvs < 0.0)

            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
