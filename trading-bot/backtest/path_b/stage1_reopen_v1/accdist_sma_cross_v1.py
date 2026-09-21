"""accdist-sma-cross-v1 — Accumulation/Distribution Line (ADL) x SMA signal.

Indicators:
  ta.accdist (ADL) = cumsum(MFM * volume)
  ta.sma(accdist, N)

Mode A: Long when ADL crosses above SMA(ADL, N).
Mode B (secondary): Divergence + Mode A (price lower low + ADL higher low then long cross).
Exit: Opposite cross (ADL crosses below SMA(ADL, N)) or optional ATR stop.

≠ Chaikin Osc (EMA3 - EMA10 of ADL); ≠ CMF; ≠ OBV; ≠ MFI.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import accdist, atr, crossover, crossunder, sma

STRATEGY_ID = "accdist-sma-cross-v1"


@dataclass(frozen=True)
class AccDistSmaParams:
    sma_len: int = 20  # N in {10, 20, 50, 65}
    mode: str = "mode_a"  # "mode_a" | "mode_b" (bullish divergence)
    atr_trail_mult: float = 0.0  # 0.0 = opposite cross only; >0 = ATR trail stop
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: AccDistSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for accdist-sma-cross-v1."""
    params = params or AccDistSmaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    adl_vals = accdist(highs, lows, closes, volumes)
    adl_float: list[float] = [float(v) for v in adl_vals]
    adl_sig = sma(adl_float, params.sma_len)

    adl_opt: list[float | None] = [float(v) for v in adl_vals]

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if adl_sig[i] is None:
            continue

        cross_up = crossover(adl_opt, adl_sig, i)
        cross_down = crossunder(adl_opt, adl_sig, i)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, closes[i])

            exit_hit = False
            if cross_down:
                exit_hit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if closes[i] < stop_level:
                    exit_hit = True

            if exit_hit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if cross_up:
            cond = True
            if params.mode.lower() == "mode_b":
                # Bullish divergence check over lookback window (e.g. 20 bars):
                # Price made a lower low while ADL made a higher low
                lb = min(i, 20)
                if lb >= 5:
                    mid_idx = i - lb // 2
                    p_min_prior = min(lows[i - lb : mid_idx])
                    p_min_recent = min(lows[mid_idx : i + 1])
                    adl_min_prior = min(adl_vals[i - lb : mid_idx])
                    adl_min_recent = min(adl_vals[mid_idx : i + 1])
                    cond = (p_min_recent < p_min_prior) and (adl_min_recent > adl_min_prior)
                else:
                    cond = False

            if cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = closes[i]
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = closes[i] - atr_vals[i] * params.atr_trail_mult
                    stops[i] = stop_level
                else:
                    stop_level = None

    return buys, sells, stops
