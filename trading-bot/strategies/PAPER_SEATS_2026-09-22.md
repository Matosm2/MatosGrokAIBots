# Paper Seats Handoff — 2026-09-22

**Status:** PAPER SEATS ONLY (LIVE OFF). Authorized by Nuno via CoS 2026-09-22 (`uploads/PAPER_KICK.md`, `uploads/PAPER_PARAMS.md`, `uploads/007-paper-seats-tv-cutover-result.md`).  
**Path B Research Status:** HARD STOP stays — do not resume Stage-32 / Stage-33 / Track B CK. HOLD research PRs (#60 etc.).  
**Architecture:** Two **separate named paper strategies** (do NOT combine into one bot).

---

## 1. Executive Summary & Authorized Paper Seats

The 2026-09-22 Mode-A per-coin census (`uploads/per-coin-census-2026-09-22.md`), `uploads/PAPER_KICK.md`, and `uploads/PAPER_PARAMS.md` confirmed:
- **Full-ladder PASS count:** 0 (no strategy cleared BTC→ETH→SOL→BNB all at ≥1.2× B&H).
- **Per-coin eligibility gate:** `Mode-A >= 1.2× B&H` on that coin AND dense `n >= 40`.
- **Authorized seats:** Exactly two separate seats qualified across all 30 stages:
  1. **BTCUSDT Seat:** `bostian-iii-sma-zero` @ **4h** (`smaLen=21` ONLY, not 34) — **1.412× B&H**, **n=40** (Stage 17, PR#45)
  2. **ETHUSDT Seat:** `accdist-sma-cross-v1` @ **4h** (`smaLen=50` ONLY, not 65) — **1.850× B&H**, **n=46** (Stage 1, PR#29)
  3. **SOLUSDT / BNBUSDT:** 0 eligible (no strategy achieved ≥1.2× with n≥40). No seats allocated.
- **Paper Capital Allocation:** **1,000 USDT per seat** (separate paper book allocations).
- **Balanced Risk Defaults (Locked):**
  - Buys: **OMIT `qty` / `qty_pct`** → bot uses `RISK_PER_TRADE_PCT = 2.5%`
  - Sells: **`qty_pct = 12`** → clears max position (sells not capped by 2.5%)
  - Max open positions: **4**
  - Daily loss halt: **5.0%**
  - No overrides.

---

## 2. TradingView Cutover Fixes (Claude TV Packet 007)

During the on-chart TradingView cutover (Packet 007), Claude identified two critical runtime constraints in TradingView that were fixed on-chart and are now ported into the codebase:

1. **Webhook Secret via JSON Body (TV Header Limitation):**
   - TradingView alert webhooks **cannot send custom HTTP headers** (no support for `X-Webhook-Secret`).
   - The bot server (`trading-bot/app/main.py`) validates secrets via header (`x_webhook_secret`) OR body (`alert.secret`).
   - Fix: Added script input `webhookSecret = input.string("", "Webhook secret (runtime only - never publish)")`.
   - Default is empty string `""` in git (NEVER commit secrets).
   - When filled on-chart by the operator (Nuno), the script dynamically appends `,"secret":"<WEBHOOK_SECRET>"` to the `alert()` JSON payload.
2. **Bar Time ISO-8601 Formatted in Pine (`{{time}}` Placeholder Limitation):**
   - TradingView `{{time}}` and `{{close}}` placeholders are **NOT interpolated** inside Pine-constructed strings passed to `alert()`; they only work in manual alert dialog message boxes.
   - If unhandled, `alert_id` would literally contain `"{{time}}"`, causing all alerts to collide after the first bar under the 24h idempotency store.
   - Fix: Built bar-open time in Pine using `barTimeIso = str.format_time(time, "yyyy-MM-dd'T'HH:mm:ss'Z'", "UTC")`.
   - This generates clean idempotency keys like `bostian-iii-sma-zero-BTCUSDT-2026-09-22T00:00:00Z-buy`.
3. **Price Formatting as JSON Number:**
   - In dynamic `alert()` payloads, price is output as a numeric JSON value via `str.tostring(close)` rather than a quoted placeholder string.

---

## 3. Seat Matrix & Parameters

| Parameter | Seat 1: BTCUSDT | Seat 2: ETHUSDT |
| :--- | :--- | :--- |
| **Strategy Name** | Bostian III SMA Zero | AccDist SMA Cross v1 |
| **Strategy ID** | `bostian-iii-sma-zero` | `accdist-sma-cross-v1` |
| **Pine Script** | [`bostian-iii-sma-zero.pine`](./bostian-iii-sma-zero.pine) | [`accdist-sma-cross-v1.pine`](./accdist-sma-cross-v1.pine) |
| **Symbol** | `BTCUSDT` **only** (no fan-out; TV `BINANCE:BTCUSDT`) | `ETHUSDT` **only** (no fan-out; TV `BINANCE:ETHUSDT`) |
| **Chart Timeframe** | **240 (4h)** | **240 (4h)** |
| **Paper Allocation** | **1,000 USDT** | **1,000 USDT** |
| **Core Indicator** | Bostian Intraday Intensity Index (III) | Raw Accumulation/Distribution (ADL) |
| **Core Formula** | `rng = high - low`<br>`iii = rng == 0 ? 0.0 : ((2*close-high-low)/rng)*volume`<br>`iiiS = ta.sma(iii, 21)` | `adl = ta.accdist`<br>`sig = ta.sma(adl, 50)`<br>*(Raw ADL vs SMA — NOT Chaikin Osc)* |
| **Forbidden Proxies** | CMF, OBV, CLV, AccDist labeled III | CMF, OBV, Chaikin Osc EMA3-EMA10(ADL) |
| **Primary Param** | `smaLen = 21` **ONLY** (not 34) | `smaLen = 50` **ONLY** (not 65) |
| **Entry Condition** | `ta.crossover(iiiS, 0)` closed-bar AND `cooldownOk` | `ta.crossover(adl, sig)` closed-bar AND `cooldownOk` |
| **Exit Condition** | `ta.crossunder(iiiS, 0)` + optional ATR `strategy.exit` | `ta.crossunder(adl, sig)` + optional ATR `strategy.exit` |
| **Buy Sizing** | **OMIT `qty`/`qty_pct`** (bot defaults to 2.5% risk) | **OMIT `qty`/`qty_pct`** (bot defaults to 2.5% risk) |
| **Sell Sizing** | **`qty_pct: 12`** (clears max position) | **`qty_pct: 12`** (clears max position) |
| **Cooldown Bars** | **6** bars after exit (0 disables) | **6** bars after exit (0 disables) |
| **Pyramiding** | 0 | 0 |
| **Order Execution** | `process_orders_on_close = true` | `process_orders_on_close = true` |
| **Commission Model** | 0.1% | 0.1% |
| **Hard Stop** | Signal exit (crossunder); optional ATR exit in Pine; live needs later stop brief | Signal exit (crossunder); optional ATR exit in Pine; live needs later stop brief |
| **Alert ID Shape** | `bostian-iii-sma-zero-BTCUSDT-{ISO_TIME}-buy`<br>`bostian-iii-sma-zero-BTCUSDT-{ISO_TIME}-sell` | `accdist-sma-cross-v1-ETHUSDT-{ISO_TIME}-buy`<br>`accdist-sma-cross-v1-ETHUSDT-{ISO_TIME}-sell` |

---

## 4. Webhook Endpoint & Deployment Configuration

- **Railway Webhook URL:** `https://trading-bot-production-700a.up.railway.app/webhook/tradingview`
- **Path:** `/webhook/tradingview`
- **Method:** `POST`
- **Auth:** Body `"secret":"..."` (via Pine chart input) or header `X-Webhook-Secret`
- **Bar Trigger:** **Once Per Bar Close**

---

## 5. TradingView Alert Setup

### Option B: Single Strategy `alert()` Call (Recommended & On-Chart Setup)
Only **1 alert per coin** (2 alerts total across the paper universe):
1. In TradingView layout, open Strategy **Settings -> Inputs**.
2. Paste Railway `WEBHOOK_SECRET` into **Webhook secret (runtime only - never publish)**.
3. Click **Create Alert**:
   - **Condition:** Select strategy (`bostian-iii-sma21` or `accdist-sma50`)
   - **Option:** `alert() function calls only`
   - **Webhook URL:** `https://trading-bot-production-700a.up.railway.app/webhook/tradingview`
   - **Message:** Default (Pine script builds dynamic JSON)
   - **Name:** `bostian-iii-sma21 BTCUSDT 4h paper (buy+sell)` / `accdist-sma50 ETHUSDT 4h paper (buy+sell)`

#### Dynamic Payload Generated by Script (Seat 1: BTCUSDT):
- **Buy:**
  ```json
  {"symbol":"BTCUSDT","side":"buy","strategy_id":"bostian-iii-sma-zero","price":64500.12,"alert_id":"bostian-iii-sma-zero-BTCUSDT-2026-09-22T00:00:00Z-buy","secret":"YOUR_SECRET"}
  ```
- **Sell:**
  ```json
  {"symbol":"BTCUSDT","side":"sell","qty_pct":12,"strategy_id":"bostian-iii-sma-zero","price":65100.50,"alert_id":"bostian-iii-sma-zero-BTCUSDT-2026-09-22T04:00:00Z-sell","secret":"YOUR_SECRET"}
  ```

#### Dynamic Payload Generated by Script (Seat 2: ETHUSDT):
- **Buy:**
  ```json
  {"symbol":"ETHUSDT","side":"buy","strategy_id":"accdist-sma-cross-v1","price":3450.25,"alert_id":"accdist-sma-cross-v1-ETHUSDT-2026-09-22T00:00:00Z-buy","secret":"YOUR_SECRET"}
  ```
- **Sell:**
  ```json
  {"symbol":"ETHUSDT","side":"sell","qty_pct":12,"strategy_id":"accdist-sma-cross-v1","price":3500.80,"alert_id":"accdist-sma-cross-v1-ETHUSDT-2026-09-22T04:00:00Z-sell","secret":"YOUR_SECRET"}
  ```

---

### Option A: Manual alertcondition Templates (Alternative)
If using separate manual alerts via `alertcondition()`:

#### Seat 1: BTCUSDT — `bostian-iii-sma-zero`
- **Buy:**
```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "strategy_id": "bostian-iii-sma-zero",
  "price": "{{close}}",
  "alert_id": "bostian-iii-sma-zero-BTCUSDT-{{time}}-buy",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```
- **Sell:**
```json
{
  "symbol": "BTCUSDT",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "bostian-iii-sma-zero",
  "price": "{{close}}",
  "alert_id": "bostian-iii-sma-zero-BTCUSDT-{{time}}-sell",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

#### Seat 2: ETHUSDT — `accdist-sma-cross-v1`
- **Buy:**
```json
{
  "symbol": "ETHUSDT",
  "side": "buy",
  "strategy_id": "accdist-sma-cross-v1",
  "price": "{{close}}",
  "alert_id": "accdist-sma-cross-v1-ETHUSDT-{{time}}-buy",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```
- **Sell:**
```json
{
  "symbol": "ETHUSDT",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "accdist-sma-cross-v1",
  "price": "{{close}}",
  "alert_id": "accdist-sma-cross-v1-ETHUSDT-{{time}}-sell",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

---

## 6. LIVE OFF Safety Verification Checklist & Rules

Before attaching TradingView webhooks or booting trading bot instances:

- [ ] **TRADING_MODE Verification:** Confirm `TRADING_MODE=paper` is set in the bot environment / Railway environment variables.
- [ ] **No Live API Keys:** Confirm `BINANCE_API_KEY` and `BINANCE_API_SECRET` are empty or omitted.
- [ ] **Webhook Secret Configured On-Chart:** Paste `WEBHOOK_SECRET` in chart inputs only. Never commit secret into git.
- [ ] **Separate Named Strategies:** Ensure BTC and ETH strategies run as distinct, decoupled paper seats (do NOT combine).
- [ ] **Single Symbol Lock:**
  - BTCUSDT chart is connected ONLY to `bostian-iii-sma-zero` alerts.
  - ETHUSDT chart is connected ONLY to `accdist-sma-cross-v1` alerts.
- [ ] **Timeframe Lock:** Both charts strictly set to **4h** timeframe.
- [ ] **Parameter Lock:**
  - BTC: `smaLen = 21` ONLY (sma34 strictly rejected).
  - ETH: `smaLen = 50` ONLY (sma65 strictly rejected).
- [ ] **Equity Baseline:** Initialize paper portfolio at **1,000 USDT per seat**.
- [ ] **Balanced Sizing Verification:**
  - Buy alert JSON omits `qty`/`qty_pct` → verified bot allocates 2.5% risk.
  - Sell alert JSON specifies `qty_pct: 12` → verified bot clears entire position.
- [ ] **Bar Close Trigger:** All alerts set strictly to **Once Per Bar Close**.
- [ ] **Alert ID Pattern:** Verified pattern `{strategy_id}-{SYMBOL}-{time}-{buy|sell}` with ISO-8601 bar-open time.
- [ ] **Stop Brief Gate:** Real LIVE execution is strictly gated pending a future stop brief.
- [ ] **Path B Freeze / HOLD Research PRs:** Research freeze in effect. Research PRs (#60 etc.) remain on hold while paper seats run.
- [ ] **Reporting Channel:** On live heartbeat, report seat name, symbol, paper equity start, and deploy URL/ID directly to **Strategy + CoS only** (no Nuno DM).
