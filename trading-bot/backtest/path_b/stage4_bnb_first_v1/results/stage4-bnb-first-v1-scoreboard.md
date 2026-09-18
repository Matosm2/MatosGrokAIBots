# stage4-bnb-first-v1 scoreboard (BNB-survival-FIRST)

Generated (UTC): 2026-09-17T04:41:12.166783+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Mandatory BNB smoke test:** Each strategy must satisfy BNB smoke constraints before parameter cells are promoted on BNB.
- **Closed-bar only;** UTC wall-clock hour reset for P4H; long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-3 IDs, no ALMA/T3/VWMA/PHH/PWH/Decycler/ITrend, no EMA/RSI, SMA200, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **RVOL Pivot Structure (`rvol-pivot-structure-break-v1`):** RVOL volLen in {20, 50}, k in {1.2, 1.5, 2.0}. Mode A confirmed pivots (lb=rb=2,3); Mode B close > close[L] (L in {5, 10, 20}). BNB smoke requires k>=1.5, ATR% floor, 1H+.
- **EMV Gate (`emv-zero-rvol-atr-gate-v1`):** Divisor locked per symbol (BTC 1e7, ETH 1e7, SOL 1e8, BNB 1e7). eomLen in {10, 14, 20}. RVOL and ATR% participation gates. BNB smoke requires k>=1.5, atrPctMin>=0.002, 1H+.
- **PVO Gate (`pvo-gate-sma-mom-v1`):** PVO(12, 26, 9) participation gate + SMA momentum (len in {10, 20, 34}, len!=200). Exit on gate loss mandatory for BNB smoke.
- **Prior-4H H/L (`p4h-hl-accept-break-v1`):** Prior UTC 4H bucket via session-reset var trackers (no request.security). RVOL on by default for BNB (k>=1.5). 1H preferred for BNB.
- **ZLEMA x SMA (`zlema-sma-cross-v1`):** Canonical lag-compensation ZLEMA (NOT EC gain form) x SMA. Pairs in {(10,30), (20,50), (34,89)}. RVOL>=1.2 required on BNB smoke/ladder.

## PASS_6m cells (LEAD)

- `[BTCUSDT] rvol-pivot-structure-break-v1` @ `4h` (mode_b|k1.5|v20|L10) [BNB_smoke=Y]: 6m ret=9.64% bh=7.56% ratio=1.276x wr=25.0% n=12 | full=FAIL ratio=0.214x n=52
- `[BTCUSDT] emv-zero-rvol-atr-gate-v1` @ `4h` (mode_a|len14|k1.5|atr0.002) [BNB_smoke=Y]: 6m ret=13.78% bh=7.56% ratio=1.824x wr=28.6% n=7 | full=FAIL ratio=0.556x n=34
- `[BTCUSDT] emv-zero-rvol-atr-gate-v1` @ `4h` (mode_a|len14|k1.5|atr0.004) [BNB_smoke=Y]: 6m ret=13.78% bh=7.56% ratio=1.824x wr=28.6% n=7 | full=FAIL ratio=0.556x n=34
- `[BTCUSDT] emv-zero-rvol-atr-gate-v1` @ `4h` (mode_a|len10|k1.5|atr0.002) [BNB_smoke=Y]: 6m ret=14.97% bh=7.56% ratio=1.982x wr=36.4% n=11 | full=FAIL ratio=0.017x n=37
- `[BTCUSDT] emv-zero-rvol-atr-gate-v1` @ `4h` (mode_a|len20|k1.5|atr0.002) [BNB_smoke=Y]: 6m ret=22.75% bh=7.56% ratio=3.011x wr=50.0% n=6 | full=FAIL ratio=1.121x n=28
- `[BTCUSDT] emv-zero-rvol-atr-gate-v1` @ `4h` (mode_b|len14|k1.5|atr0.002) [BNB_smoke=Y]: 6m ret=21.02% bh=7.56% ratio=2.783x wr=50.0% n=16 | full=FAIL ratio=0.001x n=61
- `[BTCUSDT] zlema-sma-cross-v1` @ `1h` (mode_a|(34,89)|k1.2) [BNB_smoke=Y]: 6m ret=21.40% bh=7.37% ratio=2.902x wr=44.4% n=9 | full=FAIL ratio=1.166x n=57
- `[BTCUSDT] zlema-sma-cross-v1` @ `1h` (mode_b|(20,50)|k1.2) [BNB_smoke=Y]: 6m ret=14.65% bh=7.37% ratio=1.987x wr=44.0% n=25 | full=FAIL ratio=-0.518x n=131
- `[BTCUSDT] zlema-sma-cross-v1` @ `4h` (mode_a|(10,30)|k1.2) [BNB_smoke=Y]: 6m ret=19.22% bh=7.56% ratio=2.544x wr=50.0% n=8 | full=PASS ratio=1.676x n=44
- `[BTCUSDT] zlema-sma-cross-v1` @ `4h` (mode_a|(20,50)|k_off) [BNB_smoke=Y]: 6m ret=10.23% bh=7.56% ratio=1.355x wr=28.6% n=14 | full=FAIL ratio=-0.648x n=69
- `[ETHUSDT] rvol-pivot-structure-break-v1` @ `4h` (mode_b|k1.5|v20|L10) [BNB_smoke=Y]: 6m ret=21.54% bh=11.45% ratio=1.882x wr=35.0% n=20 | full=PASS ratio=9.319x n=72
- `[ETHUSDT] zlema-sma-cross-v1` @ `1h` (mode_a|(34,89)|k1.2) [BNB_smoke=Y]: 6m ret=15.54% bh=11.22% ratio=1.385x wr=33.3% n=18 | full=PASS ratio=2.539x n=66
- `[ETHUSDT] zlema-sma-cross-v1` @ `4h` (mode_a|(10,30)|k1.2) [BNB_smoke=Y]: 6m ret=16.33% bh=11.45% ratio=1.426x wr=33.3% n=15 | full=PASS ratio=2.291x n=54

