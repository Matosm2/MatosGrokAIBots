# fresh-wave-v4

Path B research wave: Ehlers Fisher (16 TF) + Coppock (1d/2d) + UTC midnight ORB (1 cell).

**RESEARCH ONLY** — no paper / alerts / webhook. No OOS in this PR.

## IDs

| id | params | entry | exit | TF scope |
|----|--------|-------|------|----------|
| `ehlers-fisher-v1` | Fisher len 10 | crossover(Fish, Trigger) & prior Fish < 0 | crossunder(Fish, Trigger) | full 16 |
| `coppock-curve-v1` | ROC 14+11, WMA 10 | trough-turn while <0 OR zero-cross after ≥10 bars <0 | turn-down while >0 OR crossunder 0 | **1d, 2d only** |
| `session-orb-v1` | UTC 00:00 OR 30m | close > OR high after window | 1× OR height / opposite edge / 23:59 flat | one `orb-utc` cell from 5m |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v4
```

Scoreboard: `results/fresh-wave-v4-scoreboard.md`
