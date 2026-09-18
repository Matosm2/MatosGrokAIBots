"""stage5-dual-sol-bnb-v1 — Stage 5 DUAL SOL+BNB survival strategies (Track 1 Path B).

LOCKED ENCODE ORDER (1->5):
1. cti-fast-slow-threshold-v1
2. atrpct-percentile-sma-cross-v1
3. mad-channel-break-rvol-v1
4. vidya-dual-or-close-cross-v1
5. supersmoother-dual-cross-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage5-dual-sol-bnb-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "cti-fast-slow-threshold-v1",
    "atrpct-percentile-sma-cross-v1",
    "mad-channel-break-rvol-v1",
    "vidya-dual-or-close-cross-v1",
    "supersmoother-dual-cross-v1",
)

# Timeframes per strategy (1H and 4H primary for all five)
CTI_TFS: tuple[str, ...] = ("1h", "4h")
ATRPCT_SMA_TFS: tuple[str, ...] = ("1h", "4h")
MAD_TFS: tuple[str, ...] = ("1h", "4h")
VIDYA_TFS: tuple[str, ...] = ("1h", "4h")
SUPERSMOOTHER_TFS: tuple[str, ...] = ("1h", "4h")

# Ladder symbols: BTC -> ETH -> SOL (HARD) -> BNB (HARD)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "CTI_TFS",
    "ATRPCT_SMA_TFS",
    "MAD_TFS",
    "VIDYA_TFS",
    "SUPERSMOOTHER_TFS",
    "DEFAULT_SYMBOLS",
]
