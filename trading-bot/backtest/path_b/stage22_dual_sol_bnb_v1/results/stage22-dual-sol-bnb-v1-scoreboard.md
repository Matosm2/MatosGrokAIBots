# Scoreboard: stage22-dual-sol-bnb-v1

**Date (UTC):** 2026-09-18 07:06:27
**Track:** Track 1 Path B (Track 2 Discord OFF-LIMITS)
**Status:** RESEARCH / OPTIMISE ONLY — LIVE frozen
**Design bias:** BTC LEAD PRIMARY without over-damp (stage12/15/18/20/21 rhyme). Denser n >> 9. Stop-ladder: BTC -> ETH -> SOL -> BNB.
**VFI Early-Kill Execution:** Strategy 4 (`katsanos-vfi-zero-cross`) RETAINED.

## Summary

- Total Scored Cells: 40
- Total Skipped / Pruned Cells: 88
- BTC PASS_6m: 4 / 32
- ETH PASS_6m: 4 / 4
- SOL PASS_6m: 0 / 4
- BNB PASS_6m: 0 / 0

## Full Results Table

| Symbol | Strategy ID | TF | Mode/Params | 6m Gate | 6m Ret | 6m B&H | xB&H | 6m n | 6m WR | Full Gate | Full Ret | Full xB&H | Ops 6m | Ops Full | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Notes |
|--------|-------------|----|-------------|---------|--------|--------|------|------|------|-----------|----------|-----------|--------|----------|-----------|-----------|-----------|-----------|-------|
| BTCUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p90,p10)` | **FAIL** | -11.40% | 10.82% | -1.054x | 35 | 31.4% | FAIL | -25.62% | -0.891x | -0.23% | -0.47% | Y | Y | Y | Y |  |
| BTCUSDT | `percentile-channel-break` | 1h | `mode_a|(len70,p90,p10)` | **FAIL** | -13.85% | 10.82% | -1.280x | 29 | 27.6% | FAIL | -32.98% | -1.147x | -0.30% | -0.68% | Y | Y | Y | Y |  |
| BTCUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p95,p5)` | **FAIL** | -14.66% | 10.82% | -1.355x | 30 | 26.7% | FAIL | -26.20% | -0.911x | -0.32% | -0.51% | Y | Y | Y | Y |  |
| BTCUSDT | `percentile-channel-break` | 1h | `mode_b|(len50,p90,p10,wpr50)` | **FAIL** | 4.19% | 10.82% | 0.387x | 14 | 42.9% | FAIL | 4.19% | 0.146x | 0.16% | 0.29% | Y | Y | Y | Y |  |
| BTCUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p90,p10)` | **PASS** | 13.21% | 10.66% | 1.240x | 7 | 42.9% | PASS | 65.34% | 2.309x | 0.37% | 1.66% | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=7 in thin band [6..10]) |
| BTCUSDT | `percentile-channel-break` | 4h | `mode_a|(len70,p90,p10)` | **FAIL** | 9.83% | 10.66% | 0.922x | 5 | 40.0% | FAIL | 31.64% | 1.118x | 0.28% | 1.00% | Y | Y | Y | Y | TINY-N KILL (BTC 6m n=5 <= 5); Near-miss 6m (0.92x B&H) |
| BTCUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p95,p5)` | **FAIL** | 15.97% | 10.66% | 1.498x | 5 | 60.0% | PASS | 51.79% | 1.830x | 0.41% | 1.42% | Y | Y | Y | Y | TINY-N KILL (BTC 6m n=5 <= 5) |
| BTCUSDT | `percentile-channel-break` | 4h | `mode_b|(len50,p90,p10,wpr50)` | **FAIL** | -15.44% | 10.66% | -1.449x | 6 | 33.3% | PASS | 47.97% | 1.695x | -0.40% | 1.29% | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=6 in thin band [6..10]) |
| BTCUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.0,exit0.0)` | **FAIL** | -36.78% | 10.82% | -3.400x | 148 | 23.6% | FAIL | -82.97% | -2.885x | -1.08% | -4.14% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len30,thr1.0,exit0.0)` | **FAIL** | -22.37% | 10.82% | -2.068x | 100 | 27.0% | FAIL | -68.13% | -2.369x | -0.58% | -2.63% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.5,exit0.5)` | **FAIL** | -25.41% | 10.82% | -2.349x | 132 | 23.5% | FAIL | -75.92% | -2.640x | -0.68% | -3.35% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 1h | `mode_b|(len20,thr1.0,exit0.0,rising)` | **FAIL** | -36.78% | 10.82% | -3.400x | 148 | 23.6% | FAIL | -82.97% | -2.885x | -1.08% | -4.14% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.0,exit0.0)` | **FAIL** | -8.61% | 10.66% | -0.808x | 36 | 25.0% | FAIL | -32.25% | -1.139x | -0.16% | -0.73% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len30,thr1.0,exit0.0)` | **FAIL** | 4.43% | 10.66% | 0.416x | 22 | 27.3% | FAIL | -28.86% | -1.020x | 0.17% | -0.61% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.5,exit0.5)` | **FAIL** | -8.41% | 10.66% | -0.789x | 35 | 20.0% | FAIL | -32.01% | -1.131x | -0.17% | -0.80% | Y | Y | Y | Y |  |
| BTCUSDT | `zscore-threshold-hold` | 4h | `mode_b|(len20,thr1.0,exit0.0,rising)` | **FAIL** | -8.61% | 10.66% | -0.808x | 36 | 25.0% | FAIL | -32.25% | -1.139x | -0.16% | -0.73% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age0)` | **FAIL** | -60.49% | 10.82% | -5.591x | 337 | 18.1% | FAIL | -96.96% | -3.371x | -2.23% | -8.09% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot8,8,age0)` | **FAIL** | -53.17% | 10.82% | -4.915x | 267 | 17.2% | FAIL | -93.92% | -3.266x | -1.81% | -6.50% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age3)` | **FAIL** | -60.49% | 10.82% | -5.591x | 337 | 18.1% | FAIL | -96.96% | -3.371x | -2.23% | -8.09% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 1h | `mode_b|(pivot5,5,age3,gate)` | **FAIL** | -60.49% | 10.82% | -5.591x | 337 | 18.1% | FAIL | -96.96% | -3.371x | -2.23% | -8.09% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age0)` | **FAIL** | -16.36% | 10.66% | -1.535x | 83 | 21.7% | FAIL | -52.40% | -1.852x | -0.38% | -1.53% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot8,8,age0)` | **FAIL** | -1.50% | 10.66% | -0.140x | 60 | 20.0% | FAIL | -46.40% | -1.640x | 0.04% | -1.26% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age3)` | **FAIL** | -16.36% | 10.66% | -1.535x | 83 | 21.7% | FAIL | -52.40% | -1.852x | -0.38% | -1.53% | Y | Y | Y | Y |  |
| BTCUSDT | `anchored-vwap-swing-flip` | 4h | `mode_b|(pivot5,5,age3,gate)` | **FAIL** | -16.36% | 10.66% | -1.535x | 83 | 21.7% | FAIL | -52.40% | -1.852x | -0.38% | -1.53% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.1,vc2.5,sm3)` | **FAIL** | -10.62% | 10.82% | -0.982x | 50 | 22.0% | FAIL | -65.46% | -2.276x | -0.22% | -2.37% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per50,c0.1,vc2.5,sm3)` | **FAIL** | -18.35% | 10.82% | -1.697x | 73 | 20.5% | FAIL | -36.82% | -1.280x | -0.45% | -0.89% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.2,vc2.5,sm3)` | **FAIL** | -16.61% | 10.82% | -1.536x | 60 | 21.7% | FAIL | -56.30% | -1.957x | -0.39% | -1.78% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | **FAIL** | -8.86% | 10.82% | -0.819x | 41 | 22.0% | FAIL | -54.81% | -1.906x | -0.17% | -1.76% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.1,vc2.5,sm3)` | **FAIL** | 7.68% | 10.66% | 0.720x | 15 | 40.0% | FAIL | 22.50% | 0.795x | 0.23% | 0.83% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per50,c0.1,vc2.5,sm3)` | **PASS** | 31.29% | 10.66% | 2.935x | 13 | 53.8% | FAIL | 33.14% | 1.171x | 0.75% | 0.91% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.2,vc2.5,sm3)` | **PASS** | 14.11% | 10.66% | 1.324x | 15 | 20.0% | FAIL | 14.25% | 0.504x | 0.42% | 0.63% | Y | Y | Y | Y |  |
| BTCUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | **PASS** | 21.36% | 10.66% | 2.004x | 11 | 54.5% | FAIL | 23.54% | 0.832x | 0.52% | 0.82% | Y | Y | Y | Y |  |
| ETHUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percentile-channel-break` | 1h | `mode_a|(len70,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p95,p5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percentile-channel-break` | 1h | `mode_b|(len50,p90,p10,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p90,p10)` | **PASS** | 19.46% | 15.98% | 1.218x | 6 | 50.0% | FAIL | 5.91% | 1.005x | 0.52% | 0.81% | Y | Y | Y | Y | ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | `percentile-channel-break` | 4h | `mode_a|(len70,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p95,p5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `percentile-channel-break` | 4h | `mode_b|(len50,p90,p10,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len30,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.5,exit0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 1h | `mode_b|(len20,thr1.0,exit0.0,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len30,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.5,exit0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `zscore-threshold-hold` | 4h | `mode_b|(len20,thr1.0,exit0.0,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot8,8,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 1h | `mode_b|(pivot5,5,age3,gate)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot8,8,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `anchored-vwap-swing-flip` | 4h | `mode_b|(pivot5,5,age3,gate)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per50,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.2,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per50,c0.1,vc2.5,sm3)` | **PASS** | 58.56% | 15.98% | 3.665x | 17 | 58.8% | PASS | 51.15% | 8.703x | 1.28% | 1.66% | Y | Y | Y | Y | ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.2,vc2.5,sm3)` | **PASS** | 23.92% | 15.98% | 1.497x | 17 | 41.2% | PASS | 14.69% | 2.499x | 0.66% | 1.12% | Y | Y | Y | Y | ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | **PASS** | 25.62% | 15.98% | 1.603x | 13 | 46.2% | PASS | 23.99% | 4.081x | 0.69% | 1.31% | Y | Y | Y | Y | ETH hard filter (BTC->ETH portability check) |
| SOLUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percentile-channel-break` | 1h | `mode_a|(len70,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p95,p5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percentile-channel-break` | 1h | `mode_b|(len50,p90,p10,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p90,p10)` | **FAIL** | 16.28% | 17.66% | 0.922x | 8 | 37.5% | FAIL | -19.34% | 0.056x | 0.46% | -0.00% | Y | Y | Y | Y | Near-miss 6m (0.92x B&H); SOL hard filter |
| SOLUSDT | `percentile-channel-break` | 4h | `mode_a|(len70,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p95,p5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `percentile-channel-break` | 4h | `mode_b|(len50,p90,p10,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len30,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.5,exit0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 1h | `mode_b|(len20,thr1.0,exit0.0,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len30,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.5,exit0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `zscore-threshold-hold` | 4h | `mode_b|(len20,thr1.0,exit0.0,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot8,8,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 1h | `mode_b|(pivot5,5,age3,gate)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot8,8,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `anchored-vwap-swing-flip` | 4h | `mode_b|(pivot5,5,age3,gate)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per50,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.2,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per50,c0.1,vc2.5,sm3)` | **FAIL** | 8.78% | 17.66% | 0.497x | 15 | 40.0% | PASS | 31.48% | 2.537x | 0.27% | 0.99% | Y | Y | Y | Y | SOL hard filter |
| SOLUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.2,vc2.5,sm3)` | **FAIL** | 15.50% | 17.66% | 0.877x | 13 | 30.8% | PASS | 16.56% | 1.808x | 0.47% | 0.86% | Y | Y | Y | Y | SOL hard filter |
| SOLUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | **FAIL** | -9.98% | 17.66% | -0.565x | 18 | 22.2% | FAIL | -15.60% | 0.238x | -0.13% | 0.07% | Y | Y | Y | Y | SOL hard filter |
| BNBUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 1h | `mode_a|(len70,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 1h | `mode_a|(len50,p95,p5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 1h | `mode_b|(len50,p90,p10,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len30,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 1h | `mode_a|(len20,thr1.5,exit0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 1h | `mode_b|(len20,thr1.0,exit0.0,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot8,8,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 1h | `mode_a|(pivot5,5,age3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 1h | `mode_b|(pivot5,5,age3,gate)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per50,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_a|(per80,c0.2,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 1h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 4h | `mode_a|(len70,p90,p10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 4h | `mode_a|(len50,p95,p5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `percentile-channel-break` | 4h | `mode_b|(len50,p90,p10,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len30,thr1.0,exit0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 4h | `mode_a|(len20,thr1.5,exit0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `zscore-threshold-hold` | 4h | `mode_b|(len20,thr1.0,exit0.0,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot8,8,age0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 4h | `mode_a|(pivot5,5,age3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `anchored-vwap-swing-flip` | 4h | `mode_b|(pivot5,5,age3,gate)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per50,c0.1,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_a|(per80,c0.2,vc2.5,sm3)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `katsanos-vfi-zero-cross` | 4h | `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
