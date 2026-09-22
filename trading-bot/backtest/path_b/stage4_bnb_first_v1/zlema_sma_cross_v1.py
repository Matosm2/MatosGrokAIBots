"""zlema-sma-cross-v1 — Lag-Compensated ZLEMA x SMA Crossover (RVOL ON for BNB smoke).

LOCKED ENCODE ORDER #5 (last encode, BNB-survival-FIRST).
Thesis:
  Lag-compensated ZLEMA tracks price tighter than EMA/ALMA/T3 of similar length.
  Crossing a slower SMA (equal-weight anchor) yields dense trend flips on SOL 1H-4H with a different
  surface than wiped ALMA (Gaussian) and T3 (GDEMA nest). Pure OHLC - weaker BNB thesis,
  so RVOL gate is mandatory on BNB smoke/ladder.

Formula:
  Lag-compensation ZLEMA only:
    lag = round((len - 1) / 2)
    src_comp = close + (close - close[lag])
    zlema = EMA(src_comp, len)
  NOT the 2010 Ehlers-Way EC gain-search form.
  Slow line: SMA(close, lenS).

Entry Mode A:
  Long: ta.crossover(zlema, sma) (with RVOL >= k on cross bar when enabled).
  Short / Flat: ta.crossunder(zlema, sma).

Entry Mode B:
  Fast ZLEMA x Slow ZLEMA (dual ZLEMA, only after Mode A baseline).

RVOL Gate:
  volume >= k * ta.sma(volume, 20) on cross bar.
  MANDATORY ON BNB SMOKE / LADDER (k >= 1.2).

Exit:
  Opposite cross or ATR trail stop.

BNB Smoke Rules:
  Kill if: (1) no RVOL gate on BNB; (2) 15m; (3) dual-ZLEMA + length soup; (4) EC-form confusion.
  Require RVOL >= 1.2 on cross; prefer ZLEMA x SMA (20, 50) first.

Distinct from: ALMA, T3, EMA ribbon, SMA200, EC-ZLEMA gain sweep, Hull primary.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, rvol, sma, zlema

STRATEGY_ID = "zlema-sma-cross-v1"


@dataclass(frozen=True)
class ZlemaSmaParams:
    mode: str = "mode_a"  # "mode_a" (zlema x sma) | "mode_b" (dual zlema)
    zlema_len: int = 20
    sma_len: int = 50
    rvol_k: float = 0.0  # RVOL gate multiplier (0.0 = off; >= 1.2 on BNB smoke)
    vol_len: int = 20
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: ZlemaSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for zlema-sma-cross-v1."""
    params = params or ZlemaSmaParams()
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

    fast_line = zlema(closes, params.zlema_len)
    slow_line = zlema(closes, params.sma_len) if params.mode == "mode_b" else sma(closes, params.sma_len)

    rvol_vals = rvol(vols, params.vol_len) if params.rvol_k > 0 else None
    atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        v = vols[i]
        fl = fast_line[i]
        sl = slow_line[i]

        if fl is None or sl is None or v == 0:
            if in_pos:
                stops[i] = stop_level
            continue

        rvol_ok = True
        if params.rvol_k > 0:
            rv = rvol_vals[i] if rvol_vals else None
            rvol_ok = (rv is not None and rv >= params.rvol_k)

        entry_sig = crossover(fast_line, slow_line, i) and rvol_ok
        exit_sig = crossunder(fast_line, slow_line, i)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, c)

            hit_exit = False
            if exit_sig:
                hit_exit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
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
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = c - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level

    return buys, sells, stops