## All Scored Cells by Strategy

### rvol-pivot-structure-break-v1

| symbol | tf | mode/params | BNB_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|-----------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|k1.2|v20|p2` | Y | FAIL | -21.87% | 7.37% | -2.966× | 25.2% | 107 | FAIL | -2.290× | 463 | -0.61% | -3.06% |  |
| BTCUSDT | 1h | `mode_a|k1.5|v20|p2` | Y | FAIL | -16.32% | 7.37% | -2.214× | 25.0% | 88 | FAIL | -1.844× | 354 | -0.44% | -2.09% |  |
| BTCUSDT | 1h | `mode_a|k2.0|v20|p2` | Y | FAIL | -6.69% | 7.37% | -0.908× | 28.3% | 53 | FAIL | -1.447× | 225 | -0.17% | -1.47% |  |
| BTCUSDT | 1h | `mode_a|k1.5|v50|p2` | Y | FAIL | -10.77% | 7.37% | -1.460× | 28.8% | 73 | FAIL | -1.734× | 321 | -0.28% | -1.90% |  |
| BTCUSDT | 1h | `mode_a|k1.5|v20|p3` | Y | FAIL | -10.91% | 7.37% | -1.480× | 28.4% | 81 | FAIL | -1.787× | 327 | -0.28% | -1.98% |  |
| BTCUSDT | 1h | `mode_b|k1.2|v20|L5` | Y | FAIL | -37.06% | 7.37% | -5.026× | 16.5% | 109 | FAIL | -2.329× | 415 | -1.14% | -3.17% |  |
| BTCUSDT | 1h | `mode_b|k1.5|v20|L10` | Y | FAIL | -21.86% | 7.37% | -2.965× | 21.7% | 60 | FAIL | -1.846× | 218 | -0.61% | -2.09% |  |
| BTCUSDT | 1h | `mode_b|k2.0|v20|L20` | Y | FAIL | 6.34% | 7.37% | 0.860× | 26.7% | 30 | FAIL | -0.872× | 114 | 0.20% | -0.72% |  |
| BTCUSDT | 1h | `mode_b|k1.5|v50|L10` | Y | FAIL | -25.48% | 7.37% | -3.456× | 16.4% | 55 | FAIL | -1.796× | 198 | -0.72% | -2.00% |  |
| BTCUSDT | 4h | `mode_a|k1.2|v20|p2` | Y | FAIL | -4.79% | 7.56% | -0.634× | 20.0% | 30 | FAIL | -1.083× | 130 | -0.10% | -0.98% |  |
| BTCUSDT | 4h | `mode_a|k1.5|v20|p2` | Y | FAIL | 0.61% | 7.56% | 0.081× | 23.8% | 21 | FAIL | -0.762× | 91 | 0.03% | -0.63% |  |
| BTCUSDT | 4h | `mode_a|k2.0|v20|p2` | Y | FAIL | 3.87% | 7.56% | 0.513× | 16.7% | 12 | FAIL | -0.628× | 56 | 0.11% | -0.51% |  |
| BTCUSDT | 4h | `mode_a|k1.5|v50|p2` | Y | FAIL | 0.86% | 7.56% | 0.113× | 16.7% | 18 | FAIL | -0.714× | 83 | 0.04% | -0.59% |  |
| BTCUSDT | 4h | `mode_a|k1.5|v20|p3` | Y | FAIL | 7.80% | 7.56% | 1.032× | 30.0% | 20 | FAIL | -0.702× | 88 | 0.21% | -0.57% | Near-miss 6m (1.03x B&H) |
| BTCUSDT | 4h | `mode_b|k1.2|v20|L5` | Y | FAIL | 6.01% | 7.56% | 0.796× | 41.9% | 31 | FAIL | -1.260× | 111 | 0.17% | -1.19% |  |
| BTCUSDT | 4h | `mode_b|k1.5|v20|L10` | Y | **PASS** | 9.64% | 7.56% | 1.276× | 25.0% | 12 | FAIL | 0.214× | 52 | 0.27% | 0.25% |  |
| BTCUSDT | 4h | `mode_b|k2.0|v20|L20` | Y | FAIL | 0.23% | 7.56% | 0.031× | 33.3% | 3 | FAIL | 0.083× | 15 | 0.01% | 0.11% |  |
| BTCUSDT | 4h | `mode_b|k1.5|v50|L10` | Y | FAIL | -9.36% | 7.56% | -1.239× | 18.2% | 11 | FAIL | -0.878× | 45 | -0.24% | -0.77% |  |
| ETHUSDT | 4h | `mode_b|k1.5|v20|L10` | Y | **PASS** | 21.54% | 11.45% | 1.882× | 35.0% | 20 | **PASS** | 9.319× | 72 | 0.57% | 1.43% |  |
| SOLUSDT | 4h | `mode_b|k1.5|v20|L10` | Y | FAIL | 13.56% | 11.41% | 1.188× | 25.0% | 16 | **PASS** | 1.015× | 60 | 0.40% | -0.54% | Near-miss 6m (1.19x B&H); SOL hard filter |

### emv-zero-rvol-atr-gate-v1

| symbol | tf | mode/params | BNB_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|-----------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|len14|k1.0|atr0.002` | Y | FAIL | -13.68% | 7.37% | -1.855× | 27.4% | 95 | FAIL | -1.695× | 356 | -0.32% | -1.74% |  |
| BTCUSDT | 1h | `mode_a|len14|k1.5|atr0.002` | Y | FAIL | -2.76% | 7.37% | -0.374× | 31.6% | 57 | FAIL | -1.659× | 191 | -0.02% | -1.74% |  |
| BTCUSDT | 1h | `mode_a|len14|k1.5|atr0.004` | Y | FAIL | -1.87% | 7.37% | -0.254× | 32.1% | 53 | FAIL | -1.615× | 177 | -0.00% | -1.67% |  |
| BTCUSDT | 1h | `mode_a|len10|k1.5|atr0.002` | Y | FAIL | -17.61% | 7.37% | -2.388× | 30.2% | 53 | FAIL | -1.672× | 199 | -0.47% | -1.79% |  |
| BTCUSDT | 1h | `mode_a|len20|k1.5|atr0.002` | Y | FAIL | 0.50% | 7.37% | 0.067× | 30.2% | 43 | FAIL | -1.383× | 156 | 0.06% | -1.33% |  |
| BTCUSDT | 1h | `mode_a|len14|k1.0|atr_off` | Y | FAIL | -14.18% | 7.37% | -1.923× | 26.8% | 97 | FAIL | -1.701× | 359 | -0.33% | -1.75% |  |
| BTCUSDT | 1h | `mode_b|len14|k1.5|atr0.002` | Y | FAIL | -17.71% | 7.37% | -2.402× | 27.1% | 70 | FAIL | -1.640× | 272 | -0.48% | -1.74% |  |
| BTCUSDT | 4h | `mode_a|len14|k1.0|atr0.002` | Y | FAIL | 2.72% | 7.56% | 0.360× | 23.5% | 17 | FAIL | 0.006× | 68 | 0.12% | 0.11% |  |
| BTCUSDT | 4h | `mode_a|len14|k1.5|atr0.002` | Y | **PASS** | 13.78% | 7.56% | 1.824× | 28.6% | 7 | FAIL | 0.556× | 34 | 0.37% | 0.48% |  |
| BTCUSDT | 4h | `mode_a|len14|k1.5|atr0.004` | Y | **PASS** | 13.78% | 7.56% | 1.824× | 28.6% | 7 | FAIL | 0.556× | 34 | 0.37% | 0.48% |  |
| BTCUSDT | 4h | `mode_a|len10|k1.5|atr0.002` | Y | **PASS** | 14.97% | 7.56% | 1.982× | 36.4% | 11 | FAIL | 0.017× | 37 | 0.40% | 0.08% |  |
| BTCUSDT | 4h | `mode_a|len20|k1.5|atr0.002` | Y | **PASS** | 22.75% | 7.56% | 3.011× | 50.0% | 6 | FAIL | 1.121× | 28 | 0.57% | 0.88% |  |
| BTCUSDT | 4h | `mode_a|len14|k1.0|atr_off` | Y | FAIL | 2.72% | 7.56% | 0.360× | 23.5% | 17 | FAIL | 0.006× | 68 | 0.12% | 0.11% |  |
| BTCUSDT | 4h | `mode_b|len14|k1.5|atr0.002` | Y | **PASS** | 21.02% | 7.56% | 2.783× | 50.0% | 16 | FAIL | 0.001× | 61 | 0.51% | 0.06% |  |
| ETHUSDT | 4h | `mode_a|len14|k1.5|atr0.002` | Y | FAIL | -16.60% | 11.45% | -1.450× | 21.4% | 14 | FAIL | -4.931× | 42 | -0.44% | -0.78% |  |
| ETHUSDT | 4h | `mode_a|len14|k1.5|atr0.004` | Y | FAIL | -16.60% | 11.45% | -1.450× | 21.4% | 14 | FAIL | -4.931× | 42 | -0.44% | -0.78% |  |
| ETHUSDT | 4h | `mode_a|len10|k1.5|atr0.002` | Y | FAIL | 8.69% | 11.45% | 0.759× | 33.3% | 12 | **PASS** | 6.284× | 52 | 0.28% | 1.03% |  |
| ETHUSDT | 4h | `mode_a|len20|k1.5|atr0.002` | Y | FAIL | 7.01% | 11.45% | 0.612× | 11.1% | 9 | **PASS** | 2.061× | 42 | 0.27% | 0.65% |  |
| ETHUSDT | 4h | `mode_b|len14|k1.5|atr0.002` | Y | FAIL | -4.79% | 11.45% | -0.418× | 26.7% | 15 | **PASS** | 2.399× | 69 | -0.12% | 0.60% |  |

