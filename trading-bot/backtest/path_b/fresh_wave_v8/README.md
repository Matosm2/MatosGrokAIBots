# fresh-wave-v8

Path B research wave (FROZEN 2026-09-07): Gann HiLo, Asian→London, FI(13), Cyber Cycle, Williams Fractals — scout-wave-3 Part A seats.

**RESEARCH ONLY** — no paper / alerts / webhook. BTC scoreboard only (no ETH OOS in this PR). Hold #15–#25 unmerged. Watchlist: `ema-rsi@9h`, `schaff@2d`.

## IDs

| id | params | entry | exit | TF notes |
|----|--------|-------|------|----------|
| `gann-hilo-activator-v1` | n=3 SMA Hi/Lo | flip above activator | flip below | prefer 1h–1d; ≠ PSAR |
| `asian-london-break-v1` | box 00:00–07:00 UTC | close > Asian high after 07:00 | mid stop; TP 1× or 16:00 flat | **5m/15m only**; ≠ Session ORB / Donchian |
| `force-index-13-v1` | FI EMA(13) | crossover(FI, 0) | crossunder(FI, 0) | prefer 4h–1d; ≠ Triple Screen FI(2) |
| `cyber-cycle-v1` | α=0.07 | crossover(Cycle, Trigger) | crossunder | prefer 1h–1d; no Fisher |
| `williams-fractals-v1` | 5-bar confirmed | close > last up-fractal | close < last down-fractal | prefer 1h–4h; no Alligator |

Parked: camarilla, funding-fade, mesa-sine, Qstick/VWAP/SMI/ASI/EMV.

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v8
# optional: --prefer-coarse  --tfs 2d,1d,12h,4h  --refresh
```

Scoreboard: `results/fresh-wave-v8-scoreboard.md`
