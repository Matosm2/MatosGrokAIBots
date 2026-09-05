"""Unit tests for ema-rsi-trend-v1.1 signal + cooldown logic."""

from __future__ import annotations

from backtest.data import Bar
from backtest.engine import run_backtest
from backtest.signals import (
    SignalFrame,
    StrategyParams,
    apply_position_and_cooldown,
    compute_indicators,
)


def _synthetic_up_cross_then_down(n: int = 120) -> list[float]:
    closes: list[float] = []
    price = 100.0
    for i in range(n):
        if i < 60:
            price *= 0.998
        elif i < 85:
            price *= 1.012
        else:
            price *= 0.988
        closes.append(price)
    return closes


def test_raw_long_requires_ema_cross_rsi_and_close_ge_slow():
    closes = _synthetic_up_cross_then_down()
    frame = compute_indicators(closes, StrategyParams())
    assert any(frame.raw_long[60:90]), "expected a buy setup in rally window"
    for i, flag in enumerate(frame.raw_long):
        if not flag:
            continue
        assert frame.ema_cross_up[i]
        assert frame.rsi[i] is not None and frame.rsi[i] >= 50.0
        assert frame.ema_slow[i] is not None and closes[i] >= frame.ema_slow[i]


def test_exit_on_ema_crossunder_or_rsi_fade():
    closes = _synthetic_up_cross_then_down()
    frame = compute_indicators(closes, StrategyParams())
    assert any(frame.raw_exit), "expected exit conditions after selloff"
    for i, flag in enumerate(frame.raw_exit):
        if flag:
            assert frame.ema_cross_down[i] or frame.rsi_cross_down[i]


def test_cooldown_blocks_reentry():
    params = StrategyParams(cooldown_bars=6)
    n = 30
    raw_long = [False] * n
    raw_exit = [False] * n
    raw_long[10] = True
    raw_exit[12] = True
    raw_long[14] = True
    raw_long[20] = True

    frame = SignalFrame(
        ema_fast=[1.0] * n,
        ema_slow=[1.0] * n,
        rsi=[50.0] * n,
        ema_cross_up=raw_long[:],
        ema_cross_down=raw_exit[:],
        rsi_cross_down=[False] * n,
        raw_long=raw_long,
        raw_exit=raw_exit,
    )
    buys, sells = apply_position_and_cooldown(frame, params)
    assert buys[10] is True
    assert sells[12] is True
    assert buys[14] is False
    assert buys[20] is True


def test_no_pyramiding_and_full_close_engine():
    closes = _synthetic_up_cross_then_down(150)
    bars = [
        Bar(
            open_time_ms=1_700_000_000_000 + i * 3_600_000,
            open=c,
            high=c * 1.001,
            low=c * 0.999,
            close=c,
            volume=1.0,
            close_time_ms=1_700_000_000_000 + i * 3_600_000 + 3_599_999,
        )
        for i, c in enumerate(closes)
    ]
    res = run_backtest("TESTUSDT", bars, fee_rate=0.001, slippage_rate=0.0005)
    last_exit = -1
    for t in res.trades:
        assert t.entry_bar > last_exit
        assert t.exit_bar > t.entry_bar
        last_exit = t.exit_bar
        assert t.qty > 0
    assert res.buy_qty_pct == 2.5


def test_bar_close_no_lookahead_signal_index():
    closes = _synthetic_up_cross_then_down()
    params = StrategyParams()
    frame = compute_indicators(closes, params)
    buys, _sells = apply_position_and_cooldown(frame, params)
    for i, b in enumerate(buys):
        if b:
            assert frame.ema_fast[i] is not None
            assert frame.ema_slow[i] is not None
            assert frame.rsi[i] is not None
            assert i >= params.slow_len
