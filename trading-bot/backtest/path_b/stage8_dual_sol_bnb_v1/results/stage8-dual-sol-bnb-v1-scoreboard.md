# stage8-dual-sol-bnb-v1 scoreboard (DUAL SOL+BNB survival + density: SOL + BNB)

Generated (UTC): 2026-09-18T01:20:26.649579+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified).
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-7 IDs, no ER-gate clones, no Super Passband/RWI/Reverse EMA, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Awesome Oscillator (`ao-median-zero-cross-v1`):** SMA(HL2, Af) - SMA(HL2, As) zero-cross. (Af, As) in {(5,34), (5,21), (8,34)}. Mode A zero-cross; Mode B Williams saucer above zero.
- **Pretty Good Oscillator (`pgo-threshold-zeroexit-v1`):** (Close - SMA)/EMA(TR) threshold cross + zero exit. N in {14,21,34}; thr in {2.0, 2.5, 3.0}. Mode A thr cross + zero return; Mode B PGO > thr*0.5 & Close > SMA.
- **Rate of Change (`roc-zero-cross-v1`):** 100*(Close/Close[N] - 1) centerline cross. N in {9, 12, 14, 21}. Mode A zero-cross; Mode B oversold reclaim cross > -8.
- **Weighted Moving Average (`wma-fast-slow-cross-v1`):** Linear WMA fast x slow cross. (Lf, Ls) in {(10,30), (9,21), (12,26), (5,20)}. Mode A fast x slow cross; Mode B Close > Slow & Fast > Slow.

## PASS_6m cells (LEAD)

