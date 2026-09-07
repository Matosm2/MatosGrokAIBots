"""rvi-signal-v1 — Relative Vigor Index(10) + Signal(4): crossover + RVI>0."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, relative_vigor_index
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "rvi-signal-v1"


@dataclass(frozen=True)
class RviSignalParams:
    length: int = 10
    signal_length: int = 4
    require_rvi_positive: bool = True


def compute_raw(
    bars: list[Bar],
    params: RviSignalParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(RVI, Signal) AND (RVI > 0 if require_rvi_positive).
    Exit: crossunder(RVI, Signal) OR RVI < 0.
    """
    params = params or RviSignalParams()
    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    rvi, sig = relative_vigor_index(
        opens, highs, lows, closes, params.length, params.signal_length
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if crossover(rvi, sig, i):
            rv = rvi[i]
            if rv is None:
                continue
            if (not params.require_rvi_positive) or rv > 0.0:
                raw_long[i] = True
        if crossunder(rvi, sig, i):
            raw_exit[i] = True
        rv = rvi[i]
        if rv is not None and rv < 0.0:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: RviSignalParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
