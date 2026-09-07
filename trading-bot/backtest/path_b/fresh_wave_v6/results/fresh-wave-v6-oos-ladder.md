# fresh-wave-v6-oos-ladder

_Generated: 2026-09-07 08:00 UTC_

**RESEARCH ONLY — OOS stop-ladder on fresh-wave-v6 PASS_6m cell. Not paper/live. No retunes. No Claude.**

## Scope

- Parent: `fresh-wave-v6` BTC PASS_6m cell (frozen params / TF)
- Strategy stop-ladder: **ETH → SOL on ETH PASS → BNB on SOL PASS** (STOP on first FAIL)
- Symbols: ETHUSDT → SOLUSDT → BNBUSDT
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × that symbol's B&H** (same window), ≥1 trade; also report full(~2y)
- Agg: 5m→sub-daily. Bar-close; long-only Spot.
- Params frozen: Twiggs MF period=21 Mode B (zero-cross) @ 3h
- Hard-stop (not OOS): mass-index-bulge-v1, kst-pring-v1, demarker-zone-v1, darvas-box-v1

## Cells (frozen)

1. `twiggs-mf-v1` @ `3h|p21|B` — BTC PASS_6m 1.269× n=52

## Stop-ladder matrix (6m Mode-A PASS/FAIL + ratio)

| Cell | ETHUSDT | SOLUSDT | BNBUSDT |
|------|---------|---------|---------|
| `twiggs-mf-v1` @ `3h|p21|B` | **FAIL**(-0.77) | SKIP | SKIP |

## 6m Mode-A gate — ETHUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | twiggs-mf-v1 | 3h|p21|B | 84 | 25.00% | -21.56% | +27.87% | -0.774 | -0.50% | **FAIL** |

## Full window (~2y) Mode-A — ETHUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | twiggs-mf-v1 | 3h|p21|B | 277 | 24.55% | -44.51% | +12.56% | -3.543 | -0.72% |

## 6m Mode-A gate — SOLUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | twiggs-mf-v1 | 3h|p21|B | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — SOLUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | twiggs-mf-v1 | 3h|p21|B | — | — | — | — | — | SKIP |

## 6m Mode-A gate — BNBUSDT

| # | Strategy | Cell | Trades | 6m WR | Mode-A ret | B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|------|--------|-------|------------|-----|---------|---------|-----------|
| 1 | twiggs-mf-v1 | 3h|p21|B | — | — | — | — | — | — | **SKIP** |

## Full window (~2y) Mode-A — BNBUSDT (info)

| # | Strategy | Cell | Trades | WR | Mode-A ret | B&H | ret/B&H | Ops ret |
|---|----------|------|--------|----|------------|-----|---------|---------|
| 1 | twiggs-mf-v1 | 3h|p21|B | — | — | — | — | — | SKIP |

## Cell detail

### `ETHUSDT` · `twiggs-mf-v1` @ `3h|p21|B` — 6m **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----|-------|-----|------|
| 6m | gate | 100% | 84 | 21/63 | 25.00% | -21.56% | +27.87% | -0.774 | 45.39% | **FAIL** |
| 6m | ops | 2.5% | 84 | 21/63 | 25.00% | -0.50% | +27.87% | -0.018 | 1.48% | **—** |
| full(~2y) | gate | 100% | 277 | 68/209 | 24.55% | -44.51% | +12.56% | -3.543 | 71.73% | **FAIL** |
| full(~2y) | ops | 2.5% | 277 | 68/209 | 24.55% | -0.72% | +12.56% | -0.057 | 3.02% | **—** |

### `SOLUSDT` · `twiggs-mf-v1` @ `3h|p21|B` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

### `BNBUSDT` · `twiggs-mf-v1` @ `3h|p21|B` — 6m **SKIP**

_Skipped:_ ladder stopped: ETHUSDT had zero PASS

## Survivors

_None (full ETH→SOL→BNB). ETH PASS=0; SOL PASS=0; BNB PASS=0._

## Caveats

- Stop-ladder: later symbols only run if prior rung PASSes; STOP on first FAIL.
- Frozen params from fresh-wave-v6 — **no retune on alts**.
- Gate PASS/FAIL only on 6m Mode-A vs that symbol's B&H; full + ops informational.
- mass-index / kst-pring / demarker / darvas hard-stopped on BTC — not OOS'd.
- Not wired to paper/alerts/webhook. Hold PR #24 unmerged (push only).
- Same mtf_ohlcv aggregation + fresh_wave_v6 signal code as BTC scoreboard.

