# Research sketches — TV-free offline backtests

Strategy Bot research sketches. **Not wired to paper/live.** Does not touch
Jewel Pine or ema-rsi webhook wiring. Does **not** change live/paper bot defaults.

| ID | TF | Idea |
|----|----|------|
| `daily-adx-trend-hold-v1` | Daily | EMA50>EMA200 + ADX/DI trend hold |
| `macd-hist-regime-v1` | Daily | MACD hist cross above 0 + close>EMA100 |
| `htf-ema-pullback-wide-v1` | Daily bias + 4h entry | EMA pullback reclaim + 3×ATR stop |
| `close-above-ema20-hold-v1` | Daily | close>EMA20 + rising EMA20 (EMA20>EMA20[5]) |
| `donchian-20-10-spot-v1` | Daily | Donchian 20 breakout / 10 exit |

## Exact rules

### close-above-ema20-hold-v1
- **Entry:** close > EMA20 AND EMA20 > EMA20[5]
- **Exit:** close < EMA20
- **Optional ADX≥15:** OFF by default
- **No** EMA50>EMA200 filter

### donchian-20-10-spot-v1
- **Entry:** close > highest high of the **prior 20 bars** (excluding current) —
  classic Donchian upper-band breakout (`close > upper` built on prior highs)
- **Exit:** close < lowest low of the **prior 10 bars** (excluding current)

### daily-adx-trend-hold-v1
- **Entry:** EMA50 > EMA200 AND ADX(14) ≥ 25 AND +DI > −DI
- **Exit:** −DI > +DI OR ADX < 20 OR close < EMA200

### macd-hist-regime-v1
- **Entry:** MACD(12,26,9) histogram crosses above 0 AND close > EMA100
- **Exit:** histogram crosses below 0

### htf-ema-pullback-wide-v1 (documented interpretation)
- **Daily bias:** EMA50 > EMA200 on last fully closed daily bar
- **4h entry:** within lookback 5, low ≤ EMA50 (touch); close crosses above EMA20; close ≥ EMA50; bias on
- **Stop:** entry close − 3 × ATR(14) on 4h (checked on bar close)
- **Exit:** stop OR daily bias lost OR 4h close < EMA50

## Common simulation rules
- Symbols: BTCUSDT primary, ETHUSDT OOS (same params)
- Costs: **0.10%/side** + **5 bps** slip; full close; spot long-only; bar-close; no lookahead
- **Sizing (dual):**
  - **Mode A (gate):** **100% equity when in** — **only** this drives PASS/FAIL vs B&H
  - **Mode B (ops):** **2.5% equity** (Balanced) — parallel report column
- Data: Binance public klines via `data-api.binance.vision`
- Gate (6m): **PASS** iff n>0 AND WR ≥ 60% AND Mode A return > buy&hold

## How to re-run

```bash
cd trading-bot
source .venv/bin/activate
python -m backtest.sketches              # default: ema20 + donchian, 6m + ~2y, BTC+ETH
python -m backtest.sketches --no-2y      # 6m only
python -m backtest.sketches --refresh
python -m backtest.sketches --strategies close-above-ema20-hold-v1,donchian-20-10-spot-v1
```

Outputs under `backtest/sketches/results/`:
- `{strategy_id}.md` — per-strategy report + mandatory 6m dual-sizing gate table
- `ema20-donchian-gate-summary-6m.md` — summary for the run

## Tests

```bash
cd trading-bot
pytest tests/test_sketches_signals.py tests/test_backtest_indicators.py -q
pytest -q
```

## Layout

| Module | Role |
|--------|------|
| `ema20_hold.py` / `donchian_spot.py` | New dual-sizing sketches |
| `daily_adx.py` / `macd_hist.py` / `htf_pullback.py` | Earlier sketches |
| `engine.py` | Spot long-only + optional ATR stop |
| `report.py` | Dual-sizing gate tables + markdown |
| `__main__.py` | CLI |
| Extended `backtest/indicators.py` | ATR, ADX/DI, MACD, EMA |
