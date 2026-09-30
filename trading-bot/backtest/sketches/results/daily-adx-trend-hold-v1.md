# Offline backtest: daily-adx-trend-hold-v1

_Generated: 2026-09-05 02:56 UTC_

**RESEARCH ONLY — not enabled for paper/live.**

## Rules

- Timeframe: **Daily**
- Entry: EMA50 > EMA200 AND ADX(14) ≥ 25 AND +DI > −DI
- Exit: −DI > +DI OR ADX < 20 OR close < EMA200
- State-based entry (hold while conditions allow); pyramiding 0

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
| daily-adx-trend-hold-v1 | BTCUSDT | 0.00% | +0.00% | +18.29% | **FAIL** |
| daily-adx-trend-hold-v1 | ETHUSDT | 0.00% | +0.00% | +24.49% | **FAIL** |

## Window: 6m

### BTCUSDT (6m)

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 0 |
| Wins / Losses | 0 / 0 |
| Win rate | 0.00% |
| Strategy return | +0.00% |
| Buy & hold | +18.29% |
| Max drawdown | 0.00% |
| Expectancy (USDT) | 0.0000 |
| Avg bars held | 0.0 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

_No trades in this window — entry filters never fired (e.g. daily EMA50≤EMA200 for ADX/HTF bias). Gate = FAIL._

### ETHUSDT (6m)

Bars in window equity path: 183 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 0 |
| Wins / Losses | 0 / 0 |
| Win rate | 0.00% |
| Strategy return | +0.00% |
| Buy & hold | +24.49% |
| Max drawdown | 0.00% |
| Expectancy (USDT) | 0.0000 |
| Avg bars held | 0.0 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

_No trades in this window — entry filters never fired (e.g. daily EMA50≤EMA200 for ADX/HTF bias). Gate = FAIL._

## Window: 2y

### BTCUSDT (2y)

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 6 |
| Wins / Losses | 2 / 4 |
| Win rate | 33.33% |
| Strategy return | +0.47% |
| Buy & hold | +41.62% |
| Max drawdown | 0.66% |
| Expectancy (USDT) | 7.8142 |
| Avg bars held | 16.7 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-11-09 00:00 | 2024-12-20 00:00 | 76715.7987 | 97756.5373 | 67.9986 | 27.17% | 41 | signal |
| 2 | 2025-03-24 00:00 | 2025-03-26 00:00 | 87541.9091 | 86865.7154 | -2.4456 | -0.97% | 2 | signal |
| 3 | 2025-04-27 00:00 | 2025-05-30 00:00 | 93796.1747 | 103933.4873 | 26.6662 | 10.59% | 33 | signal |
| 4 | 2025-07-16 00:00 | 2025-08-01 00:00 | 118689.7452 | 113241.2810 | -12.0751 | -4.78% | 16 | signal |
| 5 | 2025-10-05 00:00 | 2025-10-10 00:00 | 123544.0512 | 112718.1128 | -22.5645 | -8.95% | 5 | signal |
| 6 | 2025-10-26 00:00 | 2025-10-29 00:00 | 114616.6797 | 109966.2794 | -10.6945 | -4.25% | 3 | signal |

</details>

### ETHUSDT (2y)

Bars in window equity path: 731 (2024-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 2 |
| Wins / Losses | 2 / 0 |
| Win rate | 100.00% |
| Strategy return | +1.21% |
| Buy & hold | +3.51% |
| Max drawdown | 0.53% |
| Expectancy (USDT) | 60.2574 |
| Avg bars held | 38.5 |
| Gate (WR≥60% & ret>B&H) | **FAIL** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-11-20 00:00 | 2024-12-19 00:00 | 3071.5050 | 3415.3015 | 27.4548 | 10.97% | 29 | signal |
| 2 | 2025-07-15 00:00 | 2025-09-01 00:00 | 3139.4589 | 4312.3427 | 93.0600 | 37.08% | 48 | signal |

</details>

## Caveats

- Warmup indicators computed on longer history; entries only inside each window.
- ETHUSDT is OOS with unchanged params vs BTCUSDT primary.
- Single-path sample; do not overfit to one bull/bear window.
- Not related to Jewel Pine or ema-rsi paper webhook wiring.

