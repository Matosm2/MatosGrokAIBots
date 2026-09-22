"""supersmoother-dual-cross-v1 — Ehlers 2-pole SuperSmoother Dual Cross (NO High-Pass / != Roofing).

LOCKED ENCODE ORDER #5 (DUAL-SURVIVAL: SOL + BNB).
Thesis:
  Dual SuperSmoother (2-pole IIR) crossover provides a low-lag, smooth trend-following pair.
  CRITICAL: Strictly NOT Roofing filter (Roofing = HighPass + SuperSmoother oscillator; stage2 excluded).
  This is pure 2-pole SuperSmoother directly on close prices (no high-pass stage).
  Pairs: (8, 16), (10, 30), (12, 24) — prefer (10, 30) first.
  Optional Brief-2 atrPct rank gate (lo >= 25) to avoid BNB low-vol chop while keeping lengths identical.

Formula:
  theta = sqrt(2) * pi / L
  a1 = exp(-theta)
  b1 = 2 * a1 * cos(theta)
  c2 = b1, c3 = - a1^2, c1 = 1 - c2 - c3
  filt[t] = c1 * (price[t] + price[t-1]) / 2 + c2 * filt[t-1] + c3 * filt[t-2]

Mode A (primary):
  fast = SS(close, Lf), slow = SS(close, Ls)
  Long: ta.crossover(fast, slow)

Mode B (secondary):
  price x SS(close, Ls)

Optional regime gate:
  Allow entry only if percentrank(100*ATR(14)/close, 100) >= rank_lo (default 25.0)

Exit:
  Opposite cross; ATR trail stop.

Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, percent_rank, supersmoother

STRATEGY_ID = "supersmoother-dual-cross-v1"


@dataclass(frozen=True)
class SuperSmootherParams:
    mode: str = "mode_a"  # "mode_a" (dual SS) | "mode_b" (price x SS)
    fast_len: int = 10
    slow_len: int = 30
    atr_regime_gate: bool = False  # optional rank gate
    rank_lo: float = 25.0
    rank_window: int = 100
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: SuperSmootherParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden (prefer 1H+)"
    return True, "PASS"


def validate_bnb_smoke(params: SuperSmootherParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    # Smoke requires that lengths are not retuned per coin (must be one of the locked pairs)
    valid_pairs = {(8, 16), (10, 30), (12, 24)}
    if (params.fast_len, params.slow_len) not in valid_pairs:
        return False, f"bnb_smoke: Invalid pair {(params.fast_len, params.slow_len)}, must be in {valid_pairs}"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: SuperSmootherParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for supersmoother-dual-cross-v1."""
    params = params or SuperSmootherParams()
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

    if params.mode == "mode_a":
        fast_ss = supersmoother(closes, params.fast_len)
        slow_ss = supersmoother(closes, params.slow_len)
    else:
        fast_ss = [float(c) for c in closes]
        slow_ss = supersmoother(closes, params.slow_len)

    # Optional regime gate: atrPct rank
    rank_vals: list[float | None] = [None] * n
    if params.atr_regime_gate:
        atr_pct: list[float] = [0.0] * n
        for i in range(n):
            av = atr_vals[i]
            c = closes[i]
            if av is not None and c > 0:
                atr_pct[i] = 100.0 * av / c
        rank_vals = percent_rank(atr_pct, params.rank_window)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

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
            if crossunder(fast_ss, slow_ss, i):
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
        if not in_pos and i > 0 and slow_ss[i] is not None:
            regime_ok = True
            if params.atr_regime_gate:
                rk = rank_vals[i]
                regime_ok = rk is not None and rk >= params.rank_lo

            enter_signal = False
            if regime_ok and crossover(fast_ss, slow_ss, i):
                enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
