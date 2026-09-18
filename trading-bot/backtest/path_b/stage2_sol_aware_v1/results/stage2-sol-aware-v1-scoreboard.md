# stage2-sol-aware-v1 scoreboard

Generated (UTC): 2026-09-17T03:37:20.564462+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL is the hard filter**.
- **Closed-bar only;** UTC week Monday 00:00–Monday 00:00 for PWH/PWL; long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-reopen-v1 IDs, no cmo-zone-v1 leave-50, no EMA/RSI, SMA200, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **ALMA (`alma-fast-slow-cross-v1`):** Sigma fixed at `6.0`; Offset locked at `{0.85, 0.90}`; Pairs locked at `(9,21)`, `(20,50)`, `(60,120)`. FIR Gaussian weights fallback implemented.
- **Roofing (`ehlers-roofing-zero-cross-v1`):** (hp, ss) locked at `(48,10)` lead, `(40,10)`, `(80,40)`. Documented 2-pole HighPass + 2-pole SuperSmoother IIR.
- **CG Osc (`ehlers-cg-osc-trigger-v1`):** Length in `{8, 10, 14, 20}`, default 10. Center-of-gravity FIR formula with 1-bar delayed trigger.
- **CMO (`cmo-zero-cross-v1`):** Length in `{14, 20, 25}`, default 20. Strictly zero-cross (Mode A) and SMA(9) cross (Mode B). Never leave -50 zone.
- **PWH/PWL (`pwh-pwl-accept-break-v1`):** Prior UTC ISO-week high/low. Mode A accept-break, Mode B break+retest. RVOL k in `{off, 1.0, 1.5}`.

## PASS_6m cells (LEAD)

- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_a|rvol_off): 6m ret=10.08% bh=5.72% ratio=1.763 wr=9.1% n=11 | full=FAIL ratio=0.074 n=50
- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_a|rvol1.0): 6m ret=10.71% bh=5.72% ratio=1.873 wr=10.0% n=10 | full=FAIL ratio=0.073 n=48
- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_a|rvol1.5): 6m ret=9.91% bh=5.72% ratio=1.733 wr=10.0% n=10 | full=FAIL ratio=-0.016 n=47
- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol_off): 6m ret=12.06% bh=5.72% ratio=2.109 wr=9.1% n=11 | full=FAIL ratio=0.420 n=45
- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol1.0): 6m ret=13.34% bh=5.72% ratio=2.333 wr=12.5% n=8 | full=FAIL ratio=0.495 n=40
- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol1.5): 6m ret=13.94% bh=5.72% ratio=2.438 wr=14.3% n=7 | full=FAIL ratio=0.261 n=34
- `[BTCUSDT] pwh-pwl-accept-break-v1` @ `1h` (mode_a|rvol1.5): 6m ret=7.37% bh=5.87% ratio=1.254 wr=11.1% n=9 | full=FAIL ratio=0.035 n=42
- `[BTCUSDT] alma-fast-slow-cross-v1` @ `4h` (mode_a|(60,120)|off0.85|sig6): 6m ret=31.39% bh=7.22% ratio=4.346 wr=57.1% n=7 | full=FAIL ratio=0.774 n=41
- `[BTCUSDT] alma-fast-slow-cross-v1` @ `4h` (mode_a|(60,120)|off0.9|sig6): 6m ret=22.12% bh=7.22% ratio=3.062 wr=44.4% n=9 | full=FAIL ratio=0.672 n=44
- `[ETHUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_a|rvol_off): 6m ret=12.90% bh=8.90% ratio=1.450 wr=8.3% n=12 | full=PASS ratio=2.327 n=52
- `[ETHUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_a|rvol1.0): 6m ret=12.90% bh=8.90% ratio=1.450 wr=8.3% n=12 | full=PASS ratio=2.324 n=52
- `[ETHUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_a|rvol1.5): 6m ret=12.90% bh=8.90% ratio=1.450 wr=8.3% n=12 | full=PASS ratio=2.395 n=52
- `[ETHUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol_off): 6m ret=18.36% bh=8.90% ratio=2.063 wr=8.3% n=12 | full=PASS ratio=2.544 n=43
- `[ETHUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol1.0): 6m ret=19.74% bh=8.90% ratio=2.218 wr=10.0% n=10 | full=PASS ratio=3.095 n=39
- `[ETHUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol1.5): 6m ret=20.87% bh=8.90% ratio=2.345 wr=11.1% n=9 | full=PASS ratio=3.839 n=33
- `[ETHUSDT] alma-fast-slow-cross-v1` @ `4h` (mode_a|(60,120)|off0.85|sig6): 6m ret=40.93% bh=10.63% ratio=3.850 wr=50.0% n=10 | full=FAIL ratio=-0.174 n=45
- `[ETHUSDT] alma-fast-slow-cross-v1` @ `4h` (mode_a|(60,120)|off0.9|sig6): 6m ret=31.89% bh=10.63% ratio=2.999 wr=36.4% n=11 | full=FAIL ratio=-1.457 n=48
- `[SOLUSDT] pwh-pwl-accept-break-v1` @ `15m` (mode_b|rvol_off): 6m ret=15.81% bh=10.25% ratio=1.542 wr=14.3% n=7 | full=PASS ratio=0.269 n=37
- `[SOLUSDT] alma-fast-slow-cross-v1` @ `4h` (mode_a|(60,120)|off0.9|sig6): 6m ret=19.93% bh=9.98% ratio=1.998 wr=54.5% n=11 | full=PASS ratio=-0.076 n=46

