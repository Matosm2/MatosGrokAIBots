# Offline backtest: macd-hist-regime-v1

_Generated: 2026-09-05 02:56 UTC_

**RESEARCH ONLY — not enabled for paper/live.**

## Rules

- Timeframe: **Daily**
- Entry: MACD histogram crosses above 0 AND close > EMA100
- Exit: MACD histogram crosses below 0
- MACD(12,26,9); pyramiding 0

## Common costs / sizing

| Parameter | Value |
|-----------|-------|
| Fee | 0.10% / side |
| Slippage | 5 bps adverse vs close |
| Size | 2.5% equity |
| Close | full position |
| Mode | spot long-only, bar-close, no lookahead |

## Gate table (mandatory 6m)

PASS only if **WR ≥ 60%** AND **strategy return > buy&hold** (and ≥1 trade).

| Strategy | Symbol | 6m WR | 6m return | 6m B&H | PASS/FAIL |
|----------|--------|-------|-----------|--------|-----------|
| macd-hist-regime-v1 | BTCUSDT | 50.00% | -0.04% | +18.29% | **FAIL** |
| macd-hist-regime-v1 | ETHUSDT | 100.00% | +0.18% | +24.49% | **FAIL** |

## Window: 6m

### BTCUSDT (6m)

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 2 |
| Wins / Losses | 1 / 1 |
| Win rate | 50.00% |
| Strategy return | -0.04% |
| Buy & hold | +18.29% |
| Max drawdown | 0.11% |
| Expectancy (USDT) | -2.2156 |
| Avg bars held | 4.5 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-05-04 00:00 | 2026-05-12 00:00 | 79900.9405 | 80464.2178 | 1.2607 | 0.50% | 8 | signal |
| 2 | 2026-09-03 00:00 | 2026-09-04 00:00 | 81311.0052 | 79620.9396 | -5.6918 | -2.27% | 1 | signal |

</details>

### ETHUSDT (6m)

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 1 |
| Wins / Losses | 1 / 0 |
| Win rate | 100.00% |
| Strategy return | +0.18% |
| Buy & hold | +24.49% |
| Max drawdown | 0.11% |
| Expectancy (USDT) | 17.6096 |
| Avg bars held | 13.0 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-08-19 00:00 | 2026-09-01 00:00 | 2253.9264 | 2417.3607 | 17.6096 | 7.04% | 13 | signal |

</details>

## Window: 2y

### BTCUSDT (2y)

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 17 |
| Wins / Losses | 5 / 12 |
| Win rate | 29.41% |
| Strategy return | -0.33% |
| Buy & hold | +41.62% |
| Max drawdown | 1.07% |
| Expectancy (USDT) | -1.9387 |
| Avg bars held | 7.4 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-10-14 00:00 | 2024-10-26 00:00 | 66117.0320 | 67059.2136 | 3.0590 | 1.22% | 12 | signal |
| 2 | 2024-10-28 00:00 | 2024-11-03 00:00 | 69997.1911 | 68741.6020 | -4.9815 | -1.99% | 6 | signal |
| 3 | 2024-11-06 00:00 | 2024-11-26 00:00 | 75609.7760 | 91919.1774 | 53.3620 | 21.33% | 20 | signal |
| 4 | 2024-12-16 00:00 | 2024-12-18 00:00 | 106111.6893 | 100153.9080 | -14.5972 | -5.80% | 2 | signal |
| 5 | 2025-01-05 00:00 | 2025-01-09 00:00 | 98412.7918 | 92506.2138 | -15.5467 | -6.19% | 4 | signal |
| 6 | 2025-01-15 00:00 | 2025-01-28 00:00 | 100547.5987 | 101284.8522 | 1.3341 | 0.53% | 13 | signal |
| 7 | 2025-02-20 00:00 | 2025-02-24 00:00 | 98354.1525 | 91507.1036 | -17.9271 | -7.15% | 4 | signal |
| 8 | 2025-05-18 00:00 | 2025-05-19 00:00 | 106507.4871 | 105520.9531 | -2.8147 | -1.12% | 1 | signal |
| 10 | 2025-06-10 00:00 | 2025-06-12 00:00 | 110329.5272 | 105618.8941 | -11.1598 | -4.46% | 2 | signal |
| 11 | 2025-06-26 00:00 | 2025-07-21 00:00 | 107000.5335 | 117321.6698 | 23.5568 | 9.43% | 25 | signal |
| 12 | 2025-07-22 00:00 | 2025-07-23 00:00 | 120014.3972 | 118696.6120 | -3.2453 | -1.30% | 1 | signal |
| 13 | 2025-08-11 00:00 | 2025-08-17 00:00 | 118745.3430 | 117346.3075 | -3.4446 | -1.38% | 6 | signal |
| 14 | 2025-10-01 00:00 | 2025-10-10 00:00 | 118654.2875 | 112718.1128 | -12.9981 | -5.19% | 9 | signal |
| 15 | 2025-10-26 00:00 | 2025-11-03 00:00 | 114616.6797 | 106529.7485 | -18.1025 | -7.24% | 8 | signal |
| 16 | 2026-05-04 00:00 | 2026-05-12 00:00 | 79900.9405 | 80464.2178 | 1.2571 | 0.50% | 8 | signal |
| 17 | 2026-09-03 00:00 | 2026-09-04 00:00 | 81311.0052 | 79620.9396 | -5.6756 | -2.27% | 1 | signal |

