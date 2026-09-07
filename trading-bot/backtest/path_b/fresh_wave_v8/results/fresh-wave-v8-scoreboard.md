# fresh-wave-v8 scoreboard

Generated (UTC): 2026-09-07T08:44:41.432989+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring

- **LEAD gate:** 6m Mode-A ≥ **1.2×** B&H → `PASS/FAIL_6m` (≥1 trade). WR informational.
- **Also:** full(~2y) Mode-A ≥ **1.2×** B&H → `PASS/FAIL_full` (informational)
- Costs: 0.10%/side fee + 5 bps slip; Mode-A **100%** + Mode-B ops **2.5%** (ops not scored)
- Symbol: BTCUSDT only (no ETH OOS in this PR). Agg: 5m→sub-daily; 1d native; 2d=2×1d.
- Gann HiLo Activator **n=3** Mode A SAR-style flip (≠ PSAR); prefer 1h–1d; full 16 OK.
- Asian→London: box **00:00–07:00 UTC**; break after 07:00; TP **1×** height or **16:00** flat; stop mid; score **5m/15m** only. Forbidden Session ORB / Donchian.
- Force Index **EMA(13)** zero-cross alone. Forbidden Triple Screen FI(2) / Elder Ray.
- Cyber Cycle **α=0.07** × Trigger=Cycle[1]; no Fisher graft; prefer 1h–1d.
- Williams Fractals-only (5-bar confirmed); no Alligator / Donchian.
- Watchlist (no paper): ema-rsi@9h, schaff@2d. v7 OOS hard-stop held. Hold #15–#25 unmerged.

## Strategy rules (documented)

1. **gann-hilo-activator-v1** — close flips above HiLo activator → long; flips below → exit.
2. **asian-london-break-v1** — Asian box break after 07:00 UTC; mid stop; TP 1× or 16:00 flat.
3. **force-index-13-v1** — crossover(FI13, 0) / crossunder(FI13, 0).
4. **cyber-cycle-v1** — crossover(Cycle, Trigger) / crossunder(Cycle, Trigger).
5. **williams-fractals-v1** — close > last up-fractal high; exit close < last down-fractal low.

## PASS_6m cells (LEAD)

- `gann-hilo-activator-v1` @ `2d|n3`: 6m ret=26.93% bh=13.36% ratio=2.016 wr=50.0% n=6 | full=FAIL ratio=-0.483 n=27
- `force-index-13-v1` @ `12h|ema13`: 6m ret=29.78% bh=18.56% ratio=1.604 wr=41.2% n=17 | full=FAIL ratio=0.561 n=79
- `force-index-13-v1` @ `2d|ema13`: 6m ret=20.23% bh=13.36% ratio=1.515 wr=33.3% n=6 | full=PASS ratio=2.299 n=20
- `cyber-cycle-v1` @ `2d|a0.07`: 6m ret=20.68% bh=13.36% ratio=1.548 wr=66.7% n=6 | full=FAIL ratio=-0.128 n=33
- `williams-fractals-v1` @ `1d|w2`: 6m ret=26.36% bh=16.27% ratio=1.620 wr=66.7% n=3 | full=FAIL ratio=0.918 n=15
- `williams-fractals-v1` @ `2d|w2`: 6m ret=22.50% bh=13.36% ratio=1.685 wr=100.0% n=1 | full=PASS ratio=1.373 n=8

## PASS_full cells (informational; not LEAD)

- `force-index-13-v1` @ `2d|ema13`: full ret=90.80% bh=39.49% ratio=2.299 wr=35.0% n=20 | 6m=PASS
- `williams-fractals-v1` @ `2d|w2`: full ret=54.22% bh=39.49% ratio=1.373 wr=50.0% n=8 | 6m=PASS

## LEAD 6m by family (all scored cells)

