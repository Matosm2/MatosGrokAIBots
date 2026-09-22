# stage7-dual-sol-bnb-v1 scoreboard (DUAL SOL+BNB survival: SOL + BNB)

Generated (UTC): 2026-09-18T01:05:36.491890+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-6 IDs, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, no EMA/RSI, SMA200, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Kaufman ER Gate + SMA (`er-sma-gate-cross-v1`):** ER as path efficiency gate (0-1), fast/slow SMA cross. (Lf, Ls) in {(10,30), (9,21), (12,26)}; N in {10,14,20}; thr in {0.30, 0.35, 0.40}.
- **Ehlers Super Passband Filter (`ehlers-super-passband-rms-v1`):** S&C Jul 2016 PB oscillator with alpha=5/P. Entry PB x -RMS. (P1, P2) in {(40,60), (30,50), (20,40)}; rmsLen in {40, 50}.
- **Mike Poulos Random Walk Index (`rwi-high-low-threshold-v1`):** Displacement / (ATR*sqrt(i)). LT High > 1.0 + ST Low peak > 1.0. (S, L) in {(7,64), (5,40), (8,48)}; thr=1.0.
- **Ehlers Reverse EMA (`ehlers-reverse-ema-trend-cycle-v1`):** TASC Sep 2017 RE1..RE8 cascade. Trend > 0 + Cycle zero-cross. (alpha_t, alpha_c) in {(0.05,0.30), (0.08,0.25), (0.05,0.20)}.

## PASS_6m cells (LEAD)

