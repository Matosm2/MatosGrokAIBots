# fresh-wave-v8-oos-ladder

_Generated: 2026-09-07 08:51 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v8 PASS_6m cells. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v8` BTC PASS_6m cells (frozen params / TF)
- Strategy stop-ladder: **ETH → SOL on ETH PASS → BNB on SOL PASS** (STOP that cell on first FAIL)
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window), ≥1 trade; also report full(~2y) + WR + n
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen: Gann HiLo n=3; FI EMA(13); Cyber α=0.07; Fractals wings=2 (5-bar)
- Hard-stop (not OOS): asian-london-break-v1

## Cells (frozen, CoS / best-n first)

1. `force-index-13-v1` @ `12h|ema13` — BTC PASS_6m 1.604× n=17
2. `gann-hilo-activator-v1` @ `2d|n3` — BTC PASS_6m 2.016× n=6
3. `force-index-13-v1` @ `2d|ema13` — BTC PASS_6m 1.515× n=6
4. `cyber-cycle-v1` @ `2d|a0.07` — BTC PASS_6m 1.548× n=6
5. `williams-fractals-v1` @ `1d|w2` — BTC PASS_6m 1.620× n=3
6. `williams-fractals-v1` @ `2d|w2` — BTC PASS_6m 1.685× n=1

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `force-index-13-v1` @ `12h|ema13` | **FAIL**(0.90) | SKIP | SKIP |
| `gann-hilo-activator-v1` @ `2d|n3` | **PASS**(1.69) | **FAIL**(1.06) | SKIP |
| `force-index-13-v1` @ `2d|ema13` | **PASS**(1.78) | **FAIL**(0.99) | SKIP |
| `cyber-cycle-v1` @ `2d|a0.07` | **FAIL**(0.57) | SKIP | SKIP |
| `williams-fractals-v1` @ `1d|w2` | **FAIL**(0.59) | SKIP | SKIP |
| `williams-fractals-v1` @ `2d|w2` | **PASS**(1.42) | **FAIL**(-0.55) | SKIP |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | force-index-13-v1 | 12h|ema13 | 21 | 28.57% | +23.69% | +26.22% | 0.904 | +0.65% | **FAIL** |
| 2 | gann-hilo-activator-v1 | 2d|n3 | 3 | 66.67% | +36.30% | +21.44% | 1.693 | +0.95% | **PASS** |
| 3 | force-index-13-v1 | 2d|ema13 | 6 | 33.33% | +38.25% | +21.44% | 1.784 | +0.98% | **PASS** |
| 4 | cyber-cycle-v1 | 2d|a0.07 | 8 | 50.00% | +12.20% | +21.44% | 0.569 | +0.33% | **FAIL** |
| 5 | williams-fractals-v1 | 1d|w2 | 3 | 100.00% | +14.77% | +25.04% | 0.590 | +0.36% | **FAIL** |
| 6 | williams-fractals-v1 | 2d|w2 | 2 | 50.00% | +30.54% | +21.44% | 1.424 | +0.82% | **PASS** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | force-index-13-v1 | 12h|ema13 | 86 | 23.26% | -4.99% | +10.11% | -0.494 | +0.59% |
| 2 | gann-hilo-activator-v1 | 2d|n3 | 22 | 36.36% | +8.49% | +5.62% | 1.511 | +0.91% |
| 3 | force-index-13-v1 | 2d|ema13 | 19 | 31.58% | +154.49% | +5.62% | 27.508 | +3.17% |
| 4 | cyber-cycle-v1 | 2d|a0.07 | 35 | 37.14% | -15.94% | +5.62% | -2.838 | +0.10% |
| 5 | williams-fractals-v1 | 1d|w2 | 16 | 50.00% | +19.87% | +9.61% | 2.069 | +1.07% |
| 6 | williams-fractals-v1 | 2d|w2 | 7 | 57.14% | +166.06% | +5.62% | 29.570 | +2.95% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | force-index-13-v1 | 12h|ema13 | — | — | — | — | — | — | **SKIP** |
| 2 | gann-hilo-activator-v1 | 2d|n3 | 7 | 28.57% | +22.57% | +21.28% | 1.061 | +0.65% | **FAIL** |
| 3 | force-index-13-v1 | 2d|ema13 | 6 | 33.33% | +21.10% | +21.28% | 0.992 | +0.63% | **FAIL** |
| 4 | cyber-cycle-v1 | 2d|a0.07 | — | — | — | — | — | — | **SKIP** |
| 5 | williams-fractals-v1 | 1d|w2 | — | — | — | — | — | — | **SKIP** |
| 6 | williams-fractals-v1 | 2d|w2 | 4 | 25.00% | -11.73% | +21.28% | -0.551 | -0.22% | **FAIL** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | force-index-13-v1 | 12h|ema13 | — | — | — | — | — | SKIP |
| 2 | gann-hilo-activator-v1 | 2d|n3 | 25 | 44.00% | -13.48% | -22.27% | 0.605 | +0.33% |
| 3 | force-index-13-v1 | 2d|ema13 | 23 | 43.48% | -18.82% | -22.27% | 0.845 | -0.17% |
| 4 | cyber-cycle-v1 | 2d|a0.07 | — | — | — | — | — | SKIP |
| 5 | williams-fractals-v1 | 1d|w2 | — | — | — | — | — | SKIP |
| 6 | williams-fractals-v1 | 2d|w2 | 10 | 40.00% | -20.49% | -22.27% | 0.920 | -0.13% |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | force-index-13-v1 | 12h|ema13 | — | — | — | — | — | — | **SKIP** |
| 2 | gann-hilo-activator-v1 | 2d|n3 | — | — | — | — | — | — | **SKIP** |
| 3 | force-index-13-v1 | 2d|ema13 | — | — | — | — | — | — | **SKIP** |
| 4 | cyber-cycle-v1 | 2d|a0.07 | — | — | — | — | — | — | **SKIP** |
| 5 | williams-fractals-v1 | 1d|w2 | — | — | — | — | — | — | **SKIP** |
| 6 | williams-fractals-v1 | 2d|w2 | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | force-index-13-v1 | 12h|ema13 | — | — | — | — | — | SKIP |
| 2 | gann-hilo-activator-v1 | 2d|n3 | — | — | — | — | — | SKIP |
| 3 | force-index-13-v1 | 2d|ema13 | — | — | — | — | — | SKIP |
| 4 | cyber-cycle-v1 | 2d|a0.07 | — | — | — | — | — | SKIP |
| 5 | williams-fractals-v1 | 1d|w2 | — | — | — | — | — | SKIP |
| 6 | williams-fractals-v1 | 2d|w2 | — | — | — | — | — | SKIP |

## Cell detail

### `ETHUSDT` · `force-index-13-v1` @ `12h|ema13` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 21 | 6/15 | 28.57% | +23.69% | +26.22% | 0.904 | 21.70% | **FAIL** |
| 6m | ops | 2.5% | 21 | 6/15 | 28.57% | +0.65% | +26.22% | 0.025 | 0.62% | **—** |
| full(~2y) | gate | 100% | 86 | 20/66 | 23.26% | -4.99% | +10.11% | -0.494 | 53.39% | **FAIL** |
| full(~2y) | ops | 2.5% | 86 | 20/66 | 23.26% | +0.59% | +10.11% | 0.058 | 1.84% | **—** |

### `ETHUSDT` · `gann-hilo-activator-v1` @ `2d|n3` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 3 | 2/1 | 66.67% | +36.30% | +21.44% | 1.693 | 11.69% | **PASS** |
| 6m | ops | 2.5% | 3 | 2/1 | 66.67% | +0.95% | +21.44% | 0.044 | 0.31% | **—** |
| full(~2y) | gate | 100% | 22 | 8/14 | 36.36% | +8.49% | +5.62% | 1.511 | 59.69% | **PASS** |
| full(~2y) | ops | 2.5% | 22 | 8/14 | 36.36% | +0.91% | +5.62% | 0.161 | 2.19% | **—** |

### `ETHUSDT` · `force-index-13-v1` @ `2d|ema13` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 6 | 2/4 | 33.33% | +38.25% | +21.44% | 1.784 | 16.46% | **PASS** |
| 6m | ops | 2.5% | 6 | 2/4 | 33.33% | +0.98% | +21.44% | 0.046 | 0.47% | **—** |
| full(~2y) | gate | 100% | 19 | 6/13 | 31.58% | +154.49% | +5.62% | 27.508 | 38.56% | **PASS** |
| full(~2y) | ops | 2.5% | 19 | 6/13 | 31.58% | +3.17% | +5.62% | 0.564 | 1.45% | **—** |

### `ETHUSDT` · `cyber-cycle-v1` @ `2d|a0.07` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 8 | 4/4 | 50.00% | +12.20% | +21.44% | 0.569 | 12.97% | **FAIL** |
| 6m | ops | 2.5% | 8 | 4/4 | 50.00% | +0.33% | +21.44% | 0.015 | 0.35% | **—** |
| full(~2y) | gate | 100% | 35 | 13/22 | 37.14% | -15.94% | +5.62% | -2.838 | 54.39% | **FAIL** |
| full(~2y) | ops | 2.5% | 35 | 13/22 | 37.14% | +0.10% | +5.62% | 0.017 | 1.84% | **—** |

### `ETHUSDT` · `williams-fractals-v1` @ `1d|w2` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 3 | 3/0 | 100.00% | +14.77% | +25.04% | 0.590 | 8.66% | **FAIL** |
| 6m | ops | 2.5% | 3 | 3/0 | 100.00% | +0.36% | +25.04% | 0.014 | 0.23% | **—** |
| full(~2y) | gate | 100% | 16 | 8/8 | 50.00% | +19.87% | +9.61% | 2.069 | 54.29% | **PASS** |
| full(~2y) | ops | 2.5% | 16 | 8/8 | 50.00% | +1.07% | +9.61% | 0.111 | 1.85% | **—** |

### `ETHUSDT` · `williams-fractals-v1` @ `2d|w2` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 2 | 1/1 | 50.00% | +30.54% | +21.44% | 1.424 | 14.49% | **PASS** |
| 6m | ops | 2.5% | 2 | 1/1 | 50.00% | +0.82% | +21.44% | 0.038 | 0.36% | **—** |
| full(~2y) | gate | 100% | 7 | 4/3 | 57.14% | +166.06% | +5.62% | 29.570 | 29.63% | **PASS** |
| full(~2y) | ops | 2.5% | 7 | 4/3 | 57.14% | +2.95% | +5.62% | 0.526 | 0.86% | **—** |

### `SOLUSDT` · `force-index-13-v1` @ `12h|ema13` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `cyber-cycle-v1` @ `2d|a0.07` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `williams-fractals-v1` @ `1d|w2` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `gann-hilo-activator-v1` @ `2d|n3` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 7 | 2/5 | 28.57% | +22.57% | +21.28% | 1.061 | 15.60% | **FAIL** |
| 6m | ops | 2.5% | 7 | 2/5 | 28.57% | +0.65% | +21.28% | 0.030 | 0.42% | **—** |
| full(~2y) | gate | 100% | 25 | 11/14 | 44.00% | -13.48% | -22.27% | 0.605 | 58.49% | **PASS** |
| full(~2y) | ops | 2.5% | 25 | 11/14 | 44.00% | +0.33% | -22.27% | -0.015 | 1.77% | **—** |

### `SOLUSDT` · `force-index-13-v1` @ `2d|ema13` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 6 | 2/4 | 33.33% | +21.10% | +21.28% | 0.992 | 21.10% | **FAIL** |
| 6m | ops | 2.5% | 6 | 2/4 | 33.33% | +0.63% | +21.28% | 0.029 | 0.60% | **—** |
| full(~2y) | gate | 100% | 23 | 10/13 | 43.48% | -18.82% | -22.27% | 0.845 | 58.68% | **PASS** |
| full(~2y) | ops | 2.5% | 23 | 10/13 | 43.48% | -0.17% | -22.27% | 0.007 | 2.12% | **—** |

### `SOLUSDT` · `williams-fractals-v1` @ `2d|w2` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 4 | 1/3 | 25.00% | -11.73% | +21.28% | -0.551 | 26.20% | **FAIL** |
| 6m | ops | 2.5% | 4 | 1/3 | 25.00% | -0.22% | +21.28% | -0.010 | 0.71% | **—** |
| full(~2y) | gate | 100% | 10 | 4/6 | 40.00% | -20.49% | -22.27% | 0.920 | 59.89% | **PASS** |
| full(~2y) | ops | 2.5% | 10 | 4/6 | 40.00% | -0.13% | -22.27% | 0.006 | 2.23% | **—** |

### `BNBUSDT` · `force-index-13-v1` @ `12h|ema13` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `gann-hilo-activator-v1` @ `2d|n3` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `force-index-13-v1` @ `2d|ema13` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `cyber-cycle-v1` @ `2d|a0.07` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `williams-fractals-v1` @ `1d|w2` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `williams-fractals-v1` @ `2d|w2` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

## Survivors

_None (full ETH→SOL→BNB). ETH PASS=3; SOL PASS=0; BNB PASS=0._

## Caveats

- Stop-ladder: later symbols only run if prior rung PASSes; STOP that cell on first FAIL.
- Frozen params from fresh-wave-v8 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- asian-london-break hard-stopped on BTC — not OOS'd.
- Not wired to paper/alerts/webhook. Hold PR #26 unmerged (push only).
- Same mtf_ohlcv aggregation + fresh_wave_v8 signal code as BTC scoreboard.