### pvo-gate-sma-mom-v1

| symbol | tf | mode/params | BNB_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|-----------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|pvo_pos|len10|exit_loss_on` | Y | FAIL | -37.65% | 7.37% | -5.107× | 18.9% | 132 | FAIL | -2.475× | 537 | -1.16% | -3.61% |  |
| BTCUSDT | 1h | `mode_a|pvo_pos|len20|exit_loss_on` | Y | FAIL | -29.37% | 7.37% | -3.984× | 18.9% | 90 | FAIL | -2.188× | 357 | -0.86% | -2.80% |  |
| BTCUSDT | 1h | `mode_a|pvo_pos|len34|exit_loss_on` | Y | FAIL | -25.27% | 7.37% | -3.427× | 19.5% | 77 | FAIL | -1.902× | 281 | -0.72% | -2.20% |  |
| BTCUSDT | 1h | `mode_a|pvo_sig|len20|exit_loss_on` | Y | FAIL | -27.64% | 7.37% | -3.749× | 21.3% | 89 | FAIL | -2.374× | 333 | -0.80% | -3.32% |  |
| BTCUSDT | 1h | `mode_b|pvo_pos|len20|exit_loss_on` | Y | FAIL | -39.14% | 7.37% | -5.308× | 21.8% | 170 | FAIL | -2.601× | 665 | -1.21% | -4.02% |  |
| BTCUSDT | 1h | `mode_a|pvo_pos|len20|exit_loss_off` | Y | FAIL | -32.59% | 7.37% | -4.421× | 20.0% | 90 | FAIL | -2.376× | 357 | -0.97% | -3.28% |  |
| BTCUSDT | 1h | `mode_a|pvo_pos|len50|exit_loss_on` | Y | FAIL | -18.90% | 7.37% | -2.564× | 20.8% | 72 | FAIL | -1.607× | 237 | -0.52% | -1.70% |  |
| BTCUSDT | 4h | `mode_a|pvo_pos|len10|exit_loss_on` | Y | FAIL | -15.14% | 7.56% | -2.004× | 32.4% | 34 | FAIL | -0.990× | 139 | -0.40% | -0.87% |  |
| BTCUSDT | 4h | `mode_a|pvo_pos|len20|exit_loss_on` | Y | FAIL | -9.32% | 7.56% | -1.234× | 31.6% | 19 | FAIL | -0.780× | 86 | -0.24% | -0.65% |  |
| BTCUSDT | 4h | `mode_a|pvo_pos|len34|exit_loss_on` | Y | FAIL | -8.79% | 7.56% | -1.164× | 27.3% | 22 | FAIL | -0.153× | 85 | -0.22% | -0.08% |  |
| BTCUSDT | 4h | `mode_a|pvo_sig|len20|exit_loss_on` | Y | FAIL | -9.13% | 7.56% | -1.208× | 39.1% | 23 | FAIL | -0.858× | 87 | -0.23% | -0.73% |  |
| BTCUSDT | 4h | `mode_b|pvo_pos|len20|exit_loss_on` | Y | FAIL | -12.94% | 7.56% | -1.712× | 26.5% | 49 | FAIL | -1.048× | 188 | -0.32% | -0.84% |  |
| BTCUSDT | 4h | `mode_a|pvo_pos|len20|exit_loss_off` | Y | FAIL | -12.38% | 7.56% | -1.639× | 26.3% | 19 | FAIL | -0.495× | 86 | -0.32% | -0.28% |  |
| BTCUSDT | 4h | `mode_a|pvo_pos|len50|exit_loss_on` | Y | FAIL | -16.67% | 7.56% | -2.206× | 21.1% | 19 | FAIL | -0.706× | 72 | -0.45% | -0.59% |  |

### p4h-hl-accept-break-v1

| symbol | tf | mode/params | BNB_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|-----------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 15m | `mode_a|k1.5|1trade` | Y | FAIL | -48.33% | 5.66% | -8.543× | 17.1% | 234 | FAIL | -2.897× | 920 | -1.62% | -6.13% |  |
| BTCUSDT | 15m | `mode_a|k1.2|1trade` | Y | FAIL | -59.02% | 5.66% | -10.433× | 14.6% | 287 | FAIL | -3.035× | 1139 | -2.19% | -8.07% |  |
| BTCUSDT | 15m | `mode_a|k_off|1trade` | Y | FAIL | -74.40% | 5.66% | -13.152× | 12.3% | 405 | FAIL | -3.125× | 1665 | -3.33% | -12.22% |  |
| BTCUSDT | 15m | `mode_b|k1.5|1trade` | Y | FAIL | -56.77% | 5.66% | -10.035× | 16.1% | 286 | FAIL | -3.037× | 1163 | -2.06% | -8.10% |  |
| BTCUSDT | 15m | `mode_a|k1.5|multi` | Y | FAIL | -53.33% | 5.66% | -9.427× | 17.4% | 258 | FAIL | -2.943× | 1001 | -1.87% | -6.61% |  |
| BTCUSDT | 1h | `mode_a|k1.5|1trade` | Y | FAIL | -20.06% | 7.37% | -2.720× | 28.8% | 111 | FAIL | -2.192× | 449 | -0.55% | -2.82% |  |
| BTCUSDT | 1h | `mode_a|k1.2|1trade` | Y | FAIL | -28.20% | 7.37% | -3.824× | 28.4% | 141 | FAIL | -2.575× | 593 | -0.81% | -3.99% |  |
| BTCUSDT | 1h | `mode_a|k_off|1trade` | Y | FAIL | -58.34% | 7.37% | -7.914× | 22.5% | 293 | FAIL | -3.124× | 1251 | -2.15% | -9.31% |  |
| BTCUSDT | 1h | `mode_b|k1.5|1trade` | Y | FAIL | -27.91% | 7.37% | -3.786× | 25.0% | 136 | FAIL | -2.449× | 525 | -0.80% | -3.54% |  |
| BTCUSDT | 1h | `mode_a|k1.5|multi` | Y | FAIL | -20.56% | 7.37% | -2.788× | 28.6% | 112 | FAIL | -2.204× | 459 | -0.56% | -2.85% |  |

### zlema-sma-cross-v1

| symbol | tf | mode/params | BNB_smoke | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|-----------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|(20,50)|k1.2` | Y | FAIL | 0.77% | 7.37% | 0.104× | 26.1% | 23 | FAIL | -0.667× | 86 | 0.07% | -0.47% |  |
| BTCUSDT | 1h | `mode_a|(20,50)|k1.5` | Y | FAIL | 3.61% | 7.37% | 0.490× | 28.6% | 21 | FAIL | -0.038× | 68 | 0.14% | 0.08% |  |
| BTCUSDT | 1h | `mode_a|(10,30)|k1.2` | Y | FAIL | -14.43% | 7.37% | -1.958× | 31.9% | 47 | FAIL | -1.554× | 162 | -0.38% | -1.58% |  |
| BTCUSDT | 1h | `mode_a|(34,89)|k1.2` | Y | **PASS** | 21.40% | 7.37% | 2.902× | 44.4% | 9 | FAIL | 1.166× | 57 | 0.55% | 0.96% |  |
| BTCUSDT | 1h | `mode_a|(20,50)|k_off` | Y | FAIL | -13.52% | 7.37% | -1.834× | 22.9% | 70 | FAIL | -1.464× | 266 | -0.30% | -1.26% |  |
| BTCUSDT | 1h | `mode_b|(20,50)|k1.2` | Y | **PASS** | 14.65% | 7.37% | 1.987× | 44.0% | 25 | FAIL | -0.518× | 131 | 0.38% | -0.36% |  |
| BTCUSDT | 4h | `mode_a|(20,50)|k1.2` | Y | FAIL | -9.38% | 7.56% | -1.242× | 20.0% | 5 | FAIL | -0.301× | 26 | -0.24% | -0.13% |  |
| BTCUSDT | 4h | `mode_a|(20,50)|k1.5` | Y | FAIL | 1.73% | 7.56% | 0.229× | 100.0% | 1 | FAIL | 0.093× | 19 | 0.04% | 0.18% |  |
| BTCUSDT | 4h | `mode_a|(10,30)|k1.2` | Y | **PASS** | 19.22% | 7.56% | 2.544× | 50.0% | 8 | **PASS** | 1.676× | 44 | 0.50% | 1.30% |  |
| BTCUSDT | 4h | `mode_a|(34,89)|k1.2` | Y | FAIL | 0.24% | 7.56% | 0.032× | 33.3% | 3 | FAIL | 0.634× | 17 | 0.02% | 0.57% |  |
| BTCUSDT | 4h | `mode_a|(20,50)|k_off` | Y | **PASS** | 10.23% | 7.56% | 1.355× | 28.6% | 14 | FAIL | -0.648× | 69 | 0.32% | -0.30% |  |
| BTCUSDT | 4h | `mode_b|(20,50)|k1.2` | Y | FAIL | -7.65% | 7.56% | -1.013× | 33.3% | 6 | FAIL | 0.098× | 32 | -0.20% | 0.14% |  |
| ETHUSDT | 1h | `mode_a|(34,89)|k1.2` | Y | **PASS** | 15.54% | 11.22% | 1.385× | 33.3% | 18 | **PASS** | 2.539× | 66 | 0.48% | 0.69% |  |
| ETHUSDT | 1h | `mode_b|(20,50)|k1.2` | Y | FAIL | -5.30% | 11.22% | -0.472× | 33.3% | 33 | **PASS** | 1.949× | 138 | -0.11% | 0.47% |  |
| ETHUSDT | 4h | `mode_a|(10,30)|k1.2` | Y | **PASS** | 16.33% | 11.45% | 1.426× | 33.3% | 15 | **PASS** | 2.291× | 54 | 0.48% | 0.70% |  |
| ETHUSDT | 4h | `mode_a|(20,50)|k_off` | Y | FAIL | -1.78% | 11.45% | -0.156× | 23.8% | 21 | FAIL | -2.033× | 76 | 0.06% | 0.24% |  |
| SOLUSDT | 1h | `mode_a|(34,89)|k1.2` | Y | FAIL | 2.22% | 12.35% | 0.179× | 21.1% | 19 | **PASS** | 0.576× | 63 | 0.16% | -0.10% | SOL hard filter |
| SOLUSDT | 4h | `mode_a|(10,30)|k1.2` | Y | FAIL | 5.64% | 11.41% | 0.494× | 21.4% | 14 | **PASS** | 0.670× | 50 | 0.28% | -0.07% | SOL hard filter |
