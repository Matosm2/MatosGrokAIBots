"""Unit tests for fresh-wave-v4 signal logic (synthetic bars)."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import (
    coppock_curve,
    crossover,
    fisher_transform,
    roc,
    wma,
)
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v4.coppock_curve_v1 import (
    CoppockParams,
    compute_signals as coppock_signals,
)
from backtest.path_b.fresh_wave_v4.ehlers_fisher_v1 import (
    EhlersFisherParams,
    compute_signals as fisher_signals,
)
from backtest.path_b.fresh_wave_v4.session_orb_v1 import (
    SessionOrbParams,
    compute_signals as orb_signals,
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
                volume=vol,
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


def test_roc_and_wma_basics():
    vals = [float(i) for i in range(1, 21)]
    r = roc(vals, 5)
    assert r[4] is None
    assert r[5] is not None
    assert abs(r[5] - 100.0 * (6 / 1 - 1)) < 1e-9
    dense: list[float | None] = list(vals)
    w = wma(dense, 3)
    assert w[1] is None
    # WMA([1,2,3]) = (1*1+2*2+3*3)/(1+2+3) = 14/6
    assert abs(w[2] - 14.0 / 6.0) < 1e-9


def test_fisher_transform_produces_trigger_lag():
    closes = [100.0 + i * 0.5 for i in range(40)]
    bars = _bars_from_closes(closes)
    fish, trig = fisher_transform(
        [b.high for b in bars], [b.low for b in bars], 10
    )
    assert fish[9] is not None
    assert trig[9] is None  # needs prior fish
    assert trig[10] == fish[9]
    buys, sells = fisher_signals(bars, EhlersFisherParams())
    assert len(buys) == len(bars) == len(sells)
    _assert_no_pyramid(buys, sells)
    for i, b in enumerate(buys):
        if b:
            assert fish[i - 1] is not None and fish[i - 1] < 0


def test_coppock_curve_and_signals():
    # Decline then recovery so Coppock can trough-turn under zero
    closes = [200.0 - i for i in range(40)] + [160.0 + i * 0.8 for i in range(60)]
    bars = _bars_from_closes(closes)
    series = coppock_curve([b.close for b in bars], 14, 11, 10)
    assert any(x is not None for x in series)
    buys, sells = coppock_signals(bars, CoppockParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    res = run_long_only(
        "TEST", "coppock-curve-v1", bars, buys, sells, buy_qty_pct=100.0
    )
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_session_orb_one_trade_per_utc_day():
    # Build ~3 UTC days of 5m bars: flat OR then breakout above OR high
    step = 5 * 60_000
    # Align to a UTC midnight
    t0 = 1_704_067_200_000  # 2023-12-31 00:00:00 UTC
    bars: list[Bar] = []
    # Day 0: quiet range 100-101 during OR, then break to 105
    for d in range(3):
        day_start = t0 + d * 86_400_000
        for m in range(0, 24 * 60, 5):
            ts = day_start + m * 60_000
            if m < 30:
                o = h = 101.0
                lo = c = 100.0
                # vary slightly so ATR > 0
                h = 101.0 + (m % 3) * 0.01
                lo = 100.0 - (m % 3) * 0.01
                c = 100.5
                o = 100.5
            elif m == 30:
                # breakout close beyond OR high (~101)
                o = 101.0
                h = 106.0
                lo = 100.8
                c = 105.0
            elif m < 24 * 60 - 5:
                o = 105.0
                h = 106.0
                lo = 104.0
                c = 105.0
            else:
                # last bar of day
                o = 105.0
                h = 105.5
                lo = 104.5
                c = 105.0
            bars.append(
                Bar(
                    open_time_ms=ts,
                    open=o,
                    high=h,
                    low=lo,
                    close=c,
                    volume=1000.0,
                    close_time_ms=ts + step - 1,
                )
            )
    buys, sells, stops = orb_signals(bars, SessionOrbParams())
    assert len(buys) == len(bars) == len(sells) == len(stops)
    _assert_no_pyramid(buys, sells)
    # At most one buy per UTC day
    from collections import defaultdict

    by_day: dict[int, int] = defaultdict(int)
    for i, b in enumerate(buys):
        if b:
            day = (bars[i].open_time_ms // 86_400_000) * 86_400_000
            by_day[day] += 1
            assert stops[i] is not None
    assert by_day
    assert all(v == 1 for v in by_day.values())
    # Engine with stops
    res = run_long_only(
        "TEST",
        "session-orb-v1",
        bars,
        buys,
        sells,
        stop_prices=stops,
        buy_qty_pct=100.0,
    )
    assert len(res.trades) >= 1


def test_session_orb_skips_wide_or():
    step = 5 * 60_000
    t0 = 1_704_067_200_000
    bars: list[Bar] = []
    # Warm-up day with normal ranges so ATR is defined, then wide-OR day
    for d in range(2):
        day_start = t0 + d * 86_400_000
        for m in range(0, 24 * 60, 5):
            ts = day_start + m * 60_000
            if d == 0:
                c = 100.0
                bars.append(
                    Bar(
                        open_time_ms=ts,
                        open=c,
                        high=c + 0.5,
                        low=c - 0.5,
                        close=c,
                        volume=1000.0,
                        close_time_ms=ts + step - 1,
                    )
                )
            else:
                # Huge OR height on day 1
                if m < 30:
                    bars.append(
                        Bar(
                            open_time_ms=ts,
                            open=100.0,
                            high=200.0,
                            low=50.0,
                            close=100.0,
                            volume=1000.0,
                            close_time_ms=ts + step - 1,
                        )
                    )
                else:
                    bars.append(
                        Bar(
                            open_time_ms=ts,
                            open=100.0,
                            high=210.0,
                            low=90.0,
                            close=205.0,
                            volume=1000.0,
                            close_time_ms=ts + step - 1,
                        )
                    )
    buys, sells, _stops = orb_signals(bars, SessionOrbParams())
    day1 = t0 + 86_400_000
    day1_buys = [
        i
        for i, b in enumerate(buys)
        if b and (bars[i].open_time_ms // 86_400_000) * 86_400_000 == day1
    ]
    assert day1_buys == []


def test_crossover_helper():
    a: list[float | None] = [-1.0, 0.5]
    b: list[float | None] = [0.0, 0.0]
    assert crossover(a, b, 1) is True
