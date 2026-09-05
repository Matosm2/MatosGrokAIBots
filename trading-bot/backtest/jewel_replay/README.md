# jewel_replay — Path B research harness

Offline CSV replay for **`jewel-strength-hold-v1`**. Separate from the ema-rsi
`backtest/` signal stack; reuses only shared helpers (e.g. `max_drawdown_pct`).

See [`../../strategies/README-jewel-strength-hold-v1.md`](../../strategies/README-jewel-strength-hold-v1.md).

```bash
cd trading-bot
python -m backtest.jewel_replay backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv
pytest tests/test_jewel_replay.py -q
```