### gann-hilo-activator-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 1d|n3 | FAIL(0.97) | 15.73 | 16.27 | 0.967 | 50.0 | 12 | FAIL(0.15) | 0.150 | 50 | 0.42 | 0.38 |  |
| 12h|n3 | FAIL(0.57) | 10.58 | 18.56 | 0.570 | 37.0 | 27 | FAIL(0.52) | 0.525 | 99 | 0.33 | 0.80 |  |
| 9h|n3 | FAIL(1.11) | 22.95 | 20.75 | 1.106 | 38.2 | 34 | FAIL(0.46) | 0.460 | 125 | 0.58 | 0.74 |  |
| 7h|n3 | FAIL(-0.34) | -7.06 | 20.74 | -0.340 | 29.2 | 48 | FAIL(-0.51) | -0.505 | 174 | -0.12 | -0.43 |  |
| 6h|n3 | FAIL(-0.00) | -0.04 | 20.90 | -0.002 | 30.8 | 52 | FAIL(-0.89) | -0.889 | 203 | 0.06 | -1.12 |  |
| 5h|n3 | FAIL(-0.10) | -2.03 | 20.35 | -0.100 | 42.4 | 59 | FAIL(-0.73) | -0.728 | 240 | 0.02 | -0.80 |  |
| 4h|n3 | FAIL(-0.67) | -13.85 | 20.65 | -0.671 | 31.6 | 79 | FAIL(-1.06) | -1.056 | 310 | -0.34 | -1.55 |  |
| 3h|n3 | FAIL(-1.04) | -19.34 | 18.62 | -1.039 | 32.0 | 100 | FAIL(-1.31) | -1.309 | 418 | -0.48 | -2.21 |  |
| 2h|n3 | FAIL(-1.52) | -28.04 | 18.45 | -1.520 | 24.5 | 151 | FAIL(-1.73) | -1.726 | 615 | -0.74 | -4.02 |  |
| 1h|n3 | FAIL(-3.33) | -64.10 | 19.24 | -3.331 | 22.8 | 324 | FAIL(-2.04) | -2.038 | 1288 | -2.48 | -9.29 |  |
| 2d|n3 | PASS(2.02) | 26.93 | 13.36 | 2.016 | 50.0 | 6 | FAIL(-0.48) | -0.483 | 27 | 0.67 | -0.27 |  |
| 90m|n3 | FAIL(-2.47) | -46.22 | 18.69 | -2.473 | 24.3 | 210 | FAIL(-1.87) | -1.871 | 832 | -1.47 | -5.39 |  |
| 30m|n3 | FAIL(-4.48) | -85.28 | 19.02 | -4.484 | 18.9 | 655 | FAIL(-2.04) | -2.037 | 2626 | -4.63 | -17.98 |  |
| 15m|n3 | FAIL(-5.25) | -98.34 | 18.72 | -5.253 | 15.0 | 1337 | FAIL(-1.98) | -1.979 | 5396 | -9.69 | -33.90 |  |
| 10m|n3 | FAIL(-5.35) | -99.80 | 18.66 | -5.349 | 12.8 | 2036 | FAIL(-1.98) | -1.982 | 8233 | -14.30 | -46.92 |  |
| 5m|n3 | FAIL(-5.35) | -100.00 | 18.68 | -5.353 | 9.4 | 4148 | FAIL(-2.00) | -2.004 | 16801 | -27.00 | -71.94 |  |

### asian-london-break-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 5m|box00-07|tp1|flat16|mid | FAIL(-1.66) | -31.10 | 18.68 | -1.665 | 29.4 | 102 | FAIL(-1.39) | -1.388 | 396 | -0.92 | -2.86 |  |
| 15m|box00-07|tp1|flat16|mid | FAIL(-1.71) | -31.98 | 18.72 | -1.708 | 28.3 | 99 | FAIL(-1.36) | -1.360 | 380 | -0.95 | -2.82 |  |

