"""Unit tests for stage4-bnb-first-v1 indicators, strategies, and BNB smoke rules."""

from __future__ import annotations

import math

from backtest.data import Bar
from backtest.indicators import (
    crossover,
    crossunder,
    eom,
    pivothigh,
    pivotlow,
    pvo,
    rvol,
    zlema,
)
from backtest.path_b.stage4_bnb_first_v1.emv_zero_rvol_atr_gate_v1 import (
    EmvGateParams,
    compute_signals as emv_signals,
)
from backtest.path_b.stage4_bnb_first_v1.p4h_hl_accept_break_v1 import (
    FOUR_HOURS_MS,
    P4HParams,
    compute_signals as p4h_signals,
)
from backtest.path_b.stage4_bnb_first_v1.pvo_gate_sma_mom_v1 import (
    PvoMomParams,
    compute_signals as pvo_signals,
)
from backtest.path_b.stage4_bnb_first_v1.rvol_pivot_structure_break_v1 import (
    RvolPivotParams,
    compute_signals as rvol_pivot_signals,
)
from backtest.path_b.stage4_bnb_first_v1.sweep import (
    validate_emv_bnb_smoke,
    validate_p4h_bnb_smoke,
    validate_pvo_bnb_smoke,
    validate_rvol_pivot_bnb_smoke,
    validate_zlema_bnb_smoke,
)
from backtest.path_b.stage4_bnb_first_v1.zlema_sma_cross_v1 import (
    ZlemaSmaParams,
    compute_signals as zlema_signals,
)


