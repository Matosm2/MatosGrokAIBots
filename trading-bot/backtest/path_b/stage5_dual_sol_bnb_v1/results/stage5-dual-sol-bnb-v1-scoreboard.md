# stage5-dual-sol-bnb-v1 scoreboard (DUAL-SURVIVAL: SOL + BNB)

Generated (UTC): 2026-09-17T05:06:38.107570+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **Mandatory Smoke Tests:** Both sol_smoke and bnb_smoke are logged per strategy cell.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-4 IDs, no Decycler/ITrend/PVO/P4H, no Roofing, no EMA/RSI, SMA200, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **CTI Fast/Slow (`cti-fast-slow-threshold-v1`):** Pearson correlation vs ideal rising line over L. Defaults (20,40,0.5,0). Fast cross > buyTh, slow cross < sellTh. Sol smoke: no 15m Mode B, dead-bar filter on. BNB smoke: slowL<60 on 4H, identical params.
- **ATR% Percentile SMA Cross (`atrpct-percentile-sma-cross-v1`):** atrPct percentrank regime band + SMAxSMA (10,30)/(20,50) NOT 200. Regime leave exit on. BNB smoke requires rank_lo>=25.
- **Median / MAD Channel Break (`mad-channel-break-rvol-v1`):** Rolling median +/- k*(1.4826*MAD). Mode A breakout (close-beyond only). Light RVOL kr in {1.0, 1.2} on by default for dual smoke.
- **VIDYA Dual Cross (`vidya-dual-or-close-cross-v1`):** Chande VIDYA with locked CMO scale (|CMO|/100). Mode A (9,12)x(20,50). slopeMin ON for BNB smoke.
- **SuperSmoother Dual Cross (`supersmoother-dual-cross-v1`):** 2-pole SuperSmoother fast x slow ONLY (strictly NO High-Pass / != Roofing). Pairs (8,16)/(10,30)/(12,24). Optional Brief-2 atrPct gate.

## PASS_6m cells (LEAD)

- `[BTCUSDT] cti-fast-slow-threshold-v1` @ `4h` (mode_a|(10,20)|buy0.3) [sol_smoke=Y, bnb_smoke=Y]: 6m ret=13.20% bh=7.56% ratio=1.747x wr=40.7% n=27 | full=FAIL ratio=-0.124x n=105
- `[BTCUSDT] atrpct-percentile-sma-cross-v1` @ `1h` (mode_a|(20,50)|(40,80)|W100) [sol_smoke=Y, bnb_smoke=Y]: 6m ret=12.49% bh=7.10% ratio=1.759x wr=33.3% n=18 | full=FAIL ratio=-0.165x n=74
- `[BTCUSDT] vidya-dual-or-close-cross-v1` @ `1h` (mode_a|(9,12)x(20,50)|slope0.0003) [sol_smoke=Y, bnb_smoke=Y]: 6m ret=16.33% bh=7.10% ratio=2.302x wr=42.9% n=7 | full=PASS ratio=1.201x n=19
- `[BTCUSDT] vidya-dual-or-close-cross-v1` @ `4h` (mode_a|(9,12)x(20,50)|slope_off) [sol_smoke=Y, bnb_smoke=FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON]: 6m ret=17.95% bh=7.56% ratio=2.375x wr=40.0% n=5 | full=FAIL ratio=1.007x n=24
- `[BTCUSDT] vidya-dual-or-close-cross-v1` @ `4h` (mode_b|vidya20|slope0.0003) [sol_smoke=Y, bnb_smoke=Y]: 6m ret=16.18% bh=7.56% ratio=2.141x wr=40.0% n=5 | full=FAIL ratio=0.075x n=28
- `[ETHUSDT] vidya-dual-or-close-cross-v1` @ `4h` (mode_a|(9,12)x(20,50)|slope_off) [sol_smoke=Y, bnb_smoke=FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON]: 6m ret=22.72% bh=11.45% ratio=1.984x wr=50.0% n=4 | full=PASS ratio=9.082x n=21

## All Scored Cells by Strategy

