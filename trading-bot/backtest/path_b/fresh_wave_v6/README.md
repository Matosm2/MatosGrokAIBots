# fresh-wave-v6

Path B research wave (FROZEN 2026-09-07): Mass Index bulge, Pring KST, Twiggs MF, DeMarker zone, Darvas box.

**RESEARCH ONLY** — no paper / alerts / webhook. BTC scoreboard only (no ETH OOS in this PR). Hold #15–#23 unmerged.

## IDs

| id | params | entry | exit | TF notes |
|----|--------|-------|------|----------|
| `mass-index-bulge-v1` | MI sum25; bulge >27→<26.5; EMA9 | bulge + EMA9 rising | EMA9 flip down | prefer 4h–1d; full 16 OK |
| `kst-pring-v1` | KST(10,15,20,30)/SMA(10,10,10,15)+Sig9 | Mode A: KST>0 & cross; Mode B: pure cross | crossunder / KST<0 | prefer 1d–2d first |
| `twiggs-mf-v1` | TMF21 | Mode A: channel+N + TMF>0; Mode B: zero cross | opposite / TMF<0 | full 16; ≠ CMF |
| `demarker-zone-v1` | DeM14 0.30/0.70 | was ≤0.30 then >0.30 | mid-0.50 or ≥0.70 | full 16; no RSI |
| `darvas-box-v1` | lookback 90, confirm 3 | close > box top | trail box floor | prefer 1d–2d; ≠ Donchian |

Parked: RVI / CHOP / Elder Impulse. Chandelier = exit-module only (v5).

## CLI

```bash
cd trading-bot
python -m backtest.path_b.fresh_wave_v6
# optional: --prefer-coarse  --tfs 2d,1d,12h,4h  --refresh
```

Scoreboard: `results/fresh-wave-v6-scoreboard.md`
