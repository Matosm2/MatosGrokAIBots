# Offline backtest: ema-rsi-trend-v1.1

_Generated: 2026-09-05 01:26 UTC_

## Strategy (must-match checklist)

1. **Bar-close only, no lookahead** — fills and signals at bar close.
2. **Pine v1.1:** EMA20/50 cross + RSI≥50 + close≥EMA50 buy; sell EMA crossunder OR RSI cross under 40; cooldown 6; BTC+ETH; no hard stop.
3. **Fees/slippage:** fee **0.10% per side** (Pine `commission_value=0.1`); slippage **0.050%** adverse vs close.
4. **Sell = full close** (not 2.5% clips).
5. **Buy 2.5% equity**; max pos 12% / max 4 opens apply to live bot — per-symbol offline book has ≤1 open; **daily halt not modeled**.
6. **Spot long-only** — do not conflate with failed futures v1.
7. Report includes trades, win%, expectancy, vs buy-hold, max DD, hold time; regime flags below.

## Data

- Source: Binance Spot public `/api/v3/klines` (1h)
- Requested lookback: ~2.0 years
- Symbols: BTCUSDT, ETHUSDT
- **BTCUSDT:** 17532 bars, 2024-09-04 14:00 UTC → 2026-09-05 01:00 UTC
  - Regime note: overall bullish window; halves disagree — mixed regimes (good)
- **ETHUSDT:** 17532 bars, 2024-09-04 14:00 UTC → 2026-09-05 01:00 UTC
  - Regime note: overall range-ish (±15%); halves disagree — mixed regimes (good)

## Sizing & costs

| Parameter | Value |
|-----------|-------|
| Initial equity (per symbol book) | 10_000 USDT |
| Buy size | 2.5% of equity |
| Sell | 100% of open long |
| Fee per side | 0.10% |
| Slippage per side | 0.050% adverse |
| Hard stop | none (v1.1) |
| Daily loss halt | **not modeled** |

## BTCUSDT

| Metric | Value |
|--------|-------|
| Trades | 151 |
| Wins / Losses | 42 / 109 |
| Win rate | 27.81% |
| Expectancy (USDT/trade) | -0.4931 |
| Expectancy (%/trade) | -0.1963% |
| Total PnL (USDT) | -74.45 |
| Strategy return | -0.74% |
| Buy & hold return | 38.49% |
| vs buy & hold (pp) | -39.24 |
| Max drawdown | 2.17% |
| Avg win / avg loss | 8.0710 / -3.7930 |
| Profit factor | 0.82 |
| Avg bars held (1H) | 41.7 (~41.7h) |

<details><summary>Trades (first/last 10)</summary>

