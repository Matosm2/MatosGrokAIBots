# TradingView → Binance Spot Bot

FastAPI service that receives **TradingView alert webhooks**, validates signals, applies **balanced risk rules**, and places **Binance Spot** orders.

**Default mode is `paper` (dry-run):** intended orders are logged and tracked (optionally persisted under `DATA_DIR`) — nothing is sent to Binance until you explicitly set `TRADING_MODE=live`.

> **EU / Belgium (MiCA):** Binance signup, deposits, or certain products may be restricted for residents in the EEA (including Belgium) under MiCA and local rules. Verify your eligibility and use a compliant venue if Binance is unavailable. This bot does not bypass geo or regulatory restrictions.

## Features

- TradingView JSON webhook endpoint with shared-secret auth
- Signal validation: symbol (strips `BINANCE:` etc.), side (`buy`/`sell`), optional `qty` / `qty_pct` / `close_all`, `strategy_id`
- Risk gates: per-trade % (buys only), max position %, max open positions, daily loss circuit breaker (buys halted; sells still allowed), allow-list
- Paper executor (default) with meaningful cash/equity/realized PnL; live Spot MARKET orders via REST (`httpx`) with LOT_SIZE / minNotional rounding and live balance sync
- Idempotent `alert_id` handling with claim/commit/abort (failed live orders are **not** marked duplicate)
- Public `/livez` for Docker/K8s liveness; authenticated `/health` and `/trades` (webhook secret header)
- Paper **dashboard** at `/dashboard` (login form → HttpOnly session cookie; secret never in the URL)
- Fail-closed startup if `WEBHOOK_SECRET` is default/insecure when `TRADING_MODE=live`, absolute `DATA_DIR` (e.g. `/data`), or `PAPER_REQUIRE_STRONG_SECRET=1`

## Quick start (local)

```bash
cd trading-bot
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # edit WEBHOOK_SECRET; leave TRADING_MODE=paper
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Liveness (no auth — used by Docker healthcheck):

```bash
curl http://127.0.0.1:8000/livez
```

Detailed health (requires secret header):

```bash
curl -H 'X-Webhook-Secret: change-me-to-a-long-random-string' http://127.0.0.1:8000/health
```

### Docker

```bash
cd trading-bot
cp .env.example .env
docker compose up --build
```

## TradingView alert setup

1. Deploy this service to a public HTTPS URL (or use a tunnel like ngrok for testing).
2. In TradingView: **Alerts → Notifications → Webhook URL**  
   `https://YOUR_HOST/webhook/tradingview`
3. Set the alert **Message** to a JSON payload (see template below).
4. Pass the secret either:
   - Header `X-Webhook-Secret: <WEBHOOK_SECRET>`, or
   - JSON field `"secret": "<WEBHOOK_SECRET>"` in the message body.

### JSON payload schema

| Field | Required | Description |
|-------|----------|-------------|
| `symbol` | yes | Pair, e.g. `BTCUSDT` (also `BTC/USDT`, `BINANCE:BTCUSDT`) |
| `side` | yes | `buy` or `sell` |
| `qty` | no* | Absolute base-asset quantity (buys trimmed to `RISK_PER_TRADE_PCT`) |
| `qty_pct` | no* | % of equity to allocate. **Sells are not capped by `RISK_PER_TRADE_PCT`** (e.g. `12` to exit a max-sized long) |
| `close_all` | no | `true` on sell → close entire open long |
| `strategy_id` | no | Label for the strategy |
| `price` | recommended | Reference price (paper uses seeded mids if omitted) |
| `alert_id` | recommended | Idempotency key; use `{{time}}` (not `{{timenow}}`); auto-generated if missing |
| `secret` | if no header | Must match `WEBHOOK_SECRET` |

\*If both `qty` and `qty_pct` are omitted, size defaults to `RISK_PER_TRADE_PCT` of equity. Do not send both.

### Sample Pine alert message template

Paste into the TradingView alert **Message** box (adjust placeholders). Use **`{{time}}`**, not `{{timenow}}`:

```json
{
  "symbol": "{{ticker}}",
  "side": "buy",
  "qty_pct": 2.5,
  "strategy_id": "my-pine-strategy",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-buy",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

Sell example (partial/full exit — **not** truncated to 2.5% risk):

```json
{
  "symbol": "{{ticker}}",
  "side": "sell",
  "qty_pct": 12,
  "strategy_id": "my-pine-strategy",
  "price": {{close}},
  "alert_id": "{{ticker}}-{{time}}-sell",
  "secret": "YOUR_WEBHOOK_SECRET"
}
```

Prefer a stable unique `alert_id` so retries are idempotent.

### Manual test (paper)

```bash
curl -s -X POST http://127.0.0.1:8000/webhook/tradingview \
  -H 'Content-Type: application/json' \
  -H 'X-Webhook-Secret: change-me-to-a-long-random-string' \
  -d '{
    "symbol": "BTCUSDT",
    "side": "buy",
    "price": 60000,
    "strategy_id": "manual-test",
    "alert_id": "manual-1"
  }'
