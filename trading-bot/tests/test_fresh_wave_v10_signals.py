"""Unit tests for fresh-wave-v10 signal logic + indicators."""

from __future__ import annotations

import inspect
import math

from backtest.data import Bar
from backtest.indicators import (
    chaikin_oscillator,
    crossover,
    laguerre_filter,
    session_vwap_bands,
    smi_blau,
)
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v10.chaikin_osc_v1 import (
    ChaikinOscParams,
    compute_signals as chaikin_signals,
)
from backtest.path_b.fresh_wave_v10.laguerre_price_v1 import (
    LaguerrePriceParams,
    compute_signals as laguerre_signals,
)
from backtest.path_b.fresh_wave_v10.smi_blau_v1 import (
    SmiBlauParams,
    compute_signals as smi_signals,
)
from backtest.path_b.fresh_wave_v10.vwap_utc_sigma_v1 import (
    VwapUtcSigmaParams,
    compute_signals as vwap_signals,
)
from backtest.path_b.fresh_wave_v10.woodie_utc_v1 import (
    WoodieParams,
    compute_signals as woodie_signals,
    levels_from_ohlc,
)


def _bars_from_ohlc(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 3_600_000,
    vol: float = 1000.0,
    t0: int = 1_704_067_200_000,  # 2023-12-01 00:00 UTC
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
                volume=vol + (i % 7) * 10,
                close_time_ms=t0 + i * step_ms + step_ms - 1,
            )
        )
    return out


def _bars_from_closes(
    closes: list[float], *, step_ms: int = 3_600_000, vol: float = 1000.0, t0: int = 1_704_067_200_000
) -> list[Bar]:
    rows: list[tuple[float, float, float, float]] = []
    for i, c in enumerate(closes):
        spread = 0.02 + 0.01 * ((i % 11) / 10.0)
        o = c * (1.0 - 0.002 * ((i % 3) - 1))
        h = max(o, c) * (1.0 + spread)
        lo = min(o, c) * (1.0 - spread * 0.8)
        rows.append((o, h, lo, c))
    return _bars_from_ohlc(rows, step_ms=step_ms, vol=vol, t0=t0)


def _assert_no_pyramid(buys: list[bool], sells: list[bool]) -> None:
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_woodie_levels_formula():
    lv = levels_from_ohlc(110.0, 100.0, 105.0)
    p = (110.0 + 100.0 + 2.0 * 105.0) / 4.0
    assert math.isclose(lv.p, p)
    assert math.isclose(lv.r1, 2.0 * p - 100.0)
    assert math.isclose(lv.s1, 2.0 * p - 110.0)
    assert math.isclose(lv.r2, p + 10.0)
    assert math.isclose(lv.s2, p - 10.0)


