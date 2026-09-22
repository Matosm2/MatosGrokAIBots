# stage3-bnb-sol-v1 scoreboard

Generated (UTC): 2026-09-17T04:03:09.021281+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Closed-bar only;** UTC wall-clock hour reset for PHH/PHL; long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1/stage2 IDs, no ALMA/Roofing/CG/CMO-zero/PWH, no EMA/RSI, SMA200, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **T3 (`t3-dual-cross-v1`):** vFactor locked at `0.7` (lead) and `0.5`; Pairs locked at `(5,15)`, `(8,21)`, `(10,30)`. Tillson nested GDEMA formula.
- **ITrend (`itrend-trigger-v1`):** alpha locked at `0.07` lead (simplified Pine form); optional `0.05` and `0.10` after BTC smoke. Trigger = 2*ITrend - ITrend[2].
- **Decycler (`decycler-osc-fast-slow-v1`):** K locked at `(1.2, 1.0)`; Pairs locked at `(100,125)`, `(50,63)`, `(40,50)`. 2-pole HighPass Decycler Oscillator.
- **VWMA × SMA (`vwma-sma-cross-v1`):** Lengths in `{10, 20, 34, 50}` same-len, plus `(10,20)` and `(20,50)` fast/slow. Mode A cross & Mode B state.
- **PHH/PHL (`phh-phl-accept-break-v1`):** Prior UTC clock-hour H/L. Mode A accept-break, Mode B break+retest. RVOL k in `{off, 1.0, 1.5}`.

## PASS_6m cells (LEAD)

- `[BTCUSDT] vwma-sma-cross-v1` @ `4h` (mode_a|(34,34)): 6m ret=14.34% bh=7.56% ratio=1.898x wr=40.7% n=27 | full=FAIL ratio=-0.461x n=106
- `[BTCUSDT] vwma-sma-cross-v1` @ `4h` (mode_a|(50,50)): 6m ret=24.59% bh=7.56% ratio=3.255x wr=44.4% n=27 | full=FAIL ratio=0.995x n=81
- `[BTCUSDT] vwma-sma-cross-v1` @ `4h` (mode_a|(20,50)): 6m ret=22.05% bh=7.56% ratio=2.918x wr=45.5% n=11 | full=FAIL ratio=0.325x n=54
- `[BTCUSDT] phh-phl-accept-break-v1` @ `15m` (mode_b|rvol1.0): 6m ret=25.41% bh=5.54% ratio=4.588x wr=16.7% n=6 | full=FAIL ratio=0.731x n=8
- `[BTCUSDT] phh-phl-accept-break-v1` @ `15m` (mode_b|rvol1.5): 6m ret=13.03% bh=5.54% ratio=2.353x wr=4.5% n=22 | full=FAIL ratio=-0.349x n=56
- `[BTCUSDT] t3-dual-cross-v1` @ `4h` (mode_a|(10,30)|vf0.5): 6m ret=13.69% bh=7.56% ratio=1.812x wr=30.8% n=13 | full=FAIL ratio=0.247x n=58
- `[ETHUSDT] vwma-sma-cross-v1` @ `4h` (mode_a|(34,34)): 6m ret=25.19% bh=11.45% ratio=2.200x wr=42.3% n=26 | full=PASS ratio=2.301x n=114
- `[ETHUSDT] vwma-sma-cross-v1` @ `4h` (mode_a|(50,50)): 6m ret=16.78% bh=11.45% ratio=1.466x wr=31.6% n=19 | full=PASS ratio=8.289x n=74
- `[ETHUSDT] vwma-sma-cross-v1` @ `4h` (mode_a|(20,50)): 6m ret=23.59% bh=11.45% ratio=2.061x wr=33.3% n=15 | full=PASS ratio=2.680x n=56
- `[ETHUSDT] phh-phl-accept-break-v1` @ `15m` (mode_b|rvol1.5): 6m ret=48.39% bh=8.81% ratio=5.495x wr=20.0% n=5 | full=PASS ratio=1.281x n=47
- `[ETHUSDT] t3-dual-cross-v1` @ `4h` (mode_a|(10,30)|vf0.5): 6m ret=16.95% bh=11.45% ratio=1.480x wr=37.5% n=16 | full=FAIL ratio=-0.870x n=58
- `[SOLUSDT] t3-dual-cross-v1` @ `4h` (mode_a|(10,30)|vf0.5): 6m ret=25.21% bh=11.41% ratio=2.208x wr=46.7% n=15 | full=PASS ratio=0.168x n=56

