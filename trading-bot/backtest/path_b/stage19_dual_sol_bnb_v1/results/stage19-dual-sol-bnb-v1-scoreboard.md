# stage19-dual-sol-bnb-v1 scoreboard (BTC LEAD PRIMARY without over-damp + Denser n >> 9)

Generated (UTC): 2026-09-18T05:53:35.603880+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).
- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).
- **BTC LEAD PRIMARY Bias:** Designed to clear dense BTC first without stage12/15/18 over-damp or mid-cycle chop wipe.
- **BTC LEAD & Density:** Keep dense trades without over-damp collapse (stage12/15/18) or ETH wipe (stage13/17).
- **SOL & BNB Retention:** Multi-dozen participation on SOL and quiet-wipe protection on BNB.
- **Mandatory Smoke & Retention Tests:** btc_smoke (CRITICAL), eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-18 IDs, no DPO/PPO/VHF/FOSC/PO, no HA/MDI/DSS/III/PMA, no BandPass/HP/3LB/SI/Kagi, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Higher-High / Lower-Low Structure Flip (`hhll-structure-flip`):** confirmed pivot HH/HL structure polarity. lb=3 preferred; lb=2, lb=5. Mode A bullStruct edge; Mode B BOS entry. != Kagi, != 3LB, != ZigZag look-ahead.
- **STARC Bands Break Flip (`starc-bands-break-flip`):** Stoller SMA +/- k*ATR break-flip. (6,15,2.0) preferred; (5,10,1.5), (10,15,2.5). Mode A close x upper/lower; Mode B mid-exit. != Keltner (EMA center), != BB, != Donchian.
- **Volume Zone Oscillator (`vzo-zero-cross`):** Khalil signed-volume EMA ratio x 0. len=14 preferred; len=10, len=21. Mode A VZO x 0; Mode B hold > +5. != PZO (price), != Bostian III, != CMF/OBV.
- **Negative Volume Index (`nvi-ema-cross`):** Fosback NVI x EMA signal cross. sigLen=50 on 1H preferred; sigLen=21, sigLen=100. Mode A NVI x EMA; Mode B ATR trail. != OBV, != PVI.
- **Fractal Dimension Index Low Trend (`fdi-low-trend-dir`):** Matulich-corrected Sevcik FDI < thr x close direction. (30,1.50,3) preferred; (20,1.40,1), (30,1.55,5). Mode A rising edge; Mode B thr=1.45. != FRAMA, != CHOP, != VHF.

## PASS_6m cells (LEAD)

