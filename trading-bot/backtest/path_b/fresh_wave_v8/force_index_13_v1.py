"""force-index-13-v1 — FI EMA(13) zero-cross alone. Forbidden: Triple Screen FI(2)/Elder Ray."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, ema, force_index
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "force-index-13-v1"


@dataclass(frozen=True)
class ForceIndex13Params:
    ema_length: int = 13


def _fi_ema(closes: list[float], volumes: list[float], length: int) -> list[float | None]:
    """EMA of Elder Force Index raw (ΔC×Vol), preserving bar alignment."""
    n = len(closes)
    raw = force_index(closes, volumes)
    dense: list[float] = []
    idx: list[int] = []
    for i, v in enumerate(raw):
        if v is None:
            continue
        dense.append(v)
        idx.append(i)
    out: list[float | None] = [None] * n
    if len(dense) < length:
        return out
    smoothed = ema(dense, length)
    for j, i in enumerate(idx):
        out[i] = smoothed[j]
    return out


def compute_raw(
    bars: list[Bar],
    params: ForceIndex13Params | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: crossover(FI_EMA13, 0).
    Exit: crossunder(FI_EMA13, 0).
    Standalone zero-cross — no Triple Screen tide, no FI(2), no Elder Ray.
    """
    params = params or ForceIndex13Params()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    fi = _fi_ema(closes, volumes, params.ema_length)
    zero: list[float | None] = [0.0] * n
    for i in range(n):
        if fi[i] is None:
            continue
        if crossover(fi, zero, i):
            raw_long[i] = True
        if crossunder(fi, zero, i):
            raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ForceIndex13Params | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
