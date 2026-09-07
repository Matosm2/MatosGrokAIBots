"""cmf-flow-v1 — Chaikin Money Flow zero-cross (A) / channel+CMF (B)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import cmf, crossover, crossunder
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "cmf-flow-v1"


@dataclass(frozen=True)
class CmfFlowParams:
    period: int = 21
    mode: str = "A"  # A = zero cross; B = channel break + CMF>0
    channel_n: int = 20
    min_abs_cmf: float = 0.0  # optional |CMF|>threshold on Mode A


def compute_raw(
    bars: list[Bar],
    params: CmfFlowParams | None = None,
) -> tuple[list[bool], list[bool]]:
    params = params or CmfFlowParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    series = cmf(highs, lows, closes, volumes, params.period)
    n = len(bars)
    zero: list[float | None] = [0.0] * n
    raw_long = [False] * n
    raw_exit = [False] * n

    if params.mode.upper() == "A":
        for i in range(n):
            if crossover(series, zero, i):
                v = series[i]
                if v is not None and abs(v) >= params.min_abs_cmf:
                    raw_long[i] = True
            if crossunder(series, zero, i):
                raw_exit[i] = True
        return raw_long, raw_exit

    # Mode B: close > prior N-bar high AND CMF > 0; exit close < prior N-bar low OR CMF < 0
    n_ch = params.channel_n
    for i in range(n):
        v = series[i]
        if v is None:
            continue
        if i >= n_ch:
            prior_high = max(highs[i - n_ch : i])
            prior_low = min(lows[i - n_ch : i])
            if closes[i] > prior_high and v > 0.0:
                raw_long[i] = True
            if closes[i] < prior_low or v < 0.0:
                raw_exit[i] = True
        elif v < 0.0:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: CmfFlowParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
