# Scoreboard: stage24-dual-sol-bnb-v1

**Generated:** 2026-09-18 07:56:44 UTC
**Status:** Research / Optimise Only — LIVE FROZEN.
**Design Bias:** BTC LEAD PRIMARY — push past Chande-Kroll ~1.194x near-miss without over-damp. Denser n >> 9. Keep ETH/SOL/BNB lessons. EXIT stage23 QQE/MAMA/Wilder/Chande-Kroll. Identical dual params.

## Summary
- Total Scored Cells: 32
- Total Pruned/Skipped Cells: 96
- Total PASS_6m: 0

## PASS_6m Promoted Candidates
*None. All candidates failed to clear >= 1.2x B&H on 6m or were pruned by ladder.*

## Full Ladder Results

| Symbol | Strategy | TF | Mode/Params | 6m Gate | 6m Ret% | xB&H | n_6m | Full Ret% | xB&H Full | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Notes |
|--------|----------|----|-------------|---------|---------|------|------|-----------|-----------|-----------|-----------|-----------|-----------|-------|
| BTCUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr0.0)` | **FAIL** | -48.98% | -4.415x | 187 | -89.77% | -3.087x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr1.5)` | **FAIL** | -61.01% | -5.500x | 291 | -97.34% | -3.347x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr2.0)` | **FAIL** | -54.59% | -4.921x | 244 | -93.90% | -3.229x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 1h | `mode_b|(cd3,kconf2)` | **FAIL** | -30.94% | -2.789x | 150 | -87.33% | -3.003x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr0.0)` | **FAIL** | -11.69% | -1.097x | 48 | -9.12% | -0.322x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr1.5)` | **FAIL** | -15.51% | -1.455x | 71 | -62.07% | -2.193x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr2.0)` | **FAIL** | -17.69% | -1.660x | 62 | -54.31% | -1.919x | Y | Y | Y | Y | — |
| BTCUSDT | `guppy-countback-line-flip` | 4h | `mode_b|(cd3,kconf2)` | **FAIL** | -9.98% | -0.936x | 37 | 1.95% | 0.069x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k1.75)` | **FAIL** | -17.15% | -1.546x | 101 | -71.94% | -2.474x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema30,reg20,k1.75)` | **FAIL** | -15.55% | -1.401x | 88 | -62.01% | -2.132x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k2.25)` | **FAIL** | -6.66% | -0.600x | 79 | -51.88% | -1.784x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 1h | `mode_b|(ema20,reg20,k1.75,pr50)` | **FAIL** | -9.14% | -0.823x | 54 | -53.72% | -1.847x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k1.75)` | **FAIL** | 1.29% | 0.121x | 23 | -33.74% | -1.192x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema30,reg20,k1.75)` | **FAIL** | 11.86% | 1.113x | 18 | -18.58% | -0.657x | Y | Y | Y | Y | Near-miss 6m (1.11x B&H) |
| BTCUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k2.25)` | **FAIL** | 2.63% | 0.247x | 19 | -20.26% | -0.716x | Y | Y | Y | Y | — |
| BTCUSDT | `kirshenbaum-bands-break` | 4h | `mode_b|(ema20,reg20,k1.75,pr50)` | **FAIL** | 11.16% | 1.047x | 9 | -21.79% | -0.770x | Y | Y | Y | Y | THIN-N FLAG (BTC 6m n=9 in thin band [6..10]); Near-miss 6m (1.05x B&H) |
| BTCUSDT | `imi-midline-fifty` | 1h | `mode_a|(n14)` | **FAIL** | -60.21% | -5.427x | 286 | -96.36% | -3.313x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 1h | `mode_a|(n10)` | **FAIL** | -64.66% | -5.828x | 346 | -98.26% | -3.379x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 1h | `mode_a|(n21)` | **FAIL** | -44.61% | -4.021x | 241 | -92.84% | -3.192x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 1h | `mode_b|(n14,thr55)` | **FAIL** | -17.96% | -1.619x | 104 | -63.70% | -2.190x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 4h | `mode_a|(n14)` | **FAIL** | -14.67% | -1.376x | 63 | -35.62% | -1.259x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 4h | `mode_a|(n10)` | **FAIL** | -5.56% | -0.521x | 72 | -44.97% | -1.589x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 4h | `mode_a|(n21)` | **FAIL** | -3.07% | -0.288x | 51 | -46.41% | -1.640x | Y | Y | Y | Y | — |
| BTCUSDT | `imi-midline-fifty` | 4h | `mode_b|(n14,thr55)` | **FAIL** | -0.10% | -0.010x | 24 | 9.54% | 0.337x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m21)` | **FAIL** | -65.87% | -5.937x | 305 | -98.63% | -3.392x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m14)` | **FAIL** | -75.54% | -6.809x | 393 | -99.32% | -3.415x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m34)` | **FAIL** | -52.22% | -4.707x | 235 | -93.90% | -3.229x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 1h | `mode_b|(m21,rising)` | **FAIL** | -65.87% | -5.937x | 305 | -98.63% | -3.392x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m21)` | **FAIL** | -22.39% | -2.101x | 76 | -63.46% | -2.242x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m14)` | **FAIL** | -23.82% | -2.235x | 99 | -70.50% | -2.491x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m34)` | **FAIL** | -12.96% | -1.216x | 61 | -53.23% | -1.881x | Y | Y | Y | Y | — |
| BTCUSDT | `williams-ad-sma-cross` | 4h | `mode_b|(m21,rising)` | **FAIL** | -22.39% | -2.101x | 76 | -63.46% | -2.242x | Y | Y | Y | Y | — |
| ETHUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr0.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr1.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr2.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 1h | `mode_b|(cd3,kconf2)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema30,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k2.25)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 1h | `mode_b|(ema20,reg20,k1.75,pr50)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 1h | `mode_a|(n14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 1h | `mode_a|(n10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 1h | `mode_a|(n21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 1h | `mode_b|(n14,thr55)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m34)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 1h | `mode_b|(m21,rising)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr0.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr1.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr2.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `guppy-countback-line-flip` | 4h | `mode_b|(cd3,kconf2)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema30,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k2.25)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kirshenbaum-bands-break` | 4h | `mode_b|(ema20,reg20,k1.75,pr50)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 4h | `mode_a|(n14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 4h | `mode_a|(n10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 4h | `mode_a|(n21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `imi-midline-fifty` | 4h | `mode_b|(n14,thr55)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m34)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `williams-ad-sma-cross` | 4h | `mode_b|(m21,rising)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr0.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr1.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr2.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 1h | `mode_b|(cd3,kconf2)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema30,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k2.25)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 1h | `mode_b|(ema20,reg20,k1.75,pr50)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 1h | `mode_a|(n14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 1h | `mode_a|(n10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 1h | `mode_a|(n21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 1h | `mode_b|(n14,thr55)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m34)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 1h | `mode_b|(m21,rising)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr0.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr1.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr2.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `guppy-countback-line-flip` | 4h | `mode_b|(cd3,kconf2)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema30,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k2.25)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kirshenbaum-bands-break` | 4h | `mode_b|(ema20,reg20,k1.75,pr50)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 4h | `mode_a|(n14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 4h | `mode_a|(n10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 4h | `mode_a|(n21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `imi-midline-fifty` | 4h | `mode_b|(n14,thr55)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m34)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `williams-ad-sma-cross` | 4h | `mode_b|(m21,rising)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr0.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr1.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 1h | `mode_a|(cd3,atr2.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 1h | `mode_b|(cd3,kconf2)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema30,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 1h | `mode_a|(ema20,reg20,k2.25)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 1h | `mode_b|(ema20,reg20,k1.75,pr50)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 1h | `mode_a|(n14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 1h | `mode_a|(n10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 1h | `mode_a|(n21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 1h | `mode_b|(n14,thr55)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 1h | `mode_a|(m34)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 1h | `mode_b|(m21,rising)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr0.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr1.5)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 4h | `mode_a|(cd3,atr2.0)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `guppy-countback-line-flip` | 4h | `mode_b|(cd3,kconf2)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema30,reg20,k1.75)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 4h | `mode_a|(ema20,reg20,k2.25)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kirshenbaum-bands-break` | 4h | `mode_b|(ema20,reg20,k1.75,pr50)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 4h | `mode_a|(n14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 4h | `mode_a|(n10)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 4h | `mode_a|(n21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `imi-midline-fifty` | 4h | `mode_b|(n14,thr55)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m21)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m14)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 4h | `mode_a|(m34)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `williams-ad-sma-cross` | 4h | `mode_b|(m21,rising)` | PRUNED | — | — | — | — | — | Y | Y | Y | Y | Pruned by stop-ladder (SOL PASS_6m required) |
