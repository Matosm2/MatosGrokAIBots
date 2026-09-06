"""kama-er-trend-v1 — Daily KAMA + Efficiency Ratio trend (Path B research)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import efficiency_ratio, kama
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "kama-er-trend-v1"
INTERVAL = "1d"


@dataclass(frozen=True)
class KamaErParams:
    length: int = 10
    fast: int = 2
    slow: int = 30
    er_entry: float = 0.30
    er_exit: float = 0.20


def compute_raw(
    bars: list[Bar],
    params: KamaErParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry (flat): close > KAMA AND ER > 0.30
    Exit: close < KAMA OR ER < 0.20
    """
    params = params or KamaErParams()
    closes = [b.close for b in bars]
    k = kama(closes, params.length, params.fast, params.slow)
    er = efficiency_ratio(closes, params.length)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if k[i] is None or er[i] is None:
            continue
        raw_long[i] = closes[i] > k[i] and er[i] > params.er_entry
        raw_exit[i] = closes[i] < k[i] or er[i] < params.er_exit
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: KamaErParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
