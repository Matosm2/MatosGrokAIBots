# stage23-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage23-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage22 (SOL 0.922× wipe; Kagi rhyme). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_99bf.md` & `stage23-dual-sol-bnb-briefs-2026-09-18_bbd7.md`

---

## 1. Governance & Methodological Hygiene

To enforce **SOL ≥1.2× after BTC→ETH PRIMARY** (stage16 Kagi + stage22 percentile 0.922× near-miss) + **Keep BTC LEAD without over-damp** + **Denser $n \gg 9$** + **BNB-survival after 3-coin** per Path B Stage 23 directives:
- **SOL-after-BTC+ETH PRIMARY (Kagi + Percentile 0.922× Near-Miss):** In Stage 22, BTC and ETH cleared on VFI 4H and percentile-channel path, but SOL failed under the gate at 0.922× (percentile-channel-break). In Stage 16, Kagi similarly cleared BTC+ETH then stalled on SOL. In Stage 23, we lock responsive non-MA oscillator trail, adaptive phase cross, and published ATR stop-and-reverse families outside stage 1–22 + parks that can participate on SOL impulse without regressing to 0-BTC chop or structure stall.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially never SOL-only retuning to "save" the 0.922× gap, and never BNB-only retuning) is strictly forbidden.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$), Stage 8 PGO ($n \approx 9$), and thin $n=7$ structure stalls, while avoiding parameter over-inflation that collapses BTC $n$.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD, `sol_smoke` CRITICAL) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD (keep without over-damp):** Kill if Mode A BTC 0 / chop under costs; Kill if parameters inflated until BTC $n$ collapses; Kill if improper substitutes labeled seated strategies; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY:** Kill if BTC clears $\ge 1.2\times$ dense then ETH under 1.2×; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH PRIMARY CRITICAL:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–22 grafts. Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL (HHLL/TTF LESSON):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–22 IDs (all), including percentile-channel / zscore-hold / anchored-VWAP / Katsanos-VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV, Pee TDI, stage12 smoother class.

---

## 2. Locked Strategy 1 (`qqe-trailing-cross`)

### 2.1 Formulation
- **Quantitative Qualitative Estimation — Fast × Slow Trailing Cross:**
  - `rsi = ta.rsi(close, rsiLen)`
  - `qqeFast = ta.ema(rsi, SF)`
  - `tr = abs(qqeFast - qqeFast[1])`
  - ATR-of-RSI double Wilder smooth: `atrRsi = rma(rma(tr, 2*rsiLen - 1), 2*rsiLen - 1)`
  - `dar = atrRsi * WT`
  - `qqeSlow`: classic QQE ratchet trail
  - Prefer **`(14, 5, 4.236)`**.
  - $\ne$ raw RSI 70/30, $\ne$ Schaff STC, $\ne$ WaveTrend, $\ne$ ConnorsRSI.
- **Mode A (SOL-after lean):**
  - Long entry: `crossover(qqeFast, qqeSlow)`
  - Exit: `crossunder(qqeFast, qqeSlow)`
- **Mode B (Trend Quality Filter):**
  - Require `qqeFast > 50` — only if Mode A over-whips; identical params across all four coins. Never RSI 70/30.

### 2.2 Locked Parameter Space
- Sweep: `rsiLen` $\in \{14, 21\}$, `SF` $\in \{5, 8\}$, `WT` $\in \{4.236, 5.0\}$
- Primary grid:
  1. `mode_a|(rsi14,sf5,wt4.236)` (preferred)
  2. `mode_a|(rsi21,sf5,wt4.236)`
  3. `mode_a|(rsi14,sf8,wt5.0)`
  4. `mode_b|(rsi14,sf5,wt4.236,f50)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `rsiLen` $\in \{14, 21\}$, `SF` $\in \{5, 8\}$, `WT` $\in \{4.236, 5.0\}$. Parameter inflation collapses BTC $n$ forbidden. Prefer Mode A (14,5,4.236), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m `rsiLen` $\le 5$ forbidden (spam). Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`mama-fama-cross`)

### 3.1 Formulation
- **Ehlers MAMA × FAMA Adaptive MA Cross:**
  - $\alpha$ derived from Ehlers Homodyne Discriminator pipeline (internal only)
  - `mama = alpha * hl2 + (1 - alpha) * mama[1]`
  - `fama = 0.5 * alpha * mama + (1 - 0.5 * alpha) * fama[1]`
  - Prefer **`(0.5, 0.05)`**.
  - **Do NOT trade Period / SmoothPeriod / Sine / LeadSine.**
  - $\ne$ MESA-primary dominant period, $\ne$ Hilbert Sinewave, $\ne$ PMA, $\ne$ FRAMA / HMA.
- **Mode A (Adaptive Cross):**
  - Long entry: `crossover(mama, fama)`
  - Exit: `crossunder(mama, fama)`
- **Mode B (Rising MAMA Filter):**
  - Require `mama > mama[1]` rising — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep: `fastLimit` $\in \{0.5, 0.7\}$, `slowLimit` $\in \{0.05, 0.08\}$
- Primary grid:
  1. `mode_a|(fast0.5,slow0.05)` (preferred)
  2. `mode_a|(fast0.7,slow0.05)`
  3. `mode_a|(fast0.5,slow0.08)`
  4. `mode_b|(fast0.5,slow0.05,rising)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `fastLimit` $\in \{0.5, 0.7\}$, `slowLimit` $\in \{0.05, 0.08\}$. Limits inflate until BTC $n$ collapses forbidden. Prefer Mode A (0.5,0.05), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. MESA-primary / Sinewave substitute fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`wilder-volatility-system-flip`)

