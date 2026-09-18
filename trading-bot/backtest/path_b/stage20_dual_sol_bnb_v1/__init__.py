"""stage20-dual-sol-bnb-v1 package.

Track 1 Path B after stage19 (HHLL 3-coin -> BNB -0.726x quiet wipe; TTF rhyme).
Design bias: BNB-survival CRITICAL after 3-coin clear.
Prefer denser n >> 9 (>> HHLL n=8). Keep BTC->ETH->SOL portability.
EXIT HHLL/STARC/VZO/NVI/FDI.
Identical dual params across BTC/ETH/SOL/BNB (never BNB-only Length/Mode B).
bnb_smoke CRITICAL + btc_smoke + eth_smoke + sol_smoke.
Tiny-n: BTC n <= 5 FAIL; flag n approx 9.
"""

RESEARCH_ID = "stage20-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "vpci-zero-cross",
    "bw-mfi-green-fade-flip",
    "demand-index-zero",
    "kalman-estimate-cross",
    "ravi-threshold-dir",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
