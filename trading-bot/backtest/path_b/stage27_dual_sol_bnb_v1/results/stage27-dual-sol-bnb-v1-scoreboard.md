# stage27-dual-sol-bnb-v1 — Scoreboard

- Generated: 2026-09-21 20:50:12 UTC
- Research ID: `stage27-dual-sol-bnb-v1` (Track 1 Path B)
- Stop-Ladder: `BTCUSDT -> ETHUSDT (HARD) -> SOLUSDT (HARD) -> BNBUSDT (HARD)`
- Gate Rule: Last 6m Mode-A Return >= 1.2x Buy & Hold, n > 5 (tiny-n kill threshold)
- Fees / Slip: 0.10% / side fee + 0.05% adverse slippage
- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)
- Strategy Encode Order (exactly 4):
  1. `qstick-sma-zero`
  2. `klinger-signal-cross`
  3. `percent-envelopes-break`
  4. `schwager-vr-breakout`

## Executive Summary
- Total Scored Cells: 32 / 128
- Pruned / Skipped by Stop-Ladder: 96
- Candidates Passing 6m Gate on at least 1 symbol: 0
- Full 4-Coin Ladder Complete Passes: 0

## PASS_6m Promoted Candidates
- *None. Zero candidates met the 6m >= 1.2x B&H hurdle with n > 5.*

## Full Stop-Ladder Scoreboard

