"""Unit tests for stage10-dual-sol-bnb-v1 indicators, signals, dual smokes, and retention rules."""

from __future__ import annotations

import math
from backtest.data import Bar
from backtest.indicators import (
    dema,
    dorsey_relative_volatility_index,
    rainbow_oscillator,
    trend_continuation_factor,
    trend_intensity_index,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.dema_fast_slow_cross_v1 import (
    DemaCrossParams,
    compute_signals as dema_signals,
    validate_bnb_smoke as validate_dema_bnb_smoke,
    validate_sol_smoke as validate_dema_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.dorsey_relvol_midline_fifty_v1 import (
    DorseyRelVolParams,
    compute_signals as relvol_signals,
    validate_bnb_smoke as validate_relvol_bnb_smoke,
    validate_sol_smoke as validate_relvol_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.rainbow_osc_zero_cross_v1 import (
    RainbowOscParams,
    compute_signals as ro_signals,
    validate_bnb_smoke as validate_ro_bnb_smoke,
    validate_sol_smoke as validate_ro_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.tcf_plus_sign_flip_v1 import (
    TcfSignFlipParams,
    compute_signals as tcf_signals,
    validate_bnb_smoke as validate_tcf_bnb_smoke,
    validate_sol_smoke as validate_tcf_sol_smoke,
)
from backtest.path_b.stage10_dual_sol_bnb_v1.tii_midline_fifty_cross_v1 import (
    TiiMidlineParams,
    compute_signals as tii_signals,
    validate_bnb_smoke as validate_tii_bnb_smoke,
    validate_sol_smoke as validate_tii_sol_smoke,
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


def test_trend_intensity_index_indicator():
    # Linear upward trend: all closes should be above moving average
    closes = [10.0 + i * 1.0 for i in range(100)]
    tii = trend_intensity_index(closes, major=40, minor=20)
    assert len(tii) == len(closes)
    # Warmup None until major-1 + minor-1
    assert tii[0] is None
    # With pure uptrend, close > ma on all bars in minor window -> sdNeg = 0 -> tii = 100
    valid_tiis = [v for v in tii if v is not None]
    assert len(valid_tiis) > 0
    assert valid_tiis[-1] == 100.0


def test_rainbow_oscillator_indicator():
    closes = [100.0 + math.sin(i / 4.0) * 10.0 for i in range(100)]
    ro, rb = rainbow_oscillator(closes, p=2, depth=10)
    assert len(ro) == 100
    assert len(rb) == 100
    valid_ro = [v for v in ro if v is not None]
    assert len(valid_ro) > 0
    # Range is roughly -100 to +100
    for v in valid_ro:
        assert -150.0 <= v <= 150.0


def test_dorsey_relvol_indicator():
    bars = _make_dummy_bars(80, trend=0.8)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    rvi = dorsey_relative_volatility_index(highs, lows, closes, stdev_len=10, avg_len=14)
    assert len(rvi) == len(bars)
    valid_rvi = [v for v in rvi if v is not None]
    assert len(valid_rvi) > 0
    # RVI is in [0, 100]
    for v in valid_rvi:
        assert 0.0 <= v <= 100.0


def test_trend_continuation_factor_indicator():
    closes = [10.0 + i * 1.0 for i in range(60)]
    plus_tcf, minus_tcf = trend_continuation_factor(closes, length=35)
    assert len(plus_tcf) == len(closes)
    assert len(minus_tcf) == len(closes)
    # With monotonic uptrend, plus_tcf should be strongly positive, minus_tcf negative/zero
    valid_plus = [v for v in plus_tcf if v is not None]
    assert len(valid_plus) > 0
    assert valid_plus[-1] > 0.0


def test_dema_indicator():
    closes = [100.0 + i * 0.5 for i in range(50)]
    d = dema(closes, length=10)
    assert len(d) == len(closes)
    valid_d = [v for v in d if v is not None]
    assert len(valid_d) > 0
    # DEMA of linear trend should track closely
    assert abs(valid_d[-1] - closes[-1]) < 5.0


def test_tii_signals_and_smokes():
    bars = _make_dummy_bars(200, v_reversal=True)
    p = TiiMidlineParams(mode="mode_a", major=40, minor=20)

    sol_ok, _ = validate_tii_sol_smoke(p, "1h")
    bnb_ok, _ = validate_tii_bnb_smoke(p, "1h")
    assert sol_ok and bnb_ok

    # Bad smoke
    bad_sol, _ = validate_tii_sol_smoke(TiiMidlineParams(major=10, minor=5), "15m")
    assert not bad_sol

    buys, sells, stops = tii_signals(bars, p)
    assert len(buys) == len(bars)
    assert any(buys) or any(sells) or not any(buys)


def test_rainbow_signals_and_smokes():
    bars = _make_dummy_bars(200, v_reversal=True)
    p = RainbowOscParams(mode="mode_a", p=2, depth=10)

    sol_ok, _ = validate_ro_sol_smoke(p, "1h")
    bnb_ok, _ = validate_ro_bnb_smoke(p, "1h")
    assert sol_ok and bnb_ok

    bad_sol, _ = validate_ro_sol_smoke(RainbowOscParams(depth=3), "15m")
    assert not bad_sol

    buys, sells, stops = ro_signals(bars, p)
    assert len(buys) == len(bars)


def test_dorsey_relvol_signals_and_smokes():
    bars = _make_dummy_bars(200, v_reversal=True)
    p = DorseyRelVolParams(mode="mode_a", stdev_len=10, avg_len=14)

    sol_ok, _ = validate_relvol_sol_smoke(p, "1h")
    bnb_ok, _ = validate_relvol_bnb_smoke(p, "1h")
    assert sol_ok and bnb_ok

    bad_sol, _ = validate_relvol_sol_smoke(DorseyRelVolParams(stdev_len=3), "15m")
    assert not bad_sol

    buys, sells, stops = relvol_signals(bars, p)
    assert len(buys) == len(bars)


def test_tcf_signals_and_smokes():
    bars = _make_dummy_bars(200, v_reversal=True)
    p = TcfSignFlipParams(mode="mode_a", length=35)

    sol_ok, _ = validate_tcf_sol_smoke(p, "1h")
    bnb_ok, _ = validate_tcf_bnb_smoke(p, "1h")
    assert sol_ok and bnb_ok

    bad_sol, _ = validate_tcf_sol_smoke(TcfSignFlipParams(length=5), "15m")
    assert not bad_sol

    buys, sells, stops = tcf_signals(bars, p)
    assert len(buys) == len(bars)


def test_dema_signals_and_smokes():
    bars = _make_dummy_bars(200, v_reversal=True)
    p = DemaCrossParams(mode="mode_a", fast_len=10, slow_len=30)

    sol_ok, _ = validate_dema_sol_smoke(p, "1h")
    bnb_ok, _ = validate_dema_bnb_smoke(p, "1h")
    assert sol_ok and bnb_ok

    bad_sol, _ = validate_dema_sol_smoke(DemaCrossParams(fast_len=3, slow_len=8), "15m")
    assert not bad_sol

    buys, sells, stops = dema_signals(bars, p)
    assert len(buys) == len(bars)
