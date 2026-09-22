"""stage3-bnb-sol-v1 — Stage 3 BNB+SOL-aware strategies (Track 1 Path B).

LOCKED ENCODE ORDER (1->5):
1. vwma-sma-cross-v1
2. phh-phl-accept-break-v1
3. t3-dual-cross-v1
4. decycler-osc-fast-slow-v1
5. itrend-trigger-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage3-bnb-sol-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "vwma-sma-cross-v1",
    "phh-phl-accept-break-v1",
    "t3-dual-cross-v1",
    "decycler-osc-fast-slow-v1",
    "itrend-trigger-v1",
)

# Timeframes
VWMA_SMA_TFS: tuple[str, ...] = ("1h", "4h")
PHH_PHL_TFS: tuple[str, ...] = ("15m", "1h")
T3_TFS: tuple[str, ...] = ("1h", "4h")
DECYCLER_TFS: tuple[str, ...] = ("1h", "4h")
ITREND_TFS: tuple[str, ...] = ("1h", "4h")

# Symbols (BTC first -> ETH -> SOL (HARD FILTER) -> BNB (HARD FILTER))
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "VWMA_SMA_TFS",
    "PHH_PHL_TFS",
    "T3_TFS",
    "DECYCLER_TFS",
    "ITREND_TFS",
    "DEFAULT_SYMBOLS",
]
