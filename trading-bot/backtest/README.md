# Offline backtest: ema-rsi-trend-v1.1

Pure-Python, bar-close spot long-only backtest mirroring
[`strategies/ema-rsi-trend-v1.1.pine`](../strategies/ema-rsi-trend-v1.1.pine).
**No TradingView dependency.** Uses public Binance Spot klines via data-api.binance.vision (no API keys).

## Strategy Bot checklist

| # | Rule | How this backtest handles it |
|---|------|------------------------------|
| 1 | Bar-close only, no lookahead | Signals + fills at bar close; EMA/RSI use closed series |
| 2 | Pine v1.1 rules | EMA20/50 cross + RSI≥50 + close≥EMA50 buy; sell EMA crossunder OR RSI cross under 40; cooldown 6; BTC+ETH; no hard stop |
| 3 | Explicit fees/slippage | Default **0.1% fee/side** + **5 bps slippage** adverse vs close |
| 4 | Sell = full close | Entire long closed (not 2.5% clips) |
| 5 | Buy 2.5%; max pos 12%; max 4 opens | Buy sizes 2.5% equity; ≤1 open per symbol book; **daily halt not modeled** |
| 6 | Spot long-only | Spot engine only — not futures v1 |
| 7 | Report metrics + regime flags | See `results/ema-rsi-trend-v1.1.md` |

## How to re-run

```bash
cd trading-bot
source .venv/bin/activate
python -m backtest                  # ~2y BTCUSDT+ETHUSDT
python -m backtest --years 3 --refresh
python -m backtest --symbols BTCUSDT --fee 0.001 --slippage 0.0005
```

Outputs:

- `backtest/results/ema-rsi-trend-v1.1.md` (stable name)
- `backtest/results/ema-rsi-trend-v1.1_YYYYMMDD.md` (dated copy)
- OHLCV cache: `backtest/cache/*` (**gitignored**)

## Tests

```bash
cd trading-bot
pytest tests/test_backtest_signals.py tests/test_backtest_indicators.py -q
pytest -q
```

## Layout

| Module | Role |
|--------|------|
| `data.py` | Binance klines fetch + CSV cache |
| `indicators.py` | EMA / Wilder RSI / crossover (Pine-like) |
| `signals.py` | v1.1 raw + cooldown/position gates |
| `engine.py` | Spot long-only bar-close simulator |
| `metrics.py` | Win%, expectancy, DD, vs buy-hold, combine |
| `report.py` | Markdown writer + regime flags |
| `__main__.py` | CLI |

## Secrets

Never commit `.env`, `.webhook_secret`, or API keys. Cache CSVs are local-only.

## Related: jewel-strength-hold-v1 Path B

Separate research harness under [`jewel_replay/`](jewel_replay/) — CSV Slow/High replay
(V-zone + V-wide), synthetic fixture for CI. Not part of the ema-rsi Binance kline runner.
See [`../strategies/README-jewel-strength-hold-v1.md`](../strategies/README-jewel-strength-hold-v1.md).

