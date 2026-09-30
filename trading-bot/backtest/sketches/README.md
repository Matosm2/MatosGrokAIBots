# Research sketches — TV-free offline backtests

Three Strategy Bot research sketches. **Not wired to paper/live.** Does not touch
Jewel Pine or ema-rsi webhook wiring.

| ID | TF | Idea |
|----|----|------|
| `daily-adx-trend-hold-v1` | Daily | EMA50>EMA200 + ADX/DI trend hold |
| `macd-hist-regime-v1` | Daily | MACD hist cross above 0 + price>EMA100 |
| `htf-ema-pullback-wide-v1` | Daily bias + 4h entry | EMA pullback reclaim + 3×ATR stop |

## Exact rules

### daily-adx-trend-hold-v1
- **Entry:** EMA50 > EMA200 AND ADX(14) ≥ 25 AND +DI > −DI
- **Exit:** −DI > +DI OR ADX < 20 OR close < EMA200

### macd-hist-regime-v1
- **Entry:** MACD(12,26,9) histogram crosses above 0 AND close > EMA100
- **Exit:** histogram crosses below 0

### htf-ema-pullback-wide-v1 (documented interpretation)
- **Daily bias:** EMA50 > EMA200 on last fully closed daily bar (`close_time` before 4h `open_time`)
- **4h entry:** within lookback 5, low ≤ EMA50 (touch); close crosses above EMA20; close ≥ EMA50; bias on
- **Stop:** entry close − 3 × ATR(14) on 4h (checked on bar close)
- **Exit:** stop OR daily bias lost OR 4h close < EMA50

## Common simulation rules
- Symbols: BTCUSDT primary, ETHUSDT OOS (same params)
- Costs: **0.10%/side** + **5 bps** slip; size **2.5%** equity; full close
- Spot long-only; bar-close only; no lookahead
- Data: Binance public klines via `data-api.binance.vision`
- Gate (6m): **PASS** iff WR ≥ 60% AND strategy return > buy&hold

## How to re-run

```bash
cd trading-bot
source .venv/bin/activate
python -m backtest.sketches              # 6m + ~2y, BTC+ETH
python -m backtest.sketches --no-2y      # 6m only
python -m backtest.sketches --refresh
python -m backtest.sketches --strategies daily-adx-trend-hold-v1
```

Outputs under `backtest/sketches/results/`:
- `{strategy_id}.md` — per-strategy report + mandatory 6m gate table
- `sketches-gate-summary-6m.md` — all strategies × symbols

## Tests

```bash
cd trading-bot
pytest tests/test_sketches_signals.py tests/test_backtest_indicators.py -q
pytest -q
```

## Layout

| Module | Role |
|--------|------|
| `daily_adx.py` / `macd_hist.py` / `htf_pullback.py` | Signal logic |
| `engine.py` | Spot long-only + optional ATR stop |
| `report.py` | Gate tables + markdown |
| `__main__.py` | CLI |
| Extended `backtest/indicators.py` | ATR, ADX/DI, MACD |
