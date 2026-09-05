"""Synthetic tests for jewel-strength-hold-v1 Path B replay (no real Jewel data)."""

from __future__ import annotations

from pathlib import Path

import pytest

from backtest.jewel_replay.csv_loader import load_jewel_csv
from backtest.jewel_replay.engine import run_replay
from backtest.jewel_replay.report import summarize
from backtest.jewel_replay.signals import (
    JewelParams,
    Variant,
    atr_wilder,
    compute_signals,
    crossover_level,
)

FIXTURE = (
    Path(__file__).resolve().parent.parent
    / "backtest"
    / "jewel_replay"
    / "fixtures"
    / "synthetic_jewel_btc_daily.csv"
)


def test_fixture_exists_and_loads():
    assert FIXTURE.is_file()
    bars = load_jewel_csv(FIXTURE)
    assert len(bars) >= 30
    assert bars[0].slow == pytest.approx(50.0)
    assert bars[0].jewel_high == pytest.approx(40.0)


def test_crossover_level_pine_semantics():
    s: list[float | None] = [60.0, 70.0, 71.0, 69.0, 70.5]
    assert crossover_level(s, 70.0, 0) is False
    # 60 -> 70: cur is not > level
    assert crossover_level(s, 70.0, 1) is False
    # 70 -> 71: crosses above 70
    assert crossover_level(s, 70.0, 2) is True
    # 69 -> 70.5
    assert crossover_level(s, 70.0, 4) is True


def test_entry_a_and_entry_b_and_zone_exit_on_fixture():
    bars = load_jewel_csv(FIXTURE)
    sig = compute_signals(
        highs=[b.high for b in bars],
        lows=[b.low for b in bars],
        closes=[b.close for b in bars],
        slow=[b.slow for b in bars],
        high_j=[b.jewel_high for b in bars],
        params=JewelParams(),
    )
    # Entry A at bar where Slow crosses 70 (fixture bar 21)
    assert any(sig.entry_a), "expected Entry A (Slow cross 70)"
    assert any(sig.entry_b), "expected Entry B (High cross 80 with Slow>=70)"
    assert any(sig.zone_exit), "expected zone exit bars"
    # Entry A index
    a_idxs = [i for i, f in enumerate(sig.entry_a) if f]
    assert 21 in a_idxs
    b_idxs = [i for i, f in enumerate(sig.entry_b) if f]
    assert 29 in b_idxs


def test_v_zone_replay_no_pyramiding_and_zone_exits():
    bars = load_jewel_csv(FIXTURE)
    res = run_replay(
        "SYNTH",
        bars,
        params=JewelParams(variant=Variant.V_ZONE),
        fee_rate=0.001,
        slippage_rate=0.0005,
        buy_qty_pct=2.5,
    )
    assert res.buy_qty_pct == 2.5
    assert res.fee_rate == 0.001
    assert len(res.trades) >= 1
    last_exit = -1
    for t in res.trades:
        assert t.entry_bar > last_exit
        assert t.exit_bar > t.entry_bar
        assert t.exit_reason in ("zone", "zone+atr_stop")
        last_exit = t.exit_bar
    m = summarize(res)
    assert m["trades"] == len(res.trades)
    assert "win_rate_pct" in m
    assert "buy_hold_return_pct" in m
    assert "max_drawdown_pct" in m


def test_v_wide_can_exit_on_atr_stop():
    bars = load_jewel_csv(FIXTURE)
    res = run_replay(
        "SYNTH",
        bars,
        params=JewelParams(variant=Variant.V_WIDE),
        fee_rate=0.001,
        slippage_rate=0.0005,
    )
    reasons = {t.exit_reason for t in res.trades}
    # Crash bar should trigger atr path on at least one trade
    assert any("atr_stop" in t.exit_reason for t in res.trades), (
        f"expected an ATR stop exit, got reasons={reasons}"
    )


def test_atr_wilder_warmup():
    highs = [10.0 + i * 0.1 for i in range(20)]
    lows = [9.0 + i * 0.1 for i in range(20)]
    closes = [9.5 + i * 0.1 for i in range(20)]
    atr = atr_wilder(highs, lows, closes, 14)
    assert all(x is None for x in atr[:13])
    assert atr[13] is not None and atr[13] > 0
    assert atr[19] is not None


def test_no_lookahead_signal_uses_same_bar_only():
    """Crossover at i depends on i and i-1 only — classic bar-close semantics."""
    slow: list[float | None] = [50.0] * 5 + [69.0, 71.0]
    assert crossover_level(slow, 70.0, 5) is False
    assert crossover_level(slow, 70.0, 6) is True
