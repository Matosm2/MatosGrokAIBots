# AccDist SMA Cross v1 (Pine) — PAPER ONLY (LIVE OFF)

Pine Script strategy for paper-seat TradingView → bot webhooks. Authorized by CoS/Nuno based on the 2026-09-22 Path B Mode-A per-coin census and locked in `uploads/PAPER_PARAMS.md`.

**Script:** [`accdist-sma-cross-v1.pine`](./accdist-sma-cross-v1.pine)  
**strategy_id:** `accdist-sma-cross-v1`  
**Status:** **PAPER ONLY / LIVE OFF** (never enable live API keys or LIVE trading)  
**Seat Allocation:** ETHUSDT only, **1,000 USDT paper equity allocation**.  
**Architecture:** Separate named paper strategy (do NOT combine with BTC seat).

---

## Census Performance (2026-09-22)

- **Pair:** ETHUSDT only
- **Timeframe:** 4h (Mode A)
- **Parameters:** `smaLen = 50` (`mode_a|sma50`) — **STRICT: 50 only (not sma65)**
- **Stage / PR:** Stage 1 (PR#29)
- **Trade count (n):** 46 (dense, passes `n >= 40` gate)
- **Win Rate:** 21.7%
- **Mode-A Return:** +19.67%
- **Buy & Hold:** +10.63%
- **×B&H:** **1.850×** (qualifies under per-coin gate `Mode-A >= 1.2× B&H` AND `n >= 40`)

---

## Rules & Sizing (Locked PAPER_PARAMS)

| Side | Logic | Webhook Sizing Rule |
|------|-------|---------------------|
| **Buy** | `ta.crossover(adl, adlSma)` AND `cooldownOk` | **OMIT `qty` / `qty_pct`** (bot defaults to `RISK_PER_TRADE_PCT` 2.5%) |
| **Sell** | `ta.crossunder(adl, adlSma)` AND `strategy.position_size > 0` | **`qty_pct: 12`** (clears max position; sells not capped by 2.5%) |

### Raw Accumulation/Distribution (ADL) Formula
```pinescript
// NOTE: Raw ADL vs SMA, NOT Chaikin Oscillator!
// Forbidden: CMF/OBV/Chaikin Osc EMA3-EMA10(ADL) labeled ADL
adl    = ta.accdist
adlSma = ta.sma(adl, 50)
```

- Bar close only (`process_orders_on_close = true`).
- Initial Capital in script: **1,000 USDT** per seat.
- Exits use **strategy() position / price** — does NOT read bot open-state.
- Webhook JSON from `alert()` **strips exchange prefix** (e.g. `BINANCE:`) so `symbol` is `ETHUSDT`-style.
- **Universe:** `ETHUSDT` ONLY at `4h` (no multi-coin fan-out).
- **`alert_id` exact shape:** `accdist-sma-cross-v1-ETHUSDT-{{time}}-buy` and `accdist-sma-cross-v1-ETHUSDT-{{time}}-sell`. Uses **`{{time}}`**, NOT `{{timenow}}`.
- **Secret:** No embedded secret in committed Pine. Header `X-Webhook-Secret` preferred; Trading wires secret at runtime.

---

## cooldown_bars

- Input **Cooldown bars after exit** (default **6**, matching `ema-rsi` defaults).
- Counts bars **after an exit (SELL)** before a new **BUY / re-entry** is allowed.
- Set to **0** to disable. Does not apply after entries.

---

## Stops & Optional ATR Exit

- **Base census exit is signal-only:** `ta.crossunder(adl, adlSma)`.
- **Optional ATR `strategy.exit` included:** Script includes an optional ATR-based stop loss input (`useAtrExit = false` by default, length 14, multiple 3.0× ATR). Can be enabled in TradingView Strategy Tester.
- **A hard stop brief is required in a later brief before any real live trading.**

---

## TradingView setup (two alerts)

1. Add the script to an **ETHUSDT** chart on the **4h** timeframe.
2. Verify inputs: `ADL SMA Length = 50` (do not change to 65), `Cooldown bars after exit = 6`, `Sell qty_pct = 12.0`, `strategy_id = accdist-sma-cross-v1`.
3. Create **two** alerts (Once Per Bar Close):

### Option A — alertconditions (recommended for two named alerts)

#### Alert 1 — Buy
- Condition: **AccDist SMA50 Buy**
- Trigger: **Once Per Bar Close**
- Webhook URL: `https://YOUR_RAILWAY_APP.up.railway.app/webhook/tradingview`
- Headers: `X-Webhook-Secret: YOUR_WEBHOOK_SECRET`
- Message (omits `qty`/`qty_pct` so bot sizes to 2.5% Balanced risk):
```json
{
  "symbol": "ETHUSDT",
  "side": "buy",
  "strategy_id": "accdist-sma-cross-v1",
  "price": "{{close}}",
  "alert_id": "accdist-sma-cross-v1-ETHUSDT-{{time}}-buy"
}
```

#### Alert 2 — Sell
- Condition: **AccDist SMA50 Sell**
- Trigger: **Once Per Bar Close**
- Webhook URL: `https://YOUR_RAILWAY_APP.up.railway.app/webhook/tradingview`
- Headers: `X-Webhook-Secret: YOUR_WEBHOOK_SECRET`
- Message:
```json
{
  "symbol": "ETHUSDT",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "accdist-sma-cross-v1",
  "price": "{{close}}",
  "alert_id": "accdist-sma-cross-v1-ETHUSDT-{{time}}-sell"
}
```

### Option B — single “Any alert() function call”
Uses Pine-built dynamic JSON with normalized symbol. Use **Once Per Bar Close**.
Authenticate via `X-Webhook-Secret` header or configure webhook secret in bot environment.
Keep bot `TRADING_MODE=paper`.
