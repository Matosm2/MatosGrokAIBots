# fresh-wave-v1

Five **new** Path B research IDs × 16 TFs (BTCUSDT). Reuses `path_b/mtf_ohlcv` feed.

**LEAD gate:** 6m Mode-A ≥ 1.2× B&H. Also reports full(~2y). Costs 0.1%/side + 5 bps; Mode-A 100% + ops 2.5%.

```bash
cd trading-bot
PYTHONPATH=. python -m backtest.path_b.fresh_wave
```

Scoreboard: `results/fresh-wave-v1-scoreboard.md`
