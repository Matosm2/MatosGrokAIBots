"""tsi-momentum-v1 — Blau TSI(25,13) / signal EMA(7) with zero bias."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, ema, tsi
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "tsi-momentum-v1"


@dataclass(frozen=True)
class TsiParams:
    long_length: int = 25
    short_length: int = 13
    signal_length: int = 7


def _ema_of_series(series: list[float | None], length: int) -> list[float | None]:
    """EMA over dense non-None values of an optional series."""
    n = len(series)
    out: list[float | None] = [None] * n
    dense: list[float] = []
    idx_map: list[int] = []
    for i, v in enumerate(series):
        if v is None:
            continue
        dense.append(v)
        idx_map.append(i)
    if len(dense) < length:
        return out
    smoothed = ema(dense, length)
    for j, i in enumerate(idx_map):
        out[i] = smoothed[j]
    return out


def compute_raw(
    bars: list[Bar],
    params: TsiParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(TSI, signal) AND TSI > 0.
    Exit: crossunder(TSI, signal) OR TSI < 0.
    """
    params = params or TsiParams()
    closes = [b.close for b in bars]
    series = tsi(closes, params.long_length, params.short_length)
    signal = _ema_of_series(series, params.signal_length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if series[i] is None or signal[i] is None:
            continue
        cross_up = crossover(series, signal, i)
        cross_dn = crossunder(series, signal, i)
        raw_long[i] = cross_up and series[i] > 0.0  # type: ignore[operator]
        raw_exit[i] = cross_dn or series[i] < 0.0  # type: ignore[operator]
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: TsiParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