## All Scored Cells by Strategy

### vwma-sma-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|(10,10)` | FAIL | -58.88% | 5.97% | -9.858× | 23.9% | 293 | FAIL | -3.017× | 1181 | -2.15% | -8.37% |  |
| BTCUSDT | 1h | `mode_a|(20,20)` | FAIL | -44.41% | 5.97% | -7.435× | 28.2% | 174 | FAIL | -2.618× | 641 | -1.43% | -4.37% |  |
| BTCUSDT | 1h | `mode_a|(34,34)` | FAIL | -34.95% | 5.97% | -5.852× | 26.5% | 113 | FAIL | -2.138× | 418 | -1.02% | -2.73% |  |
| BTCUSDT | 1h | `mode_a|(50,50)` | FAIL | -19.56% | 5.97% | -3.276× | 35.2% | 88 | FAIL | -1.816× | 313 | -0.48% | -1.99% |  |
| BTCUSDT | 1h | `mode_a|(10,20)` | FAIL | -25.41% | 5.97% | -4.254× | 25.4% | 130 | FAIL | -2.367× | 542 | -0.67% | -3.30% |  |
| BTCUSDT | 1h | `mode_a|(20,50)` | FAIL | -10.26% | 5.97% | -1.718× | 25.0% | 52 | FAIL | -1.468× | 213 | -0.20% | -1.34% |  |
| BTCUSDT | 1h | `mode_b|(10,10)` | FAIL | -52.04% | 5.97% | -8.713× | 21.0% | 276 | FAIL | -2.955× | 1135 | -1.79% | -7.20% |  |
| BTCUSDT | 1h | `mode_b|(20,20)` | FAIL | -40.14% | 5.97% | -6.721× | 23.9% | 184 | FAIL | -2.562× | 681 | -1.25% | -4.15% |  |
| BTCUSDT | 1h | `mode_b|(10,20)` | FAIL | -34.96% | 5.97% | -5.854× | 23.3% | 163 | FAIL | -2.659× | 674 | -1.01% | -4.55% |  |
| BTCUSDT | 4h | `mode_a|(10,10)` | FAIL | -18.71% | 7.56% | -2.476× | 33.3% | 84 | FAIL | -1.410× | 305 | -0.47% | -1.29% |  |
| BTCUSDT | 4h | `mode_a|(20,20)` | FAIL | 6.23% | 7.56% | 0.825× | 43.4% | 53 | FAIL | -0.252× | 180 | 0.22% | 0.00% |  |
| BTCUSDT | 4h | `mode_a|(34,34)` | **PASS** | 14.34% | 7.56% | 1.898× | 40.7% | 27 | FAIL | -0.461× | 106 | 0.42% | -0.23% |  |
| BTCUSDT | 4h | `mode_a|(50,50)` | **PASS** | 24.59% | 7.56% | 3.255× | 44.4% | 27 | FAIL | 0.995× | 81 | 0.64% | 0.94% |  |
| BTCUSDT | 4h | `mode_a|(10,20)` | FAIL | -12.69% | 7.56% | -1.679× | 32.3% | 31 | FAIL | -0.077× | 129 | -0.27% | 0.21% |  |
| BTCUSDT | 4h | `mode_a|(20,50)` | **PASS** | 22.05% | 7.56% | 2.918× | 45.5% | 11 | FAIL | 0.325× | 54 | 0.56% | 0.46% |  |
| BTCUSDT | 4h | `mode_b|(10,10)` | FAIL | -23.53% | 7.56% | -3.115× | 24.7% | 81 | FAIL | -1.573× | 294 | -0.63% | -1.57% |  |
| BTCUSDT | 4h | `mode_b|(20,20)` | FAIL | -2.46% | 7.56% | -0.326× | 29.6% | 54 | FAIL | -1.144× | 205 | -0.00% | -0.95% |  |
| BTCUSDT | 4h | `mode_b|(10,20)` | FAIL | -14.52% | 7.56% | -1.922× | 22.0% | 41 | FAIL | -1.188× | 173 | -0.33% | -0.95% |  |
| ETHUSDT | 4h | `mode_a|(34,34)` | **PASS** | 25.19% | 11.45% | 2.200× | 42.3% | 26 | **PASS** | 2.301× | 114 | 0.71% | 1.04% |  |
| ETHUSDT | 4h | `mode_a|(50,50)` | **PASS** | 16.78% | 11.45% | 1.466× | 31.6% | 19 | **PASS** | 8.289× | 74 | 0.55% | 1.89% |  |
| ETHUSDT | 4h | `mode_a|(20,50)` | **PASS** | 23.59% | 11.45% | 2.061× | 33.3% | 15 | **PASS** | 2.680× | 56 | 0.64% | 1.02% |  |
| SOLUSDT | 4h | `mode_a|(34,34)` | FAIL | -18.16% | 11.41% | -1.591× | 30.8% | 39 | FAIL | 1.208× | 119 | -0.37% | -0.32% | SOL hard filter |
| SOLUSDT | 4h | `mode_a|(50,50)` | FAIL | 10.57% | 11.41% | 0.926× | 38.5% | 26 | **PASS** | 0.806× | 77 | 0.46% | 0.34% | Near-miss 6m (0.93x B&H); SOL hard filter |
| SOLUSDT | 4h | `mode_a|(20,50)` | FAIL | 13.40% | 11.41% | 1.174× | 46.2% | 13 | **PASS** | -1.163× | 49 | 0.44% | 1.12% | Near-miss 6m (1.17x B&H); SOL hard filter |

