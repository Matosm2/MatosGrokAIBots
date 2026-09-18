"""atrpct-percentile-sma-cross-v1 — ATR% Percentile Regime Gate + SMA Cross.

LOCKED ENCODE ORDER #2 (DUAL-SURVIVAL: SOL + BNB).
Thesis:
  Normalizes volatility as atrPct = 100 * ATR(14) / close, then computes rolling percentile rank
  over window W bars. Entries are allowed strictly inside a regime band: lo <= rank <= hi.
  Skipping dead compression (rank < lo) protects against BNB hollow whipsaws; capping extreme
  volatility (rank > hi) avoids manic SOL blow-offs.
  Uses pure SMA (strictly NOT SMA200, NOT EMA ribbon, NOT ATR-squeeze / BB-squeeze).

Regime:
  atrPct = 100 * ATR(14) / close
  rank = percent_rank(atrPct, W), W in {100, 150}
  Allowed entry if: lo <= rank <= hi
  Pairs: (lo, hi) in {(25, 85), (30, 100), (40, 80)}

Mode A (primary):
  fast = ta.sma(close, f), slow = ta.sma(close, s)
  (f, s) in {(10, 30), (20, 50)} - NOT 200
  Long: ta.crossover(fast, slow) while lo <= rank <= hi

Mode B:
  close x ta.sma(close, len) while lo <= rank <= hi (len in {20, 50})

Exit:
  Opposite cross OR regime leave (rank < lo, if exit_on_regime_leave=True) + ATR trail stop.

Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, percent_rank, sma

STRATEGY_ID = "atrpct-percentile-sma-cross-v1"


@dataclass(frozen=True)
class AtrPctSmaParams:
    mode: str = "mode_a"  # "mode_a" (SMA x SMA) | "mode_b" (close x SMA)
    fast_len: int = 20
    slow_len: int = 50
    sma_len: int = 20  # for Mode B
    window_w: int = 100
    rank_lo: float = 25.0
    rank_hi: float = 85.0
    exit_on_regime_leave: bool = True
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: AtrPctSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.window_w == 100:
        return False, "sol_smoke: 15m with W=100 (unstable rank)"
    if params.fast_len >= 200 or params.slow_len >= 200 or params.sma_len >= 200:
        return False, "sol_smoke: SMA200 graft forbidden"
    return True, "PASS"


def validate_bnb_smoke(params: AtrPctSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.rank_lo <= 0.0:
        return False, "bnb_smoke: regime off / lo=0 (ungated SMA risk)"
    if not params.exit_on_regime_leave:
        return False, "bnb_smoke: exit_on_regime_leave must be True"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: AtrPctSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for atrpct-percentile-sma-cross-v1."""
    params = params or AtrPctSmaParams()
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

    # Compute atrPct = 100 * ATR(14) / close
    atr_pct: list[float] = [0.0] * n
    valid_atr_pct: list[float] = []
    for i in range(n):
        av = atr_vals[i]
        c = closes[i]
        if av is not None and c > 0:
            val = 100.0 * av / c
            atr_pct[i] = val
            valid_atr_pct.append(val)
        else:
            atr_pct[i] = 0.0
            valid_atr_pct.append(0.0)

    # Percent rank over window_w
    rank_vals = percent_rank(atr_pct, params.window_w)

    # MAs
    fast_sma = sma(closes, params.fast_len) if params.mode == "mode_a" else None
    slow_sma = sma(closes, params.slow_len) if params.mode == "mode_a" else sma(closes, params.sma_len)
    close_series: list[float | None] = [float(c) for c in closes]

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        rk = rank_vals[i]

        regime_allow = rk is not None and (params.rank_lo <= rk <= params.rank_hi)
        regime_leave = rk is not None and (rk < params.rank_lo)

        # Trailing stop update if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False

            if params.mode == "mode_a" and fast_sma is not None and slow_sma is not None:
                if crossunder(fast_sma, slow_sma, i):
                    exit_signal = True
            elif params.mode == "mode_b" and slow_sma is not None:
                if crossunder(close_series, slow_sma, i):
                    exit_signal = True

            # Regime leave exit
            if params.exit_on_regime_leave and regime_leave:
                exit_signal = True

            # Stop hit check
            if stop_level is not None and c < stop_level:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0
                stop_level = None
                continue

        # Check entries if flat
        if not in_pos and regime_allow:
            enter_signal = False

            if params.mode == "mode_a" and fast_sma is not None and slow_sma is not None:
                if crossover(fast_sma, slow_sma, i):
                    enter_signal = True
            elif params.mode == "mode_b" and slow_sma is not None:
                if crossover(close_series, slow_sma, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
