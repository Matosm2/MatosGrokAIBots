"""Unit tests for stage8-dual-sol-bnb-v1 indicators, signals, dual smokes, and retention rules."""

from __future__ import annotations

import math
from backtest.data import Bar
from backtest.indicators import (
    awesome_oscillator,
    pretty_good_oscillator,
    roc,
    wma,
)
from backtest.path_b.stage8_dual_sol_bnb_v1.ao_median_zero_cross_v1 import (
    AoMedianParams,
    compute_signals as ao_signals,
    validate_bnb_smoke as validate_ao_bnb_smoke,
    validate_sol_smoke as validate_ao_sol_smoke,
)
from backtest.path_b.stage8_dual_sol_bnb_v1.pgo_threshold_zeroexit_v1 import (
    PgoThresholdParams,
    compute_signals as pgo_signals,
    validate_bnb_smoke as validate_pgo_bnb_smoke,
    validate_sol_smoke as validate_pgo_sol_smoke,
)
from backtest.path_b.stage8_dual_sol_bnb_v1.roc_zero_cross_v1 import (
    RocZeroCrossParams,
    compute_signals as roc_signals,
    validate_bnb_smoke as validate_roc_bnb_smoke,
    validate_sol_smoke as validate_roc_sol_smoke,
)
from backtest.path_b.stage8_dual_sol_bnb_v1.wma_fast_slow_cross_v1 import (
    WmaCrossParams,
    compute_signals as wma_signals,
    validate_bnb_smoke as validate_wma_bnb_smoke,
    validate_sol_smoke as validate_wma_sol_smoke,
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


def test_awesome_oscillator():
    bars = _make_dummy_bars(60, trend=0.5)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    ao = awesome_oscillator(highs, lows, fast_length=5, slow_length=34)
    assert len(ao) == 60
    # Before slow_length (34), ao should be None
    assert ao[0] is None
    assert ao[32] is None
    assert ao[33] is not None
    # In upward trend, fast SMA > slow SMA -> AO > 0
    assert ao[50] is not None
    assert ao[50] > 0.0


def test_pretty_good_oscillator():
    bars = _make_dummy_bars(60, trend=1.0)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    pgo = pretty_good_oscillator(highs, lows, closes, length=14)
    assert len(pgo) == 60
    assert pgo[0] is None
    # After length=14 bars, pgo should be valid and positive in strong uptrend
    assert pgo[20] is not None
    assert pgo[20] > 0.0


def test_roc_indicator():
    closes = [100.0 + i * 1.0 for i in range(30)]
    roc_vals = roc(closes, length=12)
    assert len(roc_vals) == 30
    assert roc_vals[11] is None
    assert roc_vals[12] is not None
    # 100 * (112.0 / 100.0 - 1) = 12.0
    assert abs(roc_vals[12] - 12.0) < 1e-4


def test_wma_indicator():
    closes = [10.0, 20.0, 30.0, 40.0]
    # WMA(3) at index 2: (10*1 + 20*2 + 30*3)/(1+2+3) = (10 + 40 + 90)/6 = 140/6 = 23.3333
    w = wma(closes, 3)
    assert len(w) == 4
    assert w[0] is None
    assert w[1] is None
    assert w[2] is not None
    assert abs(w[2] - (140.0 / 6.0)) < 1e-4


def test_ao_median_smokes():
    # Valid
    p = AoMedianParams(fast_len=5, slow_len=34)
    s_ok, _ = validate_ao_sol_smoke(p, "1h")
    b_ok, _ = validate_ao_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # Forbidden Af <= 3 on 15m
    p_spam = AoMedianParams(fast_len=3, slow_len=34)
    s_ok, msg = validate_ao_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "Af<=3 forbidden" in msg

    # Invalid Af >= As
    p_inv = AoMedianParams(fast_len=34, slow_len=5)
    s_ok, msg = validate_ao_sol_smoke(p_inv, "1h")
    assert not s_ok
    assert "not in locked set" in msg


def test_pgo_smokes():
    p = PgoThresholdParams(length=14, threshold=2.5)
    s_ok, _ = validate_pgo_sol_smoke(p, "1h")
    b_ok, _ = validate_pgo_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # N >= 89 on 15m forbidden
    p_spam = PgoThresholdParams(length=89, threshold=2.5)
    s_ok, msg = validate_pgo_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "N>=89 on 15m forbidden" in msg


def test_roc_smokes():
    p = RocZeroCrossParams(length=12)
    s_ok, _ = validate_roc_sol_smoke(p, "1h")
    b_ok, _ = validate_roc_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # N <= 3 on 15m forbidden
    p_spam = RocZeroCrossParams(length=3)
    s_ok, msg = validate_roc_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "N<=3 forbidden" in msg


def test_wma_smokes():
    p = WmaCrossParams(fast_len=10, slow_len=30)
    s_ok, _ = validate_wma_sol_smoke(p, "1h")
    b_ok, _ = validate_wma_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # (3, 8) on 15m forbidden
    p_spam = WmaCrossParams(fast_len=3, slow_len=8)
    s_ok, msg = validate_wma_sol_smoke(p_spam, "15m")
    assert not s_ok
    assert "(3,8) forbidden" in msg


def test_signal_generation():
    bars = _make_dummy_bars(150, v_reversal=True)

    # Strategy 1: AO
    b1, s1, st1 = ao_signals(bars, AoMedianParams(mode="mode_a", fast_len=5, slow_len=21))
    assert len(b1) == len(bars)
    assert any(b1), "AO Mode A should generate buy signals on V-reversal"

    # Strategy 2: PGO
    b2, s2, st2 = pgo_signals(bars, PgoThresholdParams(mode="mode_a", length=14, threshold=2.0))
    assert len(b2) == len(bars)

    # Strategy 3: ROC
    b3, s3, st3 = roc_signals(bars, RocZeroCrossParams(mode="mode_a", length=12))
    assert len(b3) == len(bars)
    assert any(b3), "ROC Mode A should generate buy signals on V-reversal"

    # Strategy 4: WMA
    b4, s4, st4 = wma_signals(bars, WmaCrossParams(mode="mode_a", fast_len=9, slow_len=21))
    assert len(b4) == len(bars)
    assert any(b4), "WMA Mode A should generate buy signals on V-reversal"
