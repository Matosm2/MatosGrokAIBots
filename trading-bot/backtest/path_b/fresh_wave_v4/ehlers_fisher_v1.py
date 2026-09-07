"""ehlers-fisher-v1 — Ehlers Fisher Transform Fish×Trigger (len 10)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, fisher_transform
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "ehlers-fisher-v1"


@dataclass(frozen=True)
class EhlersFisherParams:
    length: int = 10


def compute_raw(
    bars: list[Bar],
    params: EhlersFisherParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(Fish, Trigger) AND prior Fish < 0.
    Exit: crossunder(Fish, Trigger).
    """
    params = params or EhlersFisherParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    fish, trigger = fisher_transform(highs, lows, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if fish[i] is None or trigger[i] is None:
            continue
        if crossover(fish, trigger, i) and fish[i - 1] is not None and fish[i - 1] < 0:
            raw_long[i] = True
        if crossunder(fish, trigger, i):
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: EhlersFisherParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
