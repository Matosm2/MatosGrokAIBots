"""Multi-TF join: map HTF state onto LTF bars with NO lookahead.

HTF values become available only after the HTF bar closes.
For an LTF decision at LTF close time T_ltf_close, use the latest HTF bar
whose close time <= T_ltf_close.

Supported TFs: 4H, 1D, 2D (crypto-style continuous UTC sessions).
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")

# Bar durations in milliseconds (UTC continuous sessions).
TF_MS: dict[str, int] = {
    "4H": 4 * 60 * 60 * 1000,
    "1D": 24 * 60 * 60 * 1000,
    "2D": 2 * 24 * 60 * 60 * 1000,
}

_TF_ALIASES: dict[str, str] = {
    "4H": "4H",
    "4HOUR": "4H",
    "4HR": "4H",
    "240": "4H",
    "1D": "1D",
    "D": "1D",
    "1DAY": "1D",
    "DAILY": "1D",
    "2D": "2D",
    "2DAY": "2D",
}


def normalize_tf(tf: str) -> str:
    key = tf.strip().upper().replace(" ", "")
    if key not in _TF_ALIASES:
        raise ValueError(f"Unsupported TF {tf!r}; expected one of 4H, 1D, 2D")
    return _TF_ALIASES[key]


def bar_close_ms(open_time_ms: int, tf: str) -> int:
    """Close instant (ms) for a bar that opened at open_time_ms."""
    return open_time_ms + TF_MS[normalize_tf(tf)]


def map_htf_onto_ltf(
    *,
    ltf_open_ms: list[int],
    ltf_tf: str,
    htf_open_ms: list[int],
    htf_values: list[T],
    htf_tf: str,
) -> list[T | None]:
    """
    Forward-fill HTF values onto LTF bars without lookahead.

    For each LTF bar i (decision at LTF close), attach htf_values[j] where j is
    the last HTF bar with htf_close <= ltf_close. Bars before any completed HTF
    bar get None.

    Requires len(htf_open_ms) == len(htf_values). Both open-time series must be
    sorted ascending.
    """
    if len(htf_open_ms) != len(htf_values):
        raise ValueError("htf_open_ms and htf_values length mismatch")
    indices = map_htf_indices_onto_ltf(
        ltf_open_ms=ltf_open_ms,
        ltf_tf=ltf_tf,
        htf_open_ms=htf_open_ms,
        htf_tf=htf_tf,
    )
    return [None if j is None else htf_values[j] for j in indices]


def map_htf_indices_onto_ltf(
    *,
    ltf_open_ms: list[int],
    ltf_tf: str,
    htf_open_ms: list[int],
    htf_tf: str,
) -> list[int | None]:
    """Same as map_htf_onto_ltf but returns HTF bar indices (or None)."""
    ltf_tf_n = normalize_tf(ltf_tf)
    htf_tf_n = normalize_tf(htf_tf)
    out: list[int | None] = []
    j = -1
    n_htf = len(htf_open_ms)
    for open_ms in ltf_open_ms:
        ltf_close = bar_close_ms(open_ms, ltf_tf_n)
        while j + 1 < n_htf:
            htf_close = bar_close_ms(htf_open_ms[j + 1], htf_tf_n)
            if htf_close <= ltf_close:
                j += 1
            else:
                break
        out.append(j if j >= 0 else None)
    return out


def assert_no_lookahead_sample(
    *,
    ltf_open_ms: list[int],
    ltf_tf: str,
    htf_open_ms: list[int],
    htf_tf: str,
    mapped_indices: list[int | None],
) -> None:
    """Raise if any mapped HTF bar closes after the corresponding LTF close."""
    for i, j in enumerate(mapped_indices):
        if j is None:
            continue
        ltf_close = bar_close_ms(ltf_open_ms[i], ltf_tf)
        htf_close = bar_close_ms(htf_open_ms[j], htf_tf)
        if htf_close > ltf_close:
            raise AssertionError(
                f"lookahead at LTF i={i}: HTF j={j} closes {htf_close} "
                f"> LTF close {ltf_close}"
            )
