"""stage27-dual-sol-bnb-v1 package.

Track 1 Path B after stage26 (FVE dense n=40 @1.055x FAIL LEAD; Convolution/HT/SafeZone 0 BTC).
Design bias: BTC LEAD PRIMARY CRITICAL — push past FVE 1.055x to >= 1.20 without over-damp.
Keep ETH denser n >> 9 secondary. SOL-after + BNB-survival tertiary.
EXIT stage26 FVE/Convolution/HT_TRENDLINE/SafeZone.
Locked encode order (exactly 4):
  1. qstick-sma-zero
  2. klinger-signal-cross
  3. percent-envelopes-break
  4. schwager-vr-breakout
Identical dual params across BTC/ETH/SOL/BNB (never retune per coin).
btc_smoke CRITICAL + eth_smoke + sol_smoke + bnb_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9 (6..10).
"""

RESEARCH_ID = "stage27-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "qstick-sma-zero",
    "klinger-signal-cross",
    "percent-envelopes-break",
    "schwager-vr-breakout",
)

STRATEGY_IDS = (
    "qstick-sma-zero",
    "klinger-signal-cross",
    "percent-envelopes-break",
    "schwager-vr-breakout",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
