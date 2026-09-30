"""stage17-dual-sol-bnb-v1 package.

Track 1 Path B after stage16 (Kagi BTC->ETH clear -> SOL 0.807x FAIL).
Design bias: SOL >= 1.2x after BTC->ETH clear PRIMARY.
Keep denser n >> 9 + BNB-after-3-coin.
Identical dual params; btc_smoke + eth_smoke + sol_smoke CRITICAL + bnb_smoke.
"""

RESEARCH_ID = "stage17-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "heikin-ashi-bias-flip",
    "blau-ergodic-mdi-signal-cross",
    "dss-bressert-trigger-cross",
    "bostian-iii-sma-zero",
    "ehlers-predictive-ma-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