def _make_dummy_bars(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 3_600_000,  # 1h step
    vol: float = 1000.0,
    t0: int = 1_704_067_200_000,  # 2024-01-01 00:00 UTC (Monday)
) -> list[Bar]:
    out: list[Bar] = []
    for i, (o, h, lo, c) in enumerate(rows):
        out.append(
            Bar(
                open_time_ms=t0 + i * step_ms,
                open=o,
                high=h,
                low=lo,
                close=c,
                volume=vol + (i % 5) * 100.0,
                close_time_ms=t0 + (i + 1) * step_ms - 1,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Indicator Primitive Unit Tests
# ---------------------------------------------------------------------------

def test_rvol_calculation():
    volumes = [100.0] * 20 + [300.0]
    out = rvol(volumes, length=20)
    assert out[18] is None
    # Bar 19: SMA(volumes, 20) = 100.0, vol = 100.0 -> RVOL = 1.0
    assert abs(out[19] - 1.0) < 1e-5
    # Bar 20: sum of last 20 = 19*100 + 300 = 2200, SMA = 110.0, vol = 300.0 -> RVOL = 300 / 110
    expected_sma = (19 * 100.0 + 300.0) / 20.0
    assert abs(out[20] - (300.0 / expected_sma)) < 1e-5


def test_pivothigh_pivotlow():
    highs = [10.0, 12.0, 15.0, 11.0, 9.0, 8.0]
    lows = [9.0, 11.0, 14.0, 10.0, 8.0, 7.0]
    # left=2, right=2 -> at index 4 (5th bar), index 2 (15.0) is confirmed pivot high
    ph = pivothigh(highs, left=2, right=2)
    assert ph[0] is None
    assert ph[1] is None
    assert ph[2] is None
    assert ph[3] is None
    assert ph[4] == 15.0
    assert ph[5] is None

    # Check pivot low
    lows2 = [10.0, 8.0, 5.0, 7.0, 9.0]
    pl = pivotlow(lows2, left=2, right=2)
    assert pl[4] == 5.0


def test_eom_calculation():
    # Distance moved positive with small volume -> large positive EMV
    highs = [100.0, 105.0, 110.0, 115.0]
    lows = [95.0, 100.0, 105.0, 110.0]
    vols = [1000.0, 1000.0, 1000.0, 1000.0]
    out = eom(highs, lows, vols, length=2, divisor=1e6)
    assert out[0] is None
    # For length=2 SMA, index 1 has sum of raw_emv[0] (0.0) + raw_emv[1]
    assert out[1] is not None
    assert out[2] is not None
    assert out[2] > 0.0  # upward movement produces positive EMV


def test_pvo_calculation():
    # Constant volume -> fast EMA equals slow EMA -> PVO equals 0
    vols = [1000.0] * 50
    pvo_vals, sig_vals = pvo(vols, fast_len=12, slow_len=26, signal_len=9)
    valid_pvo = [p for p in pvo_vals if p is not None]
    assert len(valid_pvo) > 0
    for p in valid_pvo:
        assert abs(p) < 1e-4

    # Rising volume produces positive PVO
    rising_vols = [100.0 * (1.1 ** i) for i in range(50)]
    pvo_rising, _ = pvo(rising_vols, fast_len=12, slow_len=26, signal_len=9)
    valid_rising = [p for p in pvo_rising if p is not None]
    assert len(valid_rising) > 10
    assert all(p > 0.0 for p in valid_rising[-10:])


def test_zlema_calculation():
    # Flat price input produces constant ZLEMA
    flat = [100.0] * 40
    out = zlema(flat, length=10)
    valid = [v for v in out if v is not None]
    assert len(valid) > 0
    for v in valid:
        assert abs(v - 100.0) < 1e-5

    # Ascending price input should produce monotonic increasing ZLEMA
    asc = [float(100 + i * 2) for i in range(50)]
    out_asc = zlema(asc, length=10)
    valid_asc = [v for v in out_asc if v is not None]
    assert len(valid_asc) > 10
    for i in range(1, len(valid_asc)):
        assert valid_asc[i] > valid_asc[i - 1]


# ---------------------------------------------------------------------------
# Strategy Signal Unit Tests
# ---------------------------------------------------------------------------

def test_rvol_pivot_signals():
    # Construct a breakout above a confirmed pivot
    rows = [
        (100, 105, 95, 100),
        (100, 110, 95, 105),
        (105, 120, 100, 115),  # Pivot High = 120
        (115, 118, 105, 110),
        (110, 112, 102, 105),  # Pivot confirmed here (index 4)
        (105, 115, 104, 112),
        (112, 125, 110, 122),  # Breakout: close 122 > 120
    ]
    bars = _make_dummy_bars(rows)
    # Give the breakout bar high volume
    bars[-1] = Bar(
        open_time_ms=bars[-1].open_time_ms,
        open=bars[-1].open,
        high=bars[-1].high,
        low=bars[-1].low,
        close=bars[-1].close,
        volume=50000.0,  # huge volume
        close_time_ms=bars[-1].close_time_ms,
    )
    p = RvolPivotParams(mode="mode_a", rvol_k=1.2, vol_len=5, pivot_len=2)
    buys, sells, stops = rvol_pivot_signals(bars, p)
    assert len(buys) == len(bars)
    assert buys[-1] is True


def test_emv_gate_signals():
    # Flat then explosive upward bar
    rows = [(100 + i * 0.1, 102 + i * 0.1, 98 + i * 0.1, 100 + i * 0.1) for i in range(25)]
    rows.append((105, 120, 104, 118))  # explosive bar
    bars = _make_dummy_bars(rows)
    bars[-1] = Bar(
        open_time_ms=bars[-1].open_time_ms,
        open=bars[-1].open,
        high=bars[-1].high,
        low=bars[-1].low,
        close=bars[-1].close,
        volume=50000.0,
        close_time_ms=bars[-1].close_time_ms,
    )
    p = EmvGateParams(mode="mode_a", eom_len=5, rvol_k=1.0, atr_pct_min=0.002)
    buys, sells, stops = emv_signals(bars, p)
    assert len(buys) == len(bars)


def test_pvo_mom_signals():
    # Closes below SMA, then cross above SMA with rising volume
    rows = [(100, 102, 98, 99) for _ in range(30)]
    rows.append((100, 115, 99, 110))  # strong cross above SMA
    bars = _make_dummy_bars(rows, vol=500.0)
    # Set rising volume on last few bars
    for i in range(25, 31):
        bars[i] = Bar(
            open_time_ms=bars[i].open_time_ms,
            open=bars[i].open,
            high=bars[i].high,
            low=bars[i].low,
            close=bars[i].close,
            volume=5000.0 + (i - 25) * 2000.0,
            close_time_ms=bars[i].close_time_ms,
        )
    p = PvoMomParams(mode="mode_a", sma_len=10, exit_on_gate_loss=True)
    buys, sells, stops = pvo_signals(bars, p)
    assert len(buys) == len(bars)
    assert buys[-1] is True


def test_p4h_signals():
    # 8 hourly bars = 2 distinct 4H buckets
    rows = [
        (100, 105, 95, 102),
        (102, 108, 101, 106),
        (106, 110, 104, 108),
        (108, 110, 105, 107),  # Bucket 1 High = 110
        # Bucket 2 starts at i=4
        (107, 109, 105, 108),
        (108, 115, 107, 112),  # Breakout: close 112 > 110
        (112, 114, 108, 110),
        (110, 111, 100, 102),  # Drop below 110 -> exit
    ]
    bars = _make_dummy_bars(rows, step_ms=3_600_000, t0=1_704_067_200_000)
    p = P4HParams(mode="mode_a", rvol_k=0.0, one_trade_per_bucket=True)
    buys, sells, stops = p4h_signals(bars, p)
    assert len(buys) == len(bars)
    assert buys[5] is True
    assert sells[7] is True


def test_zlema_sma_signals():
    # Downtrend then sharp reversal causing ZLEMA to cross above SMA
    rows = [(150 - i * 2, 152 - i * 2, 148 - i * 2, 149 - i * 2) for i in range(30)]
    # Sharp reversal
    rows.extend([
        (90, 105, 89, 102),
        (102, 120, 100, 118),
        (118, 135, 115, 132),
        (132, 150, 130, 148),
    ])
    bars = _make_dummy_bars(rows)
    p = ZlemaSmaParams(mode="mode_a", zlema_len=10, sma_len=20, rvol_k=0.0)
    buys, sells, stops = zlema_signals(bars, p)
    assert len(buys) == len(bars)
    assert any(buys)


# ---------------------------------------------------------------------------
# BNB Smoke Validation Unit Tests
# ---------------------------------------------------------------------------

def test_bnb_smoke_validators():
    # Strategy 1
    p1_fail = RvolPivotParams(rvol_k=1.2)  # k < 1.5 fails BNB smoke
    ok1, reason1 = validate_rvol_pivot_bnb_smoke("1h", p1_fail)
    assert not ok1 and "RVOL k=" in reason1

    p1_pass = RvolPivotParams(rvol_k=1.5, atr_filter=True)
    ok1_pass, _ = validate_rvol_pivot_bnb_smoke("1h", p1_pass)
    assert ok1_pass

    # Strategy 2
    p2_fail = EmvGateParams(rvol_k=1.0)
    ok2, reason2 = validate_emv_bnb_smoke("1h", p2_fail, "BNBUSDT")
    assert not ok2 and "RVOL k=" in reason2

    p2_pass = EmvGateParams(rvol_k=1.5, atr_pct_min=0.002, divisor=10_000_000.0)
    ok2_pass, _ = validate_emv_bnb_smoke("1h", p2_pass, "BNBUSDT")
    assert ok2_pass

    # Strategy 3
    p3_fail = PvoMomParams(exit_on_gate_loss=False)
    ok3, reason3 = validate_pvo_bnb_smoke("1h", p3_fail)
    assert not ok3 and "exit_on_gate_loss=False" in reason3

    p3_pass = PvoMomParams(exit_on_gate_loss=True, sma_len=20)
    ok3_pass, _ = validate_pvo_bnb_smoke("1h", p3_pass)
    assert ok3_pass

    # Strategy 4
    p4_fail = P4HParams(rvol_k=1.2)
    ok4, reason4 = validate_p4h_bnb_smoke("1h", p4_fail)
    assert not ok4 and "RVOL k=" in reason4

    p4_pass = P4HParams(rvol_k=1.5)
    ok4_pass, _ = validate_p4h_bnb_smoke("1h", p4_pass)
    assert ok4_pass

    # Strategy 5
    p5_fail = ZlemaSmaParams(rvol_k=0.0)  # RVOL off fails BNB smoke
    ok5, reason5 = validate_zlema_bnb_smoke("1h", p5_fail)
    assert not ok5 and "RVOL k=" in reason5

    p5_pass = ZlemaSmaParams(rvol_k=1.2)
    ok5_pass, _ = validate_zlema_bnb_smoke("1h", p5_pass)
    assert ok5_pass
