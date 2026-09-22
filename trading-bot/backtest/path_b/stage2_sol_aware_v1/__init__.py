"""stage2-sol-aware-v1 — Stage 2 SOL-aware strategies.

LOCKED ENCODE ORDER (1->5):
1. pwh-pwl-accept-break-v1
2. ehlers-cg-osc-trigger-v1
3. alma-fast-slow-cross-v1
4. cmo-zero-cross-v1
5. ehlers-roofing-zero-cross-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage2-sol-aware-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "pwh-pwl-accept-break-v1",
    "ehlers-cg-osc-trigger-v1",
    "alma-fast-slow-cross-v1",
    "cmo-zero-cross-v1",
    "ehlers-roofing-zero-cross-v1",
)

# Timeframes
PWH_PWL_TFS: tuple[str, ...] = ("15m", "1h")
EHLERS_CG_TFS: tuple[str, ...] = ("1h", "4h")
ALMA_TFS: tuple[str, ...] = ("1h", "4h")
CMO_TFS: tuple[str, ...] = ("1h", "4h")
ROOFING_TFS: tuple[str, ...] = ("1h", "4h")

# Symbols (BTC first -> ETH -> SOL (HARD FILTER) -> BNB)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "PWH_PWL_TFS",
    "EHLERS_CG_TFS",
    "ALMA_TFS",
    "CMO_TFS",
    "ROOFING_TFS",
    "DEFAULT_SYMBOLS",
]
