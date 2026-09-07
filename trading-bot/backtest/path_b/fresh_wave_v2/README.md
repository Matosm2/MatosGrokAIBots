# fresh-wave-v2

Path B research wave: five new single-TF long-only IDs × 16 TFs = 80 BTCUSDT cells.

**RESEARCH ONLY** — no paper / alerts / webhook. No OOS in this package (parent runs ETH→SOL→BNB after PASS_6m).

## IDs

| id | params | entry | exit |
|----|--------|-------|------|
| `psar-trend-v1` | AF 0.02/0.02/0.2 | close flips above SAR | close flips below SAR |
| `cci-mr-v1` | CCI(20, 0.015) | crossover(CCI, −100) | crossunder(CCI, +100) |
| `aroon-trend-v1` | length 25; Up≥70 | crossover(Up, Down) & Up≥70 | crossover(Down, Up) |
| `williams-r-mr-v1` | %R(14) | crossover(%R, −80) | crossunder(%R, −20) |
| `vortex-trend-v1` | Vortex(14) | crossover(VI+, VI−) | crossover(VI−, VI+) |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v2
python -m backtest.path_b.fresh_wave_v2 --oos-ladder
```

Scoreboard: `results/fresh-wave-v2-scoreboard.md`  
OOS ladder: `results/fresh-wave-v2-oos-ladder.md` (ETH→SOL→BNB on PASS_6m only)
