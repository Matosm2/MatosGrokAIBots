"""ichimoku-cloud-trend-v1 — classic Ichimoku 9/26/52 trend."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, ichimoku
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "ichimoku-cloud-trend-v1"


@dataclass(frozen=True)
class IchimokuParams:
    tenkan_len: int = 9
    kijun_len: int = 26
    senkou_b_len: int = 52
    displacement: int = 26


def compute_raw(
    bars: list[Bar],
    params: IchimokuParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: Tenkan crosses above Kijun AND close > cloud top.
    Exit: close < cloud bottom OR Tenkan crosses below Kijun.
    Cloud at bar i uses Senkou A/B computed `displacement` bars earlier (no lookahead).
    """
    params = params or IchimokuParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    tenkan, kijun, senkou_a, senkou_b, cloud_top = ichimoku(
        highs,
        lows,
        params.tenkan_len,
        params.kijun_len,
        params.senkou_b_len,
        params.displacement,
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        sa, sb = senkou_a[i], senkou_b[i]
        if sa is None or sb is None or tenkan[i] is None or kijun[i] is None:
            continue
        cloud_bottom = min(sa, sb)
        ct = cloud_top[i]
        assert ct is not None
        tk_up = crossover(tenkan, kijun, i)
        tk_down = crossunder(tenkan, kijun, i)
        raw_long[i] = tk_up and closes[i] > ct
        raw_exit[i] = closes[i] < cloud_bottom or tk_down
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: IchimokuParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