## All Scored Cells by Strategy

### pwh-pwl-accept-break-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 15m | mode_a|rvol_off | PASS(1.76) | 10.08 | 5.72 | 1.763 | 9.1 | 11 | FAIL(0.07) | 0.074 | 50 | 0.28 | 0.12 |  |
| BTCUSDT | 15m | mode_a|rvol1.0 | PASS(1.87) | 10.71 | 5.72 | 1.873 | 10.0 | 10 | FAIL(0.07) | 0.073 | 48 | 0.29 | 0.12 |  |
| BTCUSDT | 15m | mode_a|rvol1.5 | PASS(1.73) | 9.91 | 5.72 | 1.733 | 10.0 | 10 | FAIL(-0.02) | -0.016 | 47 | 0.27 | 0.05 |  |
| BTCUSDT | 15m | mode_b|rvol_off | PASS(2.11) | 12.06 | 5.72 | 2.109 | 9.1 | 11 | FAIL(0.42) | 0.420 | 45 | 0.32 | 0.38 |  |
| BTCUSDT | 15m | mode_b|rvol1.0 | PASS(2.33) | 13.34 | 5.72 | 2.333 | 12.5 | 8 | FAIL(0.49) | 0.495 | 40 | 0.35 | 0.43 |  |
| BTCUSDT | 15m | mode_b|rvol1.5 | PASS(2.44) | 13.94 | 5.72 | 2.438 | 14.3 | 7 | FAIL(0.26) | 0.261 | 34 | 0.36 | 0.25 |  |
| BTCUSDT | 1h | mode_a|rvol_off | FAIL(1.01) | 5.96 | 5.87 | 1.015 | 9.1 | 11 | FAIL(0.00) | 0.002 | 49 | 0.18 | 0.06 |  |
| BTCUSDT | 1h | mode_a|rvol1.0 | FAIL(1.01) | 5.96 | 5.87 | 1.015 | 9.1 | 11 | FAIL(0.02) | 0.023 | 48 | 0.18 | 0.08 |  |
| BTCUSDT | 1h | mode_a|rvol1.5 | PASS(1.25) | 7.37 | 5.87 | 1.254 | 11.1 | 9 | FAIL(0.04) | 0.035 | 42 | 0.21 | 0.09 |  |
| BTCUSDT | 1h | mode_b|rvol_off | FAIL(-0.60) | -3.53 | 5.87 | -0.601 | 11.1 | 9 | FAIL(0.32) | 0.317 | 39 | -0.09 | 0.28 |  |
| BTCUSDT | 1h | mode_b|rvol1.0 | FAIL(-0.65) | -3.81 | 5.87 | -0.649 | 11.1 | 9 | FAIL(-0.31) | -0.311 | 35 | -0.10 | -0.25 |  |
| BTCUSDT | 1h | mode_b|rvol1.5 | FAIL(-0.55) | -3.24 | 5.87 | -0.551 | 12.5 | 8 | FAIL(-0.18) | -0.177 | 26 | -0.08 | -0.13 |  |
| ETHUSDT | 15m | mode_a|rvol_off | PASS(1.45) | 12.90 | 8.90 | 1.450 | 8.3 | 12 | PASS(2.33) | 2.327 | 52 | 0.38 | 0.55 |  |
| ETHUSDT | 15m | mode_a|rvol1.0 | PASS(1.45) | 12.90 | 8.90 | 1.450 | 8.3 | 12 | PASS(2.32) | 2.324 | 52 | 0.38 | 0.55 |  |
| ETHUSDT | 15m | mode_a|rvol1.5 | PASS(1.45) | 12.90 | 8.90 | 1.450 | 8.3 | 12 | PASS(2.40) | 2.395 | 52 | 0.38 | 0.56 |  |
| ETHUSDT | 15m | mode_b|rvol_off | PASS(2.06) | 18.36 | 8.90 | 2.063 | 8.3 | 12 | PASS(2.54) | 2.544 | 43 | 0.50 | 0.49 |  |
| ETHUSDT | 15m | mode_b|rvol1.0 | PASS(2.22) | 19.74 | 8.90 | 2.218 | 10.0 | 10 | PASS(3.10) | 3.095 | 39 | 0.53 | 0.56 |  |
| ETHUSDT | 15m | mode_b|rvol1.5 | PASS(2.35) | 20.87 | 8.90 | 2.345 | 11.1 | 9 | PASS(3.84) | 3.839 | 33 | 0.55 | 0.66 |  |
| ETHUSDT | 1h | mode_a|rvol1.5 | FAIL(0.87) | 7.54 | 8.65 | 0.871 | 9.1 | 11 | PASS(9.02) | 9.017 | 47 | 0.26 | 1.34 |  |
| SOLUSDT | 15m | mode_a|rvol_off | FAIL(-0.86) | -8.83 | 10.25 | -0.861 | 0.0 | 9 | FAIL(1.24) | 1.236 | 44 | -0.23 | -0.87 | SOL filter |
| SOLUSDT | 15m | mode_a|rvol1.0 | FAIL(-0.86) | -8.83 | 10.25 | -0.861 | 0.0 | 9 | FAIL(1.24) | 1.242 | 44 | -0.23 | -0.88 | SOL filter |
| SOLUSDT | 15m | mode_a|rvol1.5 | FAIL(-0.86) | -8.83 | 10.25 | -0.861 | 0.0 | 9 | FAIL(1.24) | 1.235 | 44 | -0.23 | -0.87 | SOL filter |
| SOLUSDT | 15m | mode_b|rvol_off | PASS(1.54) | 15.81 | 10.25 | 1.542 | 14.3 | 7 | PASS(0.27) | 0.269 | 37 | 0.42 | -0.11 | SOL filter |
| SOLUSDT | 15m | mode_b|rvol1.0 | FAIL(-0.57) | -5.80 | 10.25 | -0.566 | 0.0 | 6 | PASS(0.96) | 0.956 | 34 | -0.15 | -0.65 | SOL filter |
| SOLUSDT | 15m | mode_b|rvol1.5 | FAIL(-0.56) | -5.75 | 10.25 | -0.561 | 0.0 | 6 | PASS(0.73) | 0.733 | 32 | -0.15 | -0.48 | SOL filter |
| BNBUSDT | 15m | mode_b|rvol_off | FAIL(-0.49) | -5.15 | 10.44 | -0.493 | 0.0 | 9 | FAIL(-0.56) | -0.556 | 42 | -0.13 | -0.54 |  |

