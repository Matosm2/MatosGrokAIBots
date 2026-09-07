# fresh-wave-v10

Path B research wave (FROZEN 2026-09-07): VWAP-UTC-σ, SMI-Blau, Woodie-UTC, Chaikin Osc, Laguerre price — scout-wave-4 seats.

**RESEARCH ONLY** — no paper / alerts / webhook. BTC scoreboard only (no ETH OOS in this PR). Hold #15–#27 unmerged. Watchlist: `ema-rsi@9h`, `schaff@2d`. v9 hard-stop 0 PASS. SOL is the hard OOS filter (not run here).

Parked (not this wave): Klinger, VR+breakout, % Envelopes.

## IDs

| id | params | entry | exit | TF notes |
|----|--------|-------|------|----------|
| `vwap-utc-sigma-v1` | UTC 00:00 reset VWAP ±σ | Mode A tag −2σ reclaim; Mode B reclaim above VWAP | VWAP touch / EOD UTC | **15m–1h**; ≠ BB |
| `smi-blau-v1` | N=13 smooth 3/3 sig 3; ±40 | Mode A SMI×sig or >0; Mode B OS reclaim | ×sig / mid-0 / ≥+40 | **15m–4h**; ≠ Stoch/Connors/RSI |
| `woodie-utc-v1` | P=(H+L+2C)/4 prior UTC day | Mode A fade S1 (SL S2); Mode B >R1 | mid/P or opposite / EOD | **5m–1h**; ≠ Camarilla/ORB |
| `chaikin-osc-v1` | EMA3−EMA10 ADL | crossover(Osc,0) | crossunder(Osc,0) | **15m–4h**; ≠ CMF/OBV/MFI |
| `laguerre-price-v1` | γ=0.8 on close | close × above Laguerre | close × below Laguerre | **1h–4h**; ≠ Laguerre RSI / EMA×RSI |

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v10
# optional: --prefer-coarse  --tfs 4h,3h,2h,1h  --refresh
```

Scoreboard: `results/fresh-wave-v10-scoreboard.md`
