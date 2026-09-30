# Offline backtest: htf-ema-pullback-wide-v1

_Generated: 2026-09-05 02:56 UTC_

**RESEARCH ONLY — not enabled for paper/live.**

## Rules

- Daily bias: EMA50 > EMA200 on last **fully closed** daily bar (no lookahead)
- 4h entry: pullback (low ≤ EMA50 within lookback 5) then close crosses back above EMA20 with close ≥ EMA50, while daily bias bullish
- Stop: entry close − 3 × ATR(14) on 4h (bar-close stop)
- Exit: stop OR daily bias lost OR 4h close < EMA50

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
| htf-ema-pullback-wide-v1 | BTCUSDT | 0.00% | +0.00% | +16.14% | **FAIL** |
| htf-ema-pullback-wide-v1 | ETHUSDT | 0.00% | +0.00% | +23.96% | **FAIL** |

## Window: 6m

### BTCUSDT (6m)

Bars in window equity path: 1096 (2026-03-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 0 |
| Wins / Losses | 0 / 0 |
| Win rate | 0.00% |
| Strategy return | +0.00% |
| Buy & hold | +16.14% |
| Max drawdown | 0.00% |
| Expectancy (USDT) | 0.0000 |
| Avg bars held | 0.0 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

_No trades in this window — entry filters never fired (e.g. daily EMA50≤EMA200 for ADX/HTF bias). Gate = FAIL._

### ETHUSDT (6m)

Bars in window equity path: 1096 (2026-03-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 0 |
| Wins / Losses | 0 / 0 |
| Win rate | 0.00% |
| Strategy return | +0.00% |
| Buy & hold | +23.96% |
| Max drawdown | 0.00% |
| Expectancy (USDT) | 0.0000 |
| Avg bars held | 0.0 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

_No trades in this window — entry filters never fired (e.g. daily EMA50≤EMA200 for ADX/HTF bias). Gate = FAIL._

## Window: 2y

### BTCUSDT (2y)

Bars in window equity path: 4383 (2024-09-04 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 53 |
| Wins / Losses | 12 / 41 |
| Win rate | 22.64% |
| Strategy return | -0.22% |
| Buy & hold | +37.04% |
| Max drawdown | 0.77% |
| Expectancy (USDT) | -0.4174 |
| Avg bars held | 16.3 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-17 08:00 | 2024-09-30 08:00 | 59110.5305 | 63787.5303 | 19.2610 | 7.70% | 78 | signal |
| 2 | 2024-10-08 00:00 | 2024-10-08 04:00 | 62661.1149 | 62288.8300 | -1.9876 | -0.79% | 1 | signal |
| 3 | 2024-10-08 08:00 | 2024-10-08 12:00 | 62655.3220 | 62256.8660 | -2.0919 | -0.83% | 1 | signal |
| 4 | 2024-10-11 12:00 | 2024-10-13 12:00 | 62290.1795 | 62198.1953 | -0.8701 | -0.35% | 12 | signal |
| 5 | 2024-10-13 16:00 | 2024-10-23 00:00 | 62765.6872 | 67048.5590 | 16.5656 | 6.61% | 56 | signal |
| 6 | 2024-10-24 08:00 | 2024-10-25 16:00 | 67319.6330 | 66816.5750 | -2.3736 | -0.95% | 8 | signal |
| 7 | 2024-10-27 00:00 | 2024-10-27 08:00 | 67323.2148 | 67094.4760 | -1.3524 | -0.54% | 2 | signal |
| 8 | 2024-10-27 12:00 | 2024-11-01 00:00 | 67825.8860 | 69335.3050 | 5.0717 | 2.02% | 27 | signal |
| 46 | 2025-09-04 20:00 | 2025-09-05 12:00 | 110786.2354 | 110661.4616 | -0.7815 | -0.31% | 4 | signal |
| 47 | 2025-09-05 16:00 | 2025-09-05 20:00 | 111670.3473 | 110604.6600 | -2.8840 | -1.15% | 1 | signal |
| 48 | 2025-09-06 00:00 | 2025-09-06 04:00 | 111137.7611 | 110770.1872 | -1.3259 | -0.53% | 1 | signal |
| 49 | 2025-09-09 20:00 | 2025-09-19 16:00 | 111602.1632 | 115067.5574 | 7.2536 | 2.90% | 59 | signal |
| 50 | 2025-10-21 12:00 | 2025-10-21 20:00 | 113479.3213 | 108243.5212 | -12.0294 | -4.80% | 2 | signal+stop |
| 51 | 2025-10-29 04:00 | 2025-10-29 12:00 | 113634.6889 | 111453.9851 | -5.2892 | -2.12% | 2 | signal |
| 52 | 2025-11-02 04:00 | 2025-11-02 12:00 | 110950.9778 | 110062.4213 | -2.4971 | -1.00% | 2 | signal |
| 53 | 2025-11-12 08:00 | 2025-11-12 12:00 | 105073.3404 | 102122.4232 | -7.5031 | -3.00% | 1 | signal |

</details>

### ETHUSDT (2y)

Bars in window equity path: 4383 (2024-09-04 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 28 |
| Wins / Losses | 4 / 24 |
| Win rate | 14.29% |
| Strategy return | -0.84% |
| Buy & hold | -0.01% |
| Max drawdown | 1.42% |
| Expectancy (USDT) | -3.0154 |
| Avg bars held | 11.0 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-11-21 04:00 | 2024-11-26 12:00 | 3138.5885 | 3294.6718 | 11.9202 | 4.76% | 32 | signal |
| 2 | 2024-11-27 04:00 | 2024-12-09 12:00 | 3425.8221 | 3822.0880 | 28.4225 | 11.34% | 74 | signal |
| 3 | 2024-12-11 12:00 | 2024-12-17 20:00 | 3789.2337 | 3891.0635 | 6.2367 | 2.48% | 38 | signal |
| 4 | 2025-01-15 12:00 | 2025-01-18 04:00 | 3336.1372 | 3285.9862 | -4.2742 | -1.70% | 16 | signal |
| 5 | 2025-01-19 00:00 | 2025-01-19 04:00 | 3337.1377 | 3274.4220 | -5.2156 | -2.08% | 1 | signal |
| 6 | 2025-01-19 12:00 | 2025-01-19 20:00 | 3385.3718 | 3213.5124 | -13.2275 | -5.27% | 2 | signal |
| 7 | 2025-01-20 04:00 | 2025-01-20 20:00 | 3384.2813 | 3282.3580 | -8.0408 | -3.21% | 4 | signal |
| 8 | 2025-01-21 16:00 | 2025-01-22 04:00 | 3333.8261 | 3286.4260 | -4.0573 | -1.62% | 3 | signal |
| 21 | 2025-09-09 04:00 | 2025-09-09 12:00 | 4363.7108 | 4282.7975 | -5.1064 | -2.05% | 2 | signal |
| 22 | 2025-09-10 20:00 | 2025-09-15 12:00 | 4351.4947 | 4497.7600 | 7.8530 | 3.15% | 28 | signal |
| 23 | 2025-09-17 04:00 | 2025-09-17 08:00 | 4546.3420 | 4489.3942 | -3.6120 | -1.45% | 1 | signal |
| 24 | 2025-09-17 20:00 | 2025-09-19 08:00 | 4592.8253 | 4511.5431 | -4.8960 | -1.97% | 9 | signal |
| 25 | 2025-10-08 20:00 | 2025-10-09 00:00 | 4527.9829 | 4448.5746 | -4.8538 | -1.95% | 1 | signal |
| 26 | 2025-10-21 12:00 | 2025-10-21 20:00 | 4083.7008 | 3871.1135 | -13.4224 | -5.40% | 2 | signal |
| 27 | 2025-11-12 08:00 | 2025-11-12 12:00 | 3551.1547 | 3426.1361 | -9.2257 | -3.71% | 1 | signal |
| 28 | 2025-11-13 04:00 | 2025-11-13 08:00 | 3540.5094 | 3500.1990 | -3.3164 | -1.34% | 1 | signal |

</details>

## Caveats

- Warmup indicators computed on longer history; entries only inside each window.
- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.
- Single-path sample; do not overfit to one bull/bear window.
- Not related to Jewel Pine or ema-rsi paper webhook wiring.

