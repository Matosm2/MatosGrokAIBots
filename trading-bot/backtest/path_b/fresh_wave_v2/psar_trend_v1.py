"""psar-trend-v1 — Parabolic SAR trend flip (AF 0.02/0.02/0.2)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import parabolic_sar
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "psar-trend-v1"


@dataclass(frozen=True)
class PsarParams:
    af_start: float = 0.02
    af_step: float = 0.02
    af_max: float = 0.2


def compute_raw(
    bars: list[Bar],
    params: PsarParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: bar close flips above SAR (prior close ≤ SAR, close > SAR).
    Exit: bar close flips below SAR (prior close ≥ SAR, close < SAR).
    """
    params = params or PsarParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    sar = parabolic_sar(
        highs,
        lows,
        closes,
        af_start=params.af_start,
        af_step=params.af_step,
        af_max=params.af_max,
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(1, n):
        if sar[i] is None or sar[i - 1] is None:
            continue
        # Flip relative to SAR using close vs SAR on consecutive bars
        prev_le = closes[i - 1] <= sar[i - 1]  # type: ignore[operator]
        prev_ge = closes[i - 1] >= sar[i - 1]  # type: ignore[operator]
        curr_above = closes[i] > sar[i]  # type: ignore[operator]
        curr_below = closes[i] < sar[i]  # type: ignore[operator]
        raw_long[i] = prev_le and curr_above
        raw_exit[i] = prev_ge and curr_below
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: PsarParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
