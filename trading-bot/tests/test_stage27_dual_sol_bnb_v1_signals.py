"""Unit tests for stage27-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    klinger_oscillator,
    percent_envelopes,
    qstick,
    schwager_volatility_ratio,
)
from backtest.path_b.stage27_dual_sol_bnb_v1.qstick_sma_zero_v1 import (
    QstickParams,
    compute_signals as qstick_signals,
    validate_bnb_smoke as validate_qstick_bnb_smoke,
    validate_btc_smoke as validate_qstick_btc_smoke,
    validate_eth_smoke as validate_qstick_eth_smoke,
    validate_sol_smoke as validate_qstick_sol_smoke,
)
from backtest.path_b.stage27_dual_sol_bnb_v1.klinger_signal_cross_v1 import (
    KlingerParams,
    compute_signals as klinger_signals,
    validate_bnb_smoke as validate_klinger_bnb_smoke,
    validate_btc_smoke as validate_klinger_btc_smoke,
    validate_eth_smoke as validate_klinger_eth_smoke,
    validate_sol_smoke as validate_klinger_sol_smoke,
)
from backtest.path_b.stage27_dual_sol_bnb_v1.percent_envelopes_break_v1 import (
    PercentEnvelopesParams,
    compute_signals as envelopes_signals,
    validate_bnb_smoke as validate_envelopes_bnb_smoke,
    validate_btc_smoke as validate_envelopes_btc_smoke,
    validate_eth_smoke as validate_envelopes_eth_smoke,
    validate_sol_smoke as validate_envelopes_sol_smoke,
)
from backtest.path_b.stage27_dual_sol_bnb_v1.schwager_vr_breakout_v1 import (
    SchwagerVrParams,
    compute_signals as schwager_signals,
    validate_bnb_smoke as validate_schwager_bnb_smoke,
    validate_btc_smoke as validate_schwager_btc_smoke,
    validate_eth_smoke as validate_schwager_eth_smoke,
    validate_sol_smoke as validate_schwager_sol_smoke,
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


def test_qstick_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    opens = [b.open for b in bars]
    closes = [b.close for b in bars]

    q_vals = qstick(opens, closes, n=8)
    assert len(q_vals) == len(bars)
    valid_q = [x for x in q_vals if x is not None]
    assert len(valid_q) > 100

    # Smoke validation
    params = QstickParams(mode="mode_a", n=8)
    ok, msg = validate_qstick_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_qstick_eth_smoke(params, "1h")[0]
    assert validate_qstick_sol_smoke(params, "1h")[0]
    assert validate_qstick_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_qstick_btc_smoke(params, "15m")[0]
    assert not validate_qstick_btc_smoke(QstickParams(n=25), "1h")[0]
    assert not validate_qstick_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = qstick_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_klinger_indicator_and_signals():
    bars = _make_dummy_bars(180, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    kvo_vals, sig_vals = klinger_oscillator(highs, lows, closes, volumes, fast=34, slow=55, signal_len=13)
    assert len(kvo_vals) == len(bars)
    assert len(sig_vals) == len(bars)
    valid_kvo = [x for x in kvo_vals if x is not None]
    valid_sig = [x for x in sig_vals if x is not None]
    assert len(valid_kvo) > 100
    assert len(valid_sig) > 80

    # Smoke validation
    params = KlingerParams(mode="mode_a", fast=34, slow=55, signal_len=13)
    ok, msg = validate_klinger_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_klinger_eth_smoke(params, "1h")[0]
    assert validate_klinger_sol_smoke(params, "1h")[0]
    assert validate_klinger_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_klinger_btc_smoke(params, "15m")[0]
    assert not validate_klinger_btc_smoke(KlingerParams(fast=10, slow=20), "1h")[0]
    assert not validate_klinger_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = klinger_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_percent_envelopes_indicator_and_signals():
    bars = _make_dummy_bars(150, trend=0.5)
    closes = [b.close for b in bars]

    mids, uppers, lowers = percent_envelopes(closes, length=20, pct=0.025)
    assert len(mids) == len(bars)
    assert len(uppers) == len(bars)
    assert len(lowers) == len(bars)

    for i in range(len(bars)):
        if mids[i] is not None:
            assert uppers[i] > mids[i]
            assert lowers[i] < mids[i]
            assert math.isclose(uppers[i], mids[i] * 1.025, rel_tol=1e-5)
            assert math.isclose(lowers[i], mids[i] * 0.975, rel_tol=1e-5)

    # Smoke validation
    params = PercentEnvelopesParams(mode="mode_a", length=20, pct=0.025)
    ok, msg = validate_envelopes_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_envelopes_eth_smoke(params, "1h")[0]
    assert validate_envelopes_sol_smoke(params, "1h")[0]
    assert validate_envelopes_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_envelopes_btc_smoke(params, "15m")[0]
    assert not validate_envelopes_btc_smoke(PercentEnvelopesParams(length=50), "1h")[0]
    assert not validate_envelopes_btc_smoke(PercentEnvelopesParams(pct=0.10), "1h")[0]
    assert not validate_envelopes_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = envelopes_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)


def test_schwager_vr_indicator_and_signals():
    bars = _make_dummy_bars(160, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    vr_vals, tr_list = schwager_volatility_ratio(highs, lows, closes, n=14)
    assert len(vr_vals) == len(bars)
    assert len(tr_list) == len(bars)
    valid_vr = [x for x in vr_vals if x is not None]
    assert len(valid_vr) > 100

    for v in valid_vr:
        assert v >= 0.0

    # Smoke validation
    params = SchwagerVrParams(mode="mode_a", n=14, thr=2.0, m=20)
    ok, msg = validate_schwager_btc_smoke(params, "1h")
    assert ok, f"BTC smoke failed: {msg}"
    assert validate_schwager_eth_smoke(params, "1h")[0]
    assert validate_schwager_sol_smoke(params, "1h")[0]
    assert validate_schwager_bnb_smoke(params, "1h")[0]

    # Smoke failure checks
    assert not validate_schwager_btc_smoke(params, "15m")[0]
    assert not validate_schwager_btc_smoke(SchwagerVrParams(n=50), "1h")[0]
    assert not validate_schwager_btc_smoke(SchwagerVrParams(thr=5.0), "1h")[0]
    assert not validate_schwager_btc_smoke(SchwagerVrParams(m=50), "1h")[0]
    assert not validate_schwager_sol_smoke(params, "15m")[0]

    # Signals
    buys, sells, stops = schwager_signals(bars, params)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert len(stops) == len(bars)
    for b, s in zip(buys, sells):
        assert not (b and s)
