"""twiggs-mf-v1 — Twiggs Money Flow (≠ CMF): Mode A channel+TMF>0 / Mode B zero-cross."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, twiggs_money_flow
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "twiggs-mf-v1"


@dataclass(frozen=True)
class TwiggsMfParams:
    period: int = 21
    mode: str = "A"  # A = channel break + TMF>0; B = TMF zero cross
    channel_n: int = 20


def compute_raw(
    bars: list[Bar],
    params: TwiggsMfParams | None = None,
) -> tuple[list[bool], list[bool]]:
    params = params or TwiggsMfParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    series = twiggs_money_flow(highs, lows, closes, volumes, params.period)
    n = len(bars)
    zero: list[float | None] = [0.0] * n
    raw_long = [False] * n
    raw_exit = [False] * n

    if params.mode.upper() == "B":
        for i in range(n):
            if crossover(series, zero, i):
                raw_long[i] = True
            if crossunder(series, zero, i):
                raw_exit[i] = True
        return raw_long, raw_exit

    # Mode A primary: close > prior N-bar high AND TMF > 0
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
    params: TwiggsMfParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
