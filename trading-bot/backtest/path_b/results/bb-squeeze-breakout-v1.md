# Offline backtest: bb-squeeze-breakout-v1

_Generated: 2026-09-05 23:34 UTC_

**RESEARCH ONLY — not enabled for paper/live. Hard-stop on FAIL (no paper/alerts/webhook).**

## Rules

- TF Daily | BTCUSDT primary (ETH OOS if BTC 6m interesting)
- Squeeze: BB width(20,2) ≤ 20th percentile of prior 100 bars (no lookahead)
- Entry: prior bar in squeeze (or squeeze true) AND close > upper BB AND volume > SMA(vol,20)
- Exit: close < middle BB OR close < entry − 2.5×ATR(14) (ATR frozen at entry)
- Pyramiding 0

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
| bb-squeeze-breakout-v1 | BTCUSDT | A (gate) | 100% | 33.33% | +7.51% | +20.99% | 0.358 | **FAIL** |
| bb-squeeze-breakout-v1 | BTCUSDT | B (ops) | 2.5% | 33.33% | +0.21% | +20.99% | — | — |

## Window: 6m

### BTCUSDT (6m) — A (gate) 100%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 3 |
| Wins / Losses | 1 / 2 |
| Win rate (info) | 33.33% |
| Strategy return | +7.51% |
| Buy & hold | +20.99% |
| ret / B&H | 0.358 |
| Max drawdown | 7.82% |
| Expectancy (USDT) | 250.4183 |
| Avg bars held | 10.0 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-05-05 00:00 | 2026-05-15 00:00 | 80945.9728 | 79073.6534 | -250.8227 | -2.51% | 10 | signal |
| 2 | 2026-07-21 00:00 | 2026-07-24 00:00 | 66589.4381 | 64107.9200 | -382.0652 | -3.92% | 3 | signal |
| 3 | 2026-08-19 00:00 | 2026-09-05 00:00 | 69369.4574 | 79779.3204 | 1384.1429 | 14.78% | 17 | eod |

</details>

### BTCUSDT (6m) — B (ops) 2.5%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 3 |
| Wins / Losses | 1 / 2 |
| Win rate (info) | 33.33% |
| Strategy return | +0.21% |
| Buy & hold | +20.99% |
| ret / B&H | 0.010 |
| Max drawdown | 0.20% |
| Expectancy (USDT) | 6.9471 |
| Avg bars held | 10.0 |
| Gate | — (ops only; not scored) |

## Window: full(~2y)

### BTCUSDT (full(~2y)) — A (gate) 100%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 10 |
| Wins / Losses | 2 / 8 |
| Win rate (info) | 20.00% |
| Strategy return | -4.30% |
| Buy & hold | +47.91% |
| ret / B&H | -0.090 |
| Max drawdown | 37.68% |
| Expectancy (USDT) | -43.0085 |
| Avg bars held | 10.5 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-11-06 00:00 | 2024-12-10 00:00 | 75609.7760 | 96544.7035 | 2743.3002 | 27.43% | 34 | signal |
| 2 | 2024-12-16 00:00 | 2024-12-19 00:00 | 106111.6893 | 97413.1291 | -1068.0125 | -8.38% | 3 | signal |
| 3 | 2025-01-06 00:00 | 2025-01-08 00:00 | 102286.7178 | 95013.0797 | -851.9015 | -7.30% | 2 | signal |
| 4 | 2025-08-13 00:00 | 2025-08-18 00:00 | 123368.0832 | 116168.9365 | -651.9621 | -6.02% | 5 | signal+stop |
| 5 | 2025-09-12 00:00 | 2025-09-22 00:00 | 116087.4347 | 112594.6645 | -325.7429 | -3.20% | 10 | signal |
| 6 | 2026-01-02 00:00 | 2026-01-20 00:00 | 90040.1276 | 88383.4462 | -200.4640 | -2.04% | 18 | signal |
| 7 | 2026-03-04 00:00 | 2026-03-07 00:00 | 72703.1034 | 67229.2785 | -744.0097 | -7.71% | 3 | signal |
| 8 | 2026-05-05 00:00 | 2026-05-15 00:00 | 80945.9728 | 79073.6534 | -223.2625 | -2.51% | 10 | signal |
| 9 | 2026-07-21 00:00 | 2026-07-24 00:00 | 66589.4381 | 64107.9200 | -340.0842 | -3.92% | 3 | signal |
| 10 | 2026-08-19 00:00 | 2026-09-05 00:00 | 69369.4574 | 79779.3204 | 1232.0543 | 14.78% | 17 | eod |

</details>

### BTCUSDT (full(~2y)) — B (ops) 2.5%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 10 |
| Wins / Losses | 2 / 8 |
| Win rate (info) | 20.00% |
| Strategy return | +0.02% |
| Buy & hold | +47.91% |
| ret / B&H | 0.001 |
| Max drawdown | 1.18% |
| Expectancy (USDT) | 0.2442 |
| Avg bars held | 10.5 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup on longer history; entries only inside each window.
- Thresholds fixed a priori — **not tuned on the 6m window**.
- Gate PASS/FAIL only on Mode A (100%-when-in); Mode B ops parallel.
- Does not change live/paper bot defaults.
- Fresh Path B IDs — not Jewel / open-proxy / ADX-RSI-EMA-MTF / #13.

