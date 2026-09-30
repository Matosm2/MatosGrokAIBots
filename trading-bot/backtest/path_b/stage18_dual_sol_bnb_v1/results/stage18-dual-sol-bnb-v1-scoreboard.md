# stage18-dual-sol-bnb-v1 scoreboard (BTC->ETH portability PRIMARY + Denser n >> 9)

Generated (UTC): 2026-09-18T05:24:55.467285+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD — Bostian/REI choke) -> SOL (HARD) -> BNB (HARD).
- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).
- **BTC->ETH Portability PRIMARY Bias:** Designed to avoid stage17 Bostian III / stage13 REI failure mode (BTC clear -> ETH wipe).
- **BTC LEAD & Density:** Keep dense trades without over-damp collapse (stage12/15) or ETH wipe (stage13/17).
- **SOL & BNB Retention:** Multi-dozen participation on SOL and quiet-wipe protection on BNB.
- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke (CRITICAL), sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-17 IDs, no HA/MDI/DSS/III/PMA, no BandPass/HP/3LB/SI/Kagi, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Detrended Price Oscillator (`dpo-zero-cross`):** displaced SMA deviation. X=20 preferred; X=14, X=28. Mode A DPO x 0; Mode B hold. != Decycler, != BandPass, != Cyber Cycle, != III.
- **Percentage Price Oscillator (`ppo-ema-signal-cross`):** %-scaled EMA spread x signal. (12,26,9) preferred; (8,21,5), (12,21,9). Mode A PPO x sig; Mode B ppo > 0. != PVO, != absolute MACD.
- **Vertical Horizontal Filter (`vhf-threshold-close-dir`):** VHF > thr x close direction. (28,0.35,3) preferred; (18,0.30,1), (28,0.40,5). Mode A rising edge; Mode B thr=0.40. != CHOP, != ADX, != RWI.
- **Forecast Oscillator (`forecast-oscillator-zero`):** %-deviation of close vs prior TSF. len=14 preferred; len=10, len=21. Mode A FOSC x 0; Mode B sig5. != LinReg channel, != PMA.
- **Projection Oscillator (`projection-oscillator-trigger-cross`):** Widner slope-adjusted stoch x trigger. (14,3) preferred; (10,3), (20,5). Mode A PO x trig; Mode B 30/70. != Stoch K/D, != DSS.

## PASS_6m cells (LEAD)

_none_

