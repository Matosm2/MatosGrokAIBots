# owned-tf-sweep-v1 scoreboard

Generated (UTC): 2026-09-06T00:10:25.942716+00:00

Gate: 6m Mode-A ≥ 1.2× B&H (dual-mom vs 50/50 BTC+ETH).
Symbol: BTCUSDT (ETH only for dual-mom cells). Hold #14 BB params.
Agg: 5m/1d native cache; UTC bucket aggregate; #12 no-lookahead HTF join.

## M2/M4 HTF map (frozen)

| LTF | HTF |
|-----|-----|
| 5m | 1h |
| 10m | 1h |
| 15m | 1h |
| 30m | 4h |
| 90m | 4h |
| 1h | 4h |
| 2h | 4h |
| 3h | 4h |
| 4h | 1d |
| 5h | 1d |
| 6h | 1d |
| 7h | 1d |
| 9h | 2d |
| 12h | 2d |
| 1d | 2d |
| 2d | 1w |

## Scoreboard (PASS/FAIL)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ema-rsi-trend-v1.1 | FAIL(-4.56) | FAIL(-3.21) | FAIL(-1.92) | FAIL(-0.04) | FAIL(0.66) | FAIL(0.01) | FAIL(0.75) | FAIL(0.35) | FAIL(0.65) | FAIL(1.08) | PASS(1.71) | FAIL(1.07) | PASS(1.21) | FAIL(0.66) | FAIL(0.39) | FAIL(-0.59) |
| openproxy-M1 | FAIL(-5.57) | FAIL(-5.05) | FAIL(-4.40) | FAIL(-3.06) | FAIL(-0.97) | FAIL(-1.83) | FAIL(-0.67) | FAIL(-0.44) | FAIL(-0.09) | FAIL(0.11) | FAIL(0.80) | FAIL(0.73) | FAIL(1.14) | PASS(1.24) | FAIL(0.03) | FAIL(0.67) |
| openproxy-M2 | FAIL(-1.16) | FAIL(-0.78) | FAIL(-0.76) | FAIL(-0.19) | FAIL(-0.63) | FAIL(-0.08) | FAIL(-0.48) | FAIL(-0.60) | FAIL(-0.34) | FAIL(-0.48) | FAIL(-0.19) | FAIL(-0.28) | FAIL(0.12) | FAIL(0.43) | FAIL(0.34) | FAIL(0.00) |
| openproxy-M3 | FAIL(-5.41) | FAIL(-4.49) | FAIL(-3.86) | FAIL(-2.29) | FAIL(-0.76) | FAIL(-0.80) | FAIL(-0.72) | FAIL(-0.01) | FAIL(0.77) | FAIL(0.66) | FAIL(0.61) | FAIL(0.57) | FAIL(0.50) | FAIL(0.55) | FAIL(0.46) | FAIL(0.30) |
| openproxy-M4 | FAIL(-0.49) | FAIL(-1.14) | FAIL(-1.33) | FAIL(0.69) | FAIL(0.42) | FAIL(0.46) | FAIL(1.02) | FAIL(0.98) | FAIL(0.26) | FAIL(0.35) | FAIL(0.16) | FAIL(0.04) | FAIL(-0.07) | FAIL(-0.34) | FAIL(0.00) | FAIL(0.00) |
| bb-squeeze-breakout-v1 | FAIL(-3.90) | FAIL(-2.65) | FAIL(-1.82) | FAIL(-0.74) | FAIL(-0.73) | FAIL(-0.78) | FAIL(-0.62) | FAIL(-0.14) | FAIL(0.23) | FAIL(0.64) | FAIL(0.85) | FAIL(1.04) | FAIL(1.01) | FAIL(0.46) | FAIL(0.36) | FAIL(0.54) |
| kama-er-trend-v1 | FAIL(-5.68) | FAIL(-5.63) | FAIL(-5.43) | FAIL(-4.68) | FAIL(-1.68) | FAIL(-2.60) | FAIL(-1.22) | FAIL(-1.51) | FAIL(-1.41) | FAIL(-0.54) | FAIL(-0.90) | FAIL(-0.88) | FAIL(0.68) | FAIL(0.86) | FAIL(-0.14) | FAIL(0.33) |
| dual-mom-btc-eth-v1 | FAIL(-4.70) | FAIL(-4.68) | FAIL(-4.68) | FAIL(-4.36) | FAIL(-2.85) | FAIL(-2.90) | FAIL(-2.02) | FAIL(-1.32) | FAIL(-1.45) | FAIL(-1.55) | FAIL(-0.68) | FAIL(0.60) | FAIL(0.95) | FAIL(0.73) | FAIL(1.02) | FAIL(0.47) |
| sma200-trend-v1 | FAIL(-5.29) | FAIL(-4.23) | FAIL(-3.34) | FAIL(-1.36) | FAIL(0.27) | FAIL(0.12) | FAIL(0.42) | FAIL(1.13) | FAIL(0.75) | FAIL(0.19) | FAIL(0.74) | FAIL(0.61) | PASS(1.25) | FAIL(0.43) | FAIL(0.71) | FAIL(0.00) |
| supertrend-atr-v1 | FAIL(-5.22) | FAIL(-3.72) | FAIL(-2.93) | FAIL(-0.47) | FAIL(-0.13) | FAIL(-0.60) | FAIL(0.49) | FAIL(-0.51) | FAIL(0.29) | FAIL(0.63) | FAIL(0.32) | FAIL(1.03) | FAIL(1.05) | FAIL(1.15) | FAIL(1.00) | FAIL(-0.08) |

