"""Unit tests for stage25-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    ehlers_dsp,
    nhnl_osc,
    volume_roc,
    elder_thermometer,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.ehlers_dsp_zero_cross_v1 import (
    EhlersDspParams,
    compute_signals as dsp_signals,
    validate_bnb_smoke as validate_dsp_bnb_smoke,
    validate_btc_smoke as validate_dsp_btc_smoke,
    validate_eth_smoke as validate_dsp_eth_smoke,
    validate_sol_smoke as validate_dsp_sol_smoke,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.nhnl_oscillator_zero_v1 import (
    NhnlParams,
    compute_signals as nhnl_signals,
    validate_bnb_smoke as validate_nhnl_bnb_smoke,
    validate_btc_smoke as validate_nhnl_btc_smoke,
    validate_eth_smoke as validate_nhnl_eth_smoke,
    validate_sol_smoke as validate_nhnl_sol_smoke,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.volume_roc_dir_v1 import (
    VolumeRocParams,
    compute_signals as vroc_signals,
    validate_bnb_smoke as validate_vroc_bnb_smoke,
    validate_btc_smoke as validate_vroc_btc_smoke,
    validate_eth_smoke as validate_vroc_eth_smoke,
    validate_sol_smoke as validate_vroc_sol_smoke,
)
from backtest.path_b.stage25_dual_sol_bnb_v1.elder_thermometer_cool_dir_v1 import (
    ElderThermometerParams,
    compute_signals as thermo_signals,
    validate_bnb_smoke as validate_thermo_bnb_smoke,
    validate_btc_smoke as validate_thermo_btc_smoke,
    validate_eth_smoke as validate_thermo_eth_smoke,
    validate_sol_smoke as validate_thermo_sol_smoke,
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


def test_ehlers_dsp_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    dsp_vals = ehlers_dsp(highs, lows, length=7)
    assert len(dsp_vals) == len(bars)
    valid_dsp = [x for x in dsp_vals if x is not None]
    assert len(valid_dsp) == len(bars)

    # Smoke validation
    params = EhlersDspParams(mode="mode_a", length=7)
    ok, msg = validate_dsp_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_dsp_eth_smoke(params, "1h")[0]
    assert validate_dsp_sol_smoke(params, "1h")[0]
    assert validate_dsp_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_dsp_btc_smoke(params, "15m")[0]
    assert not validate_dsp_btc_smoke(EhlersDspParams(length=10), "1h")[0]
    assert not validate_dsp_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = dsp_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_nhnl_osc_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    osc_vals = nhnl_osc(highs, lows, l=20, w=10)
    assert len(osc_vals) == len(bars)
    valid_osc = [x for x in osc_vals if x is not None]
    assert len(valid_osc) > 80

    # Smoke validation
    params = NhnlParams(mode="mode_a", l=20, w=10)
    ok, msg = validate_nhnl_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_nhnl_eth_smoke(params, "1h")[0]
    assert validate_nhnl_sol_smoke(params, "1h")[0]
    assert validate_nhnl_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_nhnl_btc_smoke(params, "15m")[0]
    assert not validate_nhnl_btc_smoke(NhnlParams(l=25, w=10), "1h")[0]
    assert not validate_nhnl_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = nhnl_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_volume_roc_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    volumes = [b.volume for b in bars]

    vroc_vals = volume_roc(volumes, n=14)
    assert len(vroc_vals) == len(bars)
    valid_vroc = [x for x in vroc_vals if x is not None]
    assert len(valid_vroc) > 90

    # Smoke validation
    params = VolumeRocParams(mode="mode_a", n=14, dir_len=1)
    ok, msg = validate_vroc_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vroc_eth_smoke(params, "1h")[0]
    assert validate_vroc_sol_smoke(params, "1h")[0]
    assert validate_vroc_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_vroc_btc_smoke(params, "15m")[0]
    assert not validate_vroc_btc_smoke(VolumeRocParams(n=15), "1h")[0]
    assert not validate_vroc_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = vroc_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_elder_thermometer_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    thermo_vals, tma_vals = elder_thermometer(highs, lows, ema_len=22)
    assert len(thermo_vals) == len(bars)
    assert len(tma_vals) == len(bars)
    valid_t = [x for x in thermo_vals if x is not None]
    valid_tma = [x for x in tma_vals if x is not None]
    assert len(valid_t) == len(bars)
    assert len(valid_tma) == len(bars) - 22 + 1

    # Smoke validation
    params = ElderThermometerParams(mode="mode_a", ema_len=22, k=3.0, dir_len=1)
    ok, msg = validate_thermo_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_thermo_eth_smoke(params, "1h")[0]
    assert validate_thermo_sol_smoke(params, "1h")[0]
    assert validate_thermo_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_thermo_btc_smoke(params, "15m")[0]
    assert not validate_thermo_btc_smoke(ElderThermometerParams(ema_len=25), "1h")[0]
    assert not validate_thermo_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = thermo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