- `[BTCUSDT] hhll-structure-flip` @ `4h` (mode_a|(lb3)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=14.96% bh=10.12% ratio=1.478x wr=46.2% n=26 | full=FAIL ratio=-0.317x n=116
- `[BTCUSDT] hhll-structure-flip` @ `4h` (mode_a|(lb5)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=15.53% bh=10.12% ratio=1.535x wr=42.1% n=19 | full=FAIL ratio=0.165x n=77
- `[BTCUSDT] hhll-structure-flip` @ `4h` (mode_b|(lb3,bos)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=23.64% bh=10.12% ratio=2.336x wr=62.5% n=8 | full=PASS ratio=1.480x n=35
- `[ETHUSDT] hhll-structure-flip` @ `4h` (mode_b|(lb3,bos)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=OK (ETH n=9 vs BTC n=8)]: 6m ret=26.01% bh=15.80% ratio=1.646x wr=66.7% n=9 | full=FAIL ratio=-1.053x n=39
- `[SOLUSDT] hhll-structure-flip` @ `4h` (mode_b|(lb3,bos)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=OK (SOL n=8 vs ETH n=9)]: 6m ret=21.72% bh=17.89% ratio=1.214x wr=50.0% n=8 | full=FAIL ratio=-0.535x n=39

## Ladder Promotion Rules

1. **BTC:** Evaluated on all 40 cells (5 strategies × 2 TFs × 4 parameter sets).
2. **ETH:** Evaluated ONLY on cells with `PASS_6m == PASS` on BTC. Pruned cells marked skipped (N/A).
3. **SOL:** Evaluated ONLY on cells with `PASS_6m == PASS` on ETH.
4. **BNB:** Evaluated ONLY on cells with `PASS_6m == PASS` on SOL.

## Scoreboard Table

| Symbol | Strategy ID | TF | Params | btc_smoke | eth_smoke | sol_smoke | bnb_smoke | Retention | 6m Trades | 6m WR% | 6m Ret% | 6m B&H% | 6m xB&H | 6m Gate | Full Trades | Full WR% | Full Ret% | Full B&H% | Full xB&H | Full Gate | 6m Ops% | Full Ops% | Notes |
|--------|-------------|----|--------|-----------|-----------|-----------|-----------|-----------|-----------|--------|---------|---------|---------|---------|-------------|----------|-----------|-----------|-----------|-----------|---------|-----------|-------|
| BTCUSDT | hhll-structure-flip | 1h | mode_a|(lb3) | Y | Y | Y | Y | — | 114 | 29.8% | -20.20% | +11.76% | -1.718x | **FAIL** | 456 | 28.7% | -68.61% | +28.14% | -2.438x | FAIL | -0.54% | -2.74% | — |
| BTCUSDT | hhll-structure-flip | 1h | mode_a|(lb2) | Y | Y | Y | Y | — | 171 | 25.7% | -32.30% | +11.76% | -2.746x | **FAIL** | 643 | 26.7% | -81.20% | +28.14% | -2.886x | FAIL | -0.95% | -3.98% | — |
| BTCUSDT | hhll-structure-flip | 1h | mode_a|(lb5) | Y | Y | Y | Y | — | 77 | 35.1% | -11.04% | +11.76% | -0.938x | **FAIL** | 284 | 31.7% | -47.94% | +28.14% | -1.704x | FAIL | -0.23% | -1.48% | — |
| BTCUSDT | hhll-structure-flip | 1h | mode_b|(lb3,bos) | Y | Y | Y | Y | — | 38 | 42.1% | -4.11% | +11.76% | -0.350x | **FAIL** | 152 | 37.5% | -22.86% | +28.14% | -0.812x | FAIL | -0.10% | -0.59% | — |
| BTCUSDT | hhll-structure-flip | 4h | mode_a|(lb3) | Y | Y | Y | Y | — | 26 | 46.2% | +14.96% | +10.12% | 1.478x | **PASS** | 116 | 37.9% | -8.96% | +28.30% | -0.317x | FAIL | +0.40% | -0.09% | — |
| BTCUSDT | hhll-structure-flip | 4h | mode_a|(lb2) | Y | Y | Y | Y | — | 37 | 35.1% | +2.19% | +10.12% | 0.216x | **FAIL** | 158 | 34.2% | -21.79% | +28.30% | -0.770x | FAIL | +0.11% | -0.46% | — |
| BTCUSDT | hhll-structure-flip | 4h | mode_a|(lb5) | Y | Y | Y | Y | — | 19 | 42.1% | +15.53% | +10.12% | 1.535x | **PASS** | 77 | 36.4% | +4.68% | +28.30% | 0.165x | FAIL | +0.43% | +0.24% | — |
| BTCUSDT | hhll-structure-flip | 4h | mode_b|(lb3,bos) | Y | Y | Y | Y | — | 8 | 62.5% | +23.64% | +10.12% | 2.336x | **PASS** | 35 | 62.9% | +41.90% | +28.30% | 1.480x | PASS | +0.57% | +0.96% | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
| BTCUSDT | starc-bands-break-flip | 1h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | 16 | 37.5% | -4.74% | +11.76% | -0.403x | **FAIL** | 65 | 32.3% | -19.96% | +28.14% | -0.709x | FAIL | -0.04% | -0.27% | — |
| BTCUSDT | starc-bands-break-flip | 1h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | 26 | 34.6% | +0.16% | +11.76% | 0.014x | **FAIL** | 107 | 30.8% | -25.50% | +28.14% | -0.906x | FAIL | +0.06% | -0.51% | — |
| BTCUSDT | starc-bands-break-flip | 1h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | 16 | 37.5% | -9.72% | +11.76% | -0.826x | **FAIL** | 61 | 32.8% | -36.53% | +28.14% | -1.298x | FAIL | -0.17% | -0.86% | — |
| BTCUSDT | starc-bands-break-flip | 1h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | 31 | 29.0% | -2.16% | +11.76% | -0.183x | **FAIL** | 128 | 28.9% | -33.87% | +28.14% | -1.204x | FAIL | -0.05% | -1.00% | — |
| BTCUSDT | starc-bands-break-flip | 4h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | 1 | 100.0% | +19.16% | +10.12% | 1.894x | **FAIL** | 15 | 46.7% | +71.49% | +28.30% | 2.526x | PASS | +0.48% | +1.74% | TINY-N KILL (BTC 6m n=1 <= 5) |
| BTCUSDT | starc-bands-break-flip | 4h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | 5 | 40.0% | +18.18% | +10.12% | 1.797x | **FAIL** | 25 | 36.0% | +39.54% | +28.30% | 1.397x | PASS | +0.49% | +1.11% | TINY-N KILL (BTC 6m n=5 <= 5) |
| BTCUSDT | starc-bands-break-flip | 4h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | 2 | 50.0% | +6.37% | +10.12% | 0.630x | **FAIL** | 12 | 58.3% | +51.60% | +28.30% | 1.823x | PASS | +0.21% | +1.44% | TINY-N KILL (BTC 6m n=2 <= 5) |
| BTCUSDT | starc-bands-break-flip | 4h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | 8 | 25.0% | +5.37% | +10.12% | 0.531x | **FAIL** | 34 | 29.4% | -9.96% | +28.30% | -0.352x | FAIL | +0.15% | -0.21% | THIN-N FLAG (BTC 6m n=8 in thin band [6..10]) |
| BTCUSDT | vzo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | 397 | 15.6% | -72.46% | +11.76% | -6.161x | **FAIL** | 1577 | 17.9% | -99.16% | +28.14% | -3.524x | FAIL | -3.10% | -11.05% | — |
| BTCUSDT | vzo-zero-cross | 1h | mode_a|(len10) | Y | Y | Y | Y | — | 477 | 15.3% | -78.13% | +11.76% | -6.644x | **FAIL** | 1909 | 17.2% | -99.64% | +28.14% | -3.541x | FAIL | -3.68% | -12.92% | — |
| BTCUSDT | vzo-zero-cross | 1h | mode_a|(len21) | Y | Y | Y | Y | — | 317 | 14.8% | -64.26% | +11.76% | -5.464x | **FAIL** | 1239 | 17.1% | -97.35% | +28.14% | -3.460x | FAIL | -2.48% | -8.47% | — |
| BTCUSDT | vzo-zero-cross | 1h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | 204 | 16.7% | -46.65% | +11.76% | -3.967x | **FAIL** | 826 | 20.9% | -92.58% | +28.14% | -3.290x | FAIL | -1.49% | -6.11% | — |
| BTCUSDT | vzo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | 97 | 21.6% | -30.64% | +10.12% | -3.027x | **FAIL** | 398 | 20.6% | -72.75% | +28.30% | -2.571x | FAIL | -0.85% | -2.97% | — |
| BTCUSDT | vzo-zero-cross | 4h | mode_a|(len10) | Y | Y | Y | Y | — | 122 | 22.1% | -38.40% | +10.12% | -3.795x | **FAIL** | 465 | 22.8% | -75.60% | +28.30% | -2.671x | FAIL | -1.13% | -3.22% | — |
| BTCUSDT | vzo-zero-cross | 4h | mode_a|(len21) | Y | Y | Y | Y | — | 76 | 21.1% | -19.82% | +10.12% | -1.959x | **FAIL** | 320 | 20.3% | -65.11% | +28.30% | -2.300x | FAIL | -0.48% | -2.37% | — |
| BTCUSDT | vzo-zero-cross | 4h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | 61 | 18.0% | -29.19% | +10.12% | -2.885x | **FAIL** | 197 | 22.8% | -44.31% | +28.30% | -1.566x | FAIL | -0.80% | -1.26% | — |
| BTCUSDT | nvi-ema-cross | 1h | mode_a|(sig50) | Y | Y | Y | Y | — | 142 | 28.2% | -23.36% | +11.76% | -1.987x | **FAIL** | 607 | 28.0% | -87.02% | +28.14% | -3.092x | FAIL | -0.63% | -4.72% | — |
| BTCUSDT | nvi-ema-cross | 1h | mode_a|(sig21) | Y | Y | Y | Y | — | 225 | 25.8% | -41.70% | +11.76% | -3.546x | **FAIL** | 959 | 27.3% | -94.61% | +28.14% | -3.362x | FAIL | -1.30% | -6.80% | — |
| BTCUSDT | nvi-ema-cross | 1h | mode_a|(sig100) | Y | Y | Y | Y | — | 116 | 28.4% | -22.42% | +11.76% | -1.906x | **FAIL** | 408 | 28.2% | -73.86% | +28.14% | -2.625x | FAIL | -0.60% | -3.03% | — |
| BTCUSDT | nvi-ema-cross | 1h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | 142 | 19.0% | -42.75% | +11.76% | -3.635x | **FAIL** | 607 | 24.9% | -83.86% | +28.14% | -2.980x | FAIL | -1.38% | -4.39% | — |
| BTCUSDT | nvi-ema-cross | 4h | mode_a|(sig50) | Y | Y | Y | Y | — | 45 | 31.1% | -3.20% | +10.12% | -0.316x | **FAIL** | 125 | 40.0% | -11.77% | +28.30% | -0.416x | FAIL | -0.00% | +0.04% | — |
| BTCUSDT | nvi-ema-cross | 4h | mode_a|(sig21) | Y | Y | Y | Y | — | 66 | 36.4% | +3.45% | +10.12% | 0.341x | **FAIL** | 208 | 42.3% | +22.65% | +28.30% | 0.800x | FAIL | +0.18% | +0.93% | — |
| BTCUSDT | nvi-ema-cross | 4h | mode_a|(sig100) | Y | Y | Y | Y | — | 32 | 40.6% | +4.52% | +10.12% | 0.446x | **FAIL** | 90 | 38.9% | +8.97% | +28.30% | 0.317x | FAIL | +0.18% | +0.60% | — |
| BTCUSDT | nvi-ema-cross | 4h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | 45 | 31.1% | -13.11% | +10.12% | -1.295x | **FAIL** | 125 | 38.4% | -21.33% | +28.30% | -0.754x | FAIL | -0.34% | -0.56% | — |
| BTCUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | 468 | 17.9% | -79.20% | +11.76% | -6.734x | **FAIL** | 1868 | 20.8% | -99.76% | +28.14% | -3.545x | FAIL | -3.84% | -13.81% | — |
| BTCUSDT | fdi-low-trend-dir | 1h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | 157 | 21.0% | -30.30% | +11.76% | -2.576x | **FAIL** | 646 | 18.4% | -87.49% | +28.14% | -3.109x | FAIL | -0.89% | -5.03% | — |
| BTCUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | 480 | 16.9% | -78.00% | +11.76% | -6.632x | **FAIL** | 1830 | 19.5% | -99.74% | +28.14% | -3.545x | FAIL | -3.67% | -13.66% | — |
| BTCUSDT | fdi-low-trend-dir | 1h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | 309 | 17.8% | -66.20% | +11.76% | -5.629x | **FAIL** | 1146 | 20.1% | -98.11% | +28.14% | -3.486x | FAIL | -2.67% | -9.35% | — |
| BTCUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | 137 | 23.4% | -37.83% | +10.12% | -3.738x | **FAIL** | 493 | 26.0% | -78.22% | +28.30% | -2.764x | FAIL | -1.15% | -3.56% | — |
| BTCUSDT | fdi-low-trend-dir | 4h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | 37 | 13.5% | -16.06% | +10.12% | -1.587x | **FAIL** | 181 | 30.9% | -29.98% | +28.30% | -1.059x | FAIL | -0.42% | -0.82% | — |
| BTCUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | 124 | 26.6% | -20.97% | +10.12% | -2.072x | **FAIL** | 448 | 30.1% | -58.80% | +28.30% | -2.078x | FAIL | -0.54% | -1.97% | — |
| BTCUSDT | fdi-low-trend-dir | 4h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | 77 | 20.8% | -22.44% | +10.12% | -2.217x | **FAIL** | 319 | 25.7% | -60.47% | +28.30% | -2.137x | FAIL | -0.61% | -2.18% | — |
| ETHUSDT | hhll-structure-flip | 1h | mode_a|(lb3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | hhll-structure-flip | 1h | mode_a|(lb2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | hhll-structure-flip | 1h | mode_a|(lb5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | hhll-structure-flip | 1h | mode_b|(lb3,bos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | hhll-structure-flip | 4h | mode_a|(lb2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | hhll-structure-flip | 4h | mode_a|(lb3) | Y | Y | Y | Y | OK (ETH n=33 vs BTC n=26) | 33 | 33.3% | +18.21% | +15.80% | 1.153x | **FAIL** | 116 | 36.2% | -9.78% | +5.88% | -1.664x | FAIL | +0.55% | +0.14% | Near-miss 6m (1.15x B&H); ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | hhll-structure-flip | 4h | mode_a|(lb5) | Y | Y | Y | Y | OK (ETH n=19 vs BTC n=19) | 19 | 57.9% | +16.66% | +15.80% | 1.055x | **FAIL** | 75 | 44.0% | -40.61% | +5.88% | -6.910x | FAIL | +0.44% | -1.08% | Near-miss 6m (1.05x B&H); ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | hhll-structure-flip | 4h | mode_b|(lb3,bos) | Y | Y | Y | Y | OK (ETH n=9 vs BTC n=8) | 9 | 66.7% | +26.01% | +15.80% | 1.646x | **PASS** | 39 | 33.3% | -6.19% | +5.88% | -1.053x | FAIL | +0.63% | +0.10% | ETH hard filter (BTC->ETH portability check) |
| ETHUSDT | starc-bands-break-flip | 1h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 1h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 1h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 1h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 4h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 4h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 4h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | starc-bands-break-flip | 4h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 1h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 1h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 1h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 4h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 4h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vzo-zero-cross | 4h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 1h | mode_a|(sig50) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 1h | mode_a|(sig21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 1h | mode_a|(sig100) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 1h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 4h | mode_a|(sig50) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 4h | mode_a|(sig21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 4h | mode_a|(sig100) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | nvi-ema-cross | 4h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 1h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 1h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 4h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | fdi-low-trend-dir | 4h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 1h | mode_a|(lb3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 1h | mode_a|(lb2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 1h | mode_a|(lb5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 1h | mode_b|(lb3,bos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 4h | mode_a|(lb3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 4h | mode_a|(lb2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 4h | mode_a|(lb5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | hhll-structure-flip | 4h | mode_b|(lb3,bos) | Y | Y | Y | Y | OK (SOL n=8 vs ETH n=9) | 8 | 50.0% | +21.72% | +17.89% | 1.214x | **PASS** | 39 | 33.3% | -31.45% | -20.49% | -0.535x | FAIL | +0.56% | -0.72% | SOL hard filter |
| SOLUSDT | starc-bands-break-flip | 1h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 1h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 1h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 1h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 4h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 4h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 4h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | starc-bands-break-flip | 4h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 1h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 1h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 1h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 4h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 4h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vzo-zero-cross | 4h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 1h | mode_a|(sig50) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 1h | mode_a|(sig21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 1h | mode_a|(sig100) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 1h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 4h | mode_a|(sig50) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 4h | mode_a|(sig21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 4h | mode_a|(sig100) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | nvi-ema-cross | 4h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 1h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 1h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 4h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | fdi-low-trend-dir | 4h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 1h | mode_a|(lb3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 1h | mode_a|(lb2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 1h | mode_a|(lb5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 1h | mode_b|(lb3,bos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 4h | mode_a|(lb3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 4h | mode_a|(lb2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 4h | mode_a|(lb5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | hhll-structure-flip | 4h | mode_b|(lb3,bos) | Y | Y | Y | Y | OK (BNB n=11 vs SOL n=8) | 11 | 18.2% | -12.62% | +17.38% | -0.726x | **FAIL** | 43 | 39.5% | -27.08% | +37.55% | -0.721x | FAIL | -0.33% | -0.72% | BNB hard filter |
| BNBUSDT | starc-bands-break-flip | 1h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 1h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 1h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 1h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 4h | mode_a|(sma6,atr15,k2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 4h | mode_a|(sma5,atr10,k1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 4h | mode_a|(sma10,atr15,k2.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | starc-bands-break-flip | 4h | mode_b|(sma6,atr15,k2.0,midexit) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 1h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 1h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 1h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 4h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 4h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vzo-zero-cross | 4h | mode_b|(len14,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 1h | mode_a|(sig50) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 1h | mode_a|(sig21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 1h | mode_a|(sig100) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 1h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 4h | mode_a|(sig50) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 4h | mode_a|(sig21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 4h | mode_a|(sig100) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | nvi-ema-cross | 4h | mode_b|(sig50,trail1.5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 1h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 1h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 1h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.50,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 4h | mode_a|(n20,thr1.40,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 4h | mode_a|(n30,thr1.55,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | fdi-low-trend-dir | 4h | mode_b|(n30,thr1.45,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

## Ladder Progression Summary

- **BTCUSDT:** 40 scored, **3 PASS** (37 failed/pruned)
- **ETHUSDT:** 3 scored, **1 PASS** (2 failed/pruned)
- **SOLUSDT:** 1 scored, **1 PASS** (0 failed/pruned)
- **BNBUSDT:** 1 scored, **0 PASS** (1 failed/pruned)

**Full 4-Coin Ladder Survivors:** 0

## Smoke & Retention Diagnostic Summary

- `btc_smoke` Failures: 0
- `eth_smoke` Failures: 0
- `sol_smoke` Failures: 0
- `bnb_smoke` Failures: 0
- `tiny_n_kill` Activations (BTC n <= 5): 3
- `thin_n_flag` Warnings (BTC n in [6..10]): 2
