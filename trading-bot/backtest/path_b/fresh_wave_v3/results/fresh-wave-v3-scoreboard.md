# fresh-wave-v3 scoreboard

Generated (UTC): 2026-09-06T21:05:40.725089+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes of prior families.**

## Scoring

- **LEAD gate:** 6m Mode-A ≥ **1.2×** B&H → `PASS/FAIL_6m`
- **Also:** full(~2y) Mode-A ≥ **1.2×** B&H → `PASS/FAIL_full` (informational)
- Costs: 0.10%/side fee + 5 bps slip; Mode-A **100%** + Mode-B ops **2.5%** (ops not scored)
- Symbol: BTCUSDT only. Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot. Single-TF (no HTF filter).
- Params frozen (no spray): Donchian entry20/exit10; ADX/DMI Wilder14 ADX>25; Elder EMA13; TSI(25,13)/EMA7; STC(23,50,10).

## Strategy rules (documented)

1. **donchian-breakout-v1** — Turtle S1. Enter close > prior **20**-bar high; exit close < prior **10**-bar low; no pyramid.
2. **adx-dmi-trend-v1** — Wilder **14**. Enter crossover(+DI, −DI) AND ADX>**25**; exit crossover(−DI, +DI).
3. **elder-ray-v1** — EMA**13**; Bull=High−EMA, Bear=Low−EMA. Enter EMA rising AND Bear<0 AND Bear rising; exit Bear turns down OR EMA falling.
4. **tsi-momentum-v1** — TSI(**25**,**13**) signal EMA(**7**). Enter crossover(TSI, signal) AND TSI>0; exit crossunder OR TSI<0.
5. **schaff-stc-v1** — STC(**23**,**50**,**10**). Enter crossover(STC, **25**); exit crossunder(STC, **75**).

## Scoreboard LEAD 6m PASS/FAIL_6m (ratio)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian-breakout-v1 | FAIL(-4.85) | FAIL(-4.05) | FAIL(-3.63) | FAIL(-1.90) | FAIL(-0.18) | FAIL(-0.12) | FAIL(-0.52) | FAIL(-0.82) | FAIL(0.27) | FAIL(0.40) | FAIL(0.90) | FAIL(1.14) | FAIL(0.84) | FAIL(0.43) | PASS(1.69) | FAIL(0.20) |
| adx-dmi-trend-v1 | FAIL(-3.51) | FAIL(-2.85) | FAIL(-2.09) | FAIL(-1.39) | FAIL(-0.28) | FAIL(0.69) | FAIL(0.20) | FAIL(-0.18) | FAIL(-0.29) | FAIL(-0.10) | FAIL(-0.06) | FAIL(-0.10) | FAIL(-0.12) | FAIL(0.01) | FAIL(-0.20) | FAIL(-0.41) |
| elder-ray-v1 | FAIL(-5.24) | FAIL(-5.22) | FAIL(-5.12) | FAIL(-4.53) | FAIL(-2.70) | FAIL(-3.47) | FAIL(-2.31) | FAIL(-1.84) | FAIL(-0.93) | FAIL(-0.98) | FAIL(-0.35) | FAIL(-0.17) | FAIL(-0.63) | FAIL(-0.35) | FAIL(-0.20) | FAIL(-0.03) |
| tsi-momentum-v1 | FAIL(-4.79) | FAIL(-3.52) | FAIL(-2.93) | FAIL(-1.68) | FAIL(-0.10) | FAIL(-0.73) | FAIL(-0.32) | FAIL(0.04) | FAIL(-0.27) | FAIL(-0.27) | FAIL(-0.34) | FAIL(-0.79) | FAIL(-0.55) | FAIL(-0.49) | FAIL(-0.33) | FAIL(0.00) |
| schaff-stc-v1 | FAIL(-5.19) | FAIL(-4.74) | FAIL(-4.05) | FAIL(-3.02) | FAIL(0.50) | FAIL(-1.15) | FAIL(-0.50) | FAIL(-0.45) | FAIL(0.84) | FAIL(0.06) | FAIL(0.16) | FAIL(0.28) | FAIL(0.39) | PASS(1.33) | PASS(1.31) | PASS(1.98) |

