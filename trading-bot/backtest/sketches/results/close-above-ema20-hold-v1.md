# Offline backtest: close-above-ema20-hold-v1

_Generated: 2026-09-05 02:59 UTC_

**RESEARCH ONLY — not enabled for paper/live.**

## Rules

- Timeframe: **Daily**
- Entry: close > EMA20 AND EMA20 > EMA20[5] (rising EMA20)
- Exit: close < EMA20
- Optional ADX≥15 filter: **OFF by default**
- No EMA50>EMA200 filter
- State-based / hold while above; pyramiding 0

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
| close-above-ema20-hold-v1 | BTCUSDT | A (gate) | 100% | 12.50% | +10.28% | +18.29% | **FAIL** |
| close-above-ema20-hold-v1 | BTCUSDT | B (ops) | 2.5% | 12.50% | +0.28% | +18.29% | — |
| close-above-ema20-hold-v1 | ETHUSDT | A (gate) | 100% | 22.22% | +26.73% | +24.49% | **FAIL** |
| close-above-ema20-hold-v1 | ETHUSDT | B (ops) | 2.5% | 22.22% | +0.69% | +24.49% | — |

## Window: 6m

### BTCUSDT (6m) — A (gate) 100%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 8 |
| Wins / Losses | 1 / 7 |
| Win rate | 12.50% |
| Strategy return | +10.28% |
| Buy & hold | +18.29% |
| Max drawdown | 14.80% |
| Expectancy (USDT) | -46.9162 |
| Avg bars held | 8.5 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-03-12 00:00 | 2026-03-19 00:00 | 70576.6107 | 69895.0350 | -116.3595 | -1.16% | 7 | signal |
| 2 | 2026-04-07 00:00 | 2026-05-15 00:00 | 71960.1821 | 79073.6534 | 955.3267 | 9.67% | 38 | signal |
| 3 | 2026-07-06 00:00 | 2026-07-08 00:00 | 64074.0410 | 62258.8550 | -328.1054 | -3.03% | 2 | signal |
| 4 | 2026-07-09 00:00 | 2026-07-13 00:00 | 63261.6150 | 62303.3527 | -179.8970 | -1.71% | 4 | signal |
| 5 | 2026-07-14 00:00 | 2026-07-24 00:00 | 65076.5020 | 64107.9200 | -174.0975 | -1.69% | 10 | signal |
| 6 | 2026-07-25 00:00 | 2026-07-27 00:00 | 64407.1875 | 63723.9821 | -127.8181 | -1.26% | 2 | signal |
| 7 | 2026-07-30 00:00 | 2026-07-31 00:00 | 64812.4100 | 62856.4361 | -322.1000 | -3.21% | 1 | signal |
| 8 | 2026-08-06 00:00 | 2026-08-10 00:00 | 64355.7718 | 63938.0250 | -82.2785 | -0.85% | 4 | signal |

</details>

### BTCUSDT (6m) — B (ops) 2.5%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 8 |
| Wins / Losses | 1 / 7 |
| Win rate | 12.50% |
| Strategy return | +0.28% |
| Buy & hold | +18.29% |
| Max drawdown | 0.41% |
| Expectancy (USDT) | -1.0177 |
| Avg bars held | 8.5 |
| Gate | — (ops only; not scored) |

### ETHUSDT (6m) — A (gate) 100%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 9 |
| Wins / Losses | 2 / 7 |
| Win rate | 22.22% |
| Strategy return | +26.73% |
| Buy & hold | +24.49% |
| Max drawdown | 15.79% |
| Expectancy (USDT) | -10.4632 |
| Avg bars held | 8.4 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-03-13 00:00 | 2026-03-21 00:00 | 2093.2661 | 2083.8276 | -64.9800 | -0.65% | 8 | signal |
| 2 | 2026-03-23 00:00 | 2026-03-26 00:00 | 2153.1060 | 2059.3998 | -451.3725 | -4.54% | 3 | signal |
| 3 | 2026-04-05 00:00 | 2026-04-28 00:00 | 2111.2251 | 2288.2753 | 774.7742 | 8.17% | 23 | signal |
| 4 | 2026-05-03 00:00 | 2026-05-07 00:00 | 2323.8113 | 2289.9145 | -169.8344 | -1.66% | 4 | signal |
| 5 | 2026-05-08 00:00 | 2026-05-12 00:00 | 2308.2135 | 2273.8225 | -170.1706 | -1.69% | 4 | signal |
| 6 | 2026-07-04 00:00 | 2026-07-31 00:00 | 1781.5303 | 1861.6687 | 425.4506 | 4.29% | 27 | signal |
| 7 | 2026-08-02 00:00 | 2026-08-03 00:00 | 1886.3027 | 1859.5698 | -166.9688 | -1.61% | 1 | signal |
| 8 | 2026-08-05 00:00 | 2026-08-10 00:00 | 1909.8545 | 1872.2234 | -220.4545 | -2.17% | 5 | signal |
| 9 | 2026-08-13 00:00 | 2026-08-14 00:00 | 1887.0931 | 1881.2589 | -50.6130 | -0.51% | 1 | signal |

