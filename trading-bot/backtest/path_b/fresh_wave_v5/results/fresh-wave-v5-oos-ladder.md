# fresh-wave-v5-oos-ladder

_Generated: 2026-09-07 07:32 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v5 PASS_6m cells. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v5` BTC PASS_6m cells (frozen params / TF / agg)
- Strategy stop-ladder: **ETH all → SOL on ETH PASS → BNB on SOL PASS** (sample-size cell order)
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window); also report full(~2y)
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen: CMF Mode-A periods 20/21; MFI 14 @15/85 and 20/80
- Hard-stop (not OOS): elder-triple-screen-fi-v1, linreg-r2-v1, ultimate-oscillator-v1

## Cells (priority order by sample size)

1. `cmf-flow-v1` @ `4h|p20|A`
2. `cmf-flow-v1` @ `7h|p20|A`
3. `cmf-flow-v1` @ `7h|p21|A`
4. `mfi-only-v1` @ `2d|14|15/85`
5. `mfi-only-v1` @ `2d|14|20/80`

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `cmf-flow-v1` @ `4h|p20|A` | **FAIL**(-0.22) | SKIP | SKIP |
| `cmf-flow-v1` @ `7h|p20|A` | **PASS**(1.23) | **FAIL**(-0.08) | SKIP |
| `cmf-flow-v1` @ `7h|p21|A` | **FAIL**(0.94) | SKIP | SKIP |
| `mfi-only-v1` @ `2d|14|15/85` | **FAIL**(0.22) | SKIP | SKIP |
| `mfi-only-v1` @ `2d|14|20/80` | **FAIL**(0.20) | SKIP | SKIP |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | cmf-flow-v1 | 4h|p20|A | 68 | 27.94% | -6.50% | +28.93% | -0.225 | -0.03% | **FAIL** |
| 2 | cmf-flow-v1 | 7h|p20|A | 36 | 33.33% | +35.16% | +28.67% | 1.227 | +0.94% | **PASS** |
| 3 | cmf-flow-v1 | 7h|p21|A | 38 | 31.58% | +26.99% | +28.67% | 0.941 | +0.77% | **FAIL** |
| 4 | mfi-only-v1 | 2d|14|15/85 | 1 | 100.00% | +4.75% | +21.44% | 0.221 | +0.12% | **FAIL** |
| 5 | mfi-only-v1 | 2d|14|20/80 | 1 | 100.00% | +4.27% | +21.44% | 0.199 | +0.11% | **FAIL** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | cmf-flow-v1 | 4h|p20|A | 266 | 31.20% | -55.62% | +12.23% | -4.547 | -1.10% |
| 2 | cmf-flow-v1 | 7h|p20|A | 150 | 31.33% | -7.45% | +9.43% | -0.790 | +0.62% |
| 3 | cmf-flow-v1 | 7h|p21|A | 151 | 32.45% | -25.19% | +9.43% | -2.671 | +0.14% |
| 4 | mfi-only-v1 | 2d|14|15/85 | 2 | 50.00% | -1.86% | +5.62% | -0.331 | -0.04% |
| 5 | mfi-only-v1 | 2d|14|20/80 | 2 | 50.00% | -7.61% | +5.62% | -1.356 | -0.18% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | cmf-flow-v1 | 4h|p20|A | — | — | — | — | — | — | **SKIP** |
| 2 | cmf-flow-v1 | 7h|p20|A | 46 | 32.61% | -2.21% | +28.28% | -0.078 | +0.08% | **FAIL** |
| 3 | cmf-flow-v1 | 7h|p21|A | — | — | — | — | — | — | **SKIP** |
| 4 | mfi-only-v1 | 2d|14|15/85 | — | — | — | — | — | — | **SKIP** |
| 5 | mfi-only-v1 | 2d|14|20/80 | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | cmf-flow-v1 | 4h|p20|A | — | — | — | — | — | SKIP |
| 2 | cmf-flow-v1 | 7h|p20|A | 153 | 32.68% | +0.94% | -17.47% | -0.054 | +0.96% |
| 3 | cmf-flow-v1 | 7h|p21|A | — | — | — | — | — | SKIP |
| 4 | mfi-only-v1 | 2d|14|15/85 | — | — | — | — | — | SKIP |
| 5 | mfi-only-v1 | 2d|14|20/80 | — | — | — | — | — | SKIP |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | cmf-flow-v1 | 4h|p20|A | — | — | — | — | — | — | **SKIP** |
| 2 | cmf-flow-v1 | 7h|p20|A | — | — | — | — | — | — | **SKIP** |
| 3 | cmf-flow-v1 | 7h|p21|A | — | — | — | — | — | — | **SKIP** |
| 4 | mfi-only-v1 | 2d|14|15/85 | — | — | — | — | — | — | **SKIP** |
| 5 | mfi-only-v1 | 2d|14|20/80 | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | cmf-flow-v1 | 4h|p20|A | — | — | — | — | — | SKIP |
| 2 | cmf-flow-v1 | 7h|p20|A | — | — | — | — | — | SKIP |
| 3 | cmf-flow-v1 | 7h|p21|A | — | — | — | — | — | SKIP |
| 4 | mfi-only-v1 | 2d|14|15/85 | — | — | — | — | — | SKIP |
| 5 | mfi-only-v1 | 2d|14|20/80 | — | — | — | — | — | SKIP |

## Cell detail

### `ETHUSDT` · `cmf-flow-v1` @ `4h|p20|A` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 68 | 19/49 | 27.94% | -6.50% | +28.93% | -0.225 | 37.21% | **FAIL** |
| 6m | ops | 2.5% | 68 | 19/49 | 27.94% | -0.03% | +28.93% | -0.001 | 1.14% | **—** |
| full(~2y) | gate | 100% | 266 | 83/183 | 31.20% | -55.62% | +12.23% | -4.547 | 78.24% | **FAIL** |
| full(~2y) | ops | 2.5% | 266 | 83/183 | 31.20% | -1.10% | +12.23% | -0.090 | 3.62% | **—** |

### `ETHUSDT` · `cmf-flow-v1` @ `7h|p20|A` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 36 | 12/24 | 33.33% | +35.16% | +28.67% | 1.227 | 24.54% | **PASS** |
| 6m | ops | 2.5% | 36 | 12/24 | 33.33% | +0.94% | +28.67% | 0.033 | 0.69% | **—** |
| full(~2y) | gate | 100% | 150 | 47/103 | 31.33% | -7.45% | +9.43% | -0.790 | 64.63% | **FAIL** |
| full(~2y) | ops | 2.5% | 150 | 47/103 | 31.33% | +0.62% | +9.43% | 0.066 | 2.41% | **—** |

### `ETHUSDT` · `cmf-flow-v1` @ `7h|p21|A` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 38 | 12/26 | 31.58% | +26.99% | +28.67% | 0.941 | 23.26% | **FAIL** |
| 6m | ops | 2.5% | 38 | 12/26 | 31.58% | +0.77% | +28.67% | 0.027 | 0.65% | **—** |
| full(~2y) | gate | 100% | 151 | 49/102 | 32.45% | -25.19% | +9.43% | -2.671 | 71.26% | **FAIL** |
| full(~2y) | ops | 2.5% | 151 | 49/102 | 32.45% | +0.14% | +9.43% | 0.015 | 3.02% | **—** |

### `ETHUSDT` · `mfi-only-v1` @ `2d|14|15/85` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 1 | 1/0 | 100.00% | +4.75% | +21.44% | 0.221 | 12.71% | **FAIL** |
| 6m | ops | 2.5% | 1 | 1/0 | 100.00% | +0.12% | +21.44% | 0.006 | 0.34% | **—** |
| full(~2y) | gate | 100% | 2 | 1/1 | 50.00% | -1.86% | +5.62% | -0.331 | 20.23% | **FAIL** |
| full(~2y) | ops | 2.5% | 2 | 1/1 | 50.00% | -0.04% | +5.62% | -0.007 | 0.56% | **—** |

### `ETHUSDT` · `mfi-only-v1` @ `2d|14|20/80` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 1 | 1/0 | 100.00% | +4.27% | +21.44% | 0.199 | 12.71% | **FAIL** |
| 6m | ops | 2.5% | 1 | 1/0 | 100.00% | +0.11% | +21.44% | 0.005 | 0.34% | **—** |
| full(~2y) | gate | 100% | 2 | 1/1 | 50.00% | -7.61% | +5.62% | -1.356 | 20.60% | **FAIL** |
| full(~2y) | ops | 2.5% | 2 | 1/1 | 50.00% | -0.18% | +5.62% | -0.032 | 0.55% | **—** |

### `SOLUSDT` · `cmf-flow-v1` @ `4h|p20|A` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `cmf-flow-v1` @ `7h|p21|A` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `mfi-only-v1` @ `2d|14|15/85` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `mfi-only-v1` @ `2d|14|20/80` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `cmf-flow-v1` @ `7h|p20|A` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 46 | 15/31 | 32.61% | -2.21% | +28.28% | -0.078 | 30.50% | **FAIL** |
| 6m | ops | 2.5% | 46 | 15/31 | 32.61% | +0.08% | +28.28% | 0.003 | 0.89% | **—** |
| full(~2y) | gate | 100% | 153 | 50/103 | 32.68% | +0.94% | -17.47% | -0.054 | 61.92% | **PASS** |
| full(~2y) | ops | 2.5% | 153 | 50/103 | 32.68% | +0.96% | -17.47% | -0.055 | 2.31% | **—** |

### `BNBUSDT` · `cmf-flow-v1` @ `4h|p20|A` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `cmf-flow-v1` @ `7h|p20|A` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `cmf-flow-v1` @ `7h|p21|A` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `mfi-only-v1` @ `2d|14|15/85` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `mfi-only-v1` @ `2d|14|20/80` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

## Survivors

_None (full ETH→SOL→BNB). ETH PASS=1; SOL PASS=0; BNB PASS=0._

## Caveats

- Stop-ladder: later symbols only run on cells that PASS the prior rung.
- Frozen params from fresh-wave-v5 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- elder / linreg / UO hard-stopped on BTC — not OOS'd.
- Not wired to paper/alerts/webhook. Hold PR #23 unmerged (push only).
- Same mtf_ohlcv aggregation + fresh_wave_v5 signal code as BTC scoreboard.

