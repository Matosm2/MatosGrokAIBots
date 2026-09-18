# stage14-dual-sol-bnb-v1 scoreboard (BTC->ETH portability PRIMARY + BNB-portable SECONDARY)

Generated (UTC): 2026-09-18T03:54:44.095636+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **ETH Portability (CRITICAL):** Stage 13 wipe lesson (REI cleared BTC 1.530x then wiped ETH -1.201x). BTC->ETH portability is primary.
- **BNB-portable SECONDARY:** After BTC+ETH+SOL clear, run `bnb_smoke` before declaring BNB fail; stresses BNB-after-BTC+ETH+SOL kill conditions.
- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-13 IDs, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Super Passband/RWI/Reverse EMA/PGO, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Pee TTF (`pee-ttf-zero-cross`):** Trend Trigger Factor. L=15 preferred; L=10, L=20. Mode A TTF x 0; Mode B +-100 reclaim.
- **Hannula PFE (`hannula-pfe-zero-cross`):** Polarized Fractal Efficiency. (10,5) preferred; (8,3), (14,8). Mode A PFE x 0; Mode B quality hold (pfe > 20).
- **Absolute Strength Histogram (`absolute-strength-hist-zero`):** ASH RSI-method SMA internals. (9,2) preferred; (7,1), (14,3). Mode A ASH x 0; Mode B ash > 0 quality.
- **Leibfarth APZ (`leibfarth-apz-break-flip`):** Adaptive Price Zone double-EMA band break-flip. (20,1.4) preferred; (14,1.2), (30,1.8). Mode A close x up break, exit close x dn; Mode B fade reclaim.
- **Nadaraya RQ (`nadaraya-rq-estimate-cross`):** Causal Nadaraya-Watson Rational Quadratic Kernel. (8,8) preferred; (5,1), (14,25). Mode A close x yhat; Mode B close x yhat + slope.

## PASS_6m cells (LEAD)

