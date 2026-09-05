# jewel-mtf-hub-regime-v1 — open-proxy edition

_Generated: 2026-09-05 23:17 UTC_

**RESEARCH ONLY — not paper / alerts / webhook.**

Public-indicator proxies only (ADX/DI, RSI, EMA). Not Jewel. Not Hub.

## Frozen proxies

| Proxy | Definition |
|-------|------------|
| Regime | ADX(14), +DI(14), −DI(14) Wilder; +1 if +DI>−DI and ADX≥20; −1 if −DI>+DI and ADX≥20; else 0 |
| Flip→green | prior regime ≤ 0 and current = +1 |
| Leave green | prior = +1 and current ≠ +1 |
| Strength | RSI(14); enter crossover(RSI, 60); exit RSI < 50 |
| Ribbon | EMA21 / EMA55; ribbon_low=min, ribbon_high=max; M1 also allows close×EMA21 while green (default ON) |
| HTF join | HTF state only when htf bar fully closed (htf_close ≤ ltf_close) — reuse PR #12 join |
| 2D bars | Pair consecutive 1D bars index-wise; drop trailing orphan |

## Matrix (long-only spot)

| ID | Rule |
|----|------|
| M1 | TF=2D: entry flip→green OR (green AND close×EMA21); exit leave green |
| M2 | HTF=1D regime=+1, LTF=4H: entry 4H flip→green while 1D=+1; exit 1D leave green |
| M3 | TF=2D: entry RSI cross 60; exit RSI < 50 |
| M4 | HTF=1D RSI≥60, LTF=4H: entry 4H RSI cross 60 while 1D≥60; exit 1D RSI < 50 |

## Costs / sizing

| Parameter | Value |
|-----------|-------|
| Fee | 0.10% / side |
| Slippage | 5 bps adverse vs close |
| Mode-A | 100% equity when in |
| Mode-B | 2.5% equity (ops-parallel; live/paper defaults unchanged) |
| Fills | bar-close |
| Symbol | BTCUSDT |

## Data

- Source: Binance Spot public klines via data-api.binance.vision (no API key)
- Symbol: BTCUSDT
- 1D bars: 1096 (2023-09-06 → 2026-09-05 UTC)
- 4H bars: 6579 (2023-09-05 → 2026-09-05 UTC)
- 2D: aggregate_1d_to_2d — consecutive daily pairs, drop trailing orphan
- Fetch lookback ~3y; 6m window = last 6 months

## Gate table (lead: 6m Mode-A ≥ 1.2 × B&H)

PASS if Mode-A return ≥ **1.2 ×** buy-and-hold over the same 6m window and ≥1 trade. WR is informational. On FAIL: hard-stop promotion (no paper/alerts/webhook).

| Variant | Mode | Window | Return | B&H | Ratio | WR | Trades | Gate |
|---------|------|--------|--------|-----|-------|----|--------|------|
| M1 | Mode-A | 6m | +10.95% | +16.26% | 0.67× | 50.0% | 2 | **FAIL** |
| M2 | Mode-A | 6m | -5.84% | +17.55% | -0.33× | 0.0% | 2 | **FAIL** |
| M3 | Mode-A | 6m | +4.80% | +16.26% | 0.30× | 0.0% | 1 | **FAIL** |
| M4 | Mode-A | 6m | +4.65% | +17.55% | 0.26× | 100.0% | 1 | **FAIL** |

## Results — 6m

| Variant | Mode | Return | B&H | Ratio | WR | Trades | MaxDD | Gate* |
|---------|------|--------|-----|-------|----|--------|-------|-------|
| M1 | Mode-A | +10.95% | +16.26% | 0.67× | 50.0% | 2 | 8.11% | FAIL |
| M1 | Mode-B | +0.28% | +16.26% | 0.02× | 50.0% | 2 | 0.23% | — |
| M2 | Mode-A | -5.84% | +17.55% | -0.33× | 0.0% | 2 | 12.42% | FAIL |
| M2 | Mode-B | -0.14% | +17.55% | -0.01× | 0.0% | 2 | 0.33% | — |
| M3 | Mode-A | +4.80% | +16.26% | 0.30× | 0.0% | 1 | 8.39% | FAIL |
| M3 | Mode-B | +0.13% | +16.26% | 0.01× | 0.0% | 1 | 0.22% | — |
| M4 | Mode-A | +4.65% | +17.55% | 0.26× | 100.0% | 1 | 8.28% | FAIL |
| M4 | Mode-B | +0.12% | +17.55% | 0.01× | 100.0% | 1 | 0.22% | — |

_\* Gate column applies the 1.2× B&H rule to Mode-A only (lead decision on 6m)._

## Results — full

| Variant | Mode | Return | B&H | Ratio | WR | Trades | MaxDD | Gate* |
|---------|------|--------|-----|-------|----|--------|-------|-------|
| M1 | Mode-A | +49.27% | +203.04% | 0.24× | 33.3% | 15 | 30.12% | FAIL |
| M1 | Mode-B | +1.34% | +203.04% | 0.01× | 33.3% | 15 | 0.91% | — |
| M2 | Mode-A | +61.03% | +209.75% | 0.29× | 29.4% | 17 | 35.42% | FAIL |
| M2 | Mode-B | +1.76% | +209.75% | 0.01× | 29.4% | 17 | 1.08% | — |
| M3 | Mode-A | +123.54% | +203.04% | 0.61× | 45.5% | 11 | 33.71% | FAIL |
| M3 | Mode-B | +2.62% | +203.04% | 0.01× | 45.5% | 11 | 1.16% | — |
| M4 | Mode-A | +62.19% | +209.75% | 0.30× | 35.7% | 14 | 32.81% | FAIL |
| M4 | Mode-B | +1.57% | +209.75% | 0.01× | 35.7% | 14 | 1.00% | — |

