"""stage23-dual-sol-bnb-v1 package.

Track 1 Path B after stage22 (SOL 0.922x near-miss; Kagi rhyme).
Design bias: SOL >= 1.2x after BTC->ETH PRIMARY.
Keep BTC LEAD without over-damp. Denser n >> 9.
BNB-survival after 3-coin. EXIT stage22 percentile/zscore/AVWAP/VFI.
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
sol_smoke CRITICAL + btc_smoke + eth_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9.
"""

RESEARCH_ID = "stage23-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "qqe-trailing-cross",
    "mama-fama-cross",
    "wilder-volatility-system-flip",
    "chande-kroll-stop-flip",
)

STRATEGY_IDS = (
    "qqe-trailing-cross",
    "mama-fama-cross",
    "wilder-volatility-system-flip",
    "chande-kroll-stop-flip",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
