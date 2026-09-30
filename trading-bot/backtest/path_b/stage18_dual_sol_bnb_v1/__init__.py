"""stage18-dual-sol-bnb-v1 package.

Track 1 Path B after stage17 (Bostian III dense BTC -> ETH HARD FAIL).
Design bias: BTC->ETH portability PRIMARY (stage13 REI + stage17 Bostian III rhyme).
Keep denser n >> 9 + SOL-after-BTC+ETH + BNB-after-3-coin.
Identical dual params; btc_smoke + eth_smoke CRITICAL + sol_smoke + bnb_smoke.
"""

RESEARCH_ID = "stage18-dual-sol-bnb-v1"

STRATEGY_IDS = (
    "dpo-zero-cross",
    "ppo-ema-signal-cross",
    "vhf-threshold-close-dir",
    "forecast-oscillator-zero",
    "projection-oscillator-trigger-cross",
)

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
