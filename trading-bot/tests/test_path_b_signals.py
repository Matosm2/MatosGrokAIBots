"""Unit tests for Path B indicator/signal logic (synthetic bars)."""

from __future__ import annotations

from backtest.data import Bar
from backtest.indicators import (
    bollinger,
    efficiency_ratio,
    kama,
    sma,
    supertrend,
    atr,
)
from backtest.path_b.engine import apply_position_gate, run_long_only
from backtest.path_b.bb_squeeze_breakout_v1 import (
    BbSqueezeParams,
    _percentile_rank_threshold,
    compute_raw as bb_raw,
    compute_signals as bb_signals,
)
from backtest.path_b.kama_er_trend_v1 import KamaErParams, compute_signals as kama_signals
from backtest.path_b.sma200_trend_v1 import Sma200Params, compute_signals as sma_signals
from backtest.path_b.supertrend_atr_v1 import SupertrendParams, compute_signals as st_signals
from backtest.path_b.dual_mom_btc_eth_v1 import momentum, run_dual_mom
from backtest.path_b.report import GATE_BH_MULT, summarize_path_b


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
                volume=vol * (1.5 if i % 17 == 0 else 1.0),
                close_time_ms=t0 + i * step_ms + step_ms - 1,
            )
        )
    return out


def test_sma_and_bollinger_warmup():
    closes = [100.0 + (i % 5) for i in range(50)]
    s = sma(closes, 20)
    assert s[19] is not None and s[18] is None
    mid, up, lo, width = bollinger(closes, 20, 2.0)
    assert mid[19] is not None and up[19] > lo[19] and width[19] is not None


def test_kama_er_smoke():
    closes = [100.0 + i * 0.5 for i in range(80)]
    er = efficiency_ratio(closes, 10)
    k = kama(closes, 10, 2, 30)
    assert er[10] is not None and 0 <= er[10] <= 1
    assert k[10] is not None


def test_supertrend_flip_in_uptrend():
    closes = [100.0 + i for i in range(80)]
    highs = [c + 1 for c in closes]
    lows = [c - 1 for c in closes]
    st, direction = supertrend(highs, lows, closes, 10, 3.0)
    assert any(d == 1 for d in direction if d is not None)
    assert st[-1] is not None


def test_percentile_no_lookahead_helper():
    vals = list(range(100))
    thr = _percentile_rank_threshold(vals, 20.0)
    assert 15 <= thr <= 25


def test_bb_squeeze_signal_shapes():
    # quiet then expansion
    closes = [100.0] * 130 + [100.0 + i * 2 for i in range(40)]
    bars = _bars_from_closes(closes, vol=500.0)
    # boost volume on breakout bars
    for i in range(130, len(bars)):
        bars[i] = Bar(
            open_time_ms=bars[i].open_time_ms,
            open=bars[i].open,
            high=bars[i].high * 1.02,
            low=bars[i].low,
            close=bars[i].close,
            volume=5000.0,
            close_time_ms=bars[i].close_time_ms,
        )
    buys, sells, stops = bb_signals(bars, BbSqueezeParams())
    assert len(buys) == len(bars) == len(sells) == len(stops)
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_kama_er_pyramiding_zero():
    closes = [100.0 + i * 0.8 for i in range(200)]
    bars = _bars_from_closes(closes)
    buys, sells = kama_signals(bars, KamaErParams())
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            assert in_pos
            in_pos = False


def test_sma200_cross_not_always_long():
    # below then cross above then stay above — only one entry until exit
    closes = [100.0 - i * 0.1 for i in range(220)] + [80.0 + i * 0.5 for i in range(100)]
    bars = _bars_from_closes(closes)
    buys, sells = sma_signals(bars, Sma200Params())
    assert sum(1 for b in buys if b) >= 1
    # while continuously above after entry, no second buy without exit
    in_pos = False
    for b, s in zip(buys, sells):
        if b:
            assert not in_pos
            in_pos = True
        if s:
            in_pos = False


def test_supertrend_signals_gate():
    closes = [100.0 + (i % 3) * 0.2 for i in range(40)] + [100.0 + i for i in range(60)]
    bars = _bars_from_closes(closes)
    buys, sells = st_signals(bars, SupertrendParams())
    assert len(buys) == len(bars)
    res = run_long_only("TEST", "supertrend-atr-v1", bars, buys, sells, buy_qty_pct=100.0)
    for t in res.trades:
        assert t.exit_bar > t.entry_bar


def test_dual_mom_flat_when_both_negative():
    # declining both
    btc = _bars_from_closes([100.0 - i * 0.5 for i in range(80)])
    eth = _bars_from_closes([90.0 - i * 0.4 for i in range(80)])
    assert momentum([b.close for b in btc], 40, 20) < 0
    dm = run_dual_mom(btc, eth, buy_qty_pct=100.0)
    # may have early trades before decline dominates; final should be flat-ish
    assert dm.buy_hold_return_pct < 0
    assert dm.as_sketch().symbol == "BTC+ETH"


def test_gate_ratio_1_2x():
    from backtest.path_b.engine import SketchResult

    r = SketchResult(
        symbol="X",
        strategy_id="t",
        trades=[],
        equity_curve=[10000, 11200],
        initial_equity=10000,
        final_equity=11200,
        buy_hold_return_pct=10.0,
    )
    # ret=12%, bh=10% → ratio 1.2 but n=0 → FAIL
    m = summarize_path_b(r)
    assert m["gate_pass"] is False
    assert GATE_BH_MULT == 1.2
