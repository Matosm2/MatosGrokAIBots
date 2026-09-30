"""fdi-low-trend-dir — Fractal Dimension Index low-trend regime x close direction.

LOCKED ENCODE ORDER #5 (BTC LEAD PRIMARY).
Thesis:
  Stage18 VHF x dir = 0 BTC (regime x dir over-damp / chop under costs).
  FDI (Carlos Sevcik / Alex Matulich correction) measures path fractal dimension in [~1, 2]:
    FDI < thr (~1.5) -> trending (persistent / Hurst > 0.5)
    FDI > thr -> ranging (planar / mean-reverting)
  Mode A pairs low FDI with close direction:
    bull = close > close[dirLen]
    longCond = fdi < thr and bull
    long when longCond and not longCond[1]
    exit when not longCond
  Intended to hold BTC trend legs denser than stage18 VHF wipe.
  != FRAMA (Ehlers adaptive MA).
  != CHOP (Choppiness Index).
  != VHF (stage18).
  != RWI (stage7).
  Identical (n, thr, dirLen) across all four coins.

Mode A (BTC-LEAD PRIMARY — prefer):
  long: longCond and not longCond[1]
  exit: not longCond

Mode B (BNB quiet / chatter):
  slightly lower thr / longer n — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill n/thr tighten until entries collapse (VHF stage18 rhyme);
  Kill Mode A BTC 0 / chop; Kill FRAMA/CHOP/VHF substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A (30,1.5,3), 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill thr/n retuned only on ETH; Kill direction-blind FDI or VHF/CHOP labeled this seat.
  Prefer identical (30,1.5,3); ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m n=5 thr=1.8; stage12-18 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different (n,thr,dirLen); Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: FRAMA/CHOP/VHF/RWI labeled FDI; direction-blind FDI; stage12-18 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, fdi

STRATEGY_ID = "fdi-low-trend-dir"


@dataclass(frozen=True)
class FdiParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    n: int = 30
    thr: float = 1.50
    dir_len: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: FdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {20, 30}:
        return False, f"btc_smoke: n={params.n} not in locked sweep {{20, 30}}"
    if params.thr not in {1.40, 1.45, 1.50, 1.55}:
        return False, f"btc_smoke: thr={params.thr} not in locked sweep"
    if params.dir_len not in {1, 3, 5}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in locked sweep {{1, 3, 5}}"
    if params.thr < 1.20:
        return False, f"btc_smoke: thr={params.thr} collapses BTC entries"
    return True, "PASS"


def validate_eth_smoke(params: FdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.n not in {20, 30} or params.thr not in {1.40, 1.45, 1.50, 1.55} or params.dir_len not in {1, 3, 5}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: FdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and (params.n <= 5 or params.thr >= 1.8):
        return False, "sol_smoke: 15m n<=5 thr>=1.8 forbidden (spam)"
    if params.n not in {20, 30} or params.thr not in {1.40, 1.45, 1.50, 1.55} or params.dir_len not in {1, 3, 5}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: FdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.n not in {20, 30} or params.thr not in {1.40, 1.45, 1.50, 1.55} or params.dir_len not in {1, 3, 5}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: FdiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for fdi-low-trend-dir."""
    params = params or FdiParams()
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
    fdi_vals = fdi(closes, n=params.n)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(params.dir_len, n):
        c = closes[i]
        h = highs[i]

        fdi_val = fdi_vals[i]
        fdi_prev = fdi_vals[i - 1]

        bull = c > closes[i - params.dir_len]
        prev_bull = closes[i - 1] > closes[i - 1 - params.dir_len] if (i - 1 >= params.dir_len) else False

        long_cond = (fdi_val is not None) and (fdi_val < params.thr) and bull
        prev_long_cond = (fdi_prev is not None) and (fdi_prev < params.thr) and prev_bull

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
