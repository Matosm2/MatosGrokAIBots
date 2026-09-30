"""stage29-dual-sol-bnb-v1 package.

Track 1 Path B after stage28 wipe (closest Vervoort@4h 0.832x; still short of FVE 1.055x / 1.20; BTC 0/32 FAIL LEAD).
Design bias: BTC LEAD PRIMARY CRITICAL — clear past Vervoort 0.832x / FVE 1.055x to >= 1.20 without over-damp.
Keep ETH denser n >> 9 secondary once BTC clears. SOL-after + BNB-survival tertiary.
EXIT stage28 ECxEMA / Vervoort ZL-HAxTyp / ZL-FIR / DV2.
Locked encode order (exactly 4):
  1. katsanos-stiffness-threshold
  2. cpr-range-break-accept
  3. varadi-dvs-stretch-midline
  4. historical-volatility-ratio-expand-dir
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9 (6..10).
"""

RESEARCH_ID = "stage29-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "katsanos-stiffness-threshold",
    "cpr-range-break-accept",
    "varadi-dvs-stretch-midline",
    "historical-volatility-ratio-expand-dir",
)

STRATEGY_IDS = (
    "katsanos-stiffness-threshold",
    "cpr-range-break-accept",
    "varadi-dvs-stretch-midline",
    "historical-volatility-ratio-expand-dir",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