## All Scored Cells by Strategy

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | Gate Full | Ops (6m) | Ops (full) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | dpo-zero-cross | 1h | mode_a|(len20) | Y | Y | Y | Y | — | 481 | 27.4% | -71.73% | +11.76% | -6.100x | **FAIL** | 1998 | 29.5% | -99.66% | +28.14% | -3.541x | FAIL | -3.06% | -13.00% | — |
| BTCUSDT | dpo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | 585 | 26.2% | -81.42% | +11.76% | -6.923x | **FAIL** | 2386 | 27.4% | -99.91% | +28.14% | -3.551x | FAIL | -4.08% | -15.93% | — |
| BTCUSDT | dpo-zero-cross | 1h | mode_a|(len28) | Y | Y | Y | Y | — | 405 | 29.4% | -63.65% | +11.76% | -5.412x | **FAIL** | 1697 | 29.0% | -99.38% | +28.14% | -3.532x | FAIL | -2.45% | -11.72% | — |
| BTCUSDT | dpo-zero-cross | 1h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | 361 | 27.7% | -64.08% | +11.76% | -5.448x | **FAIL** | 1410 | 29.9% | -97.94% | +28.14% | -3.480x | FAIL | -2.49% | -9.06% | — |
| BTCUSDT | dpo-zero-cross | 4h | mode_a|(len20) | Y | Y | Y | Y | — | 110 | 37.3% | -26.64% | +10.12% | -2.633x | **FAIL** | 475 | 37.7% | -84.47% | +28.30% | -2.985x | FAIL | -0.71% | -4.30% | — |
| BTCUSDT | dpo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | 148 | 37.2% | -41.12% | +10.12% | -4.063x | **FAIL** | 592 | 39.4% | -81.07% | +28.30% | -2.865x | FAIL | -1.26% | -3.86% | — |
| BTCUSDT | dpo-zero-cross | 4h | mode_a|(len28) | Y | Y | Y | Y | — | 104 | 42.3% | -12.48% | +10.12% | -1.234x | **FAIL** | 413 | 40.9% | -70.17% | +28.30% | -2.479x | FAIL | -0.28% | -2.81% | — |
| BTCUSDT | dpo-zero-cross | 4h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | 80 | 38.8% | -22.48% | +10.12% | -2.222x | **FAIL** | 337 | 38.0% | -76.07% | +28.30% | -2.688x | FAIL | -0.59% | -3.31% | — |
| BTCUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | 161 | 31.1% | -30.28% | +11.76% | -2.574x | **FAIL** | 675 | 29.5% | -85.14% | +28.14% | -3.026x | FAIL | -0.86% | -4.44% | — |
| BTCUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | 278 | 24.1% | -61.32% | +11.76% | -5.214x | **FAIL** | 1065 | 26.0% | -95.93% | +28.14% | -3.409x | FAIL | -2.31% | -7.48% | — |
| BTCUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | 177 | 32.2% | -37.81% | +11.76% | -3.215x | **FAIL** | 718 | 29.7% | -86.64% | +28.14% | -3.079x | FAIL | -1.14% | -4.69% | — |
| BTCUSDT | ppo-ema-signal-cross | 1h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | 63 | 28.6% | -10.31% | +11.76% | -0.877x | **FAIL** | 265 | 28.3% | -38.41% | +28.14% | -1.365x | FAIL | -0.26% | -1.14% | — |
| BTCUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | 41 | 31.7% | -0.08% | +10.12% | -0.008x | **FAIL** | 160 | 31.9% | -15.87% | +28.30% | -0.561x | FAIL | +0.07% | -0.19% | — |
| BTCUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | 64 | 29.7% | -26.94% | +10.12% | -2.662x | **FAIL** | 261 | 33.3% | -55.38% | +28.30% | -1.957x | FAIL | -0.74% | -1.79% | — |
| BTCUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | 42 | 28.6% | +0.82% | +10.12% | 0.081x | **FAIL** | 164 | 33.5% | +4.93% | +28.30% | 0.174x | FAIL | +0.09% | +0.36% | — |
| BTCUSDT | ppo-ema-signal-cross | 4h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | 16 | 18.8% | -8.82% | +10.12% | -0.872x | **FAIL** | 59 | 23.7% | -19.60% | +28.30% | -0.693x | FAIL | -0.23% | -0.50% | — |
| BTCUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | 308 | 14.9% | -66.58% | +11.76% | -5.661x | **FAIL** | 1158 | 19.0% | -98.16% | +28.14% | -3.488x | FAIL | -2.69% | -9.42% | — |
| BTCUSDT | vhf-threshold-close-dir | 1h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | 892 | 15.8% | -92.31% | +11.76% | -7.849x | **FAIL** | 3582 | 17.5% | -100.00% | +28.14% | -3.554x | FAIL | -6.18% | -23.89% | — |
| BTCUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | 157 | 19.1% | -37.14% | +11.76% | -3.158x | **FAIL** | 602 | 21.3% | -86.70% | +28.14% | -3.081x | FAIL | -1.14% | -4.85% | — |
| BTCUSDT | vhf-threshold-close-dir | 1h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | 191 | 15.7% | -46.42% | +11.76% | -3.947x | **FAIL** | 728 | 20.1% | -90.41% | +28.14% | -3.213x | FAIL | -1.54% | -5.63% | — |
| BTCUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | 75 | 22.7% | -24.18% | +10.12% | -2.390x | **FAIL** | 314 | 27.4% | -58.16% | +28.30% | -2.055x | FAIL | -0.66% | -2.03% | — |
| BTCUSDT | vhf-threshold-close-dir | 4h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | 255 | 20.0% | -59.90% | +10.12% | -5.919x | **FAIL** | 971 | 25.8% | -95.14% | +28.30% | -3.362x | FAIL | -2.22% | -7.16% | — |
| BTCUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | 44 | 18.2% | -10.09% | +10.12% | -0.997x | **FAIL** | 178 | 32.0% | -16.32% | +28.30% | -0.577x | FAIL | -0.24% | -0.36% | — |
| BTCUSDT | vhf-threshold-close-dir | 4h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | 48 | 25.0% | -12.34% | +10.12% | -1.220x | **FAIL** | 213 | 29.6% | -35.04% | +28.30% | -1.238x | FAIL | -0.31% | -0.99% | — |
| BTCUSDT | forecast-oscillator-zero | 1h | mode_a|(len14) | Y | Y | Y | Y | — | 506 | 20.0% | -78.09% | +11.76% | -6.640x | **FAIL** | 1988 | 22.6% | -99.79% | +28.14% | -3.546x | FAIL | -3.69% | -14.08% | — |
| BTCUSDT | forecast-oscillator-zero | 1h | mode_a|(len10) | Y | Y | Y | Y | — | 611 | 21.6% | -83.82% | +11.76% | -7.127x | **FAIL** | 2383 | 23.1% | -99.91% | +28.14% | -3.551x | FAIL | -4.43% | -15.97% | — |
| BTCUSDT | forecast-oscillator-zero | 1h | mode_a|(len21) | Y | Y | Y | Y | — | 421 | 21.1% | -75.18% | +11.76% | -6.392x | **FAIL** | 1610 | 22.9% | -99.16% | +28.14% | -3.524x | FAIL | -3.38% | -11.06% | — |
| BTCUSDT | forecast-oscillator-zero | 1h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | 587 | 24.4% | -80.06% | +11.76% | -6.807x | **FAIL** | 2368 | 26.1% | -99.87% | +28.14% | -3.549x | FAIL | -3.91% | -15.07% | — |
| BTCUSDT | forecast-oscillator-zero | 4h | mode_a|(len14) | Y | Y | Y | Y | — | 110 | 32.7% | -20.33% | +10.12% | -2.009x | **FAIL** | 471 | 32.7% | -77.17% | +28.30% | -2.727x | FAIL | -0.53% | -3.43% | — |
| BTCUSDT | forecast-oscillator-zero | 4h | mode_a|(len10) | Y | Y | Y | Y | — | 151 | 27.8% | -34.80% | +10.12% | -3.438x | **FAIL** | 589 | 29.9% | -78.81% | +28.30% | -2.785x | FAIL | -1.02% | -3.59% | — |
| BTCUSDT | forecast-oscillator-zero | 4h | mode_a|(len21) | Y | Y | Y | Y | — | 94 | 33.0% | -27.87% | +10.12% | -2.754x | **FAIL** | 367 | 32.7% | -59.92% | +28.30% | -2.117x | FAIL | -0.77% | -2.02% | — |
| BTCUSDT | forecast-oscillator-zero | 4h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | 147 | 32.0% | -35.58% | +10.12% | -3.516x | **FAIL** | 588 | 33.8% | -79.37% | +28.30% | -2.804x | FAIL | -1.05% | -3.64% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | 762 | 22.3% | -87.55% | +11.76% | -7.444x | **FAIL** | 3104 | 22.1% | -99.99% | +28.14% | -3.553x | FAIL | -5.03% | -20.36% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | 786 | 22.3% | -86.72% | +11.76% | -7.374x | **FAIL** | 3259 | 22.0% | -99.99% | +28.14% | -3.553x | FAIL | -4.88% | -21.23% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | 626 | 21.2% | -85.54% | +11.76% | -7.273x | **FAIL** | 2479 | 22.3% | -99.96% | +28.14% | -3.552x | FAIL | -4.67% | -17.36% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 1h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | 125 | 27.2% | -26.91% | +11.76% | -2.288x | **FAIL** | 520 | 31.7% | -74.92% | +28.14% | -2.662x | FAIL | -0.77% | -3.37% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | 188 | 28.7% | -43.95% | +10.12% | -4.343x | **FAIL** | 761 | 31.8% | -89.45% | +28.30% | -3.160x | FAIL | -1.40% | -5.25% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | 208 | 27.4% | -47.36% | +10.12% | -4.680x | **FAIL** | 794 | 31.4% | -86.92% | +28.30% | -3.071x | FAIL | -1.55% | -4.72% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | 134 | 33.6% | -27.51% | +10.12% | -2.719x | **FAIL** | 587 | 31.2% | -84.54% | +28.30% | -2.987x | FAIL | -0.76% | -4.38% | — |
| BTCUSDT | projection-oscillator-trigger-cross | 4h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | 33 | 36.4% | -4.29% | +10.12% | -0.424x | **FAIL** | 132 | 36.4% | -27.72% | +28.30% | -0.980x | FAIL | -0.10% | -0.76% | — |
| ETHUSDT | dpo-zero-cross | 1h | mode_a|(len20) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 1h | mode_a|(len28) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 1h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 4h | mode_a|(len20) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 4h | mode_a|(len28) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dpo-zero-cross | 4h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 1h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ppo-ema-signal-cross | 4h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 1h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 1h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 4h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | vhf-threshold-close-dir | 4h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 1h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 1h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 1h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 4h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 4h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | forecast-oscillator-zero | 4h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 1h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | projection-oscillator-trigger-cross | 4h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 1h | mode_a|(len20) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 1h | mode_a|(len28) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 1h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 4h | mode_a|(len20) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 4h | mode_a|(len28) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dpo-zero-cross | 4h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 1h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ppo-ema-signal-cross | 4h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 1h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 1h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 4h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | vhf-threshold-close-dir | 4h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 1h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 1h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 1h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 4h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 4h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | forecast-oscillator-zero | 4h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 1h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | projection-oscillator-trigger-cross | 4h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 1h | mode_a|(len20) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 1h | mode_a|(len28) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 1h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 4h | mode_a|(len20) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 4h | mode_a|(len28) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dpo-zero-cross | 4h | mode_b|(len20,hold1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 1h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 1h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow26,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast8,slow21,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 4h | mode_a|(fast12,slow21,sig9) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ppo-ema-signal-cross | 4h | mode_b|(fast12,slow26,sig9,pos) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 1h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 1h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 1h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.35,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 4h | mode_a|(n18,thr0.30,dir1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 4h | mode_a|(n28,thr0.40,dir5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | vhf-threshold-close-dir | 4h | mode_b|(n28,thr0.40,dir3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 1h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 1h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 1h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 1h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 4h | mode_a|(len14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 4h | mode_a|(len10) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 4h | mode_a|(len21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | forecast-oscillator-zero | 4h | mode_b|(len14,sig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 1h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 1h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len14,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len10,trig3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 4h | mode_a|(len20,trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | projection-oscillator-trigger-cross | 4h | mode_b|(len14,trig3,ob_os) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
