# Scoreboard: stage25-dual-sol-bnb-v1

**Generated:** 2026-09-18 09:05:52 UTC
**Status:** Research / Optimise Only — LIVE FROZEN.
**Design Bias:** BTC LEAD PRIMARY — push past Chande-Kroll ~1.194x / Kirshenbaum ~1.113x without over-damp. Denser n >> 9. Keep ETH/SOL/BNB lessons. EXIT stage24 Guppy-CBL / Kirshenbaum / IMI / Williams-AD. Identical dual params.

## Summary
- Total Scored Cells: 33
- Total Pruned/Skipped Cells: 95
- Total PASS_6m: 1

## PASS_6m Promoted Candidates
| Symbol | Strategy | TF | Mode/Params | 6m Ret% | 6m B&H% | xB&H | n_6m | WR% | MaxDD% | Smoke / Retention |
|--------|----------|----|-------------|---------|---------|------|------|-----|--------|-------------------|
| BTCUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L30,W10)` | 18.98% | 11.25% | 1.687x | 8 | 37.5% | 10.69% | — |

## Full Ladder Results

| Symbol | Strategy | TF | Mode/Params | 6m Gate | 6m Ret% | xB&H | n_6m | Full Ret% | xB&H Full | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Notes |
|--------|----------|----|-------------|---------|---------|------|------|-----------|-----------|-----------|-----------|-----------|-----------|-------|
| BTCUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len7)` | FAIL | -33.53% | -2.945x | 131 | -74.70% | -2.495x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len5)` | FAIL | -41.38% | -3.635x | 177 | -85.96% | -2.872x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len9)` | FAIL | -24.01% | -2.109x | 100 | -55.69% | -1.860x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len14)` | FAIL | -3.01% | -0.265x | 65 | -48.05% | -1.605x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len7)` | FAIL | 2.65% | 0.236x | 29 | -6.35% | -0.222x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len5)` | FAIL | 0.81% | 0.072x | 38 | -30.27% | -1.059x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len9)` | FAIL | -7.24% | -0.644x | 26 | -11.10% | -0.388x | Y | Y | Y | Y | — |
| BTCUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len14)` | FAIL | 0.95% | 0.084x | 17 | -21.77% | -0.762x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W10)` | FAIL | -9.23% | -0.811x | 70 | -46.25% | -1.545x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L14,W5)` | FAIL | -15.01% | -1.319x | 92 | -68.35% | -2.283x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W14)` | FAIL | -11.91% | -1.047x | 66 | -45.43% | -1.518x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L30,W10)` | FAIL | -4.90% | -0.430x | 49 | -19.17% | -0.641x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W10)` | FAIL | 2.63% | 0.234x | 17 | -16.06% | -0.562x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L14,W5)` | FAIL | 0.67% | 0.060x | 26 | -1.68% | -0.059x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W14)` | FAIL | 6.97% | 0.619x | 16 | -15.18% | -0.531x | Y | Y | Y | Y | — |
| BTCUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L30,W10)` | PASS | 18.98% | 1.687x | 8 | 2.75% | 0.096x | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
| BTCUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir1)` | FAIL | -61.20% | -5.375x | 308 | -97.37% | -3.253x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 1h | `mode_a|(n10,dir1)` | FAIL | -59.81% | -5.254x | 341 | -97.10% | -3.244x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 1h | `mode_a|(n20,dir1)` | FAIL | -58.54% | -5.142x | 315 | -97.40% | -3.254x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir3)` | FAIL | -61.97% | -5.444x | 316 | -97.74% | -3.265x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir1)` | FAIL | -37.06% | -3.294x | 102 | -70.30% | -2.460x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 4h | `mode_a|(n10,dir1)` | FAIL | -30.98% | -2.753x | 93 | -70.89% | -2.481x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 4h | `mode_a|(n20,dir1)` | FAIL | -24.62% | -2.188x | 95 | -62.71% | -2.195x | Y | Y | Y | Y | — |
| BTCUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir3)` | FAIL | -27.71% | -2.463x | 99 | -50.16% | -1.756x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.0)` | FAIL | -72.61% | -6.378x | 420 | -99.60% | -3.327x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema14,k3.0)` | FAIL | -73.83% | -6.485x | 440 | -99.64% | -3.329x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema20,k2.5)` | FAIL | -73.50% | -6.456x | 429 | -99.61% | -3.328x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.5)` | FAIL | -72.61% | -6.378x | 420 | -99.60% | -3.327x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.0)` | FAIL | -11.28% | -1.002x | 106 | -62.16% | -2.176x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema14,k3.0)` | FAIL | -12.14% | -1.079x | 112 | -71.15% | -2.490x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema20,k2.5)` | FAIL | -11.28% | -1.002x | 106 | -65.87% | -2.305x | Y | Y | Y | Y | — |
| BTCUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.5)` | FAIL | -11.28% | -1.002x | 106 | -62.16% | -2.176x | Y | Y | Y | Y | — |
| ETHUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len7)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len9)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len7)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len9)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L14,W5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L30,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L14,W5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L30,W10)` | FAIL | 17.87% | 1.085x | 10 | -30.15% | -4.535x | Y | Y | Y | Y | Near-miss 6m (1.08x B&H); ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 1h | `mode_a|(n10,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 1h | `mode_a|(n20,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir3)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 4h | `mode_a|(n10,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 4h | `mode_a|(n20,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir3)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema14,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema20,k2.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema14,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema20,k2.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len7)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len9)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len7)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len9)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L14,W5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L30,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L14,W5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L30,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 1h | `mode_a|(n10,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 1h | `mode_a|(n20,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir3)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 4h | `mode_a|(n10,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 4h | `mode_a|(n20,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir3)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema14,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema20,k2.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema14,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema20,k2.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len7)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len9)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 1h | `mode_a|(len14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len7)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len9)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ehlers-dsp-zero-cross` | 4h | `mode_a|(len14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L14,W5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L20,W14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 1h | `mode_a|(L30,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L14,W5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L20,W14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `nhnl-oscillator-zero` | 4h | `mode_a|(L30,W10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 1h | `mode_a|(n10,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 1h | `mode_a|(n20,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 1h | `mode_a|(n14,dir3)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 4h | `mode_a|(n10,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 4h | `mode_a|(n20,dir1)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `volume-roc-dir` | 4h | `mode_a|(n14,dir3)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema14,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema20,k2.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 1h | `mode_a|(ema22,k3.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema14,k3.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema20,k2.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `elder-thermometer-cool-dir` | 4h | `mode_a|(ema22,k3.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |

## Notes & Methodology
- **Harness:** Path B event-driven closed-bar backtest (`process_orders_on_close = True`).
- **Fees / Slippage:** 0.10% fee per side + 5 bps adverse slippage.
- **Gate Sizing:** Mode A Gate uses 100% equity; Ops uses 2.5% equity.
- **LEAD Criteria:** 6m Mode-A return >= 1.2x Buy & Hold return AND n > 5 on BTC.
- **Tiny-n Policy:** BTC Mode-A n <= 5 triggers an immediate TINY-N KILL.
- **Thin-n Flag:** BTC Mode-A n in [6..10] flagged as THIN-N.
- **Dual Survival:** Identical parameter set tested across BTC -> ETH -> SOL -> BNB ladder; never retuned per coin.
- **Status:** RESEARCH / OPTIMISE ONLY — LIVE FROZEN.