## Scoreboard full(~2y) PASS/FAIL_full (ratio)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian-breakout-v1 | FAIL(-2.31) | FAIL(-2.29) | FAIL(-2.27) | FAIL(-1.81) | FAIL(-0.23) | FAIL(-1.17) | FAIL(-0.27) | FAIL(-0.36) | FAIL(-0.01) | FAIL(-0.07) | FAIL(0.52) | FAIL(0.84) | FAIL(0.63) | FAIL(0.10) | FAIL(0.81) | FAIL(-0.09) |
| adx-dmi-trend-v1 | FAIL(-2.27) | FAIL(-2.14) | FAIL(-1.96) | FAIL(-1.56) | FAIL(-0.13) | FAIL(-0.74) | FAIL(0.19) | FAIL(-0.12) | FAIL(-0.58) | FAIL(-0.55) | FAIL(-0.67) | FAIL(-0.57) | FAIL(-0.42) | FAIL(-0.34) | FAIL(-0.30) | FAIL(-0.31) |
| elder-ray-v1 | FAIL(-2.31) | FAIL(-2.30) | FAIL(-2.31) | FAIL(-2.33) | FAIL(-2.20) | FAIL(-2.33) | FAIL(-2.04) | FAIL(-1.75) | FAIL(-1.35) | FAIL(-1.04) | FAIL(-0.66) | FAIL(-0.58) | FAIL(-0.58) | FAIL(0.09) | FAIL(0.20) | FAIL(-0.49) |
| tsi-momentum-v1 | FAIL(-2.31) | FAIL(-2.28) | FAIL(-2.25) | FAIL(-1.79) | FAIL(-0.80) | FAIL(-1.08) | FAIL(-0.87) | FAIL(0.09) | FAIL(-0.23) | FAIL(-0.11) | FAIL(0.09) | FAIL(0.25) | FAIL(0.11) | FAIL(-0.00) | FAIL(-0.15) | FAIL(0.78) |
| schaff-stc-v1 | FAIL(-2.31) | FAIL(-2.30) | FAIL(-2.30) | FAIL(-2.24) | FAIL(-1.15) | FAIL(-1.77) | FAIL(-1.21) | FAIL(-0.30) | PASS(1.71) | FAIL(-0.21) | FAIL(0.11) | FAIL(0.70) | FAIL(0.31) | FAIL(1.11) | FAIL(0.72) | PASS(2.94) |

