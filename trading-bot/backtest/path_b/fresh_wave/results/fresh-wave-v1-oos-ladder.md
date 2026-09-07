# fresh-wave-v1-oos-ladder

_Generated: 2026-09-06 00:44 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v1 PASS_6m cells. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v1` BTC PASS_6m cells (frozen params / TF / agg)
- Strategy stop-ladder: **ETH all → SOL on ETH PASS → BNB on SOL PASS**
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window); also report full(~2y)
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen: Ichimoku 9/26/52; OBV×EMA20 + EMA50; NR7/ATR14×2/10-bar

## Cells (priority order)

1. `ichimoku-cloud-trend-v1` @ `2h`
2. `obv-ema-trend-v1` @ `1d`
3. `nr7-breakout-v1` @ `2d`

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `ichimoku-cloud-trend-v1` @ `2h` | **FAIL**(0.34) | SKIP | SKIP |
| `obv-ema-trend-v1` @ `1d` | **FAIL**(0.61) | SKIP | SKIP |
| `nr7-breakout-v1` @ `2d` | **FAIL**(0.92) | SKIP | SKIP |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | ichimoku-cloud-trend-v1 | 2h | 20 | 20.00% | +8.50% | +24.71% | 0.344 | +0.30% | **FAIL** |
| 2 | obv-ema-trend-v1 | 1d | 8 | 12.50% | +17.21% | +28.06% | 0.613 | +0.49% | **FAIL** |
| 3 | nr7-breakout-v1 | 2d | 6 | 66.67% | +21.28% | +23.03% | 0.924 | +0.54% | **FAIL** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | ichimoku-cloud-trend-v1 | 2h | 86 | 29.07% | -3.65% | +4.59% | -0.794 | +0.18% |
| 2 | obv-ema-trend-v1 | 1d | 32 | 15.62% | +34.79% | +11.48% | 3.030 | +1.49% |
| 3 | nr7-breakout-v1 | 2d | 23 | 43.48% | -4.47% | +7.84% | -0.570 | +0.34% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | ichimoku-cloud-trend-v1 | 2h | — | — | — | — | — | — | **SKIP** |
| 2 | obv-ema-trend-v1 | 1d | — | — | — | — | — | — | **SKIP** |
| 3 | nr7-breakout-v1 | 2d | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | ichimoku-cloud-trend-v1 | 2h | — | — | — | — | — | SKIP |
| 2 | obv-ema-trend-v1 | 1d | — | — | — | — | — | SKIP |
| 3 | nr7-breakout-v1 | 2d | — | — | — | — | — | SKIP |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | ichimoku-cloud-trend-v1 | 2h | — | — | — | — | — | — | **SKIP** |
| 2 | obv-ema-trend-v1 | 1d | — | — | — | — | — | — | **SKIP** |
| 3 | nr7-breakout-v1 | 2d | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | ichimoku-cloud-trend-v1 | 2h | — | — | — | — | — | SKIP |
| 2 | obv-ema-trend-v1 | 1d | — | — | — | — | — | SKIP |
| 3 | nr7-breakout-v1 | 2d | — | — | — | — | — | SKIP |

## Cell detail

### `ETHUSDT` · `ichimoku-cloud-trend-v1` @ `2h` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 20 | 4/16 | 20.00% | +8.50% | +24.71% | 0.344 | 15.12% | **FAIL** |
| 6m | ops | 2.5% | 20 | 4/16 | 20.00% | +0.30% | +24.71% | 0.012 | 0.40% | **—** |
| full(~2y) | gate | 100% | 86 | 25/61 | 29.07% | -3.65% | +4.59% | -0.794 | 44.30% | **FAIL** |
| full(~2y) | ops | 2.5% | 86 | 25/61 | 29.07% | +0.18% | +4.59% | 0.040 | 1.42% | **—** |

### `ETHUSDT` · `obv-ema-trend-v1` @ `1d` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 8 | 1/7 | 12.50% | +17.21% | +28.06% | 0.613 | 11.00% | **FAIL** |
| 6m | ops | 2.5% | 8 | 1/7 | 12.50% | +0.49% | +28.06% | 0.017 | 0.29% | **—** |
| full(~2y) | gate | 100% | 32 | 5/27 | 15.62% | +34.79% | +11.48% | 3.030 | 46.53% | **PASS** |
| full(~2y) | ops | 2.5% | 32 | 5/27 | 15.62% | +1.49% | +11.48% | 0.130 | 1.63% | **—** |

### `ETHUSDT` · `nr7-breakout-v1` @ `2d` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 6 | 4/2 | 66.67% | +21.28% | +23.03% | 0.924 | 17.24% | **FAIL** |
| 6m | ops | 2.5% | 6 | 4/2 | 66.67% | +0.54% | +23.03% | 0.023 | 0.45% | **—** |
| full(~2y) | gate | 100% | 23 | 10/13 | 43.48% | -4.47% | +7.84% | -0.570 | 47.21% | **FAIL** |
| full(~2y) | ops | 2.5% | 23 | 10/13 | 43.48% | +0.34% | +7.84% | 0.044 | 1.42% | **—** |

### `SOLUSDT` · `ichimoku-cloud-trend-v1` @ `2h` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `SOLUSDT` · `obv-ema-trend-v1` @ `1d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `SOLUSDT` · `nr7-breakout-v1` @ `2d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `ichimoku-cloud-trend-v1` @ `2h` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `obv-ema-trend-v1` @ `1d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `nr7-breakout-v1` @ `2d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

## Caveats

- Stop-ladder: later symbols only run on cells that PASS the prior rung.
- Frozen params from fresh-wave-v1 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- Not wired to paper/alerts/webhook. Hold PR #18 unmerged.
- Same mtf_ohlcv aggregation + fresh_wave signal code as BTC scoreboard.

