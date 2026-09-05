# Paper trade ledger

Append-only record for the hourly scheduled task. Rules live in
`claude/trading-strategy-spec.md`. **Never edit past rows** — correct by adding
a new row that says what changed.

Every figure here is simulated at TradingView mark prices. No real order has
been placed and the Binance sub-account is unfunded.

## State

- Paper equity: **10,000.00 USDT**
- Peak paper equity: **10,000.00 USDT**
- Drawdown from peak: **0.00%**
- Kill switch (trips at -15%): **not tripped**
- Open positions: **0**
- Closed trades: **0**

## Open positions

_none_

| Symbol | Side | Opened (UTC) | Entry | Stop | Target | Qty | Notional | Last mark |
|---|---|---|---|---|---|---|---|---|

## Closed trades

_none_

| # | Symbol | Side | Opened | Closed | Entry | Exit | R | PnL USDT | Reason |
|---|---|---|---|---|---|---|---|---|---|

## Run log

Newest first. One line per run, including runs where nothing happened —
the no-trade runs are what show whether the filters are too tight.

| Run (UTC) | BTCUSDT | ETHUSDT | Action |
|---|---|---|---|
| 2026-09-04 20:29 | long regime ok (4h ADX 23.4, EMA20>EMA50); entry blocked: stoch_k 36.7 < stoch_d 37.6 | long regime ok (4h ADX 21.2); entry blocked: stoch_k 16.9 < stoch_d 17.6 | none — stood down on both |
