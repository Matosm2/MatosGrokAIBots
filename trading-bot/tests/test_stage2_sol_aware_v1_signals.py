"""Unit tests for stage2-sol-aware-v1 indicators and strategies."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    alma,
    cmo,
    crossover,
    crossunder,
    ehlers_cg,
    ehlers_roofing_filter,
)
from backtest.path_b.stage2_sol_aware_v1.alma_fast_slow_cross_v1 import (
    AlmaParams,
    compute_signals as alma_signals,
)
from backtest.path_b.stage2_sol_aware_v1.cmo_zero_cross_v1 import (
    CmoZeroCrossParams,
    compute_signals as cmo_signals,
)
from backtest.path_b.stage2_sol_aware_v1.ehlers_cg_osc_trigger_v1 import (
    EhlersCgParams,
    compute_signals as cg_signals,
)
from backtest.path_b.stage2_sol_aware_v1.ehlers_roofing_zero_cross_v1 import (
    EhlersRoofingParams,
    compute_signals as roofing_signals,
)
from backtest.path_b.stage2_sol_aware_v1.pwh_pwl_accept_break_v1 import (
    PwhPwlParams,
    compute_signals as pwh_pwl_signals,
)


def _make_dummy_bars(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 3_600_000,
    vol: float = 1000.0,
    t0: int = 1_704_067_200_000,  # 2024-01-01 00:00 UTC (Monday)
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


# ---------------------------------------------------------------------------
# Indicator Unit Tests
# ---------------------------------------------------------------------------


def test_alma_calculation():
    values = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]
    out = alma(values, length=5, offset=0.85, sigma=6.0)
    assert len(out) == 10
    # First 4 should be None
    assert out[0] is None
    assert out[3] is None
    assert out[4] is not None
    # Strictly increasing input should have ALMA near the recent values
    assert 13.0 < out[4] <= 14.0
    assert out[9] > out[4]


def test_cmo_calculation():
    # Constant values -> 0 delta -> CMO = 0
    flat = [100.0] * 30
    flat_cmo = cmo(flat, length=14)
    assert len(flat_cmo) == 30
    assert flat_cmo[14] == 0.0

    # Monotonically increasing -> Su > 0, Sd = 0 -> CMO = 100
    up = [float(100 + i) for i in range(30)]
    up_cmo = cmo(up, length=14)
    assert abs(up_cmo[14] - 100.0) < 1e-6

    # Monotonically decreasing -> Su = 0, Sd > 0 -> CMO = -100
    down = [float(100 - i) for i in range(30)]
    down_cmo = cmo(down, length=14)
    assert abs(down_cmo[14] - (-100.0)) < 1e-6


def test_ehlers_cg_osc():
    # CG formula with hl2
    prices = [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0]
    cg, trigger = ehlers_cg(prices, length=10)
    assert len(cg) == len(prices)
    assert len(trigger) == len(prices)
    assert cg[9] is not None
    assert trigger[10] == cg[9]


def test_ehlers_roofing_filter():
    # Sinusoidal input test
    prices = [100.0 + 10.0 * math.sin(i * 0.1) for i in range(200)]
    roof = ehlers_roofing_filter(prices, hp_period=48, ss_period=10)
    assert len(roof) == len(prices)
    # Warmup should be None until index >= 96
    assert roof[0] is None
    assert roof[100] is not None
    # Filter should oscillate around zero
    valid_vals = [v for v in roof if v is not None]
    assert any(v > 0 for v in valid_vals)
    assert any(v < 0 for v in valid_vals)


# ---------------------------------------------------------------------------
# Strategy Signal Tests
# ---------------------------------------------------------------------------


def test_pwh_pwl_accept_break_signals():
    # Week 1: 168 hours of 1h bars
    # Monday 00:00 to next Monday 00:00 = 168 hours
    rows_wk1 = [(100.0, 110.0, 90.0, 105.0)] * 168
    # Prior week High = 110.0, Low = 90.0

    # Week 2: First bar breaks above 110.0 (close = 112.0)
    rows_wk2 = [(105.0, 113.0, 104.0, 112.0)] + [(112.0, 114.0, 111.0, 113.0)] * 167
    bars = _make_dummy_bars(rows_wk1 + rows_wk2)

    buys, sells, stops = pwh_pwl_signals(bars, PwhPwlParams(mode="mode_a"))
    assert len(buys) == len(bars)
    assert buys[168] is True  # First bar of week 2 should trigger buy on break above PWH
    assert stops[168] == 110.0  # Stop level is broken PWH


def test_pwh_pwl_mode_b_retest_signals():
    # Week 1: H=110, L=90
    rows_wk1 = [(100.0, 110.0, 90.0, 105.0)] * 168

    # Week 2:
    # Bar 0: break above PWH (close = 112 > 110)
    # Bar 1: retest pullback (low = 109 <= 110, close = 111 >= 110) -> Mode B buy
    rows_wk2 = [
        (105.0, 113.0, 104.0, 112.0),
        (112.0, 112.5, 109.0, 111.0),
    ] + [(111.0, 115.0, 110.5, 114.0)] * 166

    bars = _make_dummy_bars(rows_wk1 + rows_wk2)
    buys, sells, stops = pwh_pwl_signals(bars, PwhPwlParams(mode="mode_b"))
    assert buys[168] is False  # Break bar does not buy in Mode B
    assert buys[169] is True   # Retest bar buys in Mode B


def test_ehlers_cg_signals():
    # Generate oscillating bars to trigger crossovers
    rows = []
    for i in range(100):
        val = 100.0 + 10.0 * math.sin(i * 0.2)
        rows.append((val - 1.0, val + 2.0, val - 2.0, val))
    bars = _make_dummy_bars(rows)

    buys, sells, stops = cg_signals(bars, EhlersCgParams(length=10, mode="mode_a"))
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys)


def test_alma_fast_slow_signals():
    # Oscillating bars to produce crossovers
    rows = []
    for i in range(120):
        val = 100.0 + 20.0 * math.sin(i * 0.1)
        rows.append((val - 1.0, val + 2.0, val - 2.0, val))
    bars = _make_dummy_bars(rows)

    buys, sells, stops = alma_signals(bars, AlmaParams(fast_len=9, slow_len=21, offset=0.85, sigma=6.0))
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys)


def test_cmo_zero_cross_signals():
    # Wave of bars to trigger zero crosses
    rows = []
    for i in range(100):
        val = 100.0 + 15.0 * math.sin(i * 0.15)
        rows.append((val - 1.0, val + 2.0, val - 2.0, val))
    bars = _make_dummy_bars(rows)

    # Mode A (zero cross)
    buys_a, sells_a, stops_a = cmo_signals(bars, CmoZeroCrossParams(length=14, mode="mode_a"))
    assert len(buys_a) == len(bars)
    assert any(buys_a)

    # Mode B (SMA(9) cross)
    buys_b, sells_b, stops_b = cmo_signals(bars, CmoZeroCrossParams(length=14, mode="mode_b"))
    assert len(buys_b) == len(bars)
    assert any(buys_b)


def test_ehlers_roofing_signals():
    rows = []
    for i in range(250):
        val = 100.0 + 20.0 * math.sin(i * 0.1)
        rows.append((val - 1.0, val + 2.0, val - 2.0, val))
    bars = _make_dummy_bars(rows)

    buys, sells, stops = roofing_signals(bars, EhlersRoofingParams(hp_period=48, ss_period=10))
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys)
