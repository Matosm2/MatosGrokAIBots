# stage26-dual-sol-bnb-v1 — Scoreboard

- Generated: 2026-09-21 20:19:12 UTC
- Research ID: `stage26-dual-sol-bnb-v1` (Track 1 Path B)
- Stop-Ladder: `BTCUSDT -> ETHUSDT (HARD) -> SOLUSDT (HARD) -> BNBUSDT (HARD)`
- Gate Rule: Last 6m Mode-A Return >= 1.2x Buy & Hold, n > 5 (tiny-n kill threshold)
- Fees / Slip: 0.10% / side fee + 0.05% adverse slippage
- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)
- Strategy Encode Order (exactly 4):
  1. `katsanos-fve-zero-cross`
  2. `ehlers-convolution-zero`
  3. `hilbert-inst-trendline-cross`
  4. `elder-safezone-trail-flip`

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
| BTCUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S22) | **FAIL** | -27.59% | 27.43% | -1.006x | 188 | 22.9% | 38.28% | FAIL | -86.00% | 37.03% | -2.322x | 730 | -0.73% | -4.55% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S14) | **FAIL** | -45.02% | 27.43% | -1.641x | 248 | 20.2% | 55.24% | FAIL | -93.00% | 37.03% | -2.511x | 962 | -1.40% | -6.18% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S18) | **FAIL** | -38.46% | 27.43% | -1.402x | 224 | 19.6% | 48.83% | FAIL | -90.81% | 37.03% | -2.452x | 848 | -1.13% | -5.55% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S30) | **FAIL** | -27.67% | 27.43% | -1.009x | 150 | 21.3% | 40.69% | FAIL | -80.96% | 37.03% | -2.186x | 587 | -0.73% | -3.83% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S22) | **FAIL** | 12.76% | 23.34% | 0.547x | 46 | 28.3% | 20.89% | FAIL | -33.32% | 36.92% | -0.903x | 187 | 0.40% | -0.74% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S14) | **FAIL** | -3.89% | 23.34% | -0.167x | 60 | 26.7% | 28.85% | FAIL | -18.31% | 36.92% | -0.496x | 223 | -0.02% | -0.22% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S18) | **FAIL** | 4.40% | 23.34% | 0.189x | 51 | 27.5% | 27.65% | FAIL | -40.01% | 36.92% | -1.084x | 206 | 0.21% | -1.00% | Y | Y | Y | Y | — | — |
| BTCUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S30) | **FAIL** | 24.62% | 23.34% | 1.055x | 40 | 32.5% | 17.66% | FAIL | -29.00% | 36.92% | -0.786x | 185 | 0.64% | -0.62% | Y | Y | Y | Y | — | Near-miss 6m (1.05x B&H) |
| BTCUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L18,T0.05) | **FAIL** | -80.47% | 27.43% | -2.934x | 516 | 22.3% | 80.84% | FAIL | -99.82% | 37.03% | -2.695x | 2026 | -3.98% | -14.46% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L13,T0.05) | **FAIL** | -83.19% | 27.43% | -3.033x | 601 | 22.1% | 84.56% | FAIL | -99.91% | 37.03% | -2.698x | 2359 | -4.33% | -16.01% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L26,T0.05) | **FAIL** | -68.76% | 27.43% | -2.507x | 430 | 27.0% | 69.02% | FAIL | -99.45% | 37.03% | -2.685x | 1737 | -2.85% | -12.09% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L39,T0.05) | **FAIL** | -61.89% | 27.43% | -2.257x | 368 | 27.2% | 63.83% | FAIL | -99.07% | 37.03% | -2.675x | 1480 | -2.36% | -11.32% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L18,T0.05) | **FAIL** | -22.41% | 23.34% | -0.960x | 126 | 33.3% | 25.68% | FAIL | -73.90% | 36.92% | -2.001x | 508 | -0.61% | -3.18% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L13,T0.05) | **FAIL** | -8.67% | 23.34% | -0.371x | 146 | 39.7% | 21.62% | FAIL | -79.99% | 36.92% | -2.166x | 593 | -0.20% | -3.82% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L26,T0.05) | **FAIL** | -5.48% | 23.34% | -0.235x | 100 | 45.0% | 14.63% | FAIL | -79.11% | 36.92% | -2.143x | 425 | -0.11% | -3.72% | Y | Y | Y | Y | — | — |
| BTCUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L39,T0.05) | **FAIL** | -20.40% | 23.34% | -0.874x | 84 | 47.6% | 23.80% | FAIL | -79.48% | 36.92% | -2.153x | 361 | -0.55% | -3.77% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(close) | **FAIL** | -50.95% | 27.43% | -1.858x | 248 | 19.4% | 61.18% | FAIL | -94.14% | 37.03% | -2.542x | 971 | -1.69% | -6.61% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(hl2) | **FAIL** | -50.09% | 27.43% | -1.826x | 240 | 18.8% | 60.16% | FAIL | -93.58% | 37.03% | -2.527x | 936 | -1.64% | -6.40% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(close) | **FAIL** | -17.82% | 27.43% | -0.650x | 100 | 19.0% | 33.81% | FAIL | -65.81% | 37.03% | -1.777x | 389 | -0.44% | -2.55% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(hl2) | **FAIL** | -14.12% | 27.43% | -0.515x | 80 | 16.2% | 29.97% | FAIL | -47.88% | 37.03% | -1.293x | 342 | -0.33% | -1.51% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(close) | **FAIL** | -6.40% | 23.34% | -0.274x | 61 | 19.7% | 31.01% | FAIL | -34.90% | 36.92% | -0.945x | 236 | -0.07% | -0.79% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(hl2) | **FAIL** | -3.55% | 23.34% | -0.152x | 56 | 21.4% | 29.31% | FAIL | -29.44% | 36.92% | -0.797x | 223 | 0.00% | -0.58% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(close) | **FAIL** | -6.34% | 23.34% | -0.272x | 20 | 20.0% | 14.79% | FAIL | -23.71% | 36.92% | -0.642x | 93 | -0.15% | -0.62% | Y | Y | Y | Y | — | — |
| BTCUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(hl2) | **FAIL** | -4.75% | 23.34% | -0.204x | 15 | 20.0% | 11.56% | FAIL | -24.63% | 36.92% | -0.667x | 75 | -0.11% | -0.66% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N10,k2.5) | **FAIL** | -17.10% | 27.43% | -0.624x | 156 | 28.8% | 34.79% | FAIL | -79.85% | 37.03% | -2.156x | 669 | -0.40% | -3.70% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema14,N10,k2.5) | **FAIL** | -26.94% | 27.43% | -0.982x | 164 | 26.2% | 41.77% | FAIL | -80.92% | 37.03% | -2.185x | 687 | -0.71% | -3.81% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N8,k2.0) | **FAIL** | -28.87% | 27.43% | -1.053x | 183 | 25.1% | 41.42% | FAIL | -89.21% | 37.03% | -2.409x | 804 | -0.80% | -5.23% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema30,N15,k3.0) | **FAIL** | -22.92% | 27.43% | -0.836x | 130 | 27.7% | 36.37% | FAIL | -74.67% | 37.03% | -2.016x | 529 | -0.58% | -3.15% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N10,k2.5) | **FAIL** | -4.43% | 23.34% | -0.190x | 45 | 28.9% | 24.96% | FAIL | -11.08% | 36.92% | -0.300x | 162 | -0.04% | -0.03% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema14,N10,k2.5) | **FAIL** | -4.42% | 23.34% | -0.189x | 48 | 27.1% | 25.94% | FAIL | -16.80% | 36.92% | -0.455x | 170 | -0.03% | -0.18% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N8,k2.0) | **FAIL** | -4.24% | 23.34% | -0.182x | 54 | 29.6% | 24.23% | FAIL | -22.60% | 36.92% | -0.612x | 197 | -0.03% | -0.42% | Y | Y | Y | Y | — | — |
| BTCUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema30,N15,k3.0) | **FAIL** | 5.20% | 23.34% | 0.223x | 35 | 31.4% | 25.10% | FAIL | 0.22% | 36.92% | 0.006x | 127 | 0.21% | 0.35% | Y | Y | Y | Y | — | — |
| ETHUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S22) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S18) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S30) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S22) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S18) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S30) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L18,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L13,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L26,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L39,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L18,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L13,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L26,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L39,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema14,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N8,k2.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema30,N15,k3.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema14,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N8,k2.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema30,N15,k3.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S22) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S18) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S30) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S22) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S18) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S30) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L18,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L13,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L26,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L39,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L18,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L13,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L26,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L39,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema14,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N8,k2.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema30,N15,k3.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema14,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N8,k2.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema30,N15,k3.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S22) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S18) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 1h | mode_a|(S30) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S22) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S14) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S18) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-fve-zero-cross` | 4h | mode_a|(S30) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L18,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L13,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L26,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 1h | mode_a|(L39,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L18,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L13,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L26,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-convolution-zero` | 4h | mode_a|(L39,T0.05) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 1h | mode_a|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 1h | mode_b|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 4h | mode_a|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `hilbert-inst-trendline-cross` | 4h | mode_b|(hl2) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema14,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema22,N8,k2.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 1h | mode_a|(ema30,N15,k3.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema14,N10,k2.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema22,N8,k2.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-safezone-trail-flip` | 4h | mode_a|(ema30,N15,k3.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
