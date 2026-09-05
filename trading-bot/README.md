# TradingView → Binance Spot Bot

FastAPI service that receives **TradingView alert webhooks**, validates signals, applies **balanced risk rules**, and places **Binance Spot** orders.

**Default mode is `paper` (dry-run):** intended orders are logged and tracked in memory — nothing is sent to Binance until you explicitly set `TRADING_MODE=live`.

> **EU / Belgium (MiCA):** Binance signup, deposits, or certain products may be restricted for residents in the EEA (including Belgium) under MiCA and local rules. Verify your eligibility and use a compliant venue if Binance is unavailable. This bot does not bypass geo or regulatory restrictions.

## Features

- TradingView JSON webhook endpoint with shared-secret auth
- Signal validation: symbol, side (`buy`/`sell`), optional `qty` or `qty_pct`, `strategy_id`
- Risk gates: per-trade %, max position %, max open positions, daily loss circuit breaker, allow-list
- Paper executor (default) and live Binance Spot MARKET orders via REST (`httpx`)
- Idempotent handling of duplicate `alert_id`s
- `/health` and `/trades` endpoints, structured JSON-ish logs

## Quick start (local)

```bash
cd trading-bot
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # edit WEBHOOK_SECRET; leave TRADING_MODE=paper
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
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
| `symbol` | yes | Pair, e.g. `BTCUSDT` (also accepts `BTC/USDT`) |
| `side` | yes | `buy` or `sell` |
| `qty` | no* | Absolute base-asset quantity |
| `qty_pct` | no* | % of equity to allocate (capped by risk rules) |
| `strategy_id` | no | Label for the strategy |
| `price` | recommended | Reference price (paper uses seeded mids if omitted) |
| `alert_id` | recommended | Idempotency key; auto-generated if missing |
| `secret` | if no header | Must match `WEBHOOK_SECRET` |

\*If both `qty` and `qty_pct` are omitted, size defaults to `RISK_PER_TRADE_PCT` of equity. Do not send both.

### Sample Pine alert message template

Paste into the TradingView alert **Message** box (adjust placeholders):

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

For sells, set `"side": "sell"`. Prefer a stable unique `alert_id` so retries are idempotent.

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
curl http://127.0.0.1:8000/trades
```

## Binance API keys

1. Create an API key on Binance **Spot** with **Enable Trading** only.
2. **Disable withdrawals** (and prefer IP allow-listing).
3. Put key/secret in `.env` as `BINANCE_API_KEY` / `BINANCE_API_SECRET`.
4. Keep `TRADING_MODE=paper` until you have verified sizing and risk behaviour.
5. To go live: set `TRADING_MODE=live` (and ensure keys are present). **Live trading can lose money.**

Never commit real keys. Do not invent placeholder live keys in git.

## Risk defaults (balanced)

| Variable | Default | Meaning |
|----------|---------|---------|
| `RISK_PER_TRADE_PCT` | `2.5` | Default notional % of equity per trade |
| `MAX_POSITION_PCT` | `12` | Cap per-symbol notional as % of equity |
| `MAX_OPEN_POSITIONS` | `4` | Max concurrent long symbols |
| `MAX_DAILY_LOSS_PCT` | `5` | Halt new buys after daily realized loss |
| `ALLOWED_SYMBOLS` | `BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT` | Allow-list |
| `TRADING_MODE` | `paper` | `paper` or `live` |
| `DEFAULT_QUOTE` | `USDT` | Quote asset |

Spot sells are only allowed against an open long (no naked shorts).

## Paper vs live

| Mode | Behaviour |
|------|-----------|
| `paper` (default) | Validates + risk-checks; logs order; updates in-memory portfolio; **no Binance call** |
| `live` | Same checks, then Spot MARKET order via signed REST |

## Tests

```bash
cd trading-bot
pip install -r requirements.txt
pytest -q
```

## Project layout

```
trading-bot/
  app/
    main.py           # FastAPI routes
    config.py         # Settings / env defaults
    models.py         # Pydantic schemas
    risk.py           # Risk engine + portfolio state
    executor.py       # Paper / live execution
    binance_client.py # Binance Spot REST
    idempotency.py    # Duplicate alert store
  tests/
  .env.example
  Dockerfile
  docker-compose.yml
  requirements.txt
  pyproject.toml
```

## Disclaimer

This software is for educational/automation purposes. Trading crypto is risky. You are responsible for compliance with local law (including MiCA in the EU), exchange ToS, and securing your secrets. Defaults favour paper trading for a reason.
