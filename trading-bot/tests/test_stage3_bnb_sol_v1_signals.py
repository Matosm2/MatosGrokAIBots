"""Unit tests for stage3-bnb-sol-v1 indicators and strategies."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    crossover,
    crossunder,
    ehlers_decycler_oscillator,
    ehlers_itrend_trigger,
    sma,
    t3,
    vwma,
)
from backtest.path_b.stage3_bnb_sol_v1.decycler_osc_fast_slow_v1 import (
    DecyclerOscParams,
    compute_signals as decycler_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.itrend_trigger_v1 import (
    ITrendParams,
    compute_signals as itrend_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.phh_phl_accept_break_v1 import (
    PhhPhlParams,
    compute_signals as phh_phl_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.t3_dual_cross_v1 import (
    T3Params,
    compute_signals as t3_signals,
)
from backtest.path_b.stage3_bnb_sol_v1.vwma_sma_cross_v1 import (
    VwmaSmaParams,
    compute_signals as vwma_sma_signals,
)


def _make_dummy_bars(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 900_000,  # 15m step
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


def test_vwma_calculation():
    closes = [10.0, 20.0, 30.0, 40.0, 50.0]
    volumes = [100.0, 100.0, 100.0, 100.0, 100.0]
    # Equal volumes -> VWMA equals SMA
    out = vwma(closes, volumes, length=3)
    assert out[0] is None
    assert out[1] is None
    assert out[2] == (10.0 + 20.0 + 30.0) / 3.0
    assert out[3] == (20.0 + 30.0 + 40.0) / 3.0
    assert out[4] == (30.0 + 40.0 + 50.0) / 3.0

    # Unequal volumes -> volume weighting shifts towards high volume price
    v_skew = [1.0, 1.0, 100.0]
    out_skew = vwma(closes[:3], v_skew, length=3)
    expected = (10.0 * 1.0 + 20.0 * 1.0 + 30.0 * 100.0) / 102.0
    assert abs(out_skew[2] - expected) < 1e-6


def test_t3_calculation():
    # Constant input should produce constant output
    values = [50.0] * 50
    out = t3(values, length=5, v_factor=0.7)
    valid = [x for x in out if x is not None]
    assert len(valid) > 0
    for v in valid:
        assert abs(v - 50.0) < 1e-5

    # Ascending values should produce monotonic T3
    asc = [float(i) for i in range(100)]
    out_asc = t3(asc, length=5, v_factor=0.7)
    valid_asc = [x for x in out_asc if x is not None]
    assert len(valid_asc) > 10
    for i in range(1, len(valid_asc)):
        assert valid_asc[i] > valid_asc[i - 1]


def test_ehlers_decycler_oscillator():
    # Flat price input produces zero oscillation
    flat = [100.0] * 60
    out = ehlers_decycler_oscillator(flat, hp_period=20, k=1.0)
    assert len(out) == 60
    # Decycler oscillation of a flat line is 0.0
    for v in out[10:]:
        assert abs(v) < 1e-4

    # Sinusoid produces oscillating values
    sine = [100.0 + 10.0 * math.sin(2 * math.pi * i / 20) for i in range(100)]
    out_sine = ehlers_decycler_oscillator(sine, hp_period=20, k=1.0)
    assert any(v > 0.05 for v in out_sine[20:])
    assert any(v < -0.05 for v in out_sine[20:])


def test_ehlers_itrend_trigger():
    highs = [105.0] * 30
    lows = [95.0] * 30
    itrend, trigger = ehlers_itrend_trigger(highs, lows, alpha=0.07)
    assert len(itrend) == 30
    assert len(trigger) == 30
    # Price hl2 is 100.0
    for i in range(7, 30):
        assert abs(itrend[i] - 100.0) < 1e-4
        assert abs(trigger[i] - 100.0) < 1e-4

    # Stepping trend: Trigger should lead ITrend
    step_highs = [100.0 + i * 2.0 for i in range(40)]
    step_lows = [90.0 + i * 2.0 for i in range(40)]
    itrend_s, trigger_s = ehlers_itrend_trigger(step_highs, step_lows, alpha=0.07)
    for i in range(15, 40):
        assert trigger_s[i] > itrend_s[i]


# ---------------------------------------------------------------------------
# Strategy Signal Unit Tests
# ---------------------------------------------------------------------------


def test_vwma_sma_cross_signals():
    # Construct bars with a clear crossover
    rows = []
    # 20 flat bars at 100
    for _ in range(20):
        rows.append((100.0, 101.0, 99.0, 100.0))
    # 10 rising bars with heavy volume
    for i in range(1, 11):
        rows.append((100.0 + i * 2, 102.0 + i * 2, 99.0 + i * 2, 101.0 + i * 2))
    # 10 falling bars
    for i in range(1, 11):
        rows.append((120.0 - i * 3, 121.0 - i * 3, 118.0 - i * 3, 119.0 - i * 3))

    bars = _make_dummy_bars(rows)
    params = VwmaSmaParams(vwma_len=10, sma_len=10, mode="mode_a")
    buys, sells, stops = vwma_sma_signals(bars, params)
    assert any(buys), "Expected at least one buy signal on upward move"
    assert any(sells), "Expected at least one sell signal on downward move"


def test_phh_phl_accept_break_signals():
    # 4 bars per hour (15m step):
    # Hour 0 (bars 0..3): High=105, Low=95, Close=100
    # Hour 1 (bars 4..7): bar 4 breaks above 105 -> close=108 -> Mode A buy!
    rows = [
        (100.0, 102.0, 98.0, 101.0),
        (101.0, 105.0, 99.0, 100.0),  # High=105
        (100.0, 103.0, 95.0, 98.0),   # Low=95
        (98.0, 101.0, 97.0, 100.0),
        # Hour 1 start: bar 4 breaks above PHH (105)
        (100.0, 109.0, 100.0, 108.0), # close > 105
        (108.0, 110.0, 107.0, 109.0),
        (109.0, 109.0, 102.0, 103.0), # falls back below PHH (close < 105) -> exit!
        (103.0, 104.0, 100.0, 101.0),
    ]
    bars = _make_dummy_bars(rows, step_ms=900_000)
    params = PhhPhlParams(mode="mode_a", rvol_k=0.0)
    buys, sells, stops = phh_phl_signals(bars, params)
    assert buys[4], "Bar 4 should trigger Mode A accept-break buy"
    assert sells[6], "Bar 6 should trigger exit on close < PHH"


def test_t3_dual_cross_signals():
    rows = []
    # Warmup flat (need >= 84 bars for slow_len=15 6-EMA cascade)
    for _ in range(100):
        rows.append((100.0, 101.0, 99.0, 100.0))
    # Upward swing
    for i in range(1, 30):
        rows.append((100.0 + i * 2, 102.0 + i * 2, 99.0 + i * 2, 101.0 + i * 2))
    # Downward swing
    for i in range(1, 30):
        rows.append((160.0 - i * 3, 161.0 - i * 3, 158.0 - i * 3, 159.0 - i * 3))

    bars = _make_dummy_bars(rows)
    params = T3Params(fast_len=5, slow_len=15, v_factor=0.7, mode="mode_a")
    buys, sells, stops = t3_signals(bars, params)
    assert any(buys), "Expected buy on T3 fast crossover slow"
    assert any(sells), "Expected sell on T3 fast crossunder slow"


def test_decycler_osc_signals():
    rows = []
    for _ in range(60):
        rows.append((100.0, 101.0, 99.0, 100.0))
    for i in range(40):
        p = 100.0 + 15.0 * math.sin(2 * math.pi * i / 20)
        rows.append((p, p + 1.0, p - 1.0, p))

    bars = _make_dummy_bars(rows)
    params = DecyclerOscParams(p_fast=40, p_slow=50, k_fast=1.2, k_slow=1.0, mode="mode_a")
    buys, sells, stops = decycler_signals(bars, params)
    assert any(buys), "Expected buy on Decycler Osc cross"


def test_itrend_trigger_signals():
    rows = []
    for _ in range(30):
        rows.append((100.0, 101.0, 99.0, 100.0))
    for i in range(1, 20):
        rows.append((100.0 + i * 3, 102.0 + i * 3, 99.0 + i * 3, 101.0 + i * 3))
    for i in range(1, 20):
        rows.append((160.0 - i * 4, 161.0 - i * 4, 158.0 - i * 4, 159.0 - i * 4))

    bars = _make_dummy_bars(rows)
    params = ITrendParams(alpha=0.07, mode="mode_a")
    buys, sells, stops = itrend_signals(bars, params)
    assert any(buys), "Expected buy on Trigger crossover ITrend"
    assert any(sells), "Expected sell on Trigger crossunder ITrend"
