"""stage19-dual-sol-bnb-v1 package.

Track 1 Path B after stage18 (0/40 BTC LEAD wipeout — stage12/15 rhyme).
Design bias: BTC LEAD PRIMARY without over-damp.
Keep denser n >> 9 + ETH portability + SOL-after-BTC+ETH + BNB-after-3-coin.
Identical dual params; btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
"""

RESEARCH_ID = "stage19-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "hhll-structure-flip",
    "starc-bands-break-flip",
    "vzo-zero-cross",
    "nvi-ema-cross",
    "fdi-low-trend-dir",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
