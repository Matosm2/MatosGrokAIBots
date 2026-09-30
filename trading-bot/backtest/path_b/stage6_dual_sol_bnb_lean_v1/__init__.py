"""stage6-dual-sol-bnb-lean-v1 — Stage 6 DUAL SOL+BNB lean survival strategies (Track 1 Path B).

LOCKED ENCODE ORDER (LOCKED — exactly 3):
1. frama-fast-slow-cross-v1
2. hma-dual-cross-v1
3. mcginley-close-slope-cross-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage6-dual-sol-bnb-lean-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "frama-fast-slow-cross-v1",
    "hma-dual-cross-v1",
    "mcginley-close-slope-cross-v1",
)

# Timeframes per strategy (1H and 4H primary for all three)
FRAMA_TFS: tuple[str, ...] = ("1h", "4h")
HMA_TFS: tuple[str, ...] = ("1h", "4h")
MCGINLEY_TFS: tuple[str, ...] = ("1h", "4h")

# Ladder symbols: BTC -> ETH -> SOL (HARD) -> BNB (HARD)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "FRAMA_TFS",
    "HMA_TFS",
    "MCGINLEY_TFS",
    "DEFAULT_SYMBOLS",
]
