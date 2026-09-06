"""obv-ema-trend-v1 — OBV×EMA20 crossover with close > EMA50 filter."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, ema, obv
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "obv-ema-trend-v1"


@dataclass(frozen=True)
class ObvEmaParams:
    obv_ema_len: int = 20
    price_ema_len: int = 50


def compute_raw(
    bars: list[Bar],
    params: ObvEmaParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry: OBV crosses above EMA20(OBV) AND close > EMA50(close).
    Exit: OBV crosses below EMA20(OBV).
    """
    params = params or ObvEmaParams()
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    obv_s = obv(closes, volumes)
    obv_ema = ema(obv_s, params.obv_ema_len)
    price_ema = ema(closes, params.price_ema_len)
    # ema() expects list[float]; obv_s is list[float] — good.
    # For crossover we need list[float|None] for both sides:
    obv_line: list[float | None] = list(obv_s)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        if obv_ema[i] is None or price_ema[i] is None:
            continue
        up = crossover(obv_line, obv_ema, i)
        down = crossunder(obv_line, obv_ema, i)
        raw_long[i] = up and closes[i] > price_ema[i]  # type: ignore[operator]
        raw_exit[i] = down
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ObvEmaParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
