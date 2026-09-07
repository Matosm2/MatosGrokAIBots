# fresh-wave-v1 scoreboard

Generated (UTC): 2026-09-06T00:41:45.319502+00:00

**RESEARCH ONLY — not paper/live. No Claude. No Jewel. No prior failed families.**

## Scoring

- **LEAD gate:** 6m Mode-A ≥ **1.2×** B&H → `PASS/FAIL_6m`
- **Also:** full(~2y) Mode-A ≥ **1.2×** B&H → `PASS/FAIL_full` (informational)
- Costs: 0.10%/side fee + 5 bps slip; Mode-A **100%** + Mode-B ops **2.5%** (ops not scored)
- Symbol: BTCUSDT only. Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen (no spray): CRSI(3,2,100); NR7/ATR14×2/10-bar; Ichimoku 9/26/52; HA streak=3; OBV EMA20 + close EMA50.

## Strategy rules (documented)

1. **connors-rsi-mr-v1** — Classic **CRSI(3,2,100)** = mean of RSI(close,3), RSI(streak,2), PercentRank(ROC1,100). Enter CRSI<10; exit CRSI>90 OR hold≥5 bars.
2. **nr7-breakout-v1** — NR7 = narrowest H-L of last 7 bars. Enter when close > that NR7 high. Exit: ±2×ATR(14) from entry (stop via engine; target via signal) OR after 10 bars (bar-close; reference mid=(NR7.H+NR7.L)/2).
3. **ichimoku-cloud-trend-v1** — Classic **9/26/52**, displacement 26 (cloud at i from i-26; no lookahead). Enter TK cross up AND close > cloud top; exit close < cloud bottom OR TK cross down.
4. **ha-streak-trend-v1** — Enter after 3 consecutive HA bull bars (HA close>HA open); exit on first HA bear bar.
5. **obv-ema-trend-v1** — Enter OBV cross above EMA20(OBV) AND close > EMA50; exit OBV cross below EMA20(OBV).

## Scoreboard LEAD 6m PASS/FAIL_6m (ratio)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| connors-rsi-mr-v1 | FAIL(-5.23) | FAIL(-3.87) | FAIL(-3.06) | FAIL(-1.51) | FAIL(0.11) | FAIL(-0.72) | FAIL(-0.53) | FAIL(-0.31) | FAIL(-0.75) | FAIL(-0.68) | FAIL(-0.58) | FAIL(0.37) | FAIL(-0.02) | FAIL(-0.50) | FAIL(-0.26) | FAIL(0.37) |
| nr7-breakout-v1 | FAIL(-5.71) | FAIL(-5.66) | FAIL(-5.59) | FAIL(-4.69) | FAIL(-2.96) | FAIL(-3.35) | FAIL(-2.00) | FAIL(-0.55) | FAIL(-0.54) | FAIL(0.09) | FAIL(0.04) | FAIL(-0.38) | FAIL(-0.51) | FAIL(0.51) | FAIL(0.06) | PASS(1.25) |
| ichimoku-cloud-trend-v1 | FAIL(-4.54) | FAIL(-3.55) | FAIL(-2.94) | FAIL(-1.28) | FAIL(-0.34) | FAIL(-0.48) | PASS(1.33) | FAIL(-0.06) | FAIL(-0.83) | FAIL(0.74) | FAIL(-0.19) | FAIL(-0.36) | FAIL(0.90) | FAIL(0.96) | FAIL(0.71) | FAIL(0.00) |
| ha-streak-trend-v1 | FAIL(-5.71) | FAIL(-5.69) | FAIL(-5.64) | FAIL(-5.07) | FAIL(-3.17) | FAIL(-3.65) | FAIL(-1.60) | FAIL(-1.00) | FAIL(-0.95) | FAIL(-0.74) | FAIL(0.22) | FAIL(-0.78) | FAIL(-0.49) | FAIL(0.21) | FAIL(-0.25) | FAIL(-0.45) |
| obv-ema-trend-v1 | FAIL(-5.70) | FAIL(-5.47) | FAIL(-5.12) | FAIL(-4.00) | FAIL(-2.09) | FAIL(-2.58) | FAIL(-1.12) | FAIL(-1.87) | FAIL(-0.88) | FAIL(0.27) | FAIL(-0.09) | FAIL(0.37) | FAIL(-0.29) | FAIL(-0.01) | PASS(1.35) | FAIL(0.54) |

