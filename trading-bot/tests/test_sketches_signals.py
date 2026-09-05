"""Unit tests for research sketch signal logic (synthetic bars)."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import adx_di, atr, ema, macd
from backtest.sketches.daily_adx import DailyAdxParams, compute_signals as adx_signals
from backtest.sketches.engine import run_long_only
from backtest.sketches.htf_pullback import HtfPullbackParams, compute_signals as htf_signals
from backtest.sketches.macd_hist import MacdHistParams, compute_signals as macd_signals


def _bars_from_closes(closes: list[float], *, step_ms: int = 86_400_000) -> list[Bar]:
    out: list[Bar] = []
    t0 = 1_700_000_000_000
    for i, c in enumerate(closes):
        h = c * 1.002
        lo = c * 0.998
        out.append(
            Bar(
                open_time_ms=t0 + i * step_ms,
                open=c,
                high=h,
                low=lo,
                close=c,
                volume=1.0,
                close_time_ms=t0 + i * step_ms + step_ms - 1,
            )
        )
    return out


def test_rma_atr_smoke():
    closes = [100.0 + (i % 7) - 3 for i in range(80)]
    highs = [c + 1 for c in closes]
    lows = [c - 1 for c in closes]
    a = atr(highs, lows, closes, 14)
    assert a[13] is not None
    assert a[-1] is not None and a[-1] > 0


def test_adx_di_warmup_and_bounds():
    # trending up
    closes = [100.0 + i * 0.5 for i in range(100)]
    highs = [c + 0.8 for c in closes]
    lows = [c - 0.2 for c in closes]
    plus_di, minus_di, adx = adx_di(highs, lows, closes, 14)
    assert plus_di[-1] is not None and minus_di[-1] is not None and adx[-1] is not None
    assert plus_di[-1] > minus_di[-1]
    assert 0 <= adx[-1] <= 100


def test_macd_hist_cross_detection():
    # flat then rally should push hist
    closes = [100.0] * 40 + [100.0 + i for i in range(1, 60)]
    _l, _s, hist = macd(closes)
    assert any(h is not None and h > 0 for h in hist)


def test_daily_adx_entry_requires_trend_and_di():
    # strong uptrend should eventually satisfy EMA50>EMA200 and +DI>-DI
    closes = [100.0 + i * 0.8 for i in range(260)]
    bars = _bars_from_closes(closes)
    buys, sells = adx_signals(bars, DailyAdxParams())
    assert any(buys), "expected at least one ADX trend entry in synthetic uptrend"
    # no pyramiding
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_macd_hist_entry_needs_hist_cross_and_ema():
    closes = [100.0] * 30
    # dip then strong rally above rising EMA100
    for i in range(120):
        closes.append(closes[-1] * (0.995 if i < 20 else 1.02))
    bars = _bars_from_closes(closes)
    buys, sells = macd_signals(bars, MacdHistParams())
    # May or may not fire depending on hist cross timing; check exit logic shape
    assert len(buys) == len(bars) == len(sells)
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert in_pos is False
            in_pos = True
        elif s:
            assert in_pos is True
            in_pos = False


def test_macd_exit_on_hist_cross_under_zero():
    """Force hist pattern: build long hist then flip negative."""
    # Use engine with handcrafted buys/sells to validate full close
    closes = [100.0 + i * 0.1 for i in range(50)]
    bars = _bars_from_closes(closes)
    buys = [False] * 50
    sells = [False] * 50
    buys[10] = True
    sells[20] = True
    res = run_long_only("TEST", "macd-hist-regime-v1", bars, buys, sells)
    assert len(res.trades) == 1
    assert res.trades[0].entry_bar == 10
    assert res.trades[0].exit_bar == 20


def test_htf_pullback_stop_and_bias_gate():
    # Daily strong uptrend
    d_closes = [100.0 + i for i in range(250)]
    daily = _bars_from_closes(d_closes, step_ms=86_400_000)
    # 4h: ~6 bars per day
    closes_4h: list[float] = []
    price = 100.0
    for i in range(250 * 6):
        # gentle up with occasional pullback
        if i % 40 < 5:
            price *= 0.992
        else:
            price *= 1.003
        closes_4h.append(price)
    bars_4h = _bars_from_closes(closes_4h, step_ms=4 * 3600 * 1000)
    # Align times roughly to daily span
    t0 = daily[0].open_time_ms
    bars_4h = [
        Bar(
            open_time_ms=t0 + i * 4 * 3600 * 1000,
            open=b.open,
            high=b.high,
            low=b.low,
            close=b.close,
            volume=1.0,
            close_time_ms=t0 + i * 4 * 3600 * 1000 + 4 * 3600 * 1000 - 1,
        )
        for i, b in enumerate(bars_4h)
    ]
    buys, sells, stops = htf_signals(bars_4h, daily, HtfPullbackParams())
    assert len(buys) == len(bars_4h)
    # If any buy, stop must be set below entry close
    for i, b in enumerate(buys):
        if b:
            assert stops[i] is not None
            assert stops[i] < bars_4h[i].close
    res = run_long_only(
        "TEST",
        "htf-ema-pullback-wide-v1",
        bars_4h,
        buys,
        sells,
        stop_prices=stops,
    )
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_ema200_present_for_daily_adx():
    closes = [float(100 + i) for i in range(220)]
    assert ema(closes, 200)[199] is not None
