"""Unit tests for stage29-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    cpr_range,
    historical_volatility_ratio,
    katsanos_stiffness,
    varadi_dvs,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.katsanos_stiffness_threshold_v1 import (
    KatsanosStiffnessParams,
    compute_signals as stiffness_signals,
    validate_bnb_smoke as validate_stiffness_bnb_smoke,
    validate_btc_smoke as validate_stiffness_btc_smoke,
    validate_eth_smoke as validate_stiffness_eth_smoke,
    validate_sol_smoke as validate_stiffness_sol_smoke,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.cpr_range_break_accept_v1 import (
    CprRangeParams,
    compute_signals as cpr_signals,
    validate_bnb_smoke as validate_cpr_bnb_smoke,
    validate_btc_smoke as validate_cpr_btc_smoke,
    validate_eth_smoke as validate_cpr_eth_smoke,
    validate_sol_smoke as validate_cpr_sol_smoke,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.varadi_dvs_stretch_midline_v1 import (
    VaradiDvsParams,
    compute_signals as dvs_signals,
    validate_bnb_smoke as validate_dvs_bnb_smoke,
    validate_btc_smoke as validate_dvs_btc_smoke,
    validate_eth_smoke as validate_dvs_eth_smoke,
    validate_sol_smoke as validate_dvs_sol_smoke,
)
from backtest.path_b.stage29_dual_sol_bnb_v1.historical_volatility_ratio_expand_dir_v1 import (
    HvrExpandDirParams,
    compute_signals as hvr_signals,
    validate_bnb_smoke as validate_hvr_bnb_smoke,
    validate_btc_smoke as validate_hvr_btc_smoke,
    validate_eth_smoke as validate_hvr_eth_smoke,
    validate_sol_smoke as validate_hvr_sol_smoke,
)


def _make_dummy_bars(n: int = 250, trend: float = 1.0) -> list[Bar]:
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        swing = 15.0 * math.sin(i * 2.0 * math.pi / 20.0)
        c = base + i * trend + swing
        h = c + 3.0
        l = c - 3.0
        o = c - 0.5
        vol = 1000.0 + 300.0 * math.cos(i * 2.0 * math.pi / 10.0)
        bars.append(
            Bar(
                open_time_ms=i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=max(50.0, vol),
                close_time_ms=(i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_katsanos_stiffness_indicator_and_signals():
    bars = _make_dummy_bars(220, trend=0.5)
    closes = [b.close for b in bars]

    stiffness, stif_raw, ma2 = katsanos_stiffness(closes, mab=100, period=60, nstd=0.2, sm=3)
    assert len(stiffness) == len(bars)
    assert len(stif_raw) == len(bars)
    assert len(ma2) == len(bars)
    valid_stif = [x for x in stiffness if x is not None]
    assert len(valid_stif) > 50

    # Smoke validation
    params = KatsanosStiffnessParams(mode="mode_a", mab=100, period=60, buy_thr=90.0, sell_thr=50.0)
    ok, msg = validate_stiffness_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_stiffness_eth_smoke(params, "1h")[0]
    assert validate_stiffness_sol_smoke(params, "1h")[0]
    assert validate_stiffness_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_stiffness_btc_smoke(params, "15m")[0]
    assert not validate_stiffness_btc_smoke(KatsanosStiffnessParams(mab=200), "1h")[0]
    assert not validate_stiffness_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = stiffness_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_cpr_range_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    tc, p_series, bc, width = cpr_range(highs, lows, closes, n=24)
    assert len(tc) == len(bars)
    assert len(p_series) == len(bars)
    assert len(bc) == len(bars)
    assert len(width) == len(bars)
    valid_tc = [x for x in tc if x is not None]
    assert len(valid_tc) > 100

    # Verify TC >= BC property
    for i in range(len(bars)):
        if tc[i] is not None and bc[i] is not None:
            assert tc[i] >= bc[i]

    # Smoke validation
    params = CprRangeParams(mode="mode_a", n=24)
    ok, msg = validate_cpr_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_cpr_eth_smoke(params, "1h")[0]
    assert validate_cpr_sol_smoke(params, "1h")[0]
    assert validate_cpr_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_cpr_btc_smoke(params, "15m")[0]
    assert not validate_cpr_btc_smoke(CprRangeParams(n=99), "1h")[0]
    assert not validate_cpr_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = cpr_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_varadi_dvs_indicator_and_signals():
    bars = _make_dummy_bars(200, trend=0.5)
    closes = [b.close for b in bars]

    dvs, raw = varadi_dvs(closes, sum_len=20, rank_len=100)
    assert len(dvs) == len(bars)
    assert len(raw) == len(bars)
    valid_dvs = [x for x in dvs if x is not None]
    assert len(valid_dvs) > 50

    # Values should be bounded in [0, 100]
    for v in valid_dvs:
        assert 0.0 <= v <= 100.0

    # Smoke validation
    params = VaradiDvsParams(mode="mode_a", sum_len=20, rank_len=100, mid=50.0)
    ok, msg = validate_dvs_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_dvs_eth_smoke(params, "1h")[0]
    assert validate_dvs_sol_smoke(params, "1h")[0]
    assert validate_dvs_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_dvs_btc_smoke(params, "15m")[0]
    assert not validate_dvs_btc_smoke(VaradiDvsParams(sum_len=5), "1h")[0]
    assert not validate_dvs_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = dvs_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_hvr_expand_dir_indicator_and_signals():
    bars = _make_dummy_bars(180, trend=0.5)
    closes = [b.close for b in bars]

    hvr, hvs, hvl = historical_volatility_ratio(closes, short_len=10, long_len=100)
    assert len(hvr) == len(bars)
    assert len(hvs) == len(bars)
    assert len(hvl) == len(bars)
    valid_hvr = [x for x in hvr if x is not None]
    assert len(valid_hvr) > 50

    # Smoke validation
    params = HvrExpandDirParams(mode="mode_a", short_len=10, long_len=100, expand_thr=0.5, dir_len=5)
    ok, msg = validate_hvr_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_hvr_eth_smoke(params, "1h")[0]
    assert validate_hvr_sol_smoke(params, "1h")[0]
    assert validate_hvr_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_hvr_btc_smoke(params, "15m")[0]
    assert not validate_hvr_btc_smoke(HvrExpandDirParams(short_len=20), "1h")[0]
    assert not validate_hvr_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = hvr_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
