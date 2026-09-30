"""Unit tests for stage12-dual-sol-bnb-v1 signals and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.path_b.stage12_dual_sol_bnb_v1.blau_csi_ergodic_signal_cross_v1 import (
    BlauCsiParams,
    compute_signals as blau_signals,
    validate_bnb_smoke as validate_blau_bnb_smoke,
    validate_sol_smoke as validate_blau_sol_smoke,
)
from backtest.path_b.stage12_dual_sol_bnb_v1.ehlers_edcf_filt_lag_cross_v1 import (
    EhlersEdcfParams,
    compute_signals as edcf_signals,
    validate_bnb_smoke as validate_edcf_bnb_smoke,
    validate_sol_smoke as validate_edcf_sol_smoke,
)
from backtest.path_b.stage12_dual_sol_bnb_v1.ehlers_gaussian_fast_slow_cross_v1 import (
    EhlersGaussianParams,
    compute_signals as gaussian_signals,
    validate_bnb_smoke as validate_gaussian_bnb_smoke,
    validate_sol_smoke as validate_gaussian_sol_smoke,
)
from backtest.path_b.stage12_dual_sol_bnb_v1.ehlers_ultimate_smoother_dual_cross_v1 import (
    EhlersUltimateSmootherParams,
    compute_signals as us_signals,
    validate_bnb_smoke as validate_us_bnb_smoke,
    validate_sol_smoke as validate_us_sol_smoke,
)
from backtest.path_b.stage12_dual_sol_bnb_v1.swenlin_pmo_signal_cross_v1 import (
    SwenlinPmoParams,
    compute_signals as pmo_signals,
    validate_bnb_smoke as validate_pmo_bnb_smoke,
    validate_sol_smoke as validate_pmo_sol_smoke,
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


def test_blau_csi_signals():
    bars = _make_dummy_bars(80)
    params = BlauCsiParams(mode="mode_a", r=20, ul=3)
    buys, sells, stops = blau_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    # Smoke validation
    ok_sol, _ = validate_blau_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_blau_bnb_smoke(params, "1h")
    assert ok_bnb

    # Invalid sol smoke (15m r<=3 spam)
    bad_sol, msg = validate_blau_sol_smoke(BlauCsiParams(r=3), "15m")
    assert not bad_sol


def test_ehlers_edcf_signals():
    bars = _make_dummy_bars(80)
    params = EhlersEdcfParams(mode="mode_a", length=15, lag=2)
    buys, sells, stops = edcf_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_edcf_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_edcf_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_edcf_sol_smoke(EhlersEdcfParams(length=5), "15m")
    assert not bad_sol


def test_ehlers_ultimate_smoother_signals():
    bars = _make_dummy_bars(80)
    params = EhlersUltimateSmootherParams(mode="mode_a", period_fast=10, period_slow=30)
    buys, sells, stops = us_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_us_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_us_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_us_sol_smoke(EhlersUltimateSmootherParams(period_fast=3), "15m")
    assert not bad_sol


def test_ehlers_gaussian_signals():
    bars = _make_dummy_bars(80)
    params = EhlersGaussianParams(mode="mode_a", period_fast=10, period_slow=30, poles=2)
    buys, sells, stops = gaussian_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_gaussian_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_gaussian_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_gaussian_sol_smoke(EhlersGaussianParams(period_fast=3), "15m")
    assert not bad_sol


def test_swenlin_pmo_signals():
    bars = _make_dummy_bars(80)
    params = SwenlinPmoParams(mode="mode_a", s1=35, s2=20, sig_len=10)
    buys, sells, stops = pmo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_pmo_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_pmo_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_pmo_sol_smoke(SwenlinPmoParams(s1=5), "15m")
    assert not bad_sol