### ehlers-cg-osc-trigger-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | mode_a|len8 | FAIL(-14.48) | -85.06 | 5.87 | -14.482 | 20.5 | 552 | FAIL(-3.11) | -3.110 | 2170 | -4.60 | -14.95 |  |
| BTCUSDT | 1h | mode_a|len10 | FAIL(-13.08) | -76.79 | 5.87 | -13.075 | 21.6 | 467 | FAIL(-3.10) | -3.099 | 1885 | -3.54 | -12.15 |  |
| BTCUSDT | 1h | mode_a|len14 | FAIL(-12.64) | -74.22 | 5.87 | -12.637 | 20.8 | 403 | FAIL(-3.09) | -3.087 | 1589 | -3.29 | -10.94 |  |
| BTCUSDT | 1h | mode_a|len20 | FAIL(-11.26) | -66.12 | 5.87 | -11.259 | 21.1 | 336 | FAIL(-3.05) | -3.045 | 1292 | -2.63 | -8.86 |  |
| BTCUSDT | 4h | mode_a|len8 | FAIL(-4.41) | -31.88 | 7.22 | -4.414 | 32.4 | 136 | FAIL(-2.42) | -2.416 | 544 | -0.91 | -3.28 |  |
| BTCUSDT | 4h | mode_a|len10 | FAIL(-4.60) | -33.25 | 7.22 | -4.604 | 29.8 | 121 | FAIL(-2.55) | -2.549 | 472 | -0.96 | -3.75 |  |
| BTCUSDT | 4h | mode_a|len14 | FAIL(-3.00) | -21.68 | 7.22 | -3.001 | 31.3 | 99 | FAIL(-2.15) | -2.153 | 384 | -0.57 | -2.57 |  |
| BTCUSDT | 4h | mode_a|len20 | FAIL(-2.64) | -19.05 | 7.22 | -2.637 | 35.6 | 73 | FAIL(-1.96) | -1.959 | 306 | -0.49 | -2.15 |  |