## PASS cells

- `ema-rsi-trend-v1.1` @ `6h`: ret=30.39% bh=17.77% ratio=1.710 trades=4
- `ema-rsi-trend-v1.1` @ `9h`: ret=22.39% bh=18.55% ratio=1.207 trades=5
- `sma200-trend-v1` @ `9h`: ret=23.27% bh=18.55% ratio=1.255 trades=7
- `openproxy-M1` @ `12h`: ret=23.17% bh=18.69% ratio=1.240 trades=7

## Cell detail

| strategy | tf | gate | modeA% | bh% | ratio | trades | error |
|----------|----|------|--------|-----|-------|--------|-------|
| ema-rsi-trend-v1.1 | 1h | FAIL | 0.22 | 17.61 | 0.012 | 37 |  |
| openproxy-M1 | 1h | FAIL | -32.26 | 17.61 | -1.832 | 118 |  |
| openproxy-M2 | 1h | FAIL | -1.33 | 17.61 | -0.075 | 22 |  |
| openproxy-M3 | 1h | FAIL | -14.03 | 17.61 | -0.797 | 81 |  |
| openproxy-M4 | 1h | FAIL | 8.13 | 17.61 | 0.462 | 15 |  |
| bb-squeeze-breakout-v1 | 1h | FAIL | -13.82 | 17.61 | -0.785 | 45 |  |
| kama-er-trend-v1 | 1h | FAIL | -45.81 | 17.61 | -2.602 | 246 |  |
| dual-mom-btc-eth-v1 | 1h | FAIL | -61.83 | 21.30 | -2.903 | 426 |  |
| sma200-trend-v1 | 1h | FAIL | 2.14 | 17.61 | 0.121 | 64 |  |
| supertrend-atr-v1 | 1h | FAIL | -10.57 | 17.61 | -0.600 | 54 |  |
| ema-rsi-trend-v1.1 | 4h | FAIL | 11.50 | 17.61 | 0.653 | 10 |  |
| openproxy-M1 | 4h | FAIL | -1.63 | 17.61 | -0.093 | 35 |  |
| openproxy-M2 | 4h | FAIL | -5.93 | 17.61 | -0.337 | 3 |  |
| openproxy-M3 | 4h | FAIL | 13.53 | 17.61 | 0.768 | 17 |  |
| openproxy-M4 | 4h | FAIL | 4.54 | 17.61 | 0.258 | 2 |  |
| bb-squeeze-breakout-v1 | 4h | FAIL | 4.10 | 17.61 | 0.233 | 14 |  |
| kama-er-trend-v1 | 4h | FAIL | -24.86 | 17.61 | -1.412 | 71 |  |
| dual-mom-btc-eth-v1 | 4h | FAIL | -30.96 | 21.41 | -1.446 | 125 |  |
| sma200-trend-v1 | 4h | FAIL | 13.15 | 17.61 | 0.747 | 19 |  |
| supertrend-atr-v1 | 4h | FAIL | 5.14 | 17.61 | 0.292 | 14 |  |
| ema-rsi-trend-v1.1 | 1d | FAIL | 8.21 | 21.09 | 0.389 | 2 |  |
| openproxy-M1 | 1d | FAIL | 0.60 | 21.09 | 0.028 | 4 |  |
| openproxy-M2 | 1d | FAIL | 7.19 | 21.09 | 0.341 | 2 |  |
| openproxy-M3 | 1d | FAIL | 9.73 | 21.09 | 0.461 | 4 |  |
| openproxy-M4 | 1d | FAIL | 0.00 | 21.09 | 0.000 | 0 |  |
| bb-squeeze-breakout-v1 | 1d | FAIL | 7.60 | 21.09 | 0.360 | 3 |  |
| kama-er-trend-v1 | 1d | FAIL | -2.97 | 21.09 | -0.141 | 11 |  |
| dual-mom-btc-eth-v1 | 1d | FAIL | 25.13 | 24.57 | 1.023 | 13 |  |
| sma200-trend-v1 | 1d | FAIL | 14.87 | 21.09 | 0.705 | 1 |  |
| supertrend-atr-v1 | 1d | FAIL | 21.10 | 21.09 | 1.001 | 2 |  |
| ema-rsi-trend-v1.1 | 2d | FAIL | -9.77 | 16.64 | -0.587 | 2 |  |
| openproxy-M1 | 2d | FAIL | 11.14 | 16.64 | 0.669 | 3 |  |
| openproxy-M2 | 2d | FAIL | 0.00 | 16.64 | 0.000 | 0 |  |
| openproxy-M3 | 2d | FAIL | 4.98 | 16.64 | 0.299 | 2 |  |
| openproxy-M4 | 2d | FAIL | 0.00 | 16.64 | 0.000 | 0 |  |
| bb-squeeze-breakout-v1 | 2d | FAIL | 8.98 | 16.64 | 0.539 | 1 |  |
| kama-er-trend-v1 | 2d | FAIL | 5.47 | 16.64 | 0.329 | 6 |  |
| dual-mom-btc-eth-v1 | 2d | FAIL | 9.23 | 19.83 | 0.465 | 5 |  |
| sma200-trend-v1 | 2d | FAIL | 0.00 | 16.64 | 0.000 | 0 |  |
| supertrend-atr-v1 | 2d | FAIL | -1.36 | 16.64 | -0.082 | 2 |  |
| ema-rsi-trend-v1.1 | 15m | FAIL | -33.57 | 17.47 | -1.921 | 154 |  |
| openproxy-M1 | 15m | FAIL | -76.80 | 17.47 | -4.396 | 428 |  |
| openproxy-M2 | 15m | FAIL | -13.23 | 17.47 | -0.757 | 64 |  |
| openproxy-M3 | 15m | FAIL | -67.49 | 17.47 | -3.863 | 344 |  |
| openproxy-M4 | 15m | FAIL | -23.25 | 17.47 | -1.331 | 65 |  |
| bb-squeeze-breakout-v1 | 15m | FAIL | -31.83 | 17.47 | -1.822 | 139 |  |
| kama-er-trend-v1 | 15m | FAIL | -94.89 | 17.47 | -5.431 | 985 |  |
| dual-mom-btc-eth-v1 | 15m | FAIL | -99.52 | 21.25 | -4.683 | 1895 |  |
| sma200-trend-v1 | 15m | FAIL | -58.37 | 17.47 | -3.341 | 307 |  |
| supertrend-atr-v1 | 15m | FAIL | -51.17 | 17.47 | -2.929 | 225 |  |
| ema-rsi-trend-v1.1 | 30m | FAIL | -0.75 | 17.40 | -0.043 | 82 |  |
| openproxy-M1 | 30m | FAIL | -53.23 | 17.40 | -3.060 | 214 |  |
| openproxy-M2 | 30m | FAIL | -3.36 | 17.40 | -0.193 | 21 |  |
| openproxy-M3 | 30m | FAIL | -39.85 | 17.40 | -2.290 | 171 |  |
| openproxy-M4 | 30m | FAIL | 11.92 | 17.40 | 0.685 | 15 |  |
| bb-squeeze-breakout-v1 | 30m | FAIL | -12.83 | 17.40 | -0.737 | 79 |  |
| kama-er-trend-v1 | 30m | FAIL | -81.36 | 17.40 | -4.676 | 501 |  |
| dual-mom-btc-eth-v1 | 30m | FAIL | -92.21 | 21.13 | -4.363 | 896 |  |
| sma200-trend-v1 | 30m | FAIL | -23.67 | 17.40 | -1.361 | 135 |  |
| supertrend-atr-v1 | 30m | FAIL | -8.19 | 17.40 | -0.471 | 100 |  |
| ema-rsi-trend-v1.1 | 5m | FAIL | -80.20 | 17.60 | -4.556 | 506 |  |
| openproxy-M1 | 5m | FAIL | -98.00 | 17.60 | -5.568 | 1283 |  |
| openproxy-M2 | 5m | FAIL | -20.49 | 17.60 | -1.164 | 84 |  |
| openproxy-M3 | 5m | FAIL | -95.30 | 17.60 | -5.415 | 1017 |  |
| openproxy-M4 | 5m | FAIL | -8.62 | 17.60 | -0.490 | 65 |  |
| bb-squeeze-breakout-v1 | 5m | FAIL | -68.72 | 17.60 | -3.904 | 396 |  |
| kama-er-trend-v1 | 5m | FAIL | -99.99 | 17.60 | -5.681 | 2970 |  |
| dual-mom-btc-eth-v1 | 5m | FAIL | -99.85 | 21.26 | -4.696 | 5649 |  |
| sma200-trend-v1 | 5m | FAIL | -93.12 | 17.60 | -5.291 | 916 |  |
| supertrend-atr-v1 | 5m | FAIL | -91.86 | 17.60 | -5.219 | 812 |  |
| ema-rsi-trend-v1.1 | 10m | FAIL | -56.35 | 17.58 | -3.205 | 247 |  |
| openproxy-M1 | 10m | FAIL | -88.76 | 17.58 | -5.049 | 649 |  |
| openproxy-M2 | 10m | FAIL | -13.78 | 17.58 | -0.784 | 67 |  |
| openproxy-M3 | 10m | FAIL | -79.00 | 17.58 | -4.494 | 507 |  |
| openproxy-M4 | 10m | FAIL | -20.07 | 17.58 | -1.142 | 64 |  |
| bb-squeeze-breakout-v1 | 10m | FAIL | -46.67 | 17.58 | -2.655 | 207 |  |
| kama-er-trend-v1 | 10m | FAIL | -98.90 | 17.58 | -5.626 | 1467 |  |
| dual-mom-btc-eth-v1 | 10m | FAIL | -99.83 | 21.32 | -4.683 | 2805 |  |
| sma200-trend-v1 | 10m | FAIL | -74.42 | 17.58 | -4.233 | 476 |  |
| supertrend-atr-v1 | 10m | FAIL | -65.32 | 17.58 | -3.715 | 360 |  |
| ema-rsi-trend-v1.1 | 90m | FAIL | 11.44 | 17.38 | 0.658 | 27 |  |
| openproxy-M1 | 90m | FAIL | -16.80 | 17.38 | -0.967 | 77 |  |
| openproxy-M2 | 90m | FAIL | -10.93 | 17.38 | -0.629 | 15 |  |
| openproxy-M3 | 90m | FAIL | -13.17 | 17.38 | -0.758 | 64 |  |
| openproxy-M4 | 90m | FAIL | 7.26 | 17.38 | 0.418 | 14 |  |
| bb-squeeze-breakout-v1 | 90m | FAIL | -12.77 | 17.38 | -0.735 | 31 |  |
| kama-er-trend-v1 | 90m | FAIL | -29.17 | 17.38 | -1.678 | 165 |  |
| dual-mom-btc-eth-v1 | 90m | FAIL | -60.02 | 21.05 | -2.852 | 311 |  |
| sma200-trend-v1 | 90m | FAIL | 4.78 | 17.38 | 0.275 | 40 |  |
| supertrend-atr-v1 | 90m | FAIL | -2.22 | 17.38 | -0.128 | 38 |  |
| ema-rsi-trend-v1.1 | 2h | FAIL | 13.09 | 17.38 | 0.753 | 23 |  |
| openproxy-M1 | 2h | FAIL | -11.59 | 17.38 | -0.667 | 64 |  |
| openproxy-M2 | 2h | FAIL | -8.33 | 17.38 | -0.479 | 17 |  |
| openproxy-M3 | 2h | FAIL | -12.58 | 17.38 | -0.724 | 48 |  |
| openproxy-M4 | 2h | FAIL | 17.79 | 17.38 | 1.023 | 13 |  |
| bb-squeeze-breakout-v1 | 2h | FAIL | -10.72 | 17.38 | -0.617 | 25 |  |
| kama-er-trend-v1 | 2h | FAIL | -21.19 | 17.38 | -1.219 | 120 |  |
| dual-mom-btc-eth-v1 | 2h | FAIL | -42.56 | 21.05 | -2.022 | 237 |  |
| sma200-trend-v1 | 2h | FAIL | 7.31 | 17.38 | 0.420 | 40 |  |
| supertrend-atr-v1 | 2h | FAIL | 8.51 | 17.38 | 0.490 | 26 |  |
| ema-rsi-trend-v1.1 | 3h | FAIL | 6.07 | 17.37 | 0.349 | 13 |  |
| openproxy-M1 | 3h | FAIL | -7.66 | 17.37 | -0.441 | 37 |  |
| openproxy-M2 | 3h | FAIL | -10.47 | 17.37 | -0.603 | 8 |  |
| openproxy-M3 | 3h | FAIL | -0.18 | 17.37 | -0.010 | 30 |  |
| openproxy-M4 | 3h | FAIL | 17.06 | 17.37 | 0.982 | 12 |  |
| bb-squeeze-breakout-v1 | 3h | FAIL | -2.38 | 17.37 | -0.137 | 20 |  |
| kama-er-trend-v1 | 3h | FAIL | -26.27 | 17.37 | -1.512 | 93 |  |
| dual-mom-btc-eth-v1 | 3h | FAIL | -27.89 | 21.10 | -1.322 | 158 |  |
| sma200-trend-v1 | 3h | FAIL | 19.60 | 17.37 | 1.129 | 18 |  |
| supertrend-atr-v1 | 3h | FAIL | -8.86 | 17.37 | -0.510 | 21 |  |
| ema-rsi-trend-v1.1 | 5h | FAIL | 19.37 | 18.01 | 1.075 | 6 |  |
| openproxy-M1 | 5h | FAIL | 1.95 | 18.01 | 0.108 | 21 |  |
| openproxy-M2 | 5h | FAIL | -8.56 | 18.01 | -0.475 | 3 |  |
| openproxy-M3 | 5h | FAIL | 11.93 | 18.01 | 0.662 | 16 |  |
| openproxy-M4 | 5h | FAIL | 6.30 | 18.01 | 0.350 | 2 |  |
| bb-squeeze-breakout-v1 | 5h | FAIL | 11.55 | 18.01 | 0.641 | 10 |  |
| kama-er-trend-v1 | 5h | FAIL | -9.72 | 18.01 | -0.540 | 60 |  |
| dual-mom-btc-eth-v1 | 5h | FAIL | -33.91 | 21.85 | -1.552 | 101 |  |
| sma200-trend-v1 | 5h | FAIL | 3.50 | 18.01 | 0.194 | 17 |  |
| supertrend-atr-v1 | 5h | FAIL | 11.39 | 18.01 | 0.632 | 11 |  |
| ema-rsi-trend-v1.1 | 6h | PASS | 30.39 | 17.77 | 1.710 | 4 |  |
| openproxy-M1 | 6h | FAIL | 14.13 | 17.77 | 0.795 | 18 |  |
| openproxy-M2 | 6h | FAIL | -3.37 | 17.77 | -0.190 | 3 |  |
| openproxy-M3 | 6h | FAIL | 10.75 | 17.77 | 0.605 | 14 |  |
| openproxy-M4 | 6h | FAIL | 2.83 | 17.77 | 0.159 | 2 |  |
| bb-squeeze-breakout-v1 | 6h | FAIL | 15.16 | 17.77 | 0.853 | 8 |  |
| kama-er-trend-v1 | 6h | FAIL | -16.02 | 17.77 | -0.902 | 55 |  |
| dual-mom-btc-eth-v1 | 6h | FAIL | -14.70 | 21.59 | -0.681 | 85 |  |
| sma200-trend-v1 | 6h | FAIL | 13.19 | 17.77 | 0.742 | 14 |  |
| supertrend-atr-v1 | 6h | FAIL | 5.66 | 17.77 | 0.319 | 10 |  |
| ema-rsi-trend-v1.1 | 7h | FAIL | 19.69 | 18.46 | 1.067 | 6 |  |
| openproxy-M1 | 7h | FAIL | 13.49 | 18.46 | 0.731 | 12 |  |
| openproxy-M2 | 7h | FAIL | -5.25 | 18.46 | -0.284 | 3 |  |
| openproxy-M3 | 7h | FAIL | 10.49 | 18.46 | 0.568 | 13 |  |
| openproxy-M4 | 7h | FAIL | 0.71 | 18.46 | 0.039 | 3 |  |
| bb-squeeze-breakout-v1 | 7h | FAIL | 19.28 | 18.46 | 1.045 | 6 |  |
| kama-er-trend-v1 | 7h | FAIL | -16.19 | 18.46 | -0.877 | 44 |  |
| dual-mom-btc-eth-v1 | 7h | FAIL | 13.32 | 22.39 | 0.595 | 65 |  |
| sma200-trend-v1 | 7h | FAIL | 11.31 | 18.46 | 0.612 | 14 |  |
| supertrend-atr-v1 | 7h | FAIL | 18.96 | 18.46 | 1.027 | 7 |  |
| ema-rsi-trend-v1.1 | 9h | PASS | 22.39 | 18.55 | 1.207 | 5 |  |
| openproxy-M1 | 9h | FAIL | 21.18 | 18.55 | 1.142 | 10 |  |
| openproxy-M2 | 9h | FAIL | 2.17 | 18.55 | 0.117 | 1 |  |
| openproxy-M3 | 9h | FAIL | 9.19 | 18.55 | 0.496 | 11 |  |
| openproxy-M4 | 9h | FAIL | -1.22 | 18.55 | -0.066 | 2 |  |
| bb-squeeze-breakout-v1 | 9h | FAIL | 18.67 | 18.55 | 1.007 | 4 |  |
| kama-er-trend-v1 | 9h | FAIL | 12.63 | 18.55 | 0.681 | 27 |  |
| dual-mom-btc-eth-v1 | 9h | FAIL | 21.14 | 22.17 | 0.954 | 47 |  |
| sma200-trend-v1 | 9h | PASS | 23.27 | 18.55 | 1.255 | 7 |  |
| supertrend-atr-v1 | 9h | FAIL | 19.41 | 18.55 | 1.046 | 5 |  |
| ema-rsi-trend-v1.1 | 12h | FAIL | 12.39 | 18.69 | 0.663 | 5 |  |
| openproxy-M1 | 12h | PASS | 23.17 | 18.69 | 1.240 | 7 |  |
| openproxy-M2 | 12h | FAIL | 8.11 | 18.69 | 0.434 | 1 |  |
| openproxy-M3 | 12h | FAIL | 10.27 | 18.69 | 0.550 | 7 |  |
| openproxy-M4 | 12h | FAIL | -6.26 | 18.69 | -0.335 | 2 |  |
| bb-squeeze-breakout-v1 | 12h | FAIL | 8.68 | 18.69 | 0.464 | 6 |  |
| kama-er-trend-v1 | 12h | FAIL | 16.08 | 18.69 | 0.860 | 18 |  |
| dual-mom-btc-eth-v1 | 12h | FAIL | 16.37 | 22.31 | 0.734 | 32 |  |
| sma200-trend-v1 | 12h | FAIL | 8.01 | 18.69 | 0.429 | 3 |  |
| supertrend-atr-v1 | 12h | FAIL | 21.42 | 18.69 | 1.146 | 3 |  |
