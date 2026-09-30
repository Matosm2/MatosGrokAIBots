"""Unit tests for stage7-dual-sol-bnb-v1 indicators, signals, dual smokes, and retention rules."""

from __future__ import annotations

import math
from backtest.data import Bar
from backtest.indicators import (
    efficiency_ratio,
    ehlers_reverse_ema,
    ehlers_super_passband,
    rms,
    rwi_high_low,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.ehlers_reverse_ema_trend_cycle_v1 import (
    ReverseEmaParams,
    compute_signals as reverse_ema_signals,
    validate_bnb_smoke as validate_reverse_ema_bnb_smoke,
    validate_sol_smoke as validate_reverse_ema_sol_smoke,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.ehlers_super_passband_rms_v1 import (
    SuperPassbandParams,
    compute_signals as super_passband_signals,
    validate_bnb_smoke as validate_super_passband_bnb_smoke,
    validate_sol_smoke as validate_super_passband_sol_smoke,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.er_sma_gate_cross_v1 import (
    ErSmaParams,
    compute_signals as er_sma_signals,
    validate_bnb_smoke as validate_er_sma_bnb_smoke,
    validate_sol_smoke as validate_er_sma_sol_smoke,
)
from backtest.path_b.stage7_dual_sol_bnb_v1.rwi_high_low_threshold_v1 import (
    RwiParams,
    compute_signals as rwi_signals,
    validate_bnb_smoke as validate_rwi_bnb_smoke,
    validate_sol_smoke as validate_rwi_sol_smoke,
)


def _make_dummy_bars(n: int = 150, trend: float = 0.5, v_reversal: bool = False) -> list[Bar]:
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
        v = 100.0 + 10.0 * math.sin(i / 3.0)
        bars.append(
            Bar(
                open_time_ms=1700000000000 + i * 3600000,
                open=o,
                high=h,
                low=l,
                close=c,
                volume=v,
                close_time_ms=1700000000000 + (i + 1) * 3600000 - 1,
            )
        )
    return bars


def test_er_indicator():
    # Linear upward trend: ER should be close to 1.0
    closes = [100.0 + i * 1.0 for i in range(50)]
    er = efficiency_ratio(closes, 10)
    assert len(er) == 50
    assert er[10] is not None
    assert abs(er[10] - 1.0) < 1e-6

    # Chop / back and forth: ER should be low
    chop_closes = [100.0 if i % 2 == 0 else 101.0 for i in range(50)]
    er_chop = efficiency_ratio(chop_closes, 10)
    assert er_chop[10] is not None
    assert er_chop[10] < 0.20


def test_ehlers_super_passband_rms():
    bars = _make_dummy_bars(100, trend=0.2)
    closes = [b.close for b in bars]
    pb = ehlers_super_passband(closes, p1=30, p2=50)
    assert len(pb) == 100
    assert pb[0] == 0.0
    assert pb[-1] is not None

    r = rms(pb, 40)
    assert len(r) == 100
    # After 40 bars, rms should be non-negative float
    assert r[50] is not None
    assert r[50] >= 0.0


def test_rwi_high_low():
    bars = _make_dummy_bars(100, trend=1.0)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    rwi_h, rwi_l = rwi_high_low(highs, lows, closes, max_lookback=40)
    assert len(rwi_h) == 100
    assert len(rwi_l) == 100
    # In strong uptrend, RWI High should exceed 1.0
    assert rwi_h[50] is not None
    assert rwi_h[50] > 1.0


def test_ehlers_reverse_ema():
    closes = [100.0 + i * 0.5 for i in range(60)]
    wave_trend = ehlers_reverse_ema(closes, alpha=0.05)
    wave_cycle = ehlers_reverse_ema(closes, alpha=0.30)
    assert len(wave_trend) == 60
    assert len(wave_cycle) == 60
    assert wave_trend[-1] is not None
    assert wave_cycle[-1] is not None


def test_er_sma_smokes():
    # Valid
    p = ErSmaParams(fast_len=10, slow_len=30, er_len=10, er_threshold=0.35)
    s_ok, _ = validate_er_sma_sol_smoke(p, "1h")
    b_ok, _ = validate_er_sma_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # Forbidden thr on 15m
    p_spam = ErSmaParams(er_threshold=0.15)
    s_ok, msg = validate_er_sma_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "thr<=0.15" in msg

    # Invalid fast >= slow
    p_inv = ErSmaParams(fast_len=30, slow_len=10)
    b_ok, msg = validate_er_sma_bnb_smoke(p_inv, "1h")
    assert not b_ok
    assert "fast_len >= slow_len" in msg


def test_super_passband_smokes():
    p = SuperPassbandParams(p1=30, p2=50, rms_len=50)
    s_ok, _ = validate_super_passband_sol_smoke(p, "1h")
    b_ok, _ = validate_super_passband_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # P1 >= P2 forbidden
    p_inv = SuperPassbandParams(p1=50, p2=30)
    s_ok, msg = validate_super_passband_sol_smoke(p_inv, "1h")
    assert not s_ok
    assert "P1 must be strictly < P2" in msg


def test_rwi_smokes():
    p = RwiParams(short_len=7, long_len=64, threshold=1.0)
    s_ok, _ = validate_rwi_sol_smoke(p, "1h")
    b_ok, _ = validate_rwi_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # S <= 2 on 15m forbidden
    p_spam = RwiParams(short_len=2, long_len=64)
    s_ok, msg = validate_rwi_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "S<=2" in msg


def test_reverse_ema_smokes():
    p = ReverseEmaParams(alpha_trend=0.05, alpha_cycle=0.30)
    s_ok, _ = validate_reverse_ema_sol_smoke(p, "1h")
    b_ok, _ = validate_reverse_ema_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # alpha_c >= 0.5 on 15m forbidden
    p_spam = ReverseEmaParams(alpha_trend=0.05, alpha_cycle=0.50)
    s_ok, msg = validate_reverse_ema_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "alpha_cycle>=0.5" in msg


def test_signals_execution():
    bars = _make_dummy_bars(120, trend=0.8, v_reversal=True)

    # Strategy 1
    buys1, sells1, stops1 = er_sma_signals(bars)
    assert len(buys1) == 120
    assert len(sells1) == 120

    # Strategy 2
    buys2, sells2, stops2 = super_passband_signals(bars)
    assert len(buys2) == 120
    assert len(sells2) == 120

    # Strategy 3
    buys3, sells3, stops3 = rwi_signals(bars)
    assert len(buys3) == 120
    assert len(sells3) == 120

    # Strategy 4
    buys4, sells4, stops4 = reverse_ema_signals(bars)
    assert len(buys4) == 120
    assert len(sells4) == 120
