# fresh-wave-v7

Path B research wave (FROZEN 2026-09-07): RVI Signal, CHOP breakout, Elder Impulse — last Part B seats (B6–B8).

**RESEARCH ONLY** — no paper / alerts / webhook. BTC scoreboard + OOS stop-ladder on PASS_6m elder cells. Hold #15–#24 unmerged.

## IDs

| id | params | entry | exit | TF notes |
|----|--------|-------|------|----------|
| `rvi-signal-v1` | RVI(10) Signal(4) | crossover + RVI>0 | crossunder or RVI<0 | prefer 4h–1d; full 16 OK |
| `chop-breakout-v1` | CHOP(14); <38.2 allow; N=20 | close > prior 20-high + CHOP gate | prior 10-low or CHOP>61.8 | full 16; not Donchian; no ADX |
| `elder-impulse-v1` | EMA13 + MACD-hist | buy-stop prior high when not Red; cancel 2 | Red bar | prefer 4h–1d; no FI; no market-on-green |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v7
# optional: --prefer-coarse  --tfs 2d,1d,12h,4h  --refresh
```

Scoreboard: `results/fresh-wave-v7-scoreboard.md`

```bash
python -m backtest.path_b.fresh_wave_v7 --oos-ladder
```

OOS stop-ladder (PASS_6m elder cells only; hard-stop rvi/chop): `results/fresh-wave-v7-oos-ladder.md`
