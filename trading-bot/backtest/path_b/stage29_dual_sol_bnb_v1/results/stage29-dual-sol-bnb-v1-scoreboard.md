# stage29-dual-sol-bnb-v1 — Scoreboard

- Generated: 2026-09-21 21:41:25 UTC
- Research ID: `stage29-dual-sol-bnb-v1` (Track 1 Path B)
- Stop-Ladder: `BTCUSDT -> ETHUSDT (HARD) -> SOLUSDT (HARD) -> BNBUSDT (HARD)`
- Gate Rule: Last 6m Mode-A Return >= 1.2x Buy & Hold, n > 5 (tiny-n kill threshold)
- Fees / Slip: 0.10% / side fee + 0.05% adverse slippage
- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)
- Strategy Encode Order (exactly 4):
  1. `katsanos-stiffness-threshold`
  2. `cpr-range-break-accept`
  3. `varadi-dvs-stretch-midline`
  4. `historical-volatility-ratio-expand-dir`

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
| BTCUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | 5.30% | 27.32% | 0.194x | 15 | 33.3% | 18.37% | FAIL | 10.13% | 38.14% | 0.266x | 50 | 0.20% | 0.43% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | 24.11% | 27.32% | 0.883x | 19 | 47.4% | 19.32% | FAIL | 6.45% | 38.14% | 0.169x | 83 | 0.62% | 0.38% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | 22.49% | 27.32% | 0.823x | 8 | 50.0% | 8.52% | FAIL | 11.76% | 38.14% | 0.308x | 37 | 0.54% | 0.43% | Y | Y | Y | Y | — | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 1h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | 19.44% | 27.32% | 0.711x | 12 | 33.3% | 11.80% | FAIL | 14.62% | 38.14% | 0.383x | 46 | 0.50% | 0.52% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | 1.00% | 23.34% | 0.043x | 3 | 33.3% | 9.06% | FAIL | 31.81% | 36.92% | 0.862x | 13 | 0.03% | 0.95% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=3 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | 0.57% | 23.34% | 0.024x | 5 | 40.0% | 12.38% | FAIL | 44.13% | 36.92% | 1.195x | 17 | 0.02% | 1.16% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=5 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | -4.31% | 23.34% | -0.184x | 3 | 33.3% | 10.57% | FAIL | 26.19% | 36.92% | 0.709x | 11 | -0.11% | 0.79% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=3 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `katsanos-stiffness-threshold` | 4h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | 0.09% | 23.34% | 0.004x | 3 | 33.3% | 10.48% | FAIL | 13.88% | 36.92% | 0.376x | 13 | 0.01% | 0.61% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=3 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 1h | mode_a|(N24) | **FAIL** | -26.49% | 27.32% | -0.970x | 201 | 21.9% | 47.50% | FAIL | -92.08% | 38.14% | -2.414x | 865 | -0.69% | -5.89% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 1h | mode_a|(N12) | **FAIL** | -55.03% | 27.32% | -2.014x | 322 | 22.0% | 62.13% | FAIL | -97.50% | 38.14% | -2.556x | 1288 | -1.90% | -8.56% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 1h | mode_a|(N48) | **FAIL** | -20.97% | 27.32% | -0.768x | 145 | 17.2% | 33.28% | FAIL | -81.74% | 38.14% | -2.143x | 612 | -0.51% | -3.91% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 1h | mode_b|(N24,narrow0.002) | **FAIL** | -14.42% | 27.32% | -0.528x | 167 | 23.4% | 39.71% | FAIL | -78.38% | 38.14% | -2.055x | 692 | -0.32% | -3.55% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 4h | mode_a|(N24) | **FAIL** | -5.34% | 23.34% | -0.229x | 52 | 21.2% | 30.80% | FAIL | -38.15% | 36.92% | -1.033x | 207 | -0.05% | -0.86% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 4h | mode_a|(N12) | **FAIL** | -3.27% | 23.34% | -0.140x | 73 | 21.9% | 26.82% | FAIL | -36.18% | 36.92% | -0.980x | 287 | -0.01% | -0.87% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 4h | mode_a|(N48) | **FAIL** | 17.51% | 23.34% | 0.750x | 28 | 25.0% | 14.97% | FAIL | -25.06% | 36.92% | -0.679x | 136 | 0.48% | -0.48% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `cpr-range-break-accept` | 4h | mode_b|(N24,narrow0.002) | **FAIL** | -19.67% | 23.34% | -0.843x | 27 | 11.1% | 20.92% | FAIL | -49.14% | 36.92% | -1.331x | 115 | -0.54% | -1.61% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum20,rank100,mid50) | **FAIL** | -25.55% | 27.32% | -0.935x | 149 | 27.5% | 39.59% | FAIL | -75.24% | 38.14% | -1.973x | 663 | -0.65% | -3.12% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum10,rank63,mid50) | **FAIL** | -51.03% | 27.32% | -1.868x | 243 | 25.1% | 59.00% | FAIL | -94.86% | 38.14% | -2.487x | 980 | -1.70% | -6.85% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum40,rank126,mid50) | **FAIL** | -23.28% | 27.32% | -0.852x | 107 | 26.2% | 33.93% | FAIL | -47.60% | 38.14% | -1.248x | 446 | -0.59% | -1.37% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 1h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | -20.84% | 27.32% | -0.763x | 124 | 30.6% | 40.58% | FAIL | -64.31% | 38.14% | -1.686x | 519 | -0.48% | -2.21% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum20,rank100,mid50) | **FAIL** | 18.92% | 23.34% | 0.811x | 47 | 31.9% | 14.63% | FAIL | -26.00% | 36.92% | -0.704x | 172 | 0.53% | -0.48% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum10,rank63,mid50) | **FAIL** | 3.36% | 23.34% | 0.144x | 57 | 38.6% | 20.36% | FAIL | -19.14% | 36.92% | -0.518x | 228 | 0.13% | -0.30% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum40,rank126,mid50) | **FAIL** | 12.51% | 23.34% | 0.536x | 37 | 32.4% | 20.76% | FAIL | -27.96% | 36.92% | -0.757x | 134 | 0.41% | -0.56% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `varadi-dvs-stretch-midline` | 4h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | 25.52% | 23.34% | 1.093x | 34 | 35.3% | 13.01% | FAIL | -0.80% | 36.92% | -0.022x | 128 | 0.67% | 0.25% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | -13.15% | 27.32% | -0.481x | 61 | 14.8% | 17.87% | FAIL | -41.62% | 38.14% | -1.091x | 225 | -0.35% | -1.30% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | -16.30% | 27.32% | -0.597x | 77 | 19.5% | 20.88% | FAIL | -63.46% | 38.14% | -1.664x | 313 | -0.44% | -2.46% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | -15.48% | 27.32% | -0.567x | 49 | 20.4% | 20.18% | FAIL | -37.08% | 38.14% | -0.972x | 198 | -0.41% | -1.12% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | -13.15% | 27.32% | -0.481x | 61 | 14.8% | 17.87% | FAIL | -41.62% | 38.14% | -1.091x | 225 | -0.35% | -1.30% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | -14.66% | 23.34% | -0.628x | 17 | 11.8% | 15.70% | FAIL | -4.70% | 36.92% | -0.127x | 62 | -0.39% | -0.08% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | -4.75% | 23.34% | -0.204x | 18 | 22.2% | 9.80% | FAIL | -23.40% | 36.92% | -0.634x | 85 | -0.12% | -0.64% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | -5.78% | 23.34% | -0.248x | 17 | 29.4% | 10.35% | FAIL | -9.26% | 36.92% | -0.251x | 56 | -0.14% | -0.20% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | -14.66% | 23.34% | -0.628x | 17 | 11.8% | 15.70% | FAIL | -4.70% | 36.92% | -0.127x | 62 | -0.39% | -0.08% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| ETHUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 1h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-stiffness-threshold` | 4h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 1h | mode_a|(N24) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 1h | mode_a|(N12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 1h | mode_a|(N48) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 1h | mode_b|(N24,narrow0.002) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 4h | mode_a|(N24) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 4h | mode_a|(N12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 4h | mode_a|(N48) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `cpr-range-break-accept` | 4h | mode_b|(N24,narrow0.002) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum20,rank100,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum10,rank63,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum40,rank126,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 1h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum20,rank100,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum10,rank63,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum40,rank126,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `varadi-dvs-stretch-midline` | 4h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 1h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-stiffness-threshold` | 4h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 1h | mode_a|(N24) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 1h | mode_a|(N12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 1h | mode_a|(N48) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 1h | mode_b|(N24,narrow0.002) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 4h | mode_a|(N24) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 4h | mode_a|(N12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 4h | mode_a|(N48) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `cpr-range-break-accept` | 4h | mode_b|(N24,narrow0.002) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum20,rank100,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum10,rank63,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum40,rank126,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 1h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum20,rank100,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum10,rank63,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum40,rank126,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `varadi-dvs-stretch-midline` | 4h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 1h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 1h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 4h | mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-stiffness-threshold` | 4h | mode_b|(mab100,p60,buy95,sell50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 1h | mode_a|(N24) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 1h | mode_a|(N12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 1h | mode_a|(N48) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 1h | mode_b|(N24,narrow0.002) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 4h | mode_a|(N24) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 4h | mode_a|(N12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 4h | mode_a|(N48) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `cpr-range-break-accept` | 4h | mode_b|(N24,narrow0.002) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum20,rank100,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum10,rank63,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 1h | mode_a|(sum40,rank126,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 1h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum20,rank100,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum10,rank63,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 4h | mode_a|(sum40,rank126,mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `varadi-dvs-stretch-midline` | 4h | mode_b|(sum20,rank100,rec40_exit50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 1h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s10,l100,exp0.5,dir5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s6,l50,exp0.4,dir3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_a|(s14,l100,exp0.6,dir8) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `historical-volatility-ratio-expand-dir` | 4h | mode_b|(s10,l100,exp0.5,dir5,comp0.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
