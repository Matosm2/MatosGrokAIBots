"""stage7-dual-sol-bnb-v1 — Stage 7 DUAL SOL+BNB survival strategies (Track 1 Path B).

LOCKED ENCODE ORDER (LOCKED — exactly 4):
1. er-sma-gate-cross-v1
2. ehlers-super-passband-rms-v1
3. rwi-high-low-threshold-v1
4. ehlers-reverse-ema-trend-cycle-v1
"""

from __future__ import annotations

RESEARCH_ID = "stage7-dual-sol-bnb-v1"

STRATEGY_IDS: tuple[str, ...] = (
    "er-sma-gate-cross-v1",
    "ehlers-super-passband-rms-v1",
    "rwi-high-low-threshold-v1",
    "ehlers-reverse-ema-trend-cycle-v1",
)

# Timeframes per strategy (1H and 4H primary for all four)
ER_SMA_TFS: tuple[str, ...] = ("1h", "4h")
SUPER_PASSBAND_TFS: tuple[str, ...] = ("1h", "4h")
RWI_TFS: tuple[str, ...] = ("1h", "4h")
REVERSE_EMA_TFS: tuple[str, ...] = ("1h", "4h")

# Ladder symbols: BTC -> ETH -> SOL (HARD) -> BNB (HARD)
DEFAULT_SYMBOLS: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")

__all__ = [
    "RESEARCH_ID",
    "STRATEGY_IDS",
    "ER_SMA_TFS",
    "SUPER_PASSBAND_TFS",
    "RWI_TFS",
    "REVERSE_EMA_TFS",
    "DEFAULT_SYMBOLS",
]
