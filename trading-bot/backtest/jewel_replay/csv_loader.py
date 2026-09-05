"""Load research CSV: time, OHLCV, Slow, High."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class JewelBar:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    slow: float | None
    jewel_high: float | None


_TIME_KEYS = ("time", "open_time", "open_time_ms", "timestamp", "datetime", "date")
_SLOW_KEYS = ("Slow", "slow", "jewel_slow", "JewelSlow")
_HIGH_KEYS = ("High", "high_jewel", "jewel_high", "JewelHigh", "jhigh")


def _pick(row: dict[str, str], keys: tuple[str, ...], *, required: str) -> str:
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    # case-insensitive fallback
    lower = {k.lower(): v for k, v in row.items()}
    for k in keys:
        if k.lower() in lower and lower[k.lower()] not in (None, ""):
            return lower[k.lower()]
    raise KeyError(f"CSV missing required column for {required}; tried {keys}")


def _pick_optional(row: dict[str, str], keys: tuple[str, ...]) -> str | None:
    """Return cell text or None when blank / missing (warm-up rows)."""
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    lower = {k.lower(): v for k, v in row.items()}
    for k in keys:
        if k.lower() in lower and lower[k.lower()] not in (None, ""):
            return lower[k.lower()]
    return None


def _parse_optional_float(raw: str | None) -> float | None:
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    return float(s)


def _parse_time_ms(raw: str) -> int:
    s = raw.strip()
    if s.isdigit():
        v = int(s)
        # seconds vs ms
        return v if v >= 1_000_000_000_000 else v * 1000
    # ISO-8601
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def load_jewel_csv(path: Path | str) -> list[JewelBar]:
    """
    Expected columns (names flexible):
      time | open_time_ms, open, high, low, close, volume, Slow, High

    Note: price column `high` is OHLC high; Jewel High is `Slow`/`High` plot columns
    (or jewel_high). If both `High` (Jewel) and OHLC high collide, prefer:
      open,high,low,close,volume,Slow,jewel_high
    or export Jewel High as `Slow`/`High` with OHLC as open/high/low/close — then
    Jewel High must be named `jewel_high` / `JewelHigh` to avoid clobbering OHLC high.

    Empty Slow / jewel_high cells are allowed as None (indicator warm-up).
    """
    path = Path(path)
    bars: list[JewelBar] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"Empty CSV: {path}")
        fields = list(reader.fieldnames)
        # Resolve Jewel High column without stealing OHLC high when both exist.
        jewel_high_col = None
        for k in ("jewel_high", "JewelHigh", "jhigh", "High", "high_jewel"):
            if k in fields:
                jewel_high_col = k
                break
        if jewel_high_col is None:
            # last resort: case-insensitive High but not the first 'high' if open present
            for name in fields:
                if name.lower() in ("jewel_high", "jhigh", "high_jewel"):
                    jewel_high_col = name
                    break
            if jewel_high_col is None:
                raise KeyError(
                    "CSV needs Jewel High column: jewel_high / JewelHigh / High "
                    f"(got columns {fields})"
                )

        # Ensure Slow column exists (may be blank on early rows).
        slow_col_present = any(
            k in fields or k.lower() in {f.lower() for f in fields} for k in _SLOW_KEYS
        )
        if not slow_col_present:
            raise KeyError(
                f"CSV missing required column for Slow; tried {_SLOW_KEYS} "
                f"(got columns {fields})"
            )

        for row in reader:
            t_raw = _pick(row, _TIME_KEYS, required="time")
            slow_raw = _pick_optional(row, _SLOW_KEYS)
            jh_raw = row.get(jewel_high_col)
            bars.append(
                JewelBar(
                    open_time_ms=_parse_time_ms(t_raw),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume") or 0.0),
                    slow=_parse_optional_float(slow_raw),
                    jewel_high=_parse_optional_float(
                        jh_raw if jh_raw not in (None, "") else None
                    ),
                )
            )
    if not bars:
        raise ValueError(f"No rows in {path}")
    return bars
