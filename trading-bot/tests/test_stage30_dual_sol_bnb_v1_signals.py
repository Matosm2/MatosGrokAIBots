"""Unit tests for stage30-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    apirine_ma_bands,
    arms_vama,
    blau_dti,
    ehlers_rmo,
)
from backtest.path_b.stage30_dual_sol_bnb_v1.blau_dti_zero_cross_v1 import (
    BlauDtiParams,
    compute_signals as dti_signals,
    validate_bnb_smoke as validate_dti_bnb_smoke,
    validate_btc_smoke as validate_dti_btc_smoke,
    validate_eth_smoke as validate_dti_eth_smoke,
    validate_sol_smoke as validate_dti_sol_smoke,
)
from backtest.path_b.stage30_dual_sol_bnb_v1.arms_vama_dual_cross_v1 import (
    ArmsVamaParams,
    compute_signals as vama_signals,
    validate_bnb_smoke as validate_vama_bnb_smoke,
    validate_btc_smoke as validate_vama_btc_smoke,
    validate_eth_smoke as validate_vama_eth_smoke,
    validate_sol_smoke as validate_vama_sol_smoke,
)
from backtest.path_b.stage30_dual_sol_bnb_v1.apirine_ma_bands_break_v1 import (
    ApirineMaBandsParams,
    compute_signals as mab_signals,
    validate_bnb_smoke as validate_mab_bnb_smoke,
    validate_btc_smoke as validate_mab_btc_smoke,
    validate_eth_smoke as validate_mab_eth_smoke,
    validate_sol_smoke as validate_mab_sol_smoke,
)
from backtest.path_b.stage30_dual_sol_bnb_v1.ehlers_recursive_median_osc_zero_v1 import (
    EhlersRmoParams,
    compute_signals as rmo_signals,
    validate_bnb_smoke as validate_rmo_bnb_smoke,
    validate_btc_smoke as validate_rmo_btc_smoke,
    validate_eth_smoke as validate_rmo_eth_smoke,
    validate_sol_smoke as validate_rmo_sol_smoke,
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


def test_blau_dti_indicator_and_signals():
    bars = _make_dummy_bars(220, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    dti, num, den = blau_dti(highs, lows, q=2, r=20, s=5, u=3)
    assert len(dti) == len(bars)
    assert len(num) == len(bars)
    assert len(den) == len(bars)
    valid_dti = [x for x in dti if x is not None]
    assert len(valid_dti) > 100

    # DTI values should generally stay within [-100, 100]
    for v in valid_dti:
        assert -105.0 <= v <= 105.0

    # Smoke validation
    params = BlauDtiParams(mode="mode_a", q=2, r=20, s=5, u=3)
    ok, msg = validate_dti_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_dti_eth_smoke(params, "1h")[0]
    assert validate_dti_sol_smoke(params, "1h")[0]
    assert validate_dti_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_dti_btc_smoke(params, "15m")[0]
    assert not validate_dti_btc_smoke(BlauDtiParams(q=5), "1h")[0]
    assert not validate_dti_btc_smoke(BlauDtiParams(r=50), "1h")[0]
    assert not validate_dti_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = dti_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_arms_vama_indicator_and_signals():
    bars = _make_dummy_bars(250, trend=0.5)
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    vfast, vslow = arms_vama(closes, volumes, fast_len=8, slow_len=55, sample_n=100)
    assert len(vfast) == len(bars)
    assert len(vslow) == len(bars)
    valid_vfast = [x for x in vfast if x is not None]
    valid_vslow = [x for x in vslow if x is not None]
    assert len(valid_vfast) > 100
    assert len(valid_vslow) > 100

    # Values should be around close prices
    for vf in valid_vfast:
        assert 50.0 < vf < 350.0

    # Smoke validation
    params = ArmsVamaParams(mode="mode_a", fast_len=8, slow_len=55, sample_n=100)
    ok, msg = validate_vama_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vama_eth_smoke(params, "1h")[0]
    assert validate_vama_sol_smoke(params, "1h")[0]
    assert validate_vama_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_vama_btc_smoke(params, "15m")[0]
    assert not validate_vama_btc_smoke(ArmsVamaParams(fast_len=20), "1h")[0]
    assert not validate_vama_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = vama_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_apirine_ma_bands_indicator_and_signals():
    bars = _make_dummy_bars(200, trend=0.5)
    closes = [b.close for b in bars]

    ma2, upper, lower, ma1 = apirine_ma_bands(closes, p1=50, p2=10, mltp=1.0)
    assert len(ma2) == len(bars)
    assert len(upper) == len(bars)
    assert len(lower) == len(bars)
    assert len(ma1) == len(bars)

    valid_upper = [x for x in upper if x is not None]
    assert len(valid_upper) > 100

    # Upper >= Lower check
    for i in range(len(bars)):
        if upper[i] is not None and lower[i] is not None:
            assert upper[i] >= lower[i]

    # Smoke validation
    params = ApirineMaBandsParams(mode="mode_a", p1=50, p2=10, mltp=1.0)
    ok, msg = validate_mab_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_mab_eth_smoke(params, "1h")[0]
    assert validate_mab_sol_smoke(params, "1h")[0]
    assert validate_mab_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_mab_btc_smoke(params, "15m")[0]
    assert not validate_mab_btc_smoke(ApirineMaBandsParams(p1=15), "1h")[0]
    assert not validate_mab_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = mab_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_ehlers_rmo_indicator_and_signals():
    bars = _make_dummy_bars(180, trend=0.5)
    closes = [b.close for b in bars]

    rmo, rm = ehlers_rmo(closes, lp=12, hp=30, med_len=5)
    assert len(rmo) == len(bars)
    assert len(rm) == len(bars)
    valid_rmo = [x for x in rmo if x is not None]
    assert len(valid_rmo) > 100

    # Smoke validation
    params = EhlersRmoParams(mode="mode_a", lp=12, hp=30, med_len=5)
    ok, msg = validate_rmo_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_rmo_eth_smoke(params, "1h")[0]
    assert validate_rmo_sol_smoke(params, "1h")[0]
    assert validate_rmo_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_rmo_btc_smoke(params, "15m")[0]
    assert not validate_rmo_btc_smoke(EhlersRmoParams(lp=4), "1h")[0]
    assert not validate_rmo_btc_smoke(EhlersRmoParams(hp=60), "1h")[0]
    assert not validate_rmo_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = rmo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
