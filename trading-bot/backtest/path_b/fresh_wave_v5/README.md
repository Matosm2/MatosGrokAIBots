# fresh-wave-v5

Path B research wave (FROZEN 2026-09-07): Elder Triple Screen+FI, CMF, LinReg+R², MFI-only, Ultimate Oscillator. Chandelier Exit = helper only.

**RESEARCH ONLY** — no paper / alerts / webhook. Part B parked. OOS stop-ladder via `--oos-ladder`.

## IDs

| id | params | entry | exit | TF scope |
|----|--------|-------|------|----------|
| `elder-triple-screen-fi-v1` | FI EMA 2 (+13); MACD-hist tide | tide rising + FI\<0 → buy-stop prior high (~2 bar cancel) | tide flip / FI\>0 | pairs `(4h,1d)`, `(1d,1w)` only |
| `cmf-flow-v1` | CMF 21 (sweep 14/20/21/30) | Mode A zero-cross; Mode B channel+CMF\>0 | opposite | full 16 |
| `linreg-r2-v1` | L20 R²0.7 (±2σ) | Mode A breakout+slope; Mode B fade −2σ | mid / opposite | prefer 4h–1d; full 16 OK |
| `mfi-only-v1` | MFI 14 @20/80 | was ≤20 then cross \>20 | ≥80 or mid-50 | full 16; **no RSI** |
| `ultimate-oscillator-v1` | UO 7/14/28 | classic div or Mode-B cross 30 | ≥70 or \>50→\<45 | prefer 4h–1d |
| `chandelier-exit` | ATR22 × 3 | *(helper)* | long trail | module/tests only |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v5
# optional: --prefer-4h-1d  --tfs 2d,1d,12h,4h  --refresh
# OOS: python -m backtest.path_b.fresh_wave_v5 --oos-ladder
```

Scoreboard: `results/fresh-wave-v5-scoreboard.md`
OOS ladder: `results/fresh-wave-v5-oos-ladder.md`
