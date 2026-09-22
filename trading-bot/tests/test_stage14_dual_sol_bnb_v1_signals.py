"""Unit tests for stage14-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    absolute_strength_hist,
    hannula_pfe,
    leibfarth_apz,
    nadaraya_rq,
    pee_ttf,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.pee_ttf_zero_cross_v1 import (
    PeeTtfParams,
    compute_signals as ttf_signals,
    validate_bnb_smoke as validate_ttf_bnb_smoke,
    validate_btc_smoke as validate_ttf_btc_smoke,
    validate_eth_smoke as validate_ttf_eth_smoke,
    validate_sol_smoke as validate_ttf_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.hannula_pfe_zero_cross_v1 import (
    HannulaPfeParams,
    compute_signals as pfe_signals,
    validate_bnb_smoke as validate_pfe_bnb_smoke,
    validate_btc_smoke as validate_pfe_btc_smoke,
    validate_eth_smoke as validate_pfe_eth_smoke,
    validate_sol_smoke as validate_pfe_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.absolute_strength_hist_zero_v1 import (
    AbsoluteStrengthHistParams,
    compute_signals as ash_signals,
    validate_bnb_smoke as validate_ash_bnb_smoke,
    validate_btc_smoke as validate_ash_btc_smoke,
    validate_eth_smoke as validate_ash_eth_smoke,
    validate_sol_smoke as validate_ash_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.leibfarth_apz_break_flip_v1 import (
    LeibfarthApzParams,
    compute_signals as apz_signals,
    validate_bnb_smoke as validate_apz_bnb_smoke,
    validate_btc_smoke as validate_apz_btc_smoke,
    validate_eth_smoke as validate_apz_eth_smoke,
    validate_sol_smoke as validate_apz_sol_smoke,
)
from backtest.path_b.stage14_dual_sol_bnb_v1.nadaraya_rq_estimate_cross_v1 import (
    NadarayaRqParams,
    compute_signals as rq_signals,
    validate_bnb_smoke as validate_rq_bnb_smoke,
    validate_btc_smoke as validate_rq_btc_smoke,
    validate_eth_smoke as validate_rq_eth_smoke,
    validate_sol_smoke as validate_rq_sol_smoke,
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


def test_pee_ttf_indicator_and_signals():
    bars = _make_dummy_bars(80)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    ttf = pee_ttf(highs, lows, length=15)
    assert len(ttf) == len(bars)
    # TTF requires 2*L bars = 30 bars, so index 29 is first valid
    assert ttf[28] is None
    assert ttf[29] is not None

    params = PeeTtfParams(mode="mode_a", length=15)
    buys, sells, stops = ttf_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_ttf_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_ttf_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_ttf_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_ttf_bnb_smoke(params, "1h")
    assert ok_bnb

    # Invalid btc smoke (15m forbidden)
    bad_btc, _ = validate_ttf_btc_smoke(params, "15m")
    assert not bad_btc

    # Invalid length
    bad_len, _ = validate_ttf_btc_smoke(PeeTtfParams(length=30), "1h")
    assert not bad_len


def test_hannula_pfe_indicator_and_signals():
    bars = _make_dummy_bars(80)
    closes = [b.close for b in bars]
    pfe = hannula_pfe(closes, period=10, smooth=5)
    assert len(pfe) == len(bars)
    # First valid PFE index is period + smooth - 1 = 10 + 5 - 1 = 14
    assert pfe[13] is None
    assert pfe[14] is not None

    params = HannulaPfeParams(mode="mode_a", period=10, smooth=5)
    buys, sells, stops = pfe_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_pfe_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_pfe_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_pfe_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_pfe_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_sol, _ = validate_pfe_sol_smoke(HannulaPfeParams(period=3), "15m")
    assert not bad_sol


def test_absolute_strength_hist_indicator_and_signals():
    bars = _make_dummy_bars(80)
    closes = [b.close for b in bars]
    ash = absolute_strength_hist(closes, length=9, smooth=2)
    assert len(ash) == len(bars)
    # First SMA valid at 8, second SMA (smooth=2) valid at 8 + 2 - 1 = 9
    assert ash[8] is None
    assert ash[9] is not None

    params = AbsoluteStrengthHistParams(mode="mode_a", length=9, smooth=2)
    buys, sells, stops = ash_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_ash_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_ash_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_ash_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_ash_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_btc, _ = validate_ash_btc_smoke(AbsoluteStrengthHistParams(length=50), "1h")
    assert not bad_btc


def test_leibfarth_apz_indicator_and_signals():
    bars = _make_dummy_bars(80)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    ds, dsg, up, dn = leibfarth_apz(highs, lows, closes, period=20, band_pct=1.4)
    assert len(up) == len(bars)
    assert len(dn) == len(bars)
    # First EMA valid at index 19 (length 20).
    # Second EMA over valid slice of length p -> valid at 19 + 20 - 1 = index 38.
    assert up[37] is None
    assert up[38] is not None
    assert dn[38] is not None
    assert up[38] > dn[38]

    params = LeibfarthApzParams(mode="mode_a", period=20, band_pct=1.4)
    buys, sells, stops = apz_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_apz_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_apz_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_apz_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_apz_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_btc, _ = validate_apz_btc_smoke(LeibfarthApzParams(period=60), "1h")
    assert not bad_btc


def test_nadaraya_rq_indicator_and_signals():
    bars = _make_dummy_bars(80)
    closes = [b.close for b in bars]
    yhat = nadaraya_rq(closes, lookback=8, alpha=8.0)
    assert len(yhat) == len(bars)
    # First valid at lookback - 1 = 7
    assert yhat[6] is None
    assert yhat[7] is not None

    params = NadarayaRqParams(mode="mode_a", lookback=8, alpha=8.0)
    buys, sells, stops = rq_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)

    ok_btc, _ = validate_rq_btc_smoke(params, "1h")
    assert ok_btc
    ok_eth, _ = validate_rq_eth_smoke(params, "1h")
    assert ok_eth
    ok_sol, _ = validate_rq_sol_smoke(params, "1h")
    assert ok_sol
    ok_bnb, _ = validate_rq_bnb_smoke(params, "1h")
    assert ok_bnb

    bad_btc, _ = validate_rq_btc_smoke(NadarayaRqParams(lookback=30), "1h")
    assert not bad_btc
