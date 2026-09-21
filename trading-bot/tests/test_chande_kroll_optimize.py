"""Unit tests for Stage-23 Chande Kroll Stop-flip indicators and strategy."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.path_b.stage23_chande_kroll_optimize_v1.indicators import (
    chande_kroll_stops,
    highest,
    lowest,
    percent_rank,
    true_range,
    wilder_atr,
)
from backtest.path_b.stage23_chande_kroll_optimize_v1.signals import (
    ChandeKrollParams,
    compute_chande_kroll_signals,
    run_chande_kroll_backtest,
)


def test_true_range():
    highs = [10.0, 12.0, 11.0]
    lows = [8.0, 9.0, 10.0]
    closes = [9.0, 11.0, 10.5]
    tr = true_range(highs, lows, closes)
    assert len(tr) == 3
    assert tr[0] == 2.0  # high - low
    # bar 1: max(12-9=3, abs(12-9)=3, abs(9-9)=0) -> 3.0
    assert tr[1] == 3.0
    # bar 2: max(11-10=1, abs(11-11)=0, abs(10-11)=1) -> 1.0
    assert tr[2] == 1.0


def test_wilder_atr_rma_warmup():
    highs = [10.0 + i for i in range(20)]
    lows = [8.0 + i for i in range(20)]
    closes = [9.0 + i for i in range(20)]
    # tr is constant 2.0 on each bar
    atr = wilder_atr(highs, lows, closes, 5)
    assert atr[:4] == [None, None, None, None]
    assert atr[4] == pytest.approx(2.0)
    assert atr[5] == pytest.approx(2.0)
    assert atr[-1] == pytest.approx(2.0)


def test_highest_and_lowest():
    vals: list[float | None] = [1.0, 3.0, 2.0, 5.0, 4.0]
    hh = highest(vals, 3)
    ll = lowest(vals, 3)
    assert hh[:2] == [None, None]
    assert hh[2] == 3.0  # max(1, 3, 2)
    assert hh[3] == 5.0  # max(3, 2, 5)
    assert hh[4] == 5.0  # max(2, 5, 4)

    assert ll[:2] == [None, None]
    assert ll[2] == 1.0  # min(1, 3, 2)
    assert ll[3] == 2.0  # min(3, 2, 5)
    assert ll[4] == 2.0  # min(2, 5, 4)


def test_chande_kroll_two_stage_stops():
    # Build 30 synthetic bars
    n = 30
    p = 5
    x = 1.0
    q = 4
    highs = [100.0 + i for i in range(n)]
    lows = [95.0 + i for i in range(n)]
    closes = [98.0 + i for i in range(n)]

    stops = chande_kroll_stops(highs, lows, closes, p=p, x=x, q=q)
    # Stage 1: highStop and lowStop are valid from index p-1 = 4
    assert stops.high_stop[:4] == [None, None, None, None]
    assert stops.high_stop[4] is not None
    assert stops.low_stop[4] is not None

    # Stage 2: stopShort and stopLong require q bars of stage 1 stops
    # Valid from index (p-1) + (q-1) = 4 + 3 = 7
    assert stops.stop_short[:7] == [None] * 7
    assert stops.stop_short[7] is not None
    assert stops.stop_long[7] is not None

    # Verify highStop = highest(high, p) - x * atr
    # At index 4: highs 0..4 are 100..104, highest=104, tr=5.0, atr=5.0
    # highStop = 104 - 1.0 * 5.0 = 99.0
    # lowStop = lowest(95..99) + 5.0 = 95 + 5.0 = 100.0
    assert stops.high_stop[4] == pytest.approx(99.0)
    assert stops.low_stop[4] == pytest.approx(100.0)


def test_percent_rank():
    # Increasing series: each element is the maximum of all previous
    vals: list[float | None] = [float(i) for i in range(15)]
    pr = percent_rank(vals, 5)
    assert pr[:5] == [None] * 5
    # For strictly increasing sequence, current value is >= all in window of 6 elements -> 100%
    assert pr[5] == pytest.approx(100.0)
    assert pr[10] == pytest.approx(100.0)


def test_chande_kroll_mode_a_signals():
    # Create a series that drops then rallies sharply then drops
    bars: list[Bar] = []
    base_price = 100.0
    ms = 1700000000000
    for i in range(60):
        if i < 25:
            base_price -= 0.5
        elif i < 45:
            base_price += 1.5
        else:
            base_price -= 1.0
        h = base_price + 0.5
        l = base_price - 0.5
        c = base_price
        o = base_price - 0.1
        bars.append(
            Bar(
                open_time_ms=ms + i * 3600 * 1000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=100.0,
                close_time_ms=ms + (i + 1) * 3600 * 1000 - 1,
            )
        )

    params = ChandeKrollParams(p=5, x=1.0, q=4, mode="A")
    sig = compute_chande_kroll_signals(bars, params)
    assert len(sig.buys) == len(bars)
    assert len(sig.sells) == len(bars)
    # Rally should trigger a buy
    assert any(sig.buys), "Expected at least one buy signal during rally"
    # End drop should trigger a sell
    assert any(sig.sells), "Expected at least one sell signal during decline"

    res = run_chande_kroll_backtest(
        "BTCUSDT",
        bars,
        params=params,
        initial_equity=10_000.0,
        buy_qty_pct=100.0,
    )
    assert len(res.trades) >= 1
    assert res.final_equity > 0