_\* Gate column applies the 1.2× B&H rule to Mode-A only (lead decision on 6m)._

## Detail — M1

### M1 / Mode-A / full

Bars: 548 (2023-09-06 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 15 |
| Win rate | 33.33% |
| Return | +49.27% |
| Buy & hold | +203.04% |
| Ratio vs B&H | 0.243× |
| Max drawdown | 30.12% |
| Gate (≥1.2× B&H) | **FAIL** |

### M1 / Mode-B / full

Bars: 548 (2023-09-06 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 15 |
| Win rate | 33.33% |
| Return | +1.34% |
| Buy & hold | +203.04% |
| Ratio vs B&H | 0.007× |
| Max drawdown | 0.91% |

### M1 / Mode-A / 6m

Bars: 91 (2026-03-08 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 2 |
| Win rate | 50.00% |
| Return | +10.95% |
| Buy & hold | +16.26% |
| Ratio vs B&H | 0.673× |
| Max drawdown | 8.11% |
| Gate (≥1.2× B&H) | **FAIL** |

### M1 / Mode-B / 6m

Bars: 91 (2026-03-08 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 2 |
| Win rate | 50.00% |
| Return | +0.28% |
| Buy & hold | +16.26% |
| Ratio vs B&H | 0.017× |
| Max drawdown | 0.23% |

## Detail — M2

### M2 / Mode-A / full

Bars: 6579 (2023-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 17 |
| Win rate | 29.41% |
| Return | +61.03% |
| Buy & hold | +209.75% |
| Ratio vs B&H | 0.291× |
| Max drawdown | 35.42% |
| Gate (≥1.2× B&H) | **FAIL** |

### M2 / Mode-B / full

Bars: 6579 (2023-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 17 |
| Win rate | 29.41% |
| Return | +1.76% |
| Buy & hold | +209.75% |
| Ratio vs B&H | 0.008× |
| Max drawdown | 1.08% |

### M2 / Mode-A / 6m

Bars: 1095 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 2 |
| Win rate | 0.00% |
| Return | -5.84% |
| Buy & hold | +17.55% |
| Ratio vs B&H | -0.333× |
| Max drawdown | 12.42% |
| Gate (≥1.2× B&H) | **FAIL** |

### M2 / Mode-B / 6m

Bars: 1095 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 2 |
| Win rate | 0.00% |
| Return | -0.14% |
| Buy & hold | +17.55% |
| Ratio vs B&H | -0.008× |
| Max drawdown | 0.33% |

## Detail — M3

### M3 / Mode-A / full

Bars: 548 (2023-09-06 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 11 |
| Win rate | 45.45% |
| Return | +123.54% |
| Buy & hold | +203.04% |
| Ratio vs B&H | 0.608× |
| Max drawdown | 33.71% |
| Gate (≥1.2× B&H) | **FAIL** |

### M3 / Mode-B / full

Bars: 548 (2023-09-06 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 11 |
| Win rate | 45.45% |
| Return | +2.62% |
| Buy & hold | +203.04% |
| Ratio vs B&H | 0.013× |
| Max drawdown | 1.16% |

### M3 / Mode-A / 6m

Bars: 91 (2026-03-08 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 1 |
| Win rate | 0.00% |
| Return | +4.80% |
| Buy & hold | +16.26% |
| Ratio vs B&H | 0.295× |
| Max drawdown | 8.39% |
| Gate (≥1.2× B&H) | **FAIL** |

### M3 / Mode-B / 6m

Bars: 91 (2026-03-08 → 2026-09-04 UTC)

| Metric | Value |
|--------|-------|
| Trades | 1 |
| Win rate | 0.00% |
| Return | +0.13% |
| Buy & hold | +16.26% |
| Ratio vs B&H | 0.008× |
| Max drawdown | 0.22% |

## Detail — M4

### M4 / Mode-A / full

Bars: 6579 (2023-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 14 |
| Win rate | 35.71% |
| Return | +62.19% |
| Buy & hold | +209.75% |
| Ratio vs B&H | 0.297× |
| Max drawdown | 32.81% |
| Gate (≥1.2× B&H) | **FAIL** |

### M4 / Mode-B / full

Bars: 6579 (2023-09-05 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 14 |
| Win rate | 35.71% |
| Return | +1.57% |
| Buy & hold | +209.75% |
| Ratio vs B&H | 0.008× |
| Max drawdown | 1.00% |

### M4 / Mode-A / 6m

Bars: 1095 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 1 |
| Win rate | 100.00% |
| Return | +4.65% |
| Buy & hold | +17.55% |
| Ratio vs B&H | 0.265× |
| Max drawdown | 8.28% |
| Gate (≥1.2× B&H) | **FAIL** |

### M4 / Mode-B / 6m

Bars: 1095 (2026-03-07 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Trades | 1 |
| Win rate | 100.00% |
| Return | +0.12% |
| Buy & hold | +17.55% |
| Ratio vs B&H | 0.007× |
| Max drawdown | 0.22% |

## Caveats

- Thresholds frozen; not tuned on the 6m evaluation window.
- Warmup indicators on full history; window books start flat.
- Single-path BTCUSDT sample; do not over-generalize.
- On FAIL vs 1.2× B&H gate: hard-stop promotion — no paper/alerts/webhook.
- Research folder id `jewel-mtf-hub-regime-v1` is archival naming only; series are open ADX/RSI/EMA proxies.

