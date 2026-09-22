# stage9-dual-sol-bnb-v1 scoreboard (DUAL SOL+BNB survival + density: SOL + BNB)

Generated (UTC): 2026-09-18T01:35:07.973380+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-8 IDs, no ER-gate clones, no Super Passband/RWI/Reverse EMA/PGO, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Psychological Line (`psy-midline-fifty-cross-v1`):** 100*SMA(up,N) midline-50 cross. N in {10,12,13,20}; prefer 12. Mode A 50-cross; Mode B 25-cross.
- **Disparity Index (`disparity-sma-zero-cross-v1`):** 100*(close-SMA)/SMA zero-cross. N in {10,14,20,30}; prefer 20. Mode A zero-cross; Mode B -ext reclaim.
- **WaveTrend Oscillator (`wavetrend-wt1-wt2-cross-v1`):** LazyBear WT with 0.015 factor. (10,21,4) default; sweep (8,21,4),(12,21,4),(10,14,3). Mode A WT1xWT2 cross; Mode B OS-gated cross.
- **Relative Momentum Index (`rmi-midline-fifty-cross-v1`):** Altman RMI with m>=3 hard. (20,5) default; (14,3),(21,5). Mode A 50-cross; Mode B 30-cross.
- **Acceleration Bands (`accel-bands-break-inside-exit-v1`):** Headley range envelope break + inside exit. N in {14,20,30}; k in {3,4}; prefer N=20 k=4. Mode A single-bar; Mode B two-bar.

## PASS_6m cells (LEAD)

_none_

## All Scored Cells by Strategy

