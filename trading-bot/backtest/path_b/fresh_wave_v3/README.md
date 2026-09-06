# fresh-wave-v3

Path B research wave: five new single-TF long-only IDs × 16 TFs = 80 BTCUSDT cells.

**RESEARCH ONLY** — no paper / alerts / webhook.

## IDs

| id | params | entry | exit |
|----|--------|-------|------|
| `donchian-breakout-v1` | entry20 / exit10 | close > prior 20-bar high | close < prior 10-bar low |
| `adx-dmi-trend-v1` | Wilder 14; ADX>25 | crossover(+DI, −DI) & ADX>25 | crossover(−DI, +DI) |
| `elder-ray-v1` | EMA13 | EMA↑ & Bear<0 & Bear↑ | Bear↓ OR EMA↓ |
| `tsi-momentum-v1` | TSI(25,13) / EMA7 | crossover(TSI,sig) & TSI>0 | crossunder OR TSI<0 |
| `schaff-stc-v1` | STC(23,50,10) | crossover(STC, 25) | crossunder(STC, 75) |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v3
python -m backtest.path_b.fresh_wave_v3 --oos-ladder
```

Scoreboard: `results/fresh-wave-v3-scoreboard.md`  
OOS ladder: `results/fresh-wave-v3-oos-ladder.md` (ETH→SOL→BNB on PASS_6m only; adx/elder/tsi not OOS'd)
