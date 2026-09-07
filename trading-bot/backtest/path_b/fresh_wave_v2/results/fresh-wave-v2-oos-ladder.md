# fresh-wave-v2-oos-ladder

_Generated: 2026-09-06 20:58 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v2 PASS_6m cells. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v2` BTC PASS_6m cells (frozen params / TF / agg)
- Strategy stop-ladder: **ETH all → SOL on ETH PASS → BNB on SOL PASS**
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window); also report full(~2y)
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen: Aroon(25)+Up≥70; PSAR AF 0.02/0.02/0.2; CCI(20,0.015)
- Hard-stop (not OOS): williams-r-mr-v1, vortex-trend-v1

## Cells (priority order)

1. `aroon-trend-v1` @ `6h`
2. `psar-trend-v1` @ `2d`
3. `cci-mr-v1` @ `2d`

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `aroon-trend-v1` @ `6h` | **FAIL**(1.19) | SKIP | SKIP |
| `psar-trend-v1` @ `2d` | **FAIL**(-0.00) | SKIP | SKIP |
| `cci-mr-v1` @ `2d` | **FAIL**(0.21) | SKIP | SKIP |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | aroon-trend-v1 | 6h | 11 | 45.45% | +32.96% | +27.67% | 1.191 | +0.83% | **FAIL** |
| 2 | psar-trend-v1 | 2d | 4 | 75.00% | -0.03% | +19.49% | -0.002 | +0.03% | **FAIL** |
| 3 | cci-mr-v1 | 2d | 1 | 100.00% | +4.07% | +19.49% | 0.209 | +0.10% | **FAIL** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | aroon-trend-v1 | 6h | 50 | 30.00% | -13.47% | +10.94% | -1.231 | +0.24% |
| 2 | psar-trend-v1 | 2d | 17 | 41.18% | -5.58% | +3.92% | -1.425 | +0.45% |
| 3 | cci-mr-v1 | 2d | 6 | 66.67% | -8.20% | +3.92% | -2.095 | +0.14% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | aroon-trend-v1 | 6h | — | — | — | — | — | — | **SKIP** |
| 2 | psar-trend-v1 | 2d | — | — | — | — | — | — | **SKIP** |
| 3 | cci-mr-v1 | 2d | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | aroon-trend-v1 | 6h | — | — | — | — | — | SKIP |
| 2 | psar-trend-v1 | 2d | — | — | — | — | — | SKIP |
| 3 | cci-mr-v1 | 2d | — | — | — | — | — | SKIP |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|-----|---------|---------|-----------|
| 1 | aroon-trend-v1 | 6h | — | — | — | — | — | — | **SKIP** |
| 2 | psar-trend-v1 | 2d | — | — | — | — | — | — | **SKIP** |
| 3 | cci-mr-v1 | 2d | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|-----|---------|---------|
| 1 | aroon-trend-v1 | 6h | — | — | — | — | — | SKIP |
| 2 | psar-trend-v1 | 2d | — | — | — | — | — | SKIP |
| 3 | cci-mr-v1 | 2d | — | — | — | — | — | SKIP |

## Cell detail

### `ETHUSDT` · `aroon-trend-v1` @ `6h` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 11 | 5/6 | 45.45% | +32.96% | +27.67% | 1.191 | 22.89% | **FAIL** |
| 6m | ops | 2.5% | 11 | 5/6 | 45.45% | +0.83% | +27.67% | 0.030 | 0.66% | **—** |
| full(~2y) | gate | 100% | 50 | 15/35 | 30.00% | -13.47% | +10.94% | -1.231 | 57.40% | **FAIL** |
| full(~2y) | ops | 2.5% | 50 | 15/35 | 30.00% | +0.24% | +10.94% | 0.022 | 2.08% | **—** |

### `ETHUSDT` · `psar-trend-v1` @ `2d` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 4 | 3/1 | 75.00% | -0.03% | +19.49% | -0.002 | 18.44% | **FAIL** |
| 6m | ops | 2.5% | 4 | 3/1 | 75.00% | +0.03% | +19.49% | 0.002 | 0.49% | **—** |
| full(~2y) | gate | 100% | 17 | 7/10 | 41.18% | -5.58% | +3.92% | -1.425 | 48.17% | **FAIL** |
| full(~2y) | ops | 2.5% | 17 | 7/10 | 41.18% | +0.45% | +3.92% | 0.114 | 1.58% | **—** |

### `ETHUSDT` · `cci-mr-v1` @ `2d` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 1 | 1/0 | 100.00% | +4.07% | +19.49% | 0.209 | 12.84% | **FAIL** |
| 6m | ops | 2.5% | 1 | 1/0 | 100.00% | +0.10% | +19.49% | 0.005 | 0.32% | **—** |
| full(~2y) | gate | 100% | 6 | 4/2 | 66.67% | -8.20% | +3.92% | -2.095 | 55.29% | **FAIL** |
| full(~2y) | ops | 2.5% | 6 | 4/2 | 66.67% | +0.14% | +3.92% | 0.037 | 1.46% | **—** |

### `SOLUSDT` · `aroon-trend-v1` @ `6h` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `SOLUSDT` · `psar-trend-v1` @ `2d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `SOLUSDT` · `cci-mr-v1` @ `2d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `aroon-trend-v1` @ `6h` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `psar-trend-v1` @ `2d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `cci-mr-v1` @ `2d` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

## Caveats

- Stop-ladder: later symbols only run on cells that PASS the prior rung.
- Frozen params from fresh-wave-v2 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- williams-r-mr-v1 + vortex-trend-v1 hard-stopped on BTC — not OOS'd.
- Not wired to paper/alerts/webhook. Hold PR #20 unmerged (push only).
- Same mtf_ohlcv aggregation + fresh_wave_v2 signal code as BTC scoreboard.