| Symbol | Strategy ID | TF | Mode/Params | 6m Gate | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | 6m MaxDD% | Full Gate | Full Ret% | Full B&H% | Full xB&H | Full n | Ops 6m% | Ops Full% | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Retention Notes | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | `qstick-sma-zero` | 1h | mode_a|(N8) | **FAIL** | -63.81% | 27.43% | -2.327x | 379 | 17.7% | 68.90% | FAIL | -98.30% | 37.03% | -2.654x | 1508 | -2.45% | -9.66% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 1h | mode_a|(N10) | **FAIL** | -59.57% | 27.43% | -2.172x | 344 | 19.2% | 65.16% | FAIL | -98.08% | 37.03% | -2.648x | 1383 | -2.16% | -9.17% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 1h | mode_a|(N14) | **FAIL** | -53.65% | 27.43% | -1.956x | 282 | 19.1% | 60.89% | FAIL | -96.02% | 37.03% | -2.593x | 1131 | -1.82% | -7.49% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 1h | mode_a|(N20) | **FAIL** | -33.77% | 27.43% | -1.231x | 234 | 20.9% | 46.41% | FAIL | -92.12% | 37.03% | -2.487x | 952 | -0.94% | -5.94% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 4h | mode_a|(N8) | **FAIL** | 2.23% | 23.34% | 0.095x | 91 | 28.6% | 21.21% | FAIL | -47.15% | 36.92% | -1.277x | 363 | 0.12% | -1.35% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 4h | mode_a|(N10) | **FAIL** | 4.95% | 23.34% | 0.212x | 72 | 27.8% | 19.83% | FAIL | -38.98% | 36.92% | -1.056x | 320 | 0.19% | -1.00% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 4h | mode_a|(N14) | **FAIL** | -1.96% | 23.34% | -0.084x | 62 | 25.8% | 24.88% | FAIL | -30.80% | 36.92% | -0.834x | 270 | 0.03% | -0.65% | Y | Y | Y | Y | — | — |
| BTCUSDT | `qstick-sma-zero` | 4h | mode_a|(N20) | **FAIL** | 7.99% | 23.34% | 0.342x | 50 | 28.0% | 27.14% | FAIL | -34.72% | 36.92% | -0.941x | 216 | 0.29% | -0.81% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,13) | **FAIL** | -66.12% | 27.43% | -2.411x | 348 | 20.4% | 69.30% | FAIL | -97.64% | 37.03% | -2.636x | 1296 | -2.62% | -8.73% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 1h | mode_a|(21,34,13) | **FAIL** | -69.62% | 27.43% | -2.538x | 387 | 21.2% | 72.23% | FAIL | -98.38% | 37.03% | -2.656x | 1425 | -2.89% | -9.57% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,9) | **FAIL** | -69.08% | 27.43% | -2.519x | 391 | 23.0% | 71.99% | FAIL | -98.62% | 37.03% | -2.663x | 1468 | -2.85% | -9.94% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 1h | mode_a|(55,89,13) | **FAIL** | -63.45% | 27.43% | -2.313x | 320 | 23.4% | 68.19% | FAIL | -97.25% | 37.03% | -2.626x | 1206 | -2.44% | -8.38% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,13) | **FAIL** | -10.23% | 23.34% | -0.438x | 77 | 33.8% | 28.21% | FAIL | -58.63% | 36.92% | -1.588x | 336 | -0.22% | -1.94% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 4h | mode_a|(21,34,13) | **FAIL** | 2.46% | 23.34% | 0.106x | 82 | 41.5% | 21.10% | FAIL | -51.75% | 36.92% | -1.402x | 362 | 0.11% | -1.54% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,9) | **FAIL** | -0.94% | 23.34% | -0.040x | 86 | 39.5% | 26.47% | FAIL | -59.24% | 36.92% | -1.604x | 375 | 0.03% | -1.97% | Y | Y | Y | Y | — | — |
| BTCUSDT | `klinger-signal-cross` | 4h | mode_a|(55,89,13) | **FAIL** | 0.43% | 23.34% | 0.019x | 74 | 28.4% | 22.16% | FAIL | -59.31% | 36.92% | -1.607x | 321 | 0.06% | -2.03% | Y | Y | Y | Y | — | — |
| BTCUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.025) | **FAIL** | 5.07% | 27.43% | 0.185x | 14 | 35.7% | 9.51% | FAIL | -26.12% | 37.03% | -0.705x | 75 | 0.15% | -0.70% | Y | Y | Y | Y | — | — |
| BTCUSDT | `percent-envelopes-break` | 1h | mode_a|(len14,pct0.015) | **FAIL** | 8.24% | 27.43% | 0.301x | 32 | 37.5% | 14.84% | FAIL | -23.09% | 37.03% | -0.623x | 171 | 0.24% | -0.55% | Y | Y | Y | Y | — | — |
| BTCUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.04) | **FAIL** | 7.30% | 27.43% | 0.266x | 5 | 20.0% | 4.16% | FAIL | -0.27% | 37.03% | -0.007x | 20 | 0.20% | 0.02% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=5 <= 5) |
| BTCUSDT | `percent-envelopes-break` | 1h | mode_a|(len30,pct0.025) | **FAIL** | 2.15% | 27.43% | 0.078x | 18 | 33.3% | 15.47% | FAIL | -26.82% | 37.03% | -0.724x | 85 | 0.08% | -0.70% | Y | Y | Y | Y | — | — |
| BTCUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.025) | **FAIL** | 6.42% | 23.34% | 0.275x | 14 | 35.7% | 10.52% | FAIL | -22.17% | 36.92% | -0.600x | 67 | 0.19% | -0.49% | Y | Y | Y | Y | — | — |
| BTCUSDT | `percent-envelopes-break` | 4h | mode_a|(len14,pct0.015) | **FAIL** | -4.03% | 23.34% | -0.173x | 28 | 28.6% | 16.60% | FAIL | -30.37% | 36.92% | -0.823x | 114 | -0.05% | -0.75% | Y | Y | Y | Y | — | — |
| BTCUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.04) | **FAIL** | 11.53% | 23.34% | 0.494x | 6 | 33.3% | 8.33% | FAIL | -7.17% | 36.92% | -0.194x | 29 | 0.30% | -0.09% | Y | Y | Y | Y | — | THIN-N FLAG (BTC 6m n=6 in thin band [6..10]) |
| BTCUSDT | `percent-envelopes-break` | 4h | mode_a|(len30,pct0.025) | **FAIL** | 14.31% | 23.34% | 0.613x | 11 | 45.5% | 7.45% | FAIL | -25.18% | 36.92% | -0.682x | 60 | 0.37% | -0.53% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr2.0,M20) | **FAIL** | 7.02% | 27.43% | 0.256x | 54 | 33.3% | 16.78% | FAIL | -37.59% | 37.03% | -1.015x | 207 | 0.22% | -1.07% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr1.5,M10) | **FAIL** | -7.21% | 27.43% | -0.263x | 101 | 25.7% | 25.19% | FAIL | -62.02% | 37.03% | -1.675x | 385 | -0.14% | -2.27% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 1h | mode_a|(n10,thr1.5,M20) | **FAIL** | 1.55% | 27.43% | 0.057x | 67 | 31.3% | 22.82% | FAIL | -43.98% | 37.03% | -1.187x | 257 | 0.09% | -1.31% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 1h | mode_a|(n20,thr2.0,M10) | **FAIL** | 0.12% | 27.43% | 0.004x | 68 | 27.9% | 18.54% | FAIL | -49.39% | 37.03% | -1.334x | 261 | 0.05% | -1.59% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr2.0,M20) | **FAIL** | 15.39% | 23.34% | 0.659x | 12 | 25.0% | 10.50% | FAIL | 9.20% | 36.92% | 0.249x | 50 | 0.42% | 0.36% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr1.5,M10) | **FAIL** | -3.08% | 23.34% | -0.132x | 26 | 34.6% | 16.70% | FAIL | -3.78% | 36.92% | -0.102x | 102 | -0.06% | -0.00% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 4h | mode_a|(n10,thr1.5,M20) | **FAIL** | 16.30% | 23.34% | 0.698x | 14 | 28.6% | 10.05% | FAIL | -2.63% | 36.92% | -0.071x | 64 | 0.44% | 0.08% | Y | Y | Y | Y | — | — |
| BTCUSDT | `schwager-vr-breakout` | 4h | mode_a|(n20,thr2.0,M10) | **FAIL** | -6.41% | 23.34% | -0.275x | 20 | 25.0% | 14.96% | FAIL | -15.29% | 36.92% | -0.414x | 69 | -0.14% | -0.34% | Y | Y | Y | Y | — | — |
| ETHUSDT | `qstick-sma-zero` | 1h | mode_a|(N8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 1h | mode_a|(N10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 1h | mode_a|(N14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 1h | mode_a|(N20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 4h | mode_a|(N8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 4h | mode_a|(N10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 4h | mode_a|(N14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qstick-sma-zero` | 4h | mode_a|(N20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 1h | mode_a|(21,34,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,9) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 1h | mode_a|(55,89,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 4h | mode_a|(21,34,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,9) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `klinger-signal-cross` | 4h | mode_a|(55,89,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 1h | mode_a|(len14,pct0.015) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.04) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 1h | mode_a|(len30,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 4h | mode_a|(len14,pct0.015) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.04) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percent-envelopes-break` | 4h | mode_a|(len30,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr2.0,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr1.5,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 1h | mode_a|(n10,thr1.5,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 1h | mode_a|(n20,thr2.0,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr2.0,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr1.5,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 4h | mode_a|(n10,thr1.5,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `schwager-vr-breakout` | 4h | mode_a|(n20,thr2.0,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 1h | mode_a|(N8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 1h | mode_a|(N10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 1h | mode_a|(N14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 1h | mode_a|(N20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 4h | mode_a|(N8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 4h | mode_a|(N10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 4h | mode_a|(N14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qstick-sma-zero` | 4h | mode_a|(N20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 1h | mode_a|(21,34,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,9) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 1h | mode_a|(55,89,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 4h | mode_a|(21,34,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,9) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `klinger-signal-cross` | 4h | mode_a|(55,89,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 1h | mode_a|(len14,pct0.015) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.04) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 1h | mode_a|(len30,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 4h | mode_a|(len14,pct0.015) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.04) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percent-envelopes-break` | 4h | mode_a|(len30,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr2.0,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr1.5,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 1h | mode_a|(n10,thr1.5,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 1h | mode_a|(n20,thr2.0,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr2.0,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr1.5,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 4h | mode_a|(n10,thr1.5,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `schwager-vr-breakout` | 4h | mode_a|(n20,thr2.0,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 1h | mode_a|(N8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 1h | mode_a|(N10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 1h | mode_a|(N14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 1h | mode_a|(N20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 4h | mode_a|(N8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 4h | mode_a|(N10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 4h | mode_a|(N14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qstick-sma-zero` | 4h | mode_a|(N20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 1h | mode_a|(21,34,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 1h | mode_a|(34,55,9) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 1h | mode_a|(55,89,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 4h | mode_a|(21,34,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 4h | mode_a|(34,55,9) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `klinger-signal-cross` | 4h | mode_a|(55,89,13) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 1h | mode_a|(len14,pct0.015) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 1h | mode_a|(len20,pct0.04) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 1h | mode_a|(len30,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 4h | mode_a|(len14,pct0.015) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 4h | mode_a|(len20,pct0.04) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percent-envelopes-break` | 4h | mode_a|(len30,pct0.025) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr2.0,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 1h | mode_a|(n14,thr1.5,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 1h | mode_a|(n10,thr1.5,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 1h | mode_a|(n20,thr2.0,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr2.0,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 4h | mode_a|(n14,thr1.5,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 4h | mode_a|(n10,thr1.5,M20) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `schwager-vr-breakout` | 4h | mode_a|(n20,thr2.0,M10) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
