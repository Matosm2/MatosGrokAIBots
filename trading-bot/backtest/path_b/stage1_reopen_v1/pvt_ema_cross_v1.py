"""pvt-ema-cross-v1 — Price Volume Trend x signal EMA.

Indicators:
  ta.pvt = cumsum(volume * (close - close[1]) / close[1])
  ta.ema(pvt, length)

Mode A: Long when PVT crosses above EMA(PVT).
Mode B: Mode A + ta.rising(pvt, 1) (i.e. pvt[i] > pvt[i-1]).
Exit: Opposite cross (PVT crosses below EMA(PVT)) or optional ATR stop.

≠ OBV twin; ≠ CMF; ≠ Chaikin Osc; ≠ RSI/SMA200 grafts.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ema, pvt

STRATEGY_ID = "pvt-ema-cross-v1"


@dataclass(frozen=True)
class PvtEmaParams:
    ema_len: int = 14
    mode: str = "mode_a"  # "mode_a" | "mode_b" (requires rising PVT on signal bar)
    atr_trail_mult: float = 0.0  # 0.0 = opposite cross only; >0 = ATR trail stop
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: PvtEmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pvt-ema-cross-v1."""
    params = params or PvtEmaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    vols = [b.volume for b in bars]
    pvt_vals = pvt(closes, vols)
    pvt_float: list[float] = [float(v) for v in pvt_vals]
    pvt_sig = ema(pvt_float, params.ema_len)

    # Convert pvt_vals to list[float | None] for crossover/crossunder
    pvt_opt: list[float | None] = [float(v) for v in pvt_vals]

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if pvt_sig[i] is None:
            continue

        cross_up = crossover(pvt_opt, pvt_sig, i)
        cross_down = crossunder(pvt_opt, pvt_sig, i)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, bars[i].close)

            exit_hit = False
            if cross_down:
                exit_hit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if bars[i].close < stop_level:
                    exit_hit = True

            if exit_hit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if cross_up:
            cond = True
            if params.mode.lower() == "mode_b":
                cond = i > 0 and pvt_vals[i] > pvt_vals[i - 1]
            if cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = bars[i].close
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = bars[i].close - atr_vals[i] * params.atr_trail_mult
                    stops[i] = stop_level
                else:
                    stop_level = None

    return buys, sells, stops
