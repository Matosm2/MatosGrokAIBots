"""fresh-wave-v4 — Fisher / Coppock / UTC-ORB Path B research IDs."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "ehlers-fisher-v1",
    "coppock-curve-v1",
    "session-orb-v1",
)

RESEARCH_ID = "fresh-wave-v4"

# Fisher: full 16 TF spray (coarse-first for compute).
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

# Coppock: slow only (kick frozen).
COPPOCK_TFS: tuple[str, ...] = ("1d", "2d")

# ORB primary cell label (built from 5m; not a TF spray).
ORB_TF_LABEL = "orb-utc"

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "COPPOCK_TFS",
    "ORB_TF_LABEL",
]
