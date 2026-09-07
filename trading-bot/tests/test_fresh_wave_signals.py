"""Unit tests for fresh-wave-v1 signal logic (synthetic bars)."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import (
    connors_rsi,
    heikin_ashi,
    ichimoku,
    obv,
    percent_rank,
    streak_series,
)
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave.connors_rsi_mr_v1 import (
    ConnorsRsiParams,
    compute_signals as crsi_signals,
)
from backtest.path_b.fresh_wave.ha_streak_trend_v1 import (
    HaStreakParams,
    compute_signals as ha_signals,
)
from backtest.path_b.fresh_wave.ichimoku_cloud_trend_v1 import (
    IchimokuParams,
    compute_signals as ichi_signals,
)
from backtest.path_b.fresh_wave.nr7_breakout_v1 import (
    Nr7Params,
    compute_signals as nr7_signals,
)
from backtest.path_b.fresh_wave.obv_ema_trend_v1 import (
    ObvEmaParams,
    compute_signals as obv_signals,
)


def _bars_from_closes(
    closes: list[float], *, step_ms: int = 86_400_000, vol: float = 1000.0
) -> list[Bar]:
    out: list[Bar] = []
    t0 = 1_700_000_000_000
    for i, c in enumerate(closes):
        h = c * 1.01
        lo = c * 0.99
        out.append(
            Bar(
                open_time_ms=t0 + i * step_ms,
                open=c,
                high=h,
                low=lo,
                close=c,
                volume=vol * (1.5 if i % 17 == 0 else 1.0),
                close_time_ms=t0 + i * step_ms + step_ms - 1,
            )
        )
    return out


def _assert_no_pyramid(buys: list[bool], sells: list[bool]) -> None:
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_connors_rsi_warmup_and_bounds():
    closes = [100.0 + (i % 7) - 3 for i in range(150)]
    crsi = connors_rsi(closes, 3, 2, 100)
    assert all(c is None or 0.0 <= c <= 100.0 for c in crsi)
    assert crsi[120] is not None
    st = streak_series(closes)
    assert st[1] != 0 or closes[1] == closes[0]
    pr = percent_rank([float(i) for i in range(50)], 10)
    assert pr[9] == 100.0  # max in window ranks 100


def test_connors_rsi_mr_signals_and_max_hold():
    # build a dip then recovery so CRSI can go low then high
    closes = [100.0] * 110 + [100.0 - i for i in range(1, 15)] + [
        85.0 + i * 2 for i in range(20)
    ]
    bars = _bars_from_closes(closes)
    buys, sells = crsi_signals(bars, ConnorsRsiParams())
    assert len(buys) == len(bars) == len(sells)
    _assert_no_pyramid(buys, sells)
    # if any trade, hold never exceeds 5 bars
    entry = None
    for i, (b, s) in enumerate(zip(buys, sells)):
        if b:
            entry = i
        if s and entry is not None:
            assert i - entry <= 5
            entry = None


def test_nr7_breakout_shapes_and_stop():
    # mostly wide ranges then a tight bar then breakout up
    closes = [100.0 + (i % 3) for i in range(40)]
    bars = _bars_from_closes(closes)
    # force a narrow bar then expand
    i_nr = 30
    bars[i_nr] = Bar(
        open_time_ms=bars[i_nr].open_time_ms,
        open=100.0,
        high=100.05,
        low=99.95,
        close=100.0,
        volume=1000.0,
        close_time_ms=bars[i_nr].close_time_ms,
    )
    for j in range(i_nr + 1, min(i_nr + 5, len(bars))):
        c = 100.0 + (j - i_nr) * 2
        bars[j] = Bar(
            open_time_ms=bars[j].open_time_ms,
            open=c,
            high=c * 1.02,
            low=c * 0.99,
            close=c,
            volume=1000.0,
            close_time_ms=bars[j].close_time_ms,
        )
    buys, sells, stops = nr7_signals(bars, Nr7Params())
    assert len(buys) == len(sells) == len(stops) == len(bars)
    _assert_no_pyramid(buys, sells)
    if any(buys):
        idx = next(i for i, b in enumerate(buys) if b)
        assert stops[idx] is not None


def test_ichimoku_cloud_no_lookahead_displacement():
    closes = [100.0 + i * 0.3 for i in range(120)]
    bars = _bars_from_closes(closes)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    tenkan, kijun, sa, sb, ct = ichimoku(highs, lows, 9, 26, 52, 26)
    # cloud should be None until index >= 26 + enough for senkou b source
    assert sa[25] is None
    assert all(x is None for x in sa[:26])
    buys, sells = ichi_signals(bars, IchimokuParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)


def test_ha_streak_three_bulls():
    # steadily rising → HA bulls
    closes = [100.0 + i for i in range(30)]
    bars = _bars_from_closes(closes)
    # set open < close for raw bars to help HA bullishness
    for i, b in enumerate(bars):
        o = b.close - 0.5
        bars[i] = Bar(
            open_time_ms=b.open_time_ms,
            open=o,
            high=b.high,
            low=b.low,
            close=b.close,
            volume=b.volume,
            close_time_ms=b.close_time_ms,
        )
    ha_o, _, _, ha_c = heikin_ashi(
        [b.open for b in bars],
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
    )
    assert any(ha_c[i] > ha_o[i] for i in range(len(bars)))
    buys, sells = ha_signals(bars, HaStreakParams(bull_streak=3))
    assert sum(1 for b in buys if b) >= 1
    _assert_no_pyramid(buys, sells)
    res = run_long_only("TEST", "ha-streak-trend-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_obv_ema_cross_filter():
    closes = [100.0 + i * 0.5 for i in range(80)]
    bars = _bars_from_closes(closes, vol=1000.0)
    # boost volume on up days late in series
    for i in range(50, len(bars)):
        bars[i] = Bar(
            open_time_ms=bars[i].open_time_ms,
            open=bars[i].open,
            high=bars[i].high,
            low=bars[i].low,
            close=bars[i].close,
            volume=5000.0,
            close_time_ms=bars[i].close_time_ms,
        )
    o = obv([b.close for b in bars], [b.volume for b in bars])
    assert o[-1] > o[0]
    buys, sells = obv_signals(bars, ObvEmaParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