### alma-fast-slow-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | mode_a|(9,21)|off0.85|sig6 | FAIL(-9.44) | -55.44 | 5.87 | -9.439 | 23.6 | 263 | FAIL(-2.92) | -2.919 | 1025 | -1.93 | -6.45 |  |
| BTCUSDT | 1h | mode_a|(9,21)|off0.9|sig6 | FAIL(-10.15) | -59.61 | 5.87 | -10.150 | 21.5 | 279 | FAIL(-2.96) | -2.964 | 1099 | -2.17 | -7.05 |  |
| BTCUSDT | 1h | mode_a|(20,50)|off0.85|sig6 | FAIL(-2.56) | -15.01 | 5.87 | -2.556 | 31.5 | 108 | FAIL(-1.87) | -1.874 | 448 | -0.35 | -2.03 |  |
| BTCUSDT | 1h | mode_a|(20,50)|off0.9|sig6 | FAIL(-4.20) | -24.67 | 5.87 | -4.200 | 32.8 | 122 | FAIL(-2.32) | -2.315 | 498 | -0.64 | -3.11 |  |
| BTCUSDT | 1h | mode_a|(60,120)|off0.85|sig6 | FAIL(-0.74) | -4.32 | 5.87 | -0.735 | 35.0 | 40 | FAIL(-0.78) | -0.778 | 168 | -0.05 | -0.48 |  |
| BTCUSDT | 1h | mode_a|(60,120)|off0.9|sig6 | FAIL(0.30) | 1.76 | 5.87 | 0.299 | 31.1 | 45 | FAIL(-0.96) | -0.962 | 185 | 0.11 | -0.68 |  |
| BTCUSDT | 4h | mode_a|(9,21)|off0.85|sig6 | FAIL(-1.66) | -11.96 | 7.22 | -1.656 | 30.6 | 62 | FAIL(-1.44) | -1.437 | 246 | -0.28 | -1.28 |  |
| BTCUSDT | 4h | mode_a|(9,21)|off0.9|sig6 | FAIL(-2.77) | -20.03 | 7.22 | -2.773 | 25.7 | 70 | FAIL(-1.57) | -1.572 | 267 | -0.52 | -1.49 |  |
| BTCUSDT | 4h | mode_a|(20,50)|off0.85|sig6 | FAIL(-0.63) | -4.56 | 7.22 | -0.631 | 29.6 | 27 | FAIL(-0.05) | -0.046 | 107 | -0.03 | 0.23 |  |
| BTCUSDT | 4h | mode_a|(20,50)|off0.9|sig6 | FAIL(-0.19) | -1.40 | 7.22 | -0.194 | 34.5 | 29 | FAIL(0.14) | 0.137 | 116 | 0.04 | 0.37 |  |
| BTCUSDT | 4h | mode_a|(60,120)|off0.85|sig6 | PASS(4.35) | 31.39 | 7.22 | 4.346 | 57.1 | 7 | FAIL(0.77) | 0.774 | 41 | 0.75 | 0.74 |  |
| BTCUSDT | 4h | mode_a|(60,120)|off0.9|sig6 | PASS(3.06) | 22.12 | 7.22 | 3.062 | 44.4 | 9 | FAIL(0.67) | 0.672 | 44 | 0.56 | 0.66 |  |
| ETHUSDT | 4h | mode_a|(60,120)|off0.85|sig6 | PASS(3.85) | 40.93 | 10.63 | 3.850 | 50.0 | 10 | FAIL(-0.17) | -0.174 | 45 | 0.98 | 0.55 |  |
| ETHUSDT | 4h | mode_a|(60,120)|off0.9|sig6 | PASS(3.00) | 31.89 | 10.63 | 2.999 | 36.4 | 11 | FAIL(-1.46) | -1.457 | 48 | 0.80 | 0.33 |  |
| SOLUSDT | 4h | mode_a|(60,120)|off0.85|sig6 | FAIL(1.10) | 11.01 | 9.98 | 1.104 | 45.5 | 11 | PASS(-0.29) | -0.285 | 43 | 0.41 | 0.56 | SOL filter; near-miss 0.9-1.2x (FAIL) |
| SOLUSDT | 4h | mode_a|(60,120)|off0.9|sig6 | PASS(2.00) | 19.93 | 9.98 | 1.998 | 54.5 | 11 | PASS(-0.08) | -0.076 | 46 | 0.58 | 0.48 | SOL filter |
| BNBUSDT | 4h | mode_a|(60,120)|off0.9|sig6 | FAIL(-1.08) | -13.00 | 12.01 | -1.082 | 30.8 | 13 | FAIL(-0.68) | -0.680 | 47 | -0.30 | -0.51 |  |

