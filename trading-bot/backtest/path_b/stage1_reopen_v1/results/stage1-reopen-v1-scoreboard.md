# stage1-reopen-v1 scoreboard

Generated (UTC): 2026-09-17T03:06:36.156387+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL is the hard filter**.
- **Closed-bar only;** UTC day 00:00–24:00; long-only first pass; pyramiding 0.
- **Hard excludes honored** (no EMA/RSI, SMA200, Woodie, Camarilla, VWAP±σ, CMF, OBV, Chaikin Osc, etc.).

## ASI Limit-Move T-Proxy Locked Specification

- Crypto has no exchange daily limit move; `T_PROXY.md` locked before ASI runs.
- **Family 1 (ATR proxy):** `T = atr_mult * ATR(14)` with `atr_mult ∈ {0.5, 1.0, 1.5, 2.0}`, baseline `1.0x`.
- **Family 2 (% of close):** `T = pct * close[i-1]` with `pct ∈ {1%, 2%, 3%}`.
- Dual breakout: `close > highest(high, N)[1]` AND `ASI > highest(ASI, N)[1]` with `N ∈ {10, 20, 55}`.

## PASS_6m cells (LEAD)

- `[BTCUSDT] pvt-ema-cross-v1` @ `4h` (mode_a|ema34): 6m ret=12.15% bh=7.22% ratio=1.682 wr=21.4% n=28 | full=FAIL ratio=-0.298 n=121
- `[BTCUSDT] accdist-sma-cross-v1` @ `4h` (mode_a|sma50): 6m ret=26.79% bh=7.22% ratio=3.709 wr=36.0% n=25 | full=FAIL ratio=-0.863 n=160
- `[BTCUSDT] accdist-sma-cross-v1` @ `4h` (mode_a|sma65): 6m ret=24.56% bh=7.22% ratio=3.400 wr=31.8% n=22 | full=FAIL ratio=-0.676 n=149
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_atr_0.5x): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.386 n=45
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_atr_1x): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.386 n=45
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_atr_1.5x): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.386 n=45
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_atr_2x): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.386 n=45
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_pct_1%): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.184 n=44
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_pct_2%): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.184 n=44
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N20|T_pct_3%): 6m ret=23.81% bh=7.22% ratio=3.296 wr=50.0% n=8 | full=FAIL ratio=-0.184 n=44
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_0.5x): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=0.972 n=16
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_1x): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=0.972 n=16
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_1.5x): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=0.972 n=16
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_2x): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=0.972 n=16
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_pct_1%): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=1.057 n=17
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_pct_2%): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=1.057 n=17
- `[BTCUSDT] asi-dual-break-v1` @ `4h` (N55|T_pct_3%): 6m ret=15.82% bh=7.22% ratio=2.191 wr=50.0% n=4 | full=FAIL ratio=1.057 n=17
- `[ETHUSDT] accdist-sma-cross-v1` @ `4h` (mode_a|sma50): 6m ret=19.67% bh=10.63% ratio=1.850 wr=21.7% n=46 | full=FAIL ratio=-4.906 n=177
- `[ETHUSDT] accdist-sma-cross-v1` @ `4h` (mode_a|sma65): 6m ret=17.27% bh=10.63% ratio=1.625 wr=22.2% n=45 | full=FAIL ratio=-6.347 n=168
- `[ETHUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_0.5x): 6m ret=14.62% bh=10.63% ratio=1.375 wr=20.0% n=5 | full=FAIL ratio=0.753 n=20
- `[ETHUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_1x): 6m ret=14.62% bh=10.63% ratio=1.375 wr=20.0% n=5 | full=FAIL ratio=0.753 n=20
- `[ETHUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_1.5x): 6m ret=14.62% bh=10.63% ratio=1.375 wr=20.0% n=5 | full=FAIL ratio=0.753 n=20
- `[ETHUSDT] asi-dual-break-v1` @ `4h` (N55|T_atr_2x): 6m ret=14.62% bh=10.63% ratio=1.375 wr=20.0% n=5 | full=FAIL ratio=0.753 n=20

## All Scored Cells by Strategy

### classic-floor-pivots-utc-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 15m | mode_a|day|buf0.0 | FAIL(-5.80) | -28.29 | 4.88 | -5.801 | 34.3 | 67 | FAIL(-1.95) | -1.954 | 266 | -0.82 | -2.34 |  |
| BTCUSDT | 15m | mode_a|day|buf0.5 | FAIL(-4.31) | -21.04 | 4.88 | -4.313 | 25.4 | 67 | FAIL(-1.93) | -1.933 | 266 | -0.58 | -2.34 |  |
| BTCUSDT | 15m | mode_a|day|buf1.0 | FAIL(-5.15) | -25.10 | 4.88 | -5.146 | 26.9 | 67 | FAIL(-1.99) | -1.988 | 266 | -0.71 | -2.44 |  |
| BTCUSDT | 15m | mode_b|day|buf0.0 | FAIL(-4.22) | -20.59 | 4.88 | -4.223 | 39.2 | 74 | FAIL(-1.82) | -1.818 | 284 | -0.56 | -2.09 |  |
| BTCUSDT | 15m | mode_b|day|buf0.5 | FAIL(-5.68) | -27.70 | 4.88 | -5.680 | 20.3 | 74 | FAIL(-1.77) | -1.774 | 284 | -0.80 | -2.04 |  |
| BTCUSDT | 15m | mode_b|day|buf1.0 | FAIL(-4.61) | -22.50 | 4.88 | -4.614 | 28.4 | 74 | FAIL(-1.80) | -1.800 | 284 | -0.63 | -2.08 |  |
| BTCUSDT | 1h | mode_a|day|buf0.0 | FAIL(-4.93) | -28.94 | 5.87 | -4.927 | 39.1 | 64 | FAIL(-1.84) | -1.842 | 252 | -0.84 | -2.15 |  |
| BTCUSDT | 1h | mode_a|day|buf0.5 | FAIL(-4.04) | -23.71 | 5.87 | -4.037 | 35.9 | 64 | FAIL(-1.69) | -1.691 | 252 | -0.67 | -1.90 |  |
| BTCUSDT | 1h | mode_a|day|buf1.0 | FAIL(-4.04) | -23.74 | 5.87 | -4.041 | 39.1 | 64 | FAIL(-1.63) | -1.629 | 252 | -0.67 | -1.79 |  |
| BTCUSDT | 1h | mode_b|day|buf0.0 | FAIL(-2.02) | -11.87 | 5.87 | -2.021 | 38.8 | 67 | FAIL(-1.51) | -1.513 | 255 | -0.31 | -1.60 |  |
| BTCUSDT | 1h | mode_b|day|buf0.5 | FAIL(-1.75) | -10.25 | 5.87 | -1.745 | 32.8 | 67 | FAIL(-1.59) | -1.591 | 255 | -0.26 | -1.73 |  |
| BTCUSDT | 1h | mode_b|day|buf1.0 | FAIL(-1.64) | -9.60 | 5.87 | -1.635 | 37.3 | 67 | FAIL(-1.53) | -1.528 | 255 | -0.24 | -1.63 |  |
| BTCUSDT | 1h | mode_a|week|buf0.0 | FAIL(-0.86) | -5.08 | 5.87 | -0.864 | 50.0 | 12 | FAIL(-0.11) | -0.113 | 42 | -0.12 | -0.03 |  |
| BTCUSDT | 1h | mode_b|week|buf0.0 | FAIL(0.32) | 1.88 | 5.87 | 0.321 | 62.5 | 8 | FAIL(0.10) | 0.095 | 40 | 0.06 | 0.12 |  |

### pdh-pdl-accept-break-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 15m | mode_a|rvol_off | FAIL(-4.59) | -22.41 | 4.88 | -4.594 | 14.0 | 86 | FAIL(-1.94) | -1.941 | 324 | -0.62 | -2.32 |  |
| BTCUSDT | 15m | mode_a|rvol1.0 | FAIL(-4.31) | -21.03 | 4.88 | -4.311 | 16.2 | 80 | FAIL(-1.87) | -1.872 | 307 | -0.57 | -2.19 |  |
| BTCUSDT | 15m | mode_a|rvol1.5 | FAIL(-4.04) | -19.73 | 4.88 | -4.045 | 16.0 | 75 | FAIL(-1.71) | -1.708 | 283 | -0.53 | -1.89 |  |
| BTCUSDT | 15m | mode_a|rvol2.0 | FAIL(-4.17) | -20.36 | 4.88 | -4.175 | 16.1 | 62 | FAIL(-1.56) | -1.559 | 248 | -0.56 | -1.65 |  |
| BTCUSDT | 15m | mode_b|rvol_off | FAIL(-3.65) | -17.79 | 4.88 | -3.647 | 9.8 | 61 | FAIL(-1.40) | -1.399 | 222 | -0.48 | -1.43 |  |
| BTCUSDT | 15m | mode_b|rvol1.0 | FAIL(-1.81) | -8.82 | 4.88 | -1.808 | 17.4 | 46 | FAIL(-0.74) | -0.735 | 169 | -0.22 | -0.63 |  |
| BTCUSDT | 15m | mode_b|rvol1.5 | FAIL(-1.80) | -8.78 | 4.88 | -1.799 | 13.2 | 38 | FAIL(-0.86) | -0.862 | 136 | -0.22 | -0.78 |  |
| BTCUSDT | 15m | mode_b|rvol2.0 | FAIL(-2.41) | -11.77 | 4.88 | -2.414 | 7.7 | 26 | FAIL(-0.83) | -0.833 | 106 | -0.31 | -0.75 |  |
| BTCUSDT | 1h | mode_a|rvol_off | FAIL(-3.91) | -22.98 | 5.87 | -3.912 | 22.1 | 77 | FAIL(-1.92) | -1.919 | 291 | -0.64 | -2.30 |  |
| BTCUSDT | 1h | mode_a|rvol1.0 | FAIL(-2.91) | -17.09 | 5.87 | -2.910 | 26.9 | 67 | FAIL(-1.66) | -1.665 | 260 | -0.46 | -1.83 |  |
| BTCUSDT | 1h | mode_a|rvol1.5 | FAIL(-2.72) | -15.96 | 5.87 | -2.718 | 30.2 | 53 | FAIL(-1.49) | -1.494 | 214 | -0.43 | -1.57 |  |
| BTCUSDT | 1h | mode_a|rvol2.0 | FAIL(-1.66) | -9.76 | 5.87 | -1.662 | 34.2 | 38 | FAIL(-1.22) | -1.225 | 167 | -0.25 | -1.20 |  |
| BTCUSDT | 1h | mode_b|rvol_off | FAIL(-3.73) | -21.90 | 5.87 | -3.729 | 14.3 | 49 | FAIL(-0.99) | -0.993 | 174 | -0.61 | -0.92 |  |
| BTCUSDT | 1h | mode_b|rvol1.0 | FAIL(-2.56) | -15.06 | 5.87 | -2.564 | 16.7 | 36 | FAIL(-1.00) | -0.999 | 133 | -0.40 | -0.95 |  |
| BTCUSDT | 1h | mode_b|rvol1.5 | FAIL(-2.00) | -11.73 | 5.87 | -1.997 | 19.2 | 26 | FAIL(-0.77) | -0.768 | 97 | -0.31 | -0.69 |  |
| BTCUSDT | 1h | mode_b|rvol2.0 | FAIL(-1.20) | -7.07 | 5.87 | -1.204 | 29.4 | 17 | FAIL(-0.73) | -0.733 | 72 | -0.18 | -0.66 |  |

### pvt-ema-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | mode_a|ema9 | FAIL(-11.31) | -66.43 | 5.87 | -11.310 | 17.6 | 330 | FAIL(-3.02) | -3.024 | 1236 | -2.62 | -8.23 |  |
| BTCUSDT | 1h | mode_a|ema14 | FAIL(-9.45) | -55.52 | 5.87 | -9.453 | 17.7 | 243 | FAIL(-2.96) | -2.965 | 952 | -1.93 | -7.08 |  |
| BTCUSDT | 1h | mode_a|ema21 | FAIL(-7.97) | -46.83 | 5.87 | -7.974 | 17.1 | 187 | FAIL(-2.71) | -2.710 | 689 | -1.49 | -4.75 |  |
| BTCUSDT | 1h | mode_a|ema34 | FAIL(-4.29) | -25.19 | 5.87 | -4.289 | 18.3 | 109 | FAIL(-2.26) | -2.259 | 432 | -0.66 | -2.92 |  |
| BTCUSDT | 4h | mode_a|ema9 | FAIL(-3.24) | -23.42 | 7.22 | -3.243 | 21.1 | 76 | FAIL(-1.80) | -1.802 | 294 | -0.60 | -1.81 |  |
| BTCUSDT | 4h | mode_a|ema14 | FAIL(-2.95) | -21.27 | 7.22 | -2.945 | 19.3 | 57 | FAIL(-1.73) | -1.733 | 219 | -0.52 | -1.71 |  |
| BTCUSDT | 4h | mode_a|ema21 | FAIL(0.29) | 2.10 | 7.22 | 0.291 | 20.5 | 39 | FAIL(-0.80) | -0.801 | 160 | 0.13 | -0.39 |  |
| BTCUSDT | 4h | mode_a|ema34 | PASS(1.68) | 12.15 | 7.22 | 1.682 | 21.4 | 28 | FAIL(-0.30) | -0.298 | 121 | 0.37 | 0.04 |  |
| ETHUSDT | 4h | mode_a|ema34 | FAIL(0.27) | 2.92 | 10.63 | 0.275 | 14.3 | 35 | FAIL(-3.51) | -3.510 | 127 | 0.20 | 0.01 |  |

### accdist-sma-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | mode_a|sma10 | FAIL(-13.65) | -80.20 | 5.87 | -13.655 | 18.3 | 447 | FAIL(-3.11) | -3.106 | 1723 | -3.92 | -13.43 |  |
| BTCUSDT | 1h | mode_a|sma20 | FAIL(-11.20) | -65.79 | 5.87 | -11.201 | 17.0 | 317 | FAIL(-3.06) | -3.056 | 1172 | -2.57 | -9.20 |  |
| BTCUSDT | 1h | mode_a|sma50 | FAIL(-5.08) | -29.81 | 5.87 | -5.076 | 21.6 | 171 | FAIL(-2.69) | -2.695 | 668 | -0.82 | -4.66 |  |
| BTCUSDT | 1h | mode_a|sma65 | FAIL(-2.71) | -15.93 | 5.87 | -2.713 | 25.4 | 142 | FAIL(-2.33) | -2.329 | 545 | -0.36 | -3.14 |  |
| BTCUSDT | 4h | mode_a|sma10 | FAIL(-4.30) | -31.06 | 7.22 | -4.300 | 21.6 | 111 | FAIL(-2.41) | -2.412 | 424 | -0.86 | -3.26 |  |
| BTCUSDT | 4h | mode_a|sma20 | FAIL(-1.50) | -10.86 | 7.22 | -1.503 | 26.9 | 67 | FAIL(-1.41) | -1.406 | 267 | -0.22 | -1.14 |  |
| BTCUSDT | 4h | mode_a|sma50 | PASS(3.71) | 26.79 | 7.22 | 3.709 | 36.0 | 25 | FAIL(-0.86) | -0.863 | 160 | 0.69 | -0.51 |  |
| BTCUSDT | 4h | mode_a|sma65 | PASS(3.40) | 24.56 | 7.22 | 3.400 | 31.8 | 22 | FAIL(-0.68) | -0.676 | 149 | 0.62 | -0.37 |  |
| ETHUSDT | 4h | mode_a|sma50 | PASS(1.85) | 19.67 | 10.63 | 1.850 | 21.7 | 46 | FAIL(-4.91) | -4.906 | 177 | 0.61 | -0.19 |  |
| ETHUSDT | 4h | mode_a|sma65 | PASS(1.62) | 17.27 | 10.63 | 1.625 | 22.2 | 45 | FAIL(-6.35) | -6.347 | 168 | 0.55 | -0.54 |  |
| SOLUSDT | 4h | mode_a|sma50 | FAIL(0.68) | 6.81 | 9.98 | 0.683 | 24.0 | 50 | FAIL(1.41) | 1.413 | 184 | 0.32 | -0.49 | SOL filter |
| SOLUSDT | 4h | mode_a|sma65 | FAIL(1.06) | 10.61 | 9.98 | 1.063 | 13.9 | 36 | FAIL(1.88) | 1.878 | 159 | 0.45 | -1.02 | SOL filter |

### asi-dual-break-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | N10|T_atr_0.5x | FAIL(-3.38) | -19.86 | 5.87 | -3.382 | 31.0 | 84 | FAIL(-1.63) | -1.633 | 346 | -0.49 | -1.63 |  |
| BTCUSDT | 1h | N10|T_atr_1x | FAIL(-3.38) | -19.86 | 5.87 | -3.382 | 31.0 | 84 | FAIL(-1.63) | -1.633 | 346 | -0.49 | -1.63 |  |
| BTCUSDT | 1h | N10|T_atr_1.5x | FAIL(-3.38) | -19.86 | 5.87 | -3.382 | 31.0 | 84 | FAIL(-1.63) | -1.633 | 346 | -0.49 | -1.63 |  |
| BTCUSDT | 1h | N10|T_atr_2x | FAIL(-3.38) | -19.86 | 5.87 | -3.382 | 31.0 | 84 | FAIL(-1.63) | -1.633 | 346 | -0.49 | -1.63 |  |
| BTCUSDT | 1h | N10|T_pct_1% | FAIL(-3.11) | -18.27 | 5.87 | -3.111 | 32.9 | 85 | FAIL(-1.57) | -1.568 | 353 | -0.44 | -1.52 |  |
| BTCUSDT | 1h | N10|T_pct_2% | FAIL(-3.11) | -18.27 | 5.87 | -3.111 | 32.9 | 85 | FAIL(-1.57) | -1.568 | 353 | -0.44 | -1.52 |  |
| BTCUSDT | 1h | N10|T_pct_3% | FAIL(-3.11) | -18.27 | 5.87 | -3.111 | 32.9 | 85 | FAIL(-1.57) | -1.568 | 353 | -0.44 | -1.52 |  |
| BTCUSDT | 1h | N20|T_atr_0.5x | FAIL(-3.56) | -20.94 | 5.87 | -3.565 | 29.4 | 51 | FAIL(-1.09) | -1.091 | 184 | -0.52 | -0.87 |  |
| BTCUSDT | 1h | N20|T_atr_1x | FAIL(-3.56) | -20.94 | 5.87 | -3.565 | 29.4 | 51 | FAIL(-1.09) | -1.091 | 184 | -0.52 | -0.87 |  |
| BTCUSDT | 1h | N20|T_atr_1.5x | FAIL(-3.56) | -20.94 | 5.87 | -3.565 | 29.4 | 51 | FAIL(-1.09) | -1.091 | 184 | -0.52 | -0.87 |  |
| BTCUSDT | 1h | N20|T_atr_2x | FAIL(-3.56) | -20.94 | 5.87 | -3.565 | 29.4 | 51 | FAIL(-1.09) | -1.091 | 184 | -0.52 | -0.87 |  |
| BTCUSDT | 1h | N20|T_pct_1% | FAIL(-3.46) | -20.33 | 5.87 | -3.461 | 28.3 | 53 | FAIL(-1.17) | -1.174 | 194 | -0.50 | -0.96 |  |
| BTCUSDT | 1h | N20|T_pct_2% | FAIL(-3.46) | -20.33 | 5.87 | -3.461 | 28.3 | 53 | FAIL(-1.17) | -1.174 | 194 | -0.50 | -0.96 |  |
| BTCUSDT | 1h | N20|T_pct_3% | FAIL(-3.46) | -20.33 | 5.87 | -3.461 | 28.3 | 53 | FAIL(-1.17) | -1.174 | 194 | -0.50 | -0.96 |  |
| BTCUSDT | 1h | N55|T_atr_0.5x | FAIL(0.56) | 3.26 | 5.87 | 0.555 | 31.2 | 16 | FAIL(0.25) | 0.247 | 68 | 0.15 | 0.48 |  |
| BTCUSDT | 1h | N55|T_atr_1x | FAIL(0.56) | 3.26 | 5.87 | 0.555 | 31.2 | 16 | FAIL(0.25) | 0.247 | 68 | 0.15 | 0.48 |  |
| BTCUSDT | 1h | N55|T_atr_1.5x | FAIL(0.56) | 3.26 | 5.87 | 0.555 | 31.2 | 16 | FAIL(0.25) | 0.247 | 68 | 0.15 | 0.48 |  |
| BTCUSDT | 1h | N55|T_atr_2x | FAIL(0.56) | 3.26 | 5.87 | 0.555 | 31.2 | 16 | FAIL(0.25) | 0.247 | 68 | 0.15 | 0.48 |  |
| BTCUSDT | 1h | N55|T_pct_1% | FAIL(0.66) | 3.88 | 5.87 | 0.660 | 36.8 | 19 | FAIL(0.01) | 0.007 | 76 | 0.17 | 0.32 |  |
| BTCUSDT | 1h | N55|T_pct_2% | FAIL(0.66) | 3.88 | 5.87 | 0.660 | 36.8 | 19 | FAIL(0.01) | 0.007 | 76 | 0.17 | 0.32 |  |
| BTCUSDT | 1h | N55|T_pct_3% | FAIL(0.66) | 3.88 | 5.87 | 0.660 | 36.8 | 19 | FAIL(0.01) | 0.007 | 76 | 0.17 | 0.32 |  |
| BTCUSDT | 4h | N10|T_atr_0.5x | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(0.13) | 0.131 | 83 | -0.23 | 0.39 |  |
| BTCUSDT | 4h | N10|T_atr_1x | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(0.13) | 0.131 | 83 | -0.23 | 0.39 |  |
| BTCUSDT | 4h | N10|T_atr_1.5x | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(0.13) | 0.131 | 83 | -0.23 | 0.39 |  |
| BTCUSDT | 4h | N10|T_atr_2x | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(0.13) | 0.131 | 83 | -0.23 | 0.39 |  |
| BTCUSDT | 4h | N10|T_pct_1% | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(-0.18) | -0.182 | 85 | -0.23 | 0.14 |  |
| BTCUSDT | 4h | N10|T_pct_2% | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(-0.18) | -0.182 | 85 | -0.23 | 0.14 |  |
| BTCUSDT | 4h | N10|T_pct_3% | FAIL(-1.50) | -10.83 | 7.22 | -1.499 | 29.2 | 24 | FAIL(-0.18) | -0.182 | 85 | -0.23 | 0.14 |  |
| BTCUSDT | 4h | N20|T_atr_0.5x | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.39) | -0.386 | 45 | 0.60 | -0.10 |  |
| BTCUSDT | 4h | N20|T_atr_1x | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.39) | -0.386 | 45 | 0.60 | -0.10 |  |
| BTCUSDT | 4h | N20|T_atr_1.5x | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.39) | -0.386 | 45 | 0.60 | -0.10 |  |
| BTCUSDT | 4h | N20|T_atr_2x | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.39) | -0.386 | 45 | 0.60 | -0.10 |  |
| BTCUSDT | 4h | N20|T_pct_1% | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.18) | -0.184 | 44 | 0.60 | 0.08 |  |
| BTCUSDT | 4h | N20|T_pct_2% | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.18) | -0.184 | 44 | 0.60 | 0.08 |  |
| BTCUSDT | 4h | N20|T_pct_3% | PASS(3.30) | 23.81 | 7.22 | 3.296 | 50.0 | 8 | FAIL(-0.18) | -0.184 | 44 | 0.60 | 0.08 |  |
| BTCUSDT | 4h | N55|T_atr_0.5x | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(0.97) | 0.972 | 16 | 0.40 | 0.95 |  |
| BTCUSDT | 4h | N55|T_atr_1x | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(0.97) | 0.972 | 16 | 0.40 | 0.95 |  |
| BTCUSDT | 4h | N55|T_atr_1.5x | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(0.97) | 0.972 | 16 | 0.40 | 0.95 |  |
| BTCUSDT | 4h | N55|T_atr_2x | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(0.97) | 0.972 | 16 | 0.40 | 0.95 |  |
| BTCUSDT | 4h | N55|T_pct_1% | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(1.06) | 1.057 | 17 | 0.40 | 1.01 |  |
| BTCUSDT | 4h | N55|T_pct_2% | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(1.06) | 1.057 | 17 | 0.40 | 1.01 |  |
| BTCUSDT | 4h | N55|T_pct_3% | PASS(2.19) | 15.82 | 7.22 | 2.191 | 50.0 | 4 | FAIL(1.06) | 1.057 | 17 | 0.40 | 1.01 |  |
| ETHUSDT | 4h | N20|T_atr_0.5x | FAIL(0.94) | 9.97 | 10.63 | 0.937 | 36.4 | 11 | FAIL(-5.31) | -5.305 | 47 | 0.33 | -0.43 |  |
| ETHUSDT | 4h | N20|T_atr_1x | FAIL(0.94) | 9.97 | 10.63 | 0.937 | 36.4 | 11 | FAIL(-5.31) | -5.305 | 47 | 0.33 | -0.43 |  |
| ETHUSDT | 4h | N20|T_atr_1.5x | FAIL(0.94) | 9.97 | 10.63 | 0.937 | 36.4 | 11 | FAIL(-5.31) | -5.305 | 47 | 0.33 | -0.43 |  |
| ETHUSDT | 4h | N20|T_atr_2x | FAIL(0.94) | 9.97 | 10.63 | 0.937 | 36.4 | 11 | FAIL(-5.31) | -5.305 | 47 | 0.33 | -0.43 |  |
| ETHUSDT | 4h | N20|T_pct_1% | FAIL(0.41) | 4.34 | 10.63 | 0.408 | 33.3 | 12 | FAIL(-5.95) | -5.953 | 50 | 0.20 | -0.58 |  |
| ETHUSDT | 4h | N20|T_pct_2% | FAIL(0.41) | 4.34 | 10.63 | 0.408 | 33.3 | 12 | FAIL(-5.95) | -5.953 | 50 | 0.20 | -0.58 |  |
| ETHUSDT | 4h | N20|T_pct_3% | FAIL(0.41) | 4.34 | 10.63 | 0.408 | 33.3 | 12 | FAIL(-5.95) | -5.953 | 50 | 0.20 | -0.58 |  |
| ETHUSDT | 4h | N55|T_atr_0.5x | PASS(1.38) | 14.62 | 10.63 | 1.375 | 20.0 | 5 | FAIL(0.75) | 0.753 | 20 | 0.51 | 0.73 |  |
| ETHUSDT | 4h | N55|T_atr_1x | PASS(1.38) | 14.62 | 10.63 | 1.375 | 20.0 | 5 | FAIL(0.75) | 0.753 | 20 | 0.51 | 0.73 |  |
| ETHUSDT | 4h | N55|T_atr_1.5x | PASS(1.38) | 14.62 | 10.63 | 1.375 | 20.0 | 5 | FAIL(0.75) | 0.753 | 20 | 0.51 | 0.73 |  |
| ETHUSDT | 4h | N55|T_atr_2x | PASS(1.38) | 14.62 | 10.63 | 1.375 | 20.0 | 5 | FAIL(0.75) | 0.753 | 20 | 0.51 | 0.73 |  |
| ETHUSDT | 4h | N55|T_pct_1% | FAIL(0.06) | 0.66 | 10.63 | 0.062 | 33.3 | 6 | FAIL(-0.06) | -0.059 | 21 | 0.06 | 0.47 |  |
| ETHUSDT | 4h | N55|T_pct_2% | FAIL(0.06) | 0.66 | 10.63 | 0.062 | 33.3 | 6 | FAIL(-0.06) | -0.059 | 21 | 0.06 | 0.47 |  |
| ETHUSDT | 4h | N55|T_pct_3% | FAIL(0.06) | 0.66 | 10.63 | 0.062 | 33.3 | 6 | FAIL(-0.06) | -0.059 | 21 | 0.06 | 0.47 |  |
| SOLUSDT | 4h | N55|T_atr_0.5x | FAIL(-0.31) | -3.06 | 9.98 | -0.306 | 20.0 | 5 | FAIL(1.29) | 1.289 | 19 | 0.04 | -0.52 | SOL filter |
| SOLUSDT | 4h | N55|T_atr_1x | FAIL(-0.31) | -3.06 | 9.98 | -0.306 | 20.0 | 5 | FAIL(1.29) | 1.289 | 19 | 0.04 | -0.52 | SOL filter |
| SOLUSDT | 4h | N55|T_atr_1.5x | FAIL(-0.31) | -3.06 | 9.98 | -0.306 | 20.0 | 5 | FAIL(1.29) | 1.289 | 19 | 0.04 | -0.52 | SOL filter |
| SOLUSDT | 4h | N55|T_atr_2x | FAIL(-0.31) | -3.06 | 9.98 | -0.306 | 20.0 | 5 | FAIL(1.29) | 1.289 | 19 | 0.04 | -0.52 | SOL filter |

## Summary & Findings

- Total evaluated cells: 111
- Total PASS_6m cells: 23
- Hard stop rules and gate compliance strictly enforced.

