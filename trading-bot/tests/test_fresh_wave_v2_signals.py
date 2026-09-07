"""Unit tests for fresh-wave-v2 signal logic (synthetic bars)."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import aroon, cci, crossover, parabolic_sar, vortex, williams_r
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v2.aroon_trend_v1 import (
    AroonParams,
    compute_signals as aroon_signals,
)
from backtest.path_b.fresh_wave_v2.cci_mr_v1 import (
    CciParams,
    compute_signals as cci_signals,
)
from backtest.path_b.fresh_wave_v2.psar_trend_v1 import (
    PsarParams,
    compute_signals as psar_signals,
)
from backtest.path_b.fresh_wave_v2.vortex_trend_v1 import (
    VortexParams,
    compute_signals as vortex_signals,
)
from backtest.path_b.fresh_wave_v2.williams_r_mr_v1 import (
    WilliamsRParams,
    compute_signals as williams_signals,
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


def test_parabolic_sar_produces_values_and_flips():
    # down then up so SAR flips into a long (close crosses above SAR)
    closes = [140.0 - i for i in range(40)] + [100.0 + i for i in range(40)]
    bars = _bars_from_closes(closes)
    for i, b in enumerate(bars):
        o = closes[i] + (0.5 if i < 40 else -0.5)
        bars[i] = Bar(
            open_time_ms=b.open_time_ms,
            open=o,
            high=max(o, closes[i]) * 1.002,
            low=min(o, closes[i]) * 0.998,
            close=closes[i],
            volume=b.volume,
            close_time_ms=b.close_time_ms,
        )
    sar = parabolic_sar(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        af_start=0.02,
        af_step=0.02,
        af_max=0.2,
    )
    assert sar[0] is None
    assert sum(1 for x in sar if x is not None) >= 70
    buys, sells = psar_signals(bars, PsarParams())
    assert len(buys) == len(bars) == len(sells)
    _assert_no_pyramid(buys, sells)
    assert sum(buys) >= 1


def test_cci_mr_crossover_levels():
    # dip then rebound to force CCI through -100 then +100
    closes = [100.0] * 25 + [100.0 - i * 2 for i in range(1, 20)] + [
        60.0 + i * 3 for i in range(40)
    ]
    bars = _bars_from_closes(closes)
    series = cci(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        20,
        0.015,
    )
    assert series[19] is not None
    buys, sells = cci_signals(bars, CciParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)


def test_aroon_strength_gate():
    # prolonged uptrend → AroonUp high
    closes = [100.0 + i * 0.8 for i in range(80)]
    bars = _bars_from_closes(closes)
    up, down = aroon([b.high for b in bars], [b.low for b in bars], 25)
    assert up[50] is not None and up[50] >= 70
    buys, sells = aroon_signals(bars, AroonParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    # entry requires Up>=70 on crossover bar
    for i, b in enumerate(buys):
        if b:
            assert up[i] is not None and up[i] >= 70


def test_williams_r_bounds_and_signals():
    closes = [100.0 + (i % 9) - 4 for i in range(60)]
    bars = _bars_from_closes(closes)
    wr = williams_r(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        14,
    )
    assert wr[13] is not None
    assert all(x is None or -100.0 <= x <= 0.0 for x in wr)
    buys, sells = williams_signals(bars, WilliamsRParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)


def test_vortex_crossover_and_engine():
    closes = [100.0 + i * 0.5 for i in range(30)] + [115.0 - i * 0.6 for i in range(30)]
    bars = _bars_from_closes(closes)
    vip, vim = vortex(
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        14,
    )
    assert vip[20] is not None and vim[20] is not None
    buys, sells = vortex_signals(bars, VortexParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)
    res = run_long_only(
        "TEST", "vortex-trend-v1", bars, buys, sells, buy_qty_pct=100.0
    )
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_crossover_helper_used_by_mr():
    a: list[float | None] = [-120.0, -90.0]
    b: list[float | None] = [-100.0, -100.0]
    assert crossover(a, b, 1) is True
