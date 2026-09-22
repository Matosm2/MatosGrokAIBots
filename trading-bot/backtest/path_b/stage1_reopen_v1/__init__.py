"""stage1-reopen-v1 — Stage 1 partial reopen strategies.

LOCKED ENCODE ORDER (1->5):
1. classic-floor-pivots-utc-v1
2. pdh-pdl-accept-break-v1
3. pvt-ema-cross-v1
4. accdist-sma-cross-v1
5. asi-dual-break-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage1-reopen-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "classic-floor-pivots-utc-v1",
    "pdh-pdl-accept-break-v1",
    "pvt-ema-cross-v1",
    "accdist-sma-cross-v1",
    "asi-dual-break-v1",
)

# Timeframes
PIVOT_TFS: tuple[str, ...] = ("15m", "1h")
PDH_PDL_TFS: tuple[str, ...] = ("15m", "1h")
PVT_TFS: tuple[str, ...] = ("1h", "4h")
ACCDIST_TFS: tuple[str, ...] = ("1h", "4h")
ASI_TFS: tuple[str, ...] = ("1h", "4h")

# Symbols
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "PIVOT_TFS",
    "PDH_PDL_TFS",
    "PVT_TFS",
    "ACCDIST_TFS",
    "ASI_TFS",
    "DEFAULT_SYMBOLS",
]
