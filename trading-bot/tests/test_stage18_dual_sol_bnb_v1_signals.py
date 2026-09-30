"""Unit tests for stage18-dual-sol-bnb-v1 signals, indicators, and smoke tests."""

from __future__ import annotations

import pytest

from backtest.data import Bar
from backtest.indicators import (
    detrended_price_oscillator,
    forecast_oscillator,
    percentage_price_oscillator,
    projection_oscillator,
    vertical_horizontal_filter,
)
from backtest.path_b.stage18_dual_sol_bnb_v1.dpo_zero_cross_v1 import (
    DpoParams,
    compute_signals as dpo_signals,
    validate_bnb_smoke as validate_dpo_bnb_smoke,
    validate_btc_smoke as validate_dpo_btc_smoke,
    validate_eth_smoke as validate_dpo_eth_smoke,
    validate_sol_smoke as validate_dpo_sol_smoke,
)
from backtest.path_b.stage18_dual_sol_bnb_v1.ppo_ema_signal_cross_v1 import (
    PpoParams,
    compute_signals as ppo_signals,
    validate_bnb_smoke as validate_ppo_bnb_smoke,
    validate_btc_smoke as validate_ppo_btc_smoke,
    validate_eth_smoke as validate_ppo_eth_smoke,
    validate_sol_smoke as validate_ppo_sol_smoke,
)
from backtest.path_b.stage18_dual_sol_bnb_v1.vhf_threshold_close_dir_v1 import (
    VhfParams,
    compute_signals as vhf_signals,
    validate_bnb_smoke as validate_vhf_bnb_smoke,
    validate_btc_smoke as validate_vhf_btc_smoke,
    validate_eth_smoke as validate_vhf_eth_smoke,
    validate_sol_smoke as validate_vhf_sol_smoke,
)
from backtest.path_b.stage18_dual_sol_bnb_v1.forecast_oscillator_zero_v1 import (
    FoscParams,
    compute_signals as fosc_signals,
    validate_bnb_smoke as validate_fosc_bnb_smoke,
    validate_btc_smoke as validate_fosc_btc_smoke,
    validate_eth_smoke as validate_fosc_eth_smoke,
    validate_sol_smoke as validate_fosc_sol_smoke,
)
from backtest.path_b.stage18_dual_sol_bnb_v1.projection_oscillator_trigger_cross_v1 import (
    ProjectionOscParams,
    compute_signals as projection_osc_signals,
    validate_bnb_smoke as validate_projection_osc_bnb_smoke,
    validate_btc_smoke as validate_projection_osc_btc_smoke,
    validate_eth_smoke as validate_projection_osc_eth_smoke,
    validate_sol_smoke as validate_projection_osc_sol_smoke,
)


