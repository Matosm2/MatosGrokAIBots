"""stage8-dual-sol-bnb-v1 — Stage 8 DUAL SOL+BNB survival strategies (Track 1 Path B).

LOCKED ENCODE ORDER (LOCKED — exactly 4):
1. ao-median-zero-cross-v1
2. pgo-threshold-zeroexit-v1
3. roc-zero-cross-v1
4. wma-fast-slow-cross-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage8-dual-sol-bnb-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "ao-median-zero-cross-v1",
    "pgo-threshold-zeroexit-v1",
    "roc-zero-cross-v1",
    "wma-fast-slow-cross-v1",
)

# Timeframes per strategy (1H and 4H primary for all four)
AO_TFS: tuple[str, ...] = ("1h", "4h")
PGO_TFS: tuple[str, ...] = ("1h", "4h")
ROC_TFS: tuple[str, ...] = ("1h", "4h")
WMA_TFS: tuple[str, ...] = ("1h", "4h")

# Ladder symbols: BTC -> ETH -> SOL (HARD) -> BNB (HARD)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "AO_TFS",
    "PGO_TFS",
    "ROC_TFS",
    "WMA_TFS",
    "DEFAULT_SYMBOLS",
]