## Scoreboard full(~2y) PASS/FAIL_full (ratio)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| connors-rsi-mr-v1 | FAIL(-2.43) | FAIL(-2.41) | FAIL(-2.33) | FAIL(-1.94) | FAIL(-0.76) | FAIL(-1.45) | FAIL(-0.88) | FAIL(-1.16) | FAIL(-0.74) | FAIL(-0.84) | FAIL(-0.01) | FAIL(0.12) | FAIL(0.48) | FAIL(0.25) | FAIL(-0.34) | FAIL(0.35) |
| nr7-breakout-v1 | FAIL(-2.42) | FAIL(-2.44) | FAIL(-2.45) | FAIL(-2.45) | FAIL(-2.09) | FAIL(-2.42) | FAIL(-1.96) | FAIL(-1.52) | FAIL(-0.50) | FAIL(-0.31) | FAIL(-0.20) | FAIL(-0.80) | FAIL(-1.09) | FAIL(-0.43) | PASS(1.60) | FAIL(-0.39) |
| ichimoku-cloud-trend-v1 | FAIL(-2.42) | FAIL(-2.32) | FAIL(-2.13) | FAIL(-1.66) | FAIL(-0.95) | FAIL(-0.67) | FAIL(0.06) | FAIL(0.14) | FAIL(0.33) | FAIL(0.89) | FAIL(-0.18) | FAIL(0.49) | FAIL(0.87) | PASS(1.49) | FAIL(0.58) | FAIL(0.83) |
| ha-streak-trend-v1 | FAIL(-2.43) | FAIL(-2.44) | FAIL(-2.45) | FAIL(-2.45) | FAIL(-2.26) | FAIL(-2.46) | FAIL(-1.96) | FAIL(-1.51) | FAIL(-1.22) | FAIL(-0.93) | FAIL(-0.46) | FAIL(-0.93) | FAIL(-0.51) | FAIL(-0.30) | FAIL(-0.06) | FAIL(-0.41) |
| obv-ema-trend-v1 | FAIL(-2.43) | FAIL(-2.44) | FAIL(-2.45) | FAIL(-2.43) | FAIL(-1.89) | FAIL(-2.21) | FAIL(-1.62) | FAIL(-1.54) | FAIL(-1.04) | FAIL(-0.88) | FAIL(-0.81) | FAIL(0.17) | FAIL(0.08) | FAIL(0.52) | FAIL(0.33) | FAIL(-0.19) |

