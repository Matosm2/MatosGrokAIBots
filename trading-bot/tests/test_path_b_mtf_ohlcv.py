"""Unit tests: TF mapping + deterministic aggregation for owned-tf-sweep-v1."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backtest.data import Bar
from backtest.path_b.mtf_ohlcv.aggregate import aggregate_bars
from backtest.path_b.mtf_ohlcv.timeframes import (
    M2_M4_HTF,
    SWEEP_TFS,
    TF_MS,
    TF_SOURCE,
    htf_for,
    mapping_table,
    normalize_tf,
)


def _ms(y, m, d, hh=0, mm=0):
    return int(datetime(y, m, d, hh, mm, tzinfo=timezone.utc).timestamp() * 1000)


def _bar(open_ms: int, o, h, l, c, v=1.0, dur_ms: int = 5 * 60_000) -> Bar:
    return Bar(open_ms, float(o), float(h), float(l), float(c), float(v), open_ms + dur_ms - 1)


def test_sweep_tf_count_and_htf_map_complete():
    assert len(SWEEP_TFS) == 16
    assert set(M2_M4_HTF) == set(SWEEP_TFS)
    assert M2_M4_HTF["5m"] == "1h"
    assert M2_M4_HTF["10m"] == "1h"
    assert M2_M4_HTF["15m"] == "1h"
    assert M2_M4_HTF["30m"] == "4h"
    assert M2_M4_HTF["90m"] == "4h"
    assert M2_M4_HTF["1h"] == "4h"
    assert M2_M4_HTF["2h"] == "4h"
    assert M2_M4_HTF["3h"] == "4h"
    assert M2_M4_HTF["4h"] == "1d"
    assert M2_M4_HTF["5h"] == "1d"
    assert M2_M4_HTF["6h"] == "1d"
    assert M2_M4_HTF["7h"] == "1d"
    assert M2_M4_HTF["9h"] == "2d"
    assert M2_M4_HTF["12h"] == "2d"
    assert M2_M4_HTF["1d"] == "2d"
    assert M2_M4_HTF["2d"] == "1w"
    # Reject interim ladders
    assert htf_for("5m") != "30m"
    assert htf_for("30m") != "2h"
    assert htf_for("2h") != "12h"


def test_mapping_table_sources():
    rows = {m.tf: m for m in mapping_table()}
    assert rows["5m"].native and rows["5m"].source == "5m"
    assert rows["1d"].native and rows["1d"].source == "1d"
    assert rows["90m"].source == "5m" and rows["90m"].factor == 18
    assert rows["2d"].source == "1d" and rows["2d"].factor == 2
    assert rows["1w"].source == "1d" and rows["1w"].factor == 7
    for tf, (src, factor) in TF_SOURCE.items():
        assert TF_MS[tf] == TF_MS[src] * factor


def test_aggregate_90m_from_30m_style_via_5m():
    """90m = 18×5m; OHLCV correctness on a single complete bucket."""
    # Use a known 90m bucket aligned to epoch
    # Find a 90m-aligned open near a fixed time
    t0 = _ms(2024, 1, 1, 0, 0)
    # Align to 90m bucket
    dur = TF_MS["90m"]
    bo = (t0 // dur) * dur
    src = []
    # 18 five-minute bars
    prices = [(100 + i, 110 + i, 90 + i, 105 + i) for i in range(18)]
    for i, (o, h, l, c) in enumerate(prices):
        src.append(_bar(bo + i * TF_MS["5m"], o, h, l, c, v=float(i + 1)))
    out = aggregate_bars(src, "90m")
    assert len(out) == 1
    b = out[0]
    assert b.open_time_ms == bo
    assert b.open == prices[0][0]
    assert b.high == max(p[1] for p in prices)
    assert b.low == min(p[2] for p in prices)
    assert b.close == prices[-1][3]
    assert b.volume == sum(range(1, 19))


def test_aggregate_2d_from_1d():
    d0 = _bar(_ms(2024, 1, 1), 10, 12, 9, 11, dur_ms=TF_MS["1d"])
    d1 = _bar(_ms(2024, 1, 2), 11, 15, 10, 14, dur_ms=TF_MS["1d"])
    d2 = _bar(_ms(2024, 1, 3), 14, 16, 13, 15, dur_ms=TF_MS["1d"])  # incomplete pair drop
    # Ensure Jan1 is on a 2d bucket boundary for UTC rule
    bo = (d0.open_time_ms // TF_MS["2d"]) * TF_MS["2d"]
    # Rebuild so first two days share same 2d bucket
    # 2d buckets from epoch: use bars whose opens fall in same bucket
    bars = [
        _bar(bo, 10, 12, 9, 11, dur_ms=TF_MS["1d"]),
        _bar(bo + TF_MS["1d"], 11, 15, 10, 14, dur_ms=TF_MS["1d"]),
        _bar(bo + 2 * TF_MS["1d"], 14, 16, 13, 15, dur_ms=TF_MS["1d"]),
    ]
    out = aggregate_bars(bars, "2d")
    assert len(out) >= 1
    b = out[0]
    assert b.open == 10
    assert b.high == 15
    assert b.low == 9
    assert b.close == 14
    assert b.volume == 2.0


def test_incomplete_bucket_dropped():
    bo = 0
    # only 2 of 3 five-minute bars for a 15m bucket
    src = [
        _bar(bo, 1, 2, 0.5, 1.5),
        _bar(bo + TF_MS["5m"], 1.5, 2.5, 1.0, 2.0),
    ]
    assert aggregate_bars(src, "15m") == []


def test_normalize_aliases():
    assert normalize_tf("4H") == "4h"
    assert normalize_tf("1D") == "1d"
    assert normalize_tf("2D") == "2d"