### `psy-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | 141 | 28.4% | -29.87% | +9.49% | -3.148× | FAIL | 567 | 30.0% | -82.78% | +27.09% | -3.056× | FAIL | -0.82% | -4.05% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | 156 | 25.6% | -37.49% | +9.49% | -3.951× | FAIL | 634 | 29.3% | -86.33% | +27.09% | -3.187× | FAIL | -1.10% | -4.58% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N13)` | `Y` | `Y` | `—` | 282 | 18.8% | -58.41% | +9.49% | -6.156× | FAIL | 1094 | 20.7% | -96.41% | +27.09% | -3.559× | FAIL | -2.11% | -7.72% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 103 | 28.2% | -26.78% | +9.49% | -2.823× | FAIL | 429 | 31.7% | -60.38% | +27.09% | -2.229× | FAIL | -0.71% | -2.05% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | 48 | 25.0% | -20.00% | +9.49% | -2.108× | FAIL | 194 | 33.0% | -49.21% | +27.09% | -1.817× | FAIL | -0.54% | -1.56% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | 38 | 26.3% | -17.16% | +10.09% | -1.700× | FAIL | 152 | 32.9% | -25.20% | +27.43% | -0.919× | FAIL | -0.41% | -0.48% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | 40 | 32.5% | -4.14% | +10.09% | -0.411× | FAIL | 155 | 34.2% | -12.89% | +27.43% | -0.470× | FAIL | -0.05% | -0.14% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N13)` | `Y` | `Y` | `—` | 61 | 23.0% | -15.21% | +10.09% | -1.508× | FAIL | 261 | 25.3% | -39.87% | +27.43% | -1.453× | FAIL | -0.35% | -1.02% | — |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 30 | 40.0% | +9.31% | +10.09% | 0.922× | FAIL | 112 | 40.2% | -6.57% | +27.43% | -0.240× | FAIL | +0.30% | +0.06% | Near-miss 6m (0.92x B&H) |
| `BTCUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | 8 | 37.5% | -15.48% | +10.09% | -1.534× | FAIL | 40 | 42.5% | -19.96% | +27.43% | -0.728× | FAIL | -0.40% | -0.49% | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
### `disparity-sma-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 261 | 18.0% | -57.41% | +9.49% | -6.051× | FAIL | 1042 | 17.5% | -95.36% | +27.09% | -3.520× | FAIL | -2.04% | -7.16% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | 402 | 16.9% | -72.11% | +9.49% | -7.600× | FAIL | 1595 | 19.9% | -99.09% | +27.09% | -3.658× | FAIL | -3.07% | -10.87% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | 347 | 16.1% | -66.13% | +9.49% | -6.970× | FAIL | 1330 | 17.5% | -98.25% | +27.09% | -3.627× | FAIL | -2.60% | -9.39% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N30)` | `Y` | `Y` | `—` | 212 | 17.9% | -46.60% | +9.49% | -4.911× | FAIL | 862 | 16.4% | -92.56% | +27.09% | -3.417× | FAIL | -1.49% | -6.07% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | 21 | 19.0% | -23.84% | +9.49% | -2.512× | FAIL | 123 | 39.8% | -27.53% | +27.09% | -1.016× | FAIL | -0.66% | -0.72% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 55 | 21.8% | -12.50% | +10.09% | -1.238× | FAIL | 242 | 19.8% | -45.75% | +27.43% | -1.668× | FAIL | -0.26% | -1.24% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | 100 | 20.0% | -27.70% | +10.09% | -2.745× | FAIL | 385 | 23.1% | -61.78% | +27.43% | -2.252× | FAIL | -0.75% | -2.15% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | 85 | 18.8% | -17.20% | +10.09% | -1.704× | FAIL | 313 | 21.4% | -57.14% | +27.43% | -2.083× | FAIL | -0.41% | -1.87% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N30)` | `Y` | `Y` | `—` | 52 | 15.4% | -14.49% | +10.09% | -1.436× | FAIL | 215 | 16.7% | -51.14% | +27.43% | -1.864× | FAIL | -0.31% | -1.46% | — |
| `BTCUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | 20 | 45.0% | +4.84% | +10.09% | 0.480× | FAIL | 78 | 44.9% | +26.77% | +27.43% | 0.976× | FAIL | +0.13% | +0.81% | — |
### `wavetrend-wt1-wt2-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | 330 | 22.7% | -67.17% | +9.49% | -7.079× | FAIL | 1290 | 25.0% | -97.64% | +27.09% | -3.605× | FAIL | -2.70% | -8.72% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | 364 | 22.8% | -70.51% | +9.49% | -7.431× | FAIL | 1406 | 24.0% | -98.31% | +27.09% | -3.629× | FAIL | -2.96% | -9.48% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | 313 | 23.3% | -65.87% | +9.49% | -6.942× | FAIL | 1221 | 25.4% | -97.22% | +27.09% | -3.589× | FAIL | -2.61% | -8.34% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | 419 | 21.7% | -74.29% | +9.49% | -7.830× | FAIL | 1627 | 24.3% | -99.05% | +27.09% | -3.656× | FAIL | -3.30% | -11.13% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | 47 | 27.7% | -17.35% | +9.49% | -1.829× | FAIL | 190 | 31.1% | -43.63% | +27.09% | -1.611× | FAIL | -0.47% | -1.35% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | 81 | 33.3% | -25.38% | +10.09% | -2.515× | FAIL | 319 | 33.5% | -49.10% | +27.43% | -1.790× | FAIL | -0.69% | -1.47% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | 87 | 31.0% | -30.85% | +10.09% | -3.058× | FAIL | 340 | 32.6% | -54.14% | +27.43% | -1.974× | FAIL | -0.88% | -1.72% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | 79 | 34.2% | -30.55% | +10.09% | -3.028× | FAIL | 295 | 35.3% | -43.81% | +27.43% | -1.597× | FAIL | -0.87% | -1.22% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | 100 | 35.0% | -25.06% | +10.09% | -2.484× | FAIL | 397 | 32.0% | -50.06% | +27.43% | -1.825× | FAIL | -0.69% | -1.51% | — |
| `BTCUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | 8 | 25.0% | -8.46% | +10.09% | -0.838× | FAIL | 42 | 33.3% | -12.95% | +27.43% | -0.472× | FAIL | -0.21% | -0.31% | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
### `rmi-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | 85 | 24.7% | -11.94% | +9.49% | -1.259× | FAIL | 356 | 24.4% | -57.51% | +27.09% | -2.123× | FAIL | -0.26% | -1.84% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | 153 | 20.9% | -35.69% | +9.49% | -3.762× | FAIL | 589 | 22.2% | -80.24% | +27.09% | -2.962× | FAIL | -1.04% | -3.76% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | 83 | 25.3% | -9.67% | +9.49% | -1.019× | FAIL | 350 | 24.3% | -59.05% | +27.09% | -2.180× | FAIL | -0.19% | -1.93% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | 59 | 32.2% | -3.48% | +9.49% | -0.367× | FAIL | 231 | 30.7% | -33.47% | +27.09% | -1.235× | FAIL | -0.07% | -0.78% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | 25 | 44.0% | -0.87% | +10.09% | -0.086× | FAIL | 92 | 33.7% | -13.79% | +27.43% | -0.503× | FAIL | +0.04% | -0.08% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | 32 | 31.2% | -3.54% | +10.09% | -0.350× | FAIL | 135 | 25.9% | -5.46% | +27.43% | -0.199× | FAIL | -0.02% | +0.15% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | 24 | 41.7% | +1.03% | +10.09% | 0.102× | FAIL | 87 | 33.3% | -9.98% | +27.43% | -0.364× | FAIL | +0.08% | -0.02% | — |
| `BTCUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | 18 | 27.8% | +9.70% | +10.09% | 0.961× | FAIL | 62 | 30.6% | -14.49% | +27.43% | -0.528× | FAIL | +0.29% | -0.28% | Near-miss 6m (0.96x B&H) |
### `accel-bands-break-inside-exit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | 73 | 21.9% | -15.25% | +9.49% | -1.608× | FAIL | 331 | 17.5% | -68.13% | +27.09% | -2.515× | FAIL | -0.40% | -2.79% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | 114 | 15.8% | -19.82% | +9.49% | -2.089× | FAIL | 479 | 18.2% | -75.26% | +27.09% | -2.778× | FAIL | -0.53% | -3.38% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | 52 | 17.3% | -12.60% | +9.49% | -1.328× | FAIL | 249 | 18.9% | -56.64% | +27.09% | -2.091× | FAIL | -0.33% | -2.05% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | 87 | 18.4% | -15.16% | +9.49% | -1.598× | FAIL | 377 | 16.4% | -67.74% | +27.09% | -2.501× | FAIL | -0.37% | -2.72% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | 43 | 18.6% | -9.97% | +9.49% | -1.051× | FAIL | 201 | 18.4% | -57.23% | +27.09% | -2.113× | FAIL | -0.26% | -2.08% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | 17 | 11.8% | -3.13% | +10.09% | -0.310× | FAIL | 84 | 22.6% | -20.08% | +27.43% | -0.732× | FAIL | -0.06% | -0.50% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | 28 | 3.6% | -11.23% | +10.09% | -1.113× | FAIL | 118 | 18.6% | -28.62% | +27.43% | -1.043× | FAIL | -0.28% | -0.77% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | 15 | 20.0% | +0.79% | +10.09% | 0.079× | FAIL | 66 | 27.3% | -9.74% | +27.43% | -0.355× | FAIL | +0.04% | -0.22% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | 26 | 3.8% | -6.23% | +10.09% | -0.618× | FAIL | 84 | 25.0% | -1.41% | +27.43% | -0.051× | FAIL | -0.12% | +0.07% | — |
| `BTCUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | 10 | 20.0% | +5.10% | +10.09% | 0.506× | FAIL | 48 | 29.2% | +3.03% | +27.43% | 0.111× | FAIL | +0.14% | +0.12% | THIN-N FLAG (BTC 6m n=10 in thin band [6..10]) |
### `psy-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N13)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N13)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `disparity-sma-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `wavetrend-wt1-wt2-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rmi-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `accel-bands-break-inside-exit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `psy-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N13)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N13)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `disparity-sma-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `wavetrend-wt1-wt2-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rmi-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `accel-bands-break-inside-exit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `psy-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N13)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `1h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N13)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `psy-midline-fifty-cross-v1` | `4h` | `mode_b|(N12,os25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `disparity-sma-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_a|(N30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `1h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_a|(N30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `disparity-sma-zero-cross-v1` | `4h` | `mode_b|(N20,ext2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `wavetrend-wt1-wt2-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `1h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(8,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(12,21,4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_a|(10,14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wavetrend-wt1-wt2-cross-v1` | `4h` | `mode_b|(10,21,4,os53)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rmi-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `1h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(20,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(14,3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_a|(21,5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rmi-midline-fifty-cross-v1` | `4h` | `mode_b|(20,5,os30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `accel-bands-break-inside-exit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `1h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N20,k3.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N14,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_a|(N30,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `accel-bands-break-inside-exit-v1` | `4h` | `mode_b|(N20,k4.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
