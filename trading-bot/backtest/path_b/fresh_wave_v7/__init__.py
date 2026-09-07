"""fresh-wave-v7 — RVI Signal / CHOP breakout / Elder Impulse (last Part B seats)."""

from __future__ import annotations

STRATEGY_IDS: tuple[str, ...] = (
    "rvi-signal-v1",
    "chop-breakout-v1",
    "elder-impulse-v1",
)

RESEARCH_ID = "fresh-wave-v7"

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

# Prefer 4h–1d for RVI / Elder Impulse (then full 16).
PREFERRED_4H_1D: tuple[str, ...] = (
    "1d",
    "12h",
    "9h",
    "7h",
    "6h",
    "5h",
    "4h",
)

# Frozen primary params
RVI_LENGTH = 10
RVI_SIGNAL = 4
CHOP_LENGTH = 14
CHOP_TREND = 38.2
CHOP_HALT = 61.8
CHOP_BREAK_N = 20
CHOP_EXIT_N = 10
ELDER_EMA = 13
ELDER_CANCEL = 2
ELDER_MACD_FAST = 12
ELDER_MACD_SLOW = 26
ELDER_MACD_SIGNAL = 9

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "COARSE_FIRST_TFS",
    "PREFERRED_4H_1D",
]