### 4.1 Formulation
- **Wilder Volatility System — ARC SAR Close Flip:**
  - `atr = ta.atr(n)`
  - `arc = factor * atr`
  - `sarLong = ta.highest(close, n) - arc`
  - `sarShort = ta.lowest(close, n) + arc`
  - Prefer **`(7, 3.0)`**; density alt **`(9, 2.0)`** identical-all-four if needed.
  - $\ne$ SuperTrend (HL2 ratchet), $\ne$ Chandelier (HH - ATR from entry), $\ne$ PSAR.
- **Mode A (Long-only SAR Flip):**
  - Long entry: `crossover(close, sarShort)` from flat
  - Exit: `crossunder(close, sarLong)`
- **Mode B (Volatility Expansion Gate):**
  - Require ATR percentrank $> \text{thr}$ — only if Mode A over-whips; identical all four.

### 4.2 Locked Parameter Space
- Sweep: `n` $\in \{7, 9\}$, `factor` $\in \{2.0, 3.0\}$
- Primary grid:
  1. `mode_a|(n7,fac3.0)` (preferred)
  2. `mode_a|(n9,fac2.0)` (density alt)
  3. `mode_a|(n9,fac3.0)`
  4. `mode_b|(n7,fac3.0,atrpr50)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `n` $\in \{7, 9\}$, `factor` $\in \{2.0, 3.0\}$. `n`/`factor` inflate until BTC $n$ collapses forbidden. Prefer Mode A (7,3.0) or (9,2.0), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m `n` $\le 3$ forbidden (spam). Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`chande-kroll-stop-flip`)

### 5.1 Formulation
- **Chande Kroll Stop — Two-Stage ATR Corridor Flip:**
  - `atr = ta.atr(p)`
  - `highStop = ta.highest(high, p) - x * atr`
  - `lowStop = ta.lowest(low, p) + x * atr`
  - `stopShort = ta.highest(highStop, q)`
  - `stopLong = ta.lowest(lowStop, q)`
  - Prefer **`(10, 1.0, 9)`**.
  - $\ne$ Chandelier (single HH - ATR), $\ne$ SuperTrend (HL2 ratchet), $\ne$ Wilder VS.
- **Mode A (Corridor Breakout):**
  - Long entry: `crossover(close, stopShort)`
  - Exit: `crossunder(close, stopLong)`
- **Mode B (Corridor Width Filter):**
  - Require `(stopShort - stopLong)` percentrank $> \text{wMin}$ — only if Mode A over-whips; identical params across all four coins.

### 5.2 Locked Parameter Space
- Sweep: `p` $\in \{10, 14\}$, `x` $\in \{1.0, 1.5\}$, `q` $\in \{9, 14\}$
- Primary grid:
  1. `mode_a|(p10,x1.0,q9)` (preferred)
  2. `mode_a|(p14,x1.0,q9)`
  3. `mode_a|(p10,x1.5,q14)`
  4. `mode_b|(p10,x1.0,q9,wpr50)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `p` $\in \{10, 14\}$, `x` $\in \{1.0, 1.5\}$, `q` $\in \{9, 14\}$. `p`/`q` inflate until BTC $n$ collapses forbidden. Prefer Mode A (10,1.0,9), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m `p` $\le 3$ forbidden (spam). Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 6. Execution Verification Matrix

| # | Strategy ID | Preferred Config | Sweep Space | Mode B Gate | Smoke Check Focus |
|---|-------------|------------------|-------------|-------------|-------------------|
| 1 | `qqe-trailing-cross` | (14, 5, 4.236) @ 1H/4H | rsiLen∈{14,21}, SF∈{5,8}, WT∈{4.236,5.0} | qqeFast > 50 | sol_smoke CRITICAL; Fast×Slow trail |
| 2 | `mama-fama-cross` | (0.5, 0.05) @ 1H/4H | fast∈{0.5,0.7}, slow∈{0.05,0.08} | mama > mama[1] | sol_smoke CRITICAL; MAMA×FAMA cross |
| 3 | `wilder-volatility-system-flip` | (7, 3.0) / (9, 2.0) @ 1H/4H | n∈{7,9}, factor∈{2.0,3.0} | ATR %rank > 50 | sol_smoke CRITICAL; close×SAR flip |
| 4 | `chande-kroll-stop-flip` | (10, 1.0, 9) @ 1H/4H | p∈{10,14}, x∈{1.0,1.5}, q∈{9,14} | Corridor %rank > 50 | sol_smoke CRITICAL; close×stop corridor |
