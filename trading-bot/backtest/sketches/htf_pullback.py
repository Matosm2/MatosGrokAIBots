"""htf-ema-pullback-wide-v1 — Daily bias + 4h pullback, wide ATR stop."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, ema
from backtest.sketches.engine import apply_position_gate


@dataclass(frozen=True)
class HtfPullbackParams:
    daily_ema_fast: int = 50
    daily_ema_slow: int = 200
    entry_ema_fast: int = 20
    entry_ema_slow: int = 50
    atr_len: int = 14
    atr_stop_mult: float = 3.0
    pullback_lookback: int = 5  # 4h bars


def _align_daily_bias(
    bars_4h: list[Bar],
    daily_bars: list[Bar],
    params: HtfPullbackParams,
) -> list[bool | None]:
    """
    For each 4h bar, bias from the last *fully closed* daily bar
    (daily.close_time_ms < 4h.open_time_ms) — no lookahead into the in-progress day.
    """
    d_closes = [b.close for b in daily_bars]
    d_ef = ema(d_closes, params.daily_ema_fast)
    d_es = ema(d_closes, params.daily_ema_slow)

    j = -1
    out: list[bool | None] = []
    for b in bars_4h:
        while j + 1 < len(daily_bars) and daily_bars[j + 1].close_time_ms < b.open_time_ms:
            j += 1
        if j < 0:
            out.append(None)
            continue
        ef, es = d_ef[j], d_es[j]
        if ef is None or es is None:
            out.append(None)
        else:
            out.append(ef > es)
    return out


def compute_raw(
    bars_4h: list[Bar],
    daily_bars: list[Bar],
    params: HtfPullbackParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    Documented interpretation (brief was thin):

    **Daily bias:** EMA50 > EMA200 on last fully closed daily bar.

    **4h entry (pullback reclaim):**
    - Bias bullish
    - Within last `pullback_lookback` 4h bars, low touched at or below EMA50
    - Close crosses back above EMA20
    - Close still >= EMA50

    **Stop ref:** close - 3 * ATR(14) on the entry bar (passed through for engine freeze)

    **Exit:** daily bias lost OR 4h close < EMA50 (stop handled in engine)
    """
    params = params or HtfPullbackParams()
    closes = [b.close for b in bars_4h]
    highs = [b.high for b in bars_4h]
    lows = [b.low for b in bars_4h]
    e20 = ema(closes, params.entry_ema_fast)
    e50 = ema(closes, params.entry_ema_slow)
    atr14 = atr(highs, lows, closes, params.atr_len)
    bias = _align_daily_bias(bars_4h, daily_bars, params)
    close_series: list[float | None] = list(closes)

    n = len(bars_4h)
    raw_long = [False] * n
    raw_exit = [False] * n
    entry_stop: list[float | None] = [None] * n

    for i in range(n):
        if e20[i] is None or e50[i] is None or atr14[i] is None or bias[i] is None:
            continue
        touched = False
        lo = max(0, i - params.pullback_lookback + 1)
        for k in range(lo, i + 1):
            if e50[k] is not None and lows[k] <= e50[k]:
                touched = True
                break
        reclaim = crossover(close_series, e20, i)
        raw_long[i] = (
            bool(bias[i])
            and touched
            and reclaim
            and closes[i] >= e50[i]
        )
        if raw_long[i]:
            entry_stop[i] = closes[i] - params.atr_stop_mult * atr14[i]

        bias_lost = bias[i] is False
        structure_break = closes[i] < e50[i]
        raw_exit[i] = bias_lost or structure_break

    return raw_long, raw_exit, entry_stop


def compute_signals(
    bars_4h: list[Bar],
    daily_bars: list[Bar],
    params: HtfPullbackParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    raw_long, raw_exit, entry_stop = compute_raw(bars_4h, daily_bars, params)
    buys, sells = apply_position_gate(raw_long, raw_exit)
    stops_series: list[float | None] = [None] * len(bars_4h)
    frozen: float | None = None
    in_pos = False
    for i in range(len(bars_4h)):
        if buys[i]:
            in_pos = True
            frozen = entry_stop[i]
            stops_series[i] = frozen
        elif in_pos:
            stops_series[i] = frozen
            if sells[i]:
                in_pos = False
                frozen = None
    return buys, sells, stops_series


STRATEGY_ID = "htf-ema-pullback-wide-v1"
ENTRY_INTERVAL = "4h"
BIAS_INTERVAL = "1d"