### cti-fast-slow-threshold-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|(20,40)|buy0.5 | Y | Y | FAIL | -7.16% | 7.10% | -1.009x | 33.3% | 54 | FAIL | -1.850x | 216 | -0.11% | -1.89% |  |
| BTCUSDT | 1h | mode_a|(20,40)|buy0.3 | Y | Y | FAIL | -4.22% | 7.10% | -0.595x | 35.8% | 53 | FAIL | -1.884x | 216 | -0.03% | -1.95% |  |
| BTCUSDT | 1h | mode_a|(10,20)|buy0.5 | Y | Y | FAIL | -28.33% | 7.10% | -3.992x | 37.1% | 105 | FAIL | -2.143x | 442 | -0.72% | -2.57% |  |
| BTCUSDT | 1h | mode_a|(10,20)|buy0.3 | Y | Y | FAIL | -26.20% | 7.10% | -3.692x | 38.5% | 109 | FAIL | -2.069x | 449 | -0.66% | -2.38% |  |
| BTCUSDT | 1h | mode_b|fast20 | Y | Y | FAIL | -22.28% | 7.10% | -3.140x | 28.7% | 115 | FAIL | -2.176x | 467 | -0.57% | -2.74% |  |
| BTCUSDT | 4h | mode_a|(20,40)|buy0.5 | Y | Y | FAIL | 5.12% | 7.56% | 0.678x | 30.0% | 10 | FAIL | -1.020x | 53 | 0.26% | -0.55% |  |
| BTCUSDT | 4h | mode_a|(20,40)|buy0.3 | Y | Y | FAIL | 4.54% | 7.56% | 0.601x | 30.0% | 10 | FAIL | -0.673x | 54 | 0.25% | -0.20% |  |
| BTCUSDT | 4h | mode_a|(10,20)|buy0.5 | Y | Y | FAIL | 3.18% | 7.56% | 0.420x | 29.6% | 27 | FAIL | 0.606x | 105 | 0.15% | 0.76% |  |
| BTCUSDT | 4h | mode_a|(10,20)|buy0.3 | Y | Y | PASS | 13.20% | 7.56% | 1.747x | 40.7% | 27 | FAIL | -0.124x | 105 | 0.38% | 0.22% |  |
| BTCUSDT | 4h | mode_b|fast20 | Y | Y | FAIL | -10.82% | 7.56% | -1.432x | 25.9% | 27 | FAIL | 0.206x | 108 | -0.22% | 0.42% |  |
| ETHUSDT | 4h | mode_a|(10,20)|buy0.3 | Y | Y | FAIL | 10.53% | 11.45% | 0.920x | 41.4% | 29 | FAIL | -3.298x | 108 | 0.38% | 0.30% | Near-miss 6m (0.92x B&H) |

### atrpct-percentile-sma-cross-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|(20,50)|(25,85)|W100 | Y | Y | FAIL | 7.03% | 7.10% | 0.991x | 23.1% | 26 | FAIL | -0.083x | 99 | 0.23% | 0.04% | Near-miss 6m (0.99x B&H) |
| BTCUSDT | 1h | mode_a|(20,50)|(30,100)|W100 | Y | Y | FAIL | -1.39% | 7.10% | -0.196x | 22.6% | 31 | FAIL | -0.337x | 122 | 0.02% | -0.16% |  |
| BTCUSDT | 1h | mode_a|(20,50)|(40,80)|W100 | Y | Y | PASS | 12.49% | 7.10% | 1.759x | 33.3% | 18 | FAIL | -0.165x | 74 | 0.35% | -0.06% |  |
| BTCUSDT | 1h | mode_a|(20,50)|(25,85)|W150 | Y | Y | FAIL | 7.85% | 7.10% | 1.106x | 38.5% | 26 | FAIL | -0.747x | 109 | 0.25% | -0.58% | Near-miss 6m (1.11x B&H) |
| BTCUSDT | 1h | mode_a|(10,30)|(25,85)|W100 | Y | Y | FAIL | -14.47% | 7.10% | -2.040x | 27.9% | 43 | FAIL | -0.648x | 188 | -0.38% | -0.49% |  |
| BTCUSDT | 1h | mode_a|(10,30)|(30,100)|W100 | Y | Y | FAIL | -12.22% | 7.10% | -1.722x | 28.6% | 56 | FAIL | -1.005x | 225 | -0.28% | -0.83% |  |
| BTCUSDT | 1h | mode_b|sma20|(25,85)|W100 | Y | Y | FAIL | -30.33% | 7.10% | -4.273x | 21.9% | 137 | FAIL | -2.603x | 521 | -0.85% | -4.33% |  |
| BTCUSDT | 4h | mode_a|(20,50)|(25,85)|W100 | Y | Y | FAIL | -7.52% | 7.56% | -0.996x | 37.5% | 8 | FAIL | -0.304x | 31 | -0.19% | -0.21% |  |
| BTCUSDT | 4h | mode_a|(20,50)|(30,100)|W100 | Y | Y | FAIL | -7.97% | 7.56% | -1.055x | 37.5% | 8 | FAIL | 0.780x | 33 | -0.20% | 0.68% |  |
| BTCUSDT | 4h | mode_a|(20,50)|(40,80)|W100 | Y | Y | FAIL | -4.71% | 7.56% | -0.624x | 20.0% | 5 | FAIL | 0.251x | 22 | -0.12% | 0.21% |  |
| BTCUSDT | 4h | mode_a|(20,50)|(25,85)|W150 | Y | Y | FAIL | -10.61% | 7.56% | -1.404x | 28.6% | 7 | FAIL | -0.426x | 33 | -0.27% | -0.32% |  |
| BTCUSDT | 4h | mode_a|(10,30)|(25,85)|W100 | Y | Y | FAIL | -11.01% | 7.56% | -1.458x | 46.2% | 13 | FAIL | -1.305x | 49 | -0.28% | -1.24% |  |
| BTCUSDT | 4h | mode_a|(10,30)|(30,100)|W100 | Y | Y | FAIL | -11.52% | 7.56% | -1.524x | 46.2% | 13 | FAIL | -0.427x | 53 | -0.30% | -0.18% |  |
| BTCUSDT | 4h | mode_b|sma20|(25,85)|W100 | Y | Y | FAIL | -9.66% | 7.56% | -1.278x | 28.1% | 32 | FAIL | -1.421x | 120 | -0.24% | -1.41% |  |
| ETHUSDT | 1h | mode_a|(20,50)|(40,80)|W100 | Y | Y | FAIL | -1.09% | 11.64% | -0.094x | 11.8% | 17 | PASS | 2.470x | 75 | 0.05% | 0.64% |  |

