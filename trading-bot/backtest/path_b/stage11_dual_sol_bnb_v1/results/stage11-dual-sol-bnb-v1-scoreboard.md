# stage11-dual-sol-bnb-v1 scoreboard (BNB-survival-FIRST + dual SOL+BNB survival + density)

Generated (UTC): 2026-09-18T02:48:18.178638+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **BNB-survival-FIRST:** After any SOL clear, run `bnb_smoke` before declaring BNB fail; stresses BNB-after-SOL kill conditions.
- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-10 IDs, no ER-gate clones, no Super Passband/RWI/Reverse EMA/PGO, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Chande TrendScore (`chande-trendscore-zero-cross-v1`):** Signed 11-20 lookback block (-10..+10) zero polarity. (11,10) preferred; (8,8), (15,7). Mode A zero-cross; Mode B EMA(5) smooth.
- **Pee TDI Direction Indicator (`pee-tdi-direction-zero-v1`):** Direction Indicator zero-cross. N=20 preferred; 14, 25. Mode A Direction zero; Mode B TDI>0 and Direction>0.
- **Ehlers Leading Indicator (`ehlers-leading-netlead-ema-v1`):** NetLead x EMA dual-line. a1=0.25 a2=0.50 preferred; (0.20,0.50), (0.25,0.33), (0.33,0.50). Mode A dual-line cross; Mode B NetLead rising.
- **GMMA Oscillator (`gmma-osc-zero-cross-v1`):** Classic Guppy 12 lengths short vs long group mean osc. Mode A zero-cross; Mode B signal EMA(15)/(10).
- **Stridsman VQI (`vqi-sum-sma-cross-v1`):** OHLC volatility quality cumulative sum x fast SMA. sma_fast=9 preferred; 5, 14. Mode A sum x SMA cross; Mode B slow SMA(200) confirm.

## PASS_6m cells (LEAD)

