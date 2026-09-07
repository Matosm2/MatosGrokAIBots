"""fresh-wave-v5 — Elder FI / CMF / LinReg-R² / MFI / UO (+ chandelier helper)."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "elder-triple-screen-fi-v1",
    "cmf-flow-v1",
    "linreg-r2-v1",
    "mfi-only-v1",
    "ultimate-oscillator-v1",
)

RESEARCH_ID = "fresh-wave-v5"

# Coarse-first for single-TF sprays (kick priority).
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

# Prefer 4h–1d first for linreg / UO (then full 16 if compute).
PREFERRED_4H_1D: tuple[str, ...] = (
    "1d",
    "12h",
    "9h",
    "7h",
    "6h",
    "5h",
    "4h",
)

# Elder entry/tide pairs only (not full 16).
ELDER_PAIRS: tuple[tuple[str, str], ...] = (
    ("4h", "1d"),
    ("1d", "1w"),
)

# Primary params (sweeps as labeled rows).
CMF_PERIODS: tuple[int, ...] = (14, 20, 21, 30)
CMF_PRIMARY_PERIOD = 21
FI_EMA_LENGTHS: tuple[int, ...] = (2, 13)
LINREG_PRIMARY = (20, 0.7)
MFI_PRIMARY = (14, 20, 80)
UO_PRIMARY = (7, 14, 28)

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "PREFERRED_4H_1D",
    "ELDER_PAIRS",
    "CMF_PERIODS",
    "CMF_PRIMARY_PERIOD",
    "FI_EMA_LENGTHS",
    "LINREG_PRIMARY",
    "MFI_PRIMARY",
    "UO_PRIMARY",
]
