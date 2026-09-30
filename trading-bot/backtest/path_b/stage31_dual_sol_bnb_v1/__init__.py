"""stage31-dual-sol-bnb-v1 package.

Track 1 Path B after stage30 wipe (Apirine MAB BTC 1.520x thin-n=8 -> ETH wipe).
NEW GATE (Nuno 2026-09-22):
  PER-COIN GATE: Score BTC / ETH / SOL / BNB independently.
  Coin PASS (paper-eligible) if Mode-A >= 1.2x B&H on that coin AND denser sample n >= 40 (mid-encode gate patch).
  Thin n < 40 -> ineligible for paper even if x >= 1.2 (flag THIN clearly).
  Multiple strategies OK — best eligible per coin.
  Do NOT kill a seat only because it fails another coin.
  Full-ladder no longer required for paper.
  Score all four coins even if BTC fails.
  LIVE still NO. Hold open draft PR.

Locked encode order (exactly 4):
  1. apirine-sdo-zero-cross
  2. ehlers-madh-zero-cross
  3. premier-stochastic-osc-zero
  4. apirine-tradj-ema-cross

Hard excludes honored (all stage1-30 IDs).
Track B Hard Ban: no CK / QQE / MAMA / Wilder-VS.
"""

RESEARCH_ID = "stage31-dual-sol-bnb-v1"

ALL_STRATEGY_IDS = (
    "apirine-sdo-zero-cross",
    "ehlers-madh-zero-cross",
    "premier-stochastic-osc-zero",
    "apirine-tradj-ema-cross",
)

STRATEGY_IDS = (
    "apirine-sdo-zero-cross",
    "ehlers-madh-zero-cross",
    "premier-stochastic-osc-zero",
    "apirine-tradj-ema-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
