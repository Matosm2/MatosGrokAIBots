# stage17-dual-sol-bnb-v1 scoreboard (SOL >= 1.2x after BTC->ETH clear PRIMARY + Denser n >> 9)

Generated (UTC): 2026-09-18T05:04:22.007075+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD — Kagi choke) -> BNB (HARD).
- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).
- **SOL >= 1.2x after BTC->ETH PRIMARY Bias:** Designed to avoid stage16 Kagi failure mode (BTC 1.202x -> ETH 2.099x -> SOL 0.807x FAIL).
- **BTC LEAD & ETH Portability:** Keep dense trades without over-damp collapse (stage12/15) or ETH wipe (stage13).
- **BNB-Survival (CRITICAL):** Withstand quieter BNB regime without quiet wipe (stage14 TTF lesson).
- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke (CRITICAL), and bnb_smoke logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-16 IDs, no BandPass/HP/3LB/SI/Kagi, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Heikin-Ashi Bias Flip (`heikin-ashi-bias-flip`):** HA close vs HA open polarity flip. confirm=1 preferred; confirm=2. Mode A single-bar flip; Mode B 2-bar confirm. Optional ATR trail 2.0. != HA-streak N>=3.
- **Blau Ergodic MDI (`blau-ergodic-mdi-signal-cross`):** Ergodic MDI x signal cross. (r=20, s=5, u=3, ul=3) preferred; r=14, r=28. Mode A MDI x sig; Mode B mdi > 0 bias. != CSI, != TSI.
- **DSS Bressert (`dss-bressert-trigger-cross`):** Double Smoothed Stochastic x Trigger cross. (PDS=10, EMA=9, Trig=5) preferred; PDS=8, PDS=14. Mode A DSS x trig; Mode B 20/80 oversold/overbought filter. != Stoch K/D, != SMI.
- **Bostian Intraday Intensity (`bostian-iii-sma-zero`):** Intraday Intensity Index SMA zero-cross. smaLen=21 preferred; smaLen=14, smaLen=34. Mode A iiiS x 0; Mode B quality hold. != CMF, != OBV, != CLV.
- **Ehlers Predictive MA (`ehlers-predictive-ma-cross`):** Fixed PMA predict x trigger cross. 7/7/4 on close preferred; src=hl2, trigger=3. Mode A predict x trig; Mode B 2-bar hold. != free WMA dual, != ZLEMA.

## PASS_6m cells (LEAD)