- `[BTCUSDT] pee-tdi-direction-zero-v1` @ `4h` (mode_a|(N25)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=24.68% bh=10.09% ratio=2.445x wr=55.6% n=9 | full=FAIL ratio=0.884x n=48
- `[ETHUSDT] pee-tdi-direction-zero-v1` @ `4h` (mode_a|(N25)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=42.98% bh=15.50% ratio=2.772x wr=50.0% n=12 | full=FAIL ratio=-1.911x n=51
- `[SOLUSDT] pee-tdi-direction-zero-v1` @ `4h` (mode_a|(N25)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=RETENTION OK: 13 trades (ETH=12)]: 6m ret=26.30% bh=15.99% ratio=1.645x wr=53.8% n=13 | full=PASS ratio=3.456x n=47

## All Scored Cells by Strategy

### `chande-trendscore-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | 171 | 22.2% | -40.22% | +10.76% | -3.739× | FAIL | 699 | 21.7% | -85.07% | +25.53% | -3.332× | FAIL | -1.21% | -4.42% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | 216 | 19.9% | -48.80% | +10.76% | -4.537× | FAIL | 858 | 21.1% | -91.62% | +25.53% | -3.588× | FAIL | -1.59% | -5.77% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | 196 | 16.8% | -47.32% | +10.76% | -4.399× | FAIL | 782 | 18.5% | -88.87% | +25.53% | -3.481× | FAIL | -1.52% | -5.11% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | 121 | 24.8% | -25.98% | +10.76% | -2.415× | FAIL | 472 | 27.1% | -68.33% | +25.53% | -2.676× | FAIL | -0.69% | -2.60% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | 34 | 23.5% | -0.60% | +10.09% | -0.059× | FAIL | 155 | 28.4% | -18.13% | +27.43% | -0.661× | FAIL | +0.06% | -0.25% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | 49 | 20.4% | -4.25% | +10.09% | -0.421× | FAIL | 191 | 23.0% | -21.82% | +27.43% | -0.796× | FAIL | -0.05% | -0.37% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | 44 | 18.2% | -14.37% | +10.09% | -1.424× | FAIL | 172 | 26.2% | -34.84% | +27.43% | -1.270× | FAIL | -0.31% | -0.85% | — |
| `BTCUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | 28 | 21.4% | -10.70% | +10.09% | -1.060× | FAIL | 110 | 30.0% | -11.64% | +27.43% | -0.424× | FAIL | -0.21% | +0.00% | — |
### `pee-tdi-direction-zero-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 59 | 39.0% | -6.56% | +10.76% | -0.610× | FAIL | 248 | 31.0% | -59.06% | +25.53% | -2.313× | FAIL | -0.10% | -1.95% | — |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | 86 | 37.2% | -18.57% | +10.76% | -1.726× | FAIL | 353 | 32.3% | -63.98% | +25.53% | -2.506× | FAIL | -0.47% | -2.29% | — |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | 50 | 34.0% | -6.00% | +10.76% | -0.558× | FAIL | 203 | 31.0% | -20.54% | +25.53% | -0.805× | FAIL | -0.09% | -0.33% | — |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_b|(N20)` | `Y` | `Y` | `—` | 0 | 0.0% | +0.00% | +10.76% | 0.000× | FAIL | 0 | 0.0% | +0.00% | +25.53% | 0.000× | FAIL | +0.00% | +0.00% | TINY-N KILL (BTC 6m n=0 <= 5 despite 0.00x B&H) |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 15 | 40.0% | +9.23% | +10.09% | 0.915× | FAIL | 71 | 31.0% | -12.31% | +27.43% | -0.449× | FAIL | +0.30% | -0.11% | Near-miss 6m (0.92x B&H) |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | 26 | 30.8% | -14.05% | +10.09% | -1.393× | FAIL | 96 | 29.2% | -38.73% | +27.43% | -1.412× | FAIL | -0.32% | -0.94% | — |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | 9 | 55.6% | +24.68% | +10.09% | 2.445× | **PASS** | 48 | 43.8% | +24.24% | +27.43% | 0.884× | FAIL | +0.62% | +0.75% | THIN-N FLAG (BTC 6m n=9 in thin band [6..10]) |
| `BTCUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_b|(N20)` | `Y` | `Y` | `—` | 0 | 0.0% | +0.00% | +10.09% | 0.000× | FAIL | 0 | 0.0% | +0.00% | +27.43% | 0.000× | FAIL | +0.00% | +0.00% | TINY-N KILL (BTC 6m n=0 <= 5 despite 0.00x B&H) |
### `ehlers-leading-netlead-ema-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | 281 | 20.3% | -59.50% | +10.76% | -5.532× | FAIL | 1058 | 23.8% | -93.51% | +25.53% | -3.663× | FAIL | -2.16% | -6.38% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | 249 | 19.7% | -56.80% | +10.76% | -5.280× | FAIL | 938 | 22.8% | -91.88% | +25.53% | -3.599× | FAIL | -2.00% | -5.85% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | 185 | 22.7% | -41.87% | +10.76% | -3.892× | FAIL | 722 | 24.2% | -85.61% | +25.53% | -3.353× | FAIL | -1.27% | -4.49% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | 342 | 18.4% | -69.53% | +10.76% | -6.463× | FAIL | 1262 | 22.5% | -97.44% | +25.53% | -3.817× | FAIL | -2.86% | -8.52% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | 166 | 22.3% | -32.15% | +10.76% | -2.988× | FAIL | 639 | 24.9% | -79.31% | +25.53% | -3.106× | FAIL | -0.93% | -3.73% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | 68 | 25.0% | -15.32% | +10.09% | -1.518× | FAIL | 255 | 27.8% | -51.36% | +27.43% | -1.872× | FAIL | -0.36% | -1.51% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | 59 | 22.0% | -14.55% | +10.09% | -1.441× | FAIL | 224 | 27.2% | -45.48% | +27.43% | -1.658× | FAIL | -0.33% | -1.25% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | 46 | 26.1% | -4.86% | +10.09% | -0.481× | FAIL | 168 | 26.8% | -37.55% | +27.43% | -1.369× | FAIL | -0.04% | -0.91% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | 77 | 24.7% | -22.03% | +10.09% | -2.183× | FAIL | 304 | 27.6% | -54.22% | +27.43% | -1.977× | FAIL | -0.58% | -1.73% | — |
| `BTCUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | 41 | 24.4% | -6.11% | +10.09% | -0.605× | FAIL | 153 | 28.1% | -19.94% | +27.43% | -0.727× | FAIL | -0.11% | -0.38% | — |
### `gmma-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | 69 | 26.1% | -10.03% | +10.76% | -0.932× | FAIL | 286 | 22.7% | -57.25% | +25.53% | -2.242× | FAIL | -0.19% | -1.83% | — |
| `BTCUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | 71 | 21.1% | -16.68% | +10.76% | -1.550× | FAIL | 286 | 23.8% | -52.39% | +25.53% | -2.052× | FAIL | -0.43% | -1.75% | — |
| `BTCUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | 83 | 20.5% | -20.91% | +10.76% | -1.944× | FAIL | 336 | 23.8% | -58.32% | +25.53% | -2.284× | FAIL | -0.57% | -2.09% | — |
| `BTCUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | 18 | 33.3% | +4.48% | +10.09% | 0.444× | FAIL | 77 | 27.3% | -13.37% | +27.43% | -0.488× | FAIL | +0.18% | -0.13% | — |
| `BTCUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | 17 | 5.9% | -17.02% | +10.09% | -1.687× | FAIL | 67 | 23.9% | -5.07% | +27.43% | -0.185× | FAIL | -0.46% | -0.07% | — |
| `BTCUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | 22 | 22.7% | -12.36% | +10.09% | -1.225× | FAIL | 87 | 23.0% | -19.03% | +27.43% | -0.694× | FAIL | -0.33% | -0.46% | — |
### `vqi-sum-sma-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | 379 | 20.1% | -66.45% | +10.76% | -6.177× | FAIL | 1534 | 21.1% | -99.09% | +25.53% | -3.881× | FAIL | -2.64% | -10.88% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | 558 | 19.4% | -81.27% | +10.76% | -7.555× | FAIL | 2218 | 20.7% | -99.87% | +25.53% | -3.912× | FAIL | -4.06% | -15.15% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | 283 | 20.1% | -49.77% | +10.76% | -4.626× | FAIL | 1148 | 20.5% | -96.04% | +25.53% | -3.762× | FAIL | -1.64% | -7.52% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | 183 | 19.1% | -39.01% | +10.76% | -3.627× | FAIL | 771 | 20.6% | -89.87% | +25.53% | -3.520× | FAIL | -1.20% | -5.45% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | 101 | 21.8% | -29.49% | +10.09% | -2.923× | FAIL | 371 | 27.2% | -53.50% | +27.43% | -1.951× | FAIL | -0.83% | -1.70% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | 144 | 26.4% | -37.75% | +10.09% | -3.741× | FAIL | 562 | 27.4% | -81.01% | +27.43% | -2.953× | FAIL | -1.11% | -3.83% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | 78 | 19.2% | -22.21% | +10.09% | -2.201× | FAIL | 281 | 24.2% | -45.52% | +27.43% | -1.659× | FAIL | -0.59% | -1.31% | — |
| `BTCUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | 64 | 18.8% | -22.36% | +10.09% | -2.216× | FAIL | 203 | 25.1% | -27.15% | +27.43% | -0.990× | FAIL | -0.60% | -0.65% | — |
### `chande-trendscore-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `pee-tdi-direction-zero-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_b|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | 12 | 50.0% | +42.98% | +15.50% | 2.772× | **PASS** | 51 | 39.2% | -7.65% | +4.00% | -1.911× | FAIL | +1.01% | +0.46% | — |
| `ETHUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_b|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `ehlers-leading-netlead-ema-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `gmma-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `vqi-sum-sma-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `chande-trendscore-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `pee-tdi-direction-zero-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_b|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `RETENTION OK: 13 trades (ETH=12)` | 13 | 53.8% | +26.30% | +15.99% | 1.645× | **PASS** | 47 | 55.3% | +56.81% | -23.13% | 3.456× | **PASS** | +0.71% | +1.60% | SOL hard filter |
| `SOLUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_b|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `ehlers-leading-netlead-ema-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `gmma-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `vqi-sum-sma-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `chande-trendscore-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `1h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(11,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(8,8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_a|(15,7)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `chande-trendscore-zero-cross-v1` | `4h` | `mode_b|(11,10,ema5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `pee-tdi-direction-zero-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `1h` | `mode_b|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | 12 | 33.3% | -19.90% | +15.75% | -1.263× | FAIL | 48 | 35.4% | -15.79% | +35.43% | -0.446× | FAIL | -0.49% | -0.18% | BNB hard filter |
| `BNBUSDT` | `pee-tdi-direction-zero-v1` | `4h` | `mode_b|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `ehlers-leading-netlead-ema-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `1h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.20,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.25,a2_0.33)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_a|(a1_0.33,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-leading-netlead-ema-v1` | `4h` | `mode_b|(a1_0.25,a2_0.50)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `gmma-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `gmma-osc-zero-cross-v1` | `1h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_a|(classic12)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig15)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `gmma-osc-zero-cross-v1` | `4h` | `mode_b|(classic12,sig10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `vqi-sum-sma-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `1h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast9)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast5)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_a|(fast14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `vqi-sum-sma-cross-v1` | `4h` | `mode_b|(fast9,slow200)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
