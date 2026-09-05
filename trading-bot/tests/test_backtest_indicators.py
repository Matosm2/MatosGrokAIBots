"""Unit tests for Pine-like EMA / RSI / cross helpers."""

from __future__ import annotations

from backtest.indicators import crossover, crossunder, ema, rsi


def test_ema_seed_and_length():
    closes = [float(i) for i in range(1, 21)]  # 1..20
    out = ema(closes, 5)
    assert out[:4] == [None, None, None, None]
    assert out[4] == sum(closes[:5]) / 5
    assert out[-1] is not None
    assert out[-1] > out[4]


def test_rsi_bounds_and_warmup():
    up = [100.0 + i for i in range(40)]
    r = rsi(up, 14)
    assert all(x is None for x in r[:14])
    assert r[14] is not None
    assert r[-1] is not None and r[-1] > 70

    down = [100.0 - i for i in range(40)]
    rd = rsi(down, 14)
    assert rd[-1] is not None and rd[-1] < 30


def test_crossover_crossunder():
    a: list[float | None] = [1.0, 1.0, 3.0, 2.0]
    b: list[float | None] = [2.0, 2.0, 2.0, 2.5]
    assert crossover(a, b, 0) is False
    assert crossover(a, b, 2) is True
    assert crossunder(a, b, 3) is True
    a2: list[float | None] = [None, 1.0, 3.0]
    b2: list[float | None] = [None, 2.0, 2.0]
    assert crossover(a2, b2, 2) is True
