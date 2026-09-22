# Bostian III SMA Zero (Pine) — PAPER ONLY (LIVE OFF)

Pine Script strategy for paper-seat TradingView → bot webhooks. Authorized by CoS/Nuno based on the 2026-09-22 Path B Mode-A per-coin census and locked in `uploads/PAPER_PARAMS.md` and `uploads/007-paper-seats-tv-cutover-result.md`.

**Script:** [`bostian-iii-sma-zero.pine`](./bostian-iii-sma-zero.pine)  
**strategy_id:** `bostian-iii-sma-zero`  
**Status:** **PAPER ONLY / LIVE OFF** (never enable live API keys or LIVE trading)  
**Seat Allocation:** BTCUSDT only, **1,000 USDT paper equity allocation**.  
**Architecture:** Separate named paper strategy (do NOT combine with ETH seat).

---

## Census Performance (2026-09-22)

- **Pair:** BTCUSDT only
- **Timeframe:** 4h (Mode A)
- **Parameters:** `smaLen = 21` (`mode_a|(sma21)`) — **STRICT: 21 only (not sma34)**
- **Stage / PR:** Stage 17 (PR#45)
- **Trade count (n):** 40 (dense, passes `n >= 40` gate)
- **Win Rate:** 27.5%
- **Mode-A Return:** +14.29%
- **Buy & Hold:** +10.12%
- **×B&H:** **1.412×** (qualifies under per-coin gate `Mode-A >= 1.2× B&H` AND `n >= 40`)

---

## Rules & Sizing (Locked PAPER_PARAMS)

| Side | Logic | Webhook Sizing Rule |
|------|-------|---------------------|
| **Buy** | `ta.crossover(iiiS, 0)` AND `cooldownOk` | **OMIT `qty` / `qty_pct`** (bot defaults to `RISK_PER_TRADE_PCT` 2.5%) |
| **Sell** | `ta.crossunder(iiiS, 0)` AND `strategy.position_size > 0` | **`qty_pct: 12`** (clears max position; sells not capped by 2.5%) |

### Bostian Intraday Intensity Index (III) Formula
```pinescript
// Forbidden: CMF/OBV/CLV/AccDist labeled III
rng  = high - low
iii  = rng == 0 ? 0.0 : ((2.0 * close - high - low) / rng) * volume
iiiS = ta.sma(iii, 21)
```

- Bar close only (`process_orders_on_close = true`).
- Initial Capital in script: **1,000 USDT** per seat.
- Exits use **strategy() position / price** — does NOT read bot open-state.
- Webhook JSON from `alert()` **strips exchange prefix** (e.g. `BINANCE:`) so `symbol` is `BTCUSDT`-style.
- **Universe:** `BTCUSDT` ONLY at `4h` (no multi-coin fan-out).

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
   - Results in exact idempotency key: `bostian-iii-sma-zero-BTCUSDT-YYYY-MM-DDTHH:MM:SSZ-buy`.
3. **Price formatted as JSON number:**
   - In dynamic `alert()`, `price` is passed as a number via `str.tostring(close)`.

---

## cooldown_bars

- Input **Cooldown bars after exit** (default **6**, matching `ema-rsi` defaults).
- Counts bars **after an exit (SELL)** before a new **BUY / re-entry** is allowed.
- Set to **0** to disable. Does not apply after entries.

---

## Stops & Optional ATR Exit

- **Base census exit is signal-only:** `ta.crossunder(iiiS, 0)`.
- **Optional ATR `strategy.exit` included:** Script includes an optional ATR-based stop loss input (`useAtrExit = false` by default, length 14, multiple 3.0× ATR). Can be enabled in TradingView Strategy Tester.
- **A hard stop brief is required in a later brief before any real live trading.**

---

## TradingView Setup (Option B: Single alert() Call — Recommended)

1. Add the script to a **BTCUSDT** chart on the **4h** timeframe.
2. In Strategy Inputs:
   - Verify `III SMA Length = 21` (do not change to 34).
   - Paste Railway `WEBHOOK_SECRET` into **Webhook secret (runtime only - never publish)**.
3. Create **ONE** alert:
   - Condition: `Bostian III SMA Zero [PAPER ONLY - LIVE OFF]`
   - Selection: **alert() function calls only**
   - Webhook URL: `https://trading-bot-production-700a.up.railway.app/webhook/tradingview`
   - Name: `bostian-iii-sma21 BTCUSDT 4h paper (buy+sell)`
   - Message: Default (script generates dynamic JSON)
