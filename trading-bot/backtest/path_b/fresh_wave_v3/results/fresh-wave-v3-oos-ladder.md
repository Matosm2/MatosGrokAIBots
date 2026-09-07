# fresh-wave-v3-oos-ladder

_Generated: 2026-09-06 21:11 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v3 PASS_6m cells. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v3` BTC PASS_6m cells (frozen params / TF / agg)
- Strategy stop-ladder: **ETH all → SOL on ETH PASS → BNB on SOL PASS** (sample-size cell order)
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window); also report full(~2y)
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen: STC(23,50,10) 25/75; Donchian entry20/exit10
- Hard-stop (not OOS): adx-dmi-trend-v1, elder-ray-v1, tsi-momentum-v1

## Cells (priority order by sample size)

1. `schaff-stc-v1` @ `12h`
2. `schaff-stc-v1` @ `1d`
3. `donchian-breakout-v1` @ `1d`
4. `schaff-stc-v1` @ `2d`

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `schaff-stc-v1` @ `12h` | **FAIL**(0.98) | SKIP | SKIP |
| `schaff-stc-v1` @ `1d` | **FAIL**(0.27) | SKIP | SKIP |
| `donchian-breakout-v1` @ `1d` | **FAIL**(-0.51) | SKIP | SKIP |
| `schaff-stc-v1` @ `2d` | **PASS**(2.00) | **PASS**(2.71) | **PASS**(1.67) |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | schaff-stc-v1 | 12h | 8 | 50.00% | +28.62% | +29.16% | 0.982 | +0.81% | **FAIL** |
| 2 | schaff-stc-v1 | 1d | 6 | 50.00% | +6.50% | +24.47% | 0.266 | +0.19% | **FAIL** |
| 3 | donchian-breakout-v1 | 1d | 4 | 25.00% | -12.51% | +24.47% | -0.511 | -0.29% | **FAIL** |
| 4 | schaff-stc-v1 | 2d | 1 | 100.00% | +39.04% | +19.49% | 2.003 | +0.98% | **PASS** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | schaff-stc-v1 | 12h | 37 | 37.84% | +14.98% | +12.43% | 1.205 | +1.09% |
| 2 | schaff-stc-v1 | 1d | 22 | 45.45% | +28.12% | +9.11% | 3.087 | +1.60% |
| 3 | donchian-breakout-v1 | 1d | 14 | 35.71% | -34.54% | +9.11% | -3.792 | -0.76% |
| 4 | schaff-stc-v1 | 2d | 8 | 50.00% | +76.27% | +3.92% | 19.475 | +2.18% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | schaff-stc-v1 | 12h | — | — | — | — | — | — | **SKIP** |
| 2 | schaff-stc-v1 | 1d | — | — | — | — | — | — | **SKIP** |
| 3 | donchian-breakout-v1 | 1d | — | — | — | — | — | — | **SKIP** |
| 4 | schaff-stc-v1 | 2d | 1 | 100.00% | +51.91% | +19.17% | 2.707 | +1.30% | **PASS** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | schaff-stc-v1 | 12h | — | — | — | — | — | SKIP |
| 2 | schaff-stc-v1 | 1d | — | — | — | — | — | SKIP |
| 3 | donchian-breakout-v1 | 1d | — | — | — | — | — | SKIP |
| 4 | schaff-stc-v1 | 2d | 10 | 60.00% | +51.05% | -23.62% | -2.162 | +1.49% |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | schaff-stc-v1 | 12h | — | — | — | — | — | — | **SKIP** |
| 2 | schaff-stc-v1 | 1d | — | — | — | — | — | — | **SKIP** |
| 3 | donchian-breakout-v1 | 1d | — | — | — | — | — | — | **SKIP** |
| 4 | schaff-stc-v1 | 2d | 1 | 100.00% | +29.56% | +17.66% | 1.674 | +0.74% | **PASS** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | schaff-stc-v1 | 12h | — | — | — | — | — | SKIP |
| 2 | schaff-stc-v1 | 1d | — | — | — | — | — | SKIP |
| 3 | donchian-breakout-v1 | 1d | — | — | — | — | — | SKIP |
| 4 | schaff-stc-v1 | 2d | 10 | 70.00% | +91.46% | +47.78% | 1.914 | +1.96% |

## Cell detail

### `ETHUSDT` · `schaff-stc-v1` @ `12h` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 8 | 4/4 | 50.00% | +28.62% | +29.16% | 0.982 | 31.05% | **FAIL** |
| 6m | ops | 2.5% | 8 | 4/4 | 50.00% | +0.81% | +29.16% | 0.028 | 0.88% | **—** |
| full(~2y) | gate | 100% | 37 | 14/23 | 37.84% | +14.98% | +12.43% | 1.205 | 58.33% | **PASS** |
| full(~2y) | ops | 2.5% | 37 | 14/23 | 37.84% | +1.09% | +12.43% | 0.088 | 2.10% | **—** |

### `ETHUSDT` · `schaff-stc-v1` @ `1d` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 6 | 3/3 | 50.00% | +6.50% | +24.47% | 0.266 | 16.77% | **FAIL** |
| 6m | ops | 2.5% | 6 | 3/3 | 50.00% | +0.19% | +24.47% | 0.008 | 0.46% | **—** |
| full(~2y) | gate | 100% | 22 | 10/12 | 45.45% | +28.12% | +9.11% | 3.087 | 51.41% | **PASS** |
| full(~2y) | ops | 2.5% | 22 | 10/12 | 45.45% | +1.60% | +9.11% | 0.175 | 1.70% | **—** |

### `ETHUSDT` · `donchian-breakout-v1` @ `1d` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 4 | 1/3 | 25.00% | -12.51% | +24.47% | -0.511 | 20.43% | **FAIL** |
| 6m | ops | 2.5% | 4 | 1/3 | 25.00% | -0.29% | +24.47% | -0.012 | 0.54% | **—** |
| full(~2y) | gate | 100% | 14 | 5/9 | 35.71% | -34.54% | +9.11% | -3.792 | 56.45% | **FAIL** |
| full(~2y) | ops | 2.5% | 14 | 5/9 | 35.71% | -0.76% | +9.11% | -0.083 | 1.98% | **—** |

### `ETHUSDT` · `schaff-stc-v1` @ `2d` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 1 | 1/0 | 100.00% | +39.04% | +19.49% | 2.003 | 3.96% | **PASS** |
| 6m | ops | 2.5% | 1 | 1/0 | 100.00% | +0.98% | +19.49% | 0.050 | 0.13% | **—** |
| full(~2y) | gate | 100% | 8 | 4/4 | 50.00% | +76.27% | +3.92% | 19.475 | 47.71% | **PASS** |
| full(~2y) | ops | 2.5% | 8 | 4/4 | 50.00% | +2.18% | +3.92% | 0.557 | 1.54% | **—** |

### `SOLUSDT` · `schaff-stc-v1` @ `12h` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `schaff-stc-v1` @ `1d` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `donchian-breakout-v1` @ `1d` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `schaff-stc-v1` @ `2d` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 1 | 1/0 | 100.00% | +51.91% | +19.17% | 2.707 | 11.71% | **PASS** |
| 6m | ops | 2.5% | 1 | 1/0 | 100.00% | +1.30% | +19.17% | 0.068 | 0.35% | **—** |
| full(~2y) | gate | 100% | 10 | 6/4 | 60.00% | +51.05% | -23.62% | -2.162 | 38.20% | **PASS** |
| full(~2y) | ops | 2.5% | 10 | 6/4 | 60.00% | +1.49% | -23.62% | -0.063 | 1.18% | **—** |

### `BNBUSDT` · `schaff-stc-v1` @ `12h` — 6m **SKIP**

_Skipped:_ prior rung SOLUSDT FAIL/ERROR/SKIP

### `BNBUSDT` · `schaff-stc-v1` @ `1d` — 6m **SKIP**

_Skipped:_ prior rung SOLUSDT FAIL/ERROR/SKIP

### `BNBUSDT` · `donchian-breakout-v1` @ `1d` — 6m **SKIP**

_Skipped:_ prior rung SOLUSDT FAIL/ERROR/SKIP

### `BNBUSDT` · `schaff-stc-v1` @ `2d` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 1 | 1/0 | 100.00% | +29.56% | +17.66% | 1.674 | 4.14% | **PASS** |
| 6m | ops | 2.5% | 1 | 1/0 | 100.00% | +0.74% | +17.66% | 0.042 | 0.10% | **—** |
| full(~2y) | gate | 100% | 10 | 7/3 | 70.00% | +91.46% | +47.78% | 1.914 | 30.30% | **PASS** |
| full(~2y) | ops | 2.5% | 10 | 7/3 | 70.00% | +1.96% | +47.78% | 0.041 | 0.87% | **—** |

## Caveats

- Stop-ladder: later symbols only run on cells that PASS the prior rung.
- Frozen params from fresh-wave-v3 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- adx-dmi / elder-ray / tsi hard-stopped on BTC — not OOS'd.
- Not wired to paper/alerts/webhook. Hold PR #21 unmerged (push only).
- Same mtf_ohlcv aggregation + fresh_wave_v3 signal code as BTC scoreboard.

