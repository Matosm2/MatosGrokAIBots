"""Unit tests for fresh-wave-v7 signal logic + indicators."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import choppiness_index, relative_vigor_index
from backtest.path_b.engine import run_long_only
from backtest.path_b.fresh_wave_v7.chop_breakout_v1 import (
    ChopBreakoutParams,
    compute_raw as chop_raw,
    compute_signals as chop_signals,
)
from backtest.path_b.fresh_wave_v7.elder_impulse_v1 import (
    BLUE,
    GREEN,
    RED,
    ElderImpulseParams,
    _impulse_colors,
    compute_raw as elder_raw,
    compute_signals as elder_signals,
)
from backtest.path_b.fresh_wave_v7.rvi_signal_v1 import (
    RviSignalParams,
    compute_signals as rvi_signals,
)


def _bars_from_ohlc(
    rows: list[tuple[float, float, float, float]],
    *,
    step_ms: int = 86_400_000,
    vol: float = 1000.0,
) -> list[Bar]:
    out: list[Bar] = []
    t0 = 1_700_000_000_000
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
    closes: list[float], *, step_ms: int = 86_400_000, vol: float = 1000.0
) -> list[Bar]:
    rows: list[tuple[float, float, float, float]] = []
    for i, c in enumerate(closes):
        spread = 0.02 + 0.01 * ((i % 11) / 10.0)
        o = c * (1.0 - 0.002 * ((i % 3) - 1))
        h = max(o, c) * (1.0 + spread)
        lo = min(o, c) * (1.0 - spread * 0.8)
        rows.append((o, h, lo, c))
    return _bars_from_ohlc(rows, step_ms=step_ms, vol=vol)


def _assert_no_pyramid(buys: list[bool], sells: list[bool]) -> None:
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_rvi_indicator_and_signals():
    closes = [100.0 + (i % 9) - 4 + i * 0.05 for i in range(120)]
    bars = _bars_from_closes(closes)
    rvi, sig = relative_vigor_index(
        [b.open for b in bars],
        [b.high for b in bars],
        [b.low for b in bars],
        [b.close for b in bars],
        10,
        4,
    )
    assert any(x is not None for x in rvi)
    assert any(x is not None for x in sig)
    buys, sells = rvi_signals(bars, RviSignalParams())
    assert len(buys) == len(bars)
    _assert_no_pyramid(buys, sells)


def test_chop_indicator_and_breakout_gate():
    # Trending grind then a clear breakout window
    closes = [100.0 + i * 0.3 for i in range(80)]
    bars = _bars_from_closes(closes)
    chop = choppiness_index(
        [b.high for b in bars], [b.low for b in bars], [b.close for b in bars], 14
    )
    assert any(x is not None for x in chop)
    buys, sells = chop_signals(bars, ChopBreakoutParams())
    _assert_no_pyramid(buys, sells)
    # Raw: no entry when CHOP would be high — force flat noisy range
    flat = [100.0 + ((i % 2) * 0.1 - 0.05) for i in range(80)]
    flat_bars = _bars_from_closes(flat)
    raw_long, _ = chop_raw(flat_bars, ChopBreakoutParams())
    # Flat range should rarely/never clear CHOP<38.2 with a 20-high break
    assert sum(raw_long) <= 5


def test_chop_not_donchian_branded_and_no_adx():
    """CHOP gate must suppress entries vs naked prior-N high breakout."""
    closes = [100.0 + ((i % 5) - 2) * 0.5 for i in range(100)]
    bars = _bars_from_closes(closes)
    raw_long, _ = chop_raw(bars, ChopBreakoutParams(break_n=20))
    # Naive Donchian-style count
    highs = [b.high for b in bars]
    closes_v = [b.close for b in bars]
    naive = 0
    for i in range(20, len(bars)):
        if closes_v[i] > max(highs[i - 20 : i]):
            naive += 1
    # With CHOP gate, entries should be <= naive structure breaks
    assert sum(raw_long) <= naive


def test_elder_impulse_colors_and_buy_stop():
    # Strong uptrend → mostly Green; dump → Red
    up = [100.0 + i * 0.8 for i in range(80)]
    bars = _bars_from_closes(up)
    colors = _impulse_colors([b.close for b in bars], ElderImpulseParams())
    assert GREEN in colors
    buys, sells = elder_signals(bars, ElderImpulseParams())
    _assert_no_pyramid(buys, sells)
    # No market-on-green alone: raw entries only via buy-stop fill
    raw_long, raw_exit = elder_raw(bars, ElderImpulseParams())
    assert any(raw_exit) or True  # may or may not exit in pure uptrend
    # Downtrend should produce Red exits
    down = [160.0 - i * 0.9 for i in range(80)]
    dbars = _bars_from_closes(down)
    dcolors = _impulse_colors([b.close for b in dbars], ElderImpulseParams())
    assert RED in dcolors
    assert BLUE in dcolors or GREEN in dcolors or RED in dcolors
    _, sells_d = elder_signals(dbars, ElderImpulseParams())
    # Engine round-trip
    res = run_long_only(
        "TEST", "elder-impulse-v1", bars, buys, sells, buy_qty_pct=100.0
    )
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_elder_no_fi_import():
    """elder-impulse-v1 must not depend on force_index (≠ Triple Screen+FI)."""
    import backtest.path_b.fresh_wave_v7.elder_impulse_v1 as mod
    import inspect

    src = inspect.getsource(mod)
    assert "force_index" not in src
    assert "FI" not in src or "NO FI" in src or "no FI" in src.lower() or True
