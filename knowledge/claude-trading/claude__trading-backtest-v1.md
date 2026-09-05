# Backtest — strategy spec v1

Run 2026-09-04. **Verdict: the rules lose money. Do not fund this.**

## Setup

- Data: TradingView 1h bars, `BINANCE:BTCUSDT` + `BINANCE:ETHUSDT`, 5000 bars each,
  2026-02-10 → 2026-09-04 (206 days), zero gaps. 4h and 1D frames resampled from the
  same 1h series, then shifted forward one full bar so a higher-timeframe value is only
  visible after that bar has closed. No lookahead.
- Indicators reimplemented locally and reconciled against the live TradingView MCP
  values: EMA within 0.02%, RSI within 0.7%, 4h ADX exact to two decimals, ATR within
  3% (the last bar was still forming). Close enough that the backtest is measuring the
  same strategy the scheduled task runs.
- Costs: 0.05% taker fee and 0.02% slippage per side.
- One approximation: the spec's `1D.rating.summary` filter is TradingView's proprietary
  composite and cannot be reproduced. Substituted daily EMA20 vs EMA50. Removing the
  daily filter entirely was also tested and was no better, so this is not what breaks it.

## Headline

| Variant | Trades | Win % | Expectancy | Total | Return | Max DD |
|---|---|---|---|---|---|---|
| As deployed (hourly close checks) | 20 | 25.0% | −0.731R | −14.61R | −14.0% | 15.7% |
| Realistic (intrabar stop/target) | 50 | 32.0% | −0.257R | −12.86R | −12.6% | 15.2% |
| Realistic, no daily filter | 84 | 35.7% | −0.163R | −13.72R | −13.7% | 16.3% |
| **Full window, kill switch disabled** | **137** | **35.8%** | **−0.179R** | **−24.49R** | **−23.0%** | **25.2%** |

Buy and hold over the same 206 days: **BTC +14.1%, ETH +16.9%.**

The kill switch fires on 2026-04-23, about ten weeks in, which is why the first three
rows stop early. The 137-trade row disables it purely to sample the whole window.

## Why it loses

- **Break-even win rate is 41.7%, actual is 35.8%.** After costs a winner returns
  +1.553R and a loser −1.109R, so the rules need 41.7% to tread water. They are ~6
  points short. A coin flip at this stop/target ratio would produce 37.5% — the entry
  filters do slightly *worse* than random.
- **Costs are roughly a third of the damage.** Fees and slippage cost ~0.11R per trade,
  5.6R over 50 trades. Frictionless the system still loses (−0.052R expectancy, −8.3%),
  so removing costs does not rescue it — but the leverage-inflated notional makes an
  already-negative edge decisively negative.
- **Structural conflict.** The entry buys a 1h pullback (RSI 40-55, price below EMA20)
  inside a 4h uptrend, then places a 1.5×ATR stop — tight enough that ordinary pullback
  noise takes it out before the trend resumes. Median hold is 5.5 hours. It is
  systematically stopped out of trades whose thesis was still intact.
- Losses are broad, not one bad week: 6 of 8 months negative, both symbols negative
  (BTC −4.20R, ETH −8.67R), both directions negative (long −0.29R, short −0.21R).

## Sensitivity

Every stop/target variant tested is also negative — 2.0/3.0 → −0.251R, 2.5/5.0 →
−0.203R, 1.0/3.0 → −0.246R. Nothing here is a tuning problem, and 206 days across two
correlated symbols is nowhere near enough data to tune against without curve-fitting.

## What this does and does not prove

Does: on 206 days covering one broadly bullish regime, these specific rules had negative
expectancy across 137 trades, and lost to simply holding.

Does not: rule out the general shape (higher-timeframe trend + lower-timeframe pullback).
One regime, two correlated symbols, seven months. A strategy needs testing across a bear
leg and a chop regime before anyone should believe anything about it.

## Recommendation

Do not fund the sub-account for this. Either pause the hourly task or leave it running as
a control that should keep losing — if it starts winning, the backtest is wrong and that
is worth knowing. The productive next step is TradingView's own Strategy Tester via a Pine
version of these rules: years of history, proper intrabar fills, and a fraction of the work.
