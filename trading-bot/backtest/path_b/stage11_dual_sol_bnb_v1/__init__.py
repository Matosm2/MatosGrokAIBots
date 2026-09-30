"""stage11-dual-sol-bnb-v1 package.

Track 1 Path B after stage10 (TII SOL->BNB wipe).
Design bias: BNB-survival-FIRST; dual SOL+BNB identical params; denser BTC n >> 9; bnb_smoke after any SOL-clear.
"""

RESEARCH_ID = "stage11-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "chande-trendscore-zero-cross-v1",
    "pee-tdi-direction-zero-v1",
    "ehlers-leading-netlead-ema-v1",
    "gmma-osc-zero-cross-v1",
    "vqi-sum-sma-cross-v1",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
