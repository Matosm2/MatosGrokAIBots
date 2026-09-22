"""Unit tests for stage20-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    bw_mfi,
    demand_index,
    kalman_1d,
    ravi,
    vpci,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.vpci_zero_cross_v1 import (
    VpciParams,
    compute_signals as vpci_signals,
    validate_bnb_smoke as validate_vpci_bnb_smoke,
    validate_btc_smoke as validate_vpci_btc_smoke,
    validate_eth_smoke as validate_vpci_eth_smoke,
    validate_sol_smoke as validate_vpci_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.bw_mfi_green_fade_flip_v1 import (
    BwMfiParams,
    compute_signals as bw_mfi_signals,
    validate_bnb_smoke as validate_bw_mfi_bnb_smoke,
    validate_btc_smoke as validate_bw_mfi_btc_smoke,
    validate_eth_smoke as validate_bw_mfi_eth_smoke,
    validate_sol_smoke as validate_bw_mfi_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.demand_index_zero_v1 import (
    DemandIndexParams,
    compute_signals as demand_index_signals,
    validate_bnb_smoke as validate_demand_index_bnb_smoke,
    validate_btc_smoke as validate_demand_index_btc_smoke,
    validate_eth_smoke as validate_demand_index_eth_smoke,
    validate_sol_smoke as validate_demand_index_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.kalman_estimate_cross_v1 import (
    KalmanParams,
    compute_signals as kalman_signals,
    validate_bnb_smoke as validate_kalman_bnb_smoke,
    validate_btc_smoke as validate_kalman_btc_smoke,
    validate_eth_smoke as validate_kalman_eth_smoke,
    validate_sol_smoke as validate_kalman_sol_smoke,
)
from backtest.path_b.stage20_dual_sol_bnb_v1.ravi_threshold_dir_v1 import (
    RaviParams,
    compute_signals as ravi_signals,
    validate_bnb_smoke as validate_ravi_bnb_smoke,
    validate_btc_smoke as validate_ravi_btc_smoke,
    validate_eth_smoke as validate_ravi_eth_smoke,
    validate_sol_smoke as validate_ravi_sol_smoke,
)


def _make_dummy_bars(n: int = 120, trend: float = 1.0) -> list[Bar]:
    import math

    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        # Sine wave swing to ensure multiple crossovers and crossunders
        swing = 25.0 * math.sin(i * 2.0 * math.pi / 16.0)
        c = base + i * trend + swing
        h = c + 1.5 + (0.5 if i % 3 == 0 else 0.0)
        l = c - 1.5
        o = c - 0.5
        # Alternating volume to exercise volume indicators
        vol = 1000.0 + (500.0 if i % 2 == 0 else -200.0) + (i * 5.0)
        # Add varying high-low spread to trigger MFI movements
        spread = 2.0 + 1.5 * math.sin(i * 1.5)
        h = c + spread
        l = c - spread
        o = c - 0.5
        bars.append(
            Bar(
                open_time_ms=i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=max(10.0, vol),
                close_time_ms=(i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_vpci_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=0.8)
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    v = vpci(closes, volumes, short_len=5, long_len=20)
    assert len(v) == len(bars)
    # Check that after warm-up we have non-None values
    valid_vals = [x for x in v if x is not None]
    assert len(valid_vals) > 50

    # Smoke tests
    params = VpciParams(mode="mode_a", short_len=5, long_len=20)
    ok, msg = validate_vpci_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vpci_eth_smoke(params, "1h")[0]
    assert validate_vpci_sol_smoke(params, "1h")[0]
    assert validate_vpci_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_vpci_btc_smoke(params, "15m")[0]
    assert not validate_vpci_btc_smoke(VpciParams(short_len=3, long_len=20), "1h")[0]
    assert not validate_vpci_sol_smoke(VpciParams(short_len=2, long_len=20), "15m")[0]

    # Signals
    buys, sells, stops = vpci_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected at least one buy signal in oscillating series"
    assert any(sells), "Expected at least one sell signal in oscillating series"


def test_bw_mfi_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=0.8)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    mfi, green, fade, fake, squat = bw_mfi(highs, lows, closes, volumes)
    assert len(mfi) == len(bars)
    assert len(green) == len(bars)
    assert len(fade) == len(bars)
    assert any(green), "Expected at least one green bar"
    assert any(fade), "Expected at least one fade bar"

    # Smoke tests
    params = BwMfiParams(mode="mode_a", confirm_bars=1)
    ok, msg = validate_bw_mfi_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_bw_mfi_eth_smoke(params, "1h")[0]
    assert validate_bw_mfi_sol_smoke(params, "1h")[0]
    assert validate_bw_mfi_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_bw_mfi_btc_smoke(params, "15m")[0]
    assert not validate_bw_mfi_btc_smoke(BwMfiParams(confirm_bars=6), "1h")[0]
    assert not validate_bw_mfi_sol_smoke(BwMfiParams(confirm_bars=1), "15m")[0]

    # Signals
    buys, sells, stops = bw_mfi_signals(bars, params)
    assert any(buys), "Expected buys in bw-mfi"
    assert any(sells), "Expected sells in bw-mfi"


def test_demand_index_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=0.8)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    di = demand_index(highs, lows, closes, volumes, n_bs=10, n_smooth=10)
    assert len(di) == len(bars)
    valid_vals = [x for x in di if x is not None]
    assert len(valid_vals) > 50

    # Smoke tests
    params = DemandIndexParams(mode="mode_a", n_bs=10, n_smooth=10)
    ok, msg = validate_demand_index_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_demand_index_eth_smoke(params, "1h")[0]
    assert validate_demand_index_sol_smoke(params, "1h")[0]
    assert validate_demand_index_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_demand_index_btc_smoke(params, "15m")[0]
    assert not validate_demand_index_btc_smoke(DemandIndexParams(n_bs=5, n_smooth=10), "1h")[0]
    assert not validate_demand_index_sol_smoke(DemandIndexParams(n_bs=3, n_smooth=10), "15m")[0]

    # Signals
    buys, sells, stops = demand_index_signals(bars, params)
    assert any(buys), "Expected buys in demand-index"
    assert any(sells), "Expected sells in demand-index"


def test_kalman_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=0.8)
    closes = [b.close for b in bars]

    k = kalman_1d(closes, length=20, r=0.01, q=0.1)
    assert len(k) == len(bars)
    valid_vals = [x for x in k if x is not None]
    assert len(valid_vals) == len(bars)

    # Smoke tests
    params = KalmanParams(mode="mode_a", length=20, r=0.01, q=0.1)
    ok, msg = validate_kalman_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_kalman_eth_smoke(params, "1h")[0]
    assert validate_kalman_sol_smoke(params, "1h")[0]
    assert validate_kalman_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_kalman_btc_smoke(params, "15m")[0]
    assert not validate_kalman_btc_smoke(KalmanParams(length=10), "1h")[0]
    assert not validate_kalman_sol_smoke(KalmanParams(length=5, q=1.0), "15m")[0]

    # Signals
    buys, sells, stops = kalman_signals(bars, params)
    assert any(buys), "Expected buys in kalman-estimate-cross"
    assert any(sells), "Expected sells in kalman-estimate-cross"


def test_ravi_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.8)
    closes = [b.close for b in bars]

    r = ravi(closes, short_len=7, long_len=65)
    assert len(r) == len(bars)
    valid_vals = [x for x in r if x is not None]
    assert len(valid_vals) > 40

    # Smoke tests
    params = RaviParams(mode="mode_a", short_len=7, long_len=65, thr=3.0, dir_len=3)
    ok, msg = validate_ravi_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_ravi_eth_smoke(params, "1h")[0]
    assert validate_ravi_sol_smoke(params, "1h")[0]
    assert validate_ravi_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_ravi_btc_smoke(params, "15m")[0]
    assert not validate_ravi_btc_smoke(RaviParams(short_len=3, long_len=65), "1h")[0]
    assert not validate_ravi_sol_smoke(RaviParams(short_len=3, thr=1.0), "15m")[0]

    # Signals (with smaller long_len=40 to get ample signals)
    params_dense = RaviParams(mode="mode_a", short_len=7, long_len=40, thr=2.0, dir_len=3)
    buys, sells, stops = ravi_signals(bars, params_dense)
    assert any(buys), "Expected buys in ravi-threshold-dir"
    assert any(sells), "Expected sells in ravi-threshold-dir"
