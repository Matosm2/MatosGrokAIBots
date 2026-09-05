# Offline backtest: donchian-20-10-spot-v1

_Generated: 2026-09-05 02:59 UTC_

**RESEARCH ONLY — not enabled for paper/live.**

## Rules

- Timeframe: **Daily**
- Entry: close > highest high of the **prior 20 bars** (excluding current) — classic Donchian upper-band breakout
- Exit: close < lowest low of the **prior 10 bars** (excluding current)
- Spot long-only; pyramiding 0

## Common costs / sizing

| Parameter | Value |
|-----------|-------|
| Fee | 0.10% / side |
| Slippage | 5 bps adverse vs close |
| Size Mode A (**gate**) | **100% equity when in** (PASS/FAIL uses this only) |
| Size Mode B (**ops**) | **2.5% equity** (Balanced realism; report only) |
| Close | full position |
| Mode | spot long-only, bar-close, no lookahead |

## Gate table (mandatory 6m) — both sizing modes

PASS only if **n>0** AND **WR ≥ 60%** AND **strategy return > buy&hold** on **Mode A (100%-when-in)**. Mode B is ops realism only (PASS/FAIL = —).

| Strategy | Symbol | Mode | Size | 6m WR | 6m return | 6m B&H | PASS/FAIL |
|----------|--------|------|------|-------|-----------|--------|-----------|
| donchian-20-10-spot-v1 | BTCUSDT | A (gate) | 100% | 50.00% | +15.53% | +18.29% | **FAIL** |
| donchian-20-10-spot-v1 | BTCUSDT | B (ops) | 2.5% | 50.00% | +0.43% | +18.29% | — |
| donchian-20-10-spot-v1 | ETHUSDT | A (gate) | 100% | 0.00% | -13.40% | +24.49% | **FAIL** |
| donchian-20-10-spot-v1 | ETHUSDT | B (ops) | 2.5% | 0.00% | -0.32% | +24.49% | — |

## Window: 6m

### BTCUSDT (6m) — A (gate) 100%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 2 |
| Wins / Losses | 1 / 1 |
| Win rate | 50.00% |
| Strategy return | +15.53% |
| Buy & hold | +18.29% |
| Max drawdown | 10.54% |
| Expectancy (USDT) | -270.4591 |
| Avg bars held | 19.5 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-03-16 00:00 | 2026-03-22 00:00 | 74922.1123 | 67825.0705 | -965.3434 | -9.65% | 6 | signal |
| 2 | 2026-04-13 00:00 | 2026-05-16 00:00 | 74455.1990 | 78108.9760 | 424.4251 | 4.70% | 33 | signal |

</details>

### BTCUSDT (6m) — B (ops) 2.5%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 2 |
| Wins / Losses | 1 / 1 |
| Win rate | 50.00% |
| Strategy return | +0.43% |
| Buy & hold | +18.29% |
| Max drawdown | 0.27% |
| Expectancy (USDT) | -6.2150 |
| Avg bars held | 19.5 |
| Gate | — (ops only; not scored) |

### ETHUSDT (6m) — A (gate) 100%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 3 |
| Wins / Losses | 0 / 3 |
| Win rate | 0.00% |
| Strategy return | -13.40% |
| Buy & hold | +24.49% |
| Max drawdown | 20.43% |
| Expectancy (USDT) | -677.0352 |
| Avg bars held | 21.0 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-03-16 00:00 | 2026-03-27 00:00 | 2354.1465 | 1991.7536 | -1556.2854 | -15.56% | 11 | signal |
| 2 | 2026-04-11 00:00 | 2026-05-15 00:00 | 2286.1325 | 2223.5477 | -247.5626 | -2.93% | 34 | signal |
| 3 | 2026-07-14 00:00 | 2026-08-01 00:00 | 1892.8159 | 1844.0175 | -227.2575 | -2.77% | 18 | signal |

</details>

### ETHUSDT (6m) — B (ops) 2.5%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 3 |
| Wins / Losses | 0 / 3 |
| Win rate | 0.00% |
| Strategy return | -0.32% |
| Buy & hold | +24.49% |
| Max drawdown | 0.54% |
| Expectancy (USDT) | -17.7204 |
| Avg bars held | 21.0 |
| Gate | — (ops only; not scored) |

## Window: 2y

