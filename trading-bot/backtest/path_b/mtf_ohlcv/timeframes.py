"""TF registry + frozen M2/M4 HTF map for owned-tf-sweep-v1.

Aggregation (CoS):
  - Cache native 5m once; aggregate all sub-daily TFs from 5m.
  - Cache native 1d once; aggregate 2d and 1w from 1d.
  - Bar-close / no lookahead: emit only complete UTC buckets.

M2/M4 HTF map (Strategy frozen — DO NOT substitute another ladder):
  5m→1h, 10m→1h, 15m→1h,
  30m→4h, 90m→4h, 1h→4h, 2h→4h, 3h→4h,
  4h→1d, 5h→1d, 6h→1d, 7h→1d,
  9h→2d, 12h→2d, 1d→2d,
  2d→1w (7×1d).

Scoring params (frozen): SMA200=200 bars; dual-mom lookback=20;
ema-rsi cooldown=6; regime ADX≥20+DI; RSI 60/50; KAMA ER 0.30/0.20;
ST ATR10×3; BB as Path B #14 (no retune).
"""

from __future__ import annotations

from dataclasses import dataclass

MS_MINUTE = 60_000
MS_HOUR = 60 * MS_MINUTE
MS_DAY = 24 * MS_HOUR

TF_MS: dict[str, int] = {
    "5m": 5 * MS_MINUTE,
    "10m": 10 * MS_MINUTE,
    "15m": 15 * MS_MINUTE,
    "30m": 30 * MS_MINUTE,
    "90m": 90 * MS_MINUTE,
    "1h": 1 * MS_HOUR,
    "2h": 2 * MS_HOUR,
    "3h": 3 * MS_HOUR,
    "4h": 4 * MS_HOUR,
    "5h": 5 * MS_HOUR,
    "6h": 6 * MS_HOUR,
    "7h": 7 * MS_HOUR,
    "9h": 9 * MS_HOUR,
    "12h": 12 * MS_HOUR,
    "1d": 1 * MS_DAY,
    "2d": 2 * MS_DAY,
    "1w": 7 * MS_DAY,
}

SWEEP_TFS: tuple[str, ...] = (
    "5m", "10m", "15m", "30m", "90m",
    "1h", "2h", "3h", "4h", "5h", "6h", "7h", "9h", "12h",
    "1d", "2d",
)

NATIVE_SOURCES: frozenset[str] = frozenset({"5m", "1d"})

# Target -> (source, factor)
TF_SOURCE: dict[str, tuple[str, int]] = {
    "5m": ("5m", 1),
    "10m": ("5m", 2),
    "15m": ("5m", 3),
    "30m": ("5m", 6),
    "90m": ("5m", 18),
    "1h": ("5m", 12),
    "2h": ("5m", 24),
    "3h": ("5m", 36),
    "4h": ("5m", 48),
    "5h": ("5m", 60),
    "6h": ("5m", 72),
    "7h": ("5m", 84),
    "9h": ("5m", 108),
    "12h": ("5m", 144),
    "1d": ("1d", 1),
    "2d": ("1d", 2),
    "1w": ("1d", 7),
}

# Exact frozen M2/M4 HTF map (lowercase canonical).
M2_M4_HTF: dict[str, str] = {
    "5m": "1h",
    "10m": "1h",
    "15m": "1h",
    "30m": "4h",
    "90m": "4h",
    "1h": "4h",
    "2h": "4h",
    "3h": "4h",
    "4h": "1d",
    "5h": "1d",
    "6h": "1d",
    "7h": "1d",
    "9h": "2d",
    "12h": "2d",
    "1d": "2d",
    "2d": "1w",
}

PRIORITY_TFS: tuple[str, ...] = ("1h", "4h", "1d", "2d", "15m", "30m")

_ALIASES: dict[str, str] = {
    "5M": "5m", "10M": "10m", "15M": "15m", "30M": "30m", "90M": "90m",
    "1H": "1h", "2H": "2h", "3H": "3h", "4H": "4h", "5H": "5h",
    "6H": "6h", "7H": "7h", "9H": "9h", "12H": "12h",
    "1D": "1d", "D": "1d", "DAILY": "1d",
    "2D": "2d", "2DAY": "2d",
    "1W": "1w", "W": "1w", "WEEKLY": "1w",
}


def normalize_tf(tf: str) -> str:
    raw = tf.strip()
    if raw in TF_MS:
        return raw
    key = raw.upper().replace(" ", "")
    if key in _ALIASES:
        return _ALIASES[key]
    low = raw.lower().replace(" ", "")
    if low in TF_MS:
        return low
    raise ValueError(f"Unsupported TF {tf!r}; expected one of {', '.join(TF_MS)}")


def bar_close_ms(open_time_ms: int, tf: str) -> int:
    return open_time_ms + TF_MS[normalize_tf(tf)]


def bucket_open_ms(open_time_ms: int, tf: str) -> int:
    dur = TF_MS[normalize_tf(tf)]
    return (open_time_ms // dur) * dur


def htf_for(ltf: str) -> str:
    """Frozen M2/M4 HTF for a decision LTF. Raises if LTF not in map."""
    key = normalize_tf(ltf)
    if key not in M2_M4_HTF:
        raise ValueError(f"No M2/M4 HTF mapping for {ltf!r}")
    return M2_M4_HTF[key]


@dataclass(frozen=True)
class TfMapping:
    tf: str
    source: str
    factor: int
    native: bool
    duration_ms: int
    m2_m4_htf: str | None

    @property
    def rule(self) -> str:
        if self.native:
            return f"native Binance `{self.tf}`"
        return f"aggregate {self.factor}× `{self.source}` → `{self.tf}` (UTC bucket, bar-close)"


def mapping_table() -> list[TfMapping]:
    out: list[TfMapping] = []
    for tf in list(SWEEP_TFS) + ["1w"]:
        src, factor = TF_SOURCE[tf]
        out.append(
            TfMapping(
                tf=tf,
                source=src,
                factor=factor,
                native=tf in NATIVE_SOURCES,
                duration_ms=TF_MS[tf],
                m2_m4_htf=M2_M4_HTF.get(tf),
            )
        )
    return out


def ordered_tfs() -> tuple[str, ...]:
    """Priority first, then remaining sweep TFs."""
    seen: list[str] = []
    for tf in PRIORITY_TFS:
        if tf not in seen:
            seen.append(tf)
    for tf in SWEEP_TFS:
        if tf not in seen:
            seen.append(tf)
    return tuple(seen)