### cmo-zero-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | mode_a|len14 | FAIL(-10.32) | -60.63 | 5.87 | -10.324 | 18.2 | 285 | FAIL(-3.00) | -2.999 | 1134 | -2.23 | -7.66 |  |
| BTCUSDT | 1h | mode_b|len14 | FAIL(-12.82) | -75.27 | 5.87 | -12.815 | 20.8 | 442 | FAIL(-3.10) | -3.096 | 1740 | -3.39 | -11.80 |  |
| BTCUSDT | 1h | mode_a|len20 | FAIL(-7.34) | -43.09 | 5.87 | -7.337 | 19.8 | 237 | FAIL(-2.88) | -2.884 | 954 | -1.32 | -6.06 |  |
| BTCUSDT | 1h | mode_b|len20 | FAIL(-12.97) | -76.20 | 5.87 | -12.975 | 20.3 | 444 | FAIL(-3.09) | -3.091 | 1710 | -3.48 | -11.27 |  |
| BTCUSDT | 1h | mode_a|len25 | FAIL(-7.81) | -45.89 | 5.87 | -7.814 | 18.0 | 206 | FAIL(-2.85) | -2.855 | 819 | -1.46 | -5.81 |  |
| BTCUSDT | 1h | mode_b|len25 | FAIL(-12.50) | -73.41 | 5.87 | -12.499 | 20.6 | 427 | FAIL(-3.10) | -3.095 | 1695 | -3.21 | -11.70 |  |
| BTCUSDT | 4h | mode_a|len14 | FAIL(-2.00) | -14.41 | 7.22 | -1.995 | 24.2 | 62 | FAIL(-1.17) | -1.169 | 271 | -0.32 | -0.89 |  |
| BTCUSDT | 4h | mode_b|len14 | FAIL(-3.25) | -23.49 | 7.22 | -3.252 | 27.4 | 95 | FAIL(-1.68) | -1.678 | 396 | -0.62 | -1.65 |  |
| BTCUSDT | 4h | mode_a|len20 | FAIL(-0.31) | -2.24 | 7.22 | -0.311 | 26.5 | 49 | FAIL(-1.24) | -1.238 | 218 | 0.03 | -0.99 |  |
| BTCUSDT | 4h | mode_b|len20 | FAIL(-4.45) | -32.16 | 7.22 | -4.452 | 26.0 | 104 | FAIL(-1.74) | -1.745 | 393 | -0.92 | -1.76 |  |
| BTCUSDT | 4h | mode_a|len25 | FAIL(-2.78) | -20.08 | 7.22 | -2.779 | 18.4 | 49 | FAIL(-1.68) | -1.682 | 219 | -0.49 | -1.60 |  |
| BTCUSDT | 4h | mode_b|len25 | FAIL(-4.85) | -35.06 | 7.22 | -4.854 | 20.7 | 111 | FAIL(-1.57) | -1.573 | 396 | -1.04 | -1.48 |  |

