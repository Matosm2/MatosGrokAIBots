"""Unit tests for fresh-wave-v6 signal logic + indicators."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import demarker, kst, mass_index, twiggs_money_flow
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v6.darvas_box_v1 import (
    DarvasBoxParams,
    compute_signals as darvas_signals,
)
from backtest.path_b.fresh_wave_v6.demarker_zone_v1 import (
    DemarkerZoneParams,
    compute_signals as dem_signals,
)
from backtest.path_b.fresh_wave_v6.kst_pring_v1 import (
    KstPringParams,
    compute_signals as kst_signals,
)
from backtest.path_b.fresh_wave_v6.mass_index_bulge_v1 import (
    MassIndexBulgeParams,
    compute_signals as mi_signals,
)
from backtest.path_b.fresh_wave_v6.twiggs_mf_v1 import (
    TwiggsMfParams,
    compute_signals as tmf_signals,
)


def _bars_from_closes(
    closes: list[float], *, step_ms: int = 86_400_000, vol: float = 1000.0
) -> list[Bar]:
    out: list[Bar] = []
    t0 = 1_700_000_000_000
    for i, c in enumerate(closes):
        # Vary HL range so Mass Index / DeM / Twiggs have signal
        spread = 0.02 + 0.01 * ((i % 11) / 10.0)
        h = c * (1.0 + spread)
        lo = c * (1.0 - spread * 0.8)
        out.append(
            Bar(
                open_time_ms=t0 + i * step_ms,
                open=c,
                high=h,
                low=lo,
                close=c,
                volume=vol + (i % 7) * 10,
                close_time_ms=t0 + i * step_ms + step_ms - 1,
            )
        )
    return out


def _assert_no_pyramid(buys: list[bool], sells: list[bool]) -> None:
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_mass_index_indicator_and_signals():
    closes = [100.0 + (i % 9) - 4 for i in range(120)]
    bars = _bars_from_closes(closes)
    mi = mass_index([b.high for b in bars], [b.low for b in bars], 9, 25)
    assert any(x is not None for x in mi)
    buys, sells = mi_signals(bars, MassIndexBulgeParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)


def test_kst_modes():
    closes = [100.0 + i * 0.2 + ((i % 7) - 3) for i in range(200)]
    bars = _bars_from_closes(closes)
    line, signal = kst([b.close for b in bars])
    assert any(x is not None for x in line)
    assert any(x is not None for x in signal)
    buys_a, sells_a = kst_signals(bars, KstPringParams(mode="A"))
    buys_b, sells_b = kst_signals(bars, KstPringParams(mode="B"))
    _assert_no_pyramid(buys_a, sells_a)
    _assert_no_pyramid(buys_b, sells_b)


def test_twiggs_mf_ne_cmf_modes():
    closes = [100.0 + (i % 5) - 2 for i in range(100)]
    bars = _bars_from_closes(closes, vol=5000.0)
    series = twiggs_money_flow(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        [b.volume for b in bars],
        21,
    )
    assert series[20] is not None
    buys_a, sells_a = tmf_signals(bars, TwiggsMfParams(mode="A", channel_n=20))
    buys_b, sells_b = tmf_signals(bars, TwiggsMfParams(mode="B"))
    _assert_no_pyramid(buys_a, sells_a)
    _assert_no_pyramid(buys_b, sells_b)


def test_demarker_zone_no_rsi():
    closes = []
    for i in range(120):
        if (i // 12) % 2 == 0:
            closes.append(100.0 - (i % 12) * 0.8)
        else:
            closes.append(90.0 + (i % 12) * 0.8)
    bars = _bars_from_closes(closes)
    series = demarker([b.high for b in bars], [b.low for b in bars], 14)
    assert any(x is not None for x in series)
    buys, sells = dem_signals(bars, DemarkerZoneParams())
    _assert_no_pyramid(buys, sells)
    res = run_long_only("TEST", "demarker-zone-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_darvas_not_donchian_stateful():
    # Build: flat, then a clear lookback high, consolidate, breakout up, then break floor
    closes = [100.0] * 100
    for i in range(100, 130):
        closes.append(100.0 + (i - 100) * 0.5)  # grind up to new highs
    for i in range(130, 145):
        closes.append(closes[-1])  # consolidate near top
    for i in range(145, 160):
        closes.append(closes[144] + 2.0 + (i - 145) * 0.3)  # breakout
    for i in range(160, 180):
        closes.append(closes[159] - (i - 159) * 1.5)  # dump through floor
    bars = _bars_from_closes(closes)
    # Force distinct highs/lows for box formation
    for i, b in enumerate(bars):
        if 100 <= i < 130:
            bars[i] = Bar(
                open_time_ms=b.open_time_ms,
                open=b.open,
                high=b.close + 1.0,
                low=b.close - 0.5,
                close=b.close,
                volume=b.volume,
                close_time_ms=b.close_time_ms,
            )
    buys, sells = darvas_signals(bars, DarvasBoxParams(lookback=90, confirm=3))
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    # Must not be identical to a naive Donchian(90) breakout every bar
    # (Darvas is stateful — far fewer entries than rolling channel)
    assert sum(buys) < len(bars) // 4
