"""Unit tests for stage21-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math
import pytest

from backtest.data import Bar
from backtest.indicators import (
    chaikin_volatility,
    inside_bar,
    outside_bar,
    parkinson_vol,
    ulcer_index,
)
from backtest.path_b.stage21_dual_sol_bnb_v1.chaikin_volatility_dir_v1 import (
    ChaikinParams,
    compute_signals as chaikin_signals,
    validate_bnb_smoke as validate_chaikin_bnb_smoke,
    validate_btc_smoke as validate_chaikin_btc_smoke,
    validate_eth_smoke as validate_chaikin_eth_smoke,
    validate_sol_smoke as validate_chaikin_sol_smoke,
)
from backtest.path_b.stage21_dual_sol_bnb_v1.outside_bar_polarity_v1 import (
    OutsideBarParams,
    compute_signals as outside_bar_signals,
    validate_bnb_smoke as validate_outside_bar_bnb_smoke,
    validate_btc_smoke as validate_outside_bar_btc_smoke,
    validate_eth_smoke as validate_outside_bar_eth_smoke,
    validate_sol_smoke as validate_outside_bar_sol_smoke,
)
from backtest.path_b.stage21_dual_sol_bnb_v1.ulcer_index_recover_dir_v1 import (
    UlcerParams,
    compute_signals as ulcer_signals,
    validate_bnb_smoke as validate_ulcer_bnb_smoke,
    validate_btc_smoke as validate_ulcer_btc_smoke,
    validate_eth_smoke as validate_ulcer_eth_smoke,
    validate_sol_smoke as validate_ulcer_sol_smoke,
)
from backtest.path_b.stage21_dual_sol_bnb_v1.parkinson_vol_expansion_dir_v1 import (
    ParkinsonParams,
    compute_signals as parkinson_signals,
    validate_bnb_smoke as validate_parkinson_bnb_smoke,
    validate_btc_smoke as validate_parkinson_btc_smoke,
    validate_eth_smoke as validate_parkinson_eth_smoke,
    validate_sol_smoke as validate_parkinson_sol_smoke,
)
from backtest.path_b.stage21_dual_sol_bnb_v1.inside_bar_breakout_v1 import (
    InsideBarParams,
    compute_signals as inside_bar_signals,
    validate_bnb_smoke as validate_inside_bar_bnb_smoke,
    validate_btc_smoke as validate_inside_bar_btc_smoke,
    validate_eth_smoke as validate_inside_bar_eth_smoke,
    validate_sol_smoke as validate_inside_bar_sol_smoke,
)


def _make_dummy_bars(n: int = 140, trend: float = 1.0) -> list[Bar]:
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        swing = 20.0 * math.sin(i * 2.0 * math.pi / 16.0)
        c = base + i * trend + swing
        # Vary spread to create outside bars, inside bars, and vol expansions
        if i % 7 == 2:
            # Wide outside bar with close skewed high (bullOut)
            h = c + 4.0
            l = c - 8.0  # mid is c - 2.0, so c > mid (bullOut)
        elif i % 7 == 4:
            # Wide outside bar with close skewed low (bearOut)
            h = c + 8.0
            l = c - 4.0  # mid is c + 2.0, so c < mid (bearOut)
        elif i % 7 == 3:
            # Narrow bar (potential inside bar)
            h = c + 1.0
            l = c - 1.0
        else:
            h = c + 2.5
            l = c - 2.5
        o = c - 0.2
        vol = 1000.0 + (500.0 if i % 2 == 0 else -200.0)
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


def test_chaikin_volatility_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    cv = chaikin_volatility(highs, lows, ema_len=10, roc_len=10)
    assert len(cv) == len(bars)
    valid_cv = [x for x in cv if x is not None]
    assert len(valid_cv) > 80

    # Smoke validation
    params = ChaikinParams(mode="mode_a", ema_len=10, roc_len=10, dir_len=1)
    ok, msg = validate_chaikin_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_chaikin_eth_smoke(params, "1h")[0]
    assert validate_chaikin_sol_smoke(params, "1h")[0]
    assert validate_chaikin_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_chaikin_btc_smoke(params, "15m")[0]
    assert not validate_chaikin_btc_smoke(ChaikinParams(ema_len=20), "1h")[0]
    assert not validate_chaikin_sol_smoke(ChaikinParams(ema_len=3), "15m")[0]

    # Signals
    buys, sells, stops = chaikin_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected buy signals"
    assert any(sells), "Expected sell signals"


def test_outside_bar_polarity_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    outside, bull_out, bear_out = outside_bar(highs, lows, closes, mid_frac=0.5)
    assert len(outside) == len(bars)
    assert len(bull_out) == len(bars)
    assert len(bear_out) == len(bars)
    assert any(outside), "Expected some outside bars"

    # Smoke validation
    params = OutsideBarParams(mode="mode_a", mid_frac=0.5, confirm_bars=1)
    ok, msg = validate_outside_bar_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_outside_bar_eth_smoke(params, "1h")[0]
    assert validate_outside_bar_sol_smoke(params, "1h")[0]
    assert validate_outside_bar_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_outside_bar_btc_smoke(params, "15m")[0]
    assert not validate_outside_bar_btc_smoke(OutsideBarParams(mid_frac=0.8), "1h")[0]

    # Signals
    buys, sells, stops = outside_bar_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected buy signals"
    assert any(sells), "Expected sell signals"


def test_ulcer_index_recover_dir_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    closes = [b.close for b in bars]

    ui = ulcer_index(closes, ui_len=14)
    assert len(ui) == len(bars)
    valid_ui = [x for x in ui if x is not None]
    assert len(valid_ui) > 80

    # Smoke validation
    params = UlcerParams(mode="mode_a", ui_len=14, dir_len=1)
    ok, msg = validate_ulcer_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_ulcer_eth_smoke(params, "1h")[0]
    assert validate_ulcer_sol_smoke(params, "1h")[0]
    assert validate_ulcer_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_ulcer_btc_smoke(params, "15m")[0]
    assert not validate_ulcer_btc_smoke(UlcerParams(ui_len=40), "1h")[0]

    # Signals
    buys, sells, stops = ulcer_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected buy signals"
    assert any(sells), "Expected sell signals"


def test_parkinson_vol_expansion_dir_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    park = parkinson_vol(highs, lows, n_park=10)
    assert len(park) == len(bars)
    valid_park = [x for x in park if x is not None]
    assert len(valid_park) > 80

    # Smoke validation
    params = ParkinsonParams(mode="mode_a", n_park=10, dir_len=1)
    ok, msg = validate_parkinson_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_parkinson_eth_smoke(params, "1h")[0]
    assert validate_parkinson_sol_smoke(params, "1h")[0]
    assert validate_parkinson_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_parkinson_btc_smoke(params, "15m")[0]
    assert not validate_parkinson_btc_smoke(ParkinsonParams(n_park=50), "1h")[0]

    # Signals
    buys, sells, stops = parkinson_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected buy signals"
    assert any(sells), "Expected sell signals"


def test_inside_bar_breakout_indicator_and_signals():
    bars = _make_dummy_bars(120, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    ins = inside_bar(highs, lows)
    assert len(ins) == len(bars)
    assert any(ins), "Expected inside bars"

    # Smoke validation
    params = InsideBarParams(mode="mode_a", cancel_bars=5, k=0.0)
    ok, msg = validate_inside_bar_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_inside_bar_eth_smoke(params, "1h")[0]
    assert validate_inside_bar_sol_smoke(params, "1h")[0]
    assert validate_inside_bar_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_inside_bar_btc_smoke(params, "15m")[0]
    assert not validate_inside_bar_btc_smoke(InsideBarParams(cancel_bars=20), "1h")[0]

    # Signals
    buys, sells, stops = inside_bar_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected buy signals"
    assert any(sells), "Expected sell signals"
