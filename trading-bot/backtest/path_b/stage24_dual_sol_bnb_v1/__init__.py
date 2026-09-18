"""stage24-dual-sol-bnb-v1 package.

Track 1 Path B after stage23 (BTC PASS 0/32; Chande-Kroll ~1.194x near-miss).
Design bias: BTC LEAD PRIMARY — push past ~1.194x without over-damp.
Denser n >> 9. Keep ETH/SOL/BNB lessons.
EXIT stage23 QQE/MAMA/Wilder/Chande-Kroll.
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9.
"""

RESEARCH_ID = "stage24-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "guppy-countback-line-flip",
    "kirshenbaum-bands-break",
    "imi-midline-fifty",
    "williams-ad-sma-cross",
)

STRATEGY_IDS = (
    "guppy-countback-line-flip",
    "kirshenbaum-bands-break",
    "imi-midline-fifty",
    "williams-ad-sma-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