### force-index-13-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 1d|ema13 | FAIL(0.83) | 13.57 | 16.27 | 0.834 | 28.6 | 14 | FAIL(0.75) | 0.755 | 47 | 0.39 | 1.12 |  |
| 12h|ema13 | PASS(1.60) | 29.78 | 18.56 | 1.604 | 41.2 | 17 | FAIL(0.56) | 0.561 | 79 | 0.73 | 0.90 |  |
| 9h|ema13 | FAIL(0.79) | 16.33 | 20.75 | 0.787 | 32.1 | 28 | FAIL(0.09) | 0.092 | 103 | 0.47 | 0.45 |  |
| 7h|ema13 | FAIL(0.30) | 6.20 | 20.74 | 0.299 | 26.3 | 38 | FAIL(-0.84) | -0.844 | 148 | 0.23 | -0.98 |  |
| 6h|ema13 | FAIL(0.61) | 12.73 | 20.90 | 0.609 | 22.2 | 36 | FAIL(-0.69) | -0.692 | 155 | 0.38 | -0.67 |  |
| 5h|ema13 | FAIL(-0.19) | -3.76 | 20.35 | -0.185 | 19.1 | 47 | FAIL(-0.84) | -0.842 | 171 | -0.02 | -1.04 |  |
| 4h|ema13 | FAIL(-0.34) | -6.96 | 20.65 | -0.337 | 26.4 | 53 | FAIL(-0.97) | -0.966 | 217 | -0.10 | -1.28 |  |
| 2d|ema13 | PASS(1.51) | 20.23 | 13.36 | 1.515 | 33.3 | 6 | PASS(2.30) | 2.299 | 20 | 0.53 | 2.05 |  |
| 3h|ema13 | FAIL(-0.85) | -15.83 | 18.62 | -0.850 | 21.8 | 78 | FAIL(-1.47) | -1.473 | 306 | -0.37 | -2.71 |  |
| 2h|ema13 | FAIL(-1.81) | -33.47 | 18.45 | -1.814 | 22.8 | 127 | FAIL(-1.57) | -1.574 | 459 | -0.95 | -3.17 |  |
| 1h|ema13 | FAIL(-2.74) | -52.76 | 19.24 | -2.742 | 19.1 | 251 | FAIL(-1.99) | -1.993 | 1008 | -1.78 | -7.50 |  |
| 90m|ema13 | FAIL(-1.83) | -34.13 | 18.69 | -1.826 | 19.4 | 170 | FAIL(-1.73) | -1.734 | 635 | -0.96 | -4.20 |  |
| 30m|ema13 | FAIL(-4.26) | -80.96 | 19.02 | -4.257 | 15.1 | 531 | FAIL(-2.03) | -2.032 | 2033 | -3.99 | -13.73 |  |
| 15m|ema13 | FAIL(-5.11) | -95.60 | 18.72 | -5.107 | 12.3 | 1022 | FAIL(-1.98) | -1.979 | 4230 | -7.54 | -27.62 |  |
| 10m|ema13 | FAIL(-5.30) | -98.78 | 18.66 | -5.295 | 12.0 | 1520 | FAIL(-1.98) | -1.982 | 6365 | -10.67 | -38.09 |  |
| 5m|ema13 | FAIL(-5.35) | -99.99 | 18.68 | -5.353 | 8.0 | 3056 | FAIL(-2.00) | -2.004 | 12649 | -20.75 | -61.75 |  |

### cyber-cycle-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 1d|a0.07 | FAIL(-0.72) | -11.77 | 16.27 | -0.723 | 22.7 | 22 | FAIL(-0.87) | -0.868 | 79 | -0.23 | -1.04 |  |
| 12h|a0.07 | FAIL(-0.06) | -1.06 | 18.56 | -0.057 | 25.0 | 36 | FAIL(0.81) | 0.808 | 139 | 0.05 | 1.07 |  |
| 9h|a0.07 | FAIL(0.45) | 9.35 | 20.75 | 0.450 | 38.3 | 47 | FAIL(0.41) | 0.406 | 190 | 0.30 | 0.65 |  |
| 7h|a0.07 | FAIL(0.15) | 3.05 | 20.74 | 0.147 | 47.5 | 61 | FAIL(-0.62) | -0.624 | 248 | 0.12 | -0.67 |  |
| 6h|a0.07 | FAIL(0.04) | 0.85 | 20.90 | 0.041 | 45.8 | 72 | FAIL(-1.01) | -1.015 | 298 | 0.07 | -1.40 |  |
| 5h|a0.07 | FAIL(-0.08) | -1.55 | 20.35 | -0.076 | 39.5 | 81 | FAIL(-0.99) | -0.990 | 350 | 0.02 | -1.38 |  |
| 4h|a0.07 | FAIL(-1.28) | -26.36 | 20.65 | -1.276 | 35.1 | 111 | FAIL(-1.28) | -1.284 | 447 | -0.71 | -2.14 |  |
| 3h|a0.07 | FAIL(-1.41) | -26.30 | 18.62 | -1.412 | 34.9 | 149 | FAIL(-1.75) | -1.749 | 610 | -0.72 | -4.21 |  |
| 2h|a0.07 | FAIL(-2.20) | -40.56 | 18.45 | -2.199 | 31.8 | 223 | FAIL(-1.94) | -1.942 | 898 | -1.25 | -6.15 |  |
| 1h|a0.07 | FAIL(-4.14) | -79.69 | 19.24 | -4.141 | 23.3 | 473 | FAIL(-2.07) | -2.065 | 1830 | -3.87 | -11.98 |  |
| 2d|a0.07 | PASS(1.55) | 20.68 | 13.36 | 1.548 | 66.7 | 6 | FAIL(-0.13) | -0.128 | 33 | 0.51 | 0.10 |  |
| 90m|a0.07 | FAIL(-3.48) | -65.02 | 18.69 | -3.479 | 26.3 | 308 | FAIL(-2.00) | -2.000 | 1195 | -2.55 | -7.72 |  |
| 30m|a0.07 | FAIL(-4.90) | -93.25 | 19.02 | -4.903 | 19.2 | 932 | FAIL(-2.04) | -2.037 | 3686 | -6.52 | -23.09 |  |
| 15m|a0.07 | FAIL(-5.31) | -99.49 | 18.72 | -5.315 | 15.2 | 1810 | FAIL(-1.98) | -1.979 | 7380 | -12.29 | -42.31 |  |
| 10m|a0.07 | FAIL(-5.36) | -99.98 | 18.66 | -5.359 | 12.5 | 2770 | FAIL(-1.98) | -1.982 | 11211 | -18.71 | -57.56 |  |
| 5m|a0.07 | FAIL(-5.35) | -100.00 | 18.68 | -5.353 | 8.7 | 5483 | FAIL(-2.00) | -2.004 | 22370 | -33.67 | -81.47 |  |