## Combined (6m LEAD | full)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| connors-rsi-mr-v1 | F-5.23|F-2.43 | F-3.87|F-2.41 | F-3.06|F-2.33 | F-1.51|F-1.94 | F0.11|F-0.76 | F-0.72|F-1.45 | F-0.53|F-0.88 | F-0.31|F-1.16 | F-0.75|F-0.74 | F-0.68|F-0.84 | F-0.58|F-0.01 | F0.37|F0.12 | F-0.02|F0.48 | F-0.50|F0.25 | F-0.26|F-0.34 | F0.37|F0.35 |
| nr7-breakout-v1 | F-5.71|F-2.42 | F-5.66|F-2.44 | F-5.59|F-2.45 | F-4.69|F-2.45 | F-2.96|F-2.09 | F-3.35|F-2.42 | F-2.00|F-1.96 | F-0.55|F-1.52 | F-0.54|F-0.50 | F0.09|F-0.31 | F0.04|F-0.20 | F-0.38|F-0.80 | F-0.51|F-1.09 | F0.51|F-0.43 | F0.06|P1.60 | P1.25|F-0.39 |
| ichimoku-cloud-trend-v1 | F-4.54|F-2.42 | F-3.55|F-2.32 | F-2.94|F-2.13 | F-1.28|F-1.66 | F-0.34|F-0.95 | F-0.48|F-0.67 | P1.33|F0.06 | F-0.06|F0.14 | F-0.83|F0.33 | F0.74|F0.89 | F-0.19|F-0.18 | F-0.36|F0.49 | F0.90|F0.87 | F0.96|P1.49 | F0.71|F0.58 | F0.00|F0.83 |
| ha-streak-trend-v1 | F-5.71|F-2.43 | F-5.69|F-2.44 | F-5.64|F-2.45 | F-5.07|F-2.45 | F-3.17|F-2.26 | F-3.65|F-2.46 | F-1.60|F-1.96 | F-1.00|F-1.51 | F-0.95|F-1.22 | F-0.74|F-0.93 | F0.22|F-0.46 | F-0.78|F-0.93 | F-0.49|F-0.51 | F0.21|F-0.30 | F-0.25|F-0.06 | F-0.45|F-0.41 |
| obv-ema-trend-v1 | F-5.70|F-2.43 | F-5.47|F-2.44 | F-5.12|F-2.45 | F-4.00|F-2.43 | F-2.09|F-1.89 | F-2.58|F-2.21 | F-1.12|F-1.62 | F-1.87|F-1.54 | F-0.88|F-1.04 | F0.27|F-0.88 | F-0.09|F-0.81 | F0.37|F0.17 | F-0.29|F0.08 | F-0.01|F0.52 | P1.35|F0.33 | F0.54|F-0.19 |

_Legend: P=PASS F=FAIL; `P6m|Pfull` compact ratios._

## PASS_6m cells (LEAD)

- `obv-ema-trend-v1` @ `1d`: 6m ret=28.55% bh=21.09% ratio=1.354 wr=40.0% n=5 | full=FAIL ratio=0.329 n=26
- `nr7-breakout-v1` @ `2d`: 6m ret=20.76% bh=16.64% ratio=1.247 wr=60.0% n=5 | full=FAIL ratio=-0.393 n=22
- `ichimoku-cloud-trend-v1` @ `2h`: 6m ret=23.16% bh=17.38% ratio=1.332 wr=53.3% n=15 | full=FAIL ratio=0.064 n=85

## PASS_full cells (informational; not LEAD)

- `nr7-breakout-v1` @ `1d`: full ret=77.08% bh=48.03% ratio=1.605 wr=58.3% n=48 | 6m=FAIL
- `ichimoku-cloud-trend-v1` @ `12h`: full ret=63.37% bh=42.56% ratio=1.489 wr=41.2% n=17 | 6m=FAIL

## Cell detail (Mode-A gate; both windows)

