"""stage14-dual-sol-bnb-v1 package.

Track 1 Path B after stage13 (REI BTC PASS 1.530x -> ETH wipe -1.201x).
Design bias: BTC->ETH portability PRIMARY + BNB-portable SECONDARY.
Dual SOL+BNB identical params; denser BTC n >> 9; btc_smoke + eth_smoke + sol_smoke + bnb_smoke mandatory.
"""

RESEARCH_ID = "stage14-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "pee-ttf-zero-cross",
    "hannula-pfe-zero-cross",
    "absolute-strength-hist-zero",
    "leibfarth-apz-break-flip",
    "nadaraya-rq-estimate-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
