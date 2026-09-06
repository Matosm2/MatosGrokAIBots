"""Unit tests for fresh-wave-v3 signal logic (synthetic bars)."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import adx_di, crossover, donchian, schaff_stc, tsi
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v3.adx_dmi_trend_v1 import (
    AdxDmiParams,
    compute_signals as adx_signals,
)
from backtest.path_b.fresh_wave_v3.donchian_breakout_v1 import (
    DonchianParams,
    compute_signals as donchian_signals,
)
from backtest.path_b.fresh_wave_v3.elder_ray_v1 import (
    ElderRayParams,
    compute_signals as elder_signals,
)
from backtest.path_b.fresh_wave_v3.schaff_stc_v1 import (
    SchaffStcParams,
    compute_signals as stc_signals,
)
from backtest.path_b.fresh_wave_v3.tsi_momentum_v1 import (
    TsiParams,
    compute_signals as tsi_signals,
)


def _bars_from_closes(
    closes: list[float], *, step_ms: int = 86_400_000, vol: float = 1000.0
) -> list[Bar]:
    out: list[Bar] = []
    t0 = 1_700_000_000_000
    for i, c in enumerate(closes):
        h = c * 1.01
        lo = c * 0.99
        out.append(
            Bar(
                open_time_ms=t0 + i * step_ms,
                open=c,
                high=h,
                low=lo,
                close=c,
                volume=vol,
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


def test_donchian_prior_channel_breakout():
    # flat channel then close clearly above prior 20-bar high
    closes = [100.0] * 30 + [120.0] * 20
    bars = _bars_from_closes(closes)
    # keep flat highs at 101 for first 30; breakout bars close=120 high=122
    for i in range(30):
        bars[i] = Bar(
            open_time_ms=bars[i].open_time_ms,
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.0,
            volume=1000.0,
            close_time_ms=bars[i].close_time_ms,
        )
    for i in range(30, len(bars)):
        bars[i] = Bar(
            open_time_ms=bars[i].open_time_ms,
            open=118.0,
            high=122.0,
            low=117.0,
            close=120.0,
            volume=1000.0,
            close_time_ms=bars[i].close_time_ms,
        )
    upper, _ = donchian([b.high for b in bars], [b.low for b in bars], 20)
    assert upper[20] is not None
    assert upper[19] is None  # needs 20 prior bars → first at index 20
    assert upper[30] == 101.0
    buys, sells = donchian_signals(bars, DonchianParams())
    assert len(buys) == len(bars) == len(sells)
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1
    assert buys[30] is True


def test_adx_dmi_crossover_gate():
    closes = [100.0 + i * 0.8 for i in range(80)]
    bars = _bars_from_closes(closes)
    plus_di, minus_di, adx = adx_di(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        14,
    )
    assert plus_di[40] is not None and adx[40] is not None
    buys, sells = adx_signals(bars, AdxDmiParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    for i, b in enumerate(buys):
        if b:
            assert adx[i] is not None and adx[i] > 25


def test_elder_ray_bear_fade():
    # down then recovery so bear power negative then rising under rising EMA
    closes = [120.0 - i for i in range(40)] + [80.0 + i * 0.5 for i in range(40)]
    bars = _bars_from_closes(closes)
    buys, sells = elder_signals(bars, ElderRayParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)


def test_tsi_signal_and_zero_bias():
    closes = [100.0 + (i % 7) - 3 for i in range(30)] + [
        100.0 + i * 0.7 for i in range(80)
    ]
    bars = _bars_from_closes(closes)
    series = tsi([b.close for b in bars], 25, 13)
    assert any(x is not None for x in series)
    buys, sells = tsi_signals(bars, TsiParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    for i, b in enumerate(buys):
        if b:
            assert series[i] is not None and series[i] > 0


def test_schaff_stc_levels_and_engine():
    closes = [100.0 + i * 0.4 for i in range(60)] + [
        124.0 - i * 0.5 for i in range(60)
    ]
    bars = _bars_from_closes(closes)
    stc = schaff_stc([b.close for b in bars], 23, 50, 10)
    assert any(x is not None for x in stc)
    buys, sells = stc_signals(bars, SchaffStcParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    res = run_long_only(
        "TEST", "schaff-stc-v1", bars, buys, sells, buy_qty_pct=100.0
    )
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_crossover_helper():
    a: list[float | None] = [20.0, 30.0]
    b: list[float | None] = [25.0, 25.0]
    assert crossover(a, b, 1) is True
