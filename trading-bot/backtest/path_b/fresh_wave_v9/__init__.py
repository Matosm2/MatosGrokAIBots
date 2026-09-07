"""fresh-wave-v9 — Camarilla UTC / MESA Sine / Funding-fade."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "camarilla-utc-v1",
    "mesa-sine-v1",
    "funding-fade-v1",
)

RESEARCH_ID = "fresh-wave-v9"

# Coarse-first for sprays that allow full 16 (mesa).
COARSE_FIRST_TFS: tuple[str, ...] = (
    "2d",
    "1d",
    "12h",
    "9h",
    "7h",
    "6h",
    "5h",
    "4h",
    "3h",
    "2h",
    "1h",
    "90m",
    "30m",
    "15m",
    "10m",
    "5m",
)

# Camarilla: TF 15m–1h vs daily levels (primary Mode A).
CAMARILLA_TFS: tuple[str, ...] = ("1h", "30m", "15m")

# MESA: prefer 1h–4h; full 16 OK.
PREFERRED_1H_4H: tuple[str, ...] = (
    "4h",
    "3h",
    "2h",
    "1h",
    "90m",
)

# Funding fade: price mgmt on Spot 1h–4h.
FUNDING_TFS: tuple[str, ...] = ("4h", "3h", "2h", "1h")

# Frozen params
CAMARILLA_ADJ_MULT = 1.1
MESA_DOMINANT_CYCLE = 15
MESA_ADVANCE_DEG = 45.0
FUNDING_MODE_A_THR = 0.001  # 0.10% per 8h in Binance decimal units
FUNDING_Z_TAU = 2.0
FUNDING_Z_WINDOW_SETTLEMENTS = 90  # ~30d × 3 settlements/day
FUNDING_EXIT_SETTLEMENTS = 2

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "CAMARILLA_TFS",
    "PREFERRED_1H_4H",
    "FUNDING_TFS",
]