### phh-phl-accept-break-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 15m | `mode_a|rvol_off` | FAIL | 0.00% | 5.54% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 15m | `mode_a|rvol1.0` | FAIL | 0.00% | 5.54% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 15m | `mode_a|rvol1.5` | FAIL | 0.00% | 5.54% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 15m | `mode_b|rvol_off` | FAIL | 0.00% | 5.54% | 0.000× | 0.0% | 0 | FAIL | 0.960× | 1 | 0.00% | 0.77% |  |
| BTCUSDT | 15m | `mode_b|rvol1.0` | **PASS** | 25.41% | 5.54% | 4.588× | 16.7% | 6 | FAIL | 0.731× | 8 | 0.66% | 0.62% |  |
| BTCUSDT | 15m | `mode_b|rvol1.5` | **PASS** | 13.03% | 5.54% | 2.353× | 4.5% | 22 | FAIL | -0.349× | 56 | 0.39% | -0.21% |  |
| BTCUSDT | 1h | `mode_a|rvol_off` | FAIL | 0.00% | 5.97% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 1h | `mode_a|rvol1.0` | FAIL | 0.00% | 5.97% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 1h | `mode_a|rvol1.5` | FAIL | 0.00% | 5.97% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 1h | `mode_b|rvol_off` | FAIL | 0.00% | 5.97% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 1h | `mode_b|rvol1.0` | FAIL | 0.00% | 5.97% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| BTCUSDT | 1h | `mode_b|rvol1.5` | FAIL | 0.00% | 5.97% | 0.000× | 0.0% | 0 | FAIL | 0.000× | 0 | 0.00% | 0.00% |  |
| ETHUSDT | 15m | `mode_b|rvol1.0` | FAIL | 0.00% | 8.81% | 0.000× | 0.0% | 0 | FAIL | 0.817× | 64 | 0.00% | 0.54% |  |
| ETHUSDT | 15m | `mode_b|rvol1.5` | **PASS** | 48.39% | 8.81% | 5.495× | 20.0% | 5 | **PASS** | 1.281× | 47 | 1.25% | 0.45% |  |
| SOLUSDT | 15m | `mode_b|rvol1.5` | FAIL | -16.29% | 10.21% | -1.596× | 1.7% | 58 | FAIL | 1.883× | 99 | -0.39% | -1.43% | SOL hard filter |