| # | Entry (UTC) | Exit (UTC) | Entry | Exit | PnL | PnL% | Bars |
|---|-------------|------------|-------|------|-----|------|------|
| 1 | 2024-09-09 06:00 UTC | 2024-09-11 05:00 UTC | 54925.4490 | 56215.8780 | 5.3677 | 2.14% | 47 |
| 2 | 2024-09-17 15:00 UTC | 2024-09-22 09:00 UTC | 61166.0677 | 62671.5885 | 5.6503 | 2.26% | 114 |
| 3 | 2024-09-22 19:00 UTC | 2024-09-25 17:00 UTC | 63191.5800 | 63136.4160 | -0.7188 | -0.29% | 70 |
| 4 | 2024-09-26 10:00 UTC | 2024-09-30 01:00 UTC | 64424.1860 | 64737.6050 | 0.7158 | 0.29% | 87 |
| 5 | 2024-10-04 16:00 UTC | 2024-10-08 09:00 UTC | 62275.1220 | 62506.1113 | 0.4268 | 0.17% | 89 |
| 6 | 2024-10-11 16:00 UTC | 2024-10-13 14:00 UTC | 62303.1360 | 62218.4752 | -0.8403 | -0.34% | 46 |
| 7 | 2024-10-24 13:00 UTC | 2024-10-25 17:00 UTC | 67939.9430 | 66802.5920 | -4.6859 | -1.87% | 28 |
| 8 | 2024-10-27 14:00 UTC | 2024-10-31 13:00 UTC | 67729.8380 | 71272.3460 | 12.5702 | 5.02% | 95 |
| 9 | 2024-11-05 14:00 UTC | 2024-11-14 15:00 UTC | 69998.9820 | 87904.0160 | 63.5007 | 25.33% | 217 |
| 10 | 2024-11-15 11:00 UTC | 2024-11-17 20:00 UTC | 89786.1206 | 89591.1820 | -1.0508 | -0.42% | 57 |
| 142 | 2026-07-26 16:00 UTC | 2026-07-27 15:00 UTC | 64766.5371 | 64521.7330 | -1.4288 | -0.58% | 23 |
| 143 | 2026-07-29 11:00 UTC | 2026-07-29 19:00 UTC | 64539.7938 | 63557.6653 | -4.2547 | -1.72% | 8 |
| 144 | 2026-07-30 09:00 UTC | 2026-07-31 07:00 UTC | 64599.8438 | 63918.0350 | -3.1012 | -1.25% | 22 |
| 145 | 2026-08-02 22:00 UTC | 2026-08-03 03:00 UTC | 63456.2923 | 62839.0548 | -2.8959 | -1.17% | 5 |
| 146 | 2026-08-03 17:00 UTC | 2026-08-09 02:00 UTC | 63937.9530 | 64787.6000 | 2.7859 | 1.13% | 129 |
| 147 | 2026-08-17 04:00 UTC | 2026-08-23 05:00 UTC | 63564.2062 | 76015.3433 | 47.8692 | 19.35% | 145 |
| 148 | 2026-08-27 01:00 UTC | 2026-08-28 15:00 UTC | 78938.1193 | 78291.9644 | -2.5275 | -1.02% | 38 |
| 149 | 2026-08-30 15:00 UTC | 2026-08-30 23:00 UTC | 78863.0418 | 77643.1590 | -4.3332 | -1.74% | 8 |
| 150 | 2026-08-31 16:00 UTC | 2026-09-01 08:00 UTC | 78678.8898 | 77844.3384 | -3.1261 | -1.26% | 16 |
| 151 | 2026-09-03 12:00 UTC | 2026-09-04 12:00 UTC | 78691.7062 | 79414.2330 | 1.7795 | 0.72% | 24 |

_… 131 trades omitted …_

</details>

## ETHUSDT

| Metric | Value |
|--------|-------|
| Trades | 172 |
| Wins / Losses | 49 / 123 |
| Win rate | 28.49% |
| Expectancy (USDT/trade) | -1.0644 |
| Expectancy (%/trade) | -0.4271% |
| Total PnL (USDT) | -183.08 |
| Strategy return | -1.83% |
| Buy & hold return | 0.59% |
| vs buy & hold (pp) | -2.42 |
| Max drawdown | 2.75% |
| Avg win / avg loss | 10.5088 / -5.6749 |
| Profit factor | 0.74 |
| Avg bars held (1H) | 36.8 (~36.8h) |

<details><summary>Trades (first/last 10)</summary>

