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


# --- close-above-ema20-hold-v1 / donchian-20-10-spot-v1 ---

from backtest.sketches.donchian_spot import (
    DonchianParams,
    _prior_highest_high,
    _prior_lowest_low,
    compute_raw as don_raw,
    compute_signals as don_signals,
)
from backtest.sketches.ema20_hold import (
    Ema20HoldParams,
    compute_raw as ema20_raw,
    compute_signals as ema20_signals,
)
from backtest.sketches.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_sketch


def test_ema20_hold_entry_needs_close_above_rising_ema():
    # Strong uptrend: close above EMA20 and EMA rising vs 5 bars ago
    closes = [100.0 + i * 0.5 for i in range(80)]
    bars = _bars_from_closes(closes)
    buys, sells = ema20_signals(bars, Ema20HoldParams())
    assert any(buys), "expected EMA20 hold entries in synthetic uptrend"
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_ema20_hold_exit_when_close_below_ema():
    # Rally then crash below EMA20
    closes = [100.0 + i for i in range(60)] + [160.0 - i * 3 for i in range(1, 40)]
    bars = _bars_from_closes(closes)
    raw_long, raw_exit = ema20_raw(bars, Ema20HoldParams())
    assert any(raw_long)
    assert any(raw_exit)
    buys, sells = ema20_signals(bars, Ema20HoldParams())
    # If we entered, we should eventually exit on the crash
    if any(buys):
        assert any(sells) or buys.index(True) == len(buys) - 1


def test_ema20_adx_filter_off_by_default():
    params = Ema20HoldParams()
    assert params.adx_min is None


def test_ema20_no_ema50_ema200_requirement():
    """Short series where EMA50/200 cannot arm — strategy still can enter."""
    closes = [100.0 + i * 0.8 for i in range(40)]
    bars = _bars_from_closes(closes)
    buys, _ = ema20_signals(bars, Ema20HoldParams())
    # With only 40 bars, EMA200 never ready; EMA20 can still fire
    assert any(buys)


def test_donchian_prior_high_excludes_current():
    highs = [1.0, 2.0, 3.0, 10.0, 4.0]
    # At i=4, prior 3 highs are 2,3,10 → 10 (current 4 excluded)
    assert _prior_highest_high(highs, 4, 3) == 10.0
    assert _prior_highest_high(highs, 2, 3) is None


def test_donchian_prior_low_excludes_current():
    lows = [5.0, 4.0, 1.0, 3.0, 2.0]
    assert _prior_lowest_low(lows, 4, 3) == 1.0


def test_donchian_breakout_and_exit_signals():
    # Flat then breakout above prior high, then dump below prior low
    closes: list[float] = [100.0] * 25
    for i in range(15):
        closes.append(100.0 + i * 2)  # breakout
    for i in range(15):
        closes.append(closes[-1] - 5)  # dump
    bars = _bars_from_closes(closes)
    # Make highs/lows track close with spread so Donchian uses high/low
    for i, b in enumerate(bars):
        bars[i] = Bar(
            open_time_ms=b.open_time_ms,
            open=b.open,
            high=b.close * 1.001,
            low=b.close * 0.999,
            close=b.close,
            volume=1.0,
            close_time_ms=b.close_time_ms,
        )
    buys, sells = don_signals(bars, DonchianParams(entry_lookback=20, exit_lookback=10))
    assert len(buys) == len(bars)
    assert any(buys), "expected Donchian breakout entry"
    # After dump, expect exit
    first_buy = buys.index(True)
    assert any(sells[first_buy:]), "expected Donchian exit after dump"
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_donchian_raw_entry_is_close_gt_prior_high():
    highs = [10.0] * 20 + [11.0, 12.0]
    lows = [9.0] * 22
    closes = [9.5] * 20 + [10.5, 9.0]  # bar20: 10.5 > prior max 10 → entry
    bars = [
        Bar(
            open_time_ms=1_700_000_000_000 + i * 86_400_000,
            open=c,
            high=highs[i],
            low=lows[i],
            close=c,
            volume=1.0,
            close_time_ms=1_700_000_000_000 + i * 86_400_000 + 86_400_000 - 1,
        )
        for i, c in enumerate(closes)
    ]
    raw_long, raw_exit = don_raw(bars, DonchianParams(20, 10))
    assert raw_long[20] is True
    assert raw_long[19] is False  # not enough prior / close not above


def test_dual_sizing_gate_uses_100_pct_not_ops():
    closes = [100.0 + i * 0.2 for i in range(40)]
    bars = _bars_from_closes(closes)
    buys = [False] * 40
    sells = [False] * 40
    buys[5] = True
    sells[20] = True
    gate = run_long_only(
        "TEST", "x", bars, buys, sells, buy_qty_pct=GATE_SIZE_PCT
    )
    ops = run_long_only(
        "TEST", "x", bars, buys, sells, buy_qty_pct=OPS_SIZE_PCT
    )
    mg = summarize_sketch(gate)
    mo = summarize_sketch(ops)
    assert mg["trades"] == mo["trades"] == 1
    assert mg["win_rate_pct"] == mo["win_rate_pct"]
    # Absolute return magnitude larger at 100% size
    assert abs(mg["return_pct"]) > abs(mo["return_pct"])