### BTCUSDT (2y) — A (gate) 100%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 10 |
| Wins / Losses | 4 / 6 |
| Win rate | 40.00% |
| Strategy return | +37.93% |
| Buy & hold | +41.62% |
| Max drawdown | 38.33% |
| Expectancy (USDT) | 129.3387 |
| Avg bars held | 29.7 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-18 00:00 | 2024-10-01 00:00 | 61790.8700 | 60775.3771 | -183.9952 | -1.84% | 13 | signal |
| 2 | 2024-10-15 00:00 | 2025-02-02 00:00 | 67107.6771 | 97651.7397 | 4439.2161 | 45.22% | 110 | signal |
| 3 | 2025-04-22 00:00 | 2025-05-30 00:00 | 93489.7115 | 103933.4873 | 1560.7932 | 10.95% | 38 | signal |
| 4 | 2025-07-09 00:00 | 2025-08-01 00:00 | 111289.6070 | 113241.2810 | 245.2092 | 1.55% | 23 | signal |
| 5 | 2025-08-13 00:00 | 2025-08-19 00:00 | 123368.0832 | 112816.5035 | -1403.0501 | -8.74% | 6 | signal |
| 6 | 2025-09-16 00:00 | 2025-09-22 00:00 | 116847.3545 | 112594.6645 | -561.7092 | -3.83% | 6 | signal |
| 7 | 2025-10-01 00:00 | 2025-11-04 00:00 | 118654.2875 | 101446.4714 | -2068.4173 | -14.67% | 34 | signal |
| 8 | 2026-01-04 00:00 | 2026-01-20 00:00 | 91575.4949 | 88383.4462 | -442.4562 | -3.68% | 16 | signal |
| 9 | 2026-03-04 00:00 | 2026-03-22 00:00 | 72703.1034 | 67825.0705 | -798.9330 | -6.90% | 18 | signal |
| 10 | 2026-04-13 00:00 | 2026-05-16 00:00 | 74455.1990 | 78108.9760 | 506.7296 | 4.70% | 33 | signal |

</details>

### BTCUSDT (2y) — B (ops) 2.5%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 10 |
| Wins / Losses | 4 / 6 |
| Win rate | 40.00% |
| Strategy return | +1.12% |
| Buy & hold | +41.62% |
| Max drawdown | 1.17% |
| Expectancy (USDT) | 5.6333 |
| Avg bars held | 29.7 |
| Gate | — (ops only; not scored) |

### ETHUSDT (2y) — A (gate) 100%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 13 |
| Wins / Losses | 4 / 9 |
| Win rate | 30.77% |
| Strategy return | -35.21% |
| Buy & hold | +3.51% |
| Max drawdown | 56.45% |
| Expectancy (USDT) | -310.5964 |
| Avg bars held | 19.5 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-21 00:00 | 2024-10-01 00:00 | 2613.7062 | 2446.5661 | -658.1778 | -6.58% | 10 | signal |
| 2 | 2024-10-20 00:00 | 2024-10-25 00:00 | 2748.2835 | 2439.3997 | -1066.5088 | -11.42% | 5 | signal |
| 3 | 2024-11-07 00:00 | 2024-12-19 00:00 | 2896.9177 | 3415.3015 | 1461.3184 | 17.66% | 42 | signal |
| 4 | 2025-05-08 00:00 | 2025-06-05 00:00 | 2208.4937 | 2412.8030 | 879.4891 | 9.03% | 28 | signal |
| 5 | 2025-06-10 00:00 | 2025-06-20 00:00 | 2817.8082 | 2405.2868 | -1572.2845 | -14.81% | 10 | signal |
| 6 | 2025-07-09 00:00 | 2025-08-01 00:00 | 2770.1244 | 3486.4559 | 2315.9200 | 25.61% | 23 | signal |
| 7 | 2025-08-08 00:00 | 2025-09-22 00:00 | 4011.5047 | 4196.9805 | 501.4828 | 4.41% | 45 | signal |
| 8 | 2025-10-06 00:00 | 2025-10-10 00:00 | 4686.3520 | 3827.8051 | -2192.3543 | -18.48% | 4 | signal |
| 9 | 2025-12-09 00:00 | 2025-12-17 00:00 | 3319.6990 | 2832.0733 | -1436.7292 | -14.86% | 8 | signal |
| 10 | 2026-01-05 00:00 | 2026-01-20 00:00 | 3226.6025 | 2938.4101 | -750.2553 | -9.11% | 15 | signal |
| 11 | 2026-03-16 00:00 | 2026-03-27 00:00 | 2354.1465 | 1991.7536 | -1164.3973 | -15.56% | 11 | signal |
| 12 | 2026-04-11 00:00 | 2026-05-15 00:00 | 2286.1325 | 2223.5477 | -185.2239 | -2.93% | 34 | signal |
| 13 | 2026-07-14 00:00 | 2026-08-01 00:00 | 1892.8159 | 1844.0175 | -170.0318 | -2.77% | 18 | signal |

</details>

### ETHUSDT (2y) — B (ops) 2.5%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 13 |
| Wins / Losses | 4 / 9 |
| Win rate | 30.77% |
| Strategy return | -0.78% |
| Buy & hold | +3.51% |
| Max drawdown | 1.98% |
| Expectancy (USDT) | -7.6834 |
| Avg bars held | 19.5 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup indicators computed on longer history; entries only inside each window.
- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.
- Single-path sample; do not overfit to one bull/bear window.
- Gate PASS/FAIL is **only** on Mode A (100%-when-in); Mode B is ops parallel.
- Not related to Jewel Pine or ema-rsi paper webhook wiring.
- Does not change live/paper bot defaults.