### t3-dual-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|(5,15)|vf0.7` | FAIL | -21.14% | 5.97% | -3.538× | 31.2% | 125 | FAIL | -2.459× | 531 | -0.53% | -3.60% |  |
| BTCUSDT | 1h | `mode_a|(8,21)|vf0.7` | FAIL | -14.59% | 5.97% | -2.442× | 39.1% | 87 | FAIL | -1.930× | 366 | -0.35% | -2.17% |  |
| BTCUSDT | 1h | `mode_a|(10,30)|vf0.7` | FAIL | -14.75% | 5.97% | -2.470× | 35.8% | 67 | FAIL | -1.679× | 256 | -0.36% | -1.71% |  |
| BTCUSDT | 1h | `mode_a|(5,15)|vf0.5` | FAIL | -22.03% | 5.97% | -3.688× | 30.9% | 110 | FAIL | -2.215× | 459 | -0.56% | -2.85% |  |
| BTCUSDT | 1h | `mode_a|(8,21)|vf0.5` | FAIL | -20.39% | 5.97% | -3.413× | 32.9% | 76 | FAIL | -2.000× | 306 | -0.53% | -2.34% |  |
| BTCUSDT | 1h | `mode_a|(10,30)|vf0.5` | FAIL | -4.57% | 5.97% | -0.765× | 32.1% | 56 | FAIL | -1.295× | 222 | -0.04% | -1.10% |  |
| BTCUSDT | 4h | `mode_a|(5,15)|vf0.7` | FAIL | -5.21% | 7.56% | -0.690× | 28.1% | 32 | FAIL | 0.064× | 134 | -0.05% | 0.27% |  |
| BTCUSDT | 4h | `mode_a|(8,21)|vf0.7` | FAIL | -5.24% | 7.56% | -0.694× | 34.8% | 23 | FAIL | -0.269× | 92 | -0.06% | -0.02% |  |
| BTCUSDT | 4h | `mode_a|(10,30)|vf0.7` | FAIL | -3.73% | 7.56% | -0.494× | 27.8% | 18 | FAIL | -0.894× | 71 | -0.02% | -0.62% |  |
| BTCUSDT | 4h | `mode_a|(5,15)|vf0.5` | FAIL | -8.61% | 7.56% | -1.139× | 31.0% | 29 | FAIL | -0.253× | 115 | -0.15% | 0.04% |  |
| BTCUSDT | 4h | `mode_a|(8,21)|vf0.5` | FAIL | -4.43% | 7.56% | -0.586× | 36.4% | 22 | FAIL | -0.606× | 86 | -0.04% | -0.29% |  |
| BTCUSDT | 4h | `mode_a|(10,30)|vf0.5` | **PASS** | 13.69% | 7.56% | 1.812× | 30.8% | 13 | FAIL | 0.247× | 58 | 0.39% | 0.40% |  |
| ETHUSDT | 4h | `mode_a|(10,30)|vf0.5` | **PASS** | 16.95% | 11.45% | 1.480× | 37.5% | 16 | FAIL | -0.870× | 58 | 0.49% | 0.48% |  |
| SOLUSDT | 4h | `mode_a|(10,30)|vf0.5` | **PASS** | 25.21% | 11.41% | 2.208× | 46.7% | 15 | **PASS** | 0.168× | 56 | 0.72% | 0.47% | SOL hard filter |
| BNBUSDT | 4h | `mode_a|(10,30)|vf0.5` | FAIL | -11.56% | 11.95% | -0.967× | 33.3% | 15 | FAIL | -0.540× | 56 | -0.27% | -0.32% | BNB hard filter |

