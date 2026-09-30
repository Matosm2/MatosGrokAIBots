"""Unit tests for stage1-reopen-v1 signals and indicators."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import (
    accdist,
    accumulative_swing_index,
    atr,
    crossover,
    crossunder,
    pvt,
    swing_index,
)
from backtest.path_b.stage1_reopen_v1.accdist_sma_cross_v1 import (
    AccDistSmaParams,
    compute_signals as accdist_signals,
)
from backtest.path_b.stage1_reopen_v1.asi_dual_break_v1 import (
    AsiDualBreakParams,
    compute_signals as asi_signals,
)
from backtest.path_b.stage1_reopen_v1.classic_floor_pivots_utc_v1 import (
    ClassicFloorPivotsParams,
    compute_signals as pivot_signals,
    floor_pivots_from_hlc,
)
from backtest.path_b.stage1_reopen_v1.pdh_pdl_accept_break_v1 import (
    PdhPdlParams,
    compute_signals as pdh_pdl_signals,
)
from backtest.path_b.stage1_reopen_v1.pvt_ema_cross_v1 import (
    PvtEmaParams,
    compute_signals as pvt_signals,
)


def _make_dummy_bars(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 3_600_000,
    vol: float = 1000.0,
    t0: int = 1_704_067_200_000,  # 2024-01-01 00:00 UTC
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
                volume=vol + i * 10,
                close_time_ms=t0 + (i + 1) * step_ms - 1,
            )
        )
    return out


def test_classic_floor_pivots_math():
    # H=100, L=80, C=90
    # PP = (100 + 80 + 90)/3 = 90
    # R1 = 2*90 - 80 = 100
    # S1 = 2*90 - 100 = 80
    # R2 = 90 + (100 - 80) = 110
    # S2 = 90 - (100 - 80) = 70
    lv = floor_pivots_from_hlc(100.0, 80.0, 90.0)
    assert abs(lv.pp - 90.0) < 1e-6
    assert abs(lv.r1 - 100.0) < 1e-6
    assert abs(lv.s1 - 80.0) < 1e-6
    assert abs(lv.r2 - 110.0) < 1e-6
    assert abs(lv.s2 - 70.0) < 1e-6


def test_classic_floor_pivots_signals():
    # 2 days of 1h bars (48 bars)
    rows_day1 = [(100.0, 105.0, 95.0, 100.0)] * 24
    # Day 1 H=105, L=95, C=100 -> PP = 100, R1 = 105, S1 = 95, R2 = 110, S2 = 90
    # Day 2: test S1 bounce (Mode A)
    # Bar 25: dip below S1 (low=94) then close back above S1 (close=96)
    rows_day2 = [(100.0, 101.0, 94.0, 96.0)] + [(96.0, 102.0, 95.0, 101.0)] * 23
    bars = _make_dummy_bars(rows_day1 + rows_day2)
    buys, sells, stops = pivot_signals(bars, ClassicFloorPivotsParams(mode="mode_a"))
    assert any(buys)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)


def test_pdh_pdl_accept_break_signals():
    # Day 1: H=105, L=95, C=100
    rows_day1 = [(100.0, 105.0, 95.0, 100.0)] * 24
    # Day 2: Bar 0 close=102, Bar 1 close=106 (> PDH=105)
    rows_day2 = [(100.0, 103.0, 99.0, 102.0), (102.0, 107.0, 101.0, 106.0)] + [(106.0, 108.0, 104.0, 107.0)] * 22
    bars = _make_dummy_bars(rows_day1 + rows_day2)
    buys, sells, stops = pdh_pdl_signals(bars, PdhPdlParams(mode="mode_a"))
    assert buys[25] is True  # Bar 1 of day 2 breaks PDH


def test_pvt_calculation_and_signals():
    closes = [100.0, 105.0, 110.0, 108.0, 112.0]
    volumes = [10.0, 20.0, 15.0, 10.0, 25.0]
    pvt_vals = pvt(closes, volumes)
    assert len(pvt_vals) == 5
    assert pvt_vals[0] == 0.0
    # Day 1: 20 * (105 - 100)/100 = 1.0
    assert abs(pvt_vals[1] - 1.0) < 1e-6

    # Test signals
    rows = [(100.0 + i, 105.0 + i, 95.0 + i, 100.0 + i) for i in range(50)]
    bars = _make_dummy_bars(rows)
    buys, sells, stops = pvt_signals(bars, PvtEmaParams(ema_len=5))
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)


def test_accdist_calculation_and_signals():
    highs = [105.0, 110.0, 115.0]
    lows = [95.0, 100.0, 105.0]
    closes = [100.0, 110.0, 105.0]  # Mid, High, Low
    volumes = [100.0, 100.0, 100.0]
    adl = accdist(highs, lows, closes, volumes)
    assert len(adl) == 3
    # Bar 0: (100-95 - (105-100))/(105-95) = 0 -> adl=0
    assert abs(adl[0]) < 1e-6
    # Bar 1: close==high -> MFM = 1 -> adl = 100
    assert abs(adl[1] - 100.0) < 1e-6
    # Bar 2: close==low -> MFM = -1 -> adl = 100 - 100 = 0
    assert abs(adl[2] - 0.0) < 1e-6

    rows = [(100.0 + i, 105.0 + i, 95.0 + i, 100.0 + i) for i in range(50)]
    bars = _make_dummy_bars(rows)
    buys, sells, stops = accdist_signals(bars, AccDistSmaParams(sma_len=5))
    assert len(buys) == len(bars)


def test_swing_index_and_asi():
    opens = [100.0, 102.0, 105.0, 103.0]
    highs = [105.0, 107.0, 108.0, 106.0]
    lows = [98.0, 100.0, 102.0, 99.0]
    closes = [102.0, 105.0, 104.0, 101.0]
    limit_move = 5.0
    si = swing_index(opens, highs, lows, closes, limit_move)
    assert len(si) == 4
    assert si[0] == 0.0

    asi = accumulative_swing_index(opens, highs, lows, closes, limit_move)
    assert len(asi) == 4
    assert abs(asi[1] - si[1]) < 1e-6
    assert abs(asi[2] - (si[1] + si[2])) < 1e-6

    # Test signals
    rows = [(100.0 + i, 105.0 + i, 95.0 + i, 100.0 + i) for i in range(50)]
    bars = _make_dummy_bars(rows)
    buys, sells, stops = asi_signals(bars, AsiDualBreakParams(n=10, proxy_family="pct", pct_close=0.02))
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
