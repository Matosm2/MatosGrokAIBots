"""Unit tests for stage17-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    blau_ergodic_mdi,
    bostian_iii,
    dss_bressert,
    ehlers_predictive_ma,
    heikin_ashi_bias,
)
from backtest.path_b.stage17_dual_sol_bnb_v1.heikin_ashi_bias_flip_v1 import (
    HeikinAshiParams,
    compute_signals as heikin_ashi_signals,
    validate_bnb_smoke as validate_heikin_ashi_bnb_smoke,
    validate_btc_smoke as validate_heikin_ashi_btc_smoke,
    validate_eth_smoke as validate_heikin_ashi_eth_smoke,
    validate_sol_smoke as validate_heikin_ashi_sol_smoke,
)
from backtest.path_b.stage17_dual_sol_bnb_v1.blau_ergodic_mdi_signal_cross_v1 import (
    BlauMdiParams,
    compute_signals as blau_mdi_signals,
    validate_bnb_smoke as validate_blau_mdi_bnb_smoke,
    validate_btc_smoke as validate_blau_mdi_btc_smoke,
    validate_eth_smoke as validate_blau_mdi_eth_smoke,
    validate_sol_smoke as validate_blau_mdi_sol_smoke,
)
from backtest.path_b.stage17_dual_sol_bnb_v1.dss_bressert_trigger_cross_v1 import (
    DssBressertParams,
    compute_signals as dss_bressert_signals,
    validate_bnb_smoke as validate_dss_bressert_bnb_smoke,
    validate_btc_smoke as validate_dss_bressert_btc_smoke,
    validate_eth_smoke as validate_dss_bressert_eth_smoke,
    validate_sol_smoke as validate_dss_bressert_sol_smoke,
)
from backtest.path_b.stage17_dual_sol_bnb_v1.bostian_iii_sma_zero_v1 import (
    BostianIiiParams,
    compute_signals as bostian_iii_signals,
    validate_bnb_smoke as validate_bostian_iii_bnb_smoke,
    validate_btc_smoke as validate_bostian_iii_btc_smoke,
    validate_eth_smoke as validate_bostian_iii_eth_smoke,
    validate_sol_smoke as validate_bostian_iii_sol_smoke,
)
from backtest.path_b.stage17_dual_sol_bnb_v1.ehlers_predictive_ma_cross_v1 import (
    PredictiveMaParams,
    compute_signals as predictive_ma_signals,
    validate_bnb_smoke as validate_predictive_ma_bnb_smoke,
    validate_btc_smoke as validate_predictive_ma_btc_smoke,
    validate_eth_smoke as validate_predictive_ma_eth_smoke,
    validate_sol_smoke as validate_predictive_ma_sol_smoke,
)


def _make_dummy_bars(n: int = 100, trend: float = 1.0) -> list[Bar]:
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        c = base + i * trend + (5.0 if i % 2 == 0 else -5.0)
        h = c + 4.0 + (1.0 if i % 3 == 0 else 0.0)
        l = c - 4.0
        o = c - 1.0
        bars.append(
            Bar(
                open_time_ms=i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=1000.0 + (i * 10.0),
                close_time_ms=(i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_heikin_ashi_bias_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.5)
    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    ha_o, ha_c, bull = heikin_ashi_bias(opens, highs, lows, closes)
    assert len(ha_o) == len(bars)
    assert len(ha_c) == len(bars)
    assert len(bull) == len(bars)
    assert any(bull)
    assert not all(bull)

    params_a = HeikinAshiParams(mode="mode_a", confirm=1)
    buys_a, sells_a, stops_a = heikin_ashi_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = HeikinAshiParams(mode="mode_b", confirm=2, atr_trail_mult=2.0)
    buys_b, sells_b, stops_b = heikin_ashi_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_heikin_ashi_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_heikin_ashi_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_confirm, _ = validate_heikin_ashi_btc_smoke(HeikinAshiParams(confirm=3), "1h")
    assert not bad_btc_confirm

    ok_eth, _ = validate_heikin_ashi_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_heikin_ashi_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_heikin_ashi_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_blau_ergodic_mdi_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.2)
    closes = [b.close for b in bars]

    mdi, sig = blau_ergodic_mdi(closes, r=20, s=5, u=3, ul=3)
    assert len(mdi) == len(bars)
    assert len(sig) == len(bars)
    assert mdi[0] is None
    assert sig[-1] is not None

    params_a = BlauMdiParams(mode="mode_a", r=20, s=5, u=3, ul=3)
    buys_a, sells_a, stops_a = blau_mdi_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = BlauMdiParams(mode="mode_b", r=20, s=5, u=3, ul=3)
    buys_b, sells_b, stops_b = blau_mdi_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_blau_mdi_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_blau_mdi_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_r, _ = validate_blau_mdi_btc_smoke(BlauMdiParams(r=40), "1h")
    assert not bad_btc_r

    ok_eth, _ = validate_blau_mdi_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_blau_mdi_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_blau_mdi_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_dss_bressert_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    dss, trig = dss_bressert(highs, lows, closes, pds=10, ema_len=9, trigger_len=5)
    assert len(dss) == len(bars)
    assert len(trig) == len(bars)
    assert dss[0] is None
    assert dss[-1] is not None
    assert 0.0 <= float(dss[-1]) <= 100.0

    params_a = DssBressertParams(mode="mode_a", pds=10, ema_len=9, trigger_len=5)
    buys_a, sells_a, stops_a = dss_bressert_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = DssBressertParams(mode="mode_b", pds=10, ema_len=9, trigger_len=5)
    buys_b, sells_b, stops_b = dss_bressert_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_dss_bressert_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_dss_bressert_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_pds, _ = validate_dss_bressert_btc_smoke(DssBressertParams(pds=25), "1h")
    assert not bad_btc_pds

    ok_eth, _ = validate_dss_bressert_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_dss_bressert_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_dss_bressert_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_bostian_iii_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    iii, iii_s = bostian_iii(highs, lows, closes, volumes, sma_len=21)
    assert len(iii) == len(bars)
    assert len(iii_s) == len(bars)
    assert iii[0] != 0.0 or highs[0] == lows[0]
    assert iii_s[-1] is not None

    params_a = BostianIiiParams(mode="mode_a", sma_len=21)
    buys_a, sells_a, stops_a = bostian_iii_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = BostianIiiParams(mode="mode_b", sma_len=21, quality_threshold=10.0)
    buys_b, sells_b, stops_b = bostian_iii_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_bostian_iii_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_bostian_iii_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_len, _ = validate_bostian_iii_btc_smoke(BostianIiiParams(sma_len=60), "1h")
    assert not bad_btc_len

    ok_eth, _ = validate_bostian_iii_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_bostian_iii_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_bostian_iii_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_ehlers_predictive_ma_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    closes = [b.close for b in bars]

    predict, trig = ehlers_predictive_ma(closes, wma_len=7, trigger_len=4)
    assert len(predict) == len(bars)
    assert len(trig) == len(bars)
    assert predict[0] is None
    assert trig[-1] is not None

    params_a = PredictiveMaParams(mode="mode_a", src="close", wma_len=7, trigger_len=4)
    buys_a, sells_a, stops_a = predictive_ma_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = PredictiveMaParams(mode="mode_b", src="hl2", wma_len=7, trigger_len=4)
    buys_b, sells_b, stops_b = predictive_ma_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_predictive_ma_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_predictive_ma_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_len, _ = validate_predictive_ma_btc_smoke(PredictiveMaParams(wma_len=14), "1h")
    assert not bad_btc_len

    ok_eth, _ = validate_predictive_ma_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_predictive_ma_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_predictive_ma_bnb_smoke(params_a, "1h")
    assert ok_bnb