- `[BTCUSDT] er-sma-gate-cross-v1` @ `4h` (mode_a|(12,26,N20,thr0.40)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=23.29% bh=10.09% ratio=2.308x wr=100.0% n=2 | full=PASS ratio=2.780x n=5

## All Scored Cells by Strategy

### `er-sma-gate-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | 52 | 34.6% | -7.77% | +9.49% | -0.819× | FAIL | 209 | 34.4% | -29.20% | +27.09% | -1.078× | FAIL | -0.15% | -0.67% | — |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | 21 | 23.8% | +2.90% | +9.49% | 0.305× | FAIL | 95 | 30.5% | -9.71% | +27.09% | -0.358× | FAIL | +0.11% | -0.17% | — |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | 2 | 50.0% | +11.36% | +9.49% | 1.198× | FAIL | 5 | 20.0% | +6.93% | +27.09% | 0.256× | FAIL | +0.29% | +0.19% | Near-miss 6m (1.20x B&H) |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | 105 | 24.8% | -13.54% | +9.49% | -1.427× | FAIL | 461 | 21.7% | -71.60% | +27.09% | -2.643× | FAIL | -0.31% | -2.90% | — |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | 15 | 33.3% | -3.75% | +10.09% | -0.371× | FAIL | 57 | 29.8% | -25.21% | +27.43% | -0.919× | FAIL | -0.04% | -0.52% | — |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | 11 | 18.2% | -4.86% | +10.09% | -0.482× | FAIL | 32 | 37.5% | +22.35% | +27.43% | 0.815× | FAIL | -0.05% | +0.66% | — |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | 2 | 100.0% | +23.29% | +10.09% | 2.308× | **PASS** | 5 | 80.0% | +76.25% | +27.43% | 2.780× | **PASS** | +0.57% | +1.58% | — |
| `BTCUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | 31 | 19.4% | -4.32% | +10.09% | -0.428× | FAIL | 121 | 24.0% | -32.79% | +27.43% | -1.195× | FAIL | -0.04% | -0.77% | — |
### `ehlers-super-passband-rms-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | 49 | 49.0% | -7.70% | +9.49% | -0.812× | FAIL | 211 | 41.2% | -34.09% | +27.09% | -1.259× | FAIL | -0.17% | -0.84% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | 69 | 43.5% | -13.42% | +9.49% | -1.414× | FAIL | 254 | 37.4% | -56.45% | +27.09% | -2.084× | FAIL | -0.33% | -1.89% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | 87 | 43.7% | -19.20% | +9.49% | -2.024× | FAIL | 365 | 36.2% | -75.47% | +27.09% | -2.786× | FAIL | -0.50% | -3.27% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | 88 | 27.3% | -18.43% | +9.49% | -1.942× | FAIL | 365 | 27.1% | -54.24% | +27.09% | -2.002× | FAIL | -0.45% | -1.71% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | 17 | 29.4% | +1.00% | +10.09% | 0.099× | FAIL | 57 | 29.8% | -34.86% | +27.43% | -1.271× | FAIL | +0.11% | -0.90% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | 20 | 30.0% | +3.03% | +10.09% | 0.300× | FAIL | 73 | 32.9% | -32.94% | +27.43% | -1.201× | FAIL | +0.16% | -0.82% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | 25 | 32.0% | +1.17% | +10.09% | 0.116× | FAIL | 87 | 42.5% | -24.28% | +27.43% | -0.885× | FAIL | +0.10% | -0.51% | — |
| `BTCUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | 26 | 34.6% | -6.84% | +10.09% | -0.678× | FAIL | 96 | 32.3% | -18.89% | +27.43% | -0.689× | FAIL | -0.11% | -0.28% | — |
### `rwi-high-low-threshold-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | 276 | 14.5% | -48.47% | +9.49% | -5.108× | FAIL | 1027 | 17.8% | -92.46% | +27.09% | -3.413× | FAIL | -1.59% | -6.12% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | 256 | 13.7% | -47.21% | +9.49% | -4.976× | FAIL | 948 | 17.0% | -92.25% | +27.09% | -3.406× | FAIL | -1.54% | -6.08% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | 267 | 15.0% | -46.48% | +9.49% | -4.899× | FAIL | 1010 | 17.9% | -92.02% | +27.09% | -3.397× | FAIL | -1.50% | -5.99% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | 463 | 16.2% | -78.15% | +9.49% | -8.237× | FAIL | 1726 | 18.8% | -99.52% | +27.09% | -3.674× | FAIL | -3.66% | -12.24% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | 72 | 27.8% | -6.90% | +10.09% | -0.684× | FAIL | 287 | 28.6% | -60.22% | +27.43% | -2.195× | FAIL | -0.17% | -2.19% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | 69 | 26.1% | -8.07% | +10.09% | -0.800× | FAIL | 270 | 28.5% | -53.28% | +27.43% | -1.942× | FAIL | -0.20% | -1.79% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | 72 | 26.4% | -8.10% | +10.09% | -0.802× | FAIL | 286 | 28.0% | -56.28% | +27.43% | -2.052× | FAIL | -0.20% | -1.96% | — |
| `BTCUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | 103 | 26.2% | -23.09% | +10.09% | -2.288× | FAIL | 416 | 29.8% | -63.11% | +27.43% | -2.301× | FAIL | -0.61% | -2.23% | — |
### `ehlers-reverse-ema-trend-cycle-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | 69 | 27.5% | -11.51% | +9.49% | -1.213× | FAIL | 296 | 27.4% | -36.15% | +27.09% | -1.334× | FAIL | -0.25% | -0.97% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | 65 | 32.3% | -4.33% | +9.49% | -0.456× | FAIL | 265 | 28.7% | -33.00% | +27.09% | -1.218× | FAIL | -0.06% | -0.86% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | 59 | 32.2% | -3.32% | +9.49% | -0.350× | FAIL | 255 | 27.8% | -39.96% | +27.09% | -1.475× | FAIL | -0.04% | -1.14% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | 113 | 30.1% | -24.24% | +9.49% | -2.554× | FAIL | 450 | 26.7% | -63.53% | +27.09% | -2.345× | FAIL | -0.63% | -2.25% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | 13 | 46.2% | -1.73% | +10.09% | -0.172× | FAIL | 64 | 31.2% | -24.04% | +27.43% | -0.876× | FAIL | -0.04% | -0.63% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | 9 | 22.2% | -7.32% | +10.09% | -0.725× | FAIL | 57 | 22.8% | -27.97% | +27.43% | -1.020× | FAIL | -0.19% | -0.77% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | 12 | 33.3% | -7.23% | +10.09% | -0.716× | FAIL | 56 | 23.2% | -28.74% | +27.43% | -1.048× | FAIL | -0.18% | -0.80% | — |
| `BTCUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | 27 | 33.3% | -7.16% | +10.09% | -0.709× | FAIL | 113 | 30.1% | -18.59% | +27.43% | -0.678× | FAIL | -0.12% | -0.21% | — |
### `er-sma-gate-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | 2 | 0.0% | -8.17% | +15.50% | -0.527× | FAIL | 3 | 33.3% | +11.84% | +4.00% | 2.957× | **PASS** | -0.21% | +0.34% | — |
| `ETHUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ehlers-super-passband-rms-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rwi-high-low-threshold-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ehlers-reverse-ema-trend-cycle-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `er-sma-gate-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ehlers-super-passband-rms-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rwi-high-low-threshold-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ehlers-reverse-ema-trend-cycle-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `er-sma-gate-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `1h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(9,21,N14,thr0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_a|(12,26,N20,thr0.40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `er-sma-gate-cross-v1` | `4h` | `mode_b|(10,30,N10,thr0.35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ehlers-super-passband-rms-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `1h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(40,60,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(30,50,rms50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_a|(20,40,rms40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-super-passband-rms-v1` | `4h` | `mode_b|(30,50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rwi-high-low-threshold-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `1h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(5,40,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_a|(8,48,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rwi-high-low-threshold-v1` | `4h` | `mode_b|(7,64,thr1.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ehlers-reverse-ema-trend-cycle-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `1h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.08,0.25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_a|(0.05,0.20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ehlers-reverse-ema-trend-cycle-v1` | `4h` | `mode_b|(0.10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
