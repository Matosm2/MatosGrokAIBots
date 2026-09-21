"""stage12-dual-sol-bnb-v1 package.

Track 1 Path B after stage11 (Pee TDI SOL->BNB wipe).
Design bias: BNB-survival-CRITICAL; dual SOL+BNB identical params; denser BTC n >> 9; bnb_smoke CRITICAL after any SOL-clear.
"""

RESEARCH_ID = "stage12-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "blau-csi-ergodic-signal-cross-v1",
    "ehlers-edcf-filt-lag-cross-v1",
    "ehlers-ultimate-smoother-dual-cross-v1",
    "ehlers-gaussian-fast-slow-cross-v1",
    "swenlin-pmo-signal-cross-v1",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
