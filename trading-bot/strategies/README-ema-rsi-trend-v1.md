# EMA RSI Trend v1.1 (Pine)

Pine Script strategy for paper-first TradingView → bot webhooks.

**Script:** [`ema-rsi-trend-v1.1.pine`](./ema-rsi-trend-v1.1.pine)

## Rules

| Side | Logic | `qty_pct` |
|------|--------|-----------|
| **Buy** | EMA20 crosses above EMA50, RSI14 ≥ 50, close ≥ slow EMA | `2.5` |
| **Sell** | EMA20 crossunder EMA50 **OR** RSI14 crossunder 40 | `12` |

- Exits are **signal / price only** — the script does **not** read bot open-state or exchange positions.
- **Paper universe:** `BTCUSDT` and `ETHUSDT` only (set bot `ALLOWED_SYMBOLS` accordingly for paper).
- **`alert_id`:** `{{ticker}}-{{time}}-ema-rsi-v1-buy` / `...-sell` (use **`{{time}}`**, not `{{timenow}}`).

## cooldown_bars

- Input **Cooldown bars after exit** (default **6**).
- Counts bars **after an exit (SELL)** before a new **BUY / re-entry** is allowed.
- Set to **0** to disable.
- This is **not** a cooldown after entries.

## Stops

- **No hard stop in v1.1** — exits are signal-only (EMA crossunder / RSI crossunder 40).
- A **hard stop is required in a later brief before real live** trading.

## TradingView setup (two alerts)

1. Add the script to a **BTCUSDT** or **ETHUSDT** chart (paper universe).
2. Create **two** alerts on this strategy/indicator:

### Alert 1 — Buy

- Condition: **EMA-RSI v1.1 Buy** (or “order fills” / alertcondition buy).
- Webhook URL: `https://YOUR_HOST/webhook/tradingview`
- Message:

```json
{
  "symbol": "{{ticker}}",
  "side": "buy",
  "qty_pct": 2.5,
  "strategy_id": "ema-rsi-trend-v1",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-ema-rsi-v1-buy",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

### Alert 2 — Sell

- Condition: **EMA-RSI v1.1 Sell**.
- Same webhook URL.
- Message:

```json
{
  "symbol": "{{ticker}}",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "ema-rsi-trend-v1",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-ema-rsi-v1-sell",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

Replace `YOUR_WEBHOOK_SECRET` with the bot `WEBHOOK_SECRET`. Keep bot `TRADING_MODE=paper` until risk behaviour is verified.

## Bot compatibility notes

- Sell `qty_pct: 12` is intentional (max-position-sized exit). The bot must **not** cap sells with `RISK_PER_TRADE_PCT` (see safety PR).
- Prefer header `X-Webhook-Secret` if your tunnel/TV setup supports custom headers; otherwise keep `"secret"` in the JSON body.