```

List recent trades:

```bash
curl -H 'X-Webhook-Secret: change-me-to-a-long-random-string' http://127.0.0.1:8000/trades
```


## Paper dashboard

Open `http://127.0.0.1:8000/dashboard` (or your deployed HTTPS host).

1. Enter the same `WEBHOOK_SECRET` used for TradingView alerts.
2. The secret is POSTed once; the server sets an **HttpOnly** `dashboard_session` cookie (HMAC of the secret — the raw secret is not kept in the cookie or query string). On HTTPS (including behind Railway via `X-Forwarded-Proto`), the cookie also gets the **Secure** flag (`ProxyHeadersMiddleware`).
3. The page shows **mode**, **equity**, **cash**, **open positions**, **daily PnL**, **last alert**, and a **trade log**.

`POST /dashboard/login` has a simple **in-memory rate limit** (10 attempts / 60s per client IP). It is per-process and resets on restart — adequate for paper; not a substitute for edge WAF on a high-traffic host.

Log out via the button (clears the cookie). Keep `TRADING_MODE=paper` unless you intentionally go live.


### Paper portfolio reset

If `DATA_DIR` has an old `portfolio.json` (e.g. ~10k equity) after changing `PAPER_EQUITY_USDT`, either:

1. **Preferred:** `POST /paper/reset` with header `X-Webhook-Secret` (paper mode only) — sets equity/cash to `PAPER_EQUITY_USDT`, clears positions and in-memory trade log, rewrites `portfolio.json`.
2. **Ops:** delete `/data/portfolio.json` on the volume and restart (idempotency file can stay).

## Durable deploy (Railway preferred)

Do **not** keep relying on an ephemeral Cloudflare tunnel for production paper alerts. Deploy once, get a stable HTTPS URL, then point TradingView at it.

### Required environment variables

| Variable | Required | Notes |
|----------|----------|-------|
| `WEBHOOK_SECRET` | **yes** | Long random string; used by TV webhook + dashboard login |
| `TRADING_MODE` | yes | Keep **`paper`** (default). Never set `live` until keys + risk review |
| `PAPER_EQUITY_USDT` | recommended | Starting paper equity (default `10000`) |
| `DATA_DIR` | recommended | Persist portfolio/idempotency — use `/data` with a volume (**attach in Railway UI**; `railway.toml` does not create it) |
| `PAPER_REQUIRE_STRONG_SECRET` | optional | `1`/`true` → refuse default `WEBHOOK_SECRET` even in paper (also auto when `DATA_DIR` is absolute, e.g. `/data`) |
| `ALLOWED_SYMBOLS` | optional | Default BTC/ETH/SOL/BNB USDT |
| `RISK_PER_TRADE_PCT` / `MAX_POSITION_PCT` / `MAX_OPEN_POSITIONS` / `MAX_DAILY_LOSS_PCT` | optional | See risk table below |
| `BINANCE_API_KEY` / `BINANCE_API_SECRET` | live only | Leave empty in paper |
| `PORT` | platform | Railway injects this; Dockerfile/`Procfile` honour it |
| `LOG_LEVEL` | optional | Default `INFO` |

### Railway (Docker)

1. Create a Railway project and connect this GitHub repo.
2. Set the service **root directory** to `trading-bot` (monorepo) **or** deploy from a repo that contains the Dockerfile at the root.
3. `railway.toml` uses the Dockerfile builder and healthchecks `/livez`.
4. **Volume (manual):** `railway.toml` does **not** create a volume. In the Railway UI, attach a **persistent volume** mounted at `/data`, then set `DATA_DIR=/data`. Without this, portfolio/idempotency state is ephemeral across restarts.
5. Set env vars from the table above (`TRADING_MODE=paper`, **strong** `WEBHOOK_SECRET`, etc.). With `DATA_DIR=/data`, a default/weak secret fails closed at startup.
6. Deploy. Note the public HTTPS URL, e.g. `https://YOUR_SERVICE.up.railway.app`.
7. Verify:
   - `curl https://YOUR_HOST/livez` → `{"status":"ok"}`
   - Open `https://YOUR_HOST/dashboard` and sign in with `WEBHOOK_SECRET`

CLI (optional, if already logged in):

```bash
cd trading-bot
# railway login   # only if needed
railway up
```

### Docker / Compose

```bash
cd trading-bot
cp .env.example .env   # set WEBHOOK_SECRET; keep TRADING_MODE=paper
docker compose up --build -d
```

