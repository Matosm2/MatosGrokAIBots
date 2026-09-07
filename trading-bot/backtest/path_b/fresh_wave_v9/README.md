# fresh-wave-v9

Path B research wave (FROZEN 2026-09-07): Camarilla UTC, MESA Sine, Funding-fade — scout-wave-3 parked seats.

**RESEARCH ONLY** — no paper / alerts / webhook. BTC scoreboard only (no ETH OOS in this PR). Hold #15–#26 unmerged. Watchlist: `ema-rsi@9h`, `schaff@2d`. v8 OOS hard-stop 0 survivors.

## IDs

| id | params | entry | exit | TF notes |
|----|--------|-------|------|----------|
| `camarilla-utc-v1` | prior UTC day H/L/C; adj=(H−L)×1.1 | Mode A fade L3 (SL beyond L4); Mode B close>H4 | Mode A mid/H3; Mode B <H3 or EOD | **15m–1h**; ≠ Session ORB |
| `mesa-sine-v1` | DominantCycle=15 Advance=45 | crossover(Sine, LeadSine) | crossunder | prefer 1h–4h; full 16 OK; no Fisher/RSI |
| `funding-fade-v1` | Mode A ≤−0.10%/8h; Mode B z≤−2 ~30d | next bar after funding print | neutral / 2 settlements | Spot **1h–4h**; USDT-M funding signal; ERROR if fetch blocked |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v9
# optional: --prefer-coarse  --tfs 4h,3h,2h,1h  --refresh
```

Scoreboard: `results/fresh-wave-v9-scoreboard.md`
