# stage12-dual-sol-bnb-v1 scoreboard (BNB-survival-CRITICAL + dual SOL+BNB survival + density)

Generated (UTC): 2026-09-18T03:11:19.501240+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **BNB-survival-CRITICAL:** After any SOL clear, run `bnb_smoke` before declaring BNB fail; stresses BNB-after-SOL kill conditions.
- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-11 IDs, no ER-gate clones, no Super Passband/RWI/Reverse EMA/PGO, no FRAMA/HMA/McGinley, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Blau CSI Ergodic (`blau-csi-ergodic-signal-cross-v1`):** Ergodic CSI x Signal triple-smooth. (20,3) preferred; (14,3), (25,3), (20,5). Mode A CSI x sig; Mode B csi > 0 entry.
- **Ehlers Distance Coefficient Filter (`ehlers-edcf-filt-lag-cross-v1`):** EDCF filt x filt[lag]. (15,2) preferred; (10,2), (20,2), (15,3). Mode A filt x filt[lag]; Mode B price x filt.
- **Ehlers Ultimate Smoother (`ehlers-ultimate-smoother-dual-cross-v1`):** Fast x slow US dual-line cross. (10,30) preferred; (8,24), (12,40). Mode A fast x slow; Mode B close > slow.
- **Ehlers Gaussian Filter (`ehlers-gaussian-fast-slow-cross-v1`):** Fast x slow N-pole Gaussian cross. (10,30,N=2) preferred; (8,24,N=2), (12,40,N=2), (10,30,N=4). Mode A N=2; Mode B N=4.
- **Swenlin PMO (`swenlin-pmo-signal-cross-v1`):** StockCharts PMO x Signal line cross. (35,20,10) preferred; (25,20,10), (35,15,10), (35,20,8). Mode A PMO x sig; Mode B pmo > 0.

## PASS_6m cells (LEAD)

_none_

## All Scored Cells by Strategy

