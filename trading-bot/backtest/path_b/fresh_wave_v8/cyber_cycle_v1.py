"""cyber-cycle-v1 — Ehlers Cyber Cycle × Trigger (α=0.07). No Fisher graft."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, cyber_cycle
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "cyber-cycle-v1"


@dataclass(frozen=True)
class CyberCycleParams:
    alpha: float = 0.07


def compute_raw(
    bars: list[Bar],
    params: CyberCycleParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(Cycle, Trigger).
    Exit: crossunder(Cycle, Trigger).
    Trigger = Cycle[1]. No Fisher / RSI grafts.
    """
    params = params or CyberCycleParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    cycle, trigger = cyber_cycle(highs, lows, params.alpha)
    for i in range(n):
        if cycle[i] is None or trigger[i] is None:
            continue
        if crossover(cycle, trigger, i):
            raw_long[i] = True
        if crossunder(cycle, trigger, i):
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: CyberCycleParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
