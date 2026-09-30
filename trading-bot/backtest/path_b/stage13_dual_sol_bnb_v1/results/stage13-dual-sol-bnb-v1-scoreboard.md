# stage13-dual-sol-bnb-v1 scoreboard (BTC-clearing PRIMARY + BNB-portable SECONDARY)

Generated (UTC): 2026-09-18T03:34:39.785736+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **BNB-portable SECONDARY:** After BTC+SOL clear, run `bnb_smoke` before declaring BNB fail; stresses BNB-after-BTC+SOL kill conditions.
- **Mandatory Smoke & Retention Tests:** btc_smoke, sol_smoke, and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-12 IDs, no CSI/PMO/Gaussian/US damp, no Super Passband/RWI/Reverse EMA/PGO, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **DeMark REI (`demark-rei-zero-cross-v1`):** DeMark Range Expansion Index. L=8 preferred; L=5, L=13. Mode A REI x 0; Mode B ±60 reclaim.
- **Khalil PZO (`khalil-pzo-zero-cross-v1`):** Price Zone Oscillator. n=14 preferred; n=10, n=20. Mode A PZO x 0; Mode B pzo > 0 quality.
- **Mobius TMO (`mobius-tmo-main-zero-v1`):** True Momentum Oscillator. (14,5,3) preferred; (10,5,3), (21,5,3). Mode A Main x 0; Mode B main > 0 quality. (NO Main x Signal).
- **Donovan Range Filter (`donovan-range-filter-flip-v1`):** DW Range Filter. (20,1.618) preferred; (14,1.618), (20,2.0). Mode A dir flip +1/-1; Mode B src > filt.
- **CLV SMA (`clv-sma-zero-cross-v1`):** Close Location Value SMA. N=14 preferred; N=8, N=21. Mode A CLVS x 0; Mode B clvs > 0 quality. Volume-free.

## PASS_6m cells (LEAD)

- `[BTCUSDT] demark-rei-zero-cross-v1` @ `4h` (mode_b|(L8)) [btc_smoke=Y, sol_smoke=Y, bnb_smoke=Y, sol_retention=—]: 6m ret=13.38% bh=8.74% ratio=1.530x wr=66.7% n=15 | full=FAIL ratio=-0.789x n=62

## All Scored Cells by Strategy

