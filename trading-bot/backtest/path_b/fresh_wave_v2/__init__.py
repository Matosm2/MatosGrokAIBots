"""fresh-wave-v2 — five new Path B research IDs (no remakes of prior families)."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "psar-trend-v1",
    "cci-mr-v1",
    "aroon-trend-v1",
    "williams-r-mr-v1",
    "vortex-trend-v1",
)

RESEARCH_ID = "fresh-wave-v2"

# Coarser TFs first when compute-bound (kick packet priority).
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

__all__ = ["RESEARCH_ID", "STRATEGY_IDS", "COARSE_FIRST_TFS"]
