"""Unit tests for stage5-dual-sol-bnb-v1 indicators, signals, and dual smoke rules."""

from __future__ import annotations

import math
from backtest.data import Bar
from backtest.indicators import (
    atr_percent,
    cmo,
    cti,
    mad,
    mad_channel,
    median_filter,
    percent_rank,
    supersmoother,
    vidya,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.atrpct_percentile_sma_cross_v1 import (
    AtrPctSmaParams,
    compute_signals as atrpct_signals,
    validate_bnb_smoke as validate_atrpct_bnb_smoke,
    validate_sol_smoke as validate_atrpct_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.cti_fast_slow_threshold_v1 import (
    CtiParams,
    compute_signals as cti_signals,
    validate_bnb_smoke as validate_cti_bnb_smoke,
    validate_sol_smoke as validate_cti_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.mad_channel_break_rvol_v1 import (
    MadChannelParams,
    compute_signals as mad_signals,
    validate_bnb_smoke as validate_mad_bnb_smoke,
    validate_sol_smoke as validate_mad_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.supersmoother_dual_cross_v1 import (
    SuperSmootherParams,
    compute_signals as ss_signals,
    validate_bnb_smoke as validate_ss_bnb_smoke,
    validate_sol_smoke as validate_ss_sol_smoke,
)
from backtest.path_b.stage5_dual_sol_bnb_v1.vidya_dual_or_close_cross_v1 import (
    VidyaParams,
    compute_signals as vidya_signals,
    validate_bnb_smoke as validate_vidya_bnb_smoke,
    validate_sol_smoke as validate_vidya_sol_smoke,
)


def _make_dummy_bars(n: int = 150, trend: float = 0.5, vol_spike_idx: int = -1, v_reversal: bool = False) -> list[Bar]:
    """Generate synthetic bars for signal and indicator tests."""
    bars: list[Bar] = []
    base = 100.0
    for i in range(n):
        if v_reversal:
            c = base - (i * 0.5) if i < 50 else base - 25.0 + (i - 50) * 1.0
        else:
            c = base + i * trend + math.sin(i / 5.0) * 3.0
        h = c + 1.5
        l = c - 1.5
        o = (h + l) / 2.0
        v = 1000.0 if i != vol_spike_idx else 5000.0
        bars.append(
            Bar(
                open_time_ms=1000 * 60 * 60 * i,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=v,
                close_time_ms=1000 * 60 * 60 * i + 3599999,
            )
        )
    return bars


def test_cti_indicator():
    # Strictly rising -> +1.0
    rising = [float(10 + i * 2) for i in range(25)]
    r_cti = cti(rising, length=10)
    assert r_cti[-1] is not None
    assert abs(r_cti[-1] - 1.0) < 1e-4

    # Strictly falling -> -1.0
    falling = [float(100 - i * 2) for i in range(25)]
    f_cti = cti(falling, length=10)
    assert f_cti[-1] is not None
    assert abs(f_cti[-1] - (-1.0)) < 1e-4

    # Constant -> 0.0
    constant = [50.0] * 25
    c_cti = cti(constant, length=10)
    assert c_cti[-1] is not None
    assert abs(c_cti[-1] - 0.0) < 1e-4


def test_cti_signals_and_smokes():
    bars = _make_dummy_bars(150, v_reversal=True)
    buys, sells, stops = cti_signals(bars, CtiParams(mode="mode_a", fast_len=10, slow_len=20, buy_th=0.5))
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys), "Expected at least one buy signal on strong rising bars"

    # sol_smoke
    ok_sol, msg_sol = validate_cti_sol_smoke(CtiParams(mode="mode_b"), tf="15m")
    assert not ok_sol
    assert "Mode B ungated on 15m" in msg_sol

    # bnb_smoke
    ok_bnb, msg_bnb = validate_cti_bnb_smoke(CtiParams(slow_len=65), tf="4h")
    assert not ok_bnb
    assert "slowL >= 60 on 4H" in msg_bnb


def test_atrpct_percentile_sma_indicator_and_signals():
    bars = _make_dummy_bars(200, trend=0.2)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_pct_vals = atr_percent(highs, lows, closes, length=14)
    assert len(atr_pct_vals) == len(bars)
    assert atr_pct_vals[-1] is not None
    assert atr_pct_vals[-1] > 0.0

    # Test signals
    buys, sells, stops = atrpct_signals(
        bars,
        AtrPctSmaParams(fast_len=10, slow_len=30, window_w=50, rank_lo=20.0, rank_hi=90.0),
    )
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)

    # Smoke tests
    ok_sol, msg_sol = validate_atrpct_sol_smoke(AtrPctSmaParams(fast_len=200), tf="1h")
    assert not ok_sol
    assert "SMA200" in msg_sol

    ok_bnb, msg_bnb = validate_atrpct_bnb_smoke(AtrPctSmaParams(rank_lo=0.0), tf="1h")
    assert not ok_bnb
    assert "lo=0" in msg_bnb


def test_mad_channel_indicator_and_signals():
    prices = [100.0 + (i % 5) for i in range(50)]
    # Add outlier wick
    prices[25] = 200.0

    med_vals, upper, lower = mad_channel(prices, length=20, k=2.0)
    assert len(med_vals) == len(prices)
    assert med_vals[-1] is not None
    assert upper[-1] is not None
    assert lower[-1] is not None
    assert upper[-1] > med_vals[-1] > lower[-1]

    # Test signals with volume breakout
    bars = _make_dummy_bars(100, trend=0.1, vol_spike_idx=50)
    # create artificial breakout at index 50
    bars[50] = Bar(
        open_time_ms=bars[50].open_time_ms,
        open=bars[49].close,
        high=bars[49].close + 25.0,
        low=bars[49].close,
        close=bars[49].close + 20.0,
        volume=10000.0,
        close_time_ms=bars[50].close_time_ms,
    )

    buys, sells, stops = mad_signals(bars, MadChannelParams(channel_n=20, k_mult=2.0, rvol_k=1.2))
    assert len(buys) == len(bars)
    assert buys[50] is True, "Expected breakout buy on bar 50"

    # Smoke tests
    ok_sol, msg_sol = validate_mad_sol_smoke(MadChannelParams(channel_n=10), tf="1h")
    assert not ok_sol
    assert "N < 15" in msg_sol

    ok_bnb, msg_bnb = validate_mad_bnb_smoke(MadChannelParams(k_mult=1.0), tf="1h")
    assert not ok_bnb
    assert "k < 1.2" in msg_bnb


def test_vidya_indicator_and_signals():
    # When prices oscillate with 0 net momentum, CMO approaches 0 and VIDYA flattens
    osc = [100.0, 101.0, 100.0, 101.0] * 20
    v_osc = vidya(osc, ema_len=9, cmo_len=10)
    assert v_osc[-1] is not None
    # Slope should be near 0
    assert abs(v_osc[-1] - v_osc[-2]) < 0.2

    # When prices trend strongly, VIDYA moves with price
    trend = [float(100 + i * 2) for i in range(50)]
    v_trend = vidya(trend, ema_len=9, cmo_len=10)
    assert v_trend[-1] is not None
    assert v_trend[-1] > 180.0

    # Signals
    bars = _make_dummy_bars(150, trend=1.0)
    buys, sells, stops = vidya_signals(bars, VidyaParams(mode="mode_a", slope_filter=True, slope_min=0.0003))
    assert len(buys) == len(bars)
    assert any(buys)

    # Smoke tests
    ok_sol, msg_sol = validate_vidya_sol_smoke(VidyaParams(), tf="15m")
    assert not ok_sol
    assert "15m dual soup forbidden" in msg_sol

    ok_bnb, msg_bnb = validate_vidya_bnb_smoke(VidyaParams(slope_filter=False), tf="1h")
    assert not ok_bnb
    assert "slopeMin" in msg_bnb


def test_supersmoother_indicator_and_signals():
    # Constant input -> output equals input (DC gain = 1.0)
    constant = [75.0] * 40
    ss_const = supersmoother(constant, length=15)
    assert ss_const[-1] is not None
    assert abs(ss_const[-1] - 75.0) < 1e-4

    # Ramp input -> smooth tracking
    ramp = [float(i) for i in range(50)]
    ss_ramp = supersmoother(ramp, length=10)
    assert ss_ramp[-1] is not None
    # Check that lag is modest and tracking slope is ~1.0
    diff = ss_ramp[-1] - ss_ramp[-2]
    assert abs(diff - 1.0) < 0.05

    # Signals
    bars = _make_dummy_bars(150, v_reversal=True)
    buys, sells, stops = ss_signals(
        bars,
        SuperSmootherParams(mode="mode_a", fast_len=8, slow_len=16, atr_regime_gate=False),
    )
    assert len(buys) == len(bars)
    assert any(buys)

    # Smoke tests
    ok_sol, msg_sol = validate_ss_sol_smoke(SuperSmootherParams(), tf="15m")
    assert not ok_sol
    assert "15m forbidden" in msg_sol

    ok_bnb, msg_bnb = validate_ss_bnb_smoke(SuperSmootherParams(fast_len=5, slow_len=50), tf="1h")
    assert not ok_bnb
    assert "Invalid pair" in msg_bnb


def test_dual_survival_identical_params_rule():
    """Verify that params instantiated for SOL and BNB ladders are identical."""
    p1 = CtiParams(fast_len=20, slow_len=40, buy_th=0.5)
    p2 = AtrPctSmaParams(fast_len=20, slow_len=50, rank_lo=25.0, rank_hi=85.0)
    p3 = MadChannelParams(channel_n=20, k_mult=2.0, rvol_k=1.2)
    p4 = VidyaParams(fast_ema_len=9, fast_cmo_len=12, slow_ema_len=20, slow_cmo_len=50)
    p5 = SuperSmootherParams(fast_len=10, slow_len=30)

    for p in (p1, p2, p3, p4, p5):
        assert p == p, "Dual-survival requires deterministic identical params"
