# fresh-wave-v7-oos-ladder

_Generated: 2026-09-07 08:22 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v7 PASS_6m cells. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v7` BTC PASS_6m cells (frozen params / TF)
- Strategy stop-ladder: **ETH → SOL on ETH PASS → BNB on SOL PASS** (STOP that cell on first FAIL)
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window), ≥1 trade; also report full(~2y) + WR + n
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot.
- Params frozen: Elder Impulse EMA(13) cancel(2) + MACD-hist; no FI; no market-on-green
- Hard-stop (not OOS): rvi-signal-v1, chop-breakout-v1

## Cells (frozen)

1. `elder-impulse-v1` @ `1d|ema13|cancel2` — BTC PASS_6m 1.231× n=14
2. `elder-impulse-v1` @ `2d|ema13|cancel2` — BTC PASS_6m 1.826× n=6

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `elder-impulse-v1` @ `1d|ema13|cancel2` | **PASS**(1.37) | **FAIL**(0.98) | SKIP |
| `elder-impulse-v1` @ `2d|ema13|cancel2` | **FAIL**(1.10) | SKIP | SKIP |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | elder-impulse-v1 | 1d|ema13|cancel2 | 14 | 42.86% | +34.29% | +25.04% | 1.369 | +0.87% | **PASS** |
| 2 | elder-impulse-v1 | 2d|ema13|cancel2 | 5 | 40.00% | +23.66% | +21.44% | 1.103 | +0.73% | **FAIL** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | elder-impulse-v1 | 1d|ema13|cancel2 | 54 | 27.78% | -22.27% | +9.61% | -2.318 | +0.11% |
| 2 | elder-impulse-v1 | 2d|ema13|cancel2 | 26 | 26.92% | -3.82% | +5.62% | -0.679 | +0.94% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | elder-impulse-v1 | 1d|ema13|cancel2 | 15 | 33.33% | +23.16% | +23.59% | 0.982 | +0.69% | **FAIL** |
| 2 | elder-impulse-v1 | 2d|ema13|cancel2 | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | elder-impulse-v1 | 1d|ema13|cancel2 | 57 | 31.58% | -18.47% | -17.78% | 1.039 | +0.15% |
| 2 | elder-impulse-v1 | 2d|ema13|cancel2 | — | — | — | — | — | SKIP |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | elder-impulse-v1 | 1d|ema13|cancel2 | — | — | — | — | — | — | **SKIP** |
| 2 | elder-impulse-v1 | 2d|ema13|cancel2 | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | elder-impulse-v1 | 1d|ema13|cancel2 | — | — | — | — | — | SKIP |
| 2 | elder-impulse-v1 | 2d|ema13|cancel2 | — | — | — | — | — | SKIP |

## Cell detail

### `ETHUSDT` · `elder-impulse-v1` @ `1d|ema13|cancel2` — 6m **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 14 | 6/8 | 42.86% | +34.29% | +25.04% | 1.369 | 16.02% | **PASS** |
| 6m | ops | 2.5% | 14 | 6/8 | 42.86% | +0.87% | +25.04% | 0.035 | 0.45% | **—** |
| full(~2y) | gate | 100% | 54 | 15/39 | 27.78% | -22.27% | +9.61% | -2.318 | 64.98% | **FAIL** |
| full(~2y) | ops | 2.5% | 54 | 15/39 | 27.78% | +0.11% | +9.61% | 0.011 | 2.56% | **—** |

### `ETHUSDT` · `elder-impulse-v1` @ `2d|ema13|cancel2` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 5 | 2/3 | 40.00% | +23.66% | +21.44% | 1.103 | 20.86% | **FAIL** |
| 6m | ops | 2.5% | 5 | 2/3 | 40.00% | +0.73% | +21.44% | 0.034 | 0.57% | **—** |
| full(~2y) | gate | 100% | 26 | 7/19 | 26.92% | -3.82% | +5.62% | -0.679 | 62.10% | **FAIL** |
| full(~2y) | ops | 2.5% | 26 | 7/19 | 26.92% | +0.94% | +5.62% | 0.168 | 2.49% | **—** |

### `SOLUSDT` · `elder-impulse-v1` @ `2d|ema13|cancel2` — 6m **SKIP**

_Skipped:_ prior rung ETHUSDT FAIL/ERROR/SKIP

### `SOLUSDT` · `elder-impulse-v1` @ `1d|ema13|cancel2` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 15 | 5/10 | 33.33% | +23.16% | +23.59% | 0.982 | 20.88% | **FAIL** |
| 6m | ops | 2.5% | 15 | 5/10 | 33.33% | +0.69% | +23.59% | 0.029 | 0.58% | **—** |
| full(~2y) | gate | 100% | 57 | 18/39 | 31.58% | -18.47% | -17.78% | 1.039 | 70.16% | **PASS** |
| full(~2y) | ops | 2.5% | 57 | 18/39 | 31.58% | +0.15% | -17.78% | -0.008 | 2.75% | **—** |

### `BNBUSDT` · `elder-impulse-v1` @ `1d|ema13|cancel2` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

### `BNBUSDT` · `elder-impulse-v1` @ `2d|ema13|cancel2` — 6m **SKIP**

_Skipped:_ ladder stopped: SOLUSDT had zero PASS

## Survivors

_None (full ETH→SOL→BNB). ETH PASS=1; SOL PASS=0; BNB PASS=0._

## Caveats

- Stop-ladder: later symbols only run if prior rung PASSes; STOP that cell on first FAIL.
- Frozen params from fresh-wave-v7 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- rvi-signal / chop-breakout hard-stopped on BTC — not OOS'd.
- Not wired to paper/alerts/webhook. Hold PR #25 unmerged (push only).
- Same mtf_ohlcv aggregation + fresh_wave_v7 signal code as BTC scoreboard.