### `demark-rei-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | BTC Smoke | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | 277 | 24.9% | -58.38% | +10.13% | -5.762× | FAIL | 1107 | 26.7% | -96.98% | +26.47% | -3.663× | FAIL | -2.11% | -8.15% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | 362 | 22.7% | -71.48% | +10.13% | -7.056× | FAIL | 1409 | 23.8% | -98.92% | +26.47% | -3.737× | FAIL | -3.04% | -10.50% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | 224 | 21.9% | -50.21% | +10.13% | -4.956× | FAIL | 898 | 23.6% | -93.12% | +26.47% | -3.518× | FAIL | -1.67% | -6.23% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | 59 | 47.5% | -12.36% | +10.13% | -1.220× | FAIL | 231 | 48.5% | -49.17% | +26.47% | -1.858× | FAIL | -0.28% | -1.47% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | 67 | 35.8% | -8.41% | +8.74% | -0.962× | FAIL | 267 | 33.0% | -57.76% | +27.43% | -2.106× | FAIL | -0.15% | -1.87% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | 84 | 32.1% | -11.29% | +8.74% | -1.291× | FAIL | 342 | 32.5% | -60.63% | +27.43% | -2.210× | FAIL | -0.23% | -2.07% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | 52 | 28.8% | -0.61% | +8.74% | -0.069× | FAIL | 215 | 31.2% | -10.55% | +27.43% | -0.385× | FAIL | +0.06% | -0.02% | — |
| `BTCUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | 15 | 66.7% | +13.38% | +8.74% | 1.530× | **PASS** | 62 | 54.8% | -21.65% | +27.43% | -0.789× | FAIL | +0.39% | -0.36% | — |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | 14 | 42.9% | -17.17% | +14.30% | -1.201× | FAIL | 62 | 53.2% | -28.45% | +4.00% | -7.108× | FAIL | -0.41% | -0.34% | — |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `1h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L5)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_a|(L13)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `demark-rei-zero-cross-v1` | `4h` | `mode_b|(L8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `khalil-pzo-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | BTC Smoke | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | 524 | 13.9% | -82.01% | +10.13% | -8.094× | FAIL | 2100 | 16.1% | -99.85% | +26.47% | -3.772× | FAIL | -4.12% | -14.74% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | 622 | 12.9% | -87.76% | +10.13% | -8.662× | FAIL | 2455 | 16.0% | -99.95% | +26.47% | -3.776× | FAIL | -5.07% | -17.29% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | 429 | 12.8% | -73.96% | +10.13% | -7.300× | FAIL | 1764 | 15.1% | -99.44% | +26.47% | -3.756× | FAIL | -3.24% | -11.89% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | 524 | 13.9% | -82.01% | +10.13% | -8.094× | FAIL | 2100 | 16.1% | -99.85% | +26.47% | -3.772× | FAIL | -4.12% | -14.74% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | 130 | 19.2% | -31.24% | +8.74% | -3.573× | FAIL | 518 | 21.6% | -76.02% | +27.43% | -2.771× | FAIL | -0.87% | -3.25% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | 150 | 19.3% | -31.77% | +8.74% | -3.633× | FAIL | 612 | 21.6% | -84.29% | +27.43% | -3.073× | FAIL | -0.89% | -4.26% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | 111 | 18.9% | -22.22% | +8.74% | -2.541× | FAIL | 443 | 20.5% | -69.66% | +27.43% | -2.540× | FAIL | -0.57% | -2.69% | — |
| `BTCUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | 130 | 19.2% | -31.24% | +8.74% | -3.573× | FAIL | 518 | 21.6% | -76.02% | +27.43% | -2.771× | FAIL | -0.87% | -3.25% | — |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `1h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n10)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_a|(n20)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `khalil-pzo-zero-cross-v1` | `4h` | `mode_b|(n14,pzo0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `mobius-tmo-main-zero-v1`

| Symbol | Strategy ID | TF | Params | BTC Smoke | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | 143 | 27.3% | -27.05% | +10.13% | -2.670× | FAIL | 596 | 26.2% | -79.87% | +26.47% | -3.017× | FAIL | -0.72% | -3.69% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | 180 | 24.4% | -39.74% | +10.13% | -3.922× | FAIL | 699 | 25.3% | -83.81% | +26.47% | -3.166× | FAIL | -1.19% | -4.21% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | 120 | 30.0% | -28.80% | +10.13% | -2.843× | FAIL | 478 | 28.5% | -70.84% | +26.47% | -2.676× | FAIL | -0.78% | -2.80% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | 143 | 27.3% | -27.05% | +10.13% | -2.670× | FAIL | 596 | 26.2% | -79.87% | +26.47% | -3.017× | FAIL | -0.72% | -3.69% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | 33 | 24.2% | -3.12% | +8.74% | -0.356× | FAIL | 133 | 30.8% | +15.78% | +27.43% | 0.575× | FAIL | -0.00% | +0.61% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | 42 | 33.3% | +1.30% | +8.74% | 0.149× | FAIL | 172 | 29.7% | -18.24% | +27.43% | -0.665× | FAIL | +0.10% | -0.26% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | 26 | 26.9% | -8.64% | +8.74% | -0.989× | FAIL | 111 | 30.6% | -7.14% | +27.43% | -0.260× | FAIL | -0.15% | +0.09% | — |
| `BTCUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | 33 | 24.2% | -3.12% | +8.74% | -0.356× | FAIL | 133 | 30.8% | +15.78% | +27.43% | 0.575× | FAIL | -0.00% | +0.61% | — |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `1h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len10,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_a|(len21,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `mobius-tmo-main-zero-v1` | `4h` | `mode_b|(len14,c5,s3)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `donovan-range-filter-flip-v1`

