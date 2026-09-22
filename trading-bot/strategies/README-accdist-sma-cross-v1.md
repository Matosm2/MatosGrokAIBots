# AccDist SMA Cross v1 (Pine) — PAPER ONLY (LIVE OFF)

Pine Script strategy for paper-seat TradingView → bot webhooks. Authorized by CoS/Nuno based on the 2026-09-22 Path B Mode-A per-coin census and locked in `uploads/PAPER_PARAMS.md` and `uploads/007-paper-seats-tv-cutover-result.md`.

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

---

## TradingView Cutover Fixes (Claude TV Packet 007)

1. **Webhook Secret input (`webhookSecret`):**
   - TradingView webhooks cannot send custom HTTP headers (`X-Webhook-Secret`).
   - Added input `Webhook secret (runtime only - never publish)` (default empty).
   - When filled on-chart, script includes `,"secret":"<SECRET>"` in `alert()` JSON.
   - **Do NOT commit any real webhook secret in git.**
2. **Bar Time ISO-8601 formatting in Pine:**
   - `{{time}}` is NOT expanded inside Pine-built `alert()` strings.
   - Built via `barTimeIso = str.format_time(time, "yyyy-MM-dd'T'HH:mm:ss'Z'", "UTC")`.
   - Results in exact idempotency key: `accdist-sma-cross-v1-ETHUSDT-YYYY-MM-DDTHH:MM:SSZ-buy`.
3. **Price formatted as JSON number:**
   - In dynamic `alert()`, `price` is passed as a number via `str.tostring(close)`.

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

## TradingView Setup (Option B: Single alert() Call — Recommended)

1. Add the script to an **ETHUSDT** chart on the **4h** timeframe.
2. In Strategy Inputs:
   - Verify `ADL SMA Length = 50` (do not change to 65).
   - Paste Railway `WEBHOOK_SECRET` into **Webhook secret (runtime only - never publish)**.
3. Create **ONE** alert:
   - Condition: `AccDist SMA Cross v1 [PAPER ONLY - LIVE OFF]`
   - Selection: **alert() function calls only**
   - Webhook URL: `https://trading-bot-production-700a.up.railway.app/webhook/tradingview`
   - Name: `accdist-sma50 ETHUSDT 4h paper (buy+sell)`
   - Message: Default (script generates dynamic JSON)
