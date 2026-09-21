"""Unit tests for stage31-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math
import pytest

from backtest.data import Bar
from backtest.indicators import (
    apirine_sdo,
    apirine_tradj_ema,
    ehlers_madh,
    premier_stochastic_oscillator,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.apirine_sdo_zero_cross_v1 import (
    ApirineSdoParams,
    compute_signals as sdo_signals,
    validate_bnb_smoke as validate_sdo_bnb_smoke,
    validate_btc_smoke as validate_sdo_btc_smoke,
    validate_eth_smoke as validate_sdo_eth_smoke,
    validate_sol_smoke as validate_sdo_sol_smoke,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.ehlers_madh_zero_cross_v1 import (
    EhlersMadhParams,
    compute_signals as madh_signals,
    validate_bnb_smoke as validate_madh_bnb_smoke,
    validate_btc_smoke as validate_madh_btc_smoke,
    validate_eth_smoke as validate_madh_eth_smoke,
    validate_sol_smoke as validate_madh_sol_smoke,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.premier_stochastic_osc_zero_v1 import (
    PremierStochParams,
    compute_signals as pso_signals,
    validate_bnb_smoke as validate_pso_bnb_smoke,
    validate_btc_smoke as validate_pso_btc_smoke,
    validate_eth_smoke as validate_pso_eth_smoke,
    validate_sol_smoke as validate_pso_sol_smoke,
)
from backtest.path_b.stage31_dual_sol_bnb_v1.apirine_tradj_ema_cross_v1 import (
    ApirineTradjEmaParams,
    compute_signals as tradj_signals,
    validate_bnb_smoke as validate_tradj_bnb_smoke,
    validate_btc_smoke as validate_tradj_btc_smoke,
    validate_eth_smoke as validate_tradj_eth_smoke,
    validate_sol_smoke as validate_tradj_sol_smoke,
)


def _make_dummy_bars(count: int = 150) -> list[Bar]:
    """Generate synthetic sine/trend bars for indicator testing."""
    bars: list[Bar] = []
    base_time = 1_700_000_000_000
    for i in range(count):
        t = base_time + i * 3600 * 1000
        cycle = 10.0 * math.sin(2.0 * math.pi * i / 25.0)
        trend = 0.2 * i
        c = 100.0 + cycle + trend
        h = c + 1.5
        l = c - 1.5
        o = (h + l) / 2.0
        v = 1000.0 + 100.0 * math.sin(i / 5.0)
        bars.append(Bar(t, o, h, l, c, v, t + 3600 * 1000 - 1))
    return bars


# ---------------------------------------------------------------------------
# Indicator & Signal 1: Apirine SDO
# ---------------------------------------------------------------------------

def test_apirine_sdo_calculation():
    bars = _make_dummy_bars(150)
    closes = [b.close for b in bars]
    sdo = apirine_sdo(closes, n=8, lb=30, pds=3)
    assert len(sdo) == len(closes)
    # Check warmup None
    assert all(v is None for v in sdo[: 8 + 30 - 1])
    # Later values should be finite floats
    valid = [v for v in sdo if v is not None]
    assert len(valid) > 50
    assert all(-100.0 <= v <= 100.0 for v in valid)


def test_apirine_sdo_signals():
    bars = _make_dummy_bars(150)
    params = ApirineSdoParams(mode="mode_a", n=8, lb=30, pds=3)
    buys, sells, stops = sdo_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    # Check that at least some signals are generated on alternating sine wave
    assert any(buys)
    assert any(sells)


def test_apirine_sdo_smoke_validators():
    valid_p = ApirineSdoParams(n=14, lb=100, pds=3)
    ok, _ = validate_sdo_btc_smoke(valid_p, "1h")
    assert ok is True
    ok_eth, _ = validate_sdo_eth_smoke(valid_p, "1h")
    assert ok_eth is True
    ok_sol, _ = validate_sdo_sol_smoke(valid_p, "1h")
    assert ok_sol is True
    ok_bnb, _ = validate_sdo_bnb_smoke(valid_p, "1h")
    assert ok_bnb is True

    # 15m forbidden
    bad_tf, _ = validate_sdo_btc_smoke(valid_p, "15m")
    assert bad_tf is False

    # Out of grid parameter fails
    bad_p = ApirineSdoParams(n=99)
    bad_btc, _ = validate_sdo_btc_smoke(bad_p, "1h")
    assert bad_btc is False


# ---------------------------------------------------------------------------
# Indicator & Signal 2: Ehlers MADH
# ---------------------------------------------------------------------------

def test_ehlers_madh_calculation():
    bars = _make_dummy_bars(150)
    closes = [b.close for b in bars]
    madh, filt1, filt2 = ehlers_madh(closes, short_length=8, dominant_cycle=27)
    assert len(madh) == len(closes)
    long_len = int(8 + 27 / 2)  # 21
    assert all(v is None for v in filt1[: 8 - 1])
    assert all(v is None for v in filt2[: long_len - 1])
    valid_madh = [v for v in madh if v is not None]
    assert len(valid_madh) > 50
    # On a continuous series, MADH should fluctuate around 0
    assert min(valid_madh) < 0.0 < max(valid_madh)


def test_ehlers_madh_signals():
    bars = _make_dummy_bars(150)
    params = EhlersMadhParams(mode="mode_a", short_length=8, dominant_cycle=27)
    buys, sells, stops = madh_signals(bars, params)
    assert len(buys) == len(bars)
    assert any(buys)
    assert any(sells)


def test_ehlers_madh_smoke_validators():
    valid_p = EhlersMadhParams(short_length=8, dominant_cycle=27)
    ok, _ = validate_madh_btc_smoke(valid_p, "1h")
    assert ok is True
    ok_eth, _ = validate_madh_eth_smoke(valid_p, "1h")
    assert ok_eth is True

    bad_tf, _ = validate_madh_btc_smoke(valid_p, "15m")
    assert bad_tf is False

    bad_p = EhlersMadhParams(short_length=99)
    bad_btc, _ = validate_madh_btc_smoke(bad_p, "1h")
    assert bad_btc is False


# ---------------------------------------------------------------------------
# Indicator & Signal 3: Premier Stochastic Oscillator
# ---------------------------------------------------------------------------

def test_premier_stochastic_oscillator_calculation():
    bars = _make_dummy_bars(150)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    pso = premier_stochastic_oscillator(highs, lows, closes, period=8, smooth=5)
    assert len(pso) == len(closes)
    valid_pso = [v for v in pso if v is not None]
    assert len(valid_pso) > 50
    # PSO should strictly be in (-1, 1) due to tanh form
    assert all(-1.0 < v < 1.0 for v in valid_pso)


def test_premier_stochastic_signals():
    bars = _make_dummy_bars(150)
    params = PremierStochParams(mode="mode_a", period=8, smooth=5)
    buys, sells, stops = pso_signals(bars, params)
    assert len(buys) == len(bars)
    assert any(buys)
    assert any(sells)


def test_premier_stochastic_smoke_validators():
    valid_p = PremierStochParams(period=8, smooth=5)
    ok, _ = validate_pso_btc_smoke(valid_p, "1h")
    assert ok is True
    ok_eth, _ = validate_pso_eth_smoke(valid_p, "1h")
    assert ok_eth is True

    bad_tf, _ = validate_pso_btc_smoke(valid_p, "15m")
    assert bad_tf is False

    bad_p = PremierStochParams(period=50)
    bad_btc, _ = validate_pso_btc_smoke(bad_p, "1h")
    assert bad_btc is False


# ---------------------------------------------------------------------------
# Indicator & Signal 4: Apirine TRAdj EMA
# ---------------------------------------------------------------------------

def test_apirine_tradj_ema_calculation():
    bars = _make_dummy_bars(150)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    tradj_ema, ema_ref = apirine_tradj_ema(highs, lows, closes, periods=20, pds=20, mltp=5.0)
    assert len(tradj_ema) == len(closes)
    assert len(ema_ref) == len(closes)
    valid_tr = [v for v in tradj_ema if v is not None]
    valid_ref = [v for v in ema_ref if v is not None]
    assert len(valid_tr) > 50
    assert len(valid_ref) > 50
    # Both should be near close price
    assert 80.0 < valid_tr[-1] < 150.0


def test_apirine_tradj_signals():
    bars = _make_dummy_bars(150)
    params = ApirineTradjEmaParams(mode="mode_a", periods=20, pds=20, mltp=5.0)
    buys, sells, stops = tradj_signals(bars, params)
    assert len(buys) == len(bars)
    assert any(buys)
    assert any(sells)


def test_apirine_tradj_smoke_validators():
    valid_p = ApirineTradjEmaParams(periods=20, pds=20, mltp=5.0)
    ok, _ = validate_tradj_btc_smoke(valid_p, "1h")
    assert ok is True
    ok_eth, _ = validate_tradj_eth_smoke(valid_p, "1h")
    assert ok_eth is True

    bad_tf, _ = validate_tradj_btc_smoke(valid_p, "15m")
    assert bad_tf is False

    bad_p = ApirineTradjEmaParams(periods=200)
    bad_btc, _ = validate_tradj_btc_smoke(bad_p, "1h")
    assert bad_btc is False