### mad-channel-break-rvol-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|N20|k2.0|kr1.0 | Y | Y | FAIL | -10.33% | 7.10% | -1.456x | 28.9% | 76 | FAIL | -1.396x | 304 | -0.23% | -1.35% |  |
| BTCUSDT | 1h | mode_a|N20|k2.0|kr1.2 | Y | Y | FAIL | -7.97% | 7.10% | -1.123x | 30.0% | 70 | FAIL | -1.490x | 286 | -0.16% | -1.50% |  |
| BTCUSDT | 1h | mode_a|N20|k1.5|kr1.0 | Y | Y | FAIL | -16.14% | 7.10% | -2.275x | 27.0% | 89 | FAIL | -1.613x | 355 | -0.39% | -1.67% |  |
| BTCUSDT | 1h | mode_a|N20|k2.5|kr1.0 | Y | Y | FAIL | 0.82% | 7.10% | 0.115x | 35.4% | 65 | FAIL | -0.976x | 251 | 0.06% | -0.83% |  |
| BTCUSDT | 1h | mode_a|N34|k2.0|kr1.0 | Y | Y | FAIL | -10.70% | 7.10% | -1.508x | 27.3% | 55 | FAIL | -1.210x | 222 | -0.23% | -1.09% |  |
| BTCUSDT | 1h | mode_a|N34|k2.0|kr1.2 | Y | Y | FAIL | -8.45% | 7.10% | -1.191x | 28.8% | 52 | FAIL | -1.122x | 211 | -0.17% | -0.98% |  |
| BTCUSDT | 1h | mode_b|N20|k2.0|kr1.0 | FAIL: sol_smoke: Mode B first forbidden (prefer Mode A) | FAIL: bnb_smoke: Mode B fade forbidden on BNB | FAIL | -17.52% | 7.10% | -2.469x | 53.3% | 45 | FAIL | -0.751x | 207 | -0.46% | -0.64% |  |
| BTCUSDT | 4h | mode_a|N20|k2.0|kr1.0 | Y | Y | FAIL | 3.22% | 7.56% | 0.427x | 23.5% | 17 | FAIL | -0.226x | 82 | 0.13% | -0.05% |  |
| BTCUSDT | 4h | mode_a|N20|k2.0|kr1.2 | Y | Y | FAIL | 1.56% | 7.56% | 0.206x | 13.3% | 15 | FAIL | -0.126x | 69 | 0.09% | 0.02% |  |
| BTCUSDT | 4h | mode_a|N20|k1.5|kr1.0 | Y | Y | FAIL | 0.47% | 7.56% | 0.062x | 25.0% | 20 | FAIL | -0.272x | 95 | 0.06% | -0.05% |  |
| BTCUSDT | 4h | mode_a|N20|k2.5|kr1.0 | Y | Y | FAIL | 5.26% | 7.56% | 0.696x | 18.2% | 11 | FAIL | -0.249x | 69 | 0.17% | -0.07% |  |
| BTCUSDT | 4h | mode_a|N34|k2.0|kr1.0 | Y | Y | FAIL | 3.02% | 7.56% | 0.399x | 28.6% | 14 | FAIL | -0.320x | 63 | 0.13% | -0.09% |  |
| BTCUSDT | 4h | mode_a|N34|k2.0|kr1.2 | Y | Y | FAIL | 4.94% | 7.56% | 0.654x | 27.3% | 11 | FAIL | -0.027x | 55 | 0.18% | 0.15% |  |
| BTCUSDT | 4h | mode_b|N20|k2.0|kr1.0 | FAIL: sol_smoke: Mode B first forbidden (prefer Mode A) | FAIL: bnb_smoke: Mode B fade forbidden on BNB | FAIL | -8.12% | 7.56% | -1.074x | 54.5% | 11 | FAIL | -0.055x | 52 | -0.20% | 0.01% |  |

