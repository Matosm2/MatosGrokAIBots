# Offline backtest: sma200-trend-v1

_Generated: 2026-09-05 23:34 UTC_

**RESEARCH ONLY — not enabled for paper/live. Hard-stop on FAIL (no paper/alerts/webhook).**

## Rules

- TF Daily | BTCUSDT primary
- Entry: close crosses above SMA(200) while flat (or first bar close > SMA200 after flat)
- Exit: close < SMA(200)
- No EMA add-ons; no SuperTrend on this ID

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
| sma200-trend-v1 | BTCUSDT | A (gate) | 100% | 100.00% | +14.78% | +20.99% | 0.704 | **FAIL** |
| sma200-trend-v1 | BTCUSDT | B (ops) | 2.5% | 100.00% | +0.37% | +20.99% | — | — |

## Window: 6m

### BTCUSDT (6m) — A (gate) 100%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 1 |
| Wins / Losses | 1 / 0 |
| Win rate (info) | 100.00% |
| Strategy return | +14.78% |
| Buy & hold | +20.99% |
| ret / B&H | 0.704 |
| Max drawdown | 3.63% |
| Expectancy (USDT) | 1477.6624 |
| Avg bars held | 17.0 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-08-19 00:00 | 2026-09-05 00:00 | 69369.4574 | 79779.3204 | 1477.6624 | 14.78% | 17 | eod |

</details>

### BTCUSDT (6m) — B (ops) 2.5%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 1 |
| Wins / Losses | 1 / 0 |
| Win rate (info) | 100.00% |
| Strategy return | +0.37% |
| Buy & hold | +20.99% |
| ret / B&H | 0.018 |
| Max drawdown | 0.10% |
| Expectancy (USDT) | 36.9785 |
| Avg bars held | 17.0 |
| Gate | — (ops only; not scored) |

## Window: full(~2y)

### BTCUSDT (full(~2y)) — A (gate) 100%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 12 |
| Wins / Losses | 3 / 9 |
| Win rate (info) | 25.00% |
| Strategy return | +26.73% |
| Buy & hold | +47.91% |
| ret / B&H | 0.558 |
| Max drawdown | 32.08% |
| Expectancy (USDT) | 222.7335 |
| Avg bars held | 30.7 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-24 00:00 | 2024-09-25 00:00 | 64294.8313 | 63120.4340 | -202.2732 | -2.02% | 1 | signal |
| 2 | 2024-09-26 00:00 | 2024-09-30 00:00 | 65206.5770 | 63295.9262 | -306.0904 | -3.12% | 4 | signal |
| 3 | 2024-10-14 00:00 | 2025-03-09 00:00 | 66117.0320 | 80694.0028 | 2069.4970 | 21.80% | 146 | signal |
| 4 | 2025-03-12 00:00 | 2025-03-13 00:00 | 83721.9601 | 81075.2221 | -387.8560 | -3.35% | 1 | signal |
| 5 | 2025-03-14 00:00 | 2025-03-16 00:00 | 84025.1916 | 82533.2427 | -220.3202 | -1.97% | 2 | signal |
| 6 | 2025-03-19 00:00 | 2025-03-20 00:00 | 86889.3630 | 84181.2783 | -362.5733 | -3.31% | 1 | signal |
| 7 | 2025-03-23 00:00 | 2025-03-28 00:00 | 86125.5412 | 84382.1678 | -235.1043 | -2.22% | 5 | signal |
| 8 | 2025-04-22 00:00 | 2025-10-17 00:00 | 93489.7115 | 106378.4642 | 1404.0655 | 13.56% | 178 | signal |
| 9 | 2025-10-19 00:00 | 2025-10-22 00:00 | 108697.1014 | 107513.6563 | -151.2698 | -1.29% | 3 | signal |
| 10 | 2025-10-23 00:00 | 2025-10-30 00:00 | 110133.2191 | 108268.7186 | -219.3192 | -1.89% | 7 | signal |
| 11 | 2025-10-31 00:00 | 2025-11-03 00:00 | 109662.8140 | 106529.7485 | -347.4813 | -3.05% | 3 | signal |
| 12 | 2026-08-19 00:00 | 2026-09-05 00:00 | 69369.4574 | 79779.3204 | 1631.5276 | 14.78% | 17 | eod |

</details>

### BTCUSDT (full(~2y)) — B (ops) 2.5%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 12 |
| Wins / Losses | 3 / 9 |
| Win rate (info) | 25.00% |
| Strategy return | +0.70% |
| Buy & hold | +47.91% |
| ret / B&H | 0.015 |
| Max drawdown | 1.22% |
| Expectancy (USDT) | 5.8159 |
| Avg bars held | 30.7 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup on longer history; entries only inside each window.
- Thresholds fixed a priori — **not tuned on the 6m window**.
- Gate PASS/FAIL only on Mode A (100%-when-in); Mode B ops parallel.
- Does not change live/paper bot defaults.
- Fresh Path B IDs — not Jewel / open-proxy / ADX-RSI-EMA-MTF / #13.

