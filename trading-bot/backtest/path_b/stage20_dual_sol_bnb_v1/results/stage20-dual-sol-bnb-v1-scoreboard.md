# stage20-dual-sol-bnb-v1 scoreboard (BNB-survival CRITICAL after 3-coin clear + Denser n >> 9)

Generated (UTC): 2026-09-18T06:18:54.874630+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD — TTF/HHLL choke).
- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).
- **BNB-Survival Bias:** Designed to survive quieter BNB without quiet wipe (stage14 TTF and stage19 HHLL rhyme).
- **BTC LEAD & Density:** Keep dense trades (n >> 9) without over-damp collapse (stage12/15/18) or ETH wipe (stage13/17).
- **SOL & BNB Retention:** Multi-dozen participation on SOL and quiet-wipe protection on BNB.
- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke (CRITICAL) logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-19 IDs, no DPO/PPO/VHF/FOSC/PO, no HA/MDI/DSS/III/PMA, no BandPass/HP/3LB/SI/Kagi, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no HHLL/STARC/VZO/NVI/FDI, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Volume Price Confirmation Indicator (`vpci-zero-cross`):** Dormeier VPCI x 0. (5,20) preferred; (8,20), (5,25). Mode A VPCI x 0; Mode B sig=10. != VZO / != III / != CMF / != OBV.
- **Bill Williams MFI Green/Fade Flip (`bw-mfi-green-fade-flip`):** Green+dir edge entry / Fade exit. confirmBars=1 preferred; confirmBars=2, confirmBars=3. Mode A Green+bull edge / Fade exit; Mode B not green exit. != AO / != Money Flow Index.
- **James Sibbet Demand Index (`demand-index-zero`):** Sierra Chart locked DI x 0. (10,10) preferred; (8,5), (14,14). Mode A DI x 0; Mode B hold > +5. != VZO / != Bostian III.
- **Simple 1D Kalman Filter (`kalman-estimate-cross`):** close x recursive estimate cross. (20,0.01,0.1) preferred; (14,0.01,0.05), (30,0.02,0.1). Mode A close x est; Mode B slope gate. != Nadaraya / != PMA / != SuperSmoother.
- **Chande RAVI Threshold x Dir (`ravi-threshold-dir`):** RAVI > thr x close dir. (7,65,3.0,3) preferred; (7,40,3.0,3), (5,40,2.0,1). Mode A rising edge; Mode B thr=4.0 dir=5. != dual-MA cross / != VHF / != FDI.

## PASS_6m cells (LEAD)

_none_

## Ladder Promotion Rules

1. **BTC:** Evaluated on all 40 cells (5 strategies × 2 TFs × 4 parameter sets).
2. **ETH:** Evaluated ONLY on cells with `PASS_6m == PASS` on BTC. Pruned cells marked skipped (N/A).
3. **SOL:** Evaluated ONLY on cells with `PASS_6m == PASS` on ETH.
4. **BNB:** Evaluated ONLY on cells with `PASS_6m == PASS` on SOL.

## Scoreboard Table

