# stage30-dual-sol-bnb-v1 — Scoreboard

- Generated: 2026-09-21 22:07:49 UTC
- Research ID: `stage30-dual-sol-bnb-v1` (Track 1 Path B)
- Stop-Ladder: `BTCUSDT -> ETHUSDT (HARD) -> SOLUSDT (HARD) -> BNBUSDT (HARD)`
- Gate Rule: Last 6m Mode-A Return >= 1.2x Buy & Hold, n > 5 (tiny-n kill threshold)
- Fees / Slip: 0.10% / side fee + 0.05% adverse slippage
- Sizing: Mode-A Gate (100%), Mode-A Ops (2.5%)
- Strategy Encode Order (exactly 4):
  1. `blau-dti-zero-cross`
  2. `arms-vama-dual-cross`
  3. `apirine-ma-bands-break`
  4. `ehlers-recursive-median-osc-zero`

## Executive Summary
- Total Scored Cells: 33 / 128
- Pruned / Skipped by Stop-Ladder: 95
- Candidates Passing 6m Gate on at least 1 symbol: 1
- Full 4-Coin Ladder Complete Passes: 0

## PASS_6m Promoted Candidates
| Symbol | Strategy ID | TF | Mode/Params | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_50,p2_10,mltp1.0) | 35.47% | 23.34% | 1.520x | 8 | 62.5% | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]); BTC LEAD PRIMARY CRITICAL |

## Full Stop-Ladder Scoreboard

