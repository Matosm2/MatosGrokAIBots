"""Deterministic OHLCV aggregation (UTC continuous buckets, no lookahead).

Only complete buckets are emitted: every constituent source bar must be present
for [bucket_open, bucket_open + target_ms). Incomplete trailing buckets are dropped.
"""

from __future__ import annotations

from collections import defaultdict

from backtest.data import Bar
from backtest.path_b.mtf_ohlcv.timeframes import (
    TF_MS,
    TF_SOURCE,
    bucket_open_ms,
    normalize_tf,
)


def aggregate_bars(source: list[Bar], target_tf: str) -> list[Bar]:
    """Aggregate sorted source bars into target_tf using UTC bucket opens.

    Requires source TF to divide target (per TF_SOURCE). Factor must match
    target_ms // source_ms. Emits a bar only when `factor` source bars land
    in the bucket (complete bar-close semantics).
    """
    target = normalize_tf(target_tf)
    src_tf, factor = TF_SOURCE[target]
    if factor == 1:
        return list(source)

    target_ms = TF_MS[target]
    # Group by bucket
    buckets: dict[int, list[Bar]] = defaultdict(list)
    for b in source:
        bo = bucket_open_ms(b.open_time_ms, target)
        # Only keep bars whose open falls inside the bucket window
        if bo <= b.open_time_ms < bo + target_ms:
            buckets[bo].append(b)

    out: list[Bar] = []
    for bo in sorted(buckets):
        group = sorted(buckets[bo], key=lambda x: x.open_time_ms)
        if len(group) < factor:
            continue
        # Take exactly `factor` earliest bars in bucket (ignore extras if any)
        group = group[:factor]
        # Require contiguous coverage: first open == bucket open and last covers close
        if group[0].open_time_ms != bo:
            continue
        last = group[-1]
        # last bar must close at or after bucket close for bar-close completeness
        # Using open of last + implied: if we have `factor` bars starting at bo
        # with correct source spacing, bucket is complete.
        d0 = group[0]
        out.append(
            Bar(
                open_time_ms=bo,
                open=d0.open,
                high=max(g.high for g in group),
                low=min(g.low for g in group),
                close=last.close,
                volume=sum(g.volume for g in group),
                close_time_ms=bo + target_ms - 1,
            )
        )
    return out


def aggregate_1d_to_nw(daily: list[Bar], n: int) -> list[Bar]:
    """Aggregate consecutive daily bars into n-day bars (index-paired from start).

    Used for 2d (n=2) and 1w (n=7) when preferring index pairing for daily HTFs.
    Drops a trailing incomplete group. Prefer UTC `aggregate_bars` for sweep
    consistency; this helper matches open-proxy 2D pairing style when needed.
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    out: list[Bar] = []
    usable = len(daily) - (len(daily) % n)
    for i in range(0, usable, n):
        chunk = daily[i : i + n]
        d0, dN = chunk[0], chunk[-1]
        out.append(
            Bar(
                open_time_ms=d0.open_time_ms,
                open=d0.open,
                high=max(b.high for b in chunk),
                low=min(b.low for b in chunk),
                close=dN.close,
                volume=sum(b.volume for b in chunk),
                close_time_ms=dN.close_time_ms,
            )
        )
    return out