- `[BTCUSDT] pgo-threshold-zeroexit-v1` @ `4h` (mode_a|(N21,thr2.5)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=16.15% bh=10.09% ratio=1.600x wr=33.3% n=9 | full=FAIL ratio=-0.240x n=43

## All Scored Cells by Strategy

### `ao-median-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | 96 | 30.2% | -13.37% | +9.49% | -1.410× | FAIL | 376 | 28.2% | -58.43% | +27.09% | -2.157× | FAIL | -0.29% | -1.93% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | 137 | 27.7% | -25.76% | +9.49% | -2.715× | FAIL | 541 | 26.2% | -75.68% | +27.09% | -2.794× | FAIL | -0.68% | -3.24% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | 83 | 28.9% | -13.44% | +9.49% | -1.416× | FAIL | 317 | 29.3% | -59.16% | +27.09% | -2.184× | FAIL | -0.30% | -1.98% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | 57 | 29.8% | -12.06% | +9.49% | -1.271× | FAIL | 223 | 30.0% | -33.52% | +27.09% | -1.237× | FAIL | -0.30% | -0.90% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | 26 | 38.5% | -13.56% | +10.09% | -1.344× | FAIL | 104 | 27.9% | -36.84% | +27.43% | -1.343× | FAIL | -0.30% | -0.92% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | 29 | 31.0% | +0.51% | +10.09% | 0.050× | FAIL | 128 | 31.2% | +2.19% | +27.43% | 0.080× | FAIL | +0.09% | +0.30% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | 22 | 31.8% | -11.29% | +10.09% | -1.118× | FAIL | 88 | 29.5% | -24.19% | +27.43% | -0.882× | FAIL | -0.24% | -0.43% | — |
| `BTCUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | 16 | 18.8% | -10.87% | +10.09% | -1.077× | FAIL | 68 | 29.4% | -17.96% | +27.43% | -0.655× | FAIL | -0.26% | -0.37% | — |
### `pgo-threshold-zeroexit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | 26 | 30.8% | +1.91% | +9.49% | 0.201× | FAIL | 119 | 35.3% | -23.92% | +27.09% | -0.883× | FAIL | +0.08% | -0.62% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | 50 | 22.0% | -7.12% | +9.49% | -0.750× | FAIL | 223 | 27.4% | -53.71% | +27.09% | -1.983× | FAIL | -0.14% | -1.81% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | 37 | 27.0% | -7.98% | +9.49% | -0.841× | FAIL | 165 | 33.3% | -34.49% | +27.09% | -1.273× | FAIL | -0.17% | -0.96% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | 111 | 22.5% | -24.96% | +9.49% | -2.631× | FAIL | 446 | 25.8% | -74.37% | +27.09% | -2.746× | FAIL | -0.66% | -3.19% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | 6 | 33.3% | +8.82% | +10.09% | 0.874× | FAIL | 31 | 38.7% | +1.27% | +27.43% | 0.046× | FAIL | +0.25% | +0.13% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | 13 | 23.1% | +5.94% | +10.09% | 0.589× | FAIL | 58 | 34.5% | -20.67% | +27.43% | -0.754× | FAIL | +0.18% | -0.46% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | 9 | 33.3% | +16.15% | +10.09% | 1.600× | **PASS** | 43 | 34.9% | -6.58% | +27.43% | -0.240× | FAIL | +0.43% | -0.03% | — |
| `BTCUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | 27 | 18.5% | -2.02% | +10.09% | -0.200× | FAIL | 108 | 26.9% | -16.55% | +27.43% | -0.603× | FAIL | -0.00% | -0.32% | — |
### `roc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | 330 | 16.7% | -65.98% | +9.49% | -6.954× | FAIL | 1246 | 19.5% | -97.15% | +27.09% | -3.586× | FAIL | -2.59% | -8.26% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N9)` | `Y` | `Y` | `—` | 367 | 18.3% | -66.95% | +9.49% | -7.056× | FAIL | 1452 | 18.5% | -98.55% | +27.09% | -3.638× | FAIL | -2.66% | -9.81% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | 286 | 18.2% | -60.73% | +9.49% | -6.400× | FAIL | 1134 | 18.3% | -96.41% | +27.09% | -3.559× | FAIL | -2.23% | -7.73% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `1h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | 0 | 0.0% | +0.00% | +9.49% | 0.000× | FAIL | 3 | 33.3% | +1.22% | +27.09% | 0.045× | FAIL | +0.00% | +0.03% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | 68 | 22.1% | -12.27% | +10.09% | -1.216× | FAIL | 304 | 21.7% | -56.26% | +27.43% | -2.051× | FAIL | -0.27% | -1.84% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N9)` | `Y` | `Y` | `—` | 86 | 24.4% | -21.04% | +10.09% | -2.085× | FAIL | 350 | 24.0% | -65.11% | +27.43% | -2.374× | FAIL | -0.56% | -2.40% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | 62 | 24.2% | -14.41% | +10.09% | -1.428× | FAIL | 270 | 26.3% | -35.43% | +27.43% | -1.292× | FAIL | -0.32% | -0.83% | — |
| `BTCUSDT` | `roc-zero-cross-v1` | `4h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | 1 | 0.0% | -9.33% | +10.09% | -0.925× | FAIL | 13 | 46.2% | -11.67% | +27.43% | -0.426× | FAIL | -0.23% | -0.28% | — |
### `wma-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | 112 | 30.4% | -24.56% | +9.49% | -2.588× | FAIL | 437 | 28.4% | -66.20% | +27.09% | -2.444× | FAIL | -0.64% | -2.43% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | 144 | 25.0% | -29.44% | +9.49% | -3.102× | FAIL | 566 | 27.2% | -77.85% | +27.09% | -2.874× | FAIL | -0.80% | -3.46% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | 106 | 33.0% | -14.92% | +9.49% | -1.572× | FAIL | 445 | 29.0% | -64.19% | +27.09% | -2.370× | FAIL | -0.35% | -2.30% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | 111 | 30.6% | -24.28% | +9.49% | -2.559× | FAIL | 431 | 28.8% | -64.82% | +27.09% | -2.393× | FAIL | -0.63% | -2.33% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | 26 | 30.8% | -7.10% | +10.09% | -0.703× | FAIL | 106 | 30.2% | -9.50% | +27.43% | -0.347× | FAIL | -0.11% | +0.06% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | 32 | 31.2% | -0.89% | +10.09% | -0.089× | FAIL | 135 | 32.6% | +3.72% | +27.43% | 0.136× | FAIL | +0.05% | +0.33% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | 27 | 25.9% | -9.07% | +10.09% | -0.898× | FAIL | 105 | 33.3% | +0.06% | +27.43% | 0.002× | FAIL | -0.17% | +0.30% | — |
| `BTCUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | 26 | 30.8% | -7.10% | +10.09% | -0.703× | FAIL | 106 | 30.2% | -11.34% | +27.43% | -0.414× | FAIL | -0.11% | +0.00% | — |
### `ao-median-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `pgo-threshold-zeroexit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | 10 | 20.0% | -1.94% | +15.50% | -0.125× | FAIL | 48 | 27.1% | -9.30% | +4.00% | -2.324× | FAIL | -0.01% | +0.06% | — |
| `ETHUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `roc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `1h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `roc-zero-cross-v1` | `4h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `wma-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ao-median-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `pgo-threshold-zeroexit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `roc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `1h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `roc-zero-cross-v1` | `4h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `wma-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `ao-median-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `1h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(5,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_a|(8,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `ao-median-zero-cross-v1` | `4h` | `mode_b|(5,34)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `pgo-threshold-zeroexit-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `1h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N14,thr2.0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_a|(N21,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `pgo-threshold-zeroexit-v1` | `4h` | `mode_b|(N14,thr2.5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `roc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `1h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `roc-zero-cross-v1` | `4h` | `mode_b|(N12,ext8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `wma-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `1h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(9,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `wma-fast-slow-cross-v1` | `4h` | `mode_b|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
