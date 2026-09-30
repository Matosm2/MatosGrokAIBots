"""ehlers-reverse-ema-trend-cycle-v1 — Ehlers Reverse EMA Trend×Cycle zero.

LOCKED ENCODE ORDER #4 (DUAL-SURVIVAL: SOL + BNB survival).
Thesis:
  Unused Ehlers causal reverse-EMA Wave (S&C Sep 2017): classic EMA minus scaled
  multi-stage reverse EMA cascade (Z-transform lag removal).
  Dual-alpha: slow Trend Wave (alpha approx 0.05) as regime sign, faster Cycle Wave
  (alpha approx 0.3) for timing crosses.
  Distinct from burned Laguerre, Roofing, CyberCycle, SuperSmoother, Decycler, ITrend, FRAMA/HMA/McGinley.
  Close-only oscillator -> identical (alpha_t, alpha_c) on SOL+BNB;
  Cycle crosses supply SOL 1H–4H density while Trend > 0 filters BNB hollow flips.

Formula (TASC Sep 2017):
  CC = 1.0 - alpha
  EMA = alpha * Close + CC * EMA[1]
  RE1 = CC * EMA + EMA[1]
  RE_k = (CC^(2^(k-1))) * RE_{k-1} + RE_{k-1}[1] for k=2..8
  Wave = EMA - alpha * RE8

Mode A (primary / article rules):
  trend = ReverseEMA(alpha_t)
  cycle = ReverseEMA(alpha_c)
  long: trend > 0 and ta.crossover(cycle, 0)
  exit: ta.crossunder(trend, 0) or ta.crossunder(cycle, 0) or ATR stop.
  (alpha_t, alpha_c) in {(0.05, 0.30), (0.08, 0.25), (0.05, 0.20)} with alpha_t < alpha_c.

Mode B (secondary denser):
  single Wave(alpha=0.1) zero-cross only — if Mode A under-fires SOL.

sol_smoke:
  Kill if: Laguerre/Roofing substitute; plain EMAxEMA labeled reverse; 15m alpha_c=0.5.
  Prefer Mode A (0.05, 0.30), 1H+.
  Retention check: Cycle crosses must still fire on SOL while Trend>0 after ETH.
  If Trend stuck <= 0 through SOL up-legs -> kill.

bnb_smoke:
  Kill if: different alpha than SOL; Mode B shorts ungated; SuperSmoother graft.
  Prefer identical alpha; long-only; ATR exit.

Forbidden: Laguerre, Roofing, SuperSmoother, Decycler, ITrend, FRAMA, HMA, McGinley, RSI.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_reverse_ema

STRATEGY_ID = "ehlers-reverse-ema-trend-cycle-v1"


@dataclass(frozen=True)
class ReverseEmaParams:
    mode: str = "mode_a"  # "mode_a" (trend > 0 & cycle cross > 0) | "mode_b" (single wave cross > 0)
    alpha_trend: float = 0.05
    alpha_cycle: float = 0.30
    alpha_single: float = 0.10
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: ReverseEmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.alpha_cycle >= 0.5:
        return False, "sol_smoke: 15m alpha_cycle>=0.5 forbidden (spam)"
    if params.mode == "mode_a":
        allowed_pairs = {(0.05, 0.30), (0.08, 0.25), (0.05, 0.20)}
        pair = (round(params.alpha_trend, 2), round(params.alpha_cycle, 2))
        if pair not in allowed_pairs:
            return False, f"sol_smoke: (alpha_t, alpha_c)={pair} not in locked set"
        if params.alpha_trend >= params.alpha_cycle:
            return False, "sol_smoke: alpha_trend must be strictly < alpha_cycle"
    return True, "PASS"


def validate_bnb_smoke(params: ReverseEmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.mode == "mode_a" and params.alpha_trend >= params.alpha_cycle:
        return False, "bnb_smoke: alpha_trend >= alpha_cycle invalid"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ReverseEmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-reverse-ema-trend-cycle-v1."""
    params = params or ReverseEmaParams()
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
        trend_vals = ehlers_reverse_ema(closes, params.alpha_trend)
        cycle_vals = ehlers_reverse_ema(closes, params.alpha_cycle)
    else:
        single_vals = ehlers_reverse_ema(closes, params.alpha_single)
        trend_vals = single_vals
        cycle_vals = single_vals

    zeros: list[float | None] = [0.0] * n

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
            if params.mode == "mode_a":
                # Exit when trend crosses under 0 or cycle crosses under 0
                if crossunder(trend_vals, zeros, i) or crossunder(cycle_vals, zeros, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                # Exit on cycle/wave crossunder 0
                if crossunder(cycle_vals, zeros, i):
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
        if not in_pos and i > 0:
            enter_signal = False
            t_val = trend_vals[i]
            if params.mode == "mode_a":
                # Long: trend > 0 and crossover(cycle, 0)
                if t_val is not None and t_val > 0.0 and crossover(cycle_vals, zeros, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Long: crossover(single, 0)
                if crossover(cycle_vals, zeros, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
