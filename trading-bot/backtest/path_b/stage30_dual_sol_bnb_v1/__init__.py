"""stage30-dual-sol-bnb-v1 package.

Track 1 Path B after stage29 wipe (closest DVS@4h Mode B 1.093x; still short of 1.20; BTC 0/32 FAIL LEAD).
Design bias: BTC LEAD PRIMARY CRITICAL — clear past DVS 1.093x / FVE 1.055x / Vervoort 0.832x to >= 1.20 without over-damp.
Keep ETH denser n >> 9 secondary once BTC clears. SOL-after + BNB-survival tertiary.
EXIT stage29 Stiffness / CPR / DVS / HVR.
Locked encode order (exactly 4):
  1. blau-dti-zero-cross
  2. arms-vama-dual-cross
  3. apirine-ma-bands-break
  4. ehlers-recursive-median-osc-zero
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9 (6..10).
"""

RESEARCH_ID = "stage30-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "blau-dti-zero-cross",
    "arms-vama-dual-cross",
    "apirine-ma-bands-break",
    "ehlers-recursive-median-osc-zero",
)

STRATEGY_IDS = (
    "blau-dti-zero-cross",
    "arms-vama-dual-cross",
    "apirine-ma-bands-break",
    "ehlers-recursive-median-osc-zero",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
