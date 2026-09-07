"""Unit tests for fresh-wave-v5 signal logic + chandelier helper."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import (
    chandelier_exit_long,
    cmf,
    force_index,
    linreg_channel,
    macd_hist,
    mfi,
    ultimate_oscillator,
)
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v5.chandelier_exit import (
    ChandelierParams,
    compute_long_stops,
)
from backtest.path_b.fresh_wave_v5.cmf_flow_v1 import (
    CmfFlowParams,
    compute_signals as cmf_signals,
)
from backtest.path_b.fresh_wave_v5.elder_triple_screen_fi_v1 import (
    ElderTripleScreenParams,
    compute_signals as elder_signals,
)
from backtest.path_b.fresh_wave_v5.linreg_r2_v1 import (
    LinregR2Params,
    compute_signals as linreg_signals,
)
from backtest.path_b.fresh_wave_v5.mfi_only_v1 import (
    MfiOnlyParams,
    compute_signals as mfi_signals,
)
from backtest.path_b.fresh_wave_v5.mtf_join import map_htf_onto_ltf
from backtest.path_b.fresh_wave_v5.ultimate_oscillator_v1 import (
    UltimateOscParams,
    compute_signals as uo_signals,
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


def test_force_index_and_macd_hist():
    closes = [100.0 + i for i in range(60)]
    vols = [1000.0] * 60
    fi = force_index(closes, vols)
    assert fi[0] is None
    assert fi[1] == (closes[1] - closes[0]) * vols[1]
    _m, _s, hist = macd_hist(closes)
    assert any(x is not None for x in hist)


def test_cmf_and_mode_a_signals():
    closes = [100.0 + (i % 5) - 2 for i in range(80)]
    bars = _bars_from_closes(closes)
    series = cmf(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        [b.volume for b in bars],
        21,
    )
    assert series[20] is not None
    buys, sells = cmf_signals(bars, CmfFlowParams(period=21, mode="A"))
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    buys_b, sells_b = cmf_signals(
        bars, CmfFlowParams(period=21, mode="B", channel_n=20)
    )
    _assert_no_pyramid(buys_b, sells_b)


def test_mfi_zone_exit_no_rsi():
    # Oscillate to create MFI extremes
    closes = []
    for i in range(100):
        if (i // 10) % 2 == 0:
            closes.append(100.0 - (i % 10))
        else:
            closes.append(90.0 + (i % 10))
    bars = _bars_from_closes(closes, vol=5000.0)
    series = mfi(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        [b.volume for b in bars],
        14,
    )
    assert any(x is not None for x in series)
    buys, sells = mfi_signals(bars, MfiOnlyParams())
    _assert_no_pyramid(buys, sells)
    res = run_long_only("TEST", "mfi-only-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_linreg_channel_and_modes():
    closes = [100.0 + i * 0.5 + ((i % 5) - 2) * 0.4 for i in range(80)]
    mid, upper, lower, slope, r2 = linreg_channel(closes, 20, 2.0)
    assert mid[19] is not None
    assert upper[19] > mid[19] > lower[19]
    assert slope[19] is not None and slope[19] > 0
    assert r2[19] is not None and r2[19] > 0.5
    bars = _bars_from_closes(closes)
    buys_a, sells_a = linreg_signals(bars, LinregR2Params(mode="A"))
    buys_b, sells_b = linreg_signals(bars, LinregR2Params(mode="B"))
    _assert_no_pyramid(buys_a, sells_a)
    _assert_no_pyramid(buys_b, sells_b)


def test_ultimate_oscillator_mode_b_cross():
    closes = [100.0] * 40 + [90.0 - i for i in range(20)] + [70.0 + i for i in range(40)]
    bars = _bars_from_closes(closes)
    series = ultimate_oscillator(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
    )
    assert any(x is not None for x in series)
    buys, sells = uo_signals(bars, UltimateOscParams(mode="B"))
    _assert_no_pyramid(buys, sells)
    buys_c, sells_c = uo_signals(bars, UltimateOscParams(mode="classic"))
    _assert_no_pyramid(buys_c, sells_c)


def test_chandelier_helper_atr22x3():
    closes = [100.0 + i * 0.1 for i in range(50)]
    bars = _bars_from_closes(closes)
    stops = compute_long_stops(bars, ChandelierParams())
    assert stops[21] is not None
    # Direct indicator parity
    direct = chandelier_exit_long(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        22,
        3.0,
    )
    assert stops[30] == direct[30]
    assert stops[30] < bars[30].high


def test_mtf_join_no_lookahead_4h_1d():
    # 1d bar open day0 closes at day1 00:00
    day = 86_400_000
    h4 = 4 * 3600 * 1000
    t0 = 1_704_067_200_000  # UTC midnight
    htf_open = [t0, t0 + day]
    htf_vals = [True, False]
    ltf_open = [t0 + i * h4 for i in range(6)] + [t0 + day]
    mapped = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4h",
        htf_open_ms=htf_open,
        htf_values=htf_vals,
        htf_tf="1d",
    )
    # First five 4h bars of day0 close before daily close → None
    assert mapped[:5] == [None] * 5
    assert mapped[5] is True
    assert mapped[6] is True


def test_elder_pair_signals_smoke():
    # Build simple rising tide + entry bars
    day = 86_400_000
    h4 = 4 * 3600 * 1000
    t0 = 1_704_067_200_000
    tide_closes = [100.0 + i * 0.5 for i in range(80)]
    tide = []
    for i, c in enumerate(tide_closes):
        tide.append(
            Bar(
                open_time_ms=t0 + i * day,
                open=c,
                high=c * 1.01,
                low=c * 0.99,
                close=c,
                volume=1000.0,
                close_time_ms=t0 + i * day + day - 1,
            )
        )
    entry = []
    for i in range(80 * 6):
        c = 100.0 + i * 0.05
        # Inject a pullback then breakout
        if 200 < i < 210:
            c = 100.0 + 200 * 0.05 - (i - 200) * 0.3
        entry.append(
            Bar(
                open_time_ms=t0 + i * h4,
                open=c,
                high=c * 1.01,
                low=c * 0.99,
                close=c,
                volume=1000.0 + (i % 5) * 50,
                close_time_ms=t0 + i * h4 + h4 - 1,
            )
        )
    buys, sells, stops = elder_signals(
        entry, tide, "4h", "1d", ElderTripleScreenParams(fi_ema=2)
    )
    assert len(buys) == len(entry) == len(sells) == len(stops)
    _assert_no_pyramid(buys, sells)
