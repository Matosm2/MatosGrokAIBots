"""No-lookahead HTF→LTF join using mtf_ohlcv TF_MS (supports 1w)."""

from __future__ import annotations

from typing import TypeVar

from backtest.path_b.mtf_ohlcv.timeframes import TF_MS, normalize_tf

T = TypeVar("T")


def bar_close_ms(open_time_ms: int, tf: str) -> int:
    return open_time_ms + TF_MS[normalize_tf(tf)]


def map_htf_onto_ltf(
    *,
    ltf_open_ms: list[int],
    ltf_tf: str,
    htf_open_ms: list[int],
    htf_values: list[T],
    htf_tf: str,
) -> list[T | None]:
    if len(htf_open_ms) != len(htf_values):
        raise ValueError("htf_open_ms and htf_values length mismatch")
    ltf_tf_n = normalize_tf(ltf_tf)
    htf_tf_n = normalize_tf(htf_tf)
    out: list[T | None] = []
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
        out.append(None if j < 0 else htf_values[j])
    return out
