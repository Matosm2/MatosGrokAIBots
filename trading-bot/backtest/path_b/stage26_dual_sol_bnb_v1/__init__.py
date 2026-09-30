"""stage26-dual-sol-bnb-v1 package.

Track 1 Path B after stage25 (NHNL BTC 1.687x -> ETH 1.085x FAIL; n=8 THIN).
Design bias: ETH-after-BTC PRIMARY CRITICAL — need BTC clear >= 1.20 without over-damp
PLUS ETH >= 1.2x with denser n >> 9. Keep SOL-after + BNB-survival.
EXIT stage25 DSP/NHNL/VROC/thermo.
Locked encode order (exactly 4):
  1. katsanos-fve-zero-cross
  2. ehlers-convolution-zero
  3. hilbert-inst-trendline-cross
  4. elder-safezone-trail-flip
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke CRITICAL + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9 (6..10).
"""

RESEARCH_ID = "stage26-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "katsanos-fve-zero-cross",
    "ehlers-convolution-zero",
    "hilbert-inst-trendline-cross",
    "elder-safezone-trail-flip",
)

STRATEGY_IDS = (
    "katsanos-fve-zero-cross",
    "ehlers-convolution-zero",
    "hilbert-inst-trendline-cross",
    "elder-safezone-trail-flip",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
