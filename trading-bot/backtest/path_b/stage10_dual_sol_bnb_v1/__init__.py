"""stage10-dual-sol-bnb-v1 — Stage 10 DUAL SOL+BNB survival strategies (Track 1 Path B).

LOCKED ENCODE ORDER (LOCKED — exactly 4 + optional 5th DEMA last):
1. tii-midline-fifty-cross-v1
2. rainbow-osc-zero-cross-v1
3. dorsey-relvol-midline-fifty-v1
4. tcf-plus-sign-flip-v1
5. dema-fast-slow-cross-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage10-dual-sol-bnb-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "tii-midline-fifty-cross-v1",
    "rainbow-osc-zero-cross-v1",
    "dorsey-relvol-midline-fifty-v1",
    "tcf-plus-sign-flip-v1",
    "dema-fast-slow-cross-v1",
)

# Timeframes per strategy (1H and 4H primary for all seats)
TII_TFS: tuple[str, ...] = ("1h", "4h")
RO_TFS: tuple[str, ...] = ("1h", "4h")
RELVOL_TFS: tuple[str, ...] = ("1h", "4h")
TCF_TFS: tuple[str, ...] = ("1h", "4h")
DEMA_TFS: tuple[str, ...] = ("1h", "4h")

# Ladder symbols: BTC -> ETH -> SOL (HARD) -> BNB (HARD)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "TII_TFS",
    "RO_TFS",
    "RELVOL_TFS",
    "TCF_TFS",
    "DEMA_TFS",
    "DEFAULT_SYMBOLS",
]