Compose mounts a named volume at `/data` (`DATA_DIR=/data`). Image `HEALTHCHECK` probes `/livez`.

### Cut over TradingView webhooks (tunnel → stable URL)

After deploy:

1. In TradingView, open each alert that still points at a Cloudflare tunnel / ngrok URL.
2. Change **Webhook URL** to: `https://YOUR_STABLE_HOST/webhook/tradingview`
3. Keep the JSON **Message** body (including `"secret"`) unchanged, **or** keep using header auth if your TV plan supports custom headers.
4. Fire a test alert (or use the manual `curl` below against the new host).
5. Confirm on `/dashboard` (last alert + trade log) and/or `GET /trades` with `X-Webhook-Secret`.
6. Disable/stop the old tunnel so you do not double-process alerts.

Until cutover is done, leave the tunnel running only if you still need it; prefer completing cutover in one sitting.

## Binance API keys

1. Create an API key on Binance **Spot** with **Enable Trading** only.
2. **Disable withdrawals** (and prefer IP allow-listing).
3. Put key/secret in `.env` as `BINANCE_API_KEY` / `BINANCE_API_SECRET`.
4. Keep `TRADING_MODE=paper` until you have verified sizing and risk behaviour.
5. To go live: set a **strong** `WEBHOOK_SECRET`, then `TRADING_MODE=live`. Live refuses default secrets. **Live trading can lose money.**

Never commit real keys. Do not invent placeholder live keys in git.

## Risk defaults (balanced)

| Variable | Default | Meaning |
|----------|---------|---------|
| `RISK_PER_TRADE_PCT` | `2.5` | Cap / default notional % of equity **per buy** (sells exempt) |
| `MAX_POSITION_PCT` | `12` | Cap per-symbol notional as % of equity |
| `MAX_OPEN_POSITIONS` | `4` | Max concurrent long symbols |
| `MAX_DAILY_LOSS_PCT` | `5` | Halt **new buys** after daily realized loss; sells/closes still allowed |
| `ALLOWED_SYMBOLS` | `BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT` | Allow-list |
| `TRADING_MODE` | `paper` | `paper` or `live` |
| `DEFAULT_QUOTE` | `USDT` | Quote asset |
| `DATA_DIR` | `data` | Portfolio + idempotency persistence (empty = memory only) |

Spot sells are only allowed against an open long (no naked shorts). Sell size is `min(requested, open_qty)` and is **never** reduced by `RISK_PER_TRADE_PCT`.

## Paper vs live

| Mode | Behaviour |
|------|-----------|
| `paper` (default) | Validates + risk-checks; logs order; updates cash/equity/realized PnL; **no Binance call** |
| `live` | Syncs free balances from Binance for sizing; LOT_SIZE/minNotional; Spot MARKET order; failed orders not idempotent |

## Tests

```bash
cd trading-bot
pip install -r requirements.txt
pytest -q
```

## Pine strategies

See [`strategies/`](./strategies/) for TradingView Pine scripts (e.g. EMA RSI Trend v1.1) and alert webhook templates.

## Project layout

```
trading-bot/
  app/
    main.py           # FastAPI routes + lifespan
    dashboard.py      # /dashboard login + HTML UI
    deps.py           # Shared auth / runtime deps
    config.py         # Settings / env defaults
    models.py         # Pydantic schemas
    risk.py           # Risk engine + portfolio state
    executor.py       # Paper / live execution
    binance_client.py # Binance Spot REST + filters
    idempotency.py    # Duplicate alert store
    persistence.py    # JSON portfolio / idempotency persistence
  strategies/         # Optional Pine scripts (separate PRs)
  tests/
  .env.example
  Dockerfile          # uvicorn + /livez HEALTHCHECK + /data volume
  docker-compose.yml
  railway.toml
  Procfile
  requirements.txt
  pyproject.toml
```

## Disclaimer

This software is for educational/automation purposes. Trading crypto is risky. You are responsible for compliance with local law (including MiCA in the EU), exchange ToS, and securing your secrets. Defaults favour paper trading for a reason.

## Offline backtest (ema-rsi-trend-v1.1)

Pure-Python bar-close backtest of the Pine strategy (no TradingView). Fetches public Binance Spot 1h klines, caches under `backtest/cache/`, writes markdown results.

```bash
cd trading-bot
source .venv/bin/activate
python -m backtest --years 2
pytest tests/test_backtest_signals.py tests/test_backtest_indicators.py -q
```

See [`backtest/README.md`](backtest/README.md). Results: [`backtest/results/ema-rsi-trend-v1.1.md`](backtest/results/ema-rsi-trend-v1.1.md).
Defaults: fee 0.1%/side, slippage 5 bps, buy `qty_pct` 2.5, `cooldown_bars` 6.
**Daily loss halt is not modeled offline.** Spot long-only — not futures v1.