</details>

### ETHUSDT (2y)

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 15 |
| Wins / Losses | 4 / 11 |
| Win rate | 26.67% |
| Strategy return | -0.43% |
| Buy & hold | +3.51% |
| Max drawdown | 1.46% |
| Expectancy (USDT) | -2.8378 |
| Avg bars held | 8.3 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-11-07 00:00 | 2024-11-20 00:00 | 2896.9177 | 3068.4350 | 14.2869 | 5.71% | 13 | signal |
| 2 | 2024-11-21 00:00 | 2024-12-10 00:00 | 3357.4879 | 3626.4359 | 19.5338 | 7.79% | 19 | signal |
| 3 | 2025-01-03 00:00 | 2025-01-09 00:00 | 3610.8145 | 3217.5904 | -27.7919 | -11.07% | 6 | signal |
| 4 | 2025-01-17 00:00 | 2025-01-19 00:00 | 3475.3668 | 3213.5124 | -19.3293 | -7.72% | 2 | signal |
| 5 | 2025-01-21 00:00 | 2025-01-27 00:00 | 3329.2038 | 3180.8488 | -11.6138 | -4.65% | 6 | signal |
| 6 | 2025-01-31 00:00 | 2025-02-01 00:00 | 3302.6405 | 3115.9812 | -14.5790 | -5.84% | 1 | signal |
| 7 | 2025-06-11 00:00 | 2025-06-12 00:00 | 2772.9958 | 2641.3287 | -12.3098 | -4.94% | 1 | signal |
| 8 | 2025-06-30 00:00 | 2025-07-01 00:00 | 2486.7127 | 2403.8075 | -8.7808 | -3.53% | 1 | signal |
| 9 | 2025-07-02 00:00 | 2025-07-30 00:00 | 2571.6952 | 3808.0950 | 118.8485 | 47.78% | 28 | signal |
| 10 | 2025-08-09 00:00 | 2025-08-19 00:00 | 4262.7503 | 4073.5522 | -11.6524 | -4.63% | 10 | signal |
| 11 | 2025-08-23 00:00 | 2025-08-25 00:00 | 4780.7892 | 4373.9919 | -21.8526 | -8.69% | 2 | signal |
| 12 | 2025-09-12 00:00 | 2025-09-19 00:00 | 4714.5161 | 4466.3557 | -13.6800 | -5.45% | 7 | signal |
| 13 | 2025-10-02 00:00 | 2025-10-10 00:00 | 4486.5922 | 3827.8051 | -37.2131 | -14.85% | 8 | signal |
| 14 | 2025-10-26 00:00 | 2025-11-03 00:00 | 4160.5392 | 3602.0281 | -33.9375 | -13.60% | 8 | signal |
| 15 | 2026-08-19 00:00 | 2026-09-01 00:00 | 2253.9264 | 2417.3607 | 17.5038 | 7.04% | 13 | signal |

</details>

## Caveats

- Warmup indicators computed on longer history; entries only inside each window.
- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.
- Single-path sample; do not overfit to one bull/bear window.
- Not related to Jewel Pine or ema-rsi paper webhook wiring.

