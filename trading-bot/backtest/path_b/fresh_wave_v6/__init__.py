"""fresh-wave-v6 — Mass Index / KST / Twiggs MF / DeMarker / Darvas Box."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "mass-index-bulge-v1",
    "kst-pring-v1",
    "twiggs-mf-v1",
    "demarker-zone-v1",
    "darvas-box-v1",
)

RESEARCH_ID = "fresh-wave-v6"

# Coarse-first for single-TF sprays (kick priority: 2d→4h then finer).
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

# Prefer 4h–1d for mass-index (then full 16).
PREFERRED_4H_1D: tuple[str, ...] = (
    "1d",
    "12h",
    "9h",
    "7h",
    "6h",
    "5h",
    "4h",
)

# Prefer 1d–2d first for KST / Darvas.
PREFERRED_1D_2D: tuple[str, ...] = ("2d", "1d")

# Frozen primary params
MI_SUM = 25
MI_BULGE_HIGH = 27.0
MI_BULGE_LOW = 26.5
MI_EMA = 9
KST_ROC = (10, 15, 20, 30)
KST_SMA = (10, 10, 10, 15)
KST_SIGNAL = 9
TMF_PERIOD = 21
TMF_CHANNEL_N = 20
DEM_LENGTH = 14
DEM_LOW = 0.30
DEM_HIGH = 0.70
DEM_MID = 0.50
DARVAS_LOOKBACK = 90
DARVAS_CONFIRM = 3

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "PREFERRED_4H_1D",
    "PREFERRED_1D_2D",
]
