"""vhf-threshold-close-dir — Vertical Horizontal Filter threshold x close direction.

LOCKED ENCODE ORDER #3 (BTC LEAD + ETH-PORTABLE PRIMARY).
Thesis:
  Stage17 deferred raw VHF as direction-blind; Stage17 III wiped ETH after dense BTC.
  VHF (Adam White) = (highest(close,n) - lowest(close,n)) / sum(abs(close-close[1]), n) — close-path regime gauge.
  Mode A pairs VHF > thr with close direction (close > close[dirLen]) so the seat is tradeable
  without ADX/CHOP/RWI grafts and without volume-intensity.
  Intended dense BTC clears and ETH-portable trend/range gate with identical (n, thr, dirLen).
  != CHOP.
  != ADX/DMI.
  != RWI (parked).

Formula:
  num = highest(close, n) - lowest(close, n)
  den = sum(abs(close - close[1]), n)
  vhf = den == 0 ? 0.0 : num / den
  bull = close > close[dirLen]
  longCond = vhf > thr and bull
  Prefer (28, 0.35, 3).

Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer):
  long when longCond and not longCond[1]
  exit when not longCond

Mode B (BNB quiet):
  raise thr slightly / longer n — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill n/thr inflate until entries collapse;
  Kill ADX/CHOP substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A (28,0.35,3), 1H+.

eth_smoke:
  BTC->ETH PRIMARY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill thr/n retuned only on ETH; Kill direction-blind VHF or ADX/CHOP/III labeled this seat.
  Prefer identical (28,0.35,3); ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m n=5 thr=0.1 spam; stage12-17 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different (n,thr,dirLen); Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: CHOP/ADX/RWI labeled VHF; direction-blind VHF-alone; III/volume; MA dual as direction; stage12-17.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, vertical_horizontal_filter

STRATEGY_ID = "vhf-threshold-close-dir"


@dataclass(frozen=True)
class VhfParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    n: int = 28
    thr: float = 0.35
    dir_len: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: VhfParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {18, 28}:
        return False, f"btc_smoke: n={params.n} not in locked sweep {{18, 28}}"
    if params.thr not in {0.30, 0.35, 0.40}:
        return False, f"btc_smoke: thr={params.thr} not in locked sweep {{0.30, 0.35, 0.40}}"
    if params.dir_len not in {1, 3, 5}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in locked sweep {{1, 3, 5}}"
    if params.n > 60 or params.thr > 0.60:
        return False, "btc_smoke: params inflated until entries collapse"
    return True, "PASS"


def validate_eth_smoke(params: VhfParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PRIMARY CRITICAL)."""
    if params.n not in {18, 28} or params.thr not in {0.30, 0.35, 0.40} or params.dir_len not in {1, 3, 5}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VhfParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and (params.n <= 5 or params.thr <= 0.1):
        return False, "sol_smoke: 15m n<=5 thr<=0.1 forbidden (spam)"
    if params.n not in {18, 28} or params.thr not in {0.30, 0.35, 0.40} or params.dir_len not in {1, 3, 5}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: VhfParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.n not in {18, 28} or params.thr not in {0.30, 0.35, 0.40} or params.dir_len not in {1, 3, 5}:
        return False, "bnb_smoke: params not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VhfParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vhf-threshold-close-dir."""
    params = params or VhfParams()
    n_bars = len(bars)
    buys = [False] * n_bars
    sells = [False] * n_bars
    stops: list[float | None] = [None] * n_bars
    if n_bars == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    vhf_vals = vertical_horizontal_filter(closes, length=params.n)

    # Boolean condition array
    long_cond = [False] * n_bars
    for i in range(params.dir_len, n_bars):
        v = vhf_vals[i]
        if v is not None and v > params.thr:
            bull = closes[i] > closes[i - params.dir_len]
            long_cond[i] = bull

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n_bars):
        c = closes[i]
        h = highs[i]

        curr_cond = long_cond[i]
        prev_cond = long_cond[i - 1]

        rising_edge = curr_cond and not prev_cond
        falling_edge = not curr_cond and prev_cond

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

            if stop_hit or falling_edge:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
