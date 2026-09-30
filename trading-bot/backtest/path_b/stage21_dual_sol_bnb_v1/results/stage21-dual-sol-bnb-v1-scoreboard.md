# Scoreboard: stage21-dual-sol-bnb-v1

**Date (UTC):** 2026-09-18 06:38:43
**Track:** Track 1 Path B (Track 2 Discord OFF-LIMITS)
**Status:** RESEARCH / OPTIMISE ONLY — LIVE frozen
**Design bias:** BTC LEAD PRIMARY without over-damp (stage12/15/18/20 rhyme). Denser n >> 9. Stop-ladder: BTC -> ETH -> SOL -> BNB.
**Redundancy Rule Execution:** Strategy 4 (`parkinson-vol-expansion-dir`) DROPPED before ladder scoring due to BTC-smoke redundancy with Strategy 1 (`chaikin-volatility-dir`) (>75% overlap, identical fee chop).

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
| BTCUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc10,dir1)` | **FAIL** | -89.27% | 11.57% | -7.714x | 816 | 17.2% | FAIL | -99.99% | -3.421x | -5.40% | -20.63% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema14,roc10,dir1)` | **FAIL** | -89.44% | 11.57% | -7.729x | 812 | 17.1% | FAIL | -99.99% | -3.421x | -5.44% | -20.68% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc5,dir1)` | **FAIL** | -88.73% | 11.57% | -7.668x | 786 | 17.6% | FAIL | -99.99% | -3.421x | -5.29% | -20.65% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 1h | `mode_b|(ema10,roc10,dir1,cv0)` | **FAIL** | -69.06% | 11.57% | -5.967x | 452 | 17.7% | FAIL | -99.45% | -3.403x | -2.87% | -12.12% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc10,dir1)` | **FAIL** | -56.36% | 10.12% | -5.569x | 193 | 19.2% | FAIL | -93.14% | -3.291x | -2.03% | -6.35% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema14,roc10,dir1)` | **FAIL** | -57.63% | 10.12% | -5.695x | 195 | 19.5% | FAIL | -93.19% | -3.293x | -2.11% | -6.37% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc5,dir1)` | **FAIL** | -61.93% | 10.12% | -6.120x | 211 | 17.5% | FAIL | -90.39% | -3.194x | -2.37% | -5.56% | Y | Y | Y | Y | — |
| BTCUSDT | `chaikin-volatility-dir` | 4h | `mode_b|(ema10,roc10,dir1,cv0)` | **FAIL** | -35.69% | 10.12% | -3.527x | 102 | 22.5% | FAIL | -77.61% | -2.742x | -1.08% | -3.59% | Y | Y | Y | Y | — |
| BTCUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf1)` | **FAIL** | -35.81% | 11.57% | -3.094x | 118 | 29.7% | FAIL | -76.29% | -2.610x | -1.06% | -3.34% | Y | Y | Y | Y | — |
| BTCUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.6,conf1)` | **FAIL** | -35.17% | 11.57% | -3.039x | 121 | 28.1% | FAIL | -78.65% | -2.691x | -1.04% | -3.62% | Y | Y | Y | Y | — |
| BTCUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf2)` | **FAIL** | -1.03% | 11.57% | -0.089x | 3 | 33.3% | FAIL | -6.90% | -0.236x | -0.02% | -0.18% | Y | Y | Y | Y | TINY-N KILL (BTC 6m n=3 <= 5) |
| BTCUSDT | `outside-bar-polarity` | 1h | `mode_b|(mid0.5,conf1,follth)` | **FAIL** | -33.46% | 11.57% | -2.891x | 86 | 24.4% | FAIL | -67.37% | -2.305x | -0.98% | -2.62% | Y | Y | Y | Y | — |
| BTCUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf1)` | **FAIL** | -13.06% | 10.12% | -1.290x | 38 | 34.2% | FAIL | -37.64% | -1.330x | -0.22% | -0.89% | Y | Y | Y | Y | — |
| BTCUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.6,conf1)` | **FAIL** | -20.62% | 10.12% | -2.038x | 38 | 31.6% | FAIL | -48.84% | -1.726x | -0.47% | -1.41% | Y | Y | Y | Y | — |
| BTCUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf2)` | **FAIL** | -1.18% | 10.12% | -0.117x | 2 | 50.0% | FAIL | -1.88% | -0.066x | -0.03% | -0.05% | Y | Y | Y | Y | TINY-N KILL (BTC 6m n=2 <= 5) |
| BTCUSDT | `outside-bar-polarity` | 4h | `mode_b|(mid0.5,conf1,follth)` | **FAIL** | -0.36% | 10.12% | -0.035x | 29 | 34.5% | FAIL | -22.25% | -0.786x | 0.06% | -0.46% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui14,dir1)` | **FAIL** | -87.81% | 11.57% | -7.588x | 702 | 17.7% | FAIL | -99.98% | -3.421x | -5.10% | -19.16% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui10,dir1)` | **FAIL** | -87.23% | 11.57% | -7.538x | 740 | 17.8% | FAIL | -99.98% | -3.421x | -4.98% | -19.36% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui20,dir1)` | **FAIL** | -86.41% | 11.57% | -7.466x | 687 | 15.4% | FAIL | -99.98% | -3.421x | -4.86% | -18.68% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 1h | `mode_b|(ui14,dir1,sma5)` | **FAIL** | -31.85% | 11.57% | -2.752x | 132 | 14.4% | FAIL | -81.65% | -2.794x | -0.95% | -4.13% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui14,dir1)` | **FAIL** | -47.55% | 10.12% | -4.698x | 183 | 21.9% | FAIL | -86.91% | -3.071x | -1.58% | -4.84% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui10,dir1)` | **FAIL** | -49.96% | 10.12% | -4.937x | 193 | 20.2% | FAIL | -88.85% | -3.140x | -1.69% | -5.24% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui20,dir1)` | **FAIL** | -44.84% | 10.12% | -4.431x | 175 | 17.7% | FAIL | -89.45% | -3.161x | -1.45% | -5.34% | Y | Y | Y | Y | — |
| BTCUSDT | `ulcer-index-recover-dir` | 4h | `mode_b|(ui14,dir1,sma5)` | **FAIL** | -8.33% | 10.12% | -0.823x | 29 | 34.5% | FAIL | -31.65% | -1.118x | -0.22% | -0.93% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel5,k0.0)` | **FAIL** | -47.79% | 11.57% | -4.129x | 179 | 25.7% | FAIL | -83.50% | -2.857x | -1.55% | -4.20% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel3,k0.0)` | **FAIL** | -42.63% | 11.57% | -3.684x | 149 | 26.2% | FAIL | -78.98% | -2.703x | -1.32% | -3.66% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel8,k0.0)` | **FAIL** | -45.90% | 11.57% | -3.966x | 189 | 27.0% | FAIL | -85.79% | -2.935x | -1.46% | -4.54% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 1h | `mode_b|(cancel5,k0.5)` | **FAIL** | -47.73% | 11.57% | -4.125x | 175 | 25.1% | FAIL | -83.06% | -2.842x | -1.54% | -4.13% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel5,k0.0)` | **FAIL** | -7.06% | 10.12% | -0.698x | 49 | 38.8% | FAIL | -38.51% | -1.361x | -0.13% | -1.01% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel3,k0.0)` | **FAIL** | -6.08% | 10.12% | -0.601x | 39 | 41.0% | FAIL | -24.01% | -0.848x | -0.11% | -0.51% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel8,k0.0)` | **FAIL** | -3.83% | 10.12% | -0.378x | 49 | 38.8% | FAIL | -29.25% | -1.034x | -0.04% | -0.66% | Y | Y | Y | Y | — |
| BTCUSDT | `inside-bar-breakout` | 4h | `mode_b|(cancel5,k0.5)` | **FAIL** | -8.52% | 10.12% | -0.841x | 46 | 39.1% | FAIL | -40.05% | -1.415x | -0.17% | -1.07% | Y | Y | Y | Y | — |
| ETHUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema14,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc5,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 1h | `mode_b|(ema10,roc10,dir1,cv0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema14,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc5,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `chaikin-volatility-dir` | 4h | `mode_b|(ema10,roc10,dir1,cv0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.6,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf2)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 1h | `mode_b|(mid0.5,conf1,follth)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.6,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf2)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `outside-bar-polarity` | 4h | `mode_b|(mid0.5,conf1,follth)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui14,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui20,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 1h | `mode_b|(ui14,dir1,sma5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui14,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui20,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ulcer-index-recover-dir` | 4h | `mode_b|(ui14,dir1,sma5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel5,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel3,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel8,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 1h | `mode_b|(cancel5,k0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel5,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel3,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel8,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `inside-bar-breakout` | 4h | `mode_b|(cancel5,k0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema14,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc5,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 1h | `mode_b|(ema10,roc10,dir1,cv0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema14,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc5,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `chaikin-volatility-dir` | 4h | `mode_b|(ema10,roc10,dir1,cv0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.6,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf2)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 1h | `mode_b|(mid0.5,conf1,follth)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.6,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf2)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `outside-bar-polarity` | 4h | `mode_b|(mid0.5,conf1,follth)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui14,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui20,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 1h | `mode_b|(ui14,dir1,sma5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui14,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui20,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ulcer-index-recover-dir` | 4h | `mode_b|(ui14,dir1,sma5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel5,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel3,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel8,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 1h | `mode_b|(cancel5,k0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel5,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel3,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel8,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `inside-bar-breakout` | 4h | `mode_b|(cancel5,k0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema14,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 1h | `mode_a|(ema10,roc5,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 1h | `mode_b|(ema10,roc10,dir1,cv0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema14,roc10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 4h | `mode_a|(ema10,roc5,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `chaikin-volatility-dir` | 4h | `mode_b|(ema10,roc10,dir1,cv0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.6,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 1h | `mode_a|(mid0.5,conf2)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 1h | `mode_b|(mid0.5,conf1,follth)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.6,conf1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 4h | `mode_a|(mid0.5,conf2)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `outside-bar-polarity` | 4h | `mode_b|(mid0.5,conf1,follth)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui14,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 1h | `mode_a|(ui20,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 1h | `mode_b|(ui14,dir1,sma5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui14,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui10,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 4h | `mode_a|(ui20,dir1)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ulcer-index-recover-dir` | 4h | `mode_b|(ui14,dir1,sma5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel5,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel3,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 1h | `mode_a|(cancel8,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 1h | `mode_b|(cancel5,k0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel5,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel3,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 4h | `mode_a|(cancel8,k0.0)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `inside-bar-breakout` | 4h | `mode_b|(cancel5,k0.5)` | PRUNED | — | — | — | — | — | PRUNED | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |

## Methodology & Governance Notes
- **Closed-bar fills only** (`process_orders_on_close=true`).
- **Identical parameters across all 4 coins** (no per-coin retuning).
- **Stop-ladder hierarchy**: BTC -> ETH -> SOL -> BNB. Progression strictly requires Mode-A 6m return >= 1.2x B&H and trade count n > 5 on BTC.
- **Tiny-n Policy**: BTC 6m n <= 5 fails automatically; n in [6..10] flagged as thin.
- **Costs**: 0.10%/side fee + 5 bps adverse slippage applied to every trade.
