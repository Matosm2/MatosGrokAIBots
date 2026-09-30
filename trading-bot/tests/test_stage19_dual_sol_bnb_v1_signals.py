"""Unit tests for stage19-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    fdi,
    hhll_structure,
    nvi,
    starc_bands,
    vzo,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.hhll_structure_flip_v1 import (
    HhllParams,
    compute_signals as hhll_signals,
    validate_bnb_smoke as validate_hhll_bnb_smoke,
    validate_btc_smoke as validate_hhll_btc_smoke,
    validate_eth_smoke as validate_hhll_eth_smoke,
    validate_sol_smoke as validate_hhll_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.starc_bands_break_flip_v1 import (
    StarcParams,
    compute_signals as starc_signals,
    validate_bnb_smoke as validate_starc_bnb_smoke,
    validate_btc_smoke as validate_starc_btc_smoke,
    validate_eth_smoke as validate_starc_eth_smoke,
    validate_sol_smoke as validate_starc_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.vzo_zero_cross_v1 import (
    VzoParams,
    compute_signals as vzo_signals,
    validate_bnb_smoke as validate_vzo_bnb_smoke,
    validate_btc_smoke as validate_vzo_btc_smoke,
    validate_eth_smoke as validate_vzo_eth_smoke,
    validate_sol_smoke as validate_vzo_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.nvi_ema_cross_v1 import (
    NviParams,
    compute_signals as nvi_signals,
    validate_bnb_smoke as validate_nvi_bnb_smoke,
    validate_btc_smoke as validate_nvi_btc_smoke,
    validate_eth_smoke as validate_nvi_eth_smoke,
    validate_sol_smoke as validate_nvi_sol_smoke,
)
from backtest.path_b.stage19_dual_sol_bnb_v1.fdi_low_trend_dir_v1 import (
    FdiParams,
    compute_signals as fdi_signals,
    validate_bnb_smoke as validate_fdi_bnb_smoke,
    validate_btc_smoke as validate_fdi_btc_smoke,
    validate_eth_smoke as validate_fdi_eth_smoke,
    validate_sol_smoke as validate_fdi_sol_smoke,
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
        # Alternating volume to exercise volume indicators (NVI, VZO)
        vol = 1000.0 + (500.0 if i % 2 == 0 else -200.0) + (i * 5.0)
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


def test_hhll_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=0.8)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    bull, bear, sh, sl = hhll_structure(highs, lows, lb=3)
    assert len(bull) == len(bars)
    assert len(bear) == len(bars)
    assert len(sh) == len(bars)
    assert len(sl) == len(bars)

    # Smoke tests
    params = HhllParams(mode="mode_a", lb=3)
    ok, msg = validate_hhll_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_hhll_eth_smoke(params, "1h")[0]
    assert validate_hhll_sol_smoke(params, "1h")[0]
    assert validate_hhll_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_hhll_btc_smoke(params, "15m")[0]
    assert not validate_hhll_btc_smoke(HhllParams(lb=15), "1h")[0]
    assert not validate_hhll_sol_smoke(HhllParams(lb=1), "15m")[0]

    buys, sells, stops = hhll_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    assert any(buys)


def test_starc_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=1.0)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    upper, mid, lower = starc_bands(highs, lows, closes, sma_len=6, atr_len=15, k=2.0)
    assert len(upper) == len(bars)
    assert len(mid) == len(bars)
    assert len(lower) == len(bars)

    valid_idx = [i for i in range(len(bars)) if upper[i] is not None]
    assert len(valid_idx) > 0
    for i in valid_idx:
        assert upper[i] > mid[i] > lower[i]

    # Smoke tests
    params = StarcParams(mode="mode_a", sma_len=6, atr_len=15, k=2.0)
    ok, msg = validate_starc_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_starc_eth_smoke(params, "1h")[0]
    assert validate_starc_sol_smoke(params, "1h")[0]
    assert validate_starc_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_starc_btc_smoke(params, "15m")[0]
    assert not validate_starc_btc_smoke(StarcParams(k=4.0), "1h")[0]
    assert not validate_starc_sol_smoke(StarcParams(sma_len=3, k=1.0), "15m")[0]

    buys, sells, stops = starc_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    assert any(buys)


def test_vzo_indicator_and_signals():
    bars = _make_dummy_bars(100, trend=0.5)
    closes = [b.close for b in bars]
    vols = [b.volume for b in bars]

    vzo_vals = vzo(closes, vols, length=14)
    assert len(vzo_vals) == len(bars)
    valid_vzo = [v for v in vzo_vals if v is not None]
    assert len(valid_vzo) > 0
    # Must oscillate around zero
    assert any(v > 0 for v in valid_vzo)
    assert any(v < 0 for v in valid_vzo)

    # Smoke tests
    params = VzoParams(mode="mode_a", length=14)
    ok, msg = validate_vzo_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vzo_eth_smoke(params, "1h")[0]
    assert validate_vzo_sol_smoke(params, "1h")[0]
    assert validate_vzo_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_vzo_btc_smoke(params, "15m")[0]
    assert not validate_vzo_btc_smoke(VzoParams(length=50), "1h")[0]
    assert not validate_vzo_sol_smoke(VzoParams(length=5), "15m")[0]

    buys, sells, stops = vzo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    assert any(buys)


def test_nvi_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    closes = [b.close for b in bars]
    vols = [b.volume for b in bars]

    nvi_vals, sig_vals = nvi(closes, vols, sig_len=50)
    assert len(nvi_vals) == len(bars)
    assert len(sig_vals) == len(bars)
    # NVI starts at 1000.0 and varies
    assert nvi_vals[0] == 1000.0
    valid_sig = [s for s in sig_vals if s is not None]
    assert len(valid_sig) > 0

    # Smoke tests
    params = NviParams(mode="mode_a", sig_len=50)
    ok, msg = validate_nvi_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_nvi_eth_smoke(params, "1h")[0]
    assert validate_nvi_sol_smoke(params, "1h")[0]
    assert validate_nvi_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_nvi_btc_smoke(params, "15m")[0]
    assert not validate_nvi_btc_smoke(NviParams(sig_len=255), "1h")[0]
    assert not validate_nvi_sol_smoke(NviParams(sig_len=5), "15m")[0]

    buys, sells, stops = nvi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    assert any(buys)


def test_fdi_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=1.5)
    closes = [b.close for b in bars]

    fdi_vals = fdi(closes, n=30)
    assert len(fdi_vals) == len(bars)
    valid_fdi = [v for v in fdi_vals if v is not None]
    assert len(valid_fdi) > 0
    # FDI values are strictly within [1.0, 2.0]
    for v in valid_fdi:
        assert 1.0 <= v <= 2.0

    # Smoke tests
    params = FdiParams(mode="mode_a", n=30, thr=1.50, dir_len=3)
    ok, msg = validate_fdi_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_fdi_eth_smoke(params, "1h")[0]
    assert validate_fdi_sol_smoke(params, "1h")[0]
    assert validate_fdi_bnb_smoke(params, "1h")[0]

    # Smoke failures
    assert not validate_fdi_btc_smoke(params, "15m")[0]
    assert not validate_fdi_btc_smoke(FdiParams(thr=1.10), "1h")[0]
    assert not validate_fdi_sol_smoke(FdiParams(n=5, thr=1.85), "15m")[0]

    buys, sells, stops = fdi_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    assert any(buys)
