"""Unit tests for stage22-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math
import pytest

from backtest.data import Bar
from backtest.indicators import (
    anchored_vwap_pivot_low,
    katsanos_vfi,
    percentile_channel,
    percentile_nearest_rank,
    percentrank,
    rolling_zscore,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.percentile_channel_break_v1 import (
    PercentileChannelParams,
    compute_signals as percentile_signals,
    validate_bnb_smoke as validate_percentile_bnb_smoke,
    validate_btc_smoke as validate_percentile_btc_smoke,
    validate_eth_smoke as validate_percentile_eth_smoke,
    validate_sol_smoke as validate_percentile_sol_smoke,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.zscore_threshold_hold_v1 import (
    ZscoreParams,
    compute_signals as zscore_signals,
    validate_bnb_smoke as validate_zscore_bnb_smoke,
    validate_btc_smoke as validate_zscore_btc_smoke,
    validate_eth_smoke as validate_zscore_eth_smoke,
    validate_sol_smoke as validate_zscore_sol_smoke,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.anchored_vwap_swing_flip_v1 import (
    AnchoredVwapParams,
    compute_signals as vwap_signals,
    validate_bnb_smoke as validate_vwap_bnb_smoke,
    validate_btc_smoke as validate_vwap_btc_smoke,
    validate_eth_smoke as validate_vwap_eth_smoke,
    validate_sol_smoke as validate_vwap_sol_smoke,
)
from backtest.path_b.stage22_dual_sol_bnb_v1.katsanos_vfi_zero_cross_v1 import (
    VfiParams,
    compute_signals as vfi_signals,
    validate_bnb_smoke as validate_vfi_bnb_smoke,
    validate_btc_smoke as validate_vfi_btc_smoke,
    validate_eth_smoke as validate_vfi_eth_smoke,
    validate_sol_smoke as validate_vfi_sol_smoke,
)


def _make_dummy_bars(n: int = 150, trend: float = 1.0) -> list[Bar]:
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


def test_percentile_channel_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    up, dn = percentile_channel(highs, lows, length=50, p_hi=90.0, p_lo=10.0)
    assert len(up) == len(bars)
    assert len(dn) == len(bars)
    valid_up = [x for x in up if x is not None]
    assert len(valid_up) > 60

    # Smoke validation
    params = PercentileChannelParams(mode="mode_a", length=50, p_hi=90.0, p_lo=10.0)
    ok, msg = validate_percentile_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_percentile_eth_smoke(params, "1h")[0]
    assert validate_percentile_sol_smoke(params, "1h")[0]
    assert validate_percentile_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_percentile_btc_smoke(params, "15m")[0]
    assert not validate_percentile_btc_smoke(PercentileChannelParams(length=30), "1h")[0]
    assert not validate_percentile_sol_smoke(PercentileChannelParams(length=10), "15m")[0]

    # Signals
    buys, sells, stops = percentile_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    # Never buy and sell on same bar
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_zscore_threshold_hold_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    closes = [b.close for b in bars]

    z = rolling_zscore(closes, length=20)
    assert len(z) == len(bars)
    valid_z = [x for x in z if x is not None]
    assert len(valid_z) > 90

    # Smoke validation
    params = ZscoreParams(mode="mode_a", length=20, thr=1.0, exit_thr=0.0)
    ok, msg = validate_zscore_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_zscore_eth_smoke(params, "1h")[0]
    assert validate_zscore_sol_smoke(params, "1h")[0]
    assert validate_zscore_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_zscore_btc_smoke(params, "15m")[0]
    assert not validate_zscore_btc_smoke(ZscoreParams(length=14), "1h")[0]
    assert not validate_zscore_sol_smoke(ZscoreParams(length=5), "15m")[0]

    # Signals
    buys, sells, stops = zscore_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_anchored_vwap_swing_flip_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    avwap, age = anchored_vwap_pivot_low(highs, lows, closes, volumes, pivot_left=5, pivot_right=5)
    assert len(avwap) == len(bars)
    assert len(age) == len(bars)

    # Smoke validation
    params = AnchoredVwapParams(mode="mode_a", pivot_l=5, pivot_r=5, min_age=0)
    ok, msg = validate_vwap_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vwap_eth_smoke(params, "1h")[0]
    assert validate_vwap_sol_smoke(params, "1h")[0]
    assert validate_vwap_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_vwap_btc_smoke(params, "15m")[0]
    assert not validate_vwap_btc_smoke(AnchoredVwapParams(pivot_l=3), "1h")[0]
    assert not validate_vwap_sol_smoke(AnchoredVwapParams(pivot_l=1), "15m")[0]

    # Signals
    buys, sells, stops = vwap_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_katsanos_vfi_zero_cross_indicator_and_signals():
    bars = _make_dummy_bars(140, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    vfi = katsanos_vfi(highs, lows, closes, volumes, period=80, coef=0.1, vcoef=2.5, smooth=3)
    assert len(vfi) == len(bars)
    valid_vfi = [x for x in vfi if x is not None]
    assert len(valid_vfi) > 40

    # Smoke validation
    params = VfiParams(mode="mode_a", period=80, coef=0.1, vcoef=2.5, smooth=3)
    ok, msg = validate_vfi_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vfi_eth_smoke(params, "1h")[0]
    assert validate_vfi_sol_smoke(params, "1h")[0]
    assert validate_vfi_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_vfi_btc_smoke(params, "15m")[0]
    assert not validate_vfi_btc_smoke(VfiParams(period=130), "1h")[0]
    assert not validate_vfi_sol_smoke(VfiParams(period=20), "15m")[0]

    # Signals
    buys, sells, stops = vfi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
