"""stage9-dual-sol-bnb-v1 — Stage 9 DUAL SOL+BNB survival strategies (Track 1 Path B).

LOCKED ENCODE ORDER (LOCKED — exactly 5):
1. psy-midline-fifty-cross-v1
2. disparity-sma-zero-cross-v1
3. wavetrend-wt1-wt2-cross-v1
4. rmi-midline-fifty-cross-v1
5. accel-bands-break-inside-exit-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage9-dual-sol-bnb-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "psy-midline-fifty-cross-v1",
    "disparity-sma-zero-cross-v1",
    "wavetrend-wt1-wt2-cross-v1",
    "rmi-midline-fifty-cross-v1",
    "accel-bands-break-inside-exit-v1",
)

# Timeframes per strategy (1H and 4H primary for all five)
PSY_TFS: tuple[str, ...] = ("1h", "4h")
DI_TFS: tuple[str, ...] = ("1h", "4h")
WT_TFS: tuple[str, ...] = ("1h", "4h")
RMI_TFS: tuple[str, ...] = ("1h", "4h")
ACCEL_TFS: tuple[str, ...] = ("1h", "4h")

# Ladder symbols: BTC -> ETH -> SOL (HARD) -> BNB (HARD)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "PSY_TFS",
    "DI_TFS",
    "WT_TFS",
    "RMI_TFS",
    "ACCEL_TFS",
    "DEFAULT_SYMBOLS",
]
