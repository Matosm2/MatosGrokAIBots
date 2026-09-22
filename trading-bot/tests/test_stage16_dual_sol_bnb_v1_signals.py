"""Unit tests for stage16-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    ehlers_bandpass,
    ehlers_twopole_hp,
    nison_kagi,
    three_line_break,
    wilder_swing_index,
)
from backtest.path_b.stage16_dual_sol_bnb_v1.ehlers_bandpass_zero_v1 import (
    BandpassParams,
    compute_signals as bandpass_signals,
    validate_bnb_smoke as validate_bandpass_bnb_smoke,
    validate_btc_smoke as validate_bandpass_btc_smoke,
    validate_eth_smoke as validate_bandpass_eth_smoke,
    validate_sol_smoke as validate_bandpass_sol_smoke,
)
from backtest.path_b.stage16_dual_sol_bnb_v1.ehlers_twopole_hp_zero_v1 import (
    TwopoleHpParams,
    compute_signals as twopole_hp_signals,
    validate_bnb_smoke as validate_twopole_hp_bnb_smoke,
    validate_btc_smoke as validate_twopole_hp_btc_smoke,
    validate_eth_smoke as validate_twopole_hp_eth_smoke,
    validate_sol_smoke as validate_twopole_hp_sol_smoke,
)
from backtest.path_b.stage16_dual_sol_bnb_v1.three_line_break_flip_v1 import (
    ThreeLineBreakParams,
    compute_signals as three_line_break_signals,
    validate_bnb_smoke as validate_three_line_break_bnb_smoke,
    validate_btc_smoke as validate_three_line_break_btc_smoke,
    validate_eth_smoke as validate_three_line_break_eth_smoke,
    validate_sol_smoke as validate_three_line_break_sol_smoke,
)
from backtest.path_b.stage16_dual_sol_bnb_v1.wilder_swing_index_zero_v1 import (
    SwingIndexParams,
    compute_signals as swing_index_signals,
    validate_bnb_smoke as validate_swing_index_bnb_smoke,
    validate_btc_smoke as validate_swing_index_btc_smoke,
    validate_eth_smoke as validate_swing_index_eth_smoke,
    validate_sol_smoke as validate_swing_index_sol_smoke,
)
from backtest.path_b.stage16_dual_sol_bnb_v1.nison_kagi_yang_yin_flip_v1 import (
    KagiParams,
    compute_signals as kagi_signals,
    validate_bnb_smoke as validate_kagi_bnb_smoke,
    validate_btc_smoke as validate_kagi_btc_smoke,
    validate_eth_smoke as validate_kagi_eth_smoke,
    validate_sol_smoke as validate_kagi_sol_smoke,
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


def test_ehlers_bandpass_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.5)
    closes = [b.close for b in bars]
    bp = ehlers_bandpass(closes, period=20, bandwidth=0.3)
    assert len(bp) == len(bars)
    assert bp[0] == 0.0
    assert bp[1] == 0.0
    assert bp[5] is not None

    params_a = BandpassParams(mode="mode_a", period=20, bandwidth=0.3)
    buys_a, sells_a, stops_a = bandpass_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = BandpassParams(mode="mode_b", period=20, bandwidth=0.3, quality_threshold=0.1)
    buys_b, sells_b, stops_b = bandpass_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_bandpass_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_bandpass_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_p = BandpassParams(period=50)
    assert not validate_bandpass_btc_smoke(bad_p, "1h")[0]

    assert validate_bandpass_eth_smoke(params_a, "1h")[0]
    assert validate_bandpass_sol_smoke(params_a, "1h")[0]
    assert validate_bandpass_bnb_smoke(params_a, "1h")[0]


def test_ehlers_twopole_hp_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    closes = [b.close for b in bars]
    hp = ehlers_twopole_hp(closes, period=40)
    assert len(hp) == len(bars)
    assert hp[0] == 0.0
    assert hp[1] == 0.0
    assert hp[5] is not None

    params_a = TwopoleHpParams(mode="mode_a", period=40)
    buys_a, sells_a, stops_a = twopole_hp_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = TwopoleHpParams(mode="mode_b", period=40, quality_threshold=0.1)
    buys_b, sells_b, stops_b = twopole_hp_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    assert validate_twopole_hp_btc_smoke(params_a, "1h")[0]
    assert not validate_twopole_hp_btc_smoke(params_a, "15m")[0]
    bad_p = TwopoleHpParams(period=100)
    assert not validate_twopole_hp_btc_smoke(bad_p, "1h")[0]

    assert validate_twopole_hp_eth_smoke(params_a, "1h")[0]
    assert validate_twopole_hp_sol_smoke(params_a, "1h")[0]
    assert validate_twopole_hp_bnb_smoke(params_a, "1h")[0]


def test_three_line_break_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    closes = [b.close for b in bars]
    dirs, bulls, bears = three_line_break(closes, n=3)
    assert len(dirs) == len(bars)
    assert len(bulls) == len(bars)
    assert len(bears) == len(bars)

    params_a = ThreeLineBreakParams(mode="mode_a", n_lines=3)
    buys_a, sells_a, stops_a = three_line_break_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = ThreeLineBreakParams(mode="mode_b", n_lines=4)
    buys_b, sells_b, stops_b = three_line_break_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    assert validate_three_line_break_btc_smoke(params_a, "1h")[0]
    assert not validate_three_line_break_btc_smoke(params_a, "15m")[0]
    bad_n = ThreeLineBreakParams(n_lines=8)
    assert not validate_three_line_break_btc_smoke(bad_n, "1h")[0]

    assert validate_three_line_break_eth_smoke(params_a, "1h")[0]
    assert validate_three_line_break_sol_smoke(params_a, "1h")[0]
    assert validate_three_line_break_bnb_smoke(params_a, "1h")[0]


def test_wilder_swing_index_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    si = wilder_swing_index(opens, highs, lows, closes, atr_len=14)
    assert len(si) == len(bars)
    assert si[0] is None
    assert si[1] is not None

    params_a = SwingIndexParams(mode="mode_a", atr_len=14)
    buys_a, sells_a, stops_a = swing_index_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = SwingIndexParams(mode="mode_b", atr_len=14, quality_threshold=5.0)
    buys_b, sells_b, stops_b = swing_index_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    assert validate_swing_index_btc_smoke(params_a, "1h")[0]
    assert not validate_swing_index_btc_smoke(params_a, "15m")[0]
    bad_len = SwingIndexParams(atr_len=50)
    assert not validate_swing_index_btc_smoke(bad_len, "1h")[0]

    assert validate_swing_index_eth_smoke(params_a, "1h")[0]
    assert validate_swing_index_sol_smoke(params_a, "1h")[0]
    assert validate_swing_index_bnb_smoke(params_a, "1h")[0]


def test_nison_kagi_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    dirs, yys, yang_flips, yin_flips = nison_kagi(closes, highs=highs, lows=lows, atr_mult=1.0, atr_len=14)
    assert len(dirs) == len(bars)
    assert len(yys) == len(bars)
    assert len(yang_flips) == len(bars)
    assert len(yin_flips) == len(bars)

    params_a = KagiParams(mode="mode_a", atr_mult=1.0, atr_len=14)
    buys_a, sells_a, stops_a = kagi_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)

    params_b = KagiParams(mode="mode_b", atr_mult=1.5, atr_len=14)
    buys_b, sells_b, stops_b = kagi_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    assert validate_kagi_btc_smoke(params_a, "1h")[0]
    assert not validate_kagi_btc_smoke(params_a, "15m")[0]
    bad_mult = KagiParams(atr_mult=4.0)
    assert not validate_kagi_btc_smoke(bad_mult, "1h")[0]

    assert validate_kagi_eth_smoke(params_a, "1h")[0]
    assert validate_kagi_sol_smoke(params_a, "1h")[0]
    assert validate_kagi_bnb_smoke(params_a, "1h")[0]
