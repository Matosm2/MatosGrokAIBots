"""Synthetic tests for jewel-strength-hold-v1 Path B replay (no real Jewel data)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from backtest.jewel_replay.csv_loader import JewelBar, load_jewel_csv
from backtest.jewel_replay.engine import run_replay
from backtest.jewel_replay.report import (
    MODE_A_PCT,
    MODE_B_PCT,
    DualModeRow,
    summarize,
)
from backtest.jewel_replay.signals import (
    JewelParams,
    Variant,
    atr_wilder,
    compute_signals,
    crossover_level,
)
from backtest.jewel_replay.window import (
    apply_window,
    filter_bars_last_months,
    months_before,
    resolve_windows,
    window_start_ms,
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


def _ms(y: int, m: int, d: int) -> int:
    return int(datetime(y, m, d, tzinfo=timezone.utc).timestamp() * 1000)


def _bar(ms: int, close: float = 100.0) -> JewelBar:
    return JewelBar(
        open_time_ms=ms,
        open=close,
        high=close + 1,
        low=close - 1,
        close=close,
        volume=1.0,
        slow=50.0,
        jewel_high=40.0,
    )


def test_months_before_and_window_start_ms():
    end = datetime(2024, 9, 5, tzinfo=timezone.utc)
    start = months_before(end, 6)
    assert start == datetime(2024, 3, 5, tzinfo=timezone.utc)
    # Day clamp: Mar 31 - 1 month -> Feb 28/29
    assert months_before(datetime(2024, 3, 31, tzinfo=timezone.utc), 1) == datetime(
        2024, 2, 29, tzinfo=timezone.utc
    )
    end_ms = _ms(2024, 9, 5)
    start_ms = window_start_ms(end_ms=end_ms, months=6)
    assert start_ms == _ms(2024, 3, 5)


def test_filter_bars_last_6m_keeps_trailing_window():
    bars = [
        _bar(_ms(2023, 1, 1)),
        _bar(_ms(2024, 1, 1)),
        _bar(_ms(2024, 4, 1)),
        _bar(_ms(2024, 8, 1)),
        _bar(_ms(2024, 9, 1)),
    ]
    filtered = filter_bars_last_months(bars, months=6)
    # end=2024-09-01 → start=2024-03-01; keep Apr, Aug, Sep
    assert [b.open_time_ms for b in filtered] == [
        _ms(2024, 4, 1),
        _ms(2024, 8, 1),
        _ms(2024, 9, 1),
    ]
    assert apply_window(bars, "all") == bars
    assert len(apply_window(bars, "6m")) == 3


def test_resolve_windows_both_all_6m():
    assert resolve_windows("all") == [("full", "all")]
    assert resolve_windows("6m") == [("last_6m", "6m")]
    assert resolve_windows("both") == [("full", "all"), ("last_6m", "6m")]


def test_dual_sizing_mode_a_vs_mode_b_on_fixture():
    """Mode A (100%) and Mode B (2.5%) share trade count/WR; returns scale."""
    bars = load_jewel_csv(FIXTURE)
    params = JewelParams(variant=Variant.V_ZONE)
    a = run_replay(
        "SYNTH",
        bars,
        params=params,
        buy_qty_pct=MODE_A_PCT,
        fee_rate=0.001,
        slippage_rate=0.0005,
    )
    b = run_replay(
        "SYNTH",
        bars,
        params=params,
        buy_qty_pct=MODE_B_PCT,
        fee_rate=0.001,
        slippage_rate=0.0005,
    )
    assert a.buy_qty_pct == 100.0
    assert b.buy_qty_pct == 2.5
    assert len(a.trades) == len(b.trades)
    assert len(a.trades) >= 1
    sa, sb = summarize(a), summarize(b)
    assert sa["trades"] == sb["trades"]
    assert sa["win_rate_pct"] == pytest.approx(sb["win_rate_pct"])
    # Same B&H (same bars); Mode A |return| should exceed Mode B |return|
    assert abs(float(sa["return_pct"])) > abs(float(sb["return_pct"]))
    row = DualModeRow(
        symbol="SYNTH",
        variant=Variant.V_ZONE.value,
        window_label="full",
        mode_a=a,
        mode_b=b,
    )
    sm = row.summarize()
    assert sm["trades"] == len(a.trades)
    # Gate requires n>0, WR>=60, Mode-A > B&H — fixture typically FAILs WR
    assert sm["gate_label"] in ("PASS", "FAIL")
    if sm["trades"] > 0 and float(sm["win_rate_pct"]) >= 60.0 and float(
        sm["mode_a_return_pct"]
    ) > float(sm["buy_hold_return_pct"]):
        assert sm["gate_pass"] is True
    else:
        assert sm["gate_pass"] is False


def test_gate_pass_requires_n_and_wr_and_mode_a_vs_bh():
    bars = load_jewel_csv(FIXTURE)
    a = run_replay("SYNTH", bars, buy_qty_pct=MODE_A_PCT)
    b = run_replay("SYNTH", bars, buy_qty_pct=MODE_B_PCT)
    row = DualModeRow(
        symbol="SYNTH",
        variant="V-zone",
        window_label="full",
        mode_a=a,
        mode_b=b,
    )
    sm = row.summarize()
    n = int(sm["trades"])
    expected = (
        n > 0
        and float(sm["win_rate_pct"]) >= 60.0
        and float(sm["mode_a_return_pct"]) > float(sm["buy_hold_return_pct"])
    )
    assert bool(sm["gate_pass"]) is expected


def test_window_filter_on_fixture_shortens_or_keeps():
    bars = load_jewel_csv(FIXTURE)
    six = apply_window(bars, "6m")
    # Fixture spans ~40 days — entire series fits inside last 6m of its own end
    assert len(six) == len(bars)
    assert six[0].open_time_ms == bars[0].open_time_ms


def test_prepare_closed_sample_drops_last_and_cuts_warmup():
    from backtest.jewel_replay.prepare import (
        DEFAULT_SAMPLE_START_MS,
        prepare_closed_sample,
    )

    bars = [
        _bar(_ms(2017, 10, 24)),
        _bar(_ms(2017, 12, 30)),
        _bar(_ms(2017, 12, 31)),
        _bar(_ms(2018, 1, 1)),
        _bar(_ms(2026, 9, 5)),  # open/partial — dropped
    ]
    out, notes = prepare_closed_sample(bars)
    assert out[0].open_time_ms == _ms(2017, 12, 31)
    assert out[-1].open_time_ms == _ms(2018, 1, 1)
    assert len(out) == 2
    assert any("Dropped last open" in n for n in notes)
    assert any("2017-12-31" in n for n in notes)
    assert DEFAULT_SAMPLE_START_MS == _ms(2017, 12, 31)


def test_win_rate_display_na_when_no_closed_trades():
    """ETH last-6m style: n=0 → WR n/a (not 0%), gate FAIL."""
    flat = [
        JewelBar(
            open_time_ms=_ms(2025, 9, 1) + i * 86_400_000,
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.0,
            volume=1.0,
            slow=50.0,
            jewel_high=40.0,
        )
        for i in range(10)
    ]
    a = run_replay("ETHUSDT", flat, buy_qty_pct=MODE_A_PCT)
    b = run_replay("ETHUSDT", flat, buy_qty_pct=MODE_B_PCT)
    assert len(a.trades) == 0
    row = DualModeRow(
        symbol="ETHUSDT",
        variant="V-zone",
        window_label="last_6m",
        mode_a=a,
        mode_b=b,
    )
    sm = row.summarize()
    assert sm["trades"] == 0
    assert sm["win_rate_display"] == "n/a"
    assert sm["gate_pass"] is False
    assert sm["gate_label"] == "FAIL"


def test_load_real_csv_allows_empty_slow_high_warmup():
    data = (
        Path(__file__).resolve().parent.parent
        / "backtest"
        / "jewel_replay"
        / "data"
        / "jewel-btc-daily.csv"
    )
    if not data.is_file():
        pytest.skip("real jewel-btc-daily.csv not on disk")
    bars = load_jewel_csv(data)
    assert len(bars) > 3000
    assert bars[0].slow is None or bars[0].jewel_high is None
    from backtest.jewel_replay.prepare import prepare_closed_sample

    prepared, _ = prepare_closed_sample(bars)
    assert prepared[0].slow is not None and prepared[0].jewel_high is not None
    # Last open bar dropped: prepared end < raw end
    assert prepared[-1].open_time_ms < bars[-1].open_time_ms