### `blau-csi-ergodic-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | 295 | 25.8% | -59.75% | +10.13% | -5.897× | FAIL | 1140 | 27.1% | -95.70% | +26.47% | -3.615× | FAIL | -2.21% | -7.33% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | 311 | 26.7% | -63.16% | +10.13% | -6.234× | FAIL | 1218 | 27.5% | -96.78% | +26.47% | -3.656× | FAIL | -2.42% | -7.99% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | 296 | 24.7% | -64.26% | +10.13% | -6.343× | FAIL | 1118 | 26.7% | -96.04% | +26.47% | -3.628× | FAIL | -2.50% | -7.53% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | 117 | 23.1% | -29.62% | +10.13% | -2.924× | FAIL | 450 | 23.8% | -69.42% | +26.47% | -2.622× | FAIL | -0.87% | -2.85% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | 73 | 31.5% | -25.73% | +8.74% | -2.942× | FAIL | 274 | 33.6% | -48.00% | +27.43% | -1.750× | FAIL | -0.69% | -1.40% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | 80 | 32.5% | -27.35% | +8.74% | -3.127× | FAIL | 291 | 37.5% | -40.22% | +27.43% | -1.466× | FAIL | -0.75% | -1.04% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | 72 | 31.9% | -31.77% | +8.74% | -3.633× | FAIL | 277 | 32.9% | -55.38% | +27.43% | -2.019× | FAIL | -0.90% | -1.78% | — |
| `BTCUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | 27 | 18.5% | -7.31% | +8.74% | -0.836× | FAIL | 98 | 29.6% | +0.24% | +27.43% | 0.009× | FAIL | -0.17% | +0.09% | — |
### `ehlers-edcf-filt-lag-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | 339 | 24.2% | -60.44% | +10.13% | -5.966× | FAIL | 1388 | 24.5% | -97.13% | +26.47% | -3.669× | FAIL | -2.24% | -8.28% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | 400 | 22.8% | -67.78% | +10.13% | -6.689× | FAIL | 1506 | 22.3% | -99.18% | +26.47% | -3.747× | FAIL | -2.74% | -11.11% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | 302 | 25.8% | -50.71% | +10.13% | -5.005× | FAIL | 1248 | 25.7% | -96.56% | +26.47% | -3.648× | FAIL | -1.69% | -7.84% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | 257 | 19.8% | -52.75% | +10.13% | -5.206× | FAIL | 993 | 20.8% | -94.18% | +26.47% | -3.558× | FAIL | -1.78% | -6.63% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | 78 | 30.8% | -20.63% | +8.74% | -2.359× | FAIL | 321 | 33.3% | -60.64% | +27.43% | -2.211× | FAIL | -0.49% | -2.02% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | 83 | 33.7% | -13.96% | +8.74% | -1.596× | FAIL | 365 | 31.8% | -53.35% | +27.43% | -1.945× | FAIL | -0.31% | -1.65% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | 69 | 33.3% | -4.19% | +8.74% | -0.479× | FAIL | 291 | 33.0% | -34.13% | +27.43% | -1.244× | FAIL | -0.02% | -0.75% | — |
| `BTCUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | 61 | 23.0% | -15.95% | +8.74% | -1.824× | FAIL | 228 | 25.4% | -37.33% | +27.43% | -1.361× | FAIL | -0.37% | -0.88% | — |
### `ehlers-ultimate-smoother-dual-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | 304 | 28.0% | -66.67% | +10.13% | -6.581× | FAIL | 1188 | 29.5% | -96.85% | +26.47% | -3.659× | FAIL | -2.67% | -8.06% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | 367 | 25.3% | -71.44% | +10.13% | -7.051× | FAIL | 1452 | 28.6% | -98.61% | +26.47% | -3.725× | FAIL | -3.04% | -9.92% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | 242 | 27.3% | -55.64% | +10.13% | -5.492× | FAIL | 944 | 29.7% | -92.83% | +26.47% | -3.507× | FAIL | -1.97% | -6.16% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | 287 | 28.2% | -64.33% | +10.13% | -6.350× | FAIL | 1088 | 31.0% | -95.45% | +26.47% | -3.606× | FAIL | -2.50% | -7.22% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | 73 | 37.0% | -13.13% | +8.74% | -1.502× | FAIL | 291 | 39.2% | -45.63% | +27.43% | -1.664× | FAIL | -0.30% | -1.27% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | 89 | 32.6% | -21.01% | +8.74% | -2.403× | FAIL | 367 | 33.8% | -69.37% | +27.43% | -2.529× | FAIL | -0.54% | -2.68% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | 57 | 33.3% | -16.23% | +8.74% | -1.856× | FAIL | 234 | 38.5% | -43.13% | +27.43% | -1.573× | FAIL | -0.40% | -1.19% | — |
| `BTCUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | 65 | 38.5% | -14.15% | +8.74% | -1.618× | FAIL | 260 | 41.9% | -39.75% | +27.43% | -1.449× | FAIL | -0.33% | -1.04% | — |
### `ehlers-gaussian-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | 228 | 20.6% | -48.94% | +10.13% | -4.830× | FAIL | 907 | 22.5% | -92.04% | +26.47% | -3.477× | FAIL | -1.60% | -5.91% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | 291 | 21.0% | -58.49% | +10.13% | -5.773× | FAIL | 1134 | 22.7% | -95.74% | +26.47% | -3.617× | FAIL | -2.11% | -7.35% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | 170 | 25.9% | -36.91% | +10.13% | -3.643× | FAIL | 697 | 24.4% | -83.56% | +26.47% | -3.157× | FAIL | -1.07% | -4.17% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | 203 | 22.2% | -41.60% | +10.13% | -4.105× | FAIL | 824 | 23.5% | -89.42% | +26.47% | -3.378× | FAIL | -1.27% | -5.23% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | 54 | 25.9% | -4.68% | +8.74% | -0.536× | FAIL | 209 | 26.8% | -36.36% | +27.43% | -1.326× | FAIL | -0.06% | -0.88% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | 79 | 21.5% | -18.70% | +8.74% | -2.139× | FAIL | 281 | 25.3% | -42.93% | +27.43% | -1.565× | FAIL | -0.46% | -1.17% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | 41 | 29.3% | -3.66% | +8.74% | -0.419× | FAIL | 162 | 27.2% | -22.29% | +27.43% | -0.813× | FAIL | -0.02% | -0.38% | — |
| `BTCUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | 50 | 26.0% | -3.61% | +8.74% | -0.413× | FAIL | 193 | 28.0% | -33.60% | +27.43% | -1.225× | FAIL | -0.03% | -0.76% | — |
### `swenlin-pmo-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | 123 | 30.9% | -21.64% | +10.13% | -2.136× | FAIL | 513 | 29.2% | -76.55% | +26.47% | -2.892× | FAIL | -0.56% | -3.35% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | 132 | 30.3% | -23.77% | +10.13% | -2.346× | FAIL | 551 | 29.8% | -78.29% | +26.47% | -2.957× | FAIL | -0.63% | -3.52% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | 138 | 28.3% | -27.35% | +10.13% | -2.699× | FAIL | 573 | 28.4% | -80.92% | +26.47% | -3.057× | FAIL | -0.75% | -3.84% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | 54 | 27.8% | -6.56% | +10.13% | -0.647× | FAIL | 212 | 26.9% | -35.08% | +26.47% | -1.325× | FAIL | -0.15% | -1.00% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | 32 | 21.9% | +2.53% | +8.74% | 0.289× | FAIL | 132 | 32.6% | -14.28% | +27.43% | -0.521× | FAIL | +0.15% | -0.15% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | 34 | 23.5% | +0.95% | +8.74% | 0.109× | FAIL | 141 | 31.2% | -9.14% | +27.43% | -0.333× | FAIL | +0.11% | +0.01% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | 32 | 25.0% | +2.53% | +8.74% | 0.290× | FAIL | 143 | 30.8% | -14.48% | +27.43% | -0.528× | FAIL | +0.14% | -0.16% | — |
| `BTCUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | 11 | 9.1% | -10.93% | +8.74% | -1.250× | FAIL | 43 | 34.9% | +19.33% | +27.43% | 0.705× | FAIL | -0.29% | +0.50% | — |
### `blau-csi-ergodic-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `ehlers-edcf-filt-lag-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `ehlers-ultimate-smoother-dual-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `ehlers-gaussian-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `swenlin-pmo-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
### `blau-csi-ergodic-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `ehlers-edcf-filt-lag-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `ehlers-ultimate-smoother-dual-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `ehlers-gaussian-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `swenlin-pmo-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
### `blau-csi-ergodic-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `1h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r14,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_a|(r25,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `blau-csi-ergodic-signal-cross-v1` | `4h` | `mode_b|(r20,ul3)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `ehlers-edcf-filt-lag-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `1h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L15,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L10,lag2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_a|(L20,2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-edcf-filt-lag-cross-v1` | `4h` | `mode_b|(L15,price)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `ehlers-ultimate-smoother-dual-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `1h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(10,30)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(8,24)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_a|(12,40)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-ultimate-smoother-dual-cross-v1` | `4h` | `mode_b|(10,30,close_gate)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `ehlers-gaussian-fast-slow-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `1h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(10,30,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(8,24,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_a|(12,40,N2)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-gaussian-fast-slow-cross-v1` | `4h` | `mode_b|(10,30,N4)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
### `swenlin-pmo-signal-cross-v1`

| Symbol | Strategy ID | TF | Params | SOL Smoke | BNB Smoke | SOL Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `1h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(25,20,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_a|(35,15,10)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `swenlin-pmo-signal-cross-v1` | `4h` | `mode_b|(35,20,10,pmo0)` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
