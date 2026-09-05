# Offline backtest: supertrend-atr-v1

_Generated: 2026-09-05 23:34 UTC_

**RESEARCH ONLY — not enabled for paper/live. Hard-stop on FAIL (no paper/alerts/webhook).**

## Rules

- TF Daily | BTCUSDT primary
- SuperTrend(ATR length 10, mult 3)
- Entry: flip to bullish (direction +1) while flat
- Exit: flip to bearish
- Long-only Spot; no param spray

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
| supertrend-atr-v1 | BTCUSDT | A (gate) | 100% | 100.00% | +21.01% | +20.99% | 1.001 | **FAIL** |
| supertrend-atr-v1 | BTCUSDT | B (ops) | 2.5% | 100.00% | +0.52% | +20.99% | — | — |

## Window: 6m

### BTCUSDT (6m) — A (gate) 100%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 2 |
| Wins / Losses | 2 / 0 |
| Win rate (info) | 100.00% |
| Strategy return | +21.01% |
| Buy & hold | +20.99% |
| ret / B&H | 1.001 |
| Max drawdown | 13.53% |
| Expectancy (USDT) | 1050.3387 |
| Avg bars held | 42.5 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-04-13 00:00 | 2026-05-22 00:00 | 74455.1990 | 75501.7303 | 120.2977 | 1.20% | 39 | signal |
| 2 | 2026-07-21 00:00 | 2026-09-05 00:00 | 66589.4381 | 79779.3204 | 1980.3796 | 19.57% | 46 | eod |

</details>

### BTCUSDT (6m) — B (ops) 2.5%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 2 |
| Wins / Losses | 2 / 0 |
| Win rate (info) | 100.00% |
| Strategy return | +0.52% |
| Buy & hold | +20.99% |
| ret / B&H | 0.025 |
| Max drawdown | 0.37% |
| Expectancy (USDT) | 25.9975 |
| Avg bars held | 42.5 |
| Gate | — (ops only; not scored) |

## Window: full(~2y)

### BTCUSDT (full(~2y)) — A (gate) 100%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 10 |
| Wins / Losses | 5 / 5 |
| Win rate (info) | 50.00% |
| Strategy return | +14.25% |
| Buy & hold | +47.91% |
| ret / B&H | 0.297 |
| Max drawdown | 46.51% |
| Expectancy (USDT) | 142.5163 |
| Avg bars held | 37.1 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-19 00:00 | 2024-12-23 00:00 | 62979.4640 | 94834.0293 | 5027.8432 | 50.28% | 95 | signal |
| 2 | 2025-01-17 00:00 | 2025-02-24 00:00 | 104129.5187 | 91507.1036 | -1848.0373 | -12.30% | 38 | signal |
| 3 | 2025-03-02 00:00 | 2025-03-10 00:00 | 94317.1350 | 78556.5621 | -2224.3036 | -16.88% | 8 | signal |
| 4 | 2025-04-22 00:00 | 2025-06-22 00:00 | 93489.7115 | 100913.3881 | 846.3092 | 7.72% | 61 | signal |
| 5 | 2025-07-09 00:00 | 2025-08-21 00:00 | 111289.6070 | 112443.7500 | 98.5676 | 0.84% | 43 | signal |
| 6 | 2025-10-01 00:00 | 2025-10-10 00:00 | 118654.2875 | 112718.1128 | -617.9534 | -5.19% | 9 | signal |
| 7 | 2026-01-13 00:00 | 2026-01-20 00:00 | 95461.7070 | 88383.4462 | -857.4361 | -7.60% | 7 | signal |
| 8 | 2026-03-04 00:00 | 2026-03-29 00:00 | 72703.1034 | 65977.9245 | -983.2343 | -9.43% | 25 | signal |
| 9 | 2026-04-13 00:00 | 2026-05-22 00:00 | 74455.1990 | 75501.7303 | 113.5821 | 1.20% | 39 | signal |
| 10 | 2026-07-21 00:00 | 2026-09-05 00:00 | 66589.4381 | 79779.3204 | 1869.8260 | 19.57% | 46 | eod |

</details>

### BTCUSDT (full(~2y)) — B (ops) 2.5%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 10 |
| Wins / Losses | 5 / 5 |
| Win rate (info) | 50.00% |
| Strategy return | +0.70% |
| Buy & hold | +47.91% |
| ret / B&H | 0.015 |
| Max drawdown | 1.62% |
| Expectancy (USDT) | 6.9727 |
| Avg bars held | 37.1 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup on longer history; entries only inside each window.
- Thresholds fixed a priori — **not tuned on the 6m window**.
- Gate PASS/FAIL only on Mode A (100%-when-in); Mode B ops parallel.
- Does not change live/paper bot defaults.
- Fresh Path B IDs — not Jewel / open-proxy / ADX-RSI-EMA-MTF / #13.

