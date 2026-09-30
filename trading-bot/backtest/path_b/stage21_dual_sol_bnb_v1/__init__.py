"""stage21-dual-sol-bnb-v1 package.

Track 1 Path B after stage20 (0 BTC chop under costs; stage12/15/18/20 rhyme).
Design bias: BTC LEAD PRIMARY without over-damp.
Prefer denser n >> 9. Keep ETH/SOL/BNB lessons.
Prefer Chaikin-vol / outside-bar / Ulcer-recover / Parkinson / inside-bar.
EXIT stage20 VPCI/BW-MFI/DI/Kalman/RAVI.
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9.
Parkinson #4: DROPPED due to BTC-smoke redundancy with Chaikin #1 (>75% overlap, identical chop).
"""

RESEARCH_ID = "stage21-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "chaikin-volatility-dir",
    "outside-bar-polarity",
    "ulcer-index-recover-dir",
    "parkinson-vol-expansion-dir",
    "inside-bar-breakout",
)

# Active strategy list after Parkinson #4 dropped for BTC-smoke redundancy with Chaikin #1
STRATEGY_IDS = (
    "chaikin-volatility-dir",
    "outside-bar-polarity",
    "ulcer-index-recover-dir",
    "inside-bar-breakout",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
