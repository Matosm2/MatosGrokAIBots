# Trading strategy spec — v1 (paper)

Owner: Matos. Created 2026-09-04. **Status: BACKTESTED AND FAILED. Paper only. Do not fund.**

> A 206-day backtest over 137 trades (see `claude/trading-backtest-v1.md`) gives these
> rules an expectancy of **-0.179R** and a **-23%** return, against +14% / +17% for simply
> holding BTC / ETH. Break-even needs a 41.7% win rate; the rules deliver 35.8%. Every
> stop/target variant tested was also negative. Keep running it on paper if you want a
> control, but no real money should follow these rules as written.
This file is the authority on when to trade. The scheduled task reads it every run.
Changing it resets the track record — note the date and reason at the bottom.

## Scope

- Market: Binance USDⓈ-M futures, `BTCUSDT` and `ETHUSDT` only.
- Leverage: **3x fixed**. Margin type: ISOLATED.
- Cadence: hourly. Every decision is made from one snapshot; no intra-hour reaction.
- Mode: paper. Real-money orders are proposed to Matos, never placed by the task.

## Data source

One call per symbol: `analyze_multi_timeframe(symbol, ["1h","4h","1D"])`.
Every field below comes from that response. If a field is missing or null for a
symbol, **skip that symbol for the run** and say so — do not substitute a guess.

## Regime filter (4h) — decides direction, or no trade at all

Long regime requires ALL of:
- `4h.moving_averages.ema20 > 4h.moving_averages.ema50`
- `price.price > 4h.moving_averages.ema50`
- `4h.oscillators.adx >= 20`
- `1D.rating.summary` is not `Sell` or `Strong Sell`

Short regime requires ALL of:
- `4h.moving_averages.ema20 < 4h.moving_averages.ema50`
- `price.price < 4h.moving_averages.ema50`
- `4h.oscillators.adx >= 20`
- `1D.rating.summary` is not `Buy` or `Strong Buy`

Neither satisfied → **no trade on that symbol this run.** ADX below 20 means there is
no trend to pull back into; standing down is the correct output, not a failure.

## Entry trigger (1h) — only evaluated if a regime passed

Long entry requires ALL of:
- `40 <= 1h.oscillators.rsi <= 55` (pulled back, not capitulating)
- `price.price <= 1h.moving_averages.ema20` (actually in a pullback)
- `1h.oscillators.stoch_k > 1h.oscillators.stoch_d` (turning back up)

Short entry requires ALL of:
- `45 <= 1h.oscillators.rsi <= 60`
- `price.price >= 1h.moving_averages.ema20`
- `1h.oscillators.stoch_k < 1h.oscillators.stoch_d`

## Levels and sizing

Let `A = 1h.atr`, `P = price.price`.

- Entry: market at `P`.
- Stop: long `P - 1.5A`, short `P + 1.5A`.
- Target: long `P + 2.5A`, short `P - 2.5A`.
- R:R is 1.67 by construction. If computed R:R < 1.5, skip — this catches bad ATR data.
- **Stop is mandatory.** No position is ever opened without one.

Risk per trade: **1% of paper equity.** This is a ceiling and a target, not a floor —
if the sizing math or the caps below produce something smaller, take the smaller size.
There is no minimum position size and no obligation to trade.

- `risk_usdt = equity * 0.01`
- `stop_distance = 1.5 * A`
- `qty = risk_usdt / stop_distance`
- `notional = qty * P`
- Cap: `notional <= equity * 3`. If it exceeds, reduce `qty` to fit — never raise leverage.
- Round `qty` down to the symbol's step size (fetch from Binance exchange info at run time).

## Position and loss limits

- Max 1 open position per symbol; max 2 concurrent total.
- No new entry on a symbol that already has an open position — manage it instead.
- Time stop: close any position open more than 48 hours, at market, regardless of PnL.
- **Kill switch:** if paper equity falls more than 15% below its peak, take no new
  entries. Manage open positions to their stops and report the drawdown to Matos.
  Only Matos clears the kill switch.

## Managing open positions (checked first, every run)

For each open position in the ledger, compare current `price.price` to its levels:
- Long: `P <= stop` → close at stop, `-1.0R`. `P >= target` → close at target, `+1.67R`.
- Short: mirrored.
- Neither, and under 48h → leave it open, record the mark price.
- Over 48h → close at `P`, record the actual R multiple.

Because the check is hourly, a wick through the stop between runs is missed and the
recorded loss will understate the real one. This is a known bias in the paper record
and must be stated whenever results are reported.

## What "paper" means here

The Binance MCP tools in this session address the **live** account — there is no testnet
endpoint. Paper fills are therefore **simulated in the ledger at the real TradingView
mark price**, with no order book, no slippage, and no funding cost. A real fill would be
worse. Treat the paper record as an optimistic upper bound on the rules' performance.

Starting paper equity: 10,000 USDT (notional; the real sub-account is unfunded).

## Change log

- 2026-09-04 — v1 written. No live trading. No track record yet.
- 2026-09-04 — v1 backtested on 206 days of 1h BTC/ETH data: negative expectancy across
  137 trades, kill switch would have fired 2026-04-23. Marked failed. Root cause looks
  structural — a 1.5xATR stop on a 1h pullback entry is inside normal noise, median hold
  5.5h, so it is stopped out of trades whose thesis is intact. v2 should widen the stop
  relative to the entry trigger, or trigger on trend continuation rather than pullback.
