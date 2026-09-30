# stage31-dual-sol-bnb-v1 — Scoreboard (Independent Per-Coin Gate)

- Generated: 2026-09-21 22:41:54 UTC
- Research ID: `stage31-dual-sol-bnb-v1` (Track 1 Path B)
- NEW PER-COIN GATE (Nuno 2026-09-22 + Mid-Encode Patch):
  - Mode-A 6m Return >= 1.2x Buy & Hold on that coin AND denser sample n >= 40.
  - Thin n < 40 -> Ineligible for paper even if x >= 1.2 (flagged THIN).
  - BTC, ETH, SOL, BNB scored independently — no seat killed solely for failing another coin.
- Fees / Slip: 0.10% / side fee + 0.05% adverse slippage
- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)
- Strategy Encode Order (exactly 4):
  1. `apirine-sdo-zero-cross`
  2. `ehlers-madh-zero-cross`
  3. `premier-stochastic-osc-zero`
  4. `apirine-tradj-ema-cross`
- Track B Hard Ban: Honored (no CK / QQE / MAMA / Wilder-VS)

## Executive Summary
- Total Scored Cells: 168 / 168
- Coin PASS (Paper-Eligible, x >= 1.2 & n >= 40): 0
- Thin Leaders (x >= 1.2 but n < 40, Ineligible): 2

## Per-Coin PASS List (Paper-Eligible)
- *None. Zero candidates met the per-coin gate (x >= 1.2x B&H AND n >= 40).*

## THIN Leaders (x >= 1.2x B&H but n < 40 — Ineligible for Paper)
| Coin | Strategy ID | TF | Mode/Params | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | `apirine-sdo-zero-cross` | 4h | mode_a|(n40,lb200,pds6) | 30.89% | 23.37% | 1.322x | 15 | 33.3% | THIN-N (Mode-A 6m n=15 < 40; ineligible for paper even though x=1.32 >= 1.2) |
| SOLUSDT | `apirine-sdo-zero-cross` | 4h | mode_a|(n40,lb200,pds6) | 43.24% | 34.37% | 1.258x | 15 | 46.7% | THIN-N (Mode-A 6m n=15 < 40; ineligible for paper even though x=1.26 >= 1.2) |

## Full Per-Coin Scoreboard

