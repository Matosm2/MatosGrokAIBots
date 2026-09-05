# Offline backtest: kama-er-trend-v1

_Generated: 2026-09-05 23:34 UTC_

**RESEARCH ONLY — not enabled for paper/live. Hard-stop on FAIL (no paper/alerts/webhook).**

## Rules

- TF Daily | BTC then ETH if needed
- KAMA(10, fast=2, slow=30) + ER(10)
- Entry: close > KAMA AND ER > 0.30 (and flat)
- Exit: close < KAMA OR ER < 0.20

## Common costs / sizing

| Parameter | Value |
|-----------|-------|
| Fee | 0.10% / side |
| Slippage | 5 bps adverse vs close |
| Size Mode A (**gate**) | **100% equity when in** (PASS/FAIL uses this only) |
| Size Mode B (**ops**) | **2.5% equity** (report only) |
| Close | full position |
| Mode | spot long-only, bar-close, no lookahead |
| Data | Binance Spot OHLCV via **ccxt** (owned cache) |

## Gate table (mandatory 6m Mode-A lead)

PASS iff **n>0** AND **Mode-A return ≥ 1.2 × B&H** (same window). WR informational only. Mode B = —.

| Strategy | Symbol | Mode | Size | 6m WR | 6m Mode-A ret | 6m B&H | ret/B&H | PASS/FAIL |
|----------|--------|------|------|-------|---------------|--------|---------|-----------|
| kama-er-trend-v1 | BTCUSDT | A (gate) | 100% | 27.27% | -2.97% | +20.99% | -0.141 | **FAIL** |
| kama-er-trend-v1 | BTCUSDT | B (ops) | 2.5% | 27.27% | -0.04% | +20.99% | — | — |

## Window: 6m

### BTCUSDT (6m) — A (gate) 100%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 11 |
| Wins / Losses | 3 / 8 |
| Win rate (info) | 27.27% |
| Strategy return | -2.97% |
| Buy & hold | +20.99% |
| ret / B&H | -0.141 |
| Max drawdown | 15.99% |
| Expectancy (USDT) | -26.9757 |
| Avg bars held | 5.0 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-03-16 00:00 | 2026-03-19 00:00 | 74922.1123 | 69895.0350 | -689.6132 | -6.90% | 3 | signal |
| 2 | 2026-04-06 00:00 | 2026-04-19 00:00 | 68888.0868 | 73764.8891 | 639.1922 | 6.87% | 13 | signal |
| 3 | 2026-04-22 00:00 | 2026-04-27 00:00 | 78217.3191 | 77332.6343 | -132.1901 | -1.33% | 5 | signal |
| 4 | 2026-05-05 00:00 | 2026-05-13 00:00 | 80945.9728 | 79273.9532 | -221.9979 | -2.26% | 8 | signal |
| 5 | 2026-06-07 00:00 | 2026-06-08 00:00 | 63363.6760 | 63054.4470 | -65.9057 | -0.69% | 1 | signal |
| 6 | 2026-06-11 00:00 | 2026-06-13 00:00 | 63657.8030 | 64425.7810 | 95.6956 | 1.00% | 2 | signal |
| 7 | 2026-06-15 00:00 | 2026-06-17 00:00 | 66361.9044 | 64477.1453 | -292.0518 | -3.03% | 2 | signal |
| 8 | 2026-07-05 00:00 | 2026-07-13 00:00 | 63681.8250 | 62303.3527 | -220.2711 | -2.36% | 8 | signal |
| 9 | 2026-07-21 00:00 | 2026-07-24 00:00 | 66589.4381 | 64107.9200 | -357.1282 | -3.92% | 3 | signal |
| 10 | 2026-08-19 00:00 | 2026-08-28 00:00 | 69369.4574 | 77806.9471 | 1045.3480 | 11.94% | 9 | signal |
| 11 | 2026-08-29 00:00 | 2026-08-30 00:00 | 78269.1150 | 77643.1590 | -97.8099 | -1.00% | 1 | signal |

</details>