- `[BTCUSDT] bostian-iii-sma-zero` @ `4h` (mode_a|(sma21)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=14.29% bh=10.12% ratio=1.412x wr=27.5% n=40 | full=FAIL ratio=-0.811x n=216
- `[BTCUSDT] bostian-iii-sma-zero` @ `4h` (mode_a|(sma34)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=24.98% bh=10.12% ratio=2.468x wr=38.7% n=31 | full=FAIL ratio=-0.410x n=172
- `[BTCUSDT] bostian-iii-sma-zero` @ `4h` (mode_b|(sma21)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=14.29% bh=10.12% ratio=1.412x wr=27.5% n=40 | full=FAIL ratio=-0.811x n=216

## All Scored Cells by Strategy

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | Gate Full | Ops (6m) | Ops (full) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1) | Y | Y | Y | Y | — | 576 | 17.2% | -84.79% | +11.76% | -7.209x | **FAIL** | 2237 | 19.4% | -99.91% | +28.14% | -3.550x | FAIL | -4.55% | -15.84% | — |
| BTCUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2) | Y | Y | Y | Y | — | 373 | 18.2% | -74.05% | +11.76% | -6.297x | **FAIL** | 1434 | 23.3% | -98.81% | +28.14% | -3.512x | FAIL | -3.27% | -10.27% | — |
| BTCUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | 576 | 18.4% | -86.62% | +11.76% | -7.365x | **FAIL** | 2237 | 20.7% | -99.92% | +28.14% | -3.551x | FAIL | -4.87% | -16.20% | — |
| BTCUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | 387 | 20.2% | -77.23% | +11.76% | -6.566x | **FAIL** | 1504 | 24.7% | -99.08% | +28.14% | -3.521x | FAIL | -3.60% | -10.91% | — |
| BTCUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1) | Y | Y | Y | Y | — | 135 | 26.7% | -30.26% | +10.12% | -2.991x | **FAIL** | 545 | 27.5% | -72.31% | +28.30% | -2.555x | FAIL | -0.86% | -2.94% | — |
| BTCUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2) | Y | Y | Y | Y | — | 85 | 32.9% | -23.67% | +10.12% | -2.339x | **FAIL** | 340 | 33.2% | -51.10% | +28.30% | -1.806x | FAIL | -0.63% | -1.56% | — |
| BTCUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | 135 | 28.1% | -30.96% | +10.12% | -3.059x | **FAIL** | 545 | 28.4% | -77.72% | +28.30% | -2.746x | FAIL | -0.89% | -3.52% | — |
| BTCUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | 90 | 31.1% | -25.86% | +10.12% | -2.556x | **FAIL** | 366 | 32.0% | -65.44% | +28.30% | -2.312x | FAIL | -0.71% | -2.46% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | 292 | 25.3% | -62.78% | +11.76% | -5.338x | **FAIL** | 1135 | 26.6% | -96.66% | +28.14% | -3.435x | FAIL | -2.40% | -7.93% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | 313 | 25.2% | -65.70% | +11.76% | -5.586x | **FAIL** | 1212 | 27.2% | -97.44% | +28.14% | -3.463x | FAIL | -2.60% | -8.52% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | 283 | 24.4% | -60.88% | +11.76% | -5.177x | **FAIL** | 1088 | 26.8% | -96.14% | +28.14% | -3.416x | FAIL | -2.28% | -7.60% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | 121 | 21.5% | -33.90% | +11.76% | -2.882x | **FAIL** | 447 | 23.5% | -72.13% | +28.14% | -2.563x | FAIL | -1.02% | -3.08% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | 73 | 31.5% | -20.54% | +10.12% | -2.029x | **FAIL** | 275 | 34.9% | -51.96% | +28.30% | -1.836x | FAIL | -0.53% | -1.60% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | 78 | 37.2% | -18.77% | +10.12% | -1.855x | **FAIL** | 295 | 38.0% | -48.95% | +28.30% | -1.730x | FAIL | -0.47% | -1.43% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | 68 | 32.4% | -21.57% | +10.12% | -2.131x | **FAIL** | 265 | 34.3% | -51.35% | +28.30% | -1.814x | FAIL | -0.56% | -1.58% | — |
| BTCUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | 29 | 17.2% | -7.39% | +10.12% | -0.730x | **FAIL** | 99 | 31.3% | -2.24% | +28.30% | -0.079x | FAIL | -0.17% | +0.02% | — |
| BTCUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | 225 | 32.0% | -53.64% | +11.76% | -4.561x | **FAIL** | 910 | 30.4% | -93.46% | +28.14% | -3.321x | FAIL | -1.86% | -6.37% | — |
| BTCUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | 266 | 27.4% | -59.98% | +11.76% | -5.100x | **FAIL** | 1045 | 31.5% | -95.59% | +28.14% | -3.397x | FAIL | -2.22% | -7.29% | — |
| BTCUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | 188 | 33.0% | -42.62% | +11.76% | -3.624x | **FAIL** | 748 | 32.2% | -91.12% | +28.14% | -3.238x | FAIL | -1.34% | -5.65% | — |
| BTCUSDT | dss-bressert-trigger-cross | 1h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | 66 | 33.3% | -27.61% | +11.76% | -2.348x | **FAIL** | 269 | 41.6% | -53.06% | +28.14% | -1.886x | FAIL | -0.80% | -1.82% | — |
| BTCUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | 56 | 41.1% | -14.71% | +10.12% | -1.453x | **FAIL** | 226 | 41.2% | -33.48% | +28.30% | -1.183x | FAIL | -0.35% | -0.79% | — |
| BTCUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | 60 | 46.7% | +1.87% | +10.12% | 0.185x | **FAIL** | 252 | 42.9% | -24.62% | +28.30% | -0.870x | FAIL | +0.09% | -0.46% | — |
| BTCUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | 43 | 41.9% | -7.56% | +10.12% | -0.747x | **FAIL** | 178 | 43.3% | -18.31% | +28.30% | -0.647x | FAIL | -0.17% | -0.31% | — |
| BTCUSDT | dss-bressert-trigger-cross | 4h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | 17 | 41.2% | -11.37% | +10.12% | -1.124x | **FAIL** | 78 | 41.0% | -38.79% | +28.30% | -1.370x | FAIL | -0.29% | -1.16% | — |
| BTCUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma21) | Y | Y | Y | Y | — | 268 | 20.1% | -53.31% | +11.76% | -4.533x | **FAIL** | 964 | 21.0% | -93.22% | +28.14% | -3.313x | FAIL | -1.83% | -6.28% | — |
| BTCUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma14) | Y | Y | Y | Y | — | 290 | 21.0% | -56.22% | +11.76% | -4.780x | **FAIL** | 1212 | 21.3% | -98.08% | +28.14% | -3.486x | FAIL | -1.99% | -9.20% | — |
| BTCUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma34) | Y | Y | Y | Y | — | 182 | 27.5% | -28.04% | +11.76% | -2.384x | **FAIL** | 706 | 24.4% | -86.18% | +28.14% | -3.063x | FAIL | -0.74% | -4.60% | — |
| BTCUSDT | bostian-iii-sma-zero | 1h | mode_b|(sma21) | Y | Y | Y | Y | — | 268 | 20.1% | -53.31% | +11.76% | -4.533x | **FAIL** | 964 | 21.0% | -93.22% | +28.14% | -3.313x | FAIL | -1.83% | -6.28% | — |
| BTCUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma21) | Y | Y | Y | Y | — | 40 | 27.5% | +14.29% | +10.12% | 1.412x | **PASS** | 216 | 31.0% | -22.94% | +28.30% | -0.811x | FAIL | +0.40% | -0.32% | — |
| BTCUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma14) | Y | Y | Y | Y | — | 65 | 29.2% | -10.88% | +10.12% | -1.075x | **FAIL** | 296 | 29.1% | -47.90% | +28.30% | -1.693x | FAIL | -0.21% | -1.30% | — |
| BTCUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma34) | Y | Y | Y | Y | — | 31 | 38.7% | +24.98% | +10.12% | 2.468x | **PASS** | 172 | 32.0% | -11.61% | +28.30% | -0.410x | FAIL | +0.63% | -0.06% | — |
| BTCUSDT | bostian-iii-sma-zero | 4h | mode_b|(sma21) | Y | Y | Y | Y | — | 40 | 27.5% | +14.29% | +10.12% | 1.412x | **PASS** | 216 | 31.0% | -22.94% | +28.30% | -0.811x | FAIL | +0.40% | -0.32% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | 431 | 20.9% | -75.70% | +11.76% | -6.437x | **FAIL** | 1680 | 23.2% | -99.57% | +28.14% | -3.538x | FAIL | -3.43% | -12.53% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | 395 | 19.5% | -75.94% | +11.76% | -6.457x | **FAIL** | 1516 | 24.3% | -99.06% | +28.14% | -3.520x | FAIL | -3.45% | -10.81% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | 480 | 19.6% | -78.60% | +11.76% | -6.683x | **FAIL** | 1884 | 21.9% | -99.73% | +28.14% | -3.544x | FAIL | -3.74% | -13.54% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 1h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | 0 | 0.0% | +0.00% | +11.76% | 0.000x | **FAIL** | 0 | 0.0% | +0.00% | +28.14% | 0.000x | FAIL | +0.00% | +0.00% | TINY-N KILL (BTC 6m n=0 <= 5 despite 0.00x B&H) |
| BTCUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | 103 | 28.2% | -26.32% | +10.12% | -2.600x | **FAIL** | 410 | 29.3% | -63.73% | +28.30% | -2.252x | FAIL | -0.72% | -2.28% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | 87 | 36.8% | -15.12% | +10.12% | -1.494x | **FAIL** | 364 | 32.7% | -60.46% | +28.30% | -2.136x | FAIL | -0.36% | -2.06% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | 111 | 27.9% | -26.64% | +10.12% | -2.633x | **FAIL** | 457 | 27.8% | -69.54% | +28.30% | -2.457x | FAIL | -0.73% | -2.71% | — |
| BTCUSDT | ehlers-predictive-ma-cross | 4h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | 0 | 0.0% | +0.00% | +10.12% | 0.000x | **FAIL** | 0 | 0.0% | +0.00% | +28.30% | 0.000x | FAIL | +0.00% | +0.00% | TINY-N KILL (BTC 6m n=0 <= 5 despite 0.00x B&H) |
| ETHUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 1h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | dss-bressert-trigger-cross | 4h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma34) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | bostian-iii-sma-zero | 1h | mode_b|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma21) | Y | Y | Y | Y | OK (ETH n=66 vs BTC n=40) | 66 | 27.3% | +4.02% | +15.80% | 0.255x | **FAIL** | 242 | 30.6% | -25.68% | +5.88% | -4.369x | FAIL | +0.24% | -0.00% | ETH hard filter |
| ETHUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma34) | Y | Y | Y | Y | OK (ETH n=53 vs BTC n=31) | 53 | 35.8% | +10.09% | +15.80% | 0.639x | **FAIL** | 207 | 36.2% | -11.43% | +5.88% | -1.944x | FAIL | +0.38% | +0.44% | ETH hard filter |
| ETHUSDT | bostian-iii-sma-zero | 4h | mode_b|(sma21) | Y | Y | Y | Y | OK (ETH n=66 vs BTC n=40) | 66 | 27.3% | +4.02% | +15.80% | 0.255x | **FAIL** | 242 | 30.6% | -25.68% | +5.88% | -4.369x | FAIL | +0.24% | -0.00% | ETH hard filter |
| ETHUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 1h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| ETHUSDT | ehlers-predictive-ma-cross | 4h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 1h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | dss-bressert-trigger-cross | 4h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma34) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 1h | mode_b|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma34) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | bostian-iii-sma-zero | 4h | mode_b|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 1h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| SOLUSDT | ehlers-predictive-ma-cross | 4h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 1h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 1h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 4h | mode_a|(confirm1,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | heikin-ashi-bias-flip | 4h | mode_b|(confirm2,atr2.0) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 1h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r14,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_a|(r28,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | blau-ergodic-mdi-signal-cross | 4h | mode_b|(r20,s5,u3,ul3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 1h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 1h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS8,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 4h | mode_a|(PDS14,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | dss-bressert-trigger-cross | 4h | mode_b|(PDS10,EMA9,Trig5) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 1h | mode_a|(sma34) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 1h | mode_b|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma14) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 4h | mode_a|(sma34) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | bostian-iii-sma-zero | 4h | mode_b|(sma21) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 1h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 1h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(hl2,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 4h | mode_a|(close,7/7/3) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| BNBUSDT | ehlers-predictive-ma-cross | 4h | mode_b|(close,7/7/4) | Y | Y | Y | Y | — | — | — | — | — | — | **FAIL** | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
