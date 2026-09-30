"""Unit tests for stage28-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    dv2_varadi,
    ehlers_ec,
    ehlers_fir_zl,
    vervoort_zlha_typ,
)
from backtest.path_b.stage28_dual_sol_bnb_v1.ehlers_ec_ema_cross_v1 import (
    EhlersEcParams,
    compute_signals as ec_signals,
    validate_bnb_smoke as validate_ec_bnb_smoke,
    validate_btc_smoke as validate_ec_btc_smoke,
    validate_eth_smoke as validate_ec_eth_smoke,
    validate_sol_smoke as validate_ec_sol_smoke,
)
from backtest.path_b.stage28_dual_sol_bnb_v1.vervoort_zlha_typ_cross_v1 import (
    VervoortZlhaParams,
    compute_signals as vervoort_signals,
    validate_bnb_smoke as validate_vervoort_bnb_smoke,
    validate_btc_smoke as validate_vervoort_btc_smoke,
    validate_eth_smoke as validate_vervoort_eth_smoke,
    validate_sol_smoke as validate_vervoort_sol_smoke,
)
from backtest.path_b.stage28_dual_sol_bnb_v1.ehlers_fir_zl_price_cross_v1 import (
    EhlersFirZlParams,
    compute_signals as fir_signals,
    validate_bnb_smoke as validate_fir_bnb_smoke,
    validate_btc_smoke as validate_fir_btc_smoke,
    validate_eth_smoke as validate_fir_eth_smoke,
    validate_sol_smoke as validate_fir_sol_smoke,
)
from backtest.path_b.stage28_dual_sol_bnb_v1.dv2_varadi_midline_v1 import (
    Dv2VaradiParams,
    compute_signals as dv2_signals,
    validate_bnb_smoke as validate_dv2_bnb_smoke,
    validate_btc_smoke as validate_dv2_btc_smoke,
    validate_eth_smoke as validate_dv2_eth_smoke,
    validate_sol_smoke as validate_dv2_sol_smoke,
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


def test_ehlers_ec_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    closes = [b.close for b in bars]

    ec_vals, ema_vals, err_pcts = ehlers_ec(closes, length=20, gain_limit=50)
    assert len(ec_vals) == len(bars)
    assert len(ema_vals) == len(bars)
    assert len(err_pcts) == len(bars)
    valid_ec = [x for x in ec_vals if x is not None]
    assert len(valid_ec) == len(bars)

    # Smoke validation
    params = EhlersEcParams(mode="mode_a", length=20, gain_limit=50, thresh=0.0)
    ok, msg = validate_ec_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_ec_eth_smoke(params, "1h")[0]
    assert validate_ec_sol_smoke(params, "1h")[0]
    assert validate_ec_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_ec_btc_smoke(params, "15m")[0]
    assert not validate_ec_btc_smoke(EhlersEcParams(length=50), "1h")[0]
    assert not validate_ec_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = ec_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_vervoort_zlha_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    zl_typ, zl_ha = vervoort_zlha_typ(opens, highs, lows, closes, n=34)
    assert len(zl_typ) == len(bars)
    assert len(zl_ha) == len(bars)
    valid_typ = [x for x in zl_typ if x is not None]
    assert len(valid_typ) > 100

    # Smoke validation
    params = VervoortZlhaParams(mode="mode_a", n=34)
    ok, msg = validate_vervoort_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_vervoort_eth_smoke(params, "1h")[0]
    assert validate_vervoort_sol_smoke(params, "1h")[0]
    assert validate_vervoort_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_vervoort_btc_smoke(params, "15m")[0]
    assert not validate_vervoort_btc_smoke(VervoortZlhaParams(n=99), "1h")[0]
    assert not validate_vervoort_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = vervoort_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_ehlers_fir_zl_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    closes = [b.close for b in bars]

    fir95 = ehlers_fir_zl(closes, denom_mode="9.5")
    fir12 = ehlers_fir_zl(closes, denom_mode="12")
    assert len(fir95) == len(bars)
    assert len(fir12) == len(bars)
    valid_95 = [x for x in fir95 if x is not None]
    assert len(valid_95) > 100

    # Smoke validation
    params = EhlersFirZlParams(mode="mode_a", src="close", denom="9.5")
    ok, msg = validate_fir_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_fir_eth_smoke(params, "1h")[0]
    assert validate_fir_sol_smoke(params, "1h")[0]
    assert validate_fir_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_fir_btc_smoke(params, "15m")[0]
    assert not validate_fir_btc_smoke(EhlersFirZlParams(src="open"), "1h")[0]
    assert not validate_fir_btc_smoke(EhlersFirZlParams(denom="15"), "1h")[0]
    assert not validate_fir_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = fir_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_dv2_varadi_indicator_and_signals():
    bars = _make_dummy_bars(180, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    dv2_vals, dv_raw = dv2_varadi(highs, lows, closes, rank_len=100)
    assert len(dv2_vals) == len(bars)
    assert len(dv_raw) == len(bars)
    valid_dv2 = [x for x in dv2_vals if x is not None]
    assert len(valid_dv2) > 50

    # Smoke validation
    params = Dv2VaradiParams(mode="mode_a", rank_len=100, mid=50.0)
    ok, msg = validate_dv2_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_dv2_eth_smoke(params, "1h")[0]
    assert validate_dv2_sol_smoke(params, "1h")[0]
    assert validate_dv2_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_dv2_btc_smoke(params, "15m")[0]
    assert not validate_dv2_btc_smoke(Dv2VaradiParams(rank_len=10), "1h")[0]
    assert not validate_dv2_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = dv2_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
