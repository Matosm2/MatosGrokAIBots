"""rvol-pivot-structure-break-v1 — RVOL Participation Gate + Pivot / Lookback-Close Structure Break.

LOCKED ENCODE ORDER #1 (BNB-survival-FIRST).
Thesis:
  Thin BNB liquidity produces many hollow OHLC breaks; requiring relative volume (RVOL) >= k
  on the break bar filters non-participating fakeouts.
  Structure = last confirmed pivot H/L (Mode A) OR close > close[L] (Mode B, NOT ta.highest).

Indicators:
  rvol = volume / ta.sma(volume, volLen); volLen in {20, 50}.

Structure Mode A (preferred):
  Last confirmed ta.pivothigh / ta.pivotlow (lb=rb in {2, 3}).
  Long when close > last confirmed pivot high after prior close <= that level and rvol >= k.
  Short symmetric below confirmed pivot low.

Structure Mode B (denser):
  Long when close > close[L] and prior close <= close[L] and rvol >= k (L in {5, 10, 20}).
  Strictly close vs close[L], NOT ta.highest(high, n).

Exit:
  Close back through pivot / opposite structure, or ATR trail stop.

BNB Smoke Rules:
  Kill if: (1) no min RVOL (k >= 1.5 on BNB); (2) range < 0.15*ATR or range/close < 0.002;
  (3) 15m; (4) Mode B with L < 10. Skip volume == 0.

Distinct from: Donchian, ConnorsRSI, OBV/CMF, PHH/PDH/PWH.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, pivothigh, pivotlow, rvol

STRATEGY_ID = "rvol-pivot-structure-break-v1"


@dataclass(frozen=True)
class RvolPivotParams:
    mode: str = "mode_a"  # "mode_a" (pivot) | "mode_b" (lookback close)
    rvol_k: float = 1.5
    vol_len: int = 20
    pivot_len: int = 2  # left=right bars for Mode A
    lookback_l: int = 10  # L for Mode B: close > close[L]
    atr_filter: bool = True  # min ATR% / range floor
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: RvolPivotParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for rvol-pivot-structure-break-v1."""
    params = params or RvolPivotParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]

    rvol_vals = rvol(vols, params.vol_len)
    atr_vals = atr(highs, lows, closes, params.atr_len)

    ph_vals = pivothigh(highs, params.pivot_len, params.pivot_len) if params.mode == "mode_a" else None
    pl_vals = pivotlow(lows, params.pivot_len, params.pivot_len) if params.mode == "mode_a" else None

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None
    last_ph: float | None = None
    last_pl: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        l = lows[i]
        v = vols[i]
        rv = rvol_vals[i]

        # Update last confirmed pivots for Mode A
        if params.mode == "mode_a" and ph_vals is not None and pl_vals is not None:
            if ph_vals[i] is not None:
                last_ph = ph_vals[i]
            if pl_vals[i] is not None:
                last_pl = pl_vals[i]

        # Volume == 0 check (BNB smoke requirement)
        if v == 0:
            if in_pos:
                stops[i] = stop_level
            continue

        # ATR range floor check
        bar_range = h - l
        atr_cur = atr_vals[i]
        range_ok = True
        if params.atr_filter:
            if atr_cur is not None and atr_cur > 0:
                if bar_range < 0.15 * atr_cur or (c > 0 and bar_range / c < 0.002):
                    range_ok = False
            elif c > 0 and bar_range / c < 0.002:
                range_ok = False

        rvol_ok = (rv is not None and rv >= params.rvol_k)

        # Check entry / exit conditions
        entry_sig = False
        exit_sig = False

        if params.mode == "mode_a":
            if last_ph is not None and i > 0:
                prev_c = closes[i - 1]
                # Breakout: close > pivot high after prior close <= pivot high
                if prev_c <= last_ph and c > last_ph and rvol_ok and range_ok:
                    entry_sig = True
            if last_ph is not None and in_pos:
                # Close back below pivot high
                if c < last_ph:
                    exit_sig = True
            if last_pl is not None and in_pos:
                # Or close below pivot low
                if c < last_pl:
                    exit_sig = True
        else:  # mode_b
            L = params.lookback_l
            if i >= L:
                ref_c = closes[i - L]
                prev_c = closes[i - 1]
                prev_ref_c = closes[i - 1 - L] if (i - 1 >= L) else ref_c
                # Breakout: close > close[L] and prior close <= prior close[L]
                if prev_c <= prev_ref_c and c > ref_c and rvol_ok and range_ok:
                    entry_sig = True
                if in_pos and c < ref_c:
                    exit_sig = True

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, c)

            hit_exit = False
            if exit_sig:
                hit_exit = True
            elif params.atr_trail_mult > 0.0 and atr_cur is not None:
                trail_stop = highest_since_entry - atr_cur * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if c < stop_level:
                    hit_exit = True

            if hit_exit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if entry_sig:
            buys[i] = True
            in_pos = True
            highest_since_entry = c
            if params.atr_trail_mult > 0.0 and atr_cur is not None:
                stop_level = c - atr_cur * params.atr_trail_mult
                stops[i] = stop_level

    return buys, sells, stops
