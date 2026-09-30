"""Unit tests for stage15-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    ehlers_corr_cycle,
    ehlers_net_myrsi,
    ehlers_spearman,
    ehlers_uo2025,
    varadi_dvi,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_spearman_rank_zero_v1 import (
    SpearmanRankParams,
    compute_signals as spearman_signals,
    validate_bnb_smoke as validate_spearman_bnb_smoke,
    validate_btc_smoke as validate_spearman_btc_smoke,
    validate_eth_smoke as validate_spearman_eth_smoke,
    validate_sol_smoke as validate_spearman_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_uo2025_hpdiff_zero_v1 import (
    Uo2025Params,
    compute_signals as uo2025_signals,
    validate_bnb_smoke as validate_uo2025_bnb_smoke,
    validate_btc_smoke as validate_uo2025_btc_smoke,
    validate_eth_smoke as validate_uo2025_eth_smoke,
    validate_sol_smoke as validate_uo2025_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_corr_cycle_real_zero_v1 import (
    CorrCycleParams,
    compute_signals as corr_cycle_signals,
    validate_bnb_smoke as validate_corr_cycle_bnb_smoke,
    validate_btc_smoke as validate_corr_cycle_btc_smoke,
    validate_eth_smoke as validate_corr_cycle_eth_smoke,
    validate_sol_smoke as validate_corr_cycle_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.ehlers_net_myrsi_zero_v1 import (
    NetMyRsiParams,
    compute_signals as net_myrsi_signals,
    validate_bnb_smoke as validate_net_myrsi_bnb_smoke,
    validate_btc_smoke as validate_net_myrsi_btc_smoke,
    validate_eth_smoke as validate_net_myrsi_eth_smoke,
    validate_sol_smoke as validate_net_myrsi_sol_smoke,
)
from backtest.path_b.stage15_dual_sol_bnb_v1.varadi_dvi_midline_cross_v1 import (
    VaradiDviParams,
    compute_signals as dvi_signals,
    validate_bnb_smoke as validate_dvi_bnb_smoke,
    validate_btc_smoke as validate_dvi_btc_smoke,
    validate_eth_smoke as validate_dvi_eth_smoke,
    validate_sol_smoke as validate_dvi_sol_smoke,
)


def _make_dummy_bars(n: int = 100, trend: float = 1.0) -> list[Bar]:
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        c = base + i * trend + (5.0 if i % 2 == 0 else -5.0)
        h = c + 3.0
        l = c - 3.0
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


def test_ehlers_spearman_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.5)
    closes = [b.close for b in bars]
    rho, sig = ehlers_spearman(closes, length=20)
    assert len(rho) == len(bars)
    assert len(sig) == len(bars)
    assert rho[18] is None
    assert rho[19] is not None
    assert -1.0 <= rho[19] <= 1.0

    params_a = SpearmanRankParams(mode="mode_a", length=20)
    buys_a, sells_a, stops_a = spearman_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = SpearmanRankParams(mode="mode_b", length=20, quality_threshold=0.2)
    buys_b, sells_b, stops_b = spearman_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_spearman_btc_smoke(params_a, "1h")
    assert ok_btc
    ok_eth, _ = validate_spearman_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_spearman_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_spearman_bnb_smoke(params_a, "1h")
    assert ok_bnb

    # Smoke failure cases
    bad_tf, _ = validate_spearman_btc_smoke(params_a, "15m")
    assert not bad_tf
    bad_len, _ = validate_spearman_btc_smoke(SpearmanRankParams(length=50), "1h")
    assert not bad_len


def test_ehlers_uo2025_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.8)
    closes = [b.close for b in bars]
    uo, sig = ehlers_uo2025(closes, band_edge=20, bandwidth=2.0)
    assert len(uo) == len(bars)
    assert len(sig) == len(bars)
    # Check valid values exist
    valid_uos = [x for x in uo if x is not None]
    assert len(valid_uos) > 0

    params = Uo2025Params(mode="mode_a", band_edge=20, bandwidth=2.0)
    buys, sells, stops = uo2025_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    params_b = Uo2025Params(mode="mode_b", band_edge=20, bandwidth=2.0)
    buys_b, sells_b, _ = uo2025_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_uo2025_btc_smoke(params, "4h")
    assert ok_btc
    ok_eth, _ = validate_uo2025_eth_smoke(params, "4h")
    assert ok_eth
    ok_sol, _ = validate_uo2025_sol_smoke(params, "4h")
    assert ok_sol
    ok_bnb, _ = validate_uo2025_bnb_smoke(params, "4h")
    assert ok_bnb

    # Smoke failures
    bad_tf, _ = validate_uo2025_btc_smoke(params, "15m")
    assert not bad_tf
    bad_edge, _ = validate_uo2025_btc_smoke(Uo2025Params(band_edge=40), "1h")
    assert not bad_edge


def test_ehlers_corr_cycle_indicator_and_signals():
    bars = _make_dummy_bars(90, trend=1.0)
    closes = [b.close for b in bars]
    real, imag, angle, state = ehlers_corr_cycle(closes, period=20, threshold=9.0)
    assert len(real) == len(bars)
    assert len(imag) == len(bars)
    assert len(angle) == len(bars)
    assert len(state) == len(bars)

    valid_reals = [r for r in real if r is not None]
    assert len(valid_reals) > 0
    for r in valid_reals:
        assert -1.0 <= r <= 1.0

    params_a = CorrCycleParams(mode="mode_a", period=20, threshold=9.0)
    buys_a, sells_a, stops_a = corr_cycle_signals(bars, params_a)
    assert len(buys_a) == len(bars)

    params_b = CorrCycleParams(mode="mode_b", period=20, threshold=9.0)
    buys_b, sells_b, stops_b = corr_cycle_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_corr_cycle_btc_smoke(params_a, "1h")
    assert ok_btc
    ok_eth, _ = validate_corr_cycle_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_corr_cycle_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_corr_cycle_bnb_smoke(params_a, "1h")
    assert ok_bnb

    # Failures
    bad_tf, _ = validate_corr_cycle_btc_smoke(params_a, "15m")
    assert not bad_tf
    bad_th, _ = validate_corr_cycle_btc_smoke(CorrCycleParams(threshold=25.0), "1h")
    assert not bad_th


def test_ehlers_net_myrsi_indicator_and_signals():
    bars = _make_dummy_bars(90, trend=1.2)
    closes = [b.close for b in bars]
    net, my = ehlers_net_myrsi(closes, rsi_length=14, net_length=14)
    assert len(net) == len(bars)
    assert len(my) == len(bars)

    valid_nets = [x for x in net if x is not None]
    assert len(valid_nets) > 0
    for val in valid_nets:
        assert -1.0 <= val <= 1.0

    params = NetMyRsiParams(mode="mode_a", rsi_length=14, net_length=14)
    buys, sells, stops = net_myrsi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    params_b = NetMyRsiParams(mode="mode_b", rsi_length=14, net_length=14)
    buys_b, sells_b, _ = net_myrsi_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_net_myrsi_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_net_myrsi_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_net_myrsi_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_net_myrsi_bnb_smoke(params, "1h")
    assert ok_bnb

    # Smoke failure
    bad_tf, _ = validate_net_myrsi_btc_smoke(params, "15m")
    assert not bad_tf
    bad_len, _ = validate_net_myrsi_btc_smoke(NetMyRsiParams(rsi_length=50), "1h")
    assert not bad_len


def test_varadi_dvi_indicator_and_signals():
    bars = _make_dummy_bars(350, trend=0.5)
    closes = [b.close for b in bars]
    dvi, mag, st = varadi_dvi(closes, n=168, mag_weight=0.8, str_weight=0.2)
    assert len(dvi) == len(bars)
    assert len(mag) == len(bars)
    assert len(st) == len(bars)

    valid_dvis = [v for v in dvi if v is not None]
    assert len(valid_dvis) > 0
    for v in valid_dvis:
        assert 0.0 <= v <= 1.0

    params = VaradiDviParams(mode="mode_a", n=168)
    buys, sells, stops = dvi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    params_b = VaradiDviParams(mode="mode_b", n=168, entry_threshold=0.55)
    buys_b, sells_b, _ = dvi_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_dvi_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_dvi_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_dvi_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_dvi_bnb_smoke(params, "1h")
    assert ok_bnb

    # Smoke failure
    bad_tf, _ = validate_dvi_btc_smoke(params, "15m")
    assert not bad_tf
    bad_n, _ = validate_dvi_btc_smoke(VaradiDviParams(n=400), "1h")
    assert not bad_n
