"""stage4-bnb-first-v1 — Stage 4 BNB-survival-FIRST strategies (Track 1 Path B).

LOCKED ENCODE ORDER (1->5):
1. rvol-pivot-structure-break-v1
2. emv-zero-rvol-atr-gate-v1
3. pvo-gate-sma-mom-v1
4. p4h-hl-accept-break-v1
5. zlema-sma-cross-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage4-bnb-first-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "rvol-pivot-structure-break-v1",
    "emv-zero-rvol-atr-gate-v1",
    "pvo-gate-sma-mom-v1",
    "p4h-hl-accept-break-v1",
    "zlema-sma-cross-v1",
)

# Timeframes per strategy
RVOL_PIVOT_TFS: tuple[str, ...] = ("1h", "4h")
EMV_TFS: tuple[str, ...] = ("1h", "4h")
PVO_TFS: tuple[str, ...] = ("1h", "4h")
P4H_TFS: tuple[str, ...] = ("15m", "1h")
ZLEMA_TFS: tuple[str, ...] = ("1h", "4h")

# Symbols (BTC first -> ETH -> SOL (HARD FILTER) -> BNB (HARD FILTER))
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "RVOL_PIVOT_TFS",
    "EMV_TFS",
    "PVO_TFS",
    "P4H_TFS",
    "ZLEMA_TFS",
    "DEFAULT_SYMBOLS",
]