### BTCUSDT (6m) — B (ops) 2.5%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 11 |
| Wins / Losses | 3 / 8 |
| Win rate (info) | 27.27% |
| Strategy return | -0.04% |
| Buy & hold | +20.99% |
| ret / B&H | -0.002 |
| Max drawdown | 0.44% |
| Expectancy (USDT) | -0.3890 |
| Avg bars held | 5.0 |
| Gate | — (ops only; not scored) |

## Window: full(~2y)

### BTCUSDT (full(~2y)) — A (gate) 100%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 39 |
| Wins / Losses | 13 / 26 |
| Win rate (info) | 33.33% |
| Strategy return | +0.29% |
| Buy & hold | +47.91% |
| ret / B&H | 0.006 |
| Max drawdown | 36.63% |
| Expectancy (USDT) | 0.7482 |
| Avg bars held | 5.3 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-16 00:00 | 2024-09-30 00:00 | 58243.0970 | 63295.9262 | 845.8279 | 8.46% | 14 | signal |
| 2 | 2024-10-12 00:00 | 2024-10-23 00:00 | 63237.8231 | 66635.3157 | 559.8648 | 5.16% | 11 | signal |
| 3 | 2024-10-29 00:00 | 2024-11-01 00:00 | 72772.7882 | 69461.2620 | -540.7677 | -4.74% | 3 | signal |
| 4 | 2024-11-06 00:00 | 2024-11-25 00:00 | 75609.7760 | 92963.5050 | 2466.9945 | 22.71% | 19 | signal |
| 5 | 2024-12-06 00:00 | 2024-12-09 00:00 | 99790.7104 | 97227.8318 | -368.3506 | -2.76% | 3 | signal |
| 6 | 2024-12-15 00:00 | 2024-12-18 00:00 | 104516.2220 | 100153.9080 | -565.8956 | -4.37% | 3 | signal |
| 7 | 2025-01-06 00:00 | 2025-01-07 00:00 | 102286.7178 | 96906.1327 | -675.6220 | -5.45% | 1 | signal |
| 8 | 2025-01-17 00:00 | 2025-01-26 00:00 | 104129.5187 | 102568.6900 | -198.7750 | -1.70% | 9 | signal |
| 32 | 2026-05-05 00:00 | 2026-05-13 00:00 | 80945.9728 | 79273.9532 | -229.4544 | -2.26% | 8 | signal |
| 33 | 2026-06-07 00:00 | 2026-06-08 00:00 | 63363.6760 | 63054.4470 | -68.1194 | -0.69% | 1 | signal |
| 34 | 2026-06-11 00:00 | 2026-06-13 00:00 | 63657.8030 | 64425.7810 | 98.9098 | 1.00% | 2 | signal |
| 35 | 2026-06-15 00:00 | 2026-06-17 00:00 | 66361.9044 | 64477.1453 | -301.8612 | -3.03% | 2 | signal |
| 36 | 2026-07-05 00:00 | 2026-07-13 00:00 | 63681.8250 | 62303.3527 | -227.6696 | -2.36% | 8 | signal |
| 37 | 2026-07-21 00:00 | 2026-07-24 00:00 | 66589.4381 | 64107.9200 | -369.1234 | -3.92% | 3 | signal |
| 38 | 2026-08-19 00:00 | 2026-08-28 00:00 | 69369.4574 | 77806.9471 | 1080.4591 | 11.94% | 9 | signal |
| 39 | 2026-08-29 00:00 | 2026-08-30 00:00 | 78269.1150 | 77643.1590 | -101.0952 | -1.00% | 1 | signal |

</details>

### BTCUSDT (full(~2y)) — B (ops) 2.5%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 39 |
| Wins / Losses | 13 / 26 |
| Win rate (info) | 33.33% |
| Strategy return | +0.15% |
| Buy & hold | +47.91% |
| ret / B&H | 0.003 |
| Max drawdown | 1.11% |
| Expectancy (USDT) | 0.3941 |
| Avg bars held | 5.3 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup on longer history; entries only inside each window.
- Thresholds fixed a priori — **not tuned on the 6m window**.
- Gate PASS/FAIL only on Mode A (100%-when-in); Mode B ops parallel.
- Does not change live/paper bot defaults.
- Fresh Path B IDs — not Jewel / open-proxy / ADX-RSI-EMA-MTF / #13.

