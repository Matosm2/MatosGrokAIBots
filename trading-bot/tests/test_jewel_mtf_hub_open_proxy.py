"""Tests: 2D aggregation, no-lookahead join, regime/RSI open-proxy logic."""

from __future__ import annotations

from datetime import datetime, timezone

from backtest.data import Bar
from backtest.jewel_mtf_hub.aggregate import aggregate_1d_to_2d, assert_2d_duration
from backtest.jewel_mtf_hub.join import (
    assert_no_lookahead_sample,
    map_htf_indices_onto_ltf,
    map_htf_onto_ltf,
)
from backtest.jewel_mtf_hub.proxies import (
    ADX_MIN,
    RSI_ENTER,
    RSI_EXIT,
    compute_regime,
    compute_ribbon,
    compute_strength,
)
from backtest.jewel_mtf_hub.signals import signals_m1, signals_m3


def _ms(y: int, m: int, d: int, h: int = 0) -> int:
    return int(datetime(y, m, d, h, tzinfo=timezone.utc).timestamp() * 1000)


def _bar(open_ms: int, o: float, h: float, l: float, c: float, vol: float = 1.0) -> Bar:
    # Binance-style close_time = open + 1D - 1ms for daily
    return Bar(
        open_time_ms=open_ms,
        open=o,
        high=h,
        low=l,
        close=c,
        volume=vol,
        close_time_ms=open_ms + 24 * 3600 * 1000 - 1,
    )


def test_aggregate_1d_to_2d_pairs_and_drops_orphan():
    days = [
        _bar(_ms(2024, 1, 1), 100, 110, 90, 105, 10),
        _bar(_ms(2024, 1, 2), 105, 120, 100, 115, 20),
        _bar(_ms(2024, 1, 3), 115, 130, 110, 125, 30),
        _bar(_ms(2024, 1, 4), 125, 140, 120, 135, 40),
        _bar(_ms(2024, 1, 5), 135, 150, 130, 145, 50),  # orphan
    ]
    out = aggregate_1d_to_2d(days)
    assert len(out) == 2
    assert out[0].open_time_ms == _ms(2024, 1, 1)
    assert out[0].open == 100
    assert out[0].high == 120
    assert out[0].low == 90
    assert out[0].close == 115
    assert out[0].volume == 30
    assert out[0].close_time_ms == days[1].close_time_ms
    assert out[1].open_time_ms == _ms(2024, 1, 3)
    assert out[1].close == 135
    assert out[1].volume == 70
    assert_2d_duration(out)


def test_aggregate_empty_and_single():
    assert aggregate_1d_to_2d([]) == []
    assert aggregate_1d_to_2d([_bar(_ms(2024, 1, 1), 1, 2, 0.5, 1.5)]) == []


def test_no_lookahead_join_still_holds_for_regime_values():
    """Joined HTF regime never uses an HTF bar that closes after LTF close."""
    htf_open = [_ms(2024, 1, 1), _ms(2024, 1, 2)]
    htf_regime = [1, -1]
    ltf_open = [_ms(2024, 1, 1, h) for h in (0, 4, 8, 12, 16, 20)] + [
        _ms(2024, 1, 2, 0),
        _ms(2024, 1, 2, 20),
    ]
    mapped = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_values=htf_regime,
        htf_tf="1D",
    )
    idxs = map_htf_indices_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_tf="1D",
    )
    assert mapped[:5] == [None] * 5
    assert mapped[5] == 1  # Jan1 20:00 closes when daily closes
    assert mapped[6] == 1
    assert mapped[7] == -1  # Jan2 20:00 sees completed Jan2 daily
    assert_no_lookahead_sample(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_tf="1D",
        mapped_indices=idxs,
    )


def test_regime_flip_and_leave_green():
    # Synthetic path: build OHLC that yields known regime transitions via direct inject
    # Unit-test the flip/leave rules on a constructed regime path through compute_regime
    # by using a trending then reversing price series.
    n = 80
    closes = []
    highs = []
    lows = []
    price = 100.0
    for i in range(n):
        if i < 50:
            price += 1.5  # strong up
        else:
            price -= 2.0  # reverse
        closes.append(price)
        highs.append(price + 0.5)
        lows.append(price - 0.5)
    reg = compute_regime(highs, lows, closes)
    # After warmup, expect some +1 then later leave
    warm = [r for r in reg.regime if r is not None]
    assert any(r == 1 for r in warm)
    # Flip→green only when prior ≤ 0 and cur +1
    for i in range(1, n):
        prev, cur = reg.regime[i - 1], reg.regime[i]
        if prev is None or cur is None:
            assert reg.flip_to_green[i] is False
            assert reg.leave_green[i] is False
            continue
        assert reg.flip_to_green[i] == (prev <= 0 and cur == 1)
        assert reg.leave_green[i] == (prev == 1 and cur != 1)
    assert ADX_MIN == 20.0


def test_rsi_crossover_enter_and_exit_below():
    # Decline first (RSI low), then climb through 60, then fall under 50
    closes = [100.0]
    for i in range(30):
        closes.append(closes[-1] - 1.5)
    for i in range(40):
        closes.append(closes[-1] + 2.0)
    for i in range(40):
        closes.append(closes[-1] - 3.0)
    st = compute_strength(closes)
    assert RSI_ENTER == 60.0 and RSI_EXIT == 50.0
    assert any(st.enter_cross)
    assert any(st.exit_below)
    for i, flag in enumerate(st.enter_cross):
        if flag:
            assert st.rsi[i] is not None and st.rsi[i] > 60.0
            assert st.rsi[i - 1] is not None and st.rsi[i - 1] <= 60.0
            break
    for i, flag in enumerate(st.exit_below):
        if flag and st.rsi[i] is not None:
            assert st.rsi[i] < 50.0


def test_ribbon_ema21_cross_helper():
    closes = [100.0 - i * 0.5 for i in range(60)] + [
        70.0 + i for i in range(30)
    ]
    rib = compute_ribbon(closes)
    assert any(x is not None for x in rib.ribbon_low)
    for i, (lo, hi, ef, es) in enumerate(
        zip(rib.ribbon_low, rib.ribbon_high, rib.ema_fast, rib.ema_slow, strict=True)
    ):
        if lo is None:
            continue
        assert lo == min(ef, es) and hi == max(ef, es)
    assert any(rib.close_cross_ema_fast)


def test_m1_m3_produce_gated_signals_on_synthetic_daily():
    daily = []
    px = 100.0
    for d in range(1, 121):
        # crude calendar via ms offset
        t = _ms(2024, 1, 1) + (d - 1) * 24 * 3600 * 1000
        o = px
        if d < 60:
            px += 1.0
        else:
            px -= 0.8
        daily.append(_bar(t, o, max(o, px) + 1, min(o, px) - 1, px, 1.0))
    m1 = signals_m1(daily)
    m3 = signals_m3(daily)
    assert len(m1.bars) == 60  # 120/2
    assert len(m1.buys) == len(m1.bars) == len(m1.sells)
    assert sum(m1.buys) >= 0
    assert len(m3.bars) == 60
    # Position gate: never buy while already notionally in (alternating)
    in_pos = False
    for b, s in zip(m1.buys, m1.sells, strict=True):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False
