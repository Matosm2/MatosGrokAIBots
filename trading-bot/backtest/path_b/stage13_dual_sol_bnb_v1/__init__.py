"""stage13-dual-sol-bnb-v1 package.

Track 1 Path B after stage12 (0/40 BTC LEAD wipe).
Design bias: BTC-clearing PRIMARY + BNB-portable SECONDARY.
Dual SOL+BNB identical params; denser BTC n >> 9; btc_smoke + sol_smoke + bnb_smoke mandatory.
"""

RESEARCH_ID = "stage13-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "demark-rei-zero-cross-v1",
    "khalil-pzo-zero-cross-v1",
    "mobius-tmo-main-zero-v1",
    "donovan-range-filter-flip-v1",
    "clv-sma-zero-cross-v1",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
