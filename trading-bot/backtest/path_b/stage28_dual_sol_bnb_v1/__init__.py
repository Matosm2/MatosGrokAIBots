"""stage28-dual-sol-bnb-v1 package.

Track 1 Path B after stage27 wipe (closest Schwager-VR 0.698x regress vs FVE 1.055x; BTC 0/32 FAIL LEAD).
Design bias: BTC LEAD PRIMARY CRITICAL — push past FVE 1.055x / VR 0.698x to >= 1.20 without over-damp.
Keep ETH denser n >> 9 secondary. SOL-after + BNB-survival tertiary.
EXIT stage27 Qstick/Klinger/%Envelopes/Schwager-VR.
Locked encode order (exactly 4):
  1. ehlers-ec-ema-cross
  2. vervoort-zlha-typ-cross
  3. ehlers-fir-zl-price-cross
  4. dv2-varadi-midline
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9 (6..10).
"""

RESEARCH_ID = "stage28-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "ehlers-ec-ema-cross",
    "vervoort-zlha-typ-cross",
    "ehlers-fir-zl-price-cross",
    "dv2-varadi-midline",
)

STRATEGY_IDS = (
    "ehlers-ec-ema-cross",
    "vervoort-zlha-typ-cross",
    "ehlers-fir-zl-price-cross",
    "dv2-varadi-midline",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
