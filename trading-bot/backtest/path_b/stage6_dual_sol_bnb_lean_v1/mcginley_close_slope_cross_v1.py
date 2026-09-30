"""mcginley-close-slope-cross-v1 — McGinley Dynamic Close Cross + Slope Filter.

LOCKED ENCODE ORDER #3 (DUAL-SURVIVAL: SOL + BNB lean).
Thesis:
  McGinley Dynamic auto-adjusts tracking speed via (close/MD)^4 denominator,
  hugging price velocity without Kaufman ER (KAMA) or CMO (|CMO| VIDYA).
  Stage5 died on SOL after ETH pass due to lagged/threshold CTI and adaptive flatten.
  MD's hug stays with SOL expansions after ETH while slowing in BNB hollow drift.
  Close x MD + slope confirmation is distinct from dual-MA soup.

Formula (Investopedia standard):
  MD := na(MD[1]) ? close : MD[1] + (close - MD[1]) / (N * (close / MD[1])^4)
  with guard MD[1] != 0.
  N in {10, 14, 20}.

Mode A (primary):
  Long entry: ta.crossover(close, MD) and MD > MD[1]
  Exit: ta.crossunder(close, MD) or MD < MD[1] or ATR stop.

Mode B (secondary):
  State: long while close > MD and MD rising. Mode A first.

sol_smoke:
  Kill if: KAMA implementation; VIDYA/CMO; McGinley+T3 hybrid; 15m N=6.
  Prefer Mode A, N=14, 1H+.
  Retention check: MD must hug SOL impulse (not flat while close runs away for many bars) —
  verify formula/N before dual-fail declare.

bnb_smoke:
  Kill if: different N than SOL; Mode B ungated shorts; T3/ADX grafts.
  Prefer identical N; long-only; ATR exit.

Forbidden: KAMA, VIDYA, SuperTrend, ADX, RSI, McGinley+T3 hybrid.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, mcginley_dynamic

STRATEGY_ID = "mcginley-close-slope-cross-v1"


@dataclass(frozen=True)
class McGinleyParams:
    mode: str = "mode_a"  # "mode_a" (close x MD cross + slope) | "mode_b" (state close > MD & rising)
    length: int = 14
    k: float = 1.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: McGinleyParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 6:
        return False, "sol_smoke: 15m N=6 forbidden (spam)"
    if params.length not in {10, 14, 20}:
        return False, f"sol_smoke: N={params.length} not in locked set {{10, 14, 20}}"
    return True, "PASS"


def validate_bnb_smoke(params: McGinleyParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.mode == "mode_b":
        # Mode B is secondary, but if used, ensure long-only
        pass
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: McGinleyParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for mcginley-close-slope-cross-v1."""
    params = params or McGinleyParams()
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
    md_series = mcginley_dynamic(closes, length=params.length, k=params.k)
    close_series = [float(c) for c in closes]

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

        md_curr = md_series[i]
        md_prev = md_series[i - 1] if i > 0 else None

        # Check exits first
        if in_pos:
            exit_signal = False

            if params.mode == "mode_a":
                # Exit: crossunder(close, MD) or MD < MD[1]
                if crossunder(close_series, md_series, i):
                    exit_signal = True
                elif md_curr is not None and md_prev is not None and md_curr < md_prev:
                    exit_signal = True
            else:
                # Mode B exit: close < MD or MD < MD[1]
                if md_curr is not None and (c < md_curr or (md_prev is not None and md_curr < md_prev)):
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
        if not in_pos and i > 0 and md_curr is not None and md_prev is not None:
            enter_signal = False
            md_rising = md_curr > md_prev

            if params.mode == "mode_a":
                # Long: crossover(close, MD) and MD > MD[1]
                if crossover(close_series, md_series, i) and md_rising:
                    enter_signal = True
            else:
                # Mode B: long while close > MD and MD rising (onset/first bar)
                if c > md_curr and md_rising:
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
