# owned-tf-sweep-v1-dual-mom-oos

_Generated: 2026-09-06 00:26 UTC_

**RESEARCH ONLY — dual-mom-btc-eth-v1 @ 1d + 2d. Not paper/live. No param spray.**

## Scope

- Strategy: **`dual-mom-btc-eth-v1`** only (lookback **20** bars, frozen)
- TFs: **`1d`, `2d`** (longwin PASS_longwin dual-mom cells; no other TFs)
- Parent harness: `path_b/mtf_ohlcv` + `run_dual_mom` (same as owned-tf-sweep-v1-longwin)
- Costs: **0.10%/side** fee + **5 bps** slip
- Mode-A gate size: **100%** equity; Mode-B ops: **2.5%** (parallel, not scored)
- Gate (both windows): Mode-A ≥ **1.2× 50/50 BTC+ETH B&H** (dual-mom gate rule)
- **Out of scope:** ema-rsi / sma200 / openproxy ETH OOS (PR #16) — not rerun

## ETH B&H framing (read this)

- **Primary / gate benchmark = 50/50 BTC+ETH buy-and-hold** on the same window.
  This is the dual-mom standing rule (same as owned-tf-sweep / longwin).
- **NOT gated vs ETH-only B&H.** Unlike single-asset ETH OOS (`owned-tf-sweep-v1-eth-oos`),
  dual-mom rotates between BTC and ETH (or flat), so ETH-only B&H is the wrong yardstick.
- BTC-only and ETH-only B&H are reported below as **informational framing only**
  so readers can compare the 50/50 gate denominator to single-asset paths.
- Strategy already consumes ETHUSDT (paired with BTCUSDT); this is not an
  “apply BTC params to ETH” OOS — it is a focused dual-mom report at the two
  longwin-PASS TFs.

## PASS/FAIL table (Mode-A vs 50/50)

| TF | full(~2y) gate | Mode-A % | 50/50 B&H % | ratio | trades | WR % | 6m gate | Mode-A % | 50/50 B&H % | ratio | trades | WR % |
|----|----------------|----------|-------------|-------|--------|------|---------|----------|-------------|-------|--------|------|
| `1d` | **PASS** | +104.15 | +29.76 | 3.500 | 70 | 41.4 | **FAIL** | +25.13 | +24.57 | 1.023 | 13 | 53.8 |
| `2d` | **PASS** | +110.96 | +27.61 | 4.019 | 30 | 36.7 | **FAIL** | +9.23 | +19.83 | 0.465 | 5 | 40.0 |

## B&H framing by window (informational)

| TF | Window | 50/50 B&H % (gate denom) | BTC-only B&H % | ETH-only B&H % |
|----|--------|--------------------------|----------------|----------------|
| `1d` | full(~2y) | +29.76 | +48.03 | +11.48 |
| `1d` | 6m | +24.57 | +21.09 | +28.06 |
| `2d` | full(~2y) | +27.61 | +47.37 | +7.84 |
| `2d` | 6m | +19.83 | +16.64 | +23.03 |

## Cell detail (Mode-A + ops)

### `dual-mom-btc-eth-v1` @ `1d` — full **PASS** / 6m **FAIL**

- _Gate = Mode-A vs 50/50 BTC+ETH B&H (dual-mom rule). ETH-only / BTC-only B&H are framing only — not the gate._

| Window | Mode | Size | Trades | W/L | WR | Ret | 50/50 B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----------|-------|-----|------|
| full(~2y) | gate | 100% | 70 | 29/41 | 41.43% | +104.15% | +29.76% | 3.500 | 39.06% | **PASS** |
| full(~2y) | ops | 2.5% | 70 | 29/41 | 41.43% | +2.40% | +29.76% | 0.081 | 1.38% | **—** |
| 6m | gate | 100% | 13 | 7/6 | 53.85% | +25.13% | +24.57% | 1.023 | 19.91% | **FAIL** |
| 6m | ops | 2.5% | 13 | 7/6 | 53.85% | +0.59% | +24.57% | 0.024 | 0.57% | **—** |

### `dual-mom-btc-eth-v1` @ `2d` — full **PASS** / 6m **FAIL**

- _Gate = Mode-A vs 50/50 BTC+ETH B&H (dual-mom rule). ETH-only / BTC-only B&H are framing only — not the gate._

| Window | Mode | Size | Trades | W/L | WR | Ret | 50/50 B&H | ratio | MDD | Gate |
|--------|------|------|--------|-----|----|-----|-----------|-------|-----|------|
| full(~2y) | gate | 100% | 30 | 11/19 | 36.67% | +110.96% | +27.61% | 4.019 | 39.53% | **PASS** |
| full(~2y) | ops | 2.5% | 30 | 11/19 | 36.67% | +2.52% | +27.61% | 0.091 | 1.37% | **—** |
| 6m | gate | 100% | 5 | 2/3 | 40.00% | +9.23% | +19.83% | 0.465 | 19.54% | **FAIL** |
| 6m | ops | 2.5% | 5 | 2/3 | 40.00% | +0.34% | +19.83% | 0.017 | 0.52% | **—** |

## Caveats

- Frozen dual-mom lookback=20; same costs / Mode-A 100% as Path B.
- Agg: 1d native cache; 2d = 2×1d UTC bucket (mtf_ohlcv).
- full(~2y) and 6m both gated vs 50/50; neither uses ETH-only B&H.
- Not wired to paper / alerts / webhook. Hold merges.
- Reuses longwin dual-mom logic; numbers should match `owned-tf-sweep-v1-longwin-scoreboard.md` dual-mom @ 1d/2d rows.
