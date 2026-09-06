"""coppock-curve-v1 — dual-ROC + WMA trough turn / zero-cross (1d/2d only)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import coppock_curve, crossover, crossunder
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "coppock-curve-v1"


@dataclass(frozen=True)
class CoppockParams:
    roc_long: int = 14
    roc_short: int = 11
    wma_len: int = 10
    min_bars_below_zero: int = 10


def compute_raw(
    bars: list[Bar],
    params: CoppockParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: (a) Coppock < 0 and turns up after a trough
           (Coppock > Coppock[1] after Coppock[1] < Coppock[2] while Coppock < 0)
        OR (b) crossover(Coppock, 0) after ≥10 bars below 0.
    Exit: Coppock turns down while > 0 OR crossunder(Coppock, 0).
    """
    params = params or CoppockParams()
    closes = [b.close for b in bars]
    series = coppock_curve(
        closes, params.roc_long, params.roc_short, params.wma_len
    )
    n = len(bars)
    zero: list[float | None] = [0.0] * n
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        c = series[i]
        if c is None:
            continue
        c1 = series[i - 1] if i >= 1 else None
        c2 = series[i - 2] if i >= 2 else None

        trough_turn = (
            c1 is not None
            and c2 is not None
            and c < 0
            and c > c1
            and c1 < c2
        )
        zero_cross = False
        if crossover(series, zero, i):
            ok = True
            for k in range(1, params.min_bars_below_zero + 1):
                if i - k < 0 or series[i - k] is None or series[i - k] >= 0:
                    ok = False
                    break
            zero_cross = ok
        raw_long[i] = trough_turn or zero_cross

        turn_down = (
            c1 is not None
            and c2 is not None
            and c > 0
            and c < c1
            and c1 > c2
        )
        raw_exit[i] = turn_down or crossunder(series, zero, i)
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: CoppockParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
