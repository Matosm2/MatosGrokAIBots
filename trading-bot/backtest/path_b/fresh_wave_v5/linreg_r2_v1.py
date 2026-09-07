"""linreg-r2-v1 — LinReg ±2σ channel with R² gate (Mode A breakout / Mode B fade)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import linreg_channel
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "linreg-r2-v1"


@dataclass(frozen=True)
class LinregR2Params:
    length: int = 20
    r2_gate: float = 0.7
    k_sigma: float = 2.0
    mode: str = "A"  # A = breakout +slope; B = fade at −2σ


def compute_raw(
    bars: list[Bar],
    params: LinregR2Params | None = None,
) -> tuple[list[bool], list[bool]]:
    params = params or LinregR2Params()
    closes = [b.close for b in bars]
    mid, upper, lower, slope, r2 = linreg_channel(
        closes, params.length, params.k_sigma
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    mode = params.mode.upper()
    for i in range(n):
        if (
            mid[i] is None
            or upper[i] is None
            or lower[i] is None
            or slope[i] is None
            or r2[i] is None
        ):
            continue
        if r2[i] < params.r2_gate:
            # Weak fit: force exit if somehow in; no new entries
            raw_exit[i] = True
            continue
        c = closes[i]
        if mode == "A":
            if c > upper[i] and slope[i] > 0.0:
                raw_long[i] = True
            if c <= mid[i] or c <= lower[i]:
                raw_exit[i] = True
        else:
            # Mode B fade: enter at/under −2σ; exit mid reclaim or opposite (+2σ)
            if c <= lower[i]:
                raw_long[i] = True
            if c >= mid[i] or c >= upper[i]:
                raw_exit[i] = True
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: LinregR2Params | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