### vidya-dual-or-close-cross-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|(9,12)x(20,50)|slope0.0003 | Y | Y | PASS | 16.33% | 7.10% | 2.302x | 42.9% | 7 | PASS | 1.201x | 19 | 0.43% | 1.00% |  |
| BTCUSDT | 1h | mode_a|(9,12)x(20,50)|slope0.0006 | Y | Y | FAIL | -2.44% | 7.10% | -0.344x | 0.0% | 1 | FAIL | 0.571x | 4 | -0.06% | 0.52% |  |
| BTCUSDT | 1h | mode_a|(9,12)x(20,50)|slope_off | Y | FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON | FAIL | -7.13% | 7.10% | -1.005x | 19.2% | 26 | FAIL | -0.500x | 104 | -0.12% | -0.19% |  |
| BTCUSDT | 1h | mode_b|vidya20|slope0.0003 | Y | Y | FAIL | -5.66% | 7.10% | -0.798x | 22.2% | 9 | FAIL | -0.885x | 40 | -0.14% | -0.82% |  |
| BTCUSDT | 1h | mode_b|vidya20|slope_off | Y | FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON | FAIL | -33.40% | 7.10% | -4.707x | 13.1% | 160 | FAIL | -2.587x | 644 | -0.95% | -4.11% |  |
| BTCUSDT | 4h | mode_a|(9,12)x(20,50)|slope0.0003 | Y | Y | FAIL | 1.65% | 7.56% | 0.218x | 50.0% | 2 | PASS | 1.652x | 7 | 0.05% | 1.32% |  |
| BTCUSDT | 4h | mode_a|(9,12)x(20,50)|slope0.0006 | Y | Y | FAIL | 1.65% | 7.56% | 0.218x | 50.0% | 2 | FAIL | -0.170x | 3 | 0.05% | -0.12% |  |
| BTCUSDT | 4h | mode_a|(9,12)x(20,50)|slope_off | Y | FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON | PASS | 17.95% | 7.56% | 2.375x | 40.0% | 5 | FAIL | 1.007x | 24 | 0.47% | 1.02% |  |
| BTCUSDT | 4h | mode_b|vidya20|slope0.0003 | Y | Y | PASS | 16.18% | 7.56% | 2.141x | 40.0% | 5 | FAIL | 0.075x | 28 | 0.42% | 0.20% |  |
| BTCUSDT | 4h | mode_b|vidya20|slope_off | Y | FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON | FAIL | -7.95% | 7.56% | -1.052x | 22.0% | 41 | FAIL | -0.988x | 151 | -0.15% | -0.68% |  |
| ETHUSDT | 1h | mode_a|(9,12)x(20,50)|slope0.0003 | Y | Y | FAIL | -18.50% | 11.64% | -1.590x | 12.5% | 8 | FAIL | -4.009x | 32 | -0.50% | -0.58% |  |
| ETHUSDT | 4h | mode_a|(9,12)x(20,50)|slope_off | Y | FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON | PASS | 22.72% | 11.45% | 1.984x | 50.0% | 4 | PASS | 9.082x | 21 | 0.67% | 1.63% |  |
| ETHUSDT | 4h | mode_b|vidya20|slope0.0003 | Y | Y | FAIL | -10.47% | 11.45% | -0.915x | 12.5% | 8 | FAIL | -7.861x | 44 | -0.27% | -1.54% |  |
| SOLUSDT | 4h | mode_a|(9,12)x(20,50)|slope_off | Y | FAIL: bnb_smoke: slopeMin / flat-trade filter must be ON | FAIL | -4.57% | 11.41% | -0.401x | 25.0% | 8 | PASS | -0.360x | 23 | -0.03% | 0.54% | SOL hard filter |

