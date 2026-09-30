"""parkinson-vol-expansion-dir — Parkinson HV expansion x close-direction.

LOCKED ENCODE ORDER #4 (OPTIONAL DROP).
Thesis:
  Stage20 0 BTC chop. Need second distinct range-vol expansion x dir seat.
  Parkinson HV (1980):
    lr2 = math.pow(math.log(high / low), 2)  (guarded)
    park = math.sqrt(ta.sma(lr2, nPark) / (4 * math.log(2)))
    expand = park > park[1]
    bull = close > close[dirLen]
  Mode A = long rising-edge (expand and bull); exit when not.
  Mode B = require park > ta.sma(park, slowLen) x bull — only if Mode A over-whips;
  identical params across all four coins.
  Prefer (10, 1) Mode A.
  REDUNDANCY RULE: After BTC smoke on #1+#4: if Parkinson BTC behavior ≈ Chaikin
  (same cells / same chop), DROP #4 — do not encode both. Prefer keep Chaikin if tie.
  != ATR%ile / != Chaikin CV / != Garman-Klass.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill nPark inflate until n collapses;
  Kill ATR%ile/Chaikin/Mass labeled Parkinson. Prefer Mode A (10,1), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill nPark retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m nPark=3; stage12-20 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill nPark retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: ATR%ile labeled Parkinson; Chaikin CV labeled Parkinson; GK labeled this ID;
request.security; stage12-20 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, parkinson_vol, sma

STRATEGY_ID = "parkinson-vol-expansion-dir"


@dataclass(frozen=True)
class ParkinsonParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    n_park: int = 10
    dir_len: int = 1
    slow_len: int = 0  # 0 = raw rising; >0 = park > sma(park, slow_len)
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ParkinsonParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n_park not in {10, 14}:
        return False, f"btc_smoke: n_park={params.n_park} not in locked sweep {{10, 14}}"
    if params.dir_len not in {1, 3}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in locked sweep {{1, 3}}"
    if params.slow_len not in {0, 10}:
        return False, f"btc_smoke: slow_len={params.slow_len} not in locked sweep {{0, 10}}"
    if params.n_park > 30:
        return False, f"btc_smoke: n_park={params.n_park} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: ParkinsonParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.n_park not in {10, 14} or params.dir_len not in {1, 3} or params.slow_len not in {0, 10}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ParkinsonParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.n_park <= 3:
        return False, "sol_smoke: 15m n_park<=3 forbidden (spam)"
    if params.n_park not in {10, 14} or params.dir_len not in {1, 3} or params.slow_len not in {0, 10}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ParkinsonParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.n_park not in {10, 14} or params.dir_len not in {1, 3} or params.slow_len not in {0, 10}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ParkinsonParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for parkinson-vol-expansion-dir."""
    params = params or ParkinsonParams()
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
    park_vals = parkinson_vol(highs, lows, n_park=params.n_park)

    sma_park: list[float | None] = [None] * n
    if params.mode == "mode_b" and params.slow_len > 0:
        valid_park = [v if v is not None else 0.0 for v in park_vals]
        sma_park = sma(valid_park, params.slow_len)

    in_pos = False
    highest_since_entry = 0.0
    prev_long_cond = False

    min_bar = max(1, params.dir_len)

    for i in range(min_bar, n):
        c = closes[i]
        h = highs[i]

        park_cur = park_vals[i]
        park_prev = park_vals[i - 1]

        if park_cur is not None and park_prev is not None:
            expand = park_cur > park_prev
            if params.mode == "mode_b" and params.slow_len > 0:
                s_val = sma_park[i]
                expand = expand and (s_val is not None and park_cur > s_val)
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
