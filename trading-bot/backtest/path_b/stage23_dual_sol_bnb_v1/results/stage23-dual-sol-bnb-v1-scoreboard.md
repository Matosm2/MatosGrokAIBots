# Scoreboard: stage23-dual-sol-bnb-v1

**Date (UTC):** 2026-09-18 07:30:50
**Track:** Track 1 Path B (Track 2 Discord OFF-LIMITS)
**Status:** RESEARCH / OPTIMISE ONLY — LIVE frozen
**Design bias:** SOL >= 1.2x after BTC->ETH PRIMARY (stage16 Kagi + stage22 percentile 0.922x near-miss). Denser n >> 9. Stop-ladder: BTC -> ETH -> SOL -> BNB.

## Summary

- Total Scored Cells: 32
- Total Skipped / Pruned Cells: 96
- BTC PASS_6m: 0 / 32
- ETH PASS_6m: 0 / 0
- SOL PASS_6m: 0 / 0
- BNB PASS_6m: 0 / 0

## Full Results Table

| Symbol | Strategy ID | TF | Mode/Params | 6m Gate | 6m Ret | 6m B&H | xB&H | 6m n | 6m WR | Full Gate | Full Ret | Full xB&H | Ops 6m | Ops Full | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Notes |
|--------|-------------|----|-------------|---------|--------|--------|------|------|------|-----------|----------|-----------|--------|----------|-----------|-----------|-----------|-----------|-------|
| BTCUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf5,wt4.236)` | **FAIL** | -28.90% | 11.09% | -2.605x | 125 | 32.8% | FAIL | -82.66% | -2.842x | -0.81% | -4.09% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi21,sf5,wt4.236)` | **FAIL** | -19.71% | 11.09% | -1.777x | 118 | 34.7% | FAIL | -76.35% | -2.625x | -0.50% | -3.33% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf8,wt5.0)` | **FAIL** | -24.94% | 11.09% | -2.248x | 103 | 32.0% | FAIL | -66.41% | -2.284x | -0.67% | -2.49% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 1h | `mode_b|(rsi14,sf5,wt4.236,f50)` | **FAIL** | -15.71% | 11.09% | -1.416x | 52 | 25.0% | FAIL | -48.77% | -1.677x | -0.41% | -1.59% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf5,wt4.236)` | **FAIL** | -5.10% | 10.66% | -0.478x | 32 | 34.4% | FAIL | 6.92% | 0.245x | -0.06% | 0.43% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi21,sf5,wt4.236)` | **FAIL** | -0.87% | 10.66% | -0.082x | 29 | 31.0% | FAIL | -9.08% | -0.321x | 0.04% | 0.02% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf8,wt5.0)` | **FAIL** | -8.04% | 10.66% | -0.754x | 28 | 28.6% | FAIL | 14.52% | 0.513x | -0.14% | 0.60% | Y | Y | Y | Y |  |
| BTCUSDT | `qqe-trailing-cross` | 4h | `mode_b|(rsi14,sf5,wt4.236,f50)` | **FAIL** | -7.72% | 10.66% | -0.724x | 11 | 36.4% | FAIL | -17.18% | -0.607x | -0.20% | -0.43% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.05)` | **FAIL** | -18.05% | 11.09% | -1.627x | 91 | 33.0% | FAIL | -64.50% | -2.218x | -0.44% | -2.33% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.7,slow0.05)` | **FAIL** | -36.65% | 11.09% | -3.304x | 128 | 26.6% | FAIL | -76.71% | -2.638x | -1.08% | -3.35% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.08)` | **FAIL** | -24.06% | 11.09% | -2.169x | 100 | 30.0% | FAIL | -65.39% | -2.248x | -0.63% | -2.40% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 1h | `mode_b|(fast0.5,slow0.05,rising)` | **FAIL** | -18.05% | 11.09% | -1.627x | 91 | 33.0% | FAIL | -64.50% | -2.218x | -0.44% | -2.33% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.05)` | **FAIL** | -1.31% | 10.66% | -0.123x | 23 | 30.4% | FAIL | -12.86% | -0.455x | 0.03% | -0.09% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.7,slow0.05)` | **FAIL** | -2.88% | 10.66% | -0.270x | 28 | 35.7% | FAIL | 7.19% | 0.254x | -0.02% | 0.43% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.08)` | **FAIL** | -6.22% | 10.66% | -0.584x | 25 | 32.0% | FAIL | -19.25% | -0.680x | -0.09% | -0.29% | Y | Y | Y | Y |  |
| BTCUSDT | `mama-fama-cross` | 4h | `mode_b|(fast0.5,slow0.05,rising)` | **FAIL** | -1.31% | 10.66% | -0.123x | 23 | 30.4% | FAIL | -12.86% | -0.455x | 0.03% | -0.09% | Y | Y | Y | Y |  |
| BTCUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n7,fac3.0)` | **FAIL** | -2.87% | 11.09% | -0.259x | 25 | 32.0% | FAIL | -41.18% | -1.416x | -0.02% | -1.05% | Y | Y | Y | Y |  |
| BTCUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac2.0)` | **FAIL** | -17.53% | 11.09% | -1.580x | 89 | 36.0% | FAIL | -64.11% | -2.205x | -0.42% | -2.31% | Y | Y | Y | Y |  |
| BTCUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac3.0)` | **FAIL** | -9.75% | 11.09% | -0.878x | 32 | 28.1% | FAIL | -37.04% | -1.274x | -0.20% | -0.88% | Y | Y | Y | Y |  |
| BTCUSDT | `wilder-volatility-system-flip` | 1h | `mode_b|(n7,fac3.0,atrpr50)` | **FAIL** | -11.72% | 11.09% | -1.057x | 21 | 33.3% | FAIL | -38.76% | -1.333x | -0.29% | -1.01% | Y | Y | Y | Y |  |
| BTCUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n7,fac3.0)` | **FAIL** | 9.64% | 10.66% | 0.904x | 6 | 50.0% | FAIL | -14.80% | -0.523x | 0.29% | -0.15% | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=6 in thin band [6..10]); Near-miss 6m (0.90x B&H) |
| BTCUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac2.0)` | **FAIL** | -0.95% | 10.66% | -0.089x | 23 | 34.8% | FAIL | -13.70% | -0.484x | 0.04% | -0.17% | Y | Y | Y | Y |  |
| BTCUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac3.0)` | **FAIL** | -1.86% | 10.66% | -0.174x | 8 | 37.5% | FAIL | -22.16% | -0.783x | 0.00% | -0.36% | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
| BTCUSDT | `wilder-volatility-system-flip` | 4h | `mode_b|(n7,fac3.0,atrpr50)` | **FAIL** | 6.87% | 10.66% | 0.645x | 4 | 50.0% | FAIL | 21.17% | 0.748x | 0.20% | 0.65% | Y | Y | Y | Y | TINY-N KILL (BTC 6m n=4 <= 5) |
| BTCUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.0,q9)` | **FAIL** | -16.50% | 11.09% | -1.487x | 107 | 29.0% | FAIL | -67.88% | -2.334x | -0.38% | -2.57% | Y | Y | Y | Y |  |
| BTCUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p14,x1.0,q9)` | **FAIL** | 13.25% | 11.09% | 1.194x | 74 | 40.5% | FAIL | -54.84% | -1.886x | 0.38% | -1.72% | Y | Y | Y | Y | Near-miss 6m (1.19x B&H) |
| BTCUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.5,q14)` | **FAIL** | -16.67% | 11.09% | -1.503x | 117 | 29.1% | FAIL | -71.07% | -2.444x | -0.39% | -2.81% | Y | Y | Y | Y |  |
| BTCUSDT | `chande-kroll-stop-flip` | 1h | `mode_b|(p10,x1.0,q9,wpr50)` | **FAIL** | -16.77% | 11.09% | -1.512x | 52 | 26.9% | FAIL | -32.69% | -1.124x | -0.43% | -0.85% | Y | Y | Y | Y |  |
| BTCUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.0,q9)` | **FAIL** | -5.71% | 10.66% | -0.536x | 28 | 32.1% | FAIL | -13.02% | -0.460x | -0.07% | -0.11% | Y | Y | Y | Y |  |
| BTCUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p14,x1.0,q9)` | **FAIL** | 1.38% | 10.66% | 0.130x | 23 | 39.1% | FAIL | 2.71% | 0.096x | 0.11% | 0.37% | Y | Y | Y | Y |  |
| BTCUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.5,q14)` | **FAIL** | -5.48% | 10.66% | -0.514x | 28 | 32.1% | FAIL | -25.92% | -0.916x | -0.06% | -0.44% | Y | Y | Y | Y |  |
| BTCUSDT | `chande-kroll-stop-flip` | 4h | `mode_b|(p10,x1.0,q9,wpr50)` | **FAIL** | 6.38% | 10.66% | 0.598x | 9 | 33.3% | FAIL | 11.53% | 0.408x | 0.21% | 0.42% | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=9 in thin band [6..10]) |
| ETHUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi21,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf8,wt5.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 1h | `mode_b|(rsi14,sf5,wt4.236,f50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.7,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.08)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 1h | `mode_b|(fast0.5,slow0.05,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n7,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac2.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 1h | `mode_b|(n7,fac3.0,atrpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p14,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.5,q14)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 1h | `mode_b|(p10,x1.0,q9,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi21,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf8,wt5.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `qqe-trailing-cross` | 4h | `mode_b|(rsi14,sf5,wt4.236,f50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.7,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.08)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `mama-fama-cross` | 4h | `mode_b|(fast0.5,slow0.05,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n7,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac2.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `wilder-volatility-system-flip` | 4h | `mode_b|(n7,fac3.0,atrpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p14,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.5,q14)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chande-kroll-stop-flip` | 4h | `mode_b|(p10,x1.0,q9,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi21,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf8,wt5.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 1h | `mode_b|(rsi14,sf5,wt4.236,f50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.7,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.08)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 1h | `mode_b|(fast0.5,slow0.05,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n7,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac2.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 1h | `mode_b|(n7,fac3.0,atrpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p14,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.5,q14)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 1h | `mode_b|(p10,x1.0,q9,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi21,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf8,wt5.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `qqe-trailing-cross` | 4h | `mode_b|(rsi14,sf5,wt4.236,f50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.7,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.08)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `mama-fama-cross` | 4h | `mode_b|(fast0.5,slow0.05,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n7,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac2.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `wilder-volatility-system-flip` | 4h | `mode_b|(n7,fac3.0,atrpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p14,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.5,q14)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chande-kroll-stop-flip` | 4h | `mode_b|(p10,x1.0,q9,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi21,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 1h | `mode_a|(rsi14,sf8,wt5.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 1h | `mode_b|(rsi14,sf5,wt4.236,f50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.7,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 1h | `mode_a|(fast0.5,slow0.08)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 1h | `mode_b|(fast0.5,slow0.05,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n7,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac2.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 1h | `mode_a|(n9,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 1h | `mode_b|(n7,fac3.0,atrpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p14,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 1h | `mode_a|(p10,x1.5,q14)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 1h | `mode_b|(p10,x1.0,q9,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi21,sf5,wt4.236)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 4h | `mode_a|(rsi14,sf8,wt5.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `qqe-trailing-cross` | 4h | `mode_b|(rsi14,sf5,wt4.236,f50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.7,slow0.05)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 4h | `mode_a|(fast0.5,slow0.08)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `mama-fama-cross` | 4h | `mode_b|(fast0.5,slow0.05,rising)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n7,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac2.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 4h | `mode_a|(n9,fac3.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `wilder-volatility-system-flip` | 4h | `mode_b|(n7,fac3.0,atrpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p14,x1.0,q9)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 4h | `mode_a|(p10,x1.5,q14)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chande-kroll-stop-flip` | 4h | `mode_b|(p10,x1.0,q9,wpr50)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