### ehlers-roofing-zero-cross-v1

| symbol | tf | mode/params | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|--------|----|-------------|---------|---------|--------|------|--------|------|-----------|-----------|--------|---------|-----------|-------|
| BTCUSDT | 1h | mode_a|hp48_ss10 | FAIL(-6.53) | -38.37 | 5.87 | -6.534 | 29.2 | 171 | FAIL(-2.73) | -2.732 | 702 | -1.16 | -4.88 |  |
| BTCUSDT | 1h | mode_a|hp40_ss10 | FAIL(-7.58) | -44.54 | 5.87 | -7.583 | 29.7 | 195 | FAIL(-2.72) | -2.719 | 758 | -1.42 | -4.79 |  |
| BTCUSDT | 1h | mode_a|hp80_ss40 | FAIL(-2.34) | -13.73 | 5.87 | -2.339 | 35.8 | 67 | FAIL(-1.69) | -1.686 | 271 | -0.32 | -1.69 |  |
| BTCUSDT | 4h | mode_a|hp48_ss10 | FAIL(1.18) | 8.53 | 7.22 | 1.181 | 38.1 | 42 | FAIL(0.04) | 0.042 | 169 | 0.28 | 0.26 |  |
| BTCUSDT | 4h | mode_a|hp40_ss10 | FAIL(0.26) | 1.86 | 7.22 | 0.257 | 42.6 | 47 | FAIL(-0.48) | -0.477 | 185 | 0.12 | -0.17 |  |
| BTCUSDT | 4h | mode_a|hp80_ss40 | FAIL(0.01) | 0.06 | 7.22 | 0.008 | 31.6 | 19 | FAIL(0.05) | 0.052 | 68 | 0.07 | 0.26 |  |

## Summary & Findings

- Total evaluated cells: 69
- Total PASS_6m cells: 19
- SOL evaluated cells: 8, SOL PASS_6m cells: 2
- Hard stop rules and gate compliance strictly enforced.