| # | Entry (UTC) | Exit (UTC) | Entry | Exit | PnL | PnL% | Bars |
|---|-------------|------------|-------|------|-----|------|------|
| 1 | 2024-09-09 08:00 UTC | 2024-09-11 10:00 UTC | 2327.5732 | 2315.3218 | -1.8146 | -0.73% | 50 |
| 2 | 2024-09-11 19:00 UTC | 2024-09-12 15:00 UTC | 2341.7703 | 2322.0384 | -2.6039 | -1.04% | 20 |
| 3 | 2024-09-17 18:00 UTC | 2024-09-18 09:00 UTC | 2351.1750 | 2294.2023 | -6.5489 | -2.62% | 15 |
| 4 | 2024-09-18 23:00 UTC | 2024-09-22 21:00 UTC | 2375.9374 | 2546.3362 | 17.3926 | 6.96% | 94 |
| 5 | 2024-09-26 15:00 UTC | 2024-09-29 06:00 UTC | 2653.3360 | 2648.6750 | -0.9393 | -0.38% | 63 |
| 6 | 2024-10-04 23:00 UTC | 2024-10-07 18:00 UTC | 2415.6172 | 2423.8575 | 0.3522 | 0.14% | 67 |
| 7 | 2024-10-09 01:00 UTC | 2024-10-09 08:00 UTC | 2463.6312 | 2429.7745 | -3.9345 | -1.57% | 7 |
| 8 | 2024-10-11 13:00 UTC | 2024-10-13 14:00 UTC | 2432.5257 | 2445.8365 | 0.8668 | 0.35% | 49 |
| 9 | 2024-10-27 22:00 UTC | 2024-10-31 13:00 UTC | 2515.7472 | 2601.5386 | 8.0191 | 3.20% | 87 |
| 10 | 2024-11-06 02:00 UTC | 2024-11-13 04:00 UTC | 2569.5842 | 3188.4650 | 59.7163 | 23.84% | 170 |
| 163 | 2026-07-30 10:00 UTC | 2026-07-31 07:00 UTC | 1919.2191 | 1889.2549 | -4.3372 | -1.76% | 21 |
| 164 | 2026-08-02 23:00 UTC | 2026-08-03 03:00 UTC | 1886.3027 | 1856.2914 | -4.4085 | -1.79% | 4 |
| 165 | 2026-08-04 12:00 UTC | 2026-08-04 13:00 UTC | 1876.0476 | 1861.1290 | -2.4488 | -0.99% | 1 |
| 166 | 2026-08-12 11:00 UTC | 2026-08-12 19:00 UTC | 1916.5278 | 1878.4403 | -5.3801 | -2.18% | 8 |
| 167 | 2026-08-15 19:00 UTC | 2026-08-16 05:00 UTC | 1885.4923 | 1878.8701 | -1.3554 | -0.55% | 10 |
| 168 | 2026-08-16 16:00 UTC | 2026-08-16 21:00 UTC | 1890.5248 | 1874.6222 | -2.5595 | -1.04% | 5 |
| 169 | 2026-08-26 21:00 UTC | 2026-08-28 15:00 UTC | 2498.0684 | 2470.6541 | -3.1884 | -1.30% | 42 |
| 170 | 2026-08-30 14:00 UTC | 2026-08-30 23:00 UTC | 2478.3586 | 2415.6716 | -6.7047 | -2.72% | 9 |
| 171 | 2026-08-31 19:00 UTC | 2026-09-01 13:00 UTC | 2483.0809 | 2443.1878 | -4.4351 | -1.80% | 18 |
| 172 | 2026-09-03 15:00 UTC | 2026-09-04 12:00 UTC | 2517.8383 | 2450.0144 | -7.1004 | -2.89% | 21 |

_… 152 trades omitted …_

</details>

## COMBINED (trade-pool + mean per-symbol return)

Independent per-symbol books (each started at 10k). Expectancy/win% from pooled trades; return = mean of per-symbol returns; max DD = worst per-symbol DD.

| Metric | Value |
|--------|-------|
| Trades | 323 |
| Wins / Losses | 91 / 232 |
| Win rate | 28.17% |
| Expectancy (USDT/trade) | -0.7973 |
| Expectancy (%/trade) | -0.3192% |
| Total PnL (USDT) | -257.53 |
| Strategy return | -1.29% |
| Buy & hold return | 19.54% |
| vs buy & hold (pp) | -20.83 |
| Max drawdown | 2.75% |
| Avg win / avg loss | 9.3836 / -4.7907 |
| Profit factor | 0.77 |
| Avg bars held (1H) | 39.1 (~39.1h) |

## Caveats

- Bar-close fills only; indicators use closed bars (no lookahead).
- Fee 0.10% per side; slippage 0.050% adverse vs close (buy higher / sell lower).
- Sell closes 100% of open long (not RISK_PER_TRADE_PCT clips).
- Daily loss halt (MAX_DAILY_LOSS_PCT) not modeled in this offline engine.
- Spot long-only — not related to any failed futures v1 experiment.
- Max position 12% / max 4 opens: single-symbol run has ≤1 open; multi-symbol portfolio constraints not enforced across independent books.
- Single-regime windows: see per-symbol regime notes; do not overfit to one bull run.
- Cache under `backtest/cache/` is gitignored; re-fetch on demand.