## Combined (6m LEAD | full)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian-breakout-v1 | F-4.85|F-2.31 | F-4.05|F-2.29 | F-3.63|F-2.27 | F-1.90|F-1.81 | F-0.18|F-0.23 | F-0.12|F-1.17 | F-0.52|F-0.27 | F-0.82|F-0.36 | F0.27|F-0.01 | F0.40|F-0.07 | F0.90|F0.52 | F1.14|F0.84 | F0.84|F0.63 | F0.43|F0.10 | P1.69|F0.81 | F0.20|F-0.09 |
| adx-dmi-trend-v1 | F-3.51|F-2.27 | F-2.85|F-2.14 | F-2.09|F-1.96 | F-1.39|F-1.56 | F-0.28|F-0.13 | F0.69|F-0.74 | F0.20|F0.19 | F-0.18|F-0.12 | F-0.29|F-0.58 | F-0.10|F-0.55 | F-0.06|F-0.67 | F-0.10|F-0.57 | F-0.12|F-0.42 | F0.01|F-0.34 | F-0.20|F-0.30 | F-0.41|F-0.31 |
| elder-ray-v1 | F-5.24|F-2.31 | F-5.22|F-2.30 | F-5.12|F-2.31 | F-4.53|F-2.33 | F-2.70|F-2.20 | F-3.47|F-2.33 | F-2.31|F-2.04 | F-1.84|F-1.75 | F-0.93|F-1.35 | F-0.98|F-1.04 | F-0.35|F-0.66 | F-0.17|F-0.58 | F-0.63|F-0.58 | F-0.35|F0.09 | F-0.20|F0.20 | F-0.03|F-0.49 |
| tsi-momentum-v1 | F-4.79|F-2.31 | F-3.52|F-2.28 | F-2.93|F-2.25 | F-1.68|F-1.79 | F-0.10|F-0.80 | F-0.73|F-1.08 | F-0.32|F-0.87 | F0.04|F0.09 | F-0.27|F-0.23 | F-0.27|F-0.11 | F-0.34|F0.09 | F-0.79|F0.25 | F-0.55|F0.11 | F-0.49|F-0.00 | F-0.33|F-0.15 | F0.00|F0.78 |
| schaff-stc-v1 | F-5.19|F-2.31 | F-4.74|F-2.30 | F-4.05|F-2.30 | F-3.02|F-2.24 | F0.50|F-1.15 | F-1.15|F-1.77 | F-0.50|F-1.21 | F-0.45|F-0.30 | F0.84|P1.71 | F0.06|F-0.21 | F0.16|F0.11 | F0.28|F0.70 | F0.39|F0.31 | P1.33|F1.11 | P1.31|F0.72 | P1.98|P2.94 |

_Legend: P=PASS F=FAIL; `P6m|Pfull` compact ratios._

## PASS_6m cells (LEAD)

- `schaff-stc-v1` @ `2d`: 6m ret=27.16% bh=13.72% ratio=1.980 wr=100.0% n=1 | full=PASS ratio=2.942 n=9
- `donchian-breakout-v1` @ `1d`: 6m ret=28.20% bh=16.73% ratio=1.685 wr=100.0% n=2 | full=FAIL ratio=0.806 n=11
- `schaff-stc-v1` @ `1d`: 6m ret=22.00% bh=16.73% ratio=1.315 wr=66.7% n=6 | full=FAIL ratio=0.718 n=22
- `schaff-stc-v1` @ `12h`: 6m ret=28.09% bh=21.14% ratio=1.329 wr=81.8% n=11 | full=FAIL ratio=1.110 n=44

## PASS_full cells (informational; not LEAD)

- `schaff-stc-v1` @ `2d`: full ret=117.49% bh=39.93% ratio=2.942 wr=55.6% n=9 | 6m=PASS
- `schaff-stc-v1` @ `4h`: full ret=81.53% bh=47.71% ratio=1.709 wr=39.3% n=122 | 6m=FAIL

## Cell detail (Mode-A gate; both windows)

