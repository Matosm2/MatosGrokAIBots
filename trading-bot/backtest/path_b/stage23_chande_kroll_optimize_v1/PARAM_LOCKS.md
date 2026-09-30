# PARAM_LOCKS.md — Stage-23 Chande Kroll Optimize v1 (Track B)

**Status:** PARAMETERS LOCKED BEFORE SCORING  
**Strategy ID:** `chande-kroll-stop-flip`  
**Research ID:** `stage23-chande-kroll-optimize-v1`  
**Run Mode:** RESEARCH / OPTIMIZE ONLY (no live / paper / webhook)  
**Track:** Track 1 (Internal Grok Bot). Track 2 Discord Meta Signals = OFF-LIMITS.  
**Date:** 2026-09-21  

---

## 1. Baseline Near-Miss Definition

From Stage-23 Dual SOL+BNB briefs (`stage23-dual-sol-bnb-briefs-2026-09-18.md` and CODING_KICK):
- **Banked near-miss:** `chande-kroll-stop-flip` with **(p=10, x=1.0, q=9)** reached **~1.194×** BTC Mode-A.
- Closest-to-gate this cycle per CoS, but still below the **1.20×** threshold.
- Trade count on Stage-23 was flagged around *n*≈9.
- **Optimization Goal:** Push BTC Mode-A past **1.194× → ≥1.20×** with **denser n ≫ 9**, then evaluate the full ladder **ETH → SOL → BNB** on **identical parameters** (never retune per coin).

---

## 2. Core Indicator & Signal Specification

### Construction (Two-Stage ATR Corridor):
```
Stage 1:
  atr = ta.atr(p)                      // Wilder smoothed ATR (RMA)
  highStop = ta.highest(high, p) - x * atr
  lowStop  = ta.lowest(low, p) + x * atr

Stage 2:
  stopShort = ta.highest(highStop, q)
  stopLong  = ta.lowest(lowStop, q)
```

### Signal Execution:
- **Mode A (Long-only first):**
  - Entry: `crossover(close, stopShort)` on closed bar.
  - Exit: `crossunder(close, stopLong)` on closed bar.
  - Pyramiding: 0 (spot long-only).
- **Mode B (Quality width filter):**
  - Entry: `crossover(close, stopShort)` AND `percentrank(stopShort - stopLong, wLen) > wMin`.
  - Exit: `crossunder(close, stopLong)`.
  - Only tested if Mode A over-whips; identical parameters across all four coins.

### Exclusions & Constraints:
- NOT Chandelier Exit (which uses single highest high - ATR).
- NOT SuperTrend (which uses HL2 ratchet).
- NOT Wilder Volatility System (which uses close ± ARC).
- NOT Parabolic SAR.
- No per-coin retuning.
- Closed-bar only (`process_orders_on_close=true`), no lookahead.
- Costs: fee 0.10%/side + slippage 0.050% adverse (5 bps).

---

## 3. Parameter Grid Locked for Sweep

### Baseline Anchor:
- `p = 10, x = 1.0, q = 9` (Banked near-miss ~1.194× BTC Mode-A)

### Primary Grid (LEAN Mode A First):
- **p (Lookback for ATR & Extremes):** `[8, 10, 12, 14]`
- **x (ATR Multiplier):** `[0.8, 1.0, 1.2, 1.5]`
- **q (Second-stage smoothing lookback):** `[5, 7, 9, 11, 14]`
- **Timeframes:** `1H` vs `4H`
- **Total Neighborhood Configurations:** 4 × 4 × 5 = 80 parameter combinations per timeframe (160 total per coin).

### Coins & Ladder Sequence:
- **Sequence:** BTCUSDT (LEAD) → ETHUSDT → SOLUSDT (PRIMARY CRITICAL) → BNBUSDT
- **Identical Parameters:** Every evaluation across the ladder MUST use identical (p, x, q, TF, Mode).

---

## 4. Evaluation Windows & Gates

### Primary Lead Gate (last 6 months):
- **Window:** Most recent 180 days (~6 months) of closed bars.
- **Criterion:** Mode-A Strategy Return ≥ **1.20× Buy & Hold Return** (with positive return & B&H > 0, or strategy outperforming flat/negative B&H).
- **Tiny-n Policy:**
  - BTC *n* ≤ 5: **FAIL** (even if ratio ≥ 1.20×).
  - Flag *n* ≈ 9.
  - Prefer *n* ≫ 9.
- **Smoke Gates:**
  - `btc_smoke`: Kill if Mode A 0-trade or chop under costs; kill if fails to beat 1.194× → ≥1.20×; kill if params inflated until n collapses.
  - `eth_smoke`: Kill if BTC clears ≥1.20× then ETH drops below 1.20×; kill if retuned.
  - `sol_smoke` (CRITICAL): Kill if BTC+ETH clear then SOL drops below 1.20× (reproducing Kagi/percentile 0.922× wipe); kill if retuned.
  - `bnb_smoke`: Kill if 3-coin clears then BNB quiet wipes; kill if retuned.

### Secondary Metrics (Reported for Complete Picture):
- Full ~2.0 year lookback Mode-A return and trade density.
- Operational sizing at 2.5% equity clip vs 100% full-clip Mode-A.
- Max drawdown % and Win Rate %.
