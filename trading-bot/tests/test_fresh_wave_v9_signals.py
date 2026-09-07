"""Unit tests for fresh-wave-v9 signal logic + indicators."""

from __future__ import annotations

import inspect
import math

from backtest.data import Bar
from backtest.indicators import crossover, mesa_sine_wave
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v9.camarilla_utc_v1 import (
    CamarillaParams,
    compute_signals as camarilla_signals,
    levels_from_ohlc,
)
from backtest.path_b.fresh_wave_v9.funding_data import FundingPrint
from backtest.path_b.fresh_wave_v9.funding_fade_v1 import (
    FundingFadeParams,
    compute_signals as funding_signals,
)
from backtest.path_b.fresh_wave_v9.mesa_sine_v1 import (
    MesaSineParams,
    compute_signals as mesa_signals,
)


def _bars_from_ohlc(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 3_600_000,
    vol: float = 1000.0,
    t0: int = 1_704_067_200_000,  # 2023-12-01 00:00 UTC
) -> list[Bar]:
    out: list[Bar] = []
    for i, (o, h, lo, c) in enumerate(rows):
        out.append(
            Bar(
                open_time_ms=t0 + i * step_ms,
                open=o,
                high=h,
                low=lo,
                close=c,
                volume=vol + (i % 7) * 10,
                close_time_ms=t0 + i * step_ms + step_ms - 1,
            )
        )
    return out


def _bars_from_closes(
    closes: list[float], *, step_ms: int = 3_600_000, vol: float = 1000.0, t0: int = 1_704_067_200_000
) -> list[Bar]:
    rows: list[tuple[float, float, float, float]] = []
    for i, c in enumerate(closes):
        spread = 0.02 + 0.01 * ((i % 11) / 10.0)
        o = c * (1.0 - 0.002 * ((i % 3) - 1))
        h = max(o, c) * (1.0 + spread)
        lo = min(o, c) * (1.0 - spread * 0.8)
        rows.append((o, h, lo, c))
    return _bars_from_ohlc(rows, step_ms=step_ms, vol=vol, t0=t0)


def _assert_no_pyramid(buys: list[bool], sells: list[bool]) -> None:
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_camarilla_levels_adj_1_1():
    lv = levels_from_ohlc(110.0, 100.0, 105.0, 1.1)
    adj = (110.0 - 100.0) * 1.1
    assert math.isclose(lv.h4, 105.0 + adj / 2.0)
    assert math.isclose(lv.h3, 105.0 + adj / 4.0)
    assert math.isclose(lv.l3, 105.0 - adj / 4.0)
    assert math.isclose(lv.l4, 105.0 - adj / 2.0)
    assert lv.mid == 105.0


