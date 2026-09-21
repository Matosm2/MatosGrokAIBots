# AccDist SMA Cross v1 (Pine) — PAPER ONLY (LIVE OFF)

Pine Script strategy for paper-seat TradingView → bot webhooks. Authorized by CoS/Nuno based on the 2026-09-22 Path B Mode-A per-coin census.

**Script:** [`accdist-sma-cross-v1.pine`](./accdist-sma-cross-v1.pine)  
**strategy_id:** `accdist-sma-cross-v1`  
**Status:** **PAPER ONLY / LIVE OFF** (never enable live API keys or LIVE trading)

---

## Census Performance (2026-09-22)

- **Pair:** ETHUSDT only
- **Timeframe:** 4h (Mode A)
- **Parameters:** `smaLen = 50` (`mode_a|sma50`)
- **Stage / PR:** Stage 1 (PR#29)
- **Trade count (n):** 46 (dense, passes `n >= 40` gate)
- **Win Rate:** 21.7%
- **Mode-A Return:** +19.67%
- **Buy & Hold:** +10.63%
- **×B&H:** **1.850×** (qualifies under per-coin gate `Mode-A >= 1.2× B&H` AND `n >= 40`)

---

## Rules

| Side | Logic | `qty_pct` |
|------|-------|-----------|
| **Buy** | `ta.crossover(adl, adlSma)` AND `cooldownOk` | `2.5` |
| **Sell** | `ta.crossunder(adl, adlSma)` AND `strategy.position_size > 0` | `12` |

### Raw Accumulation/Distribution (ADL) Formula
```pinescript
// NOTE: Raw ADL vs SMA, NOT Chaikin Oscillator!
adl    = ta.accdist
adlSma = ta.sma(adl, 50)
```

- Bar close only (`process_orders_on_close = true`).
- Exits use **strategy() position / price** — does NOT read bot open-state.
- Sell **`qty_pct: 12`** is intentional (full exit within Balanced max-position framing). Do **not** omit qty on sell (bot would only size to `RISK_PER_TRADE_PCT` = 2.5%).
- Webhook JSON from `alert()` **strips exchange prefix** (e.g. `BINANCE:`) so `symbol` is `ETHUSDT`-style.
- **Universe:** `ETHUSDT` ONLY at `4h`.
- **`alert_id`:** Uses **`{{time}}`**, NOT `{{timenow}}`.

---

## cooldown_bars

- Input **Cooldown bars after exit** (default **6**, matching `ema-rsi` defaults).
- Counts bars **after an exit (SELL)** before a new **BUY / re-entry** is allowed.
- Set to **0** to disable. Does not apply after entries.

---

## Stops

- **No hard stop in this version** — exits are signal-only (`ta.crossunder(adl, adlSma)`).
- **A hard stop brief is required in a later brief before any real live trading.**

---

## TradingView setup (two alerts)

1. Add the script to an **ETHUSDT** chart on the **4h** timeframe.
2. Verify inputs: `ADL SMA Length = 50`, `Cooldown bars after exit = 6`, `Buy qty_pct = 2.5`, `Sell qty_pct = 12.0`, `strategy_id = accdist-sma-cross-v1`.
3. Create **two** alerts (Once Per Bar Close):

### Option A — alertconditions (recommended for two named alerts)

#### Alert 1 — Buy
- Condition: **AccDist SMA50 Buy**
- Trigger: **Once Per Bar Close**
- Webhook URL: `https://YOUR_RAILWAY_APP.up.railway.app/webhook/tradingview`
- Message:
```json
{
  "symbol": "{{ticker}}",
  "side": "buy",
  "qty_pct": 2.5,
  "strategy_id": "accdist-sma-cross-v1",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-accdist-sma50-buy",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

#### Alert 2 — Sell
- Condition: **AccDist SMA50 Sell**
- Trigger: **Once Per Bar Close**
- Webhook URL: `https://YOUR_RAILWAY_APP.up.railway.app/webhook/tradingview`
- Message:
```json
{
  "symbol": "{{ticker}}",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "accdist-sma-cross-v1",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-accdist-sma50-sell",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

### Option B — single “Any alert() function call”
Uses Pine-built dynamic JSON with normalized symbol. Use **Once Per Bar Close**.
Replace `YOUR_WEBHOOK_SECRET` in script settings or webhook headers.
Keep bot `TRADING_MODE=paper`.