- `[BTCUSDT] pee-ttf-zero-cross` @ `4h` (mode_b|(L15)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=35.52% bh=8.74% ratio=4.062x wr=66.7% n=6 | full=FAIL ratio=-0.458x n=38
- `[BTCUSDT] leibfarth-apz-break-flip` @ `4h` (mode_a|(p20,b1.4)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=11.76% bh=8.74% ratio=1.345x wr=40.0% n=10 | full=FAIL ratio=-0.449x n=44
- `[BTCUSDT] leibfarth-apz-break-flip` @ `4h` (mode_a|(p30,b1.8)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=23.34% bh=8.74% ratio=2.669x wr=66.7% n=6 | full=FAIL ratio=0.372x n=29
- `[ETHUSDT] pee-ttf-zero-cross` @ `4h` (mode_b|(L15)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=OK (ETH n=7 vs BTC n=6)]: 6m ret=39.12% bh=14.30% ratio=2.737x wr=42.9% n=7 | full=FAIL ratio=-3.427x n=37
- `[ETHUSDT] leibfarth-apz-break-flip` @ `4h` (mode_a|(p30,b1.8)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=OK (ETH n=5 vs BTC n=6)]: 6m ret=28.22% bh=14.30% ratio=1.974x wr=60.0% n=5 | full=PASS ratio=8.318x n=29
- `[SOLUSDT] pee-ttf-zero-cross` @ `4h` (mode_b|(L15)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=OK (SOL n=8 vs ETH n=7)]: 6m ret=32.87% bh=14.56% ratio=2.257x wr=75.0% n=8 | full=PASS ratio=3.678x n=34

## All Scored Cells by Strategy

### `pee-ttf-zero-cross`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | 86 | 34.9% | -18.92% | +10.13% | -1.867× | FAIL | 361 | 31.6% | -55.95% | +26.47% | -2.113× | FAIL | -0.45% | -1.80% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | 137 | 31.4% | -15.68% | +10.13% | -1.547× | FAIL | 550 | 30.0% | -70.19% | +26.47% | -2.651× | FAIL | -0.35% | -2.72% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | 71 | 32.4% | -16.70% | +10.13% | -1.648× | FAIL | 287 | 28.2% | -57.29% | +26.47% | -2.164× | FAIL | -0.39% | -1.88% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | 40 | 37.5% | -6.80% | +10.13% | -0.671× | FAIL | 148 | 34.5% | -6.58% | +26.47% | -0.249× | FAIL | -0.12% | +0.05% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | 26 | 30.8% | -16.03% | +8.74% | -1.833× | FAIL | 98 | 31.6% | -47.66% | +27.43% | -1.738× | FAIL | -0.36% | -1.36% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | 34 | 32.4% | -7.26% | +8.74% | -0.830× | FAIL | 132 | 37.1% | -2.86% | +27.43% | -0.104× | FAIL | -0.10% | +0.21% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | 17 | 29.4% | +4.73% | +8.74% | 0.541× | FAIL | 74 | 31.1% | -32.06% | +27.43% | -1.169× | FAIL | +0.18% | -0.75% | — |
| `BTCUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | 6 | 66.7% | +35.52% | +8.74% | 4.062× | **PASS** | 38 | 36.8% | -12.58% | +27.43% | -0.458× | FAIL | +0.83% | -0.10% | THIN-N FLAG (BTC 6m n=6 in thin band [6..10]) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `OK (ETH n=7 vs BTC n=6)` | 7 | 42.9% | +39.12% | +14.30% | 2.737× | **PASS** | 37 | 37.8% | -13.72% | +4.00% | -3.427× | FAIL | +0.92% | +0.15% | ETH hard filter |
| `SOLUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `OK (SOL n=8 vs ETH n=7)` | 8 | 75.0% | +32.87% | +14.56% | 2.257× | **PASS** | 34 | 50.0% | +61.96% | -23.13% | 3.678× | **PASS** | +0.78% | +1.64% | SOL hard filter |
| `BNBUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `1h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L15)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `pee-ttf-zero-cross` | `4h` | `mode_b|(L15)` | `Y` | `Y` | `Y` | `Y` | `OK (BNB n=8 vs SOL n=8)` | 8 | 50.0% | +1.43% | +15.36% | 0.093× | FAIL | 37 | 45.9% | -18.05% | +35.43% | -0.510× | FAIL | +0.12% | -0.22% | BNB hard filter |

### `hannula-pfe-zero-cross`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | 189 | 24.9% | -38.03% | +10.13% | -3.753× | FAIL | 711 | 24.3% | -83.68% | +26.47% | -3.161× | FAIL | -1.13% | -4.19% | — |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | 247 | 22.7% | -50.42% | +10.13% | -4.976× | FAIL | 964 | 24.0% | -92.39% | +26.47% | -3.490× | FAIL | -1.67% | -6.01% | — |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | 113 | 26.5% | -24.11% | +10.13% | -2.380× | FAIL | 461 | 28.0% | -69.14% | +26.47% | -2.612× | FAIL | -0.63% | -2.65% | — |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | 1 | 0.0% | -0.83% | +10.13% | -0.082× | FAIL | 4 | 50.0% | -0.06% | +26.47% | -0.002× | FAIL | -0.02% | -0.00% | TINY-N KILL (BTC 6m n=1 <= 5 despite -0.08x B&H) |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | 36 | 27.8% | -2.58% | +8.74% | -0.295× | FAIL | 156 | 31.4% | +7.08% | +27.43% | 0.258× | FAIL | +0.01% | +0.41% | — |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | 58 | 31.0% | -7.15% | +8.74% | -0.817× | FAIL | 226 | 29.2% | -43.26% | +27.43% | -1.577× | FAIL | -0.12% | -1.16% | — |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | 27 | 25.9% | -14.74% | +8.74% | -1.685× | FAIL | 109 | 36.7% | -4.24% | +27.43% | -0.154× | FAIL | -0.33% | +0.19% | — |
| `BTCUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | 0 | 0.0% | +0.00% | +8.74% | 0.000× | FAIL | 0 | 0.0% | +0.00% | +27.43% | 0.000× | FAIL | +0.00% | +0.00% | TINY-N KILL (BTC 6m n=0 <= 5 despite 0.00x B&H) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `1h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p8,s3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_a|(p14,s8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `hannula-pfe-zero-cross` | `4h` | `mode_b|(p10,s5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `absolute-strength-hist-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | 273 | 21.6% | -55.52% | +10.13% | -5.480× | FAIL | 1054 | 22.1% | -94.84% | +26.47% | -3.583× | FAIL | -1.93% | -6.91% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | 414 | 17.6% | -72.19% | +10.13% | -7.125× | FAIL | 1652 | 18.5% | -99.28% | +26.47% | -3.750× | FAIL | -3.10% | -11.40% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | 173 | 23.1% | -39.18% | +10.13% | -3.867× | FAIL | 658 | 25.2% | -83.37% | +26.47% | -3.149× | FAIL | -1.17% | -4.14% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | 273 | 21.6% | -55.52% | +10.13% | -5.480× | FAIL | 1054 | 22.1% | -94.84% | +26.47% | -3.583× | FAIL | -1.93% | -6.91% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | 63 | 31.7% | -15.51% | +8.74% | -1.773× | FAIL | 251 | 27.5% | -50.48% | +27.43% | -1.840× | FAIL | -0.39% | -1.50% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | 99 | 23.2% | -23.59% | +8.74% | -2.698× | FAIL | 400 | 22.2% | -69.11% | +27.43% | -2.520× | FAIL | -0.61% | -2.66% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | 33 | 24.2% | -2.55% | +8.74% | -0.291× | FAIL | 149 | 30.9% | -9.21% | +27.43% | -0.336× | FAIL | +0.01% | +0.01% | — |
| `BTCUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | 63 | 31.7% | -15.51% | +8.74% | -1.773× | FAIL | 251 | 27.5% | -50.48% | +27.43% | -1.840× | FAIL | -0.39% | -1.50% | — |
| `ETHUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `1h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len7,sm1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_a|(len14,sm3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `absolute-strength-hist-zero` | `4h` | `mode_b|(len9,sm2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `leibfarth-apz-break-flip`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | 50 | 24.0% | -12.98% | +10.13% | -1.281× | FAIL | 189 | 27.5% | -47.45% | +26.47% | -1.792× | FAIL | -0.29% | -1.34% | — |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | 62 | 32.3% | -14.35% | +10.13% | -1.417× | FAIL | 246 | 32.5% | -51.56% | +26.47% | -1.948× | FAIL | -0.33% | -1.53% | — |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 34 | 26.5% | -7.34% | +10.13% | -0.724× | FAIL | 128 | 28.9% | -27.52% | +26.47% | -1.040× | FAIL | -0.12% | -0.54% | — |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | 50 | 64.0% | -8.77% | +10.13% | -0.866× | FAIL | 188 | 67.6% | -29.33% | +26.47% | -1.108× | FAIL | -0.18% | -0.66% | — |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | 10 | 40.0% | +11.76% | +8.74% | 1.345× | **PASS** | 44 | 34.1% | -12.32% | +27.43% | -0.449× | FAIL | +0.34% | -0.09% | THIN-N FLAG (BTC 6m n=10 in thin band [6..10]) |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | 18 | 33.3% | -6.69% | +8.74% | -0.765× | FAIL | 62 | 40.3% | -19.43% | +27.43% | -0.708× | FAIL | -0.11% | -0.30% | — |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 6 | 66.7% | +23.34% | +8.74% | 2.669× | **PASS** | 29 | 34.5% | +10.21% | +27.43% | 0.372× | FAIL | +0.58% | +0.48% | THIN-N FLAG (BTC 6m n=6 in thin band [6..10]) |
| `BTCUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | 11 | 54.5% | -14.36% | +8.74% | -1.642× | FAIL | 45 | 62.2% | -11.48% | +27.43% | -0.419× | FAIL | -0.33% | -0.11% | — |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `OK (ETH n=11 vs BTC n=10)` | 11 | 27.3% | +11.46% | +14.30% | 0.802× | FAIL | 45 | 35.6% | +4.49% | +4.00% | 1.121× | FAIL | +0.38% | +0.85% | ETH hard filter |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `OK (ETH n=5 vs BTC n=6)` | 5 | 60.0% | +28.22% | +14.30% | 1.974× | **PASS** | 29 | 37.9% | +33.29% | +4.00% | 8.318× | **PASS** | +0.72% | +1.49% | ETH hard filter |
| `ETHUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `OK (SOL n=7 vs ETH n=5)` | 7 | 42.9% | +10.62% | +14.56% | 0.730× | FAIL | 30 | 43.3% | -11.77% | -23.13% | 0.491× | FAIL | +0.37% | +0.14% | SOL hard filter |
| `SOLUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `1h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p14,b1.2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_a|(p30,b1.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `leibfarth-apz-break-flip` | `4h` | `mode_b|(p20,b1.4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `nadaraya-rq-estimate-cross`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | 485 | 18.6% | -77.30% | +10.13% | -7.630× | FAIL | 1953 | 19.5% | -99.74% | +26.47% | -3.768× | FAIL | -3.59% | -13.60% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | 652 | 17.5% | -87.13% | +10.13% | -8.600× | FAIL | 2531 | 19.6% | -99.96% | +26.47% | -3.776× | FAIL | -4.95% | -17.67% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | 358 | 16.8% | -66.66% | +10.13% | -6.579× | FAIL | 1381 | 18.3% | -98.18% | +26.47% | -3.709× | FAIL | -2.64% | -9.30% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | 275 | 20.0% | -57.08% | +10.13% | -5.633× | FAIL | 1065 | 21.4% | -95.37% | +26.47% | -3.603× | FAIL | -2.06% | -7.27% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | 113 | 24.8% | -26.64% | +8.74% | -3.046× | FAIL | 458 | 26.2% | -70.10% | +27.43% | -2.556× | FAIL | -0.71% | -2.74% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | 160 | 23.1% | -42.15% | +8.74% | -4.820× | FAIL | 624 | 24.7% | -83.80% | +27.43% | -3.055× | FAIL | -1.29% | -4.20% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | 91 | 18.7% | -19.05% | +8.74% | -2.179× | FAIL | 342 | 20.8% | -64.93% | +27.43% | -2.367× | FAIL | -0.47% | -2.36% | — |
| `BTCUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | 67 | 26.9% | -4.01% | +8.74% | -0.458× | FAIL | 246 | 28.5% | -31.32% | +27.43% | -1.142× | FAIL | -0.05% | -0.77% | — |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `1h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb5,a1)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_a|(lb14,a25)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nadaraya-rq-estimate-cross` | `4h` | `mode_b|(lb8,a8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

