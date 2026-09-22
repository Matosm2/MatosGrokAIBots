"""stage15-dual-sol-bnb-v1 package.

Track 1 Path B after stage14 (TTF cleared BTC->ETH->SOL then BNB 0.093x quiet wipe).
Design bias: BNB-survival CRITICAL after 3-coin clear + keep BTC->ETH portability + denser n >> 9.
Dual SOL+BNB identical params; btc_smoke + eth_smoke + sol_smoke + bnb_smoke mandatory.
"""

RESEARCH_ID = "stage15-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "ehlers-spearman-rank-zero",
    "ehlers-uo2025-hpdiff-zero",
    "ehlers-corr-cycle-real-zero",
    "ehlers-net-myrsi-zero",
    "varadi-dvi-midline-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