| Symbol | Strategy ID | TF | Params | BTC Smoke | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | 151 | 31.1% | -30.98% | +10.13% | -3.057× | FAIL | 614 | 30.8% | -84.98% | +26.47% | -3.210× | FAIL | -0.85% | -4.38% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | 150 | 28.7% | -32.93% | +10.13% | -3.250× | FAIL | 611 | 29.3% | -82.29% | +26.47% | -3.109× | FAIL | -0.92% | -4.00% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | 118 | 27.1% | -33.88% | +10.13% | -3.344× | FAIL | 453 | 31.8% | -68.38% | +26.47% | -2.583× | FAIL | -0.96% | -2.59% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | 151 | 24.5% | -39.38% | +10.13% | -3.887× | FAIL | 614 | 25.2% | -89.64% | +26.47% | -3.386× | FAIL | -1.23% | -5.41% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | 41 | 29.3% | -23.92% | +8.74% | -2.736× | FAIL | 154 | 33.1% | -43.03% | +27.43% | -1.569× | FAIL | -0.65% | -1.15% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | 41 | 29.3% | -19.97% | +8.74% | -2.284× | FAIL | 159 | 32.1% | -44.95% | +27.43% | -1.639× | FAIL | -0.52% | -1.23% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | 29 | 27.6% | -13.28% | +8.74% | -1.519× | FAIL | 114 | 34.2% | -16.14% | +27.43% | -0.588× | FAIL | -0.30% | -0.16% | — |
| `BTCUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | 41 | 24.4% | -20.21% | +8.74% | -2.311× | FAIL | 154 | 29.9% | -47.48% | +27.43% | -1.731× | FAIL | -0.53% | -1.50% | — |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `1h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p14,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_a|(p20,m2.0)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `donovan-range-filter-flip-v1` | `4h` | `mode_b|(p20,m1.618)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `clv-sma-zero-cross-v1`

| Symbol | Strategy ID | TF | Params | BTC Smoke | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | 335 | 20.6% | -62.65% | +10.13% | -6.183× | FAIL | 1274 | 21.0% | -98.57% | +26.47% | -3.723× | FAIL | -2.38% | -9.82% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | 415 | 21.4% | -72.14% | +10.13% | -7.120× | FAIL | 1615 | 21.2% | -99.41% | +26.47% | -3.755× | FAIL | -3.10% | -11.81% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | 294 | 23.1% | -57.67% | +10.13% | -5.692× | FAIL | 1054 | 22.7% | -95.66% | +26.47% | -3.614× | FAIL | -2.07% | -7.31% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | 335 | 20.6% | -62.65% | +10.13% | -6.183× | FAIL | 1274 | 21.0% | -98.57% | +26.47% | -3.723× | FAIL | -2.38% | -9.82% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | 64 | 31.2% | +3.34% | +8.74% | 0.382× | FAIL | 281 | 29.5% | -40.07% | +27.43% | -1.461× | FAIL | +0.16% | -1.00% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | 108 | 28.7% | -16.16% | +8.74% | -1.848× | FAIL | 410 | 30.0% | -59.55% | +27.43% | -2.171× | FAIL | -0.38% | -2.01% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | 55 | 29.1% | +1.50% | +8.74% | 0.172× | FAIL | 227 | 31.7% | -48.10% | +27.43% | -1.753× | FAIL | +0.11% | -1.34% | — |
| `BTCUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | 64 | 31.2% | +3.34% | +8.74% | 0.382× | FAIL | 281 | 29.5% | -40.07% | +27.43% | -1.461× | FAIL | +0.16% | -1.00% | — |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `1h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N8)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_a|(N21)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `clv-sma-zero-cross-v1` | `4h` | `mode_b|(N14)` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
