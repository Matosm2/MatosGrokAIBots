# stage10-dual-sol-bnb-v1 scoreboard (DUAL SOL+BNB survival + density: SOL + BNB)

Generated (UTC): 2026-09-18T02:28:02.040712+00:00

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
- **Hard excludes honored** (no stage1-9 IDs, no ER-gate clones, no Super Passband/RWI/Reverse EMA/PGO, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Trend Intensity Index (`tii-midline-fifty-cross-v1`):** SMA-deviation intensity midline-50 cross. (60,30) preferred; (40,20), (50,25). Mode A 50-cross; Mode B 80-cross.
- **Rainbow Oscillator (`rainbow-osc-zero-cross-v1`):** Widner recursive-SMA consensus zero-cross. p=2 depth=10 preferred; (2,8), (3,10). Mode A zero-cross; Mode B RB-filtered.
- **Dorsey Relative Volatility Index (`dorsey-relvol-midline-fifty-v1`):** Stdev-direction midline-50 cross. (10,14) preferred; (8,14), (14,14), (10,10). Mode A 50-cross; Mode B 60/40.
- **Trend Continuation Factor (`tcf-plus-sign-flip-v1`):** Pee +TCF sign polarity. N=35 preferred; 25, 20. Mode A +TCF zero flip; Mode B dual cross.
- **Double EMA Fast×Slow (`dema-fast-slow-cross-v1`):** Mulloy DEMA fast×slow cross. (10,30) preferred; (5,35), (8,21), (12,26). Mode A fast×slow cross; Mode B close×slow.

## PASS_6m cells (LEAD)

- `[BTCUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(60,30)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=16.16% bh=10.09% ratio=1.602x wr=57.1% n=7 | full=PASS ratio=1.404x n=30
- `[BTCUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(40,20)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=22.44% bh=10.09% ratio=2.224x wr=55.6% n=9 | full=FAIL ratio=0.652x n=47
- `[BTCUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(50,25)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=28.82% bh=10.09% ratio=2.856x wr=57.1% n=7 | full=FAIL ratio=1.111x n=39
- `[ETHUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(40,20)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=39.30% bh=15.50% ratio=2.535x wr=45.5% n=11 | full=PASS ratio=3.335x n=48
- `[ETHUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(50,25)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=51.76% bh=15.50% ratio=3.339x wr=57.1% n=7 | full=PASS ratio=7.955x n=36
- `[SOLUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(40,20)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=RETENTION OK: 12 trades (ETH=11)]: 6m ret=22.34% bh=15.99% ratio=1.398x wr=50.0% n=12 | full=PASS ratio=-0.978x n=46
- `[SOLUSDT] tii-midline-fifty-cross-v1` @ `4h` (mode_a|(50,25)) [sol_smoke=Y, bnb_smoke=Y, sol_retention=RETENTION OK: 8 trades (ETH=7)]: 6m ret=33.55% bh=15.99% ratio=2.099x wr=62.5% n=8 | full=PASS ratio=-3.086x n=35

## All Scored Cells by Strategy

### `tii-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | 32 | 25.0% | -6.36% | +10.76% | -0.591× | FAIL | 127 | 29.1% | +0.02% | +25.53% | 0.001× | FAIL | -0.10% | +0.25% | — |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | 45 | 35.6% | +0.84% | +10.76% | 0.078× | FAIL | 191 | 33.0% | -35.54% | +25.53% | -1.392× | FAIL | +0.09% | -0.84% | — |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | 33 | 30.3% | +5.33% | +10.76% | 0.496× | FAIL | 143 | 32.2% | +11.99% | +25.53% | 0.470× | FAIL | +0.20% | +0.52% | — |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | 28 | 25.0% | -12.59% | +10.76% | -1.170× | FAIL | 112 | 33.9% | -12.19% | +25.53% | -0.477× | FAIL | -0.27% | -0.13% | — |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | 7 | 57.1% | +16.16% | +10.09% | 1.602× | **PASS** | 30 | 36.7% | +38.51% | +27.43% | 1.404× | **PASS** | +0.41% | +1.04% | THIN-N FLAG (BTC 6m n=7 in thin band [6..10]) |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | 9 | 55.6% | +22.44% | +10.09% | 2.224× | **PASS** | 47 | 36.2% | +17.89% | +27.43% | 0.652× | FAIL | +0.57% | +0.60% | THIN-N FLAG (BTC 6m n=9 in thin band [6..10]) |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | 7 | 57.1% | +28.82% | +10.09% | 2.856× | **PASS** | 39 | 38.5% | +30.47% | +27.43% | 1.111× | FAIL | +0.70% | +0.87% | THIN-N FLAG (BTC 6m n=7 in thin band [6..10]) |
| `BTCUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | 7 | 42.9% | +2.26% | +10.09% | 0.224× | FAIL | 25 | 40.0% | +11.93% | +27.43% | 0.435× | FAIL | +0.07% | +0.46% | THIN-N FLAG (BTC 6m n=7 in thin band [6..10]) |
### `rainbow-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | 556 | 17.4% | -82.91% | +10.76% | -7.707× | FAIL | 2239 | 18.9% | -99.91% | +25.53% | -3.913× | FAIL | -4.27% | -15.99% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | 624 | 16.5% | -86.86% | +10.76% | -8.074× | FAIL | 2452 | 18.6% | -99.96% | +25.53% | -3.915× | FAIL | -4.90% | -17.48% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | 372 | 16.9% | -68.64% | +10.76% | -6.381× | FAIL | 1473 | 18.7% | -98.48% | +25.53% | -3.857× | FAIL | -2.79% | -9.70% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | 445 | 18.4% | -72.51% | +10.76% | -6.740× | FAIL | 1830 | 18.5% | -99.65% | +25.53% | -3.903× | FAIL | -3.13% | -13.03% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | 137 | 24.8% | -36.06% | +10.09% | -3.573× | FAIL | 543 | 24.9% | -79.18% | +27.43% | -2.887× | FAIL | -1.05% | -3.61% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | 150 | 25.3% | -36.35% | +10.09% | -3.602× | FAIL | 605 | 24.1% | -83.58% | +27.43% | -3.047× | FAIL | -1.05% | -4.17% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | 95 | 17.9% | -24.15% | +10.09% | -2.394× | FAIL | 359 | 22.0% | -62.62% | +27.43% | -2.283× | FAIL | -0.63% | -2.21% | — |
| `BTCUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | 117 | 23.9% | -41.61% | +10.09% | -4.123× | FAIL | 440 | 23.9% | -79.05% | +27.43% | -2.882× | FAIL | -1.32% | -3.69% | — |
### `dorsey-relvol-midline-fifty-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | 263 | 21.3% | -51.54% | +10.76% | -4.791× | FAIL | 1037 | 21.3% | -93.54% | +25.53% | -3.664× | FAIL | -1.75% | -6.41% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | 268 | 17.5% | -53.17% | +10.76% | -4.942× | FAIL | 1004 | 21.2% | -93.81% | +25.53% | -3.674× | FAIL | -1.84% | -6.53% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | 299 | 19.1% | -59.84% | +10.76% | -5.563× | FAIL | 1120 | 19.7% | -95.93% | +25.53% | -3.757× | FAIL | -2.21% | -7.47% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | 301 | 21.3% | -52.52% | +10.76% | -4.883× | FAIL | 1226 | 21.0% | -96.54% | +25.53% | -3.781× | FAIL | -1.80% | -7.84% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | 38 | 26.3% | -5.56% | +10.76% | -0.516× | FAIL | 147 | 34.7% | -9.46% | +25.53% | -0.371× | FAIL | -0.10% | -0.02% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | 68 | 27.9% | -19.50% | +10.09% | -1.932× | FAIL | 243 | 26.7% | -41.03% | +27.43% | -1.496× | FAIL | -0.50% | -0.99% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | 71 | 25.4% | -21.37% | +10.09% | -2.118× | FAIL | 250 | 24.8% | -45.21% | +27.43% | -1.648× | FAIL | -0.56% | -1.19% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | 71 | 31.0% | -18.17% | +10.09% | -1.801× | FAIL | 253 | 26.1% | -39.33% | +27.43% | -1.434× | FAIL | -0.45% | -0.90% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | 74 | 28.4% | -22.52% | +10.09% | -2.232× | FAIL | 290 | 25.5% | -49.02% | +27.43% | -1.787× | FAIL | -0.60% | -1.40% | — |
| `BTCUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | 8 | 50.0% | +7.55% | +10.09% | 0.749× | FAIL | 35 | 45.7% | +22.52% | +27.43% | 0.821× | FAIL | +0.22% | +0.72% | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
### `tcf-plus-sign-flip-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N35)` | `Y` | `Y` | `—` | 101 | 11.9% | -35.16% | +10.76% | -3.269× | FAIL | 387 | 20.9% | -68.34% | +25.53% | -2.677× | FAIL | -1.05% | -2.75% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | 158 | 18.4% | -41.67% | +10.76% | -3.874× | FAIL | 573 | 21.8% | -82.78% | +25.53% | -3.242× | FAIL | -1.31% | -4.19% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 166 | 14.5% | -39.62% | +10.76% | -3.683× | FAIL | 658 | 18.5% | -83.52% | +25.53% | -3.271× | FAIL | -1.22% | -4.27% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_b|(N35)` | `Y` | `Y` | `—` | 1 | 100.0% | +0.24% | +10.76% | 0.022× | FAIL | 3 | 33.3% | -0.62% | +25.53% | -0.024× | FAIL | +0.01% | -0.02% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N35)` | `Y` | `Y` | `—` | 17 | 29.4% | +4.29% | +10.09% | 0.425× | FAIL | 89 | 28.1% | -7.91% | +27.43% | -0.288× | FAIL | +0.13% | -0.11% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | 33 | 18.2% | -0.08% | +10.09% | -0.008× | FAIL | 128 | 21.9% | -35.04% | +27.43% | -1.277× | FAIL | +0.06% | -0.90% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | 43 | 27.9% | -3.67% | +10.09% | -0.364× | FAIL | 180 | 24.4% | -51.49% | +27.43% | -1.877× | FAIL | -0.03% | -1.63% | — |
| `BTCUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_b|(N35)` | `Y` | `Y` | `—` | 0 | 0.0% | +0.00% | +10.09% | 0.000× | FAIL | 1 | 0.0% | -3.04% | +27.43% | -0.111× | FAIL | +0.00% | -0.08% | — |
### `dema-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | 129 | 28.7% | -24.91% | +10.76% | -2.316× | FAIL | 542 | 28.4% | -80.25% | +25.53% | -3.143× | FAIL | -0.67% | -3.76% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | 173 | 24.3% | -39.42% | +10.76% | -3.665× | FAIL | 721 | 23.7% | -88.63% | +25.53% | -3.472× | FAIL | -1.19% | -5.07% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | 173 | 28.9% | -38.12% | +10.76% | -3.544× | FAIL | 710 | 28.9% | -86.93% | +25.53% | -3.405× | FAIL | -1.15% | -4.74% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | 123 | 30.1% | -22.31% | +10.76% | -2.074× | FAIL | 512 | 29.7% | -76.77% | +25.53% | -3.007× | FAIL | -0.58% | -3.36% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | 291 | 19.9% | -57.98% | +10.76% | -5.390× | FAIL | 1279 | 19.5% | -98.17% | +25.53% | -3.845× | FAIL | -2.09% | -9.31% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | 34 | 23.5% | -1.11% | +10.09% | -0.110× | FAIL | 140 | 32.9% | -22.75% | +27.43% | -0.829× | FAIL | +0.05% | -0.41% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | 43 | 25.6% | -3.23% | +10.09% | -0.320× | FAIL | 175 | 27.4% | -27.28% | +27.43% | -0.994× | FAIL | -0.02% | -0.56% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | 42 | 26.2% | -2.09% | +10.09% | -0.207× | FAIL | 167 | 31.1% | -10.54% | +27.43% | -0.384× | FAIL | +0.02% | -0.04% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | 31 | 22.6% | +0.18% | +10.09% | 0.018× | FAIL | 132 | 31.8% | -18.10% | +27.43% | -0.660× | FAIL | +0.08% | -0.27% | — |
| `BTCUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | 85 | 20.0% | -19.54% | +10.09% | -1.936× | FAIL | 331 | 21.8% | -58.02% | +27.43% | -2.115× | FAIL | -0.48% | -1.91% | — |
### `tii-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | 8 | 37.5% | +18.60% | +15.50% | 1.200× | FAIL | 31 | 35.5% | +40.01% | +4.00% | 9.995× | **PASS** | +0.53% | +1.58% | Near-miss 6m (1.20x B&H) |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | 11 | 45.5% | +39.30% | +15.50% | 2.535× | **PASS** | 48 | 37.5% | +13.35% | +4.00% | 3.335× | **PASS** | +0.94% | +0.88% | — |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | 7 | 57.1% | +51.76% | +15.50% | 3.339× | **PASS** | 36 | 44.4% | +31.84% | +4.00% | 7.955× | **PASS** | +1.17% | +1.28% | — |
| `ETHUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rainbow-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `dorsey-relvol-midline-fifty-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `tcf-plus-sign-flip-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_b|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_b|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `dema-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `ETHUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `tii-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(40,20)` | `Y` | `Y` | `RETENTION OK: 12 trades (ETH=11)` | 12 | 50.0% | +22.34% | +15.99% | 1.398× | **PASS** | 46 | 45.7% | +22.62% | -23.13% | -0.978× | **PASS** | +0.63% | +0.94% | SOL hard filter |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(50,25)` | `Y` | `Y` | `RETENTION OK: 8 trades (ETH=7)` | 8 | 62.5% | +33.55% | +15.99% | 2.099× | **PASS** | 35 | 42.9% | +71.40% | -23.13% | -3.086× | **PASS** | +0.88% | +1.79% | SOL hard filter |
| `SOLUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rainbow-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `dorsey-relvol-midline-fifty-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `tcf-plus-sign-flip-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_b|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_b|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `dema-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `SOLUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `tii-midline-fifty-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `1h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(60,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(40,20)` | `Y` | `Y` | `—` | 11 | 36.4% | -14.57% | +15.75% | -0.925× | FAIL | 43 | 37.2% | -18.51% | +35.43% | -0.522× | FAIL | -0.34% | -0.32% | BNB hard filter |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_a|(50,25)` | `Y` | `Y` | `—` | 10 | 50.0% | -10.95% | +15.75% | -0.695× | FAIL | 35 | 51.4% | +12.25% | +35.43% | 0.346× | FAIL | -0.23% | +0.47% | BNB hard filter |
| `BNBUSDT` | `tii-midline-fifty-cross-v1` | `4h` | `mode_b|(60,30,ob80)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `rainbow-osc-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `1h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p2,d8)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_a|(p3,d10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `rainbow-osc-zero-cross-v1` | `4h` | `mode_b|(p2,d10,rb38)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `dorsey-relvol-midline-fifty-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `1h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(8,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(14,14)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_a|(10,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dorsey-relvol-midline-fifty-v1` | `4h` | `mode_b|(10,14,os40_ob60)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `tcf-plus-sign-flip-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `1h` | `mode_b|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N25)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_a|(N20)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `tcf-plus-sign-flip-v1` | `4h` | `mode_b|(N35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
### `dema-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `1h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(5,35)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(8,21)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_a|(12,26)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
| `BNBUSDT` | `dema-fast-slow-cross-v1` | `4h` | `mode_b|(close,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by ladder |