def test_woodie_mode_a_fade_s1_not_camarilla_orb():
    MS_DAY = 86_400_000
    t0 = 1_704_067_200_000
    rows: list[tuple[float, float, float, float]] = []
    for i in range(24):
        if i == 0:
            rows.append((104.0, 110.0, 103.0, 108.0))
        elif i == 12:
            rows.append((108.0, 109.0, 100.0, 101.0))
        elif i == 23:
            rows.append((101.0, 106.0, 100.5, 105.0))
        else:
            rows.append((105.0, 107.0, 103.0, 105.0))
    lv = levels_from_ohlc(110.0, 100.0, 105.0)
    for i in range(24):
        if i == 5:
            rows.append((lv.s1 + 1.0, lv.s1 + 1.5, lv.s1 - 0.5, lv.s1 + 0.3))
        elif i == 10:
            rows.append((lv.p - 1.0, lv.p + 0.5, lv.p - 1.5, lv.p + 0.2))
        else:
            rows.append((105.0, 106.0, 104.0, 105.0))
    bars = _bars_from_ohlc(rows, step_ms=3_600_000, t0=t0)
    assert bars[0].open_time_ms % MS_DAY == 0
    buys, sells, stops = woodie_signals(bars, WoodieParams(mode="mode_a"))
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1
    entry_i = next(i for i, b in enumerate(buys) if b)
    assert stops[entry_i] is not None
    assert math.isclose(stops[entry_i], lv.s2)  # type: ignore[arg-type]
    import backtest.path_b.fresh_wave_v10.woodie_utc_v1 as mod

    src = inspect.getsource(mod)
    assert "Camarilla" in src or "≠ Camarilla" in (mod.__doc__ or "")
    assert "or_minutes" not in src
    assert "Session ORB" in src or "Session ORB" in (mod.__doc__ or "")
    # Not Camarilla formula
    assert "(H+L+2C)/4" in src or "2.0 * c" in src
    res = run_long_only("TEST", "woodie-utc-v1", bars, buys, sells, stop_prices=stops, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_vwap_session_reset_and_not_bollinger():
    MS_HOUR = 3_600_000
    t0 = 1_704_067_200_000
    # Two UTC days of 1h bars; day1 dips to −2σ then reclaims
    rows: list[tuple[float, float, float, float]] = []
    for day in range(2):
        for i in range(24):
            base = 100.0 + day * 0.5
            if day == 1 and i == 6:
                rows.append((base - 2.0, base - 1.0, base - 8.0, base - 1.5))
            elif day == 1 and i == 12:
                rows.append((base, base + 1.0, base - 0.5, base + 0.8))
            else:
                rows.append((base, base + 0.5, base - 0.5, base + 0.1))
    bars = _bars_from_ohlc(rows, step_ms=MS_HOUR, t0=t0, vol=5000.0)
    day_ids = [(b.open_time_ms // 86_400_000) * 86_400_000 for b in bars]
    vwap, lo2, hi2 = session_vwap_bands(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        [b.volume for b in bars],
        day_ids,
    )
    assert any(v is not None for v in vwap)
    # Reset: first bar of day1 VWAP near that bar's TP (not carry prior day)
    day1_i = 24
    assert vwap[day1_i] is not None
    tp0 = (bars[day1_i].high + bars[day1_i].low + bars[day1_i].close) / 3.0
    assert abs(vwap[day1_i] - tp0) < 1e-6  # type: ignore[arg-type]
    buys, sells = vwap_signals(bars, VwapUtcSigmaParams(mode="mode_a"))
    _assert_no_pyramid(buys, sells)
    import backtest.path_b.fresh_wave_v10.vwap_utc_sigma_v1 as mod

    src = inspect.getsource(mod)
    assert "from backtest.indicators import" in src or "session_vwap_bands" in src
    assert "bollinger(" not in src.lower()
    assert "session_vwap_bands" in src
    assert "Bollinger" in (mod.__doc__ or "") or "Bollinger" in src
    res = run_long_only("TEST", "vwap-utc-sigma-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_smi_blau_not_stoch_connors_rsi():
    closes = [100.0 + 8.0 * math.sin(2 * math.pi * i / 20.0) for i in range(200)]
    bars = _bars_from_closes(closes)
    smi, sig = smi_blau(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        length=13,
        smooth1=3,
        smooth2=3,
        signal_len=3,
    )
    assert any(x is not None for x in smi)
    assert any(x is not None for x in sig)
    defined = [smi[i] for i in range(len(bars)) if smi[i] is not None]
    assert min(defined) > -120 and max(defined) < 120  # type: ignore[type-var]
    buys, sells = smi_signals(bars, SmiBlauParams(mode="mode_a"))
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1 and sum(sells) >= 1
    import backtest.path_b.fresh_wave_v10.smi_blau_v1 as mod

    src = inspect.getsource(mod)
    assert "from backtest.indicators import rsi" not in src
    assert "stoch(" not in src.lower()
    assert "connors_rsi" not in src.lower()
    assert "smi_blau" in src
    assert "rsi(" not in src
    assert "Stoch" in (mod.__doc__ or "") or "Stoch" in src  # documented forbid
    res = run_long_only("TEST", "smi-blau-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_smi_mode_b_os_reclaim():
    # Force OS then reclaim
    closes = [100.0] * 30 + list(range(100, 70, -1)) + list(range(70, 110))
    bars = _bars_from_closes([float(c) for c in closes])
    buys, sells = smi_signals(bars, SmiBlauParams(mode="mode_b"))
    _assert_no_pyramid(buys, sells)
    # Clean run even if zero trades on synthetic
    res = run_long_only("TEST", "smi-blau-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_chaikin_osc_not_cmf_obv_mfi():
    # Alternating accumulation / distribution blocks so ADL momentum zero-crosses
    t0 = 1_704_067_200_000
    step = 3_600_000
    bars: list[Bar] = []
    price = 100.0
    for i in range(200):
        block = (i // 15) % 2
        if block == 0:
            o, h, lo, c = price, price + 2.0, price - 0.5, price + 1.5
        else:
            o, h, lo, c = price, price + 0.5, price - 2.0, price - 1.5
        price = c
        bars.append(
            Bar(
                open_time_ms=t0 + i * step,
                open=o,
                high=h,
                low=lo,
                close=c,
                volume=1000.0,
                close_time_ms=t0 + i * step + step - 1,
            )
        )
    osc = chaikin_oscillator(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        [b.volume for b in bars],
        fast=3,
        slow=10,
    )
    assert any(x is not None for x in osc)
    buys, sells = chaikin_signals(bars, ChaikinOscParams())
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1 and sum(sells) >= 1
    import backtest.path_b.fresh_wave_v10.chaikin_osc_v1 as mod

    src = inspect.getsource(mod)
    assert "cmf(" not in src
    assert " from backtest.indicators import cmf" not in src
    assert "obv(" not in src.lower()
    assert "mfi(" not in src
    assert "chaikin_oscillator" in src
    assert crossover is not None
    res = run_long_only("TEST", "chaikin-osc-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_laguerre_price_not_laguerre_rsi():
    closes = [100.0 + 5.0 * math.sin(2 * math.pi * i / 25.0) for i in range(150)]
    bars = _bars_from_closes(closes)
    filt = laguerre_filter([b.close for b in bars], gamma=0.8)
    assert all(x is not None for x in filt)
    # Filter tracks price but is smoother — not identical
    diffs = [abs(bars[i].close - filt[i]) for i in range(20, 150)]  # type: ignore[arg-type]
    assert max(diffs) > 0.01
    buys, sells = laguerre_signals(bars, LaguerrePriceParams(gamma=0.8))
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1 and sum(sells) >= 1
    import backtest.path_b.fresh_wave_v10.laguerre_price_v1 as mod

    src = inspect.getsource(mod)
    assert "laguerre_rsi" not in src.lower()
    assert "rsi(" not in src
    assert "laguerre_filter" in src
    assert "ema(" not in src  # no EMA×RSI stack
    res = run_long_only("TEST", "laguerre-price-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_vwap_mode_b_reclaim():
    MS_HOUR = 3_600_000
    t0 = 1_704_067_200_000
    rows: list[tuple[float, float, float, float]] = []
    for i in range(48):
        if i < 10:
            rows.append((100.0, 101.0, 99.0, 100.5))
        elif i < 20:
            rows.append((98.0, 99.0, 97.0, 97.5))  # below VWAP
        elif i == 20:
            rows.append((98.0, 102.0, 97.5, 101.5))  # reclaim
        else:
            rows.append((100.0, 101.0, 99.0, 100.2))
    bars = _bars_from_ohlc(rows, step_ms=MS_HOUR, t0=t0, vol=3000.0)
    buys, sells = vwap_signals(bars, VwapUtcSigmaParams(mode="mode_b"))
    _assert_no_pyramid(buys, sells)
    res = run_long_only("TEST", "vwap-utc-sigma-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar
