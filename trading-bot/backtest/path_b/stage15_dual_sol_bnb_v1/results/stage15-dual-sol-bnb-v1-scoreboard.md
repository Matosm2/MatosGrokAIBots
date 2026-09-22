# stage15-dual-sol-bnb-v1 scoreboard (BNB-survival CRITICAL + BTC->ETH portability PRESERVED)

Generated (UTC): 2026-09-18T04:17:50.356213+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **BNB-Survival (CRITICAL):** Stage 14 wipe lesson (TTF cleared BTC->ETH->SOL then wiped BNB 0.093x). BNB survival after 3-coin clear is critical.
- **BTC->ETH Portability:** Keep portability without regressing to stage13 choke.
- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-14 IDs, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Spearman Rank (`ehlers-spearman-rank-zero`):** Rank correlation rho vs time rank. L=20 preferred; L=14, L=28. Mode A rho x 0; Mode B quality rho > 0.2.
- **Ultimate Oscillator 2025 (`ehlers-uo2025-hpdiff-zero`):** Dual-HighPass / RMS. (20,2.0) preferred; (14,2.0), (28,2.0). Mode A uo x 0; Mode B uo > 0.5 quality.
- **Correlation Cycle Real (`ehlers-corr-cycle-real-zero`):** Cosine corr Real x 0. (20,9) preferred; (14,9), (28,9). Mode A Real x 0; Mode B Real x 0 AND state != 0.
- **NET MyRSI (`ehlers-net-myrsi-zero`):** Kendall NET on MyRSI. (14,14) preferred; (10,14), (20,14). Mode A NET x 0; Mode B NET > 0.2 quality.
- **Varadi DVI (`varadi-dvi-midline-cross`):** DV Intermediate Oscillator percent-rank composite. (168,0.8) preferred; (100,0.8), (252,0.8). Mode A DVI x 0.5; Mode B DVI > 0.55 / stretch.

## PASS_6m cells (LEAD)

_none_

## All Scored Cells by Strategy

### `ehlers-spearman-rank-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | 116 | 29.3% | -23.40% | +11.37% | -2.057× | FAIL | 471 | 29.3% | -73.31% | +26.94% | -2.721× | FAIL | -0.61% | -3.02% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | 180 | 23.3% | -35.51% | +11.37% | -3.123× | FAIL | 687 | 25.3% | -84.08% | +26.94% | -3.121× | FAIL | -1.03% | -4.25% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | 86 | 32.6% | -15.81% | +11.37% | -1.390× | FAIL | 339 | 28.6% | -61.68% | +26.94% | -2.289× | FAIL | -0.35% | -2.11% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | 106 | 24.5% | -30.09% | +11.37% | -2.646× | FAIL | 425 | 28.7% | -68.19% | +26.94% | -2.531× | FAIL | -0.85% | -2.62% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | 29 | 27.6% | -12.81% | +10.12% | -1.266× | FAIL | 112 | 38.4% | +9.87% | +28.30% | 0.349× | FAIL | -0.27% | +0.50% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | 36 | 30.6% | +1.87% | +10.12% | 0.185× | FAIL | 161 | 31.1% | +5.29% | +28.30% | 0.187× | FAIL | +0.11% | +0.39% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | 24 | 29.2% | -12.49% | +10.12% | -1.234× | FAIL | 93 | 25.8% | -30.78% | +28.30% | -1.087× | FAIL | -0.27% | -0.64% | — |
| `BTCUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | 26 | 23.1% | -11.90% | +10.12% | -1.176× | FAIL | 103 | 34.0% | -11.94% | +28.30% | -0.422× | FAIL | -0.25% | -0.10% | — |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `1h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_a|(L28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-spearman-rank-zero` | `4h` | `mode_b|(L20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `ehlers-uo2025-hpdiff-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 184 | 28.8% | -46.75% | +11.37% | -4.111× | FAIL | 746 | 29.5% | -91.19% | +26.94% | -3.384× | FAIL | -1.52% | -5.66% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 272 | 27.9% | -61.06% | +11.37% | -5.370× | FAIL | 1050 | 30.4% | -95.35% | +26.94% | -3.539× | FAIL | -2.29% | -7.18% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 143 | 31.5% | -33.69% | +11.37% | -2.963× | FAIL | 551 | 33.0% | -79.31% | +26.94% | -2.943× | FAIL | -0.98% | -3.63% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 143 | 29.4% | -40.14% | +11.37% | -3.530× | FAIL | 561 | 32.1% | -80.14% | +26.94% | -2.974× | FAIL | -1.24% | -3.77% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 43 | 44.2% | -2.86% | +10.12% | -0.282× | FAIL | 175 | 42.9% | -2.73% | +28.30% | -0.096× | FAIL | -0.04% | +0.12% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 65 | 41.5% | -14.92% | +10.12% | -1.474× | FAIL | 251 | 40.2% | -37.17% | +28.30% | -1.313× | FAIL | -0.35% | -0.91% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 34 | 35.3% | -7.60% | +10.12% | -0.751× | FAIL | 127 | 37.8% | +11.43% | +28.30% | 0.404× | FAIL | -0.12% | +0.54% | — |
| `BTCUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 36 | 41.7% | -5.43% | +10.12% | -0.537× | FAIL | 138 | 42.8% | -2.16% | +28.30% | -0.076× | FAIL | -0.11% | +0.10% | — |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `1h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p14,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_a|(p28,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-uo2025-hpdiff-zero` | `4h` | `mode_b|(p20,bw2.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `ehlers-corr-cycle-real-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 219 | 30.6% | -46.76% | +11.37% | -4.112× | FAIL | 877 | 30.2% | -93.26% | +26.94% | -3.461× | FAIL | -1.53% | -6.32% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 315 | 27.0% | -65.08% | +11.37% | -5.723× | FAIL | 1237 | 28.5% | -97.45% | +26.94% | -3.617× | FAIL | -2.55% | -8.55% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 161 | 36.6% | -25.45% | +11.37% | -2.238× | FAIL | 622 | 33.8% | -74.47% | +26.94% | -2.764× | FAIL | -0.69% | -3.12% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 47 | 27.7% | -18.69% | +11.37% | -1.644× | FAIL | 178 | 31.5% | -42.80% | +26.94% | -1.588× | FAIL | -0.51% | -1.34% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 53 | 49.1% | -1.58% | +10.12% | -0.157× | FAIL | 211 | 41.7% | -14.52% | +28.30% | -0.513× | FAIL | -0.00% | -0.19% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 77 | 32.5% | -23.96% | +10.12% | -2.368× | FAIL | 300 | 35.0% | -70.51% | +28.30% | -2.491× | FAIL | -0.64% | -2.79% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 39 | 30.8% | -2.98% | +10.12% | -0.294× | FAIL | 156 | 38.5% | +14.95% | +28.30% | 0.528× | FAIL | -0.00% | +0.61% | — |
| `BTCUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | 12 | 25.0% | -7.14% | +10.12% | -0.705× | FAIL | 50 | 36.0% | -18.59% | +28.30% | -0.657× | FAIL | -0.18% | -0.47% | — |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `1h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p14,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_a|(p28,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-corr-cycle-real-zero` | `4h` | `mode_b|(p20,th9)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `ehlers-net-myrsi-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 159 | 36.5% | -33.11% | +11.37% | -2.912× | FAIL | 643 | 34.2% | -80.80% | +26.94% | -2.999× | FAIL | -0.96% | -3.81% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 195 | 33.8% | -46.79% | +11.37% | -4.114× | FAIL | 806 | 31.3% | -93.08% | +26.94% | -3.455× | FAIL | -1.52% | -6.23% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 175 | 26.3% | -37.68% | +11.37% | -3.314× | FAIL | 670 | 30.0% | -86.63% | +26.94% | -3.215× | FAIL | -1.14% | -4.68% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 145 | 38.6% | -23.82% | +11.37% | -2.095× | FAIL | 589 | 33.1% | -80.16% | +26.94% | -2.975× | FAIL | -0.64% | -3.75% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 41 | 34.1% | -8.81% | +10.12% | -0.870× | FAIL | 162 | 38.3% | -8.69% | +28.30% | -0.307× | FAIL | -0.19% | -0.03% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 49 | 42.9% | -12.18% | +10.12% | -1.204× | FAIL | 193 | 40.4% | -11.28% | +28.30% | -0.398× | FAIL | -0.29% | -0.11% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 42 | 23.8% | -19.85% | +10.12% | -1.961× | FAIL | 157 | 33.8% | -27.73% | +28.30% | -0.980× | FAIL | -0.52% | -0.61% | — |
| `BTCUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | 38 | 34.2% | -11.13% | +10.12% | -1.100× | FAIL | 144 | 40.3% | +13.91% | +28.30% | 0.492× | FAIL | -0.26% | +0.52% | — |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `1h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi10,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_a|(rsi20,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-net-myrsi-zero` | `4h` | `mode_b|(rsi14,net14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `varadi-dvi-midline-cross`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 223 | 22.0% | -50.68% | +11.37% | -4.457× | FAIL | 882 | 25.4% | -90.23% | +26.94% | -3.349× | FAIL | -1.68% | -5.40% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 225 | 22.7% | -52.30% | +11.37% | -4.599× | FAIL | 896 | 25.1% | -93.21% | +26.94% | -3.459× | FAIL | -1.78% | -6.28% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 230 | 20.0% | -51.23% | +11.37% | -4.505× | FAIL | 891 | 24.2% | -91.75% | +26.94% | -3.405× | FAIL | -1.71% | -5.81% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 223 | 22.0% | -50.68% | +11.37% | -4.457× | FAIL | 882 | 25.4% | -90.23% | +26.94% | -3.349× | FAIL | -1.68% | -5.40% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 53 | 34.0% | +1.42% | +10.12% | 0.140× | FAIL | 214 | 29.4% | -45.91% | +28.30% | -1.622× | FAIL | +0.10% | -1.31% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 55 | 36.4% | -1.69% | +10.12% | -0.167× | FAIL | 217 | 31.8% | -43.49% | +28.30% | -1.537× | FAIL | +0.03% | -1.21% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 51 | 39.2% | +7.38% | +10.12% | 0.730× | FAIL | 217 | 30.9% | -47.76% | +28.30% | -1.688× | FAIL | +0.24% | -1.40% | — |
| `BTCUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | 53 | 34.0% | +1.42% | +10.12% | 0.140× | FAIL | 214 | 29.4% | -45.91% | +28.30% | -1.622× | FAIL | +0.10% | -1.31% | — |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `1h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n100,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_a|(n252,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `varadi-dvi-midline-cross` | `4h` | `mode_b|(n168,w0.8)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