### williams-fractals-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 4h|w2 | FAIL(-0.26) | -5.32 | 20.65 | -0.258 | 35.7 | 28 | FAIL(0.43) | 0.430 | 95 | -0.07 | 0.79 |  |
| 3h|w2 | FAIL(-0.16) | -2.91 | 18.62 | -0.156 | 30.8 | 39 | FAIL(0.12) | 0.121 | 130 | -0.01 | 0.39 |  |
| 2h|w2 | FAIL(-0.96) | -17.71 | 18.45 | -0.960 | 31.0 | 58 | FAIL(-0.34) | -0.339 | 200 | -0.42 | -0.18 |  |
| 1h|w2 | FAIL(-0.87) | -16.81 | 19.24 | -0.873 | 32.0 | 100 | FAIL(-1.12) | -1.125 | 414 | -0.39 | -1.72 |  |
| 90m|w2 | FAIL(-0.94) | -17.58 | 18.69 | -0.941 | 33.3 | 78 | FAIL(-1.11) | -1.108 | 291 | -0.43 | -1.68 |  |
| 1d|w2 | PASS(1.62) | 26.36 | 16.27 | 1.620 | 66.7 | 3 | FAIL(0.92) | 0.918 | 15 | 0.65 | 1.29 |  |
| 12h|w2 | FAIL(0.90) | 16.66 | 18.56 | 0.898 | 37.5 | 8 | FAIL(1.05) | 1.054 | 29 | 0.42 | 1.26 |  |
| 2d|w2 | PASS(1.68) | 22.50 | 13.36 | 1.685 | 100.0 | 1 | PASS(1.37) | 1.373 | 8 | 0.56 | 1.44 |  |
| 9h|w2 | FAIL(1.03) | 21.40 | 20.75 | 1.031 | 50.0 | 8 | FAIL(0.34) | 0.344 | 44 | 0.55 | 0.71 |  |
| 7h|w2 | FAIL(1.15) | 23.87 | 20.74 | 1.151 | 50.0 | 12 | FAIL(-0.20) | -0.200 | 60 | 0.62 | 0.05 |  |
| 6h|w2 | FAIL(0.39) | 8.25 | 20.90 | 0.395 | 36.8 | 19 | FAIL(-0.01) | -0.008 | 72 | 0.27 | 0.32 |  |
| 5h|w2 | FAIL(-0.04) | -0.89 | 20.35 | -0.044 | 40.9 | 22 | FAIL(-0.42) | -0.415 | 88 | 0.04 | -0.27 |  |
| 30m|w2 | FAIL(-2.87) | -54.55 | 19.02 | -2.869 | 24.8 | 210 | FAIL(-1.84) | -1.844 | 839 | -1.91 | -5.52 |  |
| 15m|w2 | FAIL(-4.25) | -79.59 | 18.72 | -4.252 | 19.3 | 441 | FAIL(-1.97) | -1.971 | 1743 | -3.85 | -12.73 |  |
| 10m|w2 | FAIL(-4.63) | -86.33 | 18.66 | -4.627 | 19.5 | 637 | FAIL(-1.98) | -1.981 | 2579 | -4.81 | -18.07 |  |
| 5m|w2 | FAIL(-5.25) | -98.09 | 18.68 | -5.251 | 15.6 | 1286 | FAIL(-2.00) | -2.004 | 5210 | -9.38 | -33.47 |  |

## Caveats

- LEAD = 6m Mode-A sizing only. full(~2y) context only.
- No param retune on 6m after freeze. Scout-wave-3 Part A seats.
- Hold prior PRs #15–#25 unmerged; this PR is additive fresh-wave-v8 only.
- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only.
- Watchlist (no paper): ema-rsi@9h, schaff@2d.
- v7 Elder Impulse OOS hard-stop — do not revive without Strategy OK.
- Parked (not this freeze): camarilla, funding-fade, mesa-sine, Qstick/VWAP/SMI/ASI/EMV.

## IDs frozen: gann-hilo-activator-v1, asian-london-break-v1, force-index-13-v1, cyber-cycle-v1, williams-fractals-v1

