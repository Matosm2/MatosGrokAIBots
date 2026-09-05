# jewel_mtf_hub — open-proxy edition

**research_id:** `jewel-mtf-hub-regime-v1`  
**Subtitle:** **open-proxy edition**  
**Status:** multi-TF join + M1–M4 public-indicator matrix (research only)

Maps higher-timeframe (HTF) series onto lower-timeframe (LTF) bars with
**no lookahead** (`htf_close <= ltf_close`), then scores **M1–M4** using
frozen open proxies:

| Proxy | Public indicators (honest names) |
|-------|----------------------------------|
| Regime | ADX(14), +DI(14), −DI(14) Wilder; threshold ADX ≥ 20 |
| Strength | RSI(14); enter cross 60; exit &lt; 50 |
| Ribbon | EMA21 / EMA55; M1 optional close×EMA21 while green (default ON) |

**Not Jewel. Not Hub.** Invite-only Jewel plots are not used or invented here.

## 2D aggregation

2D bars are built from 1D OHLCV by **pairing consecutive daily bars**
(index 0+1, 2+3, …; drop trailing orphan). See `aggregate.py`.

## Run

```bash
cd trading-bot
source .venv/bin/activate
pytest tests/test_jewel_mtf_hub_join.py tests/test_jewel_mtf_hub_open_proxy.py -q
python -m backtest.jewel_mtf_hub --symbol BTCUSDT
```

Report: `results/jewel-mtf-hub-regime-v1-open-proxy.md`

## Gate

Lead: **last-6-month Mode-A return ≥ 1.2 × buy-and-hold** (same window).  
WR informational. On FAIL: hard-stop promotion (no paper/alerts/webhook).

## Dual sizing (research only)

| Mode | Size |
|------|------|
| Mode-A | 100% equity when in |
| Mode-B | 2.5% equity (ops-parallel; does **not** change live/paper defaults) |

Costs: 0.10%/side + 5 bps; bar-close fills; spot long-only.

## What this is not

- Not paper/webhook wiring
- Not a retune of `jewel-strength-hold-v1` / Path B `jewel_replay`
- Not fake Hub or Jewel Slow/High under those names
