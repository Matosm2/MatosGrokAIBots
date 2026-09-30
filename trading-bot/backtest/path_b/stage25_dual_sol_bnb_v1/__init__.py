"""stage25-dual-sol-bnb-v1 package.

Track 1 Path B after stage24 (BTC PASS 0/32; Kirshenbaum ~1.113x near-miss; stage23 Chande-Kroll ~1.194x).
Design bias: BTC LEAD PRIMARY — push past ~1.194x / ~1.113x without over-damp.
Denser n >> 9. Keep ETH/SOL/BNB lessons.
EXIT stage24 Guppy-CBL / Kirshenbaum / IMI / Williams-AD.
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9.
"""

RESEARCH_ID = "stage25-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "ehlers-dsp-zero-cross",
    "nhnl-oscillator-zero",
    "volume-roc-dir",
    "elder-thermometer-cool-dir",
)

STRATEGY_IDS = (
    "ehlers-dsp-zero-cross",
    "nhnl-oscillator-zero",
    "volume-roc-dir",
    "elder-thermometer-cool-dir",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
