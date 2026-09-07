"""kst-pring-v1 — Pring KST + signal (Mode A zero-bias / Mode B pure cross)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, kst
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "kst-pring-v1"


@dataclass(frozen=True)
class KstPringParams:
    roc_lengths: tuple[int, int, int, int] = (10, 15, 20, 30)
    sma_lengths: tuple[int, int, int, int] = (10, 10, 10, 15)
    signal_length: int = 9
    mode: str = "A"  # A = KST>0 AND cross above signal; B = pure signal cross


def compute_raw(
    bars: list[Bar],
    params: KstPringParams | None = None,
) -> tuple[list[bool], list[bool]]:
    params = params or KstPringParams()
    closes = [b.close for b in bars]
    line, signal = kst(
        closes,
        params.roc_lengths,
        params.sma_lengths,
        params.signal_length,
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    mode = params.mode.upper()
    for i in range(n):
        if crossover(line, signal, i):
            if mode == "A":
                if line[i] is not None and line[i] > 0.0:
                    raw_long[i] = True
            else:
                raw_long[i] = True
        if crossunder(line, signal, i):
            raw_exit[i] = True
        elif line[i] is not None and line[i] < 0.0:
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: KstPringParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