### supersmoother-dual-cross-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|(10,30)|gate_off | Y | Y | FAIL | -39.07% | 7.10% | -5.506x | 25.8% | 182 | FAIL | -2.697x | 727 | -1.16% | -4.71% |  |
| BTCUSDT | 1h | mode_a|(10,30)|gate_lo25 | Y | Y | FAIL | -17.91% | 7.10% | -2.523x | 28.9% | 121 | FAIL | -1.988x | 486 | -0.43% | -2.32% |  |
| BTCUSDT | 1h | mode_a|(8,16)|gate_off | Y | Y | FAIL | -66.30% | 7.10% | -9.342x | 22.9% | 310 | FAIL | -2.992x | 1170 | -2.63% | -7.72% |  |
| BTCUSDT | 1h | mode_a|(8,16)|gate_lo25 | Y | Y | FAIL | -52.30% | 7.10% | -7.369x | 22.8% | 202 | FAIL | -2.665x | 794 | -1.79% | -4.58% |  |
| BTCUSDT | 1h | mode_a|(12,24)|gate_off | Y | Y | FAIL | -43.28% | 7.10% | -6.098x | 28.3% | 198 | FAIL | -2.766x | 792 | -1.36% | -5.16% |  |
| BTCUSDT | 1h | mode_a|(12,24)|gate_lo25 | Y | Y | FAIL | -28.05% | 7.10% | -3.952x | 29.2% | 137 | FAIL | -2.187x | 541 | -0.78% | -2.82% |  |
| BTCUSDT | 1h | mode_b|ss30|gate_off | Y | Y | FAIL | -62.69% | 7.10% | -8.834x | 17.6% | 330 | FAIL | -3.027x | 1304 | -2.36% | -8.55% |  |
| BTCUSDT | 4h | mode_a|(10,30)|gate_off | Y | Y | FAIL | 4.35% | 7.56% | 0.576x | 36.6% | 41 | FAIL | -0.474x | 174 | 0.17% | -0.20% |  |
| BTCUSDT | 4h | mode_a|(10,30)|gate_lo25 | Y | Y | FAIL | -7.69% | 7.56% | -1.018x | 37.5% | 24 | FAIL | -0.500x | 118 | -0.19% | -0.31% |  |
| BTCUSDT | 4h | mode_a|(8,16)|gate_off | Y | Y | FAIL | -22.19% | 7.56% | -2.937x | 31.9% | 72 | FAIL | -1.852x | 282 | -0.58% | -1.92% |  |
| BTCUSDT | 4h | mode_a|(8,16)|gate_lo25 | Y | Y | FAIL | -9.96% | 7.56% | -1.318x | 34.0% | 47 | FAIL | -1.547x | 189 | -0.23% | -1.47% |  |
| BTCUSDT | 4h | mode_a|(12,24)|gate_off | Y | Y | FAIL | 5.76% | 7.56% | 0.762x | 39.5% | 43 | FAIL | -0.604x | 184 | 0.21% | -0.30% |  |
| BTCUSDT | 4h | mode_a|(12,24)|gate_lo25 | Y | Y | FAIL | -9.34% | 7.56% | -1.236x | 40.7% | 27 | FAIL | -0.754x | 127 | -0.23% | -0.54% |  |
| BTCUSDT | 4h | mode_b|ss30|gate_off | Y | Y | FAIL | -16.23% | 7.56% | -2.148x | 19.3% | 83 | FAIL | -1.878x | 321 | -0.37% | -1.96% |  |

## Dual-Survival & Ladder Analysis

1. **Stop-Ladder Attrition:**
   - BTC PASS_6m: 5
   - ETH PASS_6m: 1
   - SOL PASS_6m: 0 (HARD FILTER)
   - BNB PASS_6m: 0 (HARD FILTER)

2. **Smoke Outcomes:**
   - All cells verified against mandatory sol_smoke and bnb_smoke rules.
   - Dual identical parameter constraint strictly preserved across all symbols.
