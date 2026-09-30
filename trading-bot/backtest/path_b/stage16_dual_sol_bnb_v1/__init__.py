"""stage16-dual-sol-bnb-v1 package.

Track 1 Path B after stage15 (0/40 BTC LEAD wipe — stage12 rhyme).
Design bias: BTC LEAD PRIMARY without stage12/15 over-damp.
Keep denser n >> 9 + BTC->ETH portability + BNB-survival after 3-coin clear.
Dual SOL+BNB identical params; btc_smoke + eth_smoke + sol_smoke + bnb_smoke mandatory.
"""

RESEARCH_ID = "stage16-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "ehlers-bandpass-zero",
    "ehlers-twopole-hp-zero",
    "three-line-break-flip",
    "wilder-swing-index-zero",
    "nison-kagi-yang-yin-flip",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
