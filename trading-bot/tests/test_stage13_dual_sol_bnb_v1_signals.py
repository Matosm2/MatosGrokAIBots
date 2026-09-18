"""Unit tests for stage13-dual-sol-bnb-v1 signals and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.path_b.stage13_dual_sol_bnb_v1.clv_sma_zero_cross_v1 import (
    ClvSmaParams,
    compute_signals as clv_signals,
    validate_bnb_smoke as validate_clv_bnb_smoke,
    validate_btc_smoke as validate_clv_btc_smoke,
    validate_sol_smoke as validate_clv_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.demark_rei_zero_cross_v1 import (
    DemarkReiParams,
    compute_signals as rei_signals,
    validate_bnb_smoke as validate_rei_bnb_smoke,
    validate_btc_smoke as validate_rei_btc_smoke,
    validate_sol_smoke as validate_rei_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.donovan_range_filter_flip_v1 import (
    DonovanRangeFilterParams,
    compute_signals as rf_signals,
    validate_bnb_smoke as validate_rf_bnb_smoke,
    validate_btc_smoke as validate_rf_btc_smoke,
    validate_sol_smoke as validate_rf_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.khalil_pzo_zero_cross_v1 import (
    KhalilPzoParams,
    compute_signals as pzo_signals,
    validate_bnb_smoke as validate_pzo_bnb_smoke,
    validate_btc_smoke as validate_pzo_btc_smoke,
    validate_sol_smoke as validate_pzo_sol_smoke,
)
from backtest.path_b.stage13_dual_sol_bnb_v1.mobius_tmo_main_zero_v1 import (
    MobiusTmoParams,
    compute_signals as tmo_signals,
    validate_bnb_smoke as validate_tmo_bnb_smoke,
    validate_btc_smoke as validate_tmo_btc_smoke,
    validate_sol_smoke as validate_tmo_sol_smoke,
)


def _make_dummy_bars(n: int = 100, trend: float = 1.0) -> list[Bar]:
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        c = base + i * trend + (5.0 if i % 2 == 0 else -5.0)
        h = c + 2.0
        l = c - 2.0
        o = c - 1.0
        bars.append(
            Bar(
                open_time_ms=i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=1000.0,
                close_time_ms=(i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_demark_rei_signals():
    bars = _make_dummy_bars(80)
    params = DemarkReiParams(mode="mode_a", length=8)
    buys, sells, stops = rei_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_rei_btc_smoke(params, "1h")
    assert ok_btc
    ok_sol, _ = validate_rei_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_rei_bnb_smoke(params, "1h")
    assert ok_bnb

    # Invalid btc smoke (15m forbidden)
    bad_btc, _ = validate_rei_btc_smoke(params, "15m")
    assert not bad_btc


def test_khalil_pzo_signals():
    bars = _make_dummy_bars(80)
    params = KhalilPzoParams(mode="mode_a", n_len=14)
    buys, sells, stops = pzo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_pzo_btc_smoke(params, "1h")
    assert ok_btc
    ok_sol, _ = validate_pzo_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_pzo_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_pzo_sol_smoke(KhalilPzoParams(n_len=3), "15m")
    assert not bad_sol


def test_mobius_tmo_signals():
    bars = _make_dummy_bars(80)
    params = MobiusTmoParams(mode="mode_a", length=14, calc_length=5, smooth_length=3)
    buys, sells, stops = tmo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_tmo_btc_smoke(params, "1h")
    assert ok_btc
    ok_sol, _ = validate_tmo_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_tmo_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_btc, _ = validate_tmo_btc_smoke(MobiusTmoParams(calc_length=15), "1h")
    assert not bad_btc


def test_donovan_range_filter_signals():
    bars = _make_dummy_bars(80)
    params = DonovanRangeFilterParams(mode="mode_a", period=20, mult=1.618)
    buys, sells, stops = rf_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_rf_btc_smoke(params, "1h")
    assert ok_btc
    ok_sol, _ = validate_rf_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_rf_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_btc, _ = validate_rf_btc_smoke(DonovanRangeFilterParams(period=50), "1h")
    assert not bad_btc


def test_clv_sma_signals():
    bars = _make_dummy_bars(80)
    params = ClvSmaParams(mode="mode_a", n_len=14)
    buys, sells, stops = clv_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_clv_btc_smoke(params, "1h")
    assert ok_btc
    ok_sol, _ = validate_clv_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_clv_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_btc, _ = validate_clv_btc_smoke(ClvSmaParams(n_len=35), "1h")
    assert not bad_btc
