# owned-tf-sweep-v1-eth-oos

_Generated: 2026-09-06 00:14 UTC_

**RESEARCH ONLY — ETHUSDT OOS on BTC PASS cells. Not paper/live. No retunes.**

## Scope

- Parent: `owned-tf-sweep-v1` BTC PASS cells (frozen params / TF / agg)
- Symbol: **ETHUSDT** only
- Costs: 0.10%/side fee + 5 bps slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate: 6m Mode-A return ≥ **1.2 × ETH B&H** (same window); WR informational
- Agg: 5m/1d native cache; UTC bucket; same Path B harness under `mtf_ohlcv/`

## Cells (priority order)

1. `ema-rsi-trend-v1.1` @ `6h`
2. `sma200-trend-v1` @ `9h`
3. `openproxy-M1` @ `12h`
4. `ema-rsi-trend-v1.1` @ `9h`

## 6m Mode-A gate table (ETH)

| # | Strategy | TF | Trades | 6m WR | Mode-A ret | ETH B&H | ret/B&H | Ops ret | PASS/FAIL |
|---|----------|----|--------|-------|------------|---------|---------|---------|-----------|
| 1 | ema-rsi-trend-v1.1 | 6h | 8 | 50.00% | +23.24% | +25.42% | 0.914 | +0.60% | **FAIL** |
| 2 | sma200-trend-v1 | 9h | 3 | 33.33% | +23.57% | +25.79% | 0.914 | +0.62% | **FAIL** |
| 3 | openproxy-M1 | 12h | 8 | 50.00% | +11.43% | +25.93% | 0.441 | +0.31% | **FAIL** |
| 4 | ema-rsi-trend-v1.1 | 9h | 3 | 66.67% | +47.72% | +25.79% | 1.851 | +1.14% | **PASS** |

## Full window (~2y) Mode-A (info)

| # | Strategy | TF | Trades | WR | Mode-A ret | ETH B&H | ret/B&H | Ops ret |
|---|----------|----|--------|----|------------|---------|---------|---------|
| 1 | ema-rsi-trend-v1.1 | 6h | 27 | 25.93% | -21.11% | +4.71% | -4.484 | -0.32% |
| 2 | sma200-trend-v1 | 9h | 16 | 25.00% | +115.60% | +3.13% | 36.990 | +2.72% |
| 3 | openproxy-M1 | 12h | 33 | 36.36% | +31.47% | +4.53% | 6.954 | +0.96% |
| 4 | ema-rsi-trend-v1.1 | 9h | 14 | 35.71% | +95.60% | +3.13% | 30.589 | +2.26% |

## Cell detail

### 1. `ema-rsi-trend-v1.1` @ `6h` — 6m gate **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | ETH B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|---------|-------|-----|------|
| 6m | gate | 100% | 8 | 4/4 | 50.00% | +23.24% | +25.42% | 0.914 | 17.81% | **FAIL** |
| 6m | ops | 2.5% | 8 | 4/4 | 50.00% | +0.60% | +25.42% | 0.024 | 0.51% | **—** |
| full(~2y) | gate | 100% | 27 | 7/20 | 25.93% | -21.11% | +4.71% | -4.484 | 53.08% | **FAIL** |
| full(~2y) | ops | 2.5% | 27 | 7/20 | 25.93% | -0.32% | +4.71% | -0.067 | 1.84% | **—** |

### 2. `sma200-trend-v1` @ `9h` — 6m gate **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | ETH B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|---------|-------|-----|------|
| 6m | gate | 100% | 3 | 1/2 | 33.33% | +23.57% | +25.79% | 0.914 | 15.14% | **FAIL** |
| 6m | ops | 2.5% | 3 | 1/2 | 33.33% | +0.62% | +25.79% | 0.024 | 0.42% | **—** |
| full(~2y) | gate | 100% | 16 | 4/12 | 25.00% | +115.60% | +3.13% | 36.990 | 36.52% | **PASS** |
| full(~2y) | ops | 2.5% | 16 | 4/12 | 25.00% | +2.72% | +3.13% | 0.870 | 1.48% | **—** |

### 3. `openproxy-M1` @ `12h` — 6m gate **FAIL**

| Window | Mode | Size | Trades | W/L | WR | Ret | ETH B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|---------|-------|-----|------|
| 6m | gate | 100% | 8 | 4/4 | 50.00% | +11.43% | +25.93% | 0.441 | 19.19% | **FAIL** |
| 6m | ops | 2.5% | 8 | 4/4 | 50.00% | +0.31% | +25.93% | 0.012 | 0.54% | **—** |
| full(~2y) | gate | 100% | 33 | 12/21 | 36.36% | +31.47% | +4.53% | 6.954 | 35.10% | **PASS** |
| full(~2y) | ops | 2.5% | 33 | 12/21 | 36.36% | +0.96% | +4.53% | 0.212 | 1.09% | **—** |

### 4. `ema-rsi-trend-v1.1` @ `9h` — 6m gate **PASS**

| Window | Mode | Size | Trades | W/L | WR | Ret | ETH B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|---------|-------|-----|------|
| 6m | gate | 100% | 3 | 2/1 | 66.67% | +47.72% | +25.79% | 1.851 | 12.97% | **PASS** |
| 6m | ops | 2.5% | 3 | 2/1 | 66.67% | +1.14% | +25.79% | 0.044 | 0.37% | **—** |
| full(~2y) | gate | 100% | 14 | 5/9 | 35.71% | +95.60% | +3.13% | 30.589 | 36.91% | **PASS** |
| full(~2y) | ops | 2.5% | 14 | 5/9 | 35.71% | +2.26% | +3.13% | 0.724 | 1.21% | **—** |

## Caveats

- Frozen params from owned-tf-sweep-v1 / Path B — **no retune on ETH**.
- Gate PASS/FAIL only on 6m Mode-A vs ETH B&H; full window + ops are informational.
- Not wired to paper/alerts/webhook.
- Same mtf_ohlcv aggregation + signal code as BTC sweep.
