"""stage22-dual-sol-bnb-v1 package.

Track 1 Path B after stage21 (0 BTC wipe on vol-expansion/bar-pattern; stage12/15/18/20/21 rhyme).
Design bias: BTC LEAD PRIMARY without over-damp.
Prefer denser n >> 9. Keep ETH/SOL/BNB lessons.
Prefer percentile-channel / zscore-hold / anchored-vwap / katsanos-vfi.
EXIT stage21 Chaikin/outside/Ulcer/Parkinson/inside.
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9.
Priority-kill #4 katsanos-vfi-zero-cross if BTC-smoke chop under costs like stage20 volume.
"""

RESEARCH_ID = "stage22-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "percentile-channel-break",
    "zscore-threshold-hold",
    "anchored-vwap-swing-flip",
    "katsanos-vfi-zero-cross",
)

STRATEGY_IDS = (
    "percentile-channel-break",
    "zscore-threshold-hold",
    "anchored-vwap-swing-flip",
    "katsanos-vfi-zero-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