def _make_dummy_bars(n: int = 120, trend: float = 1.0) -> list[Bar]:
    import math

    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        # Sine wave swing to ensure multiple crossovers and crossunders
        swing = 15.0 * math.sin(i * 2.0 * math.pi / 25.0)
        c = base + i * trend + swing
        h = c + 4.0 + (1.0 if i % 3 == 0 else 0.0)
        l = c - 4.0
        o = c - 1.0
        bars.append(
            Bar(
                open_time_ms=i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=1000.0 + (i * 10.0),
                close_time_ms=(i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_dpo_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.5)
    closes = [b.close for b in bars]

    dpo = detrended_price_oscillator(closes, length=20)
    assert len(dpo) == len(bars)
    valid_dpo = [v for v in dpo if v is not None]
    assert len(valid_dpo) > 0
    # Must oscillate around zero
    assert any(v > 0 for v in valid_dpo)
    assert any(v < 0 for v in valid_dpo)

    params_a = DpoParams(mode="mode_a", length=20)
    buys_a, sells_a, stops_a = dpo_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert len(stops_a) == len(bars)
    assert any(buys_a)

    params_b = DpoParams(mode="mode_b", length=20, hold_bars=1, atr_trail_mult=2.0)
    buys_b, sells_b, stops_b = dpo_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_dpo_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_dpo_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_len, _ = validate_dpo_btc_smoke(DpoParams(length=55), "1h")
    assert not bad_btc_len

    ok_eth, _ = validate_dpo_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_dpo_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_dpo_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_ppo_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.2)
    closes = [b.close for b in bars]

    ppo, sig, hist = percentage_price_oscillator(closes, fast_length=12, slow_length=26, signal_length=9)
    assert len(ppo) == len(bars)
    assert len(sig) == len(bars)
    assert len(hist) == len(bars)
    valid_ppo = [v for v in ppo if v is not None]
    valid_sig = [v for v in sig if v is not None]
    assert len(valid_ppo) > 0
    assert len(valid_sig) > 0

    params_a = PpoParams(mode="mode_a", fast=12, slow=26, sig=9)
    buys_a, sells_a, stops_a = ppo_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert any(buys_a)

    params_b = PpoParams(mode="mode_b", fast=12, slow=26, sig=9, atr_trail_mult=2.0)
    buys_b, sells_b, stops_b = ppo_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_ppo_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_ppo_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_param, _ = validate_ppo_btc_smoke(PpoParams(fast=5, slow=13, sig=3), "1h")
    assert not bad_btc_param

    ok_eth, _ = validate_ppo_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_ppo_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_ppo_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_vhf_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.0)
    closes = [b.close for b in bars]

    vhf = vertical_horizontal_filter(closes, length=28)
    assert len(vhf) == len(bars)
    valid_vhf = [v for v in vhf if v is not None]
    assert len(valid_vhf) > 0
    # VHF is a ratio between 0 and 1
    assert all(0.0 <= v <= 1.0 for v in valid_vhf)

    params_a = VhfParams(mode="mode_a", n=28, thr=0.35, dir_len=3)
    buys_a, sells_a, stops_a = vhf_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)

    params_b = VhfParams(mode="mode_b", n=18, thr=0.30, dir_len=1, atr_trail_mult=2.0)
    buys_b, sells_b, stops_b = vhf_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_vhf_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_vhf_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_param, _ = validate_vhf_btc_smoke(VhfParams(n=70, thr=0.8), "1h")
    assert not bad_btc_param

    ok_eth, _ = validate_vhf_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_vhf_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_vhf_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_fosc_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.1)
    closes = [b.close for b in bars]

    fosc, tsf = forecast_oscillator(closes, length=14)
    assert len(fosc) == len(bars)
    assert len(tsf) == len(bars)
    valid_fosc = [v for v in fosc if v is not None]
    valid_tsf = [v for v in tsf if v is not None]
    assert len(valid_fosc) > 0
    assert len(valid_tsf) > 0
    # FOSC oscillates around 0
    assert any(v > 0 for v in valid_fosc)
    assert any(v < 0 for v in valid_fosc)

    params_a = FoscParams(mode="mode_a", length=14)
    buys_a, sells_a, stops_a = fosc_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert any(buys_a)

    params_b = FoscParams(mode="mode_b", length=14, sig_len=5, atr_trail_mult=2.0)
    buys_b, sells_b, stops_b = fosc_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_fosc_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_fosc_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_param, _ = validate_fosc_btc_smoke(FoscParams(length=55), "1h")
    assert not bad_btc_param

    ok_eth, _ = validate_fosc_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_fosc_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_fosc_bnb_smoke(params_a, "1h")
    assert ok_bnb


def test_projection_osc_indicator_and_signals():
    bars = _make_dummy_bars(80, trend=1.3)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    po, trig = projection_oscillator(highs, lows, closes, length=14, trigger_length=3)
    assert len(po) == len(bars)
    assert len(trig) == len(bars)
    valid_po = [v for v in po if v is not None]
    valid_trig = [v for v in trig if v is not None]
    assert len(valid_po) > 0
    assert len(valid_trig) > 0
    # PO is bounded in [0, 100]
    assert all(0.0 <= v <= 100.0 for v in valid_po)

    params_a = ProjectionOscParams(mode="mode_a", length=14, trig_len=3)
    buys_a, sells_a, stops_a = projection_osc_signals(bars, params_a)
    assert len(buys_a) == len(bars)
    assert len(sells_a) == len(bars)
    assert any(buys_a)

    params_b = ProjectionOscParams(mode="mode_b", length=14, trig_len=3, atr_trail_mult=2.0)
    buys_b, sells_b, stops_b = projection_osc_signals(bars, params_b)
    assert len(buys_b) == len(bars)

    # Smoke validation
    ok_btc, _ = validate_projection_osc_btc_smoke(params_a, "1h")
    assert ok_btc
    bad_btc_tf, _ = validate_projection_osc_btc_smoke(params_a, "15m")
    assert not bad_btc_tf
    bad_btc_param, _ = validate_projection_osc_btc_smoke(ProjectionOscParams(length=55, trig_len=3), "1h")
    assert not bad_btc_param

    ok_eth, _ = validate_projection_osc_eth_smoke(params_a, "1h")
    assert ok_eth
    ok_sol, _ = validate_projection_osc_sol_smoke(params_a, "1h")
    assert ok_sol
    ok_bnb, _ = validate_projection_osc_bnb_smoke(params_a, "1h")
    assert ok_bnb