</details>

### ETHUSDT (6m) — B (ops) 2.5%

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 9 |
| Wins / Losses | 2 / 7 |
| Win rate | 22.22% |
| Strategy return | +0.69% |
| Buy & hold | +24.49% |
| Max drawdown | 0.44% |
| Expectancy (USDT) | -0.1056 |
| Avg bars held | 8.4 |
| Gate | — (ops only; not scored) |

## Window: 2y

### BTCUSDT (2y) — A (gate) 100%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 28 |
| Wins / Losses | 8 / 20 |
| Win rate | 28.57% |
| Strategy return | +40.87% |
| Buy & hold | +41.62% |
| Max drawdown | 27.92% |
| Expectancy (USDT) | 81.9438 |
| Avg bars held | 10.9 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-13 00:00 | 2024-09-16 00:00 | 60528.2490 | 58184.8830 | -406.3589 | -4.06% | 3 | signal |
| 2 | 2024-09-17 00:00 | 2024-10-01 00:00 | 60344.1470 | 60775.3771 | 49.2528 | 0.51% | 14 | signal |
| 3 | 2024-10-14 00:00 | 2024-11-04 00:00 | 66117.0320 | 67816.0850 | 228.0382 | 2.36% | 21 | signal |
| 4 | 2024-11-05 00:00 | 2024-12-19 00:00 | 69406.6960 | 97413.1291 | 3955.3590 | 40.07% | 44 | signal |
| 5 | 2025-01-05 00:00 | 2025-01-07 00:00 | 98412.7918 | 96906.1327 | -238.8768 | -1.73% | 2 | signal |
| 6 | 2025-01-16 00:00 | 2025-01-28 00:00 | 100037.2936 | 101284.8522 | 141.9615 | 1.04% | 12 | signal |
| 7 | 2025-01-29 00:00 | 2025-02-01 00:00 | 103785.1066 | 100585.3322 | -449.8728 | -3.28% | 3 | signal |
| 8 | 2025-03-25 00:00 | 2025-03-28 00:00 | 87436.5664 | 84382.1678 | -489.4950 | -3.69% | 3 | signal |
| 21 | 2026-03-12 00:00 | 2026-03-19 00:00 | 70576.6107 | 69895.0350 | -148.6361 | -1.16% | 7 | signal |
| 22 | 2026-04-07 00:00 | 2026-05-15 00:00 | 71960.1821 | 79073.6534 | 1220.3218 | 9.67% | 38 | signal |
| 23 | 2026-07-06 00:00 | 2026-07-08 00:00 | 64074.0410 | 62258.8550 | -419.1175 | -3.03% | 2 | signal |
| 24 | 2026-07-09 00:00 | 2026-07-13 00:00 | 63261.6150 | 62303.3527 | -229.7981 | -1.71% | 4 | signal |
| 25 | 2026-07-14 00:00 | 2026-07-24 00:00 | 65076.5020 | 64107.9200 | -222.3899 | -1.69% | 10 | signal |
| 26 | 2026-07-25 00:00 | 2026-07-27 00:00 | 64407.1875 | 63723.9821 | -163.2732 | -1.26% | 2 | signal |
| 27 | 2026-07-30 00:00 | 2026-07-31 00:00 | 64812.4100 | 62856.4361 | -411.4464 | -3.21% | 1 | signal |
| 28 | 2026-08-06 00:00 | 2026-08-10 00:00 | 64355.7718 | 63938.0250 | -105.1014 | -0.85% | 4 | signal |

