# EMA RSI Trend v1.1 (Pine)

Pine Script strategy for paper-first TradingView → bot webhooks.

**Script:** [`ema-rsi-trend-v1.1.pine`](./ema-rsi-trend-v1.1.pine)  
**strategy_id:** `ema-rsi-trend-v1`

## Rules

| Side | Logic | `qty_pct` |
|------|--------|-----------|
| **Buy** | EMA20 crosses above EMA50, RSI14 ≥ 50, close ≥ slow EMA | `2.5` |
| **Sell** | EMA20 crossunder EMA50 **OR** RSI14 crossunder 40 | `12` |

- Bar close only (`process_orders_on_close`).
- Exits use **strategy() position / price** — the script does **not** read bot open-state.
- Sell **`qty_pct: 12`** is intentional (full exit within Balanced max-position framing). Do **not** omit qty on sell (bot would only size to `RISK_PER_TRADE_PCT` = 2.5%).
- Webhook JSON from `alert()` **strips `BINANCE:`** (and similar) so `symbol` is `BTCUSDT`-style. The bot also normalizes `{{ticker}}` if you use alertconditions.
- **Paper universe:** `BTCUSDT` and `ETHUSDT` only.
- **`alert_id`:** use **`{{time}}`**, not `{{timenow}}`.

## cooldown_bars

- Input **Cooldown bars after exit** (default **6**).
- Counts bars **after an exit (SELL)** before a new **BUY / re-entry** is allowed.
- Set to **0** to disable. Not a cooldown after entries.

## Stops

- **No hard stop in v1.1** — exits are signal-only.
- A **hard stop is required in a later brief before real live** trading.

## TradingView setup (two alerts)

1. Add the script to a **BTCUSDT** or **ETHUSDT** chart (paper universe).
2. Create **two** alerts (Once Per Bar Close):

### Option A — alertconditions (recommended for two named alerts)

#### Alert 1 — Buy

- Condition: **EMA-RSI v1.1 Buy**
- Webhook URL: `https://YOUR_HOST/webhook/tradingview`
- Message:

```json
{
  "symbol": "{{ticker}}",
  "side": "buy",
  "qty_pct": 2.5,
  "strategy_id": "ema-rsi-trend-v1.1",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-ema-rsi-v1-buy",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

#### Alert 2 — Sell

- Condition: **EMA-RSI v1.1 Sell**
- Same webhook URL.
- Message:

```json
{
  "symbol": "{{ticker}}",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "ema-rsi-trend-v1.1",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-ema-rsi-v1-sell",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

### Option B — single “Any alert() function call”

Uses Pine-built JSON with **normalized** symbol (`BINANCE:` stripped). Still use Once Per Bar Close.
`qty_pct` comes from the script inputs **Buy qty_pct (webhook)** / **Sell qty_pct (webhook)** (defaults 2.5 / 12).

Replace `YOUR_WEBHOOK_SECRET` with the bot `WEBHOOK_SECRET`. Keep bot `TRADING_MODE=paper` until risk behaviour is verified.

Sell `alert()` / alertcondition only fire when `strategy.position_size > 0` (no flat reject noise).

## Bot compatibility notes

- Sell `qty_pct: 12` requires the bot to **not** cap sells with `RISK_PER_TRADE_PCT` (safety PR).
- Prefer header `X-Webhook-Secret` when possible; otherwise keep `"secret"` in the JSON body.