| Symbol | Strategy ID | TF | Params | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Retention | 6m Trades | 6m WR% | 6m Ret% | 6m B&H% | 6m xB&H | 6m Gate | Full Trades | Full WR% | Full Ret% | Full B&H% | Full xB&H | Full Gate | 6m Ops% | Full Ops% | Notes |
|--------|-------------|----|--------|-----------|-----------|-----------|-----------|-----------|-----------|--------|---------|---------|---------|---------|-------------|----------|-----------|-----------|-----------|-----------|---------|-----------|-------|
| BTCUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | 174 | 28.7% | -43.44% | 11.57% | -3.754x | FAIL | 641 | 28.1% | -84.42% | 29.23% | -2.889x | FAIL | -1.38% | -4.37% | — |
| BTCUSDT | `vpci-zero-cross` | 1h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | 174 | 28.7% | -43.44% | 11.57% | -3.754x | FAIL | 641 | 28.1% | -84.42% | 29.23% | -2.889x | FAIL | -1.38% | -4.37% | — |
| BTCUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | 145 | 24.8% | -45.82% | 11.57% | -3.959x | FAIL | 512 | 29.7% | -77.02% | 29.23% | -2.635x | FAIL | -1.47% | -3.43% | — |
| BTCUSDT | `vpci-zero-cross` | 1h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | 289 | 29.4% | -59.68% | 11.57% | -5.157x | FAIL | 1093 | 33.7% | -94.36% | 29.23% | -3.229x | FAIL | -2.21% | -6.72% | — |
| BTCUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | 53 | 43.4% | 6.23% | 10.12% | 0.616x | FAIL | 179 | 38.5% | -10.71% | 28.30% | -0.379x | FAIL | 0.22% | -0.07% | — |
| BTCUSDT | `vpci-zero-cross` | 4h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | 53 | 43.4% | 6.23% | 10.12% | 0.616x | FAIL | 179 | 38.5% | -10.71% | 28.30% | -0.379x | FAIL | 0.22% | -0.07% | — |
| BTCUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | 39 | 33.3% | -0.14% | 10.12% | -0.014x | FAIL | 140 | 30.7% | -40.83% | 28.30% | -1.443x | FAIL | 0.07% | -1.10% | — |
| BTCUSDT | `vpci-zero-cross` | 4h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | 71 | 43.7% | -14.17% | 10.12% | -1.400x | FAIL | 280 | 42.9% | -37.53% | 28.30% | -1.326x | FAIL | -0.33% | -0.95% | — |
| BTCUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf1)` | Y | Y | Y | Y | — | 313 | 26.8% | -56.45% | 11.57% | -4.878x | FAIL | 1243 | 27.0% | -97.36% | 29.23% | -3.331x | FAIL | -2.03% | -8.53% | — |
| BTCUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf2)` | Y | Y | Y | Y | — | 36 | 16.7% | -8.82% | 11.57% | -0.762x | FAIL | 141 | 27.7% | -26.83% | 29.23% | -0.918x | FAIL | -0.23% | -0.76% | — |
| BTCUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf3)` | Y | Y | Y | Y | — | 1 | 100.0% | 0.85% | 11.57% | 0.074x | FAIL | 6 | 33.3% | -0.79% | 29.23% | -0.027x | FAIL | 0.02% | -0.02% | TINY-N KILL (BTC 6m n=1 <= 5) |
| BTCUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | 370 | 18.4% | -67.31% | 11.57% | -5.816x | FAIL | 1476 | 17.6% | -98.74% | 29.23% | -3.379x | FAIL | -2.74% | -10.31% | — |
| BTCUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf1)` | Y | Y | Y | Y | — | 88 | 26.1% | -42.36% | 10.12% | -4.186x | FAIL | 354 | 36.2% | -67.72% | 28.30% | -2.393x | FAIL | -1.35% | -2.67% | — |
| BTCUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf2)` | Y | Y | Y | Y | — | 9 | 22.2% | -6.22% | 10.12% | -0.614x | FAIL | 38 | 28.9% | -10.48% | 28.30% | -0.370x | FAIL | -0.16% | -0.27% | THIN-N FLAG (BTC 6m n=9 in thin band [6..10]) |
| BTCUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf3)` | Y | Y | Y | Y | — | 2 | 50.0% | -1.45% | 10.12% | -0.143x | FAIL | 3 | 33.3% | -1.64% | 28.30% | -0.058x | FAIL | -0.04% | -0.04% | TINY-N KILL (BTC 6m n=2 <= 5) |
| BTCUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | 99 | 19.2% | -38.11% | 10.12% | -3.766x | FAIL | 405 | 29.4% | -75.59% | 28.30% | -2.671x | FAIL | -1.18% | -3.41% | — |
| BTCUSDT | `demand-index-zero` | 1h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | 340 | 17.4% | -66.03% | 11.57% | -5.706x | FAIL | 1264 | 19.1% | -97.73% | 29.23% | -3.344x | FAIL | -2.60% | -8.80% | — |
| BTCUSDT | `demand-index-zero` | 1h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | 502 | 17.1% | -79.83% | 11.57% | -6.898x | FAIL | 1939 | 18.7% | -99.77% | 29.23% | -3.414x | FAIL | -3.88% | -13.90% | — |
| BTCUSDT | `demand-index-zero` | 1h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | 279 | 17.9% | -58.99% | 11.57% | -5.098x | FAIL | 1015 | 18.3% | -94.21% | 29.23% | -3.223x | FAIL | -2.14% | -6.65% | — |
| BTCUSDT | `demand-index-zero` | 1h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | 219 | 19.2% | -47.46% | 11.57% | -4.101x | FAIL | 817 | 20.8% | -90.05% | 29.23% | -3.081x | FAIL | -1.53% | -5.42% | — |
| BTCUSDT | `demand-index-zero` | 4h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | 88 | 20.5% | -24.58% | 10.12% | -2.429x | FAIL | 318 | 21.1% | -61.95% | 28.30% | -2.189x | FAIL | -0.64% | -2.18% | — |
| BTCUSDT | `demand-index-zero` | 4h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | 116 | 25.0% | -23.36% | 10.12% | -2.309x | FAIL | 463 | 24.0% | -63.13% | 28.30% | -2.231x | FAIL | -0.60% | -2.23% | — |
| BTCUSDT | `demand-index-zero` | 4h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | 68 | 19.1% | -16.86% | 10.12% | -1.666x | FAIL | 249 | 20.5% | -49.00% | 28.30% | -1.731x | FAIL | -0.39% | -1.42% | — |
| BTCUSDT | `demand-index-zero` | 4h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | 56 | 16.1% | -15.97% | 10.12% | -1.578x | FAIL | 208 | 24.0% | -47.94% | 28.30% | -1.694x | FAIL | -0.38% | -1.44% | — |
| BTCUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | 363 | 15.7% | -66.53% | 11.57% | -5.749x | FAIL | 1473 | 16.6% | -98.77% | 29.23% | -3.379x | FAIL | -2.63% | -10.18% | — |
| BTCUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | 365 | 15.6% | -66.87% | 11.57% | -5.778x | FAIL | 1482 | 16.6% | -98.79% | 29.23% | -3.380x | FAIL | -2.65% | -10.23% | — |
| BTCUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | 258 | 15.1% | -55.57% | 11.57% | -4.802x | FAIL | 1003 | 15.5% | -94.35% | 29.23% | -3.228x | FAIL | -1.95% | -6.71% | — |
| BTCUSDT | `kalman-estimate-cross` | 1h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | 146 | 19.2% | -32.84% | 11.57% | -2.838x | FAIL | 591 | 18.6% | -77.29% | 29.23% | -2.645x | FAIL | -0.98% | -3.54% | — |
| BTCUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | 88 | 17.0% | -22.15% | 10.12% | -2.189x | FAIL | 348 | 21.0% | -59.94% | 28.30% | -2.118x | FAIL | -0.56% | -2.00% | — |
| BTCUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | 89 | 16.9% | -22.58% | 10.12% | -2.232x | FAIL | 349 | 20.9% | -59.92% | 28.30% | -2.117x | FAIL | -0.58% | -2.00% | — |
| BTCUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | 56 | 21.4% | -4.17% | 10.12% | -0.412x | FAIL | 231 | 19.5% | -38.32% | 28.30% | -1.354x | FAIL | -0.03% | -0.89% | — |
| BTCUSDT | `kalman-estimate-cross` | 4h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | 35 | 20.0% | -5.18% | 10.12% | -0.512x | FAIL | 143 | 22.4% | -45.45% | 28.30% | -1.606x | FAIL | -0.09% | -1.41% | — |
| BTCUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | 54 | 13.0% | -21.97% | 11.57% | -1.898x | FAIL | 305 | 20.7% | -69.35% | 29.23% | -2.373x | FAIL | -0.61% | -2.87% | — |
| BTCUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | 24 | 29.2% | -3.51% | 11.57% | -0.304x | FAIL | 138 | 27.5% | -36.79% | 29.23% | -1.259x | FAIL | -0.09% | -1.11% | — |
| BTCUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | 120 | 24.2% | -22.93% | 11.57% | -1.982x | FAIL | 711 | 22.4% | -88.50% | 29.23% | -3.028x | FAIL | -0.64% | -5.20% | — |
| BTCUSDT | `ravi-threshold-dir` | 1h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | 17 | 23.5% | 0.29% | 11.57% | 0.025x | FAIL | 123 | 28.5% | -34.32% | 29.23% | -1.174x | FAIL | 0.01% | -1.01% | — |
| BTCUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | 59 | 23.7% | -19.89% | 10.12% | -1.965x | FAIL | 256 | 26.6% | -57.37% | 28.30% | -2.027x | FAIL | -0.53% | -1.99% | — |
| BTCUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | 32 | 25.0% | -9.91% | 10.12% | -0.979x | FAIL | 163 | 26.4% | -42.10% | 28.30% | -1.488x | FAIL | -0.24% | -1.27% | — |
| BTCUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | 109 | 19.3% | -35.46% | 10.12% | -3.504x | FAIL | 478 | 29.1% | -73.54% | 28.30% | -2.598x | FAIL | -1.07% | -3.13% | — |
| BTCUSDT | `ravi-threshold-dir` | 4h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | 26 | 42.3% | 0.75% | 10.12% | 0.074x | FAIL | 124 | 31.5% | -17.14% | 28.30% | -0.606x | FAIL | 0.04% | -0.37% | — |
| ETHUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 1h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 1h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 4h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `vpci-zero-cross` | 4h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf2)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf2)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 1h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 1h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 1h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 1h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 4h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 4h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 4h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `demand-index-zero` | 4h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 1h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `kalman-estimate-cross` | 4h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 1h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | `ravi-threshold-dir` | 4h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 1h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 1h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 4h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `vpci-zero-cross` | 4h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf2)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf2)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 1h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 1h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 1h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 1h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 4h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 4h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 4h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `demand-index-zero` | 4h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 1h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `kalman-estimate-cross` | 4h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 1h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | `ravi-threshold-dir` | 4h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 1h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 1h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 1h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 4h | `mode_a|(s8,l20)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 4h | `mode_a|(s5,l25)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `vpci-zero-cross` | 4h | `mode_b|(s5,l20,sig10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf2)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_a|(conf3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 1h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf2)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_a|(conf3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `bw-mfi-green-fade-flip` | 4h | `mode_b|(conf1,notgreen)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 1h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 1h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 1h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 1h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 4h | `mode_a|(bs10,sm10)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 4h | `mode_a|(bs8,sm5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 4h | `mode_a|(bs14,sm14)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `demand-index-zero` | 4h | `mode_b|(bs10,sm10,hold1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 1h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 1h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len20,r0.01,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len14,r0.01,q0.05)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 4h | `mode_a|(len30,r0.02,q0.1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `kalman-estimate-cross` | 4h | `mode_b|(len20,r0.01,q0.1,slope3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 1h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 1h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l65,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s7,l40,thr3.0,dir3)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 4h | `mode_a|(s5,l40,thr2.0,dir1)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | `ravi-threshold-dir` | 4h | `mode_b|(s7,l65,thr4.0,dir5)` | Y | Y | Y | Y | — | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
