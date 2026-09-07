"""fresh-wave-v8 — Gann HiLo / Asian-London / FI(13) / Cyber Cycle / Fractals."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "gann-hilo-activator-v1",
    "asian-london-break-v1",
    "force-index-13-v1",
    "cyber-cycle-v1",
    "williams-fractals-v1",
)

RESEARCH_ID = "fresh-wave-v8"

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

# Prefer 1h–1d for Gann HiLo / Cyber Cycle (then full 16).
PREFERRED_1H_1D: tuple[str, ...] = (
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
)

# Prefer 4h–1d for FI(13).
PREFERRED_4H_1D: tuple[str, ...] = (
    "1d",
    "12h",
    "9h",
    "7h",
    "6h",
    "5h",
    "4h",
)

# Prefer 1h–4h for Williams Fractals.
PREFERRED_1H_4H: tuple[str, ...] = (
    "4h",
    "3h",
    "2h",
    "1h",
    "90m",
)

# Asian→London scored only on 5m/15m (forbidden Session ORB encode).
ASIAN_LONDON_TFS: tuple[str, ...] = ("5m", "15m")

# Frozen primary params
GANN_HILO_N = 3
ASIAN_BOX_START_MIN = 0  # 00:00 UTC
ASIAN_BOX_END_MIN = 7 * 60  # 07:00 UTC
ASIAN_FLAT_MIN = 16 * 60  # 16:00 UTC flat
ASIAN_TP_MULT = 1.0
FI_EMA = 13
CYBER_ALPHA = 0.07
FRACTAL_BARS = 5  # classic Williams 5-bar

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "PREFERRED_1H_1D",
    "PREFERRED_4H_1D",
    "PREFERRED_1H_4H",
    "ASIAN_LONDON_TFS",
]