| strategy | tf | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ret% | full_bh% | full_ratio | full_wr% | full_n | ops_6m% | ops_full% | error |
|----------|----|----|---------|--------|----------|--------|------|------|-----------|----------|------------|----------|--------|---------|-----------|-------|
| connors-rsi-mr-v1 | 1h | FAIL | -12.72 | 17.61 | -0.723 | 37.1 | 62 | FAIL | -57.89 | 39.99 | -1.448 | 36.3 | 278 | -0.33 | -2.09 |  |
| nr7-breakout-v1 | 1h | FAIL | -58.93 | 17.61 | -3.347 | 37.2 | 285 | FAIL | -96.67 | 39.99 | -2.418 | 38.6 | 1097 | -2.16 | -8.06 |  |
| ichimoku-cloud-trend-v1 | 1h | FAIL | -8.43 | 17.61 | -0.479 | 25.6 | 43 | FAIL | -26.67 | 39.99 | -0.667 | 29.9 | 184 | -0.18 | -0.63 |  |
| ha-streak-trend-v1 | 1h | FAIL | -64.30 | 17.61 | -3.652 | 17.7 | 334 | FAIL | -98.22 | 39.99 | -2.456 | 19.7 | 1294 | -2.52 | -9.46 |  |
| obv-ema-trend-v1 | 1h | FAIL | -45.46 | 17.61 | -2.582 | 16.3 | 203 | FAIL | -88.27 | 39.99 | -2.207 | 17.4 | 757 | -1.45 | -5.06 |  |
| connors-rsi-mr-v1 | 4h | FAIL | -13.14 | 17.61 | -0.746 | 33.3 | 15 | FAIL | -31.44 | 42.40 | -0.741 | 35.8 | 67 | -0.35 | -0.89 |  |
| nr7-breakout-v1 | 4h | FAIL | -9.51 | 17.61 | -0.540 | 49.3 | 71 | FAIL | -21.34 | 42.40 | -0.503 | 51.3 | 263 | -0.21 | -0.41 |  |
| ichimoku-cloud-trend-v1 | 4h | FAIL | -14.64 | 17.61 | -0.831 | 25.0 | 12 | FAIL | 14.03 | 42.40 | 0.331 | 36.4 | 44 | -0.39 | 0.49 |  |
| ha-streak-trend-v1 | 4h | FAIL | -16.67 | 17.61 | -0.946 | 25.0 | 80 | FAIL | -51.82 | 42.40 | -1.222 | 27.5 | 324 | -0.42 | -1.68 |  |
| obv-ema-trend-v1 | 4h | FAIL | -15.51 | 17.61 | -0.881 | 19.5 | 41 | FAIL | -44.16 | 42.40 | -1.041 | 20.5 | 185 | -0.41 | -1.32 |  |
| connors-rsi-mr-v1 | 1d | FAIL | -5.42 | 21.09 | -0.257 | 0.0 | 1 | FAIL | -16.14 | 48.03 | -0.336 | 50.0 | 10 | -0.14 | -0.37 |  |
| nr7-breakout-v1 | 1d | FAIL | 1.21 | 21.09 | 0.057 | 41.7 | 12 | PASS | 77.08 | 48.03 | 1.605 | 58.3 | 48 | 0.06 | 1.65 |  |
| ichimoku-cloud-trend-v1 | 1d | FAIL | 14.87 | 21.09 | 0.705 | 100.0 | 1 | FAIL | 27.63 | 48.03 | 0.575 | 37.5 | 8 | 0.37 | 0.81 |  |
| ha-streak-trend-v1 | 1d | FAIL | -5.18 | 21.09 | -0.246 | 18.8 | 16 | FAIL | -3.00 | 48.03 | -0.062 | 33.3 | 57 | -0.11 | 0.05 |  |
| obv-ema-trend-v1 | 1d | PASS | 28.55 | 21.09 | 1.354 | 40.0 | 5 | FAIL | 15.82 | 48.03 | 0.329 | 26.9 | 26 | 0.70 | 0.56 |  |
| connors-rsi-mr-v1 | 2d | FAIL | 6.13 | 16.64 | 0.368 | 100.0 | 1 | FAIL | 16.65 | 47.37 | 0.351 | 75.0 | 4 | 0.15 | 0.40 |  |
| nr7-breakout-v1 | 2d | PASS | 20.76 | 16.64 | 1.247 | 60.0 | 5 | FAIL | -18.62 | 47.37 | -0.393 | 40.9 | 22 | 0.51 | -0.36 |  |
| ichimoku-cloud-trend-v1 | 2d | FAIL | 0.00 | 16.64 | 0.000 | 0.0 | 0 | FAIL | 39.29 | 47.37 | 0.829 | 40.0 | 5 | 0.00 | 1.16 |  |
| ha-streak-trend-v1 | 2d | FAIL | -7.57 | 16.64 | -0.455 | 25.0 | 8 | FAIL | -19.31 | 47.37 | -0.408 | 34.5 | 29 | -0.19 | -0.44 |  |
| obv-ema-trend-v1 | 2d | FAIL | 8.98 | 16.64 | 0.539 | 100.0 | 1 | FAIL | -8.83 | 47.37 | -0.186 | 23.8 | 21 | 0.22 | -0.12 |  |
| connors-rsi-mr-v1 | 15m | FAIL | -53.20 | 17.40 | -3.057 | 24.0 | 292 | FAIL | -95.10 | 40.89 | -2.326 | 27.1 | 1099 | -1.87 | -7.20 |  |
| nr7-breakout-v1 | 15m | FAIL | -97.27 | 17.40 | -5.590 | 24.8 | 1093 | FAIL | -100.00 | 40.89 | -2.446 | 26.9 | 4373 | -8.57 | -29.23 |  |
| ichimoku-cloud-trend-v1 | 15m | FAIL | -51.21 | 17.40 | -2.943 | 20.5 | 219 | FAIL | -86.91 | 40.89 | -2.125 | 23.1 | 776 | -1.76 | -4.85 |  |
| ha-streak-trend-v1 | 15m | FAIL | -98.21 | 17.40 | -5.644 | 10.4 | 1294 | FAIL | -100.00 | 40.89 | -2.446 | 11.6 | 5174 | -9.54 | -32.76 |  |
| obv-ema-trend-v1 | 15m | FAIL | -89.12 | 17.40 | -5.122 | 11.8 | 743 | FAIL | -99.99 | 40.89 | -2.445 | 11.5 | 3018 | -5.36 | -20.71 |  |
| connors-rsi-mr-v1 | 30m | FAIL | -26.32 | 17.45 | -1.509 | 30.6 | 134 | FAIL | -78.91 | 40.77 | -1.935 | 32.3 | 541 | -0.75 | -3.75 |  |
| nr7-breakout-v1 | 30m | FAIL | -81.84 | 17.45 | -4.691 | 30.2 | 560 | FAIL | -99.91 | 40.77 | -2.450 | 32.4 | 2197 | -4.14 | -15.82 |  |
| ichimoku-cloud-trend-v1 | 30m | FAIL | -22.28 | 17.45 | -1.277 | 24.7 | 93 | FAIL | -67.49 | 40.77 | -1.655 | 24.6 | 374 | -0.58 | -2.65 |  |
| ha-streak-trend-v1 | 30m | FAIL | -88.37 | 17.45 | -5.065 | 13.2 | 673 | FAIL | -99.97 | 40.77 | -2.452 | 14.8 | 2618 | -5.21 | -18.15 |  |
| obv-ema-trend-v1 | 30m | FAIL | -69.86 | 17.45 | -4.004 | 15.7 | 357 | FAIL | -99.06 | 40.77 | -2.429 | 14.8 | 1455 | -2.94 | -10.90 |  |
| connors-rsi-mr-v1 | 5m | FAIL | -91.58 | 17.50 | -5.232 | 11.3 | 811 | FAIL | -99.99 | 41.20 | -2.427 | 15.3 | 3275 | -5.98 | -21.36 |  |
| nr7-breakout-v1 | 5m | FAIL | -100.00 | 17.50 | -5.713 | 15.2 | 3398 | FAIL | -99.85 | 41.20 | -2.424 | 15.8 | 13594 | -22.31 | -64.35 |  |
| ichimoku-cloud-trend-v1 | 5m | FAIL | -79.47 | 17.50 | -4.540 | 16.2 | 551 | FAIL | -99.80 | 41.20 | -2.422 | 16.8 | 2209 | -3.86 | -14.30 |  |
| ha-streak-trend-v1 | 5m | FAIL | -100.00 | 17.50 | -5.713 | 6.2 | 3794 | FAIL | -100.00 | 41.20 | -2.427 | 6.7 | 15377 | -24.94 | -69.01 |  |
| obv-ema-trend-v1 | 5m | FAIL | -99.74 | 17.50 | -5.698 | 7.5 | 1957 | FAIL | -100.00 | 41.20 | -2.427 | 8.0 | 8471 | -13.81 | -47.13 |  |
| connors-rsi-mr-v1 | 10m | FAIL | -67.81 | 17.51 | -3.873 | 18.3 | 427 | FAIL | -98.77 | 41.02 | -2.408 | 22.9 | 1625 | -2.78 | -10.35 |  |
| nr7-breakout-v1 | 10m | FAIL | -99.05 | 17.51 | -5.657 | 22.9 | 1641 | FAIL | -100.00 | 41.02 | -2.438 | 24.2 | 6612 | -10.96 | -39.16 |  |
| ichimoku-cloud-trend-v1 | 10m | FAIL | -62.16 | 17.51 | -3.550 | 19.5 | 318 | FAIL | -95.13 | 41.02 | -2.319 | 21.3 | 1156 | -2.38 | -7.17 |  |
| ha-streak-trend-v1 | 10m | FAIL | -99.69 | 17.51 | -5.693 | 9.1 | 1914 | FAIL | -100.00 | 41.02 | -2.438 | 9.8 | 7725 | -13.39 | -44.52 |  |
| obv-ema-trend-v1 | 10m | FAIL | -95.79 | 17.51 | -5.471 | 11.3 | 1067 | FAIL | -100.00 | 41.02 | -2.438 | 10.9 | 4407 | -7.58 | -28.12 |  |
| connors-rsi-mr-v1 | 90m | FAIL | 1.92 | 17.38 | 0.111 | 48.9 | 45 | FAIL | -31.36 | 41.15 | -0.762 | 42.5 | 193 | 0.05 | -0.87 |  |
| nr7-breakout-v1 | 90m | FAIL | -51.39 | 17.38 | -2.956 | 37.1 | 186 | FAIL | -86.00 | 41.15 | -2.090 | 40.4 | 728 | -1.75 | -4.59 |  |
| ichimoku-cloud-trend-v1 | 90m | FAIL | -5.94 | 17.38 | -0.342 | 26.7 | 30 | FAIL | -39.28 | 41.15 | -0.955 | 29.3 | 133 | -0.11 | -1.10 |  |
| ha-streak-trend-v1 | 90m | FAIL | -55.17 | 17.38 | -3.174 | 17.4 | 224 | FAIL | -93.11 | 41.15 | -2.263 | 20.7 | 845 | -1.96 | -6.35 |  |
| obv-ema-trend-v1 | 90m | FAIL | -36.41 | 17.38 | -2.095 | 18.5 | 124 | FAIL | -77.59 | 41.15 | -1.885 | 19.3 | 491 | -1.11 | -3.54 |  |
| connors-rsi-mr-v1 | 2h | FAIL | -9.16 | 17.38 | -0.527 | 38.2 | 34 | FAIL | -37.40 | 42.62 | -0.878 | 42.0 | 138 | -0.23 | -1.11 |  |
| nr7-breakout-v1 | 2h | FAIL | -34.85 | 17.38 | -2.005 | 42.9 | 140 | FAIL | -83.54 | 42.62 | -1.960 | 42.5 | 541 | -1.02 | -4.19 |  |
| ichimoku-cloud-trend-v1 | 2h | PASS | 23.16 | 17.38 | 1.332 | 53.3 | 15 | FAIL | 2.74 | 42.62 | 0.064 | 34.1 | 85 | 0.57 | 0.19 |  |
| ha-streak-trend-v1 | 2h | FAIL | -27.83 | 17.38 | -1.601 | 25.8 | 163 | FAIL | -83.68 | 42.62 | -1.964 | 23.2 | 665 | -0.76 | -4.30 |  |
| obv-ema-trend-v1 | 2h | FAIL | -19.54 | 17.38 | -1.124 | 18.4 | 98 | FAIL | -68.95 | 42.62 | -1.618 | 18.5 | 352 | -0.49 | -2.74 |  |
| connors-rsi-mr-v1 | 3h | FAIL | -5.46 | 17.37 | -0.314 | 48.0 | 25 | FAIL | -47.44 | 41.04 | -1.156 | 37.0 | 92 | -0.13 | -1.54 |  |
| nr7-breakout-v1 | 3h | FAIL | -9.60 | 17.37 | -0.553 | 41.8 | 91 | FAIL | -62.31 | 41.04 | -1.518 | 45.4 | 355 | -0.21 | -2.22 |  |
| ichimoku-cloud-trend-v1 | 3h | FAIL | -1.07 | 17.37 | -0.062 | 40.0 | 15 | FAIL | 5.92 | 41.04 | 0.144 | 32.8 | 61 | 0.03 | 0.29 |  |
| ha-streak-trend-v1 | 3h | FAIL | -17.31 | 17.37 | -0.996 | 27.0 | 100 | FAIL | -62.06 | 41.04 | -1.512 | 28.1 | 416 | -0.44 | -2.25 |  |
| obv-ema-trend-v1 | 3h | FAIL | -32.46 | 17.37 | -1.869 | 13.4 | 67 | FAIL | -63.07 | 41.04 | -1.537 | 19.4 | 248 | -0.97 | -2.33 |  |
| connors-rsi-mr-v1 | 5h | FAIL | -12.29 | 18.01 | -0.682 | 43.8 | 16 | FAIL | -35.24 | 42.15 | -0.836 | 32.8 | 58 | -0.32 | -1.04 |  |
| nr7-breakout-v1 | 5h | FAIL | 1.67 | 18.01 | 0.092 | 50.9 | 55 | FAIL | -13.09 | 42.15 | -0.311 | 48.8 | 211 | 0.07 | -0.17 |  |
| ichimoku-cloud-trend-v1 | 5h | FAIL | 13.27 | 18.01 | 0.737 | 33.3 | 12 | FAIL | 37.46 | 42.15 | 0.889 | 37.8 | 37 | 0.37 | 0.96 |  |
| ha-streak-trend-v1 | 5h | FAIL | -13.35 | 18.01 | -0.741 | 30.2 | 63 | FAIL | -39.30 | 42.15 | -0.932 | 30.1 | 249 | -0.33 | -1.12 |  |
| obv-ema-trend-v1 | 5h | FAIL | 4.89 | 18.01 | 0.272 | 32.6 | 43 | FAIL | -37.08 | 42.15 | -0.880 | 23.9 | 155 | 0.18 | -1.03 |  |
| connors-rsi-mr-v1 | 6h | FAIL | -10.28 | 17.77 | -0.579 | 44.4 | 18 | FAIL | -0.32 | 42.10 | -0.008 | 48.1 | 54 | -0.26 | 0.04 |  |
| nr7-breakout-v1 | 6h | FAIL | 0.79 | 17.77 | 0.044 | 52.1 | 48 | FAIL | -8.45 | 42.10 | -0.201 | 49.7 | 179 | 0.05 | -0.06 |  |
| ichimoku-cloud-trend-v1 | 6h | FAIL | -3.41 | 17.77 | -0.192 | 42.9 | 7 | FAIL | -7.44 | 42.10 | -0.177 | 33.3 | 33 | -0.08 | -0.09 |  |
| ha-streak-trend-v1 | 6h | FAIL | 3.97 | 17.77 | 0.223 | 37.0 | 54 | FAIL | -19.38 | 42.10 | -0.460 | 31.4 | 210 | 0.12 | -0.41 |  |
| obv-ema-trend-v1 | 6h | FAIL | -1.66 | 17.77 | -0.093 | 39.1 | 23 | FAIL | -33.94 | 42.10 | -0.806 | 27.9 | 111 | -0.03 | -0.96 |  |
| connors-rsi-mr-v1 | 7h | FAIL | 6.77 | 18.46 | 0.367 | 61.5 | 13 | FAIL | 5.20 | 42.45 | 0.122 | 43.2 | 44 | 0.18 | 0.16 |  |
| nr7-breakout-v1 | 7h | FAIL | -6.98 | 18.46 | -0.378 | 45.5 | 44 | FAIL | -34.08 | 42.45 | -0.803 | 47.0 | 164 | -0.15 | -0.84 |  |
| ichimoku-cloud-trend-v1 | 7h | FAIL | -6.72 | 18.46 | -0.364 | 28.6 | 7 | FAIL | 20.96 | 42.45 | 0.494 | 38.5 | 26 | -0.17 | 0.59 |  |
| ha-streak-trend-v1 | 7h | FAIL | -14.35 | 18.46 | -0.777 | 30.6 | 49 | FAIL | -39.32 | 42.45 | -0.926 | 31.7 | 180 | -0.36 | -1.13 |  |
| obv-ema-trend-v1 | 7h | FAIL | 6.74 | 18.46 | 0.365 | 33.3 | 27 | FAIL | 7.11 | 42.45 | 0.167 | 27.3 | 88 | 0.22 | 0.36 |  |
| connors-rsi-mr-v1 | 9h | FAIL | -0.31 | 18.55 | -0.017 | 88.9 | 9 | FAIL | 19.43 | 40.54 | 0.479 | 73.0 | 37 | 0.01 | 0.49 |  |
| nr7-breakout-v1 | 9h | FAIL | -9.43 | 18.55 | -0.508 | 43.8 | 32 | FAIL | -44.18 | 40.54 | -1.090 | 45.7 | 127 | -0.20 | -1.22 |  |
| ichimoku-cloud-trend-v1 | 9h | FAIL | 16.75 | 18.55 | 0.903 | 50.0 | 4 | FAIL | 35.36 | 40.54 | 0.872 | 42.9 | 21 | 0.43 | 0.91 |  |
| ha-streak-trend-v1 | 9h | FAIL | -9.03 | 18.55 | -0.487 | 20.0 | 40 | FAIL | -20.76 | 40.54 | -0.512 | 22.4 | 147 | -0.18 | -0.43 |  |
| obv-ema-trend-v1 | 9h | FAIL | -5.45 | 18.55 | -0.294 | 31.6 | 19 | FAIL | 3.27 | 40.54 | 0.081 | 28.8 | 73 | -0.13 | 0.29 |  |
| connors-rsi-mr-v1 | 12h | FAIL | -9.32 | 18.69 | -0.499 | 42.9 | 7 | FAIL | 10.68 | 42.56 | 0.251 | 60.7 | 28 | -0.22 | 0.34 |  |
| nr7-breakout-v1 | 12h | FAIL | 9.47 | 18.69 | 0.507 | 58.3 | 24 | FAIL | -18.43 | 42.56 | -0.433 | 51.1 | 92 | 0.26 | -0.32 |  |
| ichimoku-cloud-trend-v1 | 12h | FAIL | 17.96 | 18.69 | 0.961 | 60.0 | 5 | PASS | 63.37 | 42.56 | 1.489 | 41.2 | 17 | 0.44 | 1.44 |  |
| ha-streak-trend-v1 | 12h | FAIL | 3.93 | 18.69 | 0.210 | 32.1 | 28 | FAIL | -12.73 | 42.56 | -0.299 | 31.5 | 111 | 0.16 | -0.19 |  |
| obv-ema-trend-v1 | 12h | FAIL | -0.22 | 18.69 | -0.012 | 30.0 | 20 | FAIL | 22.12 | 42.56 | 0.520 | 25.0 | 76 | 0.00 | 0.72 |  |

## Caveats

- LEAD = 6m Mode-A only. full(~2y) is reported for context, not paper clearance.
- Mode-B ops 2.5% is parallel / informational only.
- No param spray. No ema-rsi / openproxy / bb-squeeze / kama / dual-mom / sma200 / supertrend in this wave.
- Hold PRs #15–#17 unmerged; this PR is additive fresh-wave-v1 only.

