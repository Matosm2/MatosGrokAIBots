"""Unit tests for stage24-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    guppy_cbl,
    kirshenbaum_bands,
    imi,
    williams_ad,
)
from backtest.path_b.stage24_dual_sol_bnb_v1.guppy_countback_line_flip_v1 import (
    GuppyCblParams,
    compute_signals as guppy_signals,
    validate_bnb_smoke as validate_guppy_bnb_smoke,
    validate_btc_smoke as validate_guppy_btc_smoke,
    validate_eth_smoke as validate_guppy_eth_smoke,
    validate_sol_smoke as validate_guppy_sol_smoke,
)
from backtest.path_b.stage24_dual_sol_bnb_v1.kirshenbaum_bands_break_v1 import (
    KirshenbaumParams,
    compute_signals as kirshenbaum_signals,
    validate_bnb_smoke as validate_kirshenbaum_bnb_smoke,
    validate_btc_smoke as validate_kirshenbaum_btc_smoke,
    validate_eth_smoke as validate_kirshenbaum_eth_smoke,
    validate_sol_smoke as validate_kirshenbaum_sol_smoke,
)
from backtest.path_b.stage24_dual_sol_bnb_v1.imi_midline_fifty_v1 import (
    ImiParams,
    compute_signals as imi_signals,
    validate_bnb_smoke as validate_imi_bnb_smoke,
    validate_btc_smoke as validate_imi_btc_smoke,
    validate_eth_smoke as validate_imi_eth_smoke,
    validate_sol_smoke as validate_imi_sol_smoke,
)
from backtest.path_b.stage24_dual_sol_bnb_v1.williams_ad_sma_cross_v1 import (
    WilliamsAdParams,
    compute_signals as williams_signals,
    validate_bnb_smoke as validate_williams_bnb_smoke,
    validate_btc_smoke as validate_williams_btc_smoke,
    validate_eth_smoke as validate_williams_eth_smoke,
    validate_sol_smoke as validate_williams_sol_smoke,
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


def test_guppy_cbl_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    cbl_long, cbl_short = guppy_cbl(highs, lows, closes, count_depth=3)
    assert len(cbl_long) == len(bars)
    assert len(cbl_short) == len(bars)
    valid_long = [x for x in cbl_long if x is not None]
    assert len(valid_long) > 100

    # Smoke validation
    params = GuppyCblParams(mode="mode_a", count_depth=3, atr_trail_mult=0.0)
    ok, msg = validate_guppy_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_guppy_eth_smoke(params, "1h")[0]
    assert validate_guppy_sol_smoke(params, "1h")[0]
    assert validate_guppy_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_guppy_btc_smoke(params, "15m")[0]
    assert not validate_guppy_btc_smoke(GuppyCblParams(count_depth=5), "1h")[0]
    assert not validate_guppy_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = guppy_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_kirshenbaum_bands_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    closes = [b.close for b in bars]

    upper, mid, lower, stderr_series = kirshenbaum_bands(closes, ema_len=20, reg_len=20, k=1.75)
    assert len(upper) == len(bars)
    assert len(mid) == len(bars)
    assert len(lower) == len(bars)
    assert len(stderr_series) == len(bars)
    valid_u = [x for x in upper if x is not None]
    assert len(valid_u) > 90

    # Smoke validation
    params = KirshenbaumParams(mode="mode_a", ema_len=20, reg_len=20, k=1.75)
    ok, msg = validate_kirshenbaum_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_kirshenbaum_eth_smoke(params, "1h")[0]
    assert validate_kirshenbaum_sol_smoke(params, "1h")[0]
    assert validate_kirshenbaum_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_kirshenbaum_btc_smoke(params, "15m")[0]
    assert not validate_kirshenbaum_btc_smoke(KirshenbaumParams(ema_len=50), "1h")[0]
    assert not validate_kirshenbaum_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = kirshenbaum_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_imi_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    opens = [b.open for b in bars]
    closes = [b.close for b in bars]

    imi_vals = imi(opens, closes, n=14)
    assert len(imi_vals) == len(bars)
    valid_imi = [x for x in imi_vals if x is not None]
    assert len(valid_imi) > 100

    # Smoke validation
    params = ImiParams(mode="mode_a", n=14)
    ok, msg = validate_imi_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_imi_eth_smoke(params, "1h")[0]
    assert validate_imi_sol_smoke(params, "1h")[0]
    assert validate_imi_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_imi_btc_smoke(params, "15m")[0]
    assert not validate_imi_btc_smoke(ImiParams(n=5), "1h")[0]
    assert not validate_imi_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = imi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_williams_ad_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    wad_vals, sig_vals = williams_ad(highs, lows, closes, m=21)
    assert len(wad_vals) == len(bars)
    assert len(sig_vals) == len(bars)
    valid_sig = [x for x in sig_vals if x is not None]
    assert len(valid_sig) > 90

    # Smoke validation
    params = WilliamsAdParams(mode="mode_a", m=21)
    ok, msg = validate_williams_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_williams_eth_smoke(params, "1h")[0]
    assert validate_williams_sol_smoke(params, "1h")[0]
    assert validate_williams_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_williams_btc_smoke(params, "15m")[0]
    assert not validate_williams_btc_smoke(WilliamsAdParams(m=5), "1h")[0]
    assert not validate_williams_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = williams_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