</details>

### BTCUSDT (2y) — B (ops) 2.5%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 28 |
| Wins / Losses | 8 / 20 |
| Win rate | 28.57% |
| Strategy return | +1.14% |
| Buy & hold | +41.62% |
| Max drawdown | 0.83% |
| Expectancy (USDT) | 2.7549 |
| Avg bars held | 10.9 |
| Gate | — (ops only; not scored) |

### ETHUSDT (2y) — A (gate) 100%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 26 |
| Wins / Losses | 7 / 19 |
| Win rate | 26.92% |
| Strategy return | +89.87% |
| Buy & hold | +3.51% |
| Max drawdown | 33.71% |
| Expectancy (USDT) | 186.1688 |
| Avg bars held | 10.7 |
| Gate (WR≥60% & ret>B&H on 100%) | **FAIL** |

<details><summary>Trades (first/last 8) — gate book</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-21 00:00 | 2024-10-01 00:00 | 2613.7062 | 2446.5661 | -658.1778 | -6.58% | 10 | signal |
| 2 | 2024-10-14 00:00 | 2024-10-23 00:00 | 2631.1049 | 2523.3477 | -400.4959 | -4.29% | 9 | signal |
| 3 | 2024-10-30 00:00 | 2024-10-31 00:00 | 2660.5196 | 2517.3507 | -498.0575 | -5.57% | 1 | signal |
| 4 | 2024-11-07 00:00 | 2024-12-18 00:00 | 2896.9177 | 3624.9866 | 2100.8980 | 24.88% | 41 | signal |
| 5 | 2025-01-04 00:00 | 2025-01-07 00:00 | 3658.7084 | 3379.6193 | -823.7774 | -7.81% | 3 | signal |
| 6 | 2025-04-23 00:00 | 2025-06-05 00:00 | 1795.9675 | 2412.8030 | 3312.4323 | 34.08% | 43 | signal |
| 7 | 2025-06-07 00:00 | 2025-06-08 00:00 | 2525.8923 | 2508.5751 | -115.2126 | -0.88% | 1 | signal |
| 8 | 2025-06-09 00:00 | 2025-06-13 00:00 | 2681.4701 | 2577.9004 | -523.7450 | -4.05% | 4 | signal |
| 19 | 2026-03-23 00:00 | 2026-03-26 00:00 | 2153.1060 | 2059.3998 | -676.2222 | -4.54% | 3 | signal |
| 20 | 2026-04-05 00:00 | 2026-04-28 00:00 | 2111.2251 | 2288.2753 | 1160.7255 | 8.17% | 23 | signal |
| 21 | 2026-05-03 00:00 | 2026-05-07 00:00 | 2323.8113 | 2289.9145 | -254.4369 | -1.66% | 4 | signal |
| 22 | 2026-05-08 00:00 | 2026-05-12 00:00 | 2308.2135 | 2273.8225 | -254.9406 | -1.69% | 4 | signal |
| 23 | 2026-07-04 00:00 | 2026-07-31 00:00 | 1781.5303 | 1861.6687 | 637.3875 | 4.29% | 27 | signal |
| 24 | 2026-08-02 00:00 | 2026-08-03 00:00 | 1886.3027 | 1859.5698 | -250.1438 | -1.61% | 1 | signal |
| 25 | 2026-08-05 00:00 | 2026-08-10 00:00 | 1909.8545 | 1872.2234 | -330.2732 | -2.17% | 5 | signal |
| 26 | 2026-08-13 00:00 | 2026-08-14 00:00 | 1887.0931 | 1881.2589 | -75.8258 | -0.51% | 1 | signal |

</details>

### ETHUSDT (2y) — B (ops) 2.5%

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 26 |
| Wins / Losses | 7 / 19 |
| Win rate | 26.92% |
| Strategy return | +2.07% |
| Buy & hold | +3.51% |
| Max drawdown | 1.08% |
| Expectancy (USDT) | 5.2187 |
| Avg bars held | 10.7 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup indicators computed on longer history; entries only inside each window.
- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.
- Single-path sample; do not overfit to one bull/bear window.
- Gate PASS/FAIL is **only** on Mode A (100%-when-in); Mode B is ops parallel.
- Not related to Jewel Pine or ema-rsi paper webhook wiring.
- Does not change live/paper bot defaults.