### decycler-osc-fast-slow-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|(100,125)` | FAIL | -21.02% | 5.97% | -3.519× | 42.7% | 82 | FAIL | -2.197× | 344 | -0.53% | -2.79% |  |
| BTCUSDT | 1h | `mode_a|(50,63)` | FAIL | -47.66% | 5.97% | -7.978× | 35.5% | 166 | FAIL | -2.559× | 657 | -1.57% | -4.04% |  |
| BTCUSDT | 1h | `mode_a|(40,50)` | FAIL | -46.86% | 5.97% | -7.845× | 33.0% | 203 | FAIL | -2.664× | 824 | -1.53% | -4.56% |  |
| BTCUSDT | 1h | `mode_b|(100,125)` | FAIL | -4.64% | 5.97% | -0.778× | 27.3% | 22 | FAIL | -0.391× | 88 | -0.12% | -0.32% |  |
| BTCUSDT | 1h | `mode_b|(50,63)` | FAIL | -8.91% | 5.97% | -1.492× | 26.8% | 41 | FAIL | -1.279× | 168 | -0.23% | -1.30% |  |
| BTCUSDT | 1h | `mode_b|(40,50)` | FAIL | -11.30% | 5.97% | -1.891× | 24.1% | 54 | FAIL | -1.358× | 209 | -0.30% | -1.41% |  |
| BTCUSDT | 4h | `mode_a|(100,125)` | FAIL | -13.16% | 7.56% | -1.742× | 26.9% | 26 | FAIL | -0.954× | 97 | -0.28% | -0.63% |  |
| BTCUSDT | 4h | `mode_a|(50,63)` | FAIL | -1.78% | 7.56% | -0.235× | 48.7% | 39 | FAIL | 0.042× | 165 | -0.02% | 0.24% |  |
| BTCUSDT | 4h | `mode_a|(40,50)` | FAIL | -4.60% | 7.56% | -0.609× | 39.2% | 51 | FAIL | -1.238× | 214 | -0.08% | -1.03% |  |
| BTCUSDT | 4h | `mode_b|(100,125)` | FAIL | -5.82% | 7.56% | -0.770× | 0.0% | 4 | FAIL | -0.149× | 22 | -0.15% | -0.11% |  |
| BTCUSDT | 4h | `mode_b|(50,63)` | FAIL | 6.72% | 7.56% | 0.889× | 62.5% | 8 | FAIL | -0.135× | 44 | 0.17% | -0.08% |  |
| BTCUSDT | 4h | `mode_b|(40,50)` | FAIL | 4.95% | 7.56% | 0.656× | 36.4% | 11 | FAIL | -0.172× | 55 | 0.13% | -0.12% |  |

### itrend-trigger-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | `mode_a|alpha0.07` | FAIL | -38.37% | 5.97% | -6.424× | 24.4% | 180 | FAIL | -2.687× | 746 | -1.13% | -4.66% |  |
| BTCUSDT | 1h | `mode_a|alpha0.05` | FAIL | -35.31% | 5.97% | -5.911× | 26.3% | 152 | FAIL | -2.373× | 606 | -1.02% | -3.33% |  |
| BTCUSDT | 1h | `mode_a|alpha0.10` | FAIL | -50.27% | 5.97% | -8.415× | 20.3% | 231 | FAIL | -2.841× | 898 | -1.66% | -5.77% |  |
| BTCUSDT | 4h | `mode_a|alpha0.07` | FAIL | -1.86% | 7.56% | -0.246× | 25.6% | 43 | FAIL | -0.823× | 180 | 0.03% | -0.50% |  |
| BTCUSDT | 4h | `mode_a|alpha0.05` | FAIL | -1.47% | 7.56% | -0.195× | 24.3% | 37 | FAIL | -0.642× | 154 | 0.03% | -0.31% |  |
| BTCUSDT | 4h | `mode_a|alpha0.10` | FAIL | -6.19% | 7.56% | -0.819× | 29.3% | 58 | FAIL | -1.042× | 221 | -0.08% | -0.72% |  |