| strategy | tf | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ret% | full_bh% | full_ratio | full_wr% | full_n | ops_6m% | ops_full% | error |
|----------|----|----|---------|--------|----------|--------|------|------|-----------|----------|------------|----------|--------|---------|-----------|-------|
| donchian-breakout-v1 | 2d | FAIL | 2.77 | 13.72 | 0.202 | 50.0 | 2 | FAIL | -3.46 | 39.93 | -0.087 | 42.9 | 7 | 0.08 | 0.15 |  |
| adx-dmi-trend-v1 | 2d | FAIL | -5.67 | 13.72 | -0.413 | 0.0 | 1 | FAIL | -12.26 | 39.93 | -0.307 | 0.0 | 3 | -0.14 | -0.32 |  |
| elder-ray-v1 | 2d | FAIL | -0.37 | 13.72 | -0.027 | 37.5 | 8 | FAIL | -19.52 | 39.93 | -0.489 | 33.3 | 30 | 0.00 | -0.49 |  |
| tsi-momentum-v1 | 2d | FAIL | 0.00 | 13.72 | 0.000 | 0.0 | 0 | FAIL | 31.00 | 39.93 | 0.776 | 33.3 | 6 | 0.00 | 0.94 |  |
| schaff-stc-v1 | 2d | PASS | 27.16 | 13.72 | 1.980 | 100.0 | 1 | PASS | 117.49 | 39.93 | 2.942 | 55.6 | 9 | 0.68 | 2.50 |  |
| donchian-breakout-v1 | 1d | PASS | 28.20 | 16.73 | 1.685 | 100.0 | 2 | FAIL | 38.28 | 47.49 | 0.806 | 45.5 | 11 | 0.68 | 1.13 |  |
| adx-dmi-trend-v1 | 1d | FAIL | -3.28 | 16.73 | -0.196 | 0.0 | 1 | FAIL | -14.29 | 47.49 | -0.301 | 0.0 | 4 | -0.08 | -0.38 |  |
| elder-ray-v1 | 1d | FAIL | -3.43 | 16.73 | -0.205 | 45.5 | 11 | FAIL | 9.53 | 47.49 | 0.201 | 43.4 | 53 | -0.08 | 0.29 |  |
| tsi-momentum-v1 | 1d | FAIL | -5.45 | 16.73 | -0.326 | 33.3 | 3 | FAIL | -7.01 | 47.49 | -0.148 | 25.0 | 12 | -0.14 | -0.11 |  |
| schaff-stc-v1 | 1d | PASS | 22.00 | 16.73 | 1.315 | 66.7 | 6 | FAIL | 34.11 | 47.49 | 0.718 | 50.0 | 22 | 0.58 | 1.01 |  |
| donchian-breakout-v1 | 12h | FAIL | 9.09 | 21.14 | 0.430 | 50.0 | 6 | FAIL | 4.95 | 48.10 | 0.103 | 37.5 | 24 | 0.26 | 0.32 |  |
| adx-dmi-trend-v1 | 12h | FAIL | 0.27 | 21.14 | 0.013 | 50.0 | 2 | FAIL | -16.28 | 48.10 | -0.338 | 10.0 | 10 | 0.01 | -0.44 |  |
| elder-ray-v1 | 12h | FAIL | -7.39 | 21.14 | -0.350 | 44.4 | 27 | FAIL | 4.42 | 48.10 | 0.092 | 43.4 | 106 | -0.18 | 0.17 |  |
| tsi-momentum-v1 | 12h | FAIL | -10.37 | 21.14 | -0.491 | 30.0 | 10 | FAIL | -0.02 | 48.10 | -0.000 | 26.1 | 23 | -0.27 | 0.07 |  |
| schaff-stc-v1 | 12h | PASS | 28.09 | 21.14 | 1.329 | 81.8 | 11 | FAIL | 53.41 | 48.10 | 1.110 | 54.5 | 44 | 0.68 | 1.31 |  |
| donchian-breakout-v1 | 9h | FAIL | 15.67 | 18.61 | 0.842 | 28.6 | 7 | FAIL | 31.73 | 50.40 | 0.630 | 32.1 | 28 | 0.42 | 0.89 |  |
| adx-dmi-trend-v1 | 9h | FAIL | -2.24 | 18.61 | -0.121 | 40.0 | 5 | FAIL | -21.19 | 50.40 | -0.420 | 15.8 | 19 | -0.06 | -0.56 |  |
| elder-ray-v1 | 9h | FAIL | -11.64 | 18.61 | -0.626 | 41.5 | 41 | FAIL | -29.23 | 50.40 | -0.580 | 37.2 | 148 | -0.30 | -0.80 |  |
| tsi-momentum-v1 | 9h | FAIL | -10.25 | 18.61 | -0.551 | 20.0 | 10 | FAIL | 5.64 | 50.40 | 0.112 | 30.3 | 33 | -0.27 | 0.20 |  |
| schaff-stc-v1 | 9h | FAIL | 7.30 | 18.61 | 0.392 | 37.5 | 16 | FAIL | 15.67 | 50.40 | 0.311 | 42.4 | 59 | 0.24 | 0.55 |  |
| donchian-breakout-v1 | 7h | FAIL | 22.46 | 19.69 | 1.141 | 42.9 | 7 | FAIL | 40.39 | 48.24 | 0.837 | 37.5 | 32 | 0.58 | 1.07 |  |
| adx-dmi-trend-v1 | 7h | FAIL | -1.90 | 19.69 | -0.096 | 0.0 | 3 | FAIL | -27.73 | 48.24 | -0.575 | 9.1 | 22 | -0.05 | -0.79 |  |
| elder-ray-v1 | 7h | FAIL | -3.36 | 19.69 | -0.170 | 46.5 | 43 | FAIL | -28.15 | 48.24 | -0.584 | 39.2 | 186 | -0.08 | -0.76 |  |
| tsi-momentum-v1 | 7h | FAIL | -15.50 | 19.69 | -0.787 | 0.0 | 12 | FAIL | 11.89 | 48.24 | 0.247 | 28.3 | 46 | -0.42 | 0.37 |  |
| schaff-stc-v1 | 7h | FAIL | 5.51 | 19.69 | 0.280 | 42.9 | 21 | FAIL | 33.69 | 48.24 | 0.698 | 46.1 | 76 | 0.21 | 0.95 |  |
| donchian-breakout-v1 | 6h | FAIL | 17.09 | 18.91 | 0.904 | 30.0 | 10 | FAIL | 24.90 | 47.85 | 0.520 | 38.1 | 42 | 0.46 | 0.77 |  |
| adx-dmi-trend-v1 | 6h | FAIL | -1.21 | 18.91 | -0.064 | 40.0 | 5 | FAIL | -31.94 | 47.85 | -0.667 | 22.2 | 27 | -0.03 | -0.92 |  |
| elder-ray-v1 | 6h | FAIL | -6.68 | 18.91 | -0.353 | 45.1 | 51 | FAIL | -31.64 | 47.85 | -0.661 | 35.4 | 206 | -0.16 | -0.88 |  |
| tsi-momentum-v1 | 6h | FAIL | -6.36 | 18.91 | -0.336 | 36.4 | 11 | FAIL | 4.42 | 47.85 | 0.092 | 34.9 | 43 | -0.16 | 0.16 |  |
| schaff-stc-v1 | 6h | FAIL | 3.06 | 18.91 | 0.162 | 34.8 | 23 | FAIL | 5.11 | 47.85 | 0.107 | 42.2 | 83 | 0.17 | 0.37 |  |
| donchian-breakout-v1 | 5h | FAIL | 7.26 | 18.33 | 0.396 | 42.9 | 14 | FAIL | -3.33 | 47.36 | -0.070 | 36.4 | 55 | 0.24 | 0.16 |  |
| adx-dmi-trend-v1 | 5h | FAIL | -1.77 | 18.33 | -0.097 | 42.9 | 7 | FAIL | -25.88 | 47.36 | -0.547 | 31.4 | 35 | -0.04 | -0.72 |  |
| elder-ray-v1 | 5h | FAIL | -17.95 | 18.33 | -0.980 | 31.1 | 61 | FAIL | -49.40 | 47.36 | -1.043 | 32.0 | 253 | -0.48 | -1.63 |  |
| tsi-momentum-v1 | 5h | FAIL | -4.97 | 18.33 | -0.271 | 26.7 | 15 | FAIL | -5.05 | 47.36 | -0.107 | 28.3 | 60 | -0.12 | -0.08 |  |
| schaff-stc-v1 | 5h | FAIL | 1.02 | 18.33 | 0.056 | 40.0 | 25 | FAIL | -10.04 | 47.36 | -0.212 | 38.4 | 99 | 0.09 | 0.01 |  |
| donchian-breakout-v1 | 4h | FAIL | 4.86 | 18.24 | 0.266 | 43.8 | 16 | FAIL | -0.24 | 47.71 | -0.005 | 38.1 | 63 | 0.16 | 0.20 |  |
| adx-dmi-trend-v1 | 4h | FAIL | -5.26 | 18.24 | -0.288 | 21.4 | 14 | FAIL | -27.57 | 47.71 | -0.578 | 17.8 | 45 | -0.13 | -0.77 |  |
| elder-ray-v1 | 4h | FAIL | -16.95 | 18.24 | -0.929 | 28.9 | 90 | FAIL | -64.62 | 47.71 | -1.354 | 29.0 | 328 | -0.44 | -2.50 |  |
| tsi-momentum-v1 | 4h | FAIL | -4.89 | 18.24 | -0.268 | 30.0 | 20 | FAIL | -10.93 | 47.71 | -0.229 | 26.4 | 72 | -0.12 | -0.24 |  |
| schaff-stc-v1 | 4h | FAIL | 15.39 | 18.24 | 0.843 | 48.3 | 29 | PASS | 81.53 | 47.71 | 1.709 | 39.3 | 122 | 0.40 | 1.70 |  |
| donchian-breakout-v1 | 3h | FAIL | -15.05 | 18.34 | -0.820 | 26.9 | 26 | FAIL | -16.77 | 45.98 | -0.365 | 30.7 | 88 | -0.35 | -0.25 |  |
| adx-dmi-trend-v1 | 3h | FAIL | -3.35 | 18.34 | -0.183 | 27.3 | 11 | FAIL | -5.71 | 45.98 | -0.124 | 22.4 | 49 | -0.08 | -0.03 |  |
| elder-ray-v1 | 3h | FAIL | -33.76 | 18.34 | -1.841 | 24.8 | 117 | FAIL | -80.69 | 45.98 | -1.755 | 26.4 | 444 | -1.01 | -3.97 |  |
| tsi-momentum-v1 | 3h | FAIL | 0.81 | 18.34 | 0.044 | 27.3 | 22 | FAIL | 4.27 | 45.98 | 0.093 | 30.8 | 91 | 0.05 | 0.20 |  |
| schaff-stc-v1 | 3h | FAIL | -8.30 | 18.34 | -0.453 | 35.7 | 42 | FAIL | -13.76 | 45.98 | -0.299 | 41.1 | 168 | -0.20 | -0.19 |  |
| donchian-breakout-v1 | 2h | FAIL | -9.25 | 17.95 | -0.515 | 27.8 | 36 | FAIL | -11.45 | 42.56 | -0.269 | 31.8 | 132 | -0.19 | -0.10 |  |
| adx-dmi-trend-v1 | 2h | FAIL | 3.51 | 17.95 | 0.195 | 50.0 | 18 | FAIL | 8.22 | 42.56 | 0.193 | 32.3 | 62 | 0.09 | 0.31 |  |
| elder-ray-v1 | 2h | FAIL | -41.40 | 17.95 | -2.306 | 21.8 | 165 | FAIL | -86.84 | 42.56 | -2.041 | 24.2 | 677 | -1.31 | -4.87 |  |
| tsi-momentum-v1 | 2h | FAIL | -5.67 | 17.95 | -0.316 | 33.3 | 39 | FAIL | -37.10 | 42.56 | -0.872 | 29.2 | 144 | -0.12 | -1.08 |  |
| schaff-stc-v1 | 2h | FAIL | -8.90 | 17.95 | -0.496 | 36.4 | 66 | FAIL | -51.38 | 42.56 | -1.207 | 37.5 | 261 | -0.18 | -1.53 |  |
| donchian-breakout-v1 | 1h | FAIL | -2.32 | 18.69 | -0.124 | 35.0 | 60 | FAIL | -49.54 | 42.23 | -1.173 | 32.7 | 263 | -0.01 | -1.53 |  |
| adx-dmi-trend-v1 | 1h | FAIL | 12.96 | 18.69 | 0.694 | 25.0 | 32 | FAIL | -31.40 | 42.23 | -0.744 | 21.5 | 130 | 0.36 | -0.86 |  |
| elder-ray-v1 | 1h | FAIL | -64.85 | 18.69 | -3.471 | 20.4 | 343 | FAIL | -98.42 | 42.23 | -2.331 | 21.2 | 1368 | -2.57 | -9.79 |  |
| tsi-momentum-v1 | 1h | FAIL | -13.65 | 18.69 | -0.731 | 28.9 | 76 | FAIL | -45.60 | 42.23 | -1.080 | 26.5 | 309 | -0.35 | -1.44 |  |
| schaff-stc-v1 | 1h | FAIL | -21.54 | 18.69 | -1.153 | 32.0 | 122 | FAIL | -74.89 | 42.23 | -1.773 | 31.5 | 521 | -0.55 | -3.18 |  |
| donchian-breakout-v1 | 90m | FAIL | -3.29 | 18.30 | -0.180 | 29.5 | 44 | FAIL | -9.77 | 42.68 | -0.229 | 34.7 | 167 | -0.03 | -0.10 |  |
| adx-dmi-trend-v1 | 90m | FAIL | -5.16 | 18.30 | -0.282 | 30.0 | 20 | FAIL | -5.39 | 42.68 | -0.126 | 30.1 | 83 | -0.13 | -0.08 |  |
| elder-ray-v1 | 90m | FAIL | -49.46 | 18.30 | -2.703 | 20.7 | 227 | FAIL | -93.85 | 42.68 | -2.199 | 22.5 | 923 | -1.68 | -6.66 |  |
| tsi-momentum-v1 | 90m | FAIL | -1.74 | 18.30 | -0.095 | 26.9 | 52 | FAIL | -34.21 | 42.68 | -0.801 | 27.0 | 211 | 0.00 | -0.93 |  |
| schaff-stc-v1 | 90m | FAIL | 9.18 | 18.30 | 0.501 | 40.0 | 80 | FAIL | -49.16 | 42.68 | -1.152 | 36.5 | 337 | 0.28 | -1.43 |  |
| donchian-breakout-v1 | 30m | FAIL | -36.11 | 18.97 | -1.904 | 24.1 | 133 | FAIL | -77.69 | 42.96 | -1.809 | 26.5 | 536 | -1.08 | -3.51 |  |
| adx-dmi-trend-v1 | 30m | FAIL | -26.42 | 18.97 | -1.393 | 12.7 | 63 | FAIL | -66.88 | 42.96 | -1.557 | 13.4 | 254 | -0.76 | -2.68 |  |
| elder-ray-v1 | 30m | FAIL | -85.97 | 18.97 | -4.533 | 14.7 | 672 | FAIL | -99.98 | 42.96 | -2.327 | 14.7 | 2771 | -4.77 | -18.72 |  |
| tsi-momentum-v1 | 30m | FAIL | -31.90 | 18.97 | -1.682 | 26.2 | 160 | FAIL | -76.94 | 42.96 | -1.791 | 22.3 | 600 | -0.94 | -3.53 |  |
| schaff-stc-v1 | 30m | FAIL | -57.22 | 18.97 | -3.017 | 27.7 | 271 | FAIL | -96.30 | 42.96 | -2.242 | 27.6 | 1053 | -2.04 | -7.66 |  |
| donchian-breakout-v1 | 15m | FAIL | -69.56 | 19.15 | -3.631 | 18.5 | 292 | FAIL | -98.24 | 43.30 | -2.269 | 22.0 | 1132 | -2.89 | -9.45 |  |
| adx-dmi-trend-v1 | 15m | FAIL | -39.95 | 19.15 | -2.086 | 14.0 | 136 | FAIL | -84.80 | 43.30 | -1.958 | 15.4 | 505 | -1.25 | -4.56 |  |
| elder-ray-v1 | 15m | FAIL | -98.14 | 19.15 | -5.123 | 9.5 | 1349 | FAIL | -100.00 | 43.30 | -2.310 | 10.6 | 5409 | -9.46 | -33.07 |  |
| tsi-momentum-v1 | 15m | FAIL | -56.13 | 19.15 | -2.930 | 20.0 | 305 | FAIL | -97.37 | 43.30 | -2.249 | 17.1 | 1205 | -2.02 | -8.63 |  |
| schaff-stc-v1 | 15m | FAIL | -77.55 | 19.15 | -4.049 | 25.0 | 535 | FAIL | -99.74 | 43.30 | -2.303 | 25.0 | 2103 | -3.63 | -13.58 |  |
| donchian-breakout-v1 | 10m | FAIL | -77.25 | 19.09 | -4.046 | 18.2 | 422 | FAIL | -99.54 | 43.46 | -2.290 | 20.5 | 1683 | -3.60 | -12.44 |  |
| adx-dmi-trend-v1 | 10m | FAIL | -54.34 | 19.09 | -2.846 | 7.5 | 201 | FAIL | -92.90 | 43.46 | -2.138 | 12.2 | 724 | -1.93 | -6.37 |  |
| elder-ray-v1 | 10m | FAIL | -99.67 | 19.09 | -5.220 | 7.3 | 1934 | FAIL | -100.00 | 43.46 | -2.301 | 8.4 | 7923 | -13.29 | -44.55 |  |
| tsi-momentum-v1 | 10m | FAIL | -67.23 | 19.09 | -3.521 | 15.0 | 412 | FAIL | -99.29 | 43.46 | -2.285 | 15.2 | 1753 | -2.73 | -11.57 |  |
| schaff-stc-v1 | 10m | FAIL | -90.55 | 19.09 | -4.742 | 20.5 | 820 | FAIL | -99.99 | 43.46 | -2.301 | 21.3 | 3237 | -5.68 | -20.91 |  |
| donchian-breakout-v1 | 5m | FAIL | -92.59 | 19.08 | -4.854 | 16.2 | 839 | FAIL | -100.00 | 43.29 | -2.310 | 16.3 | 3458 | -6.26 | -23.64 |  |
| adx-dmi-trend-v1 | 5m | FAIL | -67.03 | 19.08 | -3.514 | 10.1 | 368 | FAIL | -98.35 | 43.29 | -2.272 | 10.4 | 1370 | -2.73 | -9.70 |  |
| elder-ray-v1 | 5m | FAIL | -100.00 | 19.08 | -5.242 | 4.7 | 3552 | FAIL | -100.00 | 43.29 | -2.310 | 5.3 | 14877 | -22.99 | -66.92 |  |
| tsi-momentum-v1 | 5m | FAIL | -91.32 | 19.08 | -4.787 | 9.9 | 849 | FAIL | -100.00 | 43.29 | -2.310 | 11.4 | 3571 | -5.91 | -22.93 |  |
| schaff-stc-v1 | 5m | FAIL | -99.01 | 19.08 | -5.190 | 15.2 | 1603 | FAIL | -100.00 | 43.29 | -2.310 | 16.1 | 6503 | -10.86 | -38.16 |  |

## Caveats

- LEAD = 6m Mode-A only. full(~2y) is reported for context, not paper clearance.
- Mode-B ops 2.5% is parallel / informational only.
- No param spray / SMA200/RSI/BB/ST grafts. Excluded: owned (EMA/RSI, openproxy, BB, KAMA, dual-mom, SMA200, ST), v1 (Connors, NR7, Ichimoku, HA, OBV), v2 (PSAR, CCI, Aroon, Williams, Vortex), Jewel/Hub, Black Skull.
- No OOS (ETH/SOL/BNB) in this PR — parent runs after BTC PASS_6m.
- Hold prior PRs #15–#18 unmerged; this PR is additive fresh-wave-v3 only.
- Do NOT wire paper for ema-rsi@9h.

