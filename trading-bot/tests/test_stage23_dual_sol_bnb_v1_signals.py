"""Unit tests for stage23-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    chande_kroll_stop,
    mama_fama,
    qqe,
    wilder_volatility_system,
)
from backtest.path_b.stage23_dual_sol_bnb_v1.qqe_trailing_cross_v1 import (
    QqeParams,
    compute_signals as qqe_signals,
    validate_bnb_smoke as validate_qqe_bnb_smoke,
    validate_btc_smoke as validate_qqe_btc_smoke,
    validate_eth_smoke as validate_qqe_eth_smoke,
    validate_sol_smoke as validate_qqe_sol_smoke,
)
from backtest.path_b.stage23_dual_sol_bnb_v1.mama_fama_cross_v1 import (
    MamaFamaParams,
    compute_signals as mama_signals,
    validate_bnb_smoke as validate_mama_bnb_smoke,
    validate_btc_smoke as validate_mama_btc_smoke,
    validate_eth_smoke as validate_mama_eth_smoke,
    validate_sol_smoke as validate_mama_sol_smoke,
)
from backtest.path_b.stage23_dual_sol_bnb_v1.wilder_volatility_system_flip_v1 import (
    WilderVsParams,
    compute_signals as wilder_signals,
    validate_bnb_smoke as validate_wilder_bnb_smoke,
    validate_btc_smoke as validate_wilder_btc_smoke,
    validate_eth_smoke as validate_wilder_eth_smoke,
    validate_sol_smoke as validate_wilder_sol_smoke,
)
from backtest.path_b.stage23_dual_sol_bnb_v1.chande_kroll_stop_flip_v1 import (
    ChandeKrollParams,
    compute_signals as chande_signals,
    validate_bnb_smoke as validate_chande_bnb_smoke,
    validate_btc_smoke as validate_chande_btc_smoke,
    validate_eth_smoke as validate_chande_eth_smoke,
    validate_sol_smoke as validate_chande_sol_smoke,
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


def test_qqe_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    closes = [b.close for b in bars]

    fast, slow = qqe(closes, rsi_len=14, sf=5, wt=4.236)
    assert len(fast) == len(bars)
    assert len(slow) == len(bars)
    valid_fast = [x for x in fast if x is not None]
    assert len(valid_fast) > 60

    # Smoke validation
    params = QqeParams(mode="mode_a", rsi_len=14, sf=5, wt=4.236)
    ok, msg = validate_qqe_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_qqe_eth_smoke(params, "1h")[0]
    assert validate_qqe_sol_smoke(params, "1h")[0]
    assert validate_qqe_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_qqe_btc_smoke(params, "15m")[0]
    assert not validate_qqe_btc_smoke(QqeParams(rsi_len=10), "1h")[0]
    assert not validate_qqe_sol_smoke(QqeParams(rsi_len=5), "15m")[0]

    # Signals
    buys, sells, stops = qqe_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    # Never buy and sell on same bar
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_mama_fama_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    hl2 = [(b.high + b.low) / 2.0 for b in bars]

    mama, fama = mama_fama(hl2, fast_limit=0.5, slow_limit=0.05)
    assert len(mama) == len(bars)
    assert len(fama) == len(bars)
    valid_mama = [x for x in mama if x is not None]
    assert len(valid_mama) > 90

    # Smoke validation
    params = MamaFamaParams(mode="mode_a", fast_limit=0.5, slow_limit=0.05)
    ok, msg = validate_mama_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_mama_eth_smoke(params, "1h")[0]
    assert validate_mama_sol_smoke(params, "1h")[0]
    assert validate_mama_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_mama_btc_smoke(params, "15m")[0]
    assert not validate_mama_btc_smoke(MamaFamaParams(fast_limit=0.3), "1h")[0]
    assert not validate_mama_sol_smoke(MamaFamaParams(fast_limit=0.2), "15m")[0]

    # Signals
    buys, sells, stops = mama_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_wilder_vs_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    sar_long, sar_short = wilder_volatility_system(closes, highs, lows, n=7, factor=3.0)
    assert len(sar_long) == len(bars)
    assert len(sar_short) == len(bars)
    valid_sar = [x for x in sar_long if x is not None]
    assert len(valid_sar) > 100

    # Smoke validation
    params = WilderVsParams(mode="mode_a", n=7, factor=3.0)
    ok, msg = validate_wilder_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_wilder_eth_smoke(params, "1h")[0]
    assert validate_wilder_sol_smoke(params, "1h")[0]
    assert validate_wilder_bnb_smoke(params, "1h")[0]

    # Density alt (9, 2.0)
    alt_params = WilderVsParams(mode="mode_a", n=9, factor=2.0)
    assert validate_wilder_btc_smoke(alt_params, "1h")[0]

    # Smoke failure checks
    assert not validate_wilder_btc_smoke(params, "15m")[0]
    assert not validate_wilder_btc_smoke(WilderVsParams(n=5), "1h")[0]
    assert not validate_wilder_sol_smoke(WilderVsParams(n=3), "15m")[0]

    # Signals
    buys, sells, stops = wilder_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_chande_kroll_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    stop_short, stop_long = chande_kroll_stop(highs, lows, closes, p=10, x=1.0, q=9)
    assert len(stop_short) == len(bars)
    assert len(stop_long) == len(bars)
    valid_stops = [x for x in stop_short if x is not None]
    assert len(valid_stops) > 90

    # Smoke validation
    params = ChandeKrollParams(mode="mode_a", p=10, x=1.0, q=9)
    ok, msg = validate_chande_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_chande_eth_smoke(params, "1h")[0]
    assert validate_chande_sol_smoke(params, "1h")[0]
    assert validate_chande_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_chande_btc_smoke(params, "15m")[0]
    assert not validate_chande_btc_smoke(ChandeKrollParams(p=8), "1h")[0]
    assert not validate_chande_sol_smoke(ChandeKrollParams(p=3), "15m")[0]

    # Signals
    buys, sells, stops = chande_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
