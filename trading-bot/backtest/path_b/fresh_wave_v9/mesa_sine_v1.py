"""mesa-sine-v1 — Ehlers MESA Sine × LeadSine (DC=15, Advance=45). No Fisher/RSI."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, mesa_sine_wave
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "mesa-sine-v1"


@dataclass(frozen=True)
class MesaSineParams:
    dominant_cycle: int = 15
    advance_deg: float = 45.0


def compute_raw(
    bars: list[Bar],
    params: MesaSineParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(Sine, LeadSine).
    Exit: crossunder(Sine, LeadSine).
    Prefer 1h–4h; no Fisher / RSI / SMA200 grafts.
    """
    params = params or MesaSineParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit
    closes = [b.close for b in bars]
    sine, lead = mesa_sine_wave(closes, params.dominant_cycle, params.advance_deg)
    for i in range(n):
        if sine[i] is None or lead[i] is None:
            continue
        if crossover(sine, lead, i):
            raw_long[i] = True
        if crossunder(sine, lead, i):
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: MesaSineParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
