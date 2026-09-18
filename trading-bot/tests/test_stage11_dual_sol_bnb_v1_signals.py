"""Unit tests for stage11-dual-sol-bnb-v1 signals and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.path_b.stage11_dual_sol_bnb_v1.chande_trendscore_zero_cross_v1 import (
    ChandeTrendScoreParams,
    compute_signals as chande_signals,
    validate_bnb_smoke as validate_chande_bnb_smoke,
    validate_sol_smoke as validate_chande_sol_smoke,
)
from backtest.path_b.stage11_dual_sol_bnb_v1.ehlers_leading_netlead_ema_v1 import (
    EhlersLeadingParams,
    compute_signals as ehlers_signals,
    validate_bnb_smoke as validate_ehlers_bnb_smoke,
    validate_sol_smoke as validate_ehlers_sol_smoke,
)
from backtest.path_b.stage11_dual_sol_bnb_v1.gmma_osc_zero_cross_v1 import (
    GmmaOscParams,
    compute_signals as gmma_signals,
    validate_bnb_smoke as validate_gmma_bnb_smoke,
    validate_sol_smoke as validate_gmma_sol_smoke,
)
from backtest.path_b.stage11_dual_sol_bnb_v1.pee_tdi_direction_zero_v1 import (
    PeeTdiDirectionParams,
    compute_signals as pee_signals,
    validate_bnb_smoke as validate_pee_bnb_smoke,
    validate_sol_smoke as validate_pee_sol_smoke,
)
from backtest.path_b.stage11_dual_sol_bnb_v1.vqi_sum_sma_cross_v1 import (
    VqiSumSmaParams,
    compute_signals as vqi_signals,
    validate_bnb_smoke as validate_vqi_bnb_smoke,
    validate_sol_smoke as validate_vqi_sol_smoke,
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


def test_chande_trendscore_signals():
    bars = _make_dummy_bars(60)
    params = ChandeTrendScoreParams(mode="mode_a", start_lag=11, width=10)
    buys, sells, stops = chande_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    # Smoke validation
    ok_sol, _ = validate_chande_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_chande_bnb_smoke(params, "1h")
    assert ok_bnb

    # Invalid sol smoke
    bad_sol, msg = validate_chande_sol_smoke(ChandeTrendScoreParams(width=2), "15m")
    assert not bad_sol


def test_pee_tdi_direction_signals():
    bars = _make_dummy_bars(80)
    params = PeeTdiDirectionParams(mode="mode_a", n_len=20)
    buys, sells, stops = pee_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_pee_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_pee_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_pee_sol_smoke(PeeTdiDirectionParams(n_len=5), "15m")
    assert not bad_sol


def test_ehlers_leading_signals():
    bars = _make_dummy_bars(60)
    params = EhlersLeadingParams(mode="mode_a", a1=0.25, a2=0.50)
    buys, sells, stops = ehlers_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_ehlers_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_ehlers_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_ehlers_sol_smoke(EhlersLeadingParams(a1=0.8, a2=0.8), "15m")
    assert not bad_sol


def test_gmma_osc_signals():
    bars = _make_dummy_bars(120)
    params = GmmaOscParams(mode="mode_a")
    buys, sells, stops = gmma_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_gmma_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_gmma_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_gmma_sol_smoke(GmmaOscParams(sig_len=2), "15m")
    assert not bad_sol


def test_vqi_sum_sma_signals():
    bars = _make_dummy_bars(60)
    params = VqiSumSmaParams(mode="mode_a", sma_fast=9)
    buys, sells, stops = vqi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_sol, _ = validate_vqi_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_vqi_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_vqi_sol_smoke(VqiSumSmaParams(sma_fast=2), "15m")
    assert not bad_sol
