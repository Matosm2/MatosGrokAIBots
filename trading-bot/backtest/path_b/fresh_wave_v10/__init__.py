"""fresh-wave-v10 — VWAP-UTC-σ / SMI-Blau / Woodie-UTC / Chaikin Osc / Laguerre price."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "vwap-utc-sigma-v1",
    "smi-blau-v1",
    "woodie-utc-v1",
    "chaikin-osc-v1",
    "laguerre-price-v1",
)

RESEARCH_ID = "fresh-wave-v10"

# Coarse-first for sprays that allow full 16.
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

# VWAP UTC σ: prefer 15m–1h (session bands).
VWAP_TFS: tuple[str, ...] = ("1h", "30m", "15m")

# SMI Blau / Chaikin Osc: prefer 15m–4h.
PREFERRED_15M_4H: tuple[str, ...] = (
    "4h",
    "3h",
    "2h",
    "1h",
    "90m",
    "30m",
    "15m",
)

# Woodie UTC: prefer 5m–1h.
WOODIE_TFS: tuple[str, ...] = ("1h", "30m", "15m", "10m", "5m")

# Laguerre price: prefer 1h–4h.
PREFERRED_1H_4H: tuple[str, ...] = (
    "4h",
    "3h",
    "2h",
    "1h",
    "90m",
)

# Frozen params
VWAP_SIGMA_MULT = 2.0
SMI_LENGTH = 13
SMI_SMOOTH1 = 3
SMI_SMOOTH2 = 3
SMI_SIGNAL = 3
SMI_OB = 40.0
SMI_OS = -40.0
CHAIKIN_FAST = 3
CHAIKIN_SLOW = 10
LAGUERRE_GAMMA = 0.8

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "VWAP_TFS",
    "PREFERRED_15M_4H",
    "WOODIE_TFS",
    "PREFERRED_1H_4H",
]
