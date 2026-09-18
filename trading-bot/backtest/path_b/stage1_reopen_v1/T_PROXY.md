# Accumulative Swing Index (ASI) — Limit-Move T-Proxy Specification

**Strategy:** `asi-dual-break-v1`  
**Research ID:** `stage1-reopen-v1`  
**Status:** FROZEN BEFORE SCORING  
**Document Date:** 2026-09-17  

---

## Background & Rationale

Wilder's Accumulative Swing Index (ASI) is derived from the bar-by-bar Swing Index (SI):
\[
SI = 50 \times \frac{(C - C_y) + 0.5(C - O) + 0.25(C_y - O_y)}{R} \times \frac{K}{T}
\]
where \(T\) is the maximum daily limit move established by the exchange for commodities.

In 24/7 continuous crypto spot/perpetuals markets, there is **no exchange-mandated daily price limit move** (\(T\)). Without a defined \(T\), the swing index scaling is undefined or arbitrary. Therefore, an explicit proxy for \(T\) must be defined and locked **prior** to running any backtests or scoring.

---

## Locked First-Pass Baseline Proxy (LOCKED)

Per the Stage-1 briefs and frozen coding kick packet:

- **Baseline T-Proxy (Family 1):**  
  \[
  T = \text{atr\_mult} \times \text{ATR}(\text{atr\_len})
  \]
  - **Locked defaults for v1 baseline:**
    - `atr_mult = 1.0`
    - `atr_len = 14`
    - Executed on the active decision timeframe bar-close.

---

## Parameter Sweeps

To evaluate the sensitivity and robust behavior of ASI breakout confirmation, two distinct proxy families are defined and swept:

### Family 1: ATR Multiple (`atr_mult * ATR(14)`)
- `atr_mult ∈ {0.5, 1.0, 1.5, 2.0}`
- Lookback length: `atr_len = 14` (Wilder standard)
- Label in scoreboard: `T_atr_{atr_mult}x`

### Family 2: Alternate % of Prior Close
- \(T = \text{pct} \times C_{y}\)
- `pct ∈ {1%, 2%, 3%}` (i.e., `pct ∈ {0.01, 0.02, 0.03}`)
- Label in scoreboard: `T_pct_{pct}%`

### Lookback N for Dual Breakout
For both families, the dual breakout lookback window is evaluated across:
- `N ∈ {10, 20, 55}`
- Long entry condition:
  \[
  \text{close} > \max(\text{high}[1 \dots N]) \quad \text{AND} \quad \text{ASI} > \max(\text{ASI}[1 \dots N])
  \]
- Exit condition:
  \[
  \text{close} < \min(\text{low}[1 \dots N]) \quad \text{AND} \quad \text{ASI} < \min(\text{ASI}[1 \dots N])
  \]
  (or optional ATR trailing stop).

---

## Exclusions & Constraints Honored

- **No** Donchian-naked primary (must be dual price + ASI break).
- **No** discretionary divergence-only primary.
- **No** RSI / ADX / SMA200 grafts.
- Bar-close fills only; long-only first pass; pyramiding 0.
