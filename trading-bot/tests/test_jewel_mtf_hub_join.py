"""Tests for multi-TF OHLCV join — no lookahead (jewel-mtf-hub-regime-v1 scaffold)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backtest.jewel_mtf_hub.join import (
    TF_MS,
    assert_no_lookahead_sample,
    bar_close_ms,
    map_htf_indices_onto_ltf,
    map_htf_onto_ltf,
    normalize_tf,
)
from backtest.jewel_mtf_hub.ohlcv import OhlcvBar, join_htf_ohlcv_onto_ltf


def _ms(y: int, m: int, d: int, h: int = 0) -> int:
    return int(datetime(y, m, d, h, tzinfo=timezone.utc).timestamp() * 1000)


def test_normalize_tf_aliases():
    assert normalize_tf("4h") == "4H"
    assert normalize_tf("daily") == "1D"
    assert normalize_tf("2D") == "2D"
    with pytest.raises(ValueError):
        normalize_tf("1h")


def test_bar_close_ms_durations():
    t0 = _ms(2024, 1, 1)
    assert bar_close_ms(t0, "4H") - t0 == TF_MS["4H"]
    assert bar_close_ms(t0, "1D") - t0 == TF_MS["1D"]
    assert bar_close_ms(t0, "2D") - t0 == TF_MS["2D"]


def test_1d_onto_4h_no_lookahead_before_daily_close():
    """Daily bar 2024-01-01 closes at 2024-01-02 00:00 — unavailable on Jan 1 4H bars."""
    htf_open = [_ms(2024, 1, 1), _ms(2024, 1, 2)]
    htf_vals = [10.0, 20.0]
    # Six 4H bars on Jan 1 (0..20h) + first bar of Jan 2 (00:00)
    ltf_open = [_ms(2024, 1, 1, h) for h in (0, 4, 8, 12, 16, 20)] + [
        _ms(2024, 1, 2, 0)
    ]
    mapped = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_values=htf_vals,
        htf_tf="1D",
    )
    # Jan 1 4H opens 00..16: LTF close before daily close → None
    assert mapped[:5] == [None, None, None, None, None]
    # Jan 1 20:00 4H closes exactly when daily closes (Jan 2 00:00) → available
    assert mapped[5] == 10.0
    # Jan 2 00:00 4H still sees completed daily Jan 1 (day-2 daily not closed yet)
    assert mapped[6] == 10.0

    idxs = map_htf_indices_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_tf="1D",
    )
    assert idxs[:5] == [None] * 5
    assert idxs[5] == 0
    assert idxs[6] == 0
    assert_no_lookahead_sample(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_tf="1D",
        mapped_indices=idxs,
    )


def test_same_close_instant_allows_htf():
    """When LTF and HTF close at the same instant, HTF is usable (bar-close)."""
    # Daily open Jan1 → close Jan2 00:00
    # 4H open Jan1 20:00 → close Jan2 00:00 — same instant
    htf_open = [_ms(2024, 1, 1)]
    ltf_open = [_ms(2024, 1, 1, 20)]
    mapped = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_values=[42.0],
        htf_tf="1D",
    )
    assert mapped == [42.0]


def test_2d_onto_1d_forward_fill():
    htf_open = [_ms(2024, 1, 1), _ms(2024, 1, 3)]  # 2D bars
    htf_vals = ["A", "B"]
    # Daily bars Jan1..Jan5
    ltf_open = [_ms(2024, 1, d) for d in range(1, 6)]
    mapped = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="1D",
        htf_open_ms=htf_open,
        htf_values=htf_vals,
        htf_tf="2D",
    )
    # 2D Jan1 closes Jan3 00:00 → first available on daily open Jan3 (close Jan4)
    # daily Jan1 close=Jan2: no 2D done yet → None
    # daily Jan2 close=Jan3: 2D Jan1 closes Jan3 → "A"
    # daily Jan3 close=Jan4: still "A" (2D Jan3 closes Jan5)
    # daily Jan4 close=Jan5: 2D Jan3 closes Jan5 → "B"
    # daily Jan5 close=Jan6: "B"
    assert mapped[0] is None  # Jan1
    assert mapped[1] == "A"  # Jan2
    assert mapped[2] == "A"  # Jan3
    assert mapped[3] == "B"  # Jan4
    assert mapped[4] == "B"  # Jan5


def test_join_htf_ohlcv_onto_ltf_fields():
    htf = [
        OhlcvBar(_ms(2024, 1, 1), 100, 110, 90, 105, 10.0),
        OhlcvBar(_ms(2024, 1, 2), 105, 120, 100, 115, 20.0),
    ]
    ltf = [
        OhlcvBar(_ms(2024, 1, 1, 20), 1, 2, 0.5, 1.5, 1.0),  # closes Jan2 00:00 → sees day1
        OhlcvBar(_ms(2024, 1, 2, 4), 2, 3, 1.5, 2.5, 1.0),  # closes Jan2 08:00 → still day1
        OhlcvBar(_ms(2024, 1, 2, 20), 3, 4, 2.5, 3.5, 1.0),  # closes Jan3 00:00 → day2
    ]
    joined = join_htf_ohlcv_onto_ltf(
        ltf_bars=ltf, ltf_tf="4H", htf_bars=htf, htf_tf="1D"
    )
    assert joined[0].htf_close == 105.0
    assert joined[0].htf_open_time_ms == _ms(2024, 1, 1)
    assert joined[1].htf_close == 105.0
    assert joined[2].htf_close == 115.0
    assert joined[2].htf_volume == 20.0


def test_length_mismatch_raises():
    with pytest.raises(ValueError, match="length mismatch"):
        map_htf_onto_ltf(
            ltf_open_ms=[_ms(2024, 1, 1)],
            ltf_tf="4H",
            htf_open_ms=[_ms(2024, 1, 1)],
            htf_values=[1.0, 2.0],
            htf_tf="1D",
        )


def test_assert_no_lookahead_detects_violation():
    ltf_open = [_ms(2024, 1, 1, 0)]
    htf_open = [_ms(2024, 1, 1)]
    # Fake index 0 would be lookahead for early 4H bar (daily not closed)
    with pytest.raises(AssertionError, match="lookahead"):
        assert_no_lookahead_sample(
            ltf_open_ms=ltf_open,
            ltf_tf="4H",
            htf_open_ms=htf_open,
            htf_tf="1D",
            mapped_indices=[0],
        )
