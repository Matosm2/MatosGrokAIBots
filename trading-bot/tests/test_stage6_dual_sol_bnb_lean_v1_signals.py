"""Unit tests for stage6-dual-sol-bnb-lean-v1 indicators, signals, dual smokes, and retention rules."""

from __future__ import annotations

import math
from backtest.data import Bar
from backtest.indicators import (
    frama,
    hma,
    mcginley_dynamic,
    wma,
)
from backtest.path_b.stage6_dual_sol_bnb_lean_v1.frama_fast_slow_cross_v1 import (
    FramaParams,
    compute_signals as frama_signals,
    validate_bnb_smoke as validate_frama_bnb_smoke,
    validate_sol_smoke as validate_frama_sol_smoke,
)
from backtest.path_b.stage6_dual_sol_bnb_lean_v1.hma_dual_cross_v1 import (
    HmaParams,
    compute_signals as hma_signals,
    validate_bnb_smoke as validate_hma_bnb_smoke,
    validate_sol_smoke as validate_hma_sol_smoke,
)
from backtest.path_b.stage6_dual_sol_bnb_lean_v1.mcginley_close_slope_cross_v1 import (
    McGinleyParams,
    compute_signals as mcginley_signals,
    validate_bnb_smoke as validate_mcginley_bnb_smoke,
    validate_sol_smoke as validate_mcginley_sol_smoke,
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


def test_frama_indicator():
    bars = _make_dummy_bars(100, trend=0.8)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    f_fast = frama(highs, lows, closes, length=16)
    f_slow = frama(highs, lows, closes, length=32)

    assert len(f_fast) == 100
    assert len(f_slow) == 100
    # Warmup check: length-1 bars should be None
    assert f_fast[0] is None
    assert f_fast[14] is None
    assert f_fast[15] is not None
    assert f_slow[30] is None
    assert f_slow[31] is not None
    # Trending upwards: frama should follow close closely
    assert f_fast[-1] > f_fast[15]


def test_hma_indicator():
    closes = [100.0 + i * 0.5 for i in range(50)]
    h = hma(closes, 9)
    assert len(h) == 50
    assert h[-1] is not None
    # HMA should lag less than regular SMA/WMA
    assert h[-1] > closes[40]


def test_mcginley_dynamic_indicator():
    closes = [100.0 + i * 1.0 for i in range(50)]
    md = mcginley_dynamic(closes, length=14, k=1.0)
    assert len(md) == 50
    assert md[0] == closes[0]
    # MD should hug upward trend
    assert md[-1] > md[0]
    # MD slope is positive in strong uptrend
    assert md[-1] > md[-2]


def test_frama_smokes():
    # Valid Mode A
    p = FramaParams(mode="mode_a", fast_len=16, slow_len=32)
    s_ok, _ = validate_frama_sol_smoke(p, "1h")
    b_ok, _ = validate_frama_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # Odd length forbidden
    p_odd = FramaParams(mode="mode_a", fast_len=15, slow_len=30)
    s_ok, msg = validate_frama_sol_smoke(p_odd, "1h")
    assert not s_ok
    assert "odd N" in msg

    # Nf <= 6 on 1h forbidden for bnb_smoke
    p_spam = FramaParams(mode="mode_a", fast_len=6, slow_len=12)
    b_ok, msg = validate_frama_bnb_smoke(p_spam, "1h")
    assert not b_ok
    assert "Nf<=6" in msg


def test_hma_smokes():
    p = HmaParams(mode="mode_a", fast_len=9, slow_len=16)
    s_ok, _ = validate_hma_sol_smoke(p, "1h")
    b_ok, _ = validate_hma_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # 15m soup forbidden on SOL
    s_ok, msg = validate_hma_sol_smoke(p, "15m")
    assert not s_ok
    assert "15m" in msg

    # Lf <= 5 forbidden on BNB
    p_short = HmaParams(mode="mode_a", fast_len=5, slow_len=16)
    b_ok, msg = validate_hma_bnb_smoke(p_short, "1h")
    assert not b_ok
    assert "Lf<=5" in msg


def test_mcginley_smokes():
    p = McGinleyParams(mode="mode_a", length=14)
    s_ok, _ = validate_mcginley_sol_smoke(p, "1h")
    b_ok, _ = validate_mcginley_bnb_smoke(p, "1h")
    assert s_ok and b_ok

    # N not in locked set
    p_bad = McGinleyParams(mode="mode_a", length=25)
    s_ok, msg = validate_mcginley_sol_smoke(p_bad, "1h")
    assert not s_ok
    assert "not in locked set" in msg


def test_frama_signals_reversal():
    # Uptrend followed by downtrend and reversal
    bars = _make_dummy_bars(120, trend=0.8, v_reversal=False)
    # Add a dip and rebound
    for i in range(40, 70):
        bars[i] = Bar(
            open_time_ms=bars[i].open_time_ms,
            open=bars[i].open - 20.0,
            high=bars[i].high - 20.0,
            low=bars[i].low - 20.0,
            close=bars[i].close - 20.0,
            volume=bars[i].volume,
            close_time_ms=bars[i].close_time_ms,
        )
    p = FramaParams(mode="mode_a", fast_len=10, slow_len=20)
    buys, sells, stops = frama_signals(bars, p)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys)


def test_hma_signals_reversal():
    bars = _make_dummy_bars(120, v_reversal=True)
    p = HmaParams(mode="mode_a", fast_len=9, slow_len=16)
    buys, sells, stops = hma_signals(bars, p)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys)


def test_mcginley_signals_reversal():
    bars = _make_dummy_bars(120, v_reversal=True)
    p = McGinleyParams(mode="mode_a", length=14)
    buys, sells, stops = mcginley_signals(bars, p)
    assert len(buys) == len(bars)
    assert len(sells) == len(bars)
    assert any(buys)