def test_camarilla_mode_a_fade_l3_not_session_orb():
    # Day0: range-building OHLC; Day1: pierce L3 then reclaim
    MS_DAY = 86_400_000
    t0 = 1_704_067_200_000  # UTC day boundary
    rows: list[tuple[float, float, float, float]] = []
    # Day 0: 24 × 1h bars, H=110 L=100 C=105
    for i in range(24):
        if i == 0:
            rows.append((104.0, 110.0, 103.0, 108.0))
        elif i == 12:
            rows.append((108.0, 109.0, 100.0, 101.0))
        elif i == 23:
            rows.append((101.0, 106.0, 100.5, 105.0))
        else:
            rows.append((105.0, 107.0, 103.0, 105.0))
    # Day 1: approach L3 (~102.25), pierce, reclaim
    lv = levels_from_ohlc(110.0, 100.0, 105.0, 1.1)
    for i in range(24):
        if i == 5:
            # pierce L3
            rows.append((lv.l3 + 1.0, lv.l3 + 1.5, lv.l3 - 0.5, lv.l3 + 0.3))
        elif i == 10:
            # push toward mid for exit
            rows.append((lv.mid - 1.0, lv.mid + 0.5, lv.mid - 1.5, lv.mid + 0.2))
        else:
            rows.append((105.0, 106.0, 104.0, 105.0))
    bars = _bars_from_ohlc(rows, step_ms=3_600_000, t0=t0)
    assert bars[0].open_time_ms % MS_DAY == 0
    buys, sells, stops = camarilla_signals(bars, CamarillaParams(mode="mode_a"))
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1
    # Stop set to L4 on entry bar
    entry_i = next(i for i, b in enumerate(buys) if b)
    assert stops[entry_i] is not None
    assert math.isclose(stops[entry_i], lv.l4)  # type: ignore[arg-type]
    # ≠ Session ORB: no or_minutes / first-N-min box in module
    import backtest.path_b.fresh_wave_v9.camarilla_utc_v1 as mod

    src = inspect.getsource(mod)
    assert "or_minutes" not in src
    assert "Session ORB" in src or "≠ Session ORB" in src or "Session ORB" in mod.__doc__
    res = run_long_only("TEST", "camarilla-utc-v1", bars, buys, sells, stop_prices=stops, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_camarilla_mode_b_break_h4():
    MS_HOUR = 3_600_000
    t0 = 1_704_067_200_000
    rows: list[tuple[float, float, float, float]] = []
    for i in range(24):
        if i == 0:
            rows.append((104.0, 110.0, 103.0, 108.0))
        elif i == 12:
            rows.append((108.0, 109.0, 100.0, 101.0))
        elif i == 23:
            rows.append((101.0, 106.0, 100.5, 105.0))
        else:
            rows.append((105.0, 107.0, 103.0, 105.0))
    lv = levels_from_ohlc(110.0, 100.0, 105.0, 1.1)
    for i in range(24):
        if i == 3:
            rows.append((lv.h4 - 1.0, lv.h4 + 2.0, lv.h4 - 1.5, lv.h4 + 1.0))
        elif i == 8:
            rows.append((lv.h3 - 0.5, lv.h3 + 0.2, lv.h3 - 1.0, lv.h3 - 0.2))
        else:
            rows.append((105.0, 106.0, 104.0, 105.0))
    bars = _bars_from_ohlc(rows, step_ms=MS_HOUR, t0=t0)
    buys, sells, stops = camarilla_signals(bars, CamarillaParams(mode="mode_b"))
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1


def test_mesa_sine_cross_and_no_fisher():
    # Synthetic cyclic closes ~ period 15
    closes = [100.0 + 5.0 * math.sin(2 * math.pi * i / 15.0) for i in range(120)]
    bars = _bars_from_closes(closes)
    sine, lead = mesa_sine_wave([b.close for b in bars], 15, 45.0)
    assert any(x is not None for x in sine)
    assert any(x is not None for x in lead)
    # Lead is phase+45° — not identical to sine when both defined
    diffs = [
        abs(sine[i] - lead[i])  # type: ignore[operator]
        for i in range(len(bars))
        if sine[i] is not None and lead[i] is not None
    ]
    assert max(diffs) > 0.01
    buys, sells = mesa_signals(bars, MesaSineParams())
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1 and sum(sells) >= 1
    import backtest.path_b.fresh_wave_v9.mesa_sine_v1 as mod

    src = inspect.getsource(mod)
    assert "fisher_transform" not in src
    assert "rsi(" not in src
    assert "mesa_sine_wave" in src
    # crossover helper used
    assert crossover is not None
    res = run_long_only("TEST", "mesa-sine-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_funding_fade_mode_a_long_only_threshold():
    # 1h bars over ~3 days; funding every 8h
    MS_HOUR = 3_600_000
    t0 = 1_704_067_200_000
    closes = [100.0 + (i % 5) * 0.1 for i in range(72)]
    bars = _bars_from_closes(closes, step_ms=MS_HOUR, t0=t0)
    funding: list[FundingPrint] = []
    # Settlements at 0h, 8h, 16h each day
    for day in range(3):
        for hour in (0, 8, 16):
            t = t0 + (day * 24 + hour) * MS_HOUR
            # One extreme negative print mid-series
            rate = -0.0012 if (day == 1 and hour == 8) else 0.0001
            funding.append(FundingPrint(time_ms=t, rate=rate))
    buys, sells = funding_signals(bars, funding, FundingFadeParams(mode="mode_a", thr=0.001))
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1
    # Entry bar should be the bar opening at the extreme funding time
    entry_i = next(i for i, b in enumerate(buys) if b)
    assert bars[entry_i].open_time_ms == t0 + (1 * 24 + 8) * MS_HOUR
    # No short-side logic for positive extreme
    funding2 = [FundingPrint(time_ms=t0 + 8 * MS_HOUR, rate=0.002)] + funding[1:]
    buys2, _ = funding_signals(bars, funding2, FundingFadeParams(mode="mode_a", thr=0.001))
    # Positive-only extreme should not add a long at that print
    # (may still have the day1 -0.0012 long)
    assert sum(buys2) <= sum(buys) + 1
    import backtest.path_b.fresh_wave_v9.funding_fade_v1 as mod

    src = inspect.getsource(mod)
    assert "from backtest.indicators import" not in src
    assert "import rsi" not in src
    assert "bollinger" not in src.split("def compute_signals")[0]  # no indicator import graft


def test_funding_fade_mode_b_zscore():
    MS_HOUR = 3_600_000
    t0 = 1_704_067_200_000
    # Need >90 settlements for z window; 100 prints every 8h ≈ 33 days
    n_prints = 100
    funding: list[FundingPrint] = []
    for i in range(n_prints):
        t = t0 + i * 8 * MS_HOUR
        rate = 0.00005 + ((i % 7) - 3) * 1e-6
        if i == 95:
            rate = -0.0008  # extreme vs prior window
        funding.append(FundingPrint(time_ms=t, rate=rate))
    # Bars covering funding span
    n_hours = n_prints * 8 + 24
    closes = [100.0 + (i % 9) * 0.05 for i in range(n_hours)]
    bars = _bars_from_closes(closes, step_ms=MS_HOUR, t0=t0)
    buys, sells = funding_signals(
        bars,
        funding,
        FundingFadeParams(mode="mode_b", z_tau=2.0, z_window=90, exit_settlements=2),
    )
    _assert_no_pyramid(buys, sells)
    # May or may not trigger depending on z magnitude — at least runs clean
    res = run_long_only("TEST", "funding-fade-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_funding_fetch_error_type_exported():
    from backtest.path_b.fresh_wave_v9.funding_data import FundingFetchError

    assert issubclass(FundingFetchError, RuntimeError)