| Strategy ID | Coin | TF | Mode/Params | n | WR% | Mode-A Ret% | B&H% | xB&H | PASS_coin | THIN | MaxDD% | Full Ret% | Full B&H% | Full xB&H | Full n | Ops 6m% | Ops Full% | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `apirine-sdo-zero-cross` | BTCUSDT | 1h | mode_a|(n14,lb100,pds3) | 173 | 24.9% | -32.47% | 26.41% | -1.229x | **N** | — | 46.68% | -81.53% | 37.12% | -2.196x | 663 | -0.91% | -3.89% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 1h | mode_a|(n8,lb50,pds3) | 237 | 24.1% | -47.78% | 26.41% | -1.809x | **N** | — | 55.37% | -91.16% | 37.12% | -2.456x | 929 | -1.53% | -5.65% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 1h | mode_a|(n14,lb50,pds3) | 171 | 25.1% | -31.81% | 26.41% | -1.205x | **N** | — | 46.05% | -81.42% | 37.12% | -2.193x | 654 | -0.88% | -3.88% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 1h | mode_a|(n20,lb100,pds5) | 107 | 29.0% | -2.17% | 26.41% | -0.082x | **N** | — | 25.26% | -65.26% | 37.12% | -1.758x | 429 | 0.02% | -2.35% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 1h | mode_a|(n40,lb200,pds6) | 63 | 30.2% | 7.34% | 26.41% | 0.278x | **N** | — | 13.80% | -32.64% | 37.12% | -0.879x | 262 | 0.25% | -0.72% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 1h | mode_b|(n14,lb100,pds3,rising) | 173 | 24.9% | -32.47% | 26.41% | -1.229x | **N** | — | 46.68% | -81.53% | 37.12% | -2.196x | 663 | -0.91% | -3.89% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 4h | mode_a|(n14,lb100,pds3) | 34 | 26.5% | 4.47% | 23.37% | 0.191x | **N** | — | 21.15% | -7.59% | 36.95% | -0.205x | 153 | 0.20% | 0.07% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 4h | mode_a|(n8,lb50,pds3) | 56 | 33.9% | 3.47% | 23.37% | 0.149x | **N** | — | 18.59% | -33.88% | 36.95% | -0.917x | 217 | 0.15% | -0.78% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 4h | mode_a|(n14,lb50,pds3) | 34 | 29.4% | 4.83% | 23.37% | 0.207x | **N** | — | 21.00% | -4.83% | 36.95% | -0.131x | 151 | 0.20% | 0.14% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 4h | mode_a|(n20,lb100,pds5) | 29 | 34.5% | -1.28% | 23.37% | -0.055x | **N** | — | 22.65% | -19.68% | 36.95% | -0.533x | 112 | 0.04% | -0.33% | — |
| `apirine-sdo-zero-cross` | BTCUSDT | 4h | mode_a|(n40,lb200,pds6) | 15 | 33.3% | 30.89% | 23.37% | 1.322x | **N** | THIN | 13.94% | 20.87% | 36.95% | 0.565x | 67 | 0.77% | 0.72% | THIN-N (Mode-A 6m n=15 < 40; ineligible for paper even though x=1.32 >= 1.2) |
| `apirine-sdo-zero-cross` | BTCUSDT | 4h | mode_b|(n14,lb100,pds3,rising) | 34 | 26.5% | 4.47% | 23.37% | 0.191x | **N** | — | 21.15% | -7.59% | 36.95% | -0.205x | 153 | 0.20% | 0.07% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 1h | mode_a|(s8,dom27) | 151 | 31.8% | -22.89% | 26.41% | -0.867x | **N** | — | 38.70% | -81.34% | 37.12% | -2.191x | 611 | -0.58% | -3.87% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 1h | mode_a|(s6,dom20) | 199 | 27.1% | -33.82% | 26.41% | -1.281x | **N** | — | 44.00% | -87.14% | 37.12% | -2.347x | 793 | -0.95% | -4.77% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 1h | mode_a|(s8,dom20) | 170 | 30.0% | -16.35% | 26.41% | -0.619x | **N** | — | 32.70% | -83.89% | 37.12% | -2.260x | 695 | -0.37% | -4.22% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 1h | mode_a|(s10,dom34) | 124 | 34.7% | -11.76% | 26.41% | -0.445x | **N** | — | 34.50% | -73.00% | 37.12% | -1.967x | 496 | -0.25% | -2.96% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 1h | mode_b|(s8,dom27,rising) | 151 | 31.8% | -22.89% | 26.41% | -0.867x | **N** | — | 38.70% | -81.34% | 37.12% | -2.191x | 611 | -0.58% | -3.87% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 4h | mode_a|(s8,dom27) | 35 | 34.3% | 11.86% | 23.37% | 0.507x | **N** | — | 17.56% | 25.81% | 36.95% | 0.699x | 143 | 0.37% | 0.85% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 4h | mode_a|(s6,dom20) | 48 | 39.6% | 14.19% | 23.37% | 0.607x | **N** | — | 11.38% | -10.93% | 36.95% | -0.296x | 192 | 0.40% | -0.02% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 4h | mode_a|(s8,dom20) | 43 | 44.2% | 7.65% | 23.37% | 0.328x | **N** | — | 15.38% | 31.57% | 36.95% | 0.854x | 169 | 0.26% | 0.94% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 4h | mode_a|(s10,dom34) | 29 | 34.5% | -5.23% | 23.37% | -0.224x | **N** | — | 28.52% | -15.33% | 36.95% | -0.415x | 114 | -0.04% | -0.18% | — |
| `ehlers-madh-zero-cross` | BTCUSDT | 4h | mode_b|(s8,dom27,rising) | 35 | 34.3% | 11.86% | 23.37% | 0.507x | **N** | — | 17.56% | 25.81% | 36.95% | 0.699x | 143 | 0.37% | 0.85% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 1h | mode_a|(per8,sm5) | 169 | 29.0% | -30.43% | 26.41% | -1.152x | **N** | — | 42.93% | -83.78% | 37.12% | -2.257x | 679 | -0.83% | -4.19% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 1h | mode_a|(per5,sm3) | 300 | 22.3% | -58.76% | 26.41% | -2.225x | **N** | — | 63.50% | -95.63% | 37.12% | -2.576x | 1166 | -2.11% | -7.29% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 1h | mode_a|(per8,sm3) | 219 | 26.5% | -41.36% | 26.41% | -1.566x | **N** | — | 51.91% | -91.11% | 37.12% | -2.454x | 889 | -1.25% | -5.61% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 1h | mode_a|(per14,sm8) | 96 | 32.3% | -4.18% | 26.41% | -0.158x | **N** | — | 26.26% | -57.60% | 37.12% | -1.552x | 397 | -0.05% | -1.86% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 1h | mode_b|(per8,sm5,dip-0.2) | 150 | 30.0% | -24.27% | 26.41% | -0.919x | **N** | — | 40.73% | -78.14% | 37.12% | -2.105x | 607 | -0.62% | -3.48% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 4h | mode_a|(per8,sm5) | 42 | 35.7% | 12.60% | 23.37% | 0.539x | **N** | — | 15.30% | -8.06% | 36.95% | -0.218x | 166 | 0.37% | 0.06% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 4h | mode_a|(per5,sm3) | 67 | 29.9% | -8.37% | 23.37% | -0.358x | **N** | — | 29.90% | -44.15% | 36.95% | -1.195x | 270 | -0.17% | -1.21% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 4h | mode_a|(per8,sm3) | 57 | 38.6% | 9.54% | 23.37% | 0.408x | **N** | — | 13.35% | -16.29% | 36.95% | -0.441x | 214 | 0.27% | -0.22% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 4h | mode_a|(per14,sm8) | 28 | 35.7% | -1.21% | 23.37% | -0.052x | **N** | — | 24.58% | -5.50% | 36.95% | -0.149x | 103 | 0.06% | 0.21% | — |
| `premier-stochastic-osc-zero` | BTCUSDT | 4h | mode_b|(per8,sm5,dip-0.2) | 37 | 35.1% | 11.38% | 23.37% | 0.487x | **N** | — | 12.74% | -21.17% | 36.95% | -0.573x | 149 | 0.34% | -0.41% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 1h | mode_a|(p20,pds20,m5) | 111 | 24.3% | -16.38% | 26.41% | -0.620x | **N** | — | 35.73% | -67.68% | 37.12% | -1.823x | 454 | -0.37% | -2.56% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 1h | mode_a|(p10,pds10,m5) | 243 | 21.4% | -41.97% | 26.41% | -1.589x | **N** | — | 53.41% | -94.00% | 37.12% | -2.532x | 994 | -1.27% | -6.56% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 1h | mode_a|(p20,pds10,m8) | 150 | 24.0% | -25.32% | 26.41% | -0.959x | **N** | — | 41.88% | -80.27% | 37.12% | -2.162x | 614 | -0.66% | -3.75% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 1h | mode_a|(p40,pds40,m10) | 69 | 26.1% | -0.11% | 26.41% | -0.004x | **N** | — | 23.79% | -46.89% | 37.12% | -1.263x | 262 | 0.09% | -1.28% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 1h | mode_b|(p20,pds20,m5,close_gate) | 111 | 24.3% | -16.38% | 26.41% | -0.620x | **N** | — | 35.73% | -67.68% | 37.12% | -1.823x | 454 | -0.37% | -2.56% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 4h | mode_a|(p20,pds20,m5) | 30 | 33.3% | 7.83% | 23.37% | 0.335x | **N** | — | 18.88% | -11.62% | 36.95% | -0.314x | 112 | 0.27% | -0.00% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 4h | mode_a|(p10,pds10,m5) | 68 | 20.6% | -8.22% | 23.37% | -0.352x | **N** | — | 30.29% | -47.77% | 36.95% | -1.293x | 245 | -0.13% | -1.34% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 4h | mode_a|(p20,pds10,m8) | 42 | 26.2% | 4.90% | 23.37% | 0.210x | **N** | — | 22.53% | -29.66% | 36.95% | -0.803x | 158 | 0.21% | -0.54% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 4h | mode_a|(p40,pds40,m10) | 18 | 27.8% | 12.57% | 23.37% | 0.538x | **N** | — | 14.63% | -15.90% | 36.95% | -0.430x | 71 | 0.37% | -0.19% | — |
| `apirine-tradj-ema-cross` | BTCUSDT | 4h | mode_b|(p20,pds20,m5,close_gate) | 30 | 33.3% | 7.83% | 23.37% | 0.335x | **N** | — | 18.88% | -11.62% | 36.95% | -0.314x | 112 | 0.27% | -0.00% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 1h | mode_a|(n14,lb100,pds3) | 168 | 23.2% | -16.84% | 35.66% | -0.472x | **N** | — | 41.68% | -75.42% | 8.68% | -8.688x | 665 | -0.32% | -2.79% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 1h | mode_a|(n8,lb50,pds3) | 244 | 21.7% | -48.70% | 35.66% | -1.366x | **N** | — | 59.48% | -84.47% | 8.68% | -9.731x | 902 | -1.52% | -3.98% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 1h | mode_a|(n14,lb50,pds3) | 167 | 24.0% | -15.64% | 35.66% | -0.439x | **N** | — | 40.69% | -75.28% | 8.68% | -8.673x | 663 | -0.28% | -2.77% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 1h | mode_a|(n20,lb100,pds5) | 105 | 30.5% | 9.50% | 35.66% | 0.266x | **N** | — | 27.24% | -56.19% | 8.68% | -6.474x | 434 | 0.35% | -1.39% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 1h | mode_a|(n40,lb200,pds6) | 74 | 21.6% | -9.61% | 35.66% | -0.270x | **N** | — | 24.84% | -35.89% | 8.68% | -4.135x | 280 | -0.14% | -0.55% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 1h | mode_b|(n14,lb100,pds3,rising) | 168 | 23.2% | -16.84% | 35.66% | -0.472x | **N** | — | 41.68% | -75.42% | 8.68% | -8.688x | 665 | -0.32% | -2.79% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 4h | mode_a|(n14,lb100,pds3) | 44 | 20.5% | -11.31% | 30.15% | -0.375x | **N** | — | 31.32% | -9.93% | 8.53% | -1.163x | 174 | -0.16% | 0.44% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 4h | mode_a|(n8,lb50,pds3) | 59 | 23.7% | -14.85% | 30.15% | -0.492x | **N** | — | 27.62% | -46.89% | 8.53% | -5.495x | 224 | -0.29% | -1.00% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 4h | mode_a|(n14,lb50,pds3) | 44 | 20.5% | -10.53% | 30.15% | -0.349x | **N** | — | 31.32% | -17.56% | 8.53% | -2.057x | 173 | -0.14% | 0.23% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 4h | mode_a|(n20,lb100,pds5) | 30 | 30.0% | -1.25% | 30.15% | -0.042x | **N** | — | 28.56% | -30.14% | 8.53% | -3.532x | 109 | 0.09% | -0.27% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 4h | mode_a|(n40,lb200,pds6) | 13 | 46.2% | 35.59% | 30.15% | 1.180x | **N** | — | 13.80% | -10.62% | 8.53% | -1.244x | 65 | 0.88% | 0.33% | — |
| `apirine-sdo-zero-cross` | ETHUSDT | 4h | mode_b|(n14,lb100,pds3,rising) | 44 | 20.5% | -11.31% | 30.15% | -0.375x | **N** | — | 31.32% | -9.93% | 8.53% | -1.163x | 174 | -0.16% | 0.44% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 1h | mode_a|(s8,dom27) | 160 | 26.9% | -21.07% | 35.66% | -0.591x | **N** | — | 36.83% | -68.18% | 8.68% | -7.855x | 617 | -0.46% | -2.16% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 1h | mode_a|(s6,dom20) | 208 | 22.1% | -38.01% | 35.66% | -1.066x | **N** | — | 49.23% | -77.44% | 8.68% | -8.921x | 787 | -1.05% | -3.08% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 1h | mode_a|(s8,dom20) | 178 | 30.3% | -21.87% | 35.66% | -0.613x | **N** | — | 40.49% | -67.69% | 8.68% | -7.798x | 697 | -0.48% | -2.14% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 1h | mode_a|(s10,dom34) | 125 | 26.4% | -16.17% | 35.66% | -0.453x | **N** | — | 37.68% | -62.93% | 8.68% | -7.250x | 496 | -0.32% | -1.73% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 1h | mode_b|(s8,dom27,rising) | 160 | 26.9% | -21.07% | 35.66% | -0.591x | **N** | — | 36.83% | -68.18% | 8.68% | -7.855x | 617 | -0.46% | -2.16% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 4h | mode_a|(s8,dom27) | 43 | 34.9% | -1.04% | 30.15% | -0.035x | **N** | — | 24.72% | 18.51% | 8.53% | 2.169x | 146 | 0.11% | 1.03% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 4h | mode_a|(s6,dom20) | 49 | 26.5% | -11.52% | 30.15% | -0.382x | **N** | — | 31.50% | -37.48% | 8.53% | -4.392x | 193 | -0.20% | -0.63% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 4h | mode_a|(s8,dom20) | 47 | 23.4% | -13.80% | 30.15% | -0.458x | **N** | — | 31.90% | 4.34% | 8.53% | 0.509x | 168 | -0.25% | 0.64% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 4h | mode_a|(s10,dom34) | 33 | 30.3% | -2.78% | 30.15% | -0.092x | **N** | — | 28.93% | 22.78% | 8.53% | 2.669x | 120 | 0.07% | 1.32% | — |
| `ehlers-madh-zero-cross` | ETHUSDT | 4h | mode_b|(s8,dom27,rising) | 43 | 34.9% | -1.04% | 30.15% | -0.035x | **N** | — | 24.72% | 18.51% | 8.53% | 2.169x | 146 | 0.11% | 1.03% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 1h | mode_a|(per8,sm5) | 175 | 26.3% | -33.50% | 35.66% | -0.939x | **N** | — | 47.30% | -76.49% | 8.68% | -8.812x | 683 | -0.89% | -2.95% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 1h | mode_a|(per5,sm3) | 307 | 23.5% | -58.88% | 35.66% | -1.651x | **N** | — | 65.79% | -95.04% | 8.68% | -10.949x | 1166 | -2.10% | -6.67% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 1h | mode_a|(per8,sm3) | 224 | 25.9% | -42.83% | 35.66% | -1.201x | **N** | — | 55.11% | -89.45% | 8.68% | -10.305x | 899 | -1.26% | -4.87% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 1h | mode_a|(per14,sm8) | 98 | 32.7% | 14.53% | 35.66% | 0.408x | **N** | — | 26.55% | -38.22% | 8.68% | -4.403x | 417 | 0.48% | -0.47% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 1h | mode_b|(per8,sm5,dip-0.2) | 148 | 25.7% | -27.90% | 35.66% | -0.782x | **N** | — | 44.43% | -74.01% | 8.68% | -8.526x | 605 | -0.70% | -2.74% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 4h | mode_a|(per8,sm5) | 45 | 26.7% | 1.61% | 30.15% | 0.053x | **N** | — | 24.13% | -41.72% | 8.53% | -4.889x | 179 | 0.16% | -0.72% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 4h | mode_a|(per5,sm3) | 73 | 32.9% | 5.52% | 30.15% | 0.183x | **N** | — | 34.61% | -18.15% | 8.53% | -2.127x | 297 | 0.28% | 0.22% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 4h | mode_a|(per8,sm3) | 57 | 31.6% | 6.29% | 30.15% | 0.209x | **N** | — | 28.47% | -36.16% | 8.53% | -4.237x | 233 | 0.28% | -0.38% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 4h | mode_a|(per14,sm8) | 25 | 36.0% | 11.20% | 30.15% | 0.372x | **N** | — | 27.31% | -5.29% | 8.53% | -0.620x | 103 | 0.40% | 0.60% | — |
| `premier-stochastic-osc-zero` | ETHUSDT | 4h | mode_b|(per8,sm5,dip-0.2) | 40 | 27.5% | 4.18% | 30.15% | 0.139x | **N** | — | 22.59% | -33.82% | 8.53% | -3.963x | 152 | 0.21% | -0.46% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 1h | mode_a|(p20,pds20,m5) | 121 | 21.5% | -23.91% | 35.66% | -0.671x | **N** | — | 45.21% | -74.41% | 8.68% | -8.572x | 459 | -0.55% | -2.73% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 1h | mode_a|(p10,pds10,m5) | 242 | 19.8% | -32.17% | 35.66% | -0.902x | **N** | — | 46.47% | -87.81% | 8.68% | -10.116x | 971 | -0.82% | -4.56% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 1h | mode_a|(p20,pds10,m8) | 164 | 18.3% | -27.98% | 35.66% | -0.785x | **N** | — | 45.29% | -69.88% | 8.68% | -8.050x | 604 | -0.68% | -2.30% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 1h | mode_a|(p40,pds40,m10) | 71 | 22.5% | -11.15% | 35.66% | -0.313x | **N** | — | 33.58% | -41.26% | 8.68% | -4.753x | 271 | -0.18% | -0.74% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 1h | mode_b|(p20,pds20,m5,close_gate) | 121 | 21.5% | -23.91% | 35.66% | -0.671x | **N** | — | 45.21% | -74.41% | 8.68% | -8.572x | 459 | -0.55% | -2.73% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 4h | mode_a|(p20,pds20,m5) | 32 | 25.0% | 1.34% | 30.15% | 0.045x | **N** | — | 23.52% | -42.64% | 8.53% | -4.997x | 120 | 0.16% | -0.71% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 4h | mode_a|(p10,pds10,m5) | 63 | 25.4% | -7.43% | 30.15% | -0.246x | **N** | — | 27.89% | -45.87% | 8.53% | -5.375x | 246 | -0.08% | -0.97% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 4h | mode_a|(p20,pds10,m8) | 42 | 21.4% | -5.19% | 30.15% | -0.172x | **N** | — | 28.19% | -53.83% | 8.53% | -6.307x | 165 | -0.01% | -1.33% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 4h | mode_a|(p40,pds40,m10) | 19 | 21.1% | 10.24% | 30.15% | 0.340x | **N** | — | 22.16% | -16.85% | 8.53% | -1.974x | 74 | 0.38% | 0.21% | — |
| `apirine-tradj-ema-cross` | ETHUSDT | 4h | mode_b|(p20,pds20,m5,close_gate) | 32 | 25.0% | 1.34% | 30.15% | 0.045x | **N** | — | 23.52% | -42.64% | 8.53% | -4.997x | 120 | 0.16% | -0.71% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 1h | mode_a|(n14,lb100,pds3) | 160 | 26.9% | -13.75% | 38.78% | -0.355x | **N** | — | 42.62% | -83.75% | -18.97% | -3.414x | 625 | -0.21% | -3.77% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 1h | mode_a|(n8,lb50,pds3) | 220 | 25.9% | -33.66% | 38.78% | -0.868x | **N** | — | 53.29% | -88.75% | -18.97% | -3.678x | 873 | -0.89% | -4.64% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 1h | mode_a|(n14,lb50,pds3) | 158 | 27.2% | -12.57% | 38.78% | -0.324x | **N** | — | 41.71% | -83.20% | -18.97% | -3.385x | 620 | -0.18% | -3.69% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 1h | mode_a|(n20,lb100,pds5) | 103 | 35.0% | 5.60% | 38.78% | 0.145x | **N** | — | 33.46% | -68.64% | -18.97% | -2.618x | 408 | 0.27% | -2.18% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 1h | mode_a|(n40,lb200,pds6) | 68 | 25.0% | 2.07% | 38.78% | 0.053x | **N** | — | 27.02% | -50.62% | -18.97% | -1.668x | 259 | 0.17% | -1.18% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 1h | mode_b|(n14,lb100,pds3,rising) | 160 | 26.9% | -13.75% | 38.78% | -0.355x | **N** | — | 42.62% | -83.75% | -18.97% | -3.414x | 625 | -0.21% | -3.77% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 4h | mode_a|(n14,lb100,pds3) | 41 | 24.4% | 8.05% | 34.37% | 0.234x | **N** | — | 25.08% | -13.58% | -19.20% | 0.293x | 158 | 0.41% | 0.26% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 4h | mode_a|(n8,lb50,pds3) | 49 | 34.7% | 19.34% | 34.37% | 0.563x | **N** | — | 28.82% | -39.72% | -19.20% | -1.068x | 215 | 0.58% | -0.60% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 4h | mode_a|(n14,lb50,pds3) | 42 | 23.8% | 5.01% | 34.37% | 0.146x | **N** | — | 27.18% | -20.44% | -19.20% | -0.065x | 158 | 0.34% | 0.05% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 4h | mode_a|(n20,lb100,pds5) | 30 | 23.3% | 2.59% | 34.37% | 0.075x | **N** | — | 34.17% | -31.63% | -19.20% | -0.647x | 112 | 0.26% | -0.32% | — |
| `apirine-sdo-zero-cross` | SOLUSDT | 4h | mode_a|(n40,lb200,pds6) | 15 | 46.7% | 43.24% | 34.37% | 1.258x | **N** | THIN | 12.77% | 44.67% | -19.20% | 3.326x | 64 | 1.07% | 1.55% | THIN-N (Mode-A 6m n=15 < 40; ineligible for paper even though x=1.26 >= 1.2) |
| `apirine-sdo-zero-cross` | SOLUSDT | 4h | mode_b|(n14,lb100,pds3,rising) | 41 | 24.4% | 8.05% | 34.37% | 0.234x | **N** | — | 25.08% | -13.58% | -19.20% | 0.293x | 158 | 0.41% | 0.26% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 1h | mode_a|(s8,dom27) | 149 | 30.9% | -11.56% | 38.78% | -0.298x | **N** | — | 42.13% | -78.13% | -18.97% | -3.118x | 593 | -0.16% | -3.02% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 1h | mode_a|(s6,dom20) | 197 | 29.9% | -27.59% | 38.78% | -0.711x | **N** | — | 49.42% | -85.41% | -18.97% | -3.502x | 773 | -0.65% | -3.96% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 1h | mode_a|(s8,dom20) | 167 | 29.3% | -11.71% | 38.78% | -0.302x | **N** | — | 39.27% | -82.85% | -18.97% | -3.367x | 676 | -0.17% | -3.65% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 1h | mode_a|(s10,dom34) | 117 | 32.5% | 13.92% | 38.78% | 0.359x | **N** | — | 33.89% | -35.45% | -18.97% | -0.868x | 467 | 0.49% | -0.25% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 1h | mode_b|(s8,dom27,rising) | 149 | 30.9% | -11.56% | 38.78% | -0.298x | **N** | — | 42.13% | -78.13% | -18.97% | -3.118x | 593 | -0.16% | -3.02% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 4h | mode_a|(s8,dom27) | 40 | 35.0% | -4.31% | 34.37% | -0.125x | **N** | — | 23.50% | -37.98% | -19.20% | -0.978x | 155 | 0.02% | -0.65% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 4h | mode_a|(s6,dom20) | 46 | 39.1% | 9.96% | 34.37% | 0.290x | **N** | — | 29.81% | -50.39% | -19.20% | -1.624x | 193 | 0.38% | -1.10% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 4h | mode_a|(s8,dom20) | 44 | 36.4% | 2.56% | 34.37% | 0.074x | **N** | — | 25.59% | -15.01% | -19.20% | 0.219x | 173 | 0.20% | 0.16% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 4h | mode_a|(s10,dom34) | 30 | 26.7% | 10.54% | 34.37% | 0.307x | **N** | — | 24.63% | -46.37% | -19.20% | -1.415x | 121 | 0.50% | -0.88% | — |
| `ehlers-madh-zero-cross` | SOLUSDT | 4h | mode_b|(s8,dom27,rising) | 40 | 35.0% | -4.31% | 34.37% | -0.125x | **N** | — | 23.50% | -37.98% | -19.20% | -0.978x | 155 | 0.02% | -0.65% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 1h | mode_a|(per8,sm5) | 166 | 28.3% | -18.08% | 38.78% | -0.466x | **N** | — | 45.04% | -80.12% | -18.97% | -3.223x | 657 | -0.34% | -3.22% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 1h | mode_a|(per5,sm3) | 297 | 26.3% | -51.78% | 38.78% | -1.335x | **N** | — | 61.76% | -97.07% | -18.97% | -4.116x | 1144 | -1.69% | -7.78% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 1h | mode_a|(per8,sm3) | 225 | 25.8% | -37.25% | 38.78% | -0.960x | **N** | — | 52.52% | -89.47% | -18.97% | -3.716x | 862 | -1.03% | -4.77% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 1h | mode_a|(per14,sm8) | 91 | 34.1% | 28.69% | 38.78% | 0.740x | **N** | — | 31.85% | -51.99% | -18.97% | -1.740x | 380 | 0.79% | -0.97% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 1h | mode_b|(per8,sm5,dip-0.2) | 145 | 30.3% | -12.34% | 38.78% | -0.318x | **N** | — | 39.39% | -81.34% | -18.97% | -3.287x | 593 | -0.19% | -3.46% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 4h | mode_a|(per8,sm5) | 42 | 40.5% | 21.75% | 34.37% | 0.633x | **N** | — | 27.54% | -63.11% | -19.20% | -2.287x | 175 | 0.61% | -1.80% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 4h | mode_a|(per5,sm3) | 68 | 33.8% | 20.92% | 34.37% | 0.609x | **N** | — | 31.88% | -30.92% | -19.20% | -0.610x | 282 | 0.61% | -0.19% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 4h | mode_a|(per8,sm3) | 53 | 34.0% | 6.07% | 34.37% | 0.177x | **N** | — | 33.92% | -55.84% | -19.20% | -1.908x | 216 | 0.27% | -1.38% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 4h | mode_a|(per14,sm8) | 26 | 23.1% | 8.62% | 34.37% | 0.251x | **N** | — | 29.98% | -46.59% | -19.20% | -1.426x | 106 | 0.45% | -0.96% | — |
| `premier-stochastic-osc-zero` | SOLUSDT | 4h | mode_b|(per8,sm5,dip-0.2) | 40 | 42.5% | 29.89% | 34.37% | 0.870x | **N** | — | 22.70% | -52.21% | -19.20% | -1.719x | 159 | 0.77% | -1.25% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 1h | mode_a|(p20,pds20,m5) | 113 | 27.4% | 5.55% | 38.78% | 0.143x | **N** | — | 29.61% | -69.76% | -18.97% | -2.677x | 458 | 0.28% | -2.30% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 1h | mode_a|(p10,pds10,m5) | 237 | 24.1% | -23.18% | 38.78% | -0.598x | **N** | — | 48.04% | -94.02% | -18.97% | -3.955x | 982 | -0.49% | -6.21% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 1h | mode_a|(p20,pds10,m8) | 148 | 23.6% | 3.03% | 38.78% | 0.078x | **N** | — | 29.56% | -76.41% | -18.97% | -3.027x | 622 | 0.21% | -2.94% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 1h | mode_a|(p40,pds40,m10) | 65 | 27.7% | 10.89% | 38.78% | 0.281x | **N** | — | 27.57% | -48.47% | -18.97% | -1.555x | 262 | 0.39% | -1.02% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 1h | mode_b|(p20,pds20,m5,close_gate) | 113 | 27.4% | 5.55% | 38.78% | 0.143x | **N** | — | 29.61% | -69.76% | -18.97% | -2.677x | 458 | 0.28% | -2.30% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 4h | mode_a|(p20,pds20,m5) | 29 | 31.0% | 23.45% | 34.37% | 0.682x | **N** | — | 20.16% | -2.97% | -19.20% | 0.845x | 108 | 0.70% | 0.48% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 4h | mode_a|(p10,pds10,m5) | 66 | 27.3% | -0.06% | 34.37% | -0.002x | **N** | — | 31.49% | -49.03% | -19.20% | -1.554x | 241 | 0.13% | -1.05% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 4h | mode_a|(p20,pds10,m8) | 42 | 26.2% | 23.28% | 34.37% | 0.677x | **N** | — | 21.04% | -15.69% | -19.20% | 0.183x | 148 | 0.73% | 0.21% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 4h | mode_a|(p40,pds40,m10) | 18 | 27.8% | 18.51% | 34.37% | 0.539x | **N** | — | 20.87% | -4.03% | -19.20% | 0.790x | 68 | 0.57% | 0.49% | — |
| `apirine-tradj-ema-cross` | SOLUSDT | 4h | mode_b|(p20,pds20,m5,close_gate) | 29 | 31.0% | 23.45% | 34.37% | 0.682x | **N** | — | 20.16% | -2.97% | -19.20% | 0.845x | 108 | 0.70% | 0.48% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 1h | mode_a|(n14,lb100,pds3) | 164 | 23.2% | -21.91% | 28.29% | -0.775x | **N** | — | 36.60% | -81.32% | 38.03% | -2.138x | 629 | -0.54% | -3.82% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 1h | mode_a|(n8,lb50,pds3) | 224 | 28.1% | -38.35% | 28.29% | -1.356x | **N** | — | 46.81% | -89.34% | 38.03% | -2.349x | 888 | -1.15% | -5.15% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 1h | mode_a|(n14,lb50,pds3) | 164 | 23.2% | -20.45% | 28.29% | -0.723x | **N** | — | 36.05% | -81.31% | 38.03% | -2.138x | 625 | -0.50% | -3.82% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 1h | mode_a|(n20,lb100,pds5) | 102 | 35.3% | 13.12% | 28.29% | 0.464x | **N** | — | 17.91% | -42.85% | 38.03% | -1.127x | 409 | 0.37% | -1.14% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 1h | mode_a|(n40,lb200,pds6) | 59 | 32.2% | 3.69% | 28.29% | 0.130x | **N** | — | 13.54% | -48.61% | 38.03% | -1.278x | 269 | 0.15% | -1.44% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 1h | mode_b|(n14,lb100,pds3,rising) | 164 | 23.2% | -21.91% | 28.29% | -0.775x | **N** | — | 36.60% | -81.32% | 38.03% | -2.138x | 629 | -0.54% | -3.82% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 4h | mode_a|(n14,lb100,pds3) | 41 | 31.7% | 7.63% | 25.48% | 0.299x | **N** | — | 15.29% | -30.01% | 37.23% | -0.806x | 170 | 0.24% | -0.62% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 4h | mode_a|(n8,lb50,pds3) | 55 | 36.4% | 9.20% | 25.48% | 0.361x | **N** | — | 14.01% | -23.17% | 37.23% | -0.622x | 219 | 0.27% | -0.42% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 4h | mode_a|(n14,lb50,pds3) | 41 | 31.7% | 6.27% | 25.48% | 0.246x | **N** | — | 16.36% | -30.53% | 37.23% | -0.820x | 168 | 0.20% | -0.64% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 4h | mode_a|(n20,lb100,pds5) | 25 | 36.0% | 8.83% | 25.48% | 0.347x | **N** | — | 22.39% | -6.05% | 37.23% | -0.163x | 101 | 0.26% | 0.11% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 4h | mode_a|(n40,lb200,pds6) | 18 | 33.3% | 5.00% | 25.48% | 0.196x | **N** | — | 21.26% | -9.45% | 37.23% | -0.254x | 70 | 0.16% | -0.09% | — |
| `apirine-sdo-zero-cross` | BNBUSDT | 4h | mode_b|(n14,lb100,pds3,rising) | 41 | 31.7% | 7.63% | 25.48% | 0.299x | **N** | — | 15.29% | -30.01% | 37.23% | -0.806x | 170 | 0.24% | -0.62% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 1h | mode_a|(s8,dom27) | 154 | 31.8% | -21.12% | 28.29% | -0.747x | **N** | — | 39.47% | -86.69% | 38.03% | -2.279x | 612 | -0.51% | -4.63% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 1h | mode_a|(s6,dom20) | 200 | 28.5% | -32.72% | 28.29% | -1.157x | **N** | — | 40.43% | -84.49% | 38.03% | -2.221x | 773 | -0.92% | -4.25% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 1h | mode_a|(s8,dom20) | 176 | 28.4% | -27.79% | 28.29% | -0.982x | **N** | — | 42.27% | -82.73% | 38.03% | -2.175x | 689 | -0.73% | -4.00% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 1h | mode_a|(s10,dom34) | 121 | 28.9% | -6.02% | 28.29% | -0.213x | **N** | — | 27.72% | -74.86% | 38.03% | -1.968x | 489 | -0.09% | -3.11% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 1h | mode_b|(s8,dom27,rising) | 154 | 31.8% | -21.12% | 28.29% | -0.747x | **N** | — | 39.47% | -86.69% | 38.03% | -2.279x | 612 | -0.51% | -4.63% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 4h | mode_a|(s8,dom27) | 38 | 44.7% | 7.89% | 25.48% | 0.310x | **N** | — | 12.11% | 0.74% | 37.23% | 0.020x | 154 | 0.23% | 0.26% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 4h | mode_a|(s6,dom20) | 49 | 40.8% | 5.13% | 25.48% | 0.201x | **N** | — | 14.89% | 1.97% | 37.23% | 0.053x | 194 | 0.18% | 0.29% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 4h | mode_a|(s8,dom20) | 44 | 38.6% | -2.27% | 25.48% | -0.089x | **N** | — | 15.20% | -20.27% | 37.23% | -0.544x | 177 | -0.01% | -0.33% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 4h | mode_a|(s10,dom34) | 32 | 40.6% | -6.41% | 25.48% | -0.252x | **N** | — | 20.84% | -36.72% | 37.23% | -0.986x | 122 | -0.12% | -0.86% | — |
| `ehlers-madh-zero-cross` | BNBUSDT | 4h | mode_b|(s8,dom27,rising) | 38 | 44.7% | 7.89% | 25.48% | 0.310x | **N** | — | 12.11% | 0.74% | 37.23% | 0.020x | 154 | 0.23% | 0.26% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 1h | mode_a|(per8,sm5) | 162 | 29.6% | -25.70% | 28.29% | -0.909x | **N** | — | 39.15% | -78.54% | 38.03% | -2.065x | 654 | -0.66% | -3.44% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 1h | mode_a|(per5,sm3) | 292 | 25.0% | -50.22% | 28.29% | -1.775x | **N** | — | 53.18% | -94.03% | 38.03% | -2.473x | 1138 | -1.67% | -6.47% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 1h | mode_a|(per8,sm3) | 212 | 29.2% | -29.99% | 28.29% | -1.060x | **N** | — | 37.16% | -84.76% | 38.03% | -2.229x | 855 | -0.83% | -4.28% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 1h | mode_a|(per14,sm8) | 100 | 33.0% | -4.69% | 28.29% | -0.166x | **N** | — | 21.00% | -54.28% | 38.03% | -1.427x | 394 | -0.06% | -1.64% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 1h | mode_b|(per8,sm5,dip-0.2) | 145 | 30.3% | -26.84% | 28.29% | -0.949x | **N** | — | 34.43% | -73.29% | 38.03% | -1.927x | 587 | -0.71% | -2.93% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 4h | mode_a|(per8,sm5) | 46 | 37.0% | 1.99% | 25.48% | 0.078x | **N** | — | 16.35% | -8.58% | 37.23% | -0.230x | 179 | 0.10% | 0.01% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 4h | mode_a|(per5,sm3) | 75 | 33.3% | 13.30% | 25.48% | 0.522x | **N** | — | 15.82% | -9.57% | 37.23% | -0.257x | 286 | 0.38% | 0.04% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 4h | mode_a|(per8,sm3) | 56 | 37.5% | 4.97% | 25.48% | 0.195x | **N** | — | 18.64% | 8.12% | 37.23% | 0.218x | 220 | 0.18% | 0.47% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 4h | mode_a|(per14,sm8) | 30 | 40.0% | -13.75% | 25.48% | -0.540x | **N** | — | 26.79% | -29.68% | 37.23% | -0.797x | 111 | -0.32% | -0.59% | — |
| `premier-stochastic-osc-zero` | BNBUSDT | 4h | mode_b|(per8,sm5,dip-0.2) | 43 | 37.2% | 5.09% | 25.48% | 0.200x | **N** | — | 14.07% | 8.12% | 37.23% | 0.218x | 158 | 0.17% | 0.41% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 1h | mode_a|(p20,pds20,m5) | 115 | 25.2% | -12.57% | 28.29% | -0.444x | **N** | — | 30.67% | -69.13% | 38.03% | -1.818x | 455 | -0.28% | -2.66% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 1h | mode_a|(p10,pds10,m5) | 247 | 20.6% | -46.89% | 28.29% | -1.658x | **N** | — | 52.43% | -92.18% | 38.03% | -2.424x | 999 | -1.49% | -5.87% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 1h | mode_a|(p20,pds10,m8) | 152 | 25.7% | -20.78% | 28.29% | -0.735x | **N** | — | 36.93% | -81.61% | 38.03% | -2.146x | 614 | -0.51% | -3.89% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 1h | mode_a|(p40,pds40,m10) | 82 | 23.2% | -12.99% | 28.29% | -0.459x | **N** | — | 28.49% | -52.60% | 38.03% | -1.383x | 298 | -0.29% | -1.63% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 1h | mode_b|(p20,pds20,m5,close_gate) | 115 | 25.2% | -12.57% | 28.29% | -0.444x | **N** | — | 30.67% | -69.13% | 38.03% | -1.818x | 455 | -0.28% | -2.66% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 4h | mode_a|(p20,pds20,m5) | 28 | 35.7% | 9.51% | 25.48% | 0.373x | **N** | — | 20.98% | -17.94% | 37.23% | -0.482x | 110 | 0.27% | -0.27% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 4h | mode_a|(p10,pds10,m5) | 73 | 27.4% | -7.47% | 25.48% | -0.293x | **N** | — | 22.89% | -45.70% | 37.23% | -1.227x | 266 | -0.14% | -1.30% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 4h | mode_a|(p20,pds10,m8) | 43 | 27.9% | -0.51% | 25.48% | -0.020x | **N** | — | 26.97% | -35.90% | 37.23% | -0.964x | 159 | 0.03% | -0.87% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 4h | mode_a|(p40,pds40,m10) | 21 | 33.3% | 7.66% | 25.48% | 0.301x | **N** | — | 20.36% | -9.86% | 37.23% | -0.265x | 62 | 0.22% | -0.06% | — |
| `apirine-tradj-ema-cross` | BNBUSDT | 4h | mode_b|(p20,pds20,m5,close_gate) | 28 | 35.7% | 9.51% | 25.48% | 0.373x | **N** | — | 20.98% | -17.94% | 37.23% | -0.482x | 110 | 0.27% | -0.27% | — |