| Symbol | Strategy ID | TF | Mode/Params | 6m Gate | 6m Ret% | 6m B&H% | 6m xB&H | 6m n | 6m WR% | 6m MaxDD% | Full Gate | Full Ret% | Full B&H% | Full xB&H | Full n | Ops 6m% | Ops Full% | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Retention Notes | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q2,r20,s5,u3) | **FAIL** | -10.35% | 26.53% | -0.390x | 91 | 30.8% | 29.10% | FAIL | -61.39% | 37.25% | -1.648x | 378 | -0.20% | -2.12% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q1,r10,s3,u1) | **FAIL** | 0.00% | 26.53% | 0.000x | 0 | 0.0% | 0.00% | FAIL | 0.00% | 37.25% | 0.000x | 0 | 0.00% | 0.00% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=0 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q3,r32,s5,u3) | **FAIL** | -1.42% | 26.53% | -0.054x | 73 | 26.0% | 20.42% | FAIL | -54.58% | 37.25% | -1.465x | 295 | 0.03% | -1.70% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 1h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | -10.35% | 26.53% | -0.390x | 91 | 30.8% | 29.10% | FAIL | -61.39% | 37.25% | -1.648x | 378 | -0.20% | -2.12% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q2,r20,s5,u3) | **FAIL** | 3.21% | 23.34% | 0.137x | 26 | 34.6% | 17.83% | FAIL | -16.82% | 36.92% | -0.456x | 101 | 0.15% | -0.25% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q1,r10,s3,u1) | **FAIL** | 0.00% | 23.34% | 0.000x | 0 | 0.0% | 0.00% | FAIL | 0.00% | 36.92% | 0.000x | 0 | 0.00% | 0.00% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=0 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q3,r32,s5,u3) | **FAIL** | 9.17% | 23.34% | 0.393x | 21 | 33.3% | 13.45% | FAIL | -17.73% | 36.92% | -0.480x | 77 | 0.29% | -0.23% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `blau-dti-zero-cross` | 4h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | 3.21% | 23.34% | 0.137x | 26 | 34.6% | 17.83% | FAIL | -16.82% | 36.92% | -0.456x | 101 | 0.15% | -0.25% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f8,s55,sn100) | **FAIL** | -1.92% | 26.53% | -0.072x | 85 | 30.6% | 24.79% | FAIL | -50.26% | 37.25% | -1.350x | 352 | 0.02% | -1.48% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f5,s34,sn50) | **FAIL** | -17.69% | 26.53% | -0.667x | 139 | 26.6% | 40.97% | FAIL | -75.13% | 37.25% | -2.017x | 582 | -0.41% | -3.16% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f13,s89,sn200) | **FAIL** | 0.57% | 26.53% | 0.021x | 54 | 33.3% | 19.58% | FAIL | -24.69% | 37.25% | -0.663x | 204 | 0.09% | -0.42% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 1h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | -5.56% | 26.53% | -0.210x | 78 | 30.8% | 23.44% | FAIL | -48.38% | 37.25% | -1.299x | 323 | -0.08% | -1.40% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f8,s55,sn100) | **FAIL** | 9.96% | 23.34% | 0.427x | 23 | 43.5% | 14.15% | FAIL | -34.21% | 36.92% | -0.927x | 100 | 0.31% | -0.78% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f5,s34,sn50) | **FAIL** | 16.05% | 23.34% | 0.688x | 29 | 31.0% | 18.61% | FAIL | -15.39% | 36.92% | -0.417x | 135 | 0.46% | -0.15% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f13,s89,sn200) | **FAIL** | 22.16% | 23.34% | 0.949x | 13 | 46.2% | 13.81% | FAIL | 2.50% | 36.92% | 0.068x | 62 | 0.57% | 0.30% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `arms-vama-dual-cross` | 4h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | 13.39% | 23.34% | 0.574x | 21 | 47.6% | 11.47% | FAIL | -21.51% | 36.92% | -0.583x | 91 | 0.39% | -0.35% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | 18.20% | 26.53% | 0.686x | 39 | 35.9% | 13.79% | FAIL | -15.31% | 37.25% | -0.411x | 155 | 0.50% | -0.15% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | 9.75% | 26.53% | 0.367x | 59 | 32.2% | 15.74% | FAIL | -36.18% | 37.25% | -0.971x | 224 | 0.30% | -0.85% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | 4.91% | 26.53% | 0.185x | 18 | 33.3% | 15.63% | FAIL | -18.92% | 37.25% | -0.508x | 63 | 0.19% | -0.20% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 1h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | 17.01% | 26.53% | 0.641x | 39 | 35.9% | 13.79% | FAIL | -5.70% | 37.25% | -0.153x | 152 | 0.48% | 0.11% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_50,p2_10,mltp1.0) | **PASS** | 35.47% | 23.34% | 1.520x | 8 | 62.5% | 7.32% | FAIL | 40.57% | 36.92% | 1.099x | 37 | 0.82% | 1.06% | Y | Y | Y | Y | — | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | 15.50% | 23.34% | 0.664x | 13 | 38.5% | 13.73% | FAIL | -10.79% | 36.92% | -0.292x | 59 | 0.43% | -0.03% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | 20.20% | 23.34% | 0.865x | 5 | 60.0% | 11.36% | FAIL | 25.47% | 36.92% | 0.690x | 16 | 0.49% | 0.86% | Y | Y | Y | Y | — | TINY-N KILL (BTC 6m n=5 <= 5); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `apirine-ma-bands-break` | 4h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | 25.14% | 23.34% | 1.077x | 7 | 57.1% | 8.11% | FAIL | 1.05% | 36.92% | 0.028x | 27 | 0.62% | 0.11% | Y | Y | Y | Y | — | THIN-N FLAG (BTC 6m n=7 in thin band [6..10]); BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp12,hp30,med5) | **FAIL** | -33.20% | 26.53% | -1.252x | 189 | 30.7% | 45.68% | FAIL | -91.21% | 37.25% | -2.449x | 777 | -0.95% | -5.66% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp8,hp20,med5) | **FAIL** | -52.33% | 26.53% | -1.973x | 261 | 29.1% | 57.50% | FAIL | -95.52% | 37.25% | -2.564x | 1044 | -1.79% | -7.25% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp16,hp40,med5) | **FAIL** | -23.57% | 26.53% | -0.889x | 154 | 33.8% | 35.55% | FAIL | -86.50% | 37.25% | -2.322x | 632 | -0.62% | -4.66% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | -33.20% | 26.53% | -1.252x | 189 | 30.7% | 45.68% | FAIL | -91.21% | 37.25% | -2.449x | 777 | -0.95% | -5.66% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp12,hp30,med5) | **FAIL** | 0.73% | 23.34% | 0.031x | 46 | 34.8% | 18.19% | FAIL | -16.99% | 36.92% | -0.460x | 189 | 0.06% | -0.28% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp8,hp20,med5) | **FAIL** | 1.62% | 23.34% | 0.069x | 60 | 43.3% | 16.61% | FAIL | -46.57% | 36.92% | -1.261x | 260 | 0.08% | -1.35% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp16,hp40,med5) | **FAIL** | 9.34% | 23.34% | 0.400x | 39 | 38.5% | 13.53% | FAIL | 1.02% | 36.92% | 0.028x | 151 | 0.30% | 0.26% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| BTCUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | 0.73% | 23.34% | 0.031x | 46 | 34.8% | 18.19% | FAIL | -16.99% | 36.92% | -0.460x | 189 | 0.06% | -0.28% | Y | Y | Y | Y | — | BTC LEAD PRIMARY CRITICAL |
| ETHUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q2,r20,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q1,r10,s3,u1) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q3,r32,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 1h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q2,r20,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q1,r10,s3,u1) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q3,r32,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `blau-dti-zero-cross` | 4h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f8,s55,sn100) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f5,s34,sn50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f13,s89,sn200) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 1h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f8,s55,sn100) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f5,s34,sn50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f13,s89,sn200) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `arms-vama-dual-cross` | 4h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 1h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | -0.10% | 29.37% | -0.004x | 15 | 26.7% | 22.10% | PASS | 43.78% | 7.88% | 5.554x | 42 | 0.11% | 1.57% | Y | Y | Y | Y | OK (ETH n=15 vs BTC n=8) | ETH secondary (eth_smoke; denser n >> 9) |
| ETHUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `apirine-ma-bands-break` | 4h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp12,hp30,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp8,hp20,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp16,hp40,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp12,hp30,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp8,hp20,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp16,hp40,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q2,r20,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q1,r10,s3,u1) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q3,r32,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 1h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q2,r20,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q1,r10,s3,u1) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q3,r32,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `blau-dti-zero-cross` | 4h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f8,s55,sn100) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f5,s34,sn50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f13,s89,sn200) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 1h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f8,s55,sn100) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f5,s34,sn50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f13,s89,sn200) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `arms-vama-dual-cross` | 4h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 1h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `apirine-ma-bands-break` | 4h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp12,hp30,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp8,hp20,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp16,hp40,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp12,hp30,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp8,hp20,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp16,hp40,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q2,r20,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q1,r10,s3,u1) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 1h | mode_a|(q3,r32,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 1h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q2,r20,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q1,r10,s3,u1) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 4h | mode_a|(q3,r32,s5,u3) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `blau-dti-zero-cross` | 4h | mode_b|(q2,r20,s5,u3,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f8,s55,sn100) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f5,s34,sn50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 1h | mode_a|(f13,s89,sn200) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 1h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f8,s55,sn100) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f5,s34,sn50) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 4h | mode_a|(f13,s89,sn200) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `arms-vama-dual-cross` | 4h | mode_b|(f8,s55,sn100,trend_close) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 1h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 1h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_50,p2_10,mltp1.0) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_34,p2_8,mltp0.75) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 4h | mode_a|(p1_100,p2_20,mltp1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `apirine-ma-bands-break` | 4h | mode_b|(p1_50,p2_10,mltp1.0,narrow1.5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp12,hp30,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp8,hp20,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_a|(lp16,hp40,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 1h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp12,hp30,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp8,hp20,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_a|(lp16,hp40,med5) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-recursive-median-osc-zero` | 4h | mode_b|(lp12,hp30,med5,rising) | **FAIL** | — | — | — | — | — | — | FAIL | — | — | — | — | — | — | Y | Y | Y | Y | — | Pruned by stop-ladder (SOL PASS_6m required) |
