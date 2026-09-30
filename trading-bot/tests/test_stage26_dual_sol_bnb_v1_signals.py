"""Unit tests for stage26-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    ehlers_convolution,
    elder_safezone,
    hilbert_ht_trendline,
    katsanos_fve,
)
from backtest.path_b.stage26_dual_sol_bnb_v1.ehlers_convolution_zero_v1 import (
    EhlersConvolutionParams,
    compute_signals as conv_signals,
    validate_bnb_smoke as validate_conv_bnb_smoke,
    validate_btc_smoke as validate_conv_btc_smoke,
    validate_eth_smoke as validate_conv_eth_smoke,
    validate_sol_smoke as validate_conv_sol_smoke,
)
from backtest.path_b.stage26_dual_sol_bnb_v1.elder_safezone_trail_flip_v1 import (
    ElderSafeZoneParams,
    compute_signals as safezone_signals,
    validate_bnb_smoke as validate_safezone_bnb_smoke,
    validate_btc_smoke as validate_safezone_btc_smoke,
    validate_eth_smoke as validate_safezone_eth_smoke,
    validate_sol_smoke as validate_safezone_sol_smoke,
)
from backtest.path_b.stage26_dual_sol_bnb_v1.hilbert_inst_trendline_cross_v1 import (
    HilbertTrendlineParams,
    compute_signals as ht_signals,
    validate_bnb_smoke as validate_ht_bnb_smoke,
    validate_btc_smoke as validate_ht_btc_smoke,
    validate_eth_smoke as validate_ht_eth_smoke,
    validate_sol_smoke as validate_ht_sol_smoke,
)
from backtest.path_b.stage26_dual_sol_bnb_v1.katsanos_fve_zero_cross_v1 import (
    KatsanosFveParams,
    compute_signals as fve_signals,
    validate_bnb_smoke as validate_fve_bnb_smoke,
    validate_btc_smoke as validate_fve_btc_smoke,
    validate_eth_smoke as validate_fve_eth_smoke,
    validate_sol_smoke as validate_fve_sol_smoke,
)


def _make_dummy_bars(n: int = 180, trend: float = 1.0) -> list[Bar]:
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


def test_katsanos_fve_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    fve_vals = katsanos_fve(highs, lows, closes, volumes, samples=22)
    assert len(fve_vals) == len(bars)
    valid_fve = [x for x in fve_vals if x is not None]
    assert len(valid_fve) > 100

    # Smoke validation
    params = KatsanosFveParams(mode="mode_a", samples=22)
    ok, msg = validate_fve_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_fve_eth_smoke(params, "1h")[0]
    assert validate_fve_sol_smoke(params, "1h")[0]
    assert validate_fve_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_fve_btc_smoke(params, "15m")[0]
    assert not validate_fve_btc_smoke(KatsanosFveParams(samples=50), "1h")[0]
    assert not validate_fve_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = fve_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_ehlers_convolution_indicator_and_signals():
    bars = _make_dummy_bars(180, trend=0.5)
    closes = [b.close for b in bars]

    conv_vals = ehlers_convolution(closes, lookback=18)
    assert len(conv_vals) == len(bars)
    valid_conv = [x for x in conv_vals if x is not None]
    assert len(valid_conv) > 30

    for val in valid_conv:
        assert -1.0001 <= val <= 1.0001

    # Smoke validation
    params = EhlersConvolutionParams(mode="mode_a", lookback=18, thr=0.05)
    ok, msg = validate_conv_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_conv_eth_smoke(params, "1h")[0]
    assert validate_conv_sol_smoke(params, "1h")[0]
    assert validate_conv_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_conv_btc_smoke(params, "15m")[0]
    assert not validate_conv_btc_smoke(EhlersConvolutionParams(lookback=50), "1h")[0]
    assert not validate_conv_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = conv_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_hilbert_inst_trendline_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    closes = [b.close for b in bars]

    ht_vals = hilbert_ht_trendline(closes)
    assert len(ht_vals) == len(bars)
    valid_ht = [x for x in ht_vals if x is not None]
    assert len(valid_ht) > 70

    # Smoke validation
    params = HilbertTrendlineParams(mode="mode_a", source="close")
    ok, msg = validate_ht_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_ht_eth_smoke(params, "1h")[0]
    assert validate_ht_sol_smoke(params, "1h")[0]
    assert validate_ht_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_ht_btc_smoke(params, "15m")[0]
    assert not validate_ht_btc_smoke(HilbertTrendlineParams(source="invalid"), "1h")[0]
    assert not validate_ht_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = ht_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_elder_safezone_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    long_stops, up_series = elder_safezone(highs, lows, closes, ema_len=22, n=10, k=2.5)
    assert len(long_stops) == len(bars)
    assert len(up_series) == len(bars)
    valid_stops = [x for x in long_stops if x is not None]
    assert len(valid_stops) > 100

    # Smoke validation
    params = ElderSafeZoneParams(mode="mode_a", ema_len=22, n=10, k=2.5)
    ok, msg = validate_safezone_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_safezone_eth_smoke(params, "1h")[0]
    assert validate_safezone_sol_smoke(params, "1h")[0]
    assert validate_safezone_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_safezone_btc_smoke(params, "15m")[0]
    assert not validate_safezone_btc_smoke(ElderSafeZoneParams(ema_len=50), "1h")[0]
    assert not validate_safezone_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = safezone_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
