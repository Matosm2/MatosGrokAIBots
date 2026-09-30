# stage28-dual-sol-bnb-v1 — Scoreboard

- Generated: 2026-09-21 21:15:32 UTC
- Research ID: `stage28-dual-sol-bnb-v1` (Track 1 Path B)
- Stop-Ladder: `BTCUSDT -> ETHUSDT (HARD) -> SOLUSDT (HARD) -> BNBUSDT (HARD)`
- Gate Rule: Last 6m Mode-A Return >= 1.2x Buy & Hold, n > 5 (tiny-n kill threshold)
- Fees / Slip: 0.10% / side fee + 0.05% adverse slippage
- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)
- Strategy Encode Order (exactly 4):
  1. `ehlers-ec-ema-cross`
  2. `vervoort-zlha-typ-cross`
  3. `ehlers-fir-zl-price-cross`
  4. `dv2-varadi-midline`

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
| BTCUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len20,gain50,thr0) | **FAIL** | -38.10% | 27.32% | -1.395x | 189 | 20.1% | 50.66% | FAIL | -86.94% | 38.14% | -2.279x | 750 | -1.12% | -4.71% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len12,gain22,thr0) | **FAIL** | -44.54% | 27.32% | -1.630x | 223 | 20.6% | 54.08% | FAIL | -90.40% | 38.14% | -2.370x | 875 | -1.38% | -5.45% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len32,gain50,thr0) | **FAIL** | -15.97% | 27.32% | -0.585x | 105 | 23.8% | 32.27% | FAIL | -60.27% | 38.14% | -1.580x | 435 | -0.37% | -2.06% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 1h | mode_b|(len20,gain50,thr0.75) | **FAIL** | -1.88% | 27.32% | -0.069x | 7 | 57.1% | 4.10% | FAIL | -15.26% | 38.14% | -0.400x | 28 | -0.05% | -0.40% | Y | Y | Y | Y | — | THIN-N FLAG (BTC 6m n=7 in thin band [6..10]); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len20,gain50,thr0) | **FAIL** | 2.75% | 23.34% | 0.118x | 47 | 27.7% | 23.69% | FAIL | -29.07% | 36.92% | -0.787x | 174 | 0.16% | -0.53% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len12,gain22,thr0) | **FAIL** | 9.41% | 23.34% | 0.403x | 51 | 27.5% | 19.47% | FAIL | -17.74% | 36.92% | -0.480x | 206 | 0.32% | -0.20% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len32,gain50,thr0) | **FAIL** | 4.88% | 23.34% | 0.209x | 30 | 33.3% | 19.12% | FAIL | -13.90% | 36.92% | -0.377x | 112 | 0.19% | -0.05% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-ec-ema-cross` | 4h | mode_b|(len20,gain50,thr0.75) | **FAIL** | -1.91% | 23.34% | -0.082x | 5 | 40.0% | 9.77% | FAIL | -34.03% | 36.92% | -0.922x | 35 | -0.04% | -0.99% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=5 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N34) | **FAIL** | -38.89% | 27.32% | -1.423x | 202 | 26.2% | 50.69% | FAIL | -87.50% | 38.14% | -2.294x | 798 | -1.14% | -4.80% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N21) | **FAIL** | -55.86% | 27.32% | -2.045x | 276 | 23.2% | 60.88% | FAIL | -91.61% | 38.14% | -2.402x | 1029 | -1.97% | -5.78% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N55) | **FAIL** | -16.93% | 27.32% | -0.620x | 143 | 27.3% | 38.43% | FAIL | -80.60% | 38.14% | -2.113x | 603 | -0.39% | -3.76% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 1h | mode_b|(N34_rising) | **FAIL** | -38.20% | 27.32% | -1.398x | 200 | 26.5% | 50.13% | FAIL | -86.72% | 38.14% | -2.273x | 790 | -1.11% | -4.66% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N34) | **FAIL** | 18.17% | 23.34% | 0.778x | 45 | 33.3% | 11.85% | FAIL | -16.97% | 36.92% | -0.460x | 184 | 0.49% | -0.22% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N21) | **FAIL** | -1.45% | 23.34% | -0.062x | 62 | 35.5% | 17.38% | FAIL | -33.64% | 36.92% | -0.911x | 246 | -0.00% | -0.81% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N55) | **FAIL** | 19.41% | 23.34% | 0.832x | 38 | 28.9% | 17.55% | FAIL | -6.10% | 36.92% | -0.165x | 145 | 0.53% | 0.13% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `vervoort-zlha-typ-cross` | 4h | mode_b|(N34_rising) | **FAIL** | 18.84% | 23.34% | 0.807x | 44 | 34.1% | 11.85% | FAIL | -16.63% | 36.92% | -0.450x | 182 | 0.50% | -0.21% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_close_zl9.5) | **FAIL** | -86.12% | 27.32% | -3.152x | 723 | 23.8% | 86.84% | FAIL | -99.98% | 38.14% | -2.621x | 2969 | -4.77% | -19.26% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_hl2_zl9.5) | **FAIL** | -82.70% | 27.32% | -3.027x | 662 | 24.3% | 84.07% | FAIL | -99.96% | 38.14% | -2.621x | 2673 | -4.24% | -17.42% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_close_fir12) | **FAIL** | -83.25% | 27.32% | -3.047x | 588 | 17.7% | 84.93% | FAIL | -99.94% | 38.14% | -2.620x | 2310 | -4.32% | -16.60% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_hl2_fir12) | **FAIL** | -82.71% | 27.32% | -3.027x | 554 | 17.9% | 84.50% | FAIL | -99.90% | 38.14% | -2.619x | 2141 | -4.24% | -15.57% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_close_zl9.5) | **FAIL** | -43.31% | 23.34% | -1.855x | 185 | 30.3% | 54.57% | FAIL | -86.83% | 36.92% | -2.352x | 746 | -1.36% | -4.72% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_hl2_zl9.5) | **FAIL** | -34.95% | 23.34% | -1.497x | 166 | 33.1% | 46.74% | FAIL | -81.95% | 36.92% | -2.220x | 657 | -1.02% | -3.94% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_close_fir12) | **FAIL** | -32.92% | 23.34% | -1.410x | 141 | 27.7% | 45.63% | FAIL | -80.53% | 36.92% | -2.181x | 572 | -0.94% | -3.78% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_hl2_fir12) | **FAIL** | -33.22% | 23.34% | -1.423x | 136 | 26.5% | 44.59% | FAIL | -78.53% | 36.92% | -2.127x | 532 | -0.95% | -3.54% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank100_mid50) | **FAIL** | -90.55% | 27.32% | -3.314x | 791 | 18.7% | 91.51% | FAIL | -100.00% | 38.14% | -2.622x | 3096 | -5.68% | -21.78% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank63_mid50) | **FAIL** | -90.91% | 27.32% | -3.328x | 799 | 18.0% | 91.82% | FAIL | -100.00% | 38.14% | -2.622x | 3111 | -5.77% | -21.79% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank126_mid50) | **FAIL** | -90.15% | 27.32% | -3.300x | 795 | 18.4% | 91.10% | FAIL | -99.99% | 38.14% | -2.622x | 3094 | -5.58% | -21.68% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 1h | mode_b|(rank100_reclaim40) | **FAIL** | -89.09% | 27.32% | -3.261x | 721 | 21.2% | 89.69% | FAIL | -99.99% | 38.14% | -2.621x | 2808 | -5.34% | -19.57% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank100_mid50) | **FAIL** | -45.13% | 23.34% | -1.933x | 191 | 25.7% | 53.53% | FAIL | -89.98% | 36.92% | -2.437x | 770 | -1.43% | -5.36% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank63_mid50) | **FAIL** | -50.19% | 23.34% | -2.150x | 199 | 25.6% | 58.55% | FAIL | -91.71% | 36.92% | -2.484x | 782 | -1.67% | -5.80% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank126_mid50) | **FAIL** | -44.18% | 23.34% | -1.893x | 193 | 26.4% | 52.87% | FAIL | -90.26% | 36.92% | -2.445x | 779 | -1.39% | -5.43% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `dv2-varadi-midline` | 4h | mode_b|(rank100_reclaim40) | **FAIL** | -41.57% | 23.34% | -1.781x | 176 | 30.1% | 52.42% | FAIL | -90.06% | 36.92% | -2.439x | 705 | -1.27% | -5.36% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| ETHUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len20,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len12,gain22,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len32,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 1h | mode_b|(len20,gain50,thr0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len20,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len12,gain22,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len32,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-ec-ema-cross` | 4h | mode_b|(len20,gain50,thr0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N34) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N21) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N55) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 1h | mode_b|(N34_rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N34) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N21) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N55) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vervoort-zlha-typ-cross` | 4h | mode_b|(N34_rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_close_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_hl2_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_close_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_hl2_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_close_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_hl2_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_close_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_hl2_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank100_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank63_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank126_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 1h | mode_b|(rank100_reclaim40) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank100_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank63_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank126_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `dv2-varadi-midline` | 4h | mode_b|(rank100_reclaim40) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len20,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len12,gain22,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len32,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 1h | mode_b|(len20,gain50,thr0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len20,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len12,gain22,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len32,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-ec-ema-cross` | 4h | mode_b|(len20,gain50,thr0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N34) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N21) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N55) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 1h | mode_b|(N34_rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N34) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N21) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N55) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vervoort-zlha-typ-cross` | 4h | mode_b|(N34_rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_close_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_hl2_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_close_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_hl2_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_close_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_hl2_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_close_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_hl2_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank100_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank63_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank126_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 1h | mode_b|(rank100_reclaim40) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank100_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank63_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank126_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `dv2-varadi-midline` | 4h | mode_b|(rank100_reclaim40) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len20,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len12,gain22,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 1h | mode_a|(len32,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 1h | mode_b|(len20,gain50,thr0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len20,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len12,gain22,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 4h | mode_a|(len32,gain50,thr0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-ec-ema-cross` | 4h | mode_b|(len20,gain50,thr0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N34) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N21) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 1h | mode_a|(N55) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 1h | mode_b|(N34_rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N34) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N21) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 4h | mode_a|(N55) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vervoort-zlha-typ-cross` | 4h | mode_b|(N34_rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_close_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_a|(src_hl2_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_close_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 1h | mode_b|(src_hl2_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_close_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_a|(src_hl2_zl9.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_close_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-fir-zl-price-cross` | 4h | mode_b|(src_hl2_fir12) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank100_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank63_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 1h | mode_a|(rank126_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 1h | mode_b|(rank100_reclaim40) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank100_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank63_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 4h | mode_a|(rank126_mid50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `dv2-varadi-midline` | 4h | mode_b|(rank100_reclaim40) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
