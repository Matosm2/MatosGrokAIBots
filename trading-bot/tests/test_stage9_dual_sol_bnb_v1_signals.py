"""Unit tests for stage9-dual-sol-bnb-v1 indicators, signals, dual smokes, and retention rules."""

from __future__ import annotations

import math
from backtest.data import Bar
from backtest.indicators import (
    acceleration_bands,
    disparity_index,
    psychological_line,
    relative_momentum_index,
    wavetrend,
)
from backtest.path_b.stage9_dual_sol_bnb_v1.accel_bands_break_inside_exit_v1 import (
    AccelBandsParams,
    compute_signals as accel_signals,
    validate_bnb_smoke as validate_accel_bnb_smoke,
    validate_sol_smoke as validate_accel_sol_smoke,
)
from backtest.path_b.stage9_dual_sol_bnb_v1.disparity_sma_zero_cross_v1 import (
    DisparitySmaParams,
    compute_signals as di_signals,
    validate_bnb_smoke as validate_di_bnb_smoke,
    validate_sol_smoke as validate_di_sol_smoke,
)
from backtest.path_b.stage9_dual_sol_bnb_v1.psy_midline_fifty_cross_v1 import (
    PsyMidlineParams,
    compute_signals as psy_signals,
    validate_bnb_smoke as validate_psy_bnb_smoke,
    validate_sol_smoke as validate_psy_sol_smoke,
)
from backtest.path_b.stage9_dual_sol_bnb_v1.rmi_midline_fifty_cross_v1 import (
    RmiMidlineParams,
    compute_signals as rmi_signals,
    validate_bnb_smoke as validate_rmi_bnb_smoke,
    validate_sol_smoke as validate_rmi_sol_smoke,
)
from backtest.path_b.stage9_dual_sol_bnb_v1.wavetrend_wt1_wt2_cross_v1 import (
    WaveTrendParams,
    compute_signals as wt_signals,
    validate_bnb_smoke as validate_wt_bnb_smoke,
    validate_sol_smoke as validate_wt_sol_smoke,
)


def _make_dummy_bars(n: int = 150, trend: float = 0.5, v_reversal: bool = False) -> list[Bar]:
    """Generate synthetic bars for signal and indicator tests."""
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        if v_reversal:
            c = base - (i * 0.5) if i < 50 else base - 25.0 + (i - 50) * 1.0
        else:
            c = base + i * trend + math.sin(i / 5.0) * 3.0
        h = c + 1.5
        l = c - 1.5
        o = (h + l) / 2.0
        v = 100.0 + 10.0 * math.sin(i / 3.0)
        bars.append(
            Bar(
                open_time_ms=1700000000000 + i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=v,
                close_time_ms=1700000000000 + (i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_psychological_line_indicator():
    closes = [10.0, 11.0, 12.0, 11.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0]
    psy = psychological_line(closes, 12)
    assert len(psy) == len(closes)
    # At index 12, there are 12 steps. Count up closes:
    # 1: 10->11 (up), 2: 11->12 (up), 3: 12->11 (down), 4: 11->10 (down), 5: 10->11 (up)
    # 6: 11->12 (up), 7: 12->13 (up), 8: 13->14 (up), 9: 14->15 (up), 10: 15->16 (up)
    # 11: 16->17 (up), 12: 17->18 (up) -> 10 ups out of 12 = 100 * 10 / 12 = 83.333%
    assert psy[12] is not None
    assert abs(psy[12] - (10.0 / 12.0 * 100.0)) < 1e-4


def test_disparity_index_indicator():
    closes = [100.0] * 20
    di = disparity_index(closes, 10)
    assert di[9] is not None
    assert abs(di[9] - 0.0) < 1e-6
    closes_higher = closes + [110.0]
    di2 = disparity_index(closes_higher, 10)
    # SMA of last 10: 9*100 + 110 = 1010 / 10 = 101. DI = (110 - 101)/101 * 100 = 8.91089%
    assert di2[-1] is not None
    assert di2[-1] > 0.0


def test_wavetrend_indicator():
    bars = _make_dummy_bars(80)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    wt1, wt2 = wavetrend(highs, lows, closes, 10, 21, 4)
    assert len(wt1) == 80
    assert len(wt2) == 80
    assert wt1[-1] is not None
    assert wt2[-1] is not None


def test_relative_momentum_index_indicator():
    closes = [float(i) for i in range(50)]
    rmi = relative_momentum_index(closes, length=14, momentum=5)
    assert len(rmi) == 50
    # Consistently increasing series: mom > 0, d=0 -> RMI should be near 100
    assert rmi[-1] is not None
    assert abs(rmi[-1] - 100.0) < 1e-3


def test_acceleration_bands_indicator():
    bars = _make_dummy_bars(60)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    up, dn, mid = acceleration_bands(highs, lows, closes, length=20, k=4.0)
    assert len(up) == 60
    assert up[-1] is not None
    assert dn[-1] is not None
    assert mid[-1] is not None
    assert up[-1] > mid[-1] > dn[-1]


def test_psy_signals_and_smoke():
    bars = _make_dummy_bars(120, trend=0.5)
    params = PsyMidlineParams(mode="mode_a", length=12)
    buys, sells, stops = psy_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    sol_ok, _ = validate_psy_sol_smoke(params, "1h")
    assert sol_ok is True
    sol_bad, _ = validate_psy_sol_smoke(PsyMidlineParams(length=5), "15m")
    assert sol_bad is False


def test_di_signals_and_smoke():
    bars = _make_dummy_bars(120, trend=0.5)
    params = DisparitySmaParams(mode="mode_a", length=20)
    buys, sells, stops = di_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    sol_ok, _ = validate_di_sol_smoke(params, "1h")
    assert sol_ok is True
    sol_bad, _ = validate_di_sol_smoke(DisparitySmaParams(length=5), "15m")
    assert sol_bad is False


def test_wt_signals_and_smoke():
    bars = _make_dummy_bars(120, trend=0.5)
    params = WaveTrendParams(mode="mode_a", n1=10, n2=21, n3=4)
    buys, sells, stops = wt_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    sol_ok, _ = validate_wt_sol_smoke(params, "1h")
    assert sol_ok is True
    sol_bad, _ = validate_wt_sol_smoke(WaveTrendParams(n1=3), "15m")
    assert sol_bad is False


def test_rmi_signals_and_smoke():
    bars = _make_dummy_bars(120, trend=0.5)
    params = RmiMidlineParams(mode="mode_a", length=20, momentum=5)
    buys, sells, stops = rmi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    sol_ok, _ = validate_rmi_sol_smoke(params, "1h")
    assert sol_ok is True
    # m < 3 hard kill
    sol_bad_m, _ = validate_rmi_sol_smoke(RmiMidlineParams(length=14, momentum=1), "1h")
    assert sol_bad_m is False


def test_accel_signals_and_smoke():
    bars = _make_dummy_bars(120, trend=0.5)
    params = AccelBandsParams(mode="mode_a", length=20, k=4.0)
    buys, sells, stops = accel_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    sol_ok, _ = validate_accel_sol_smoke(params, "1h")
    assert sol_ok is True
    sol_bad, _ = validate_accel_sol_smoke(AccelBandsParams(length=5), "15m")
    assert sol_bad is False
