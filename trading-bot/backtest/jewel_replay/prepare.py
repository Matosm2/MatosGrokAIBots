"""Closed-bar sample prep for Path B real Jewel CSVs (Claude caveats)."""

from __future__ import annotations

from datetime import datetime, timezone

from backtest.jewel_replay.csv_loader import JewelBar

# Prefer sample start = first jewel_high day (Slow warms earlier; early exits are artefacts).
DEFAULT_SAMPLE_START = datetime(2017, 12, 31, tzinfo=timezone.utc)
DEFAULT_SAMPLE_START_MS = int(DEFAULT_SAMPLE_START.timestamp() * 1000)


def drop_last_open_bar(bars: list[JewelBar]) -> list[JewelBar]:
    """Drop the final row — treated as still-open / partial daily bar."""
    if not bars:
        return []
    return list(bars[:-1])


def cut_sample_start(
    bars: list[JewelBar],
    *,
    start_ms: int = DEFAULT_SAMPLE_START_MS,
) -> list[JewelBar]:
    """Inclusive cut: keep bars on/after start_ms (default 2017-12-31 UTC)."""
    return [b for b in bars if b.open_time_ms >= start_ms]


def prepare_closed_sample(
    bars: list[JewelBar],
    *,
    drop_open_last: bool = True,
    sample_start_ms: int | None = DEFAULT_SAMPLE_START_MS,
) -> tuple[list[JewelBar], list[str]]:
    """
    Apply Claude caveats before Mode-A rescore / windowing.

    1. Drop last row (still-open bar) for closed-bar fidelity.
    2. Prefer sample start 2017-12-31 (jewel_high warm-up; Slow from 2017-10-24).

    Returns (prepared_bars, notes).
    """
    notes: list[str] = []
    out = list(bars)
    if drop_open_last and out:
        last = out[-1]
        last_dt = datetime.fromtimestamp(last.open_time_ms / 1000.0, tz=timezone.utc)
        out = drop_last_open_bar(out)
        notes.append(
            f"Dropped last open/partial bar {last_dt:%Y-%m-%d} UTC "
            f"(closed-bar fidelity)."
        )
    if sample_start_ms is not None:
        before = len(out)
        out = cut_sample_start(out, start_ms=sample_start_ms)
        start_dt = datetime.fromtimestamp(sample_start_ms / 1000.0, tz=timezone.utc)
        notes.append(
            f"Sample start cut to {start_dt:%Y-%m-%d} UTC "
            f"(jewel_high warm-up; removed {before - len(out)} early bars)."
        )
    # Drop any remaining bars missing Slow or jewel_high (should be none after cut).
    complete = [
        b for b in out if b.slow is not None and b.jewel_high is not None
    ]
    if len(complete) < len(out):
        notes.append(
            f"Dropped {len(out) - len(complete)} bars with empty Slow/jewel_high."
        )
        out = complete
    return out, notes
