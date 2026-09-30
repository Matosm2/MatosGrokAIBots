# stage9-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage9-dual-sol-bnb-v1`  
**Authoritative Briefs:** `CODING_KICK_cdd9.md` & `stage9-dual-sol-bnb-briefs-2026-09-18_2e16.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce the **DUAL SOL+BNB survival + density** paradigm across SOL and BNB per Path B Stage 9 directives:
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- **Density Bias (Anti-Stage7 ER Tiny-n & Stage8 PGO n≈9):** Stage 7 wiped due to sparse coincidence ($n \approx 2$). Stage 8 wiped AO/ROC/WMA (0 BTC passes) and parked PGO ($n=9$ on BTC, ETH fail). Stage 9 selects unburned midline-cross, zero-cross, and range-scaled dual-line/band events that fire frequently on 1H–4H majors.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \lesssim 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **SOL Retention After ETH Clear:** After ETH clear, run explicit SOL retention diagnostics before declaring a SOL failure (ensuring trade density does not collapse to single digits, momentum flips respond to dumps, and oscillators do not stay frozen/stuck).
- **Mandatory Dual Smokes:** Each strategy must satisfy its dedicated `sol_smoke` and `bnb_smoke` constraints. Failed smoke conditions disqualify parameter sets.
- **Pause Cue:** If full-ladder PASS_6m = 0 for all seats $\to$ note Path B PAUSE for CoS/Nuno (no Stage-10).
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness).
- **Hard Excludes:** All stage 1–8 IDs (all). Parked: Super Passband, RWI, Reverse EMA, PGO / Pretty Good Oscillator motif. Burned motifs: ER-gate clones, AO primary, ROC zero-cross primary, WMA fast×slow primary, PGO / ATR-normalized oscillator clones. Also never: Decycler, ITrend, PVO, P4H, MAD, SuperSmoother, FRAMA, HMA, McGinley, CTI, VIDYA, ATR%ile-primary, ALMA, T3, ZLEMA, VWMA×SMA, CG, Roofing, CMO-zero, KAMA, and all previous burns.

---

## 2. Locked Strategy 1 (`psy-midline-fifty-cross-v1`)

### 2.1 Formulation
- **Psychological Line (PSY):**
  $$\text{up}_t = \begin{cases} 1.0 & \text{if } \text{close}_t > \text{close}_{t-1} \\ 0.0 & \text{otherwise} \end{cases}$$
  $$\text{PSY}_t = 100 \times \text{ta.sma}(\text{up}, N)$$
  $N \in \{10, 12, 13, 20\}$; prefer **$N=12$** first (conventional East-Asian standard).
- **Mode A (Primary — Midline Polarity Cross):**
  - Long entry: $\text{crossover}(\text{PSY}, 50)$
  - Exit: $\text{crossunder}(\text{PSY}, 50)$ (or ATR stop)
- **Mode B (Secondary — Oversold Reclaim):**
  - Long entry: $\text{crossover}(\text{PSY}, 25)$
  - Exit: $\text{crossunder}(\text{PSY}, 50)$ (or ATR stop)
- **Exit:**
  - Opposite 50-cross; ATR trailing stop (`atr_trail_mult=0.0` default long-only spot).

### 2.2 Locked Parameter Space
- $N \in \{10, 12, 13, 20\}$
- Primary grid:
  1. `mode_a|(N12)` (prefer first)
  2. `mode_a|(N10)`
  3. `mode_a|(N13)`
  4. `mode_a|(N20)`
  5. `mode_b|(N12,os25)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: RSI/Stoch grafted; 15m $N=5$ spam; ER/AO/PGO graft. Prefer Mode A $N=12$, 1H+.
- **sol_retention_note:** After ETH pass, SOL Mode-A $n$ must remain multi-dozen-class on 6m 1H. Silence $\implies N$ too long or up-count bug.
- **bnb_smoke:** Kill if: different $N$ than SOL; Mode B ungated shorts; no ATR. Prefer identical params; long-only.
- **Forbidden:** RSI, ConnorsRSI, Stoch, AO/ROC/PGO, request.security, $m=1$ RMI labeled PSY.

---

## 3. Locked Strategy 2 (`disparity-sma-zero-cross-v1`)

### 3.1 Formulation
- **Disparity Index (Nison):**
  $$\text{ma}_t = \text{ta.sma}(\text{close}, N) \quad (\text{guard } \text{ma}_t > 0)$$
  $$\text{DI}_t = 100 \times \frac{\text{close}_t - \text{ma}_t}{\text{ma}_t}$$
  $N \in \{10, 14, 20, 30\}$; prefer **$N=20$** first.
- **Mode A (Primary — Zero-Line Cross):**
  - Long entry: $\text{crossover}(\text{DI}, 0)$
  - Exit: $\text{crossunder}(\text{DI}, 0)$ (or ATR stop)
- **Mode B (Secondary — Oversold Reclaim):**
  - Long entry: $\text{crossover}(\text{DI}, -\text{ext})$ where $\text{ext} \in \{1.0, 2.0, 3.0\}$; default $\text{ext}=2.0$.
  - Exit: $\text{crossunder}(\text{DI}, 0)$ (or ATR stop)
- **Exit:**
  - Opposite zero-cross; ATR trailing stop.

### 3.2 Locked Parameter Space
- $N \in \{10, 14, 20, 30\}$
- $\text{ext} \in \{1.0, 2.0, 3.0\}$
- Primary grid:
  1. `mode_a|(N20)` (prefer first)
  2. `mode_a|(N10)`
  3. `mode_a|(N14)`
  4. `mode_a|(N30)`
  5. `mode_b|(N20,ext2.0)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: ROC/PGO substitute; WMA dual disguise; 15m $N=5$ spam; ER graft. Prefer Mode A $N=20$, 1H+.
- **sol_retention_note:** SOL $n$ after ETH should stay dense; if DI stuck positive through dumps without exit, check ma warmup / division.
- **bnb_smoke:** Kill if: different $N$ than SOL; Mode B ungated shorts; no ATR. Prefer identical params; long-only.
- **Forbidden:** ROC primary; PGO/ATR-denom; WMA dual; HMA/ZLEMA/VWMA; ER-gate; EMA-DI unlabeled.

---

## 4. Locked Strategy 3 (`wavetrend-wt1-wt2-cross-v1`)

### 4.1 Formulation
- **WaveTrend Oscillator (LazyBear):**
  $$\text{ap}_t = \frac{\text{high}_t + \text{low}_t + \text{close}_t}{3}$$
  $$\text{esa}_t = \text{ta.ema}(\text{ap}, n_1)$$
  $$d_t = \text{ta.ema}(|\text{ap} - \text{esa}|, n_1) \quad (\text{guard } d_t > 0)$$
  $$\text{ci}_t = \frac{\text{ap}_t - \text{esa}_t}{0.015 \times d_t}$$
  $$\text{wt}_1 = \text{ta.ema}(\text{ci}, n_2)$$
  $$\text{wt}_2 = \text{ta.sma}(\text{wt}_1, n_3)$$
  Defaults: $(n_1, n_2, n_3) = (10, 21, 4)$; $n_1 \in \{8, 10, 12\}$, $n_2 \in \{14, 21\}$, $n_3 \in \{3, 4\}$. Factor $0.015$ locked.
- **Mode A (Primary — WT1×WT2 Cross):**
  - Long entry: $\text{crossover}(\text{wt}_1, \text{wt}_2)$
  - Exit: $\text{crossunder}(\text{wt}_1, \text{wt}_2)$ (or ATR stop)
- **Mode B (Secondary — Oversold Gated Cross):**
  - Long entry: $\text{crossover}(\text{wt}_1, \text{wt}_2) \land \text{wt}_1 < -53$
  - Exit: $\text{crossunder}(\text{wt}_1, \text{wt}_2)$ (or ATR stop)
- **Exit:**
  - Opposite cross; ATR trailing stop.

### 4.2 Locked Parameter Space
- $(n_1, n_2, n_3) \in \{(10, 21, 4), (8, 21, 4), (12, 21, 4), (10, 14, 3)\}$
- Primary grid:
  1. `mode_a|(10,21,4)` (default)
  2. `mode_a|(8,21,4)`
  3. `mode_a|(12,21,4)`
  4. `mode_a|(10,14,3)`
  5. `mode_b|(10,21,4,os53)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: CCI/Stoch labeled WT; missing $0.015$; 15m $n_1=3$ spam; ER/AO/PGO graft. Prefer Mode A $(10,21,4)$, 1H+.
- **sol_retention_note:** After ETH, SOL cross $n$ must not collapse to PGO-class single digits.
- **bnb_smoke:** Kill if: different params than SOL; Mode B ungated shorts; no ATR. Prefer identical params; long-only.
- **Forbidden:** CCI; Stoch/SMI; RSI; ER-gate; AO/ROC/WMA/PGO; WT without $0.015$ scale.

---

## 5. Locked Strategy 4 (`rmi-midline-fifty-cross-v1`)

### 5.1 Formulation
- **Relative Momentum Index (Altman RMI):**
  $$\text{mom}_t = \text{close}_t - \text{close}_{t-m}$$
  $$u_t = \max(\text{mom}_t, 0.0), \quad d_t = \max(-\text{mom}_t, 0.0)$$
  $$U_t = \text{ta.rma}(u, n), \quad D_t = \text{ta.rma}(d, n) \quad (\text{guard } U_t + D_t > 0)$$
  $$\text{RMI}_t = 100 \times \frac{U_t}{U_t + D_t}$$
  $(n, m) \in \{(20, 5), (14, 3), (21, 5)\}$; default **$(20, 5)$**. **Hard forbid $m=1$ (RSI clone).**
- **Mode A (Primary — Midline-50 Cross):**
  - Long entry: $\text{crossover}(\text{RMI}, 50)$
  - Exit: $\text{crossunder}(\text{RMI}, 50)$ (or ATR stop)
- **Mode B (Secondary — Infront Oversold Reclaim):**
  - Long entry: $\text{crossover}(\text{RMI}, 30)$
  - Exit: $\text{crossunder}(\text{RMI}, 50)$ (or crossunder 30)
- **Exit:**
  - Opposite cross; ATR trailing stop.

### 5.2 Locked Parameter Space
- $(n, m) \in \{(20, 5), (14, 3), (21, 5)\}$ with $m \ge 3$ strictly enforced.
- Primary grid:
  1. `mode_a|(20,5)` (default)
  2. `mode_a|(14,3)`
  3. `mode_a|(21,5)`
  4. `mode_b|(20,5,os30)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: $m=1$ RSI; ConnorsRSI/CMO; 15m spam; ER/AO/PGO graft. Prefer Mode A $(20,5)$, 1H+.
- **sol_retention_note:** After ETH, SOL $n$ must stay multi-dozen-class; silence $\implies n$ too long or rma warmup.
- **bnb_smoke:** Kill if: different $(n, m)$ than SOL; Mode B ungated shorts; no ATR. Prefer identical params; long-only.
- **Forbidden:** RSI primary; CMO-zero; ConnorsRSI; StochRSI; ER-gate; $m=1$.

---

## 6. Locked Strategy 5 (`accel-bands-break-inside-exit-v1`)

### 6.1 Formulation
- **Acceleration Bands (Price Headley):**
  $$\text{rng}_t = \frac{\text{high}_t - \text{low}_t}{\text{high}_t + \text{low}_t} \quad (\text{guard } \text{high}_t + \text{low}_t > 0)$$
  $$\text{upSrc}_t = \text{high}_t \times (1.0 + k \times \text{rng}_t)$$
  $$\text{dnSrc}_t = \text{low}_t \times (1.0 - k \times \text{rng}_t)$$
  $$\text{upper}_t = \text{ta.sma}(\text{upSrc}, N), \quad \text{lower}_t = \text{ta.sma}(\text{dnSrc}, N), \quad \text{mid}_t = \text{ta.sma}(\text{close}, N)$$
  $N \in \{14, 20, 30\}$; $k \in \{3.0, 4.0\}$; prefer **$N=20, k=4.0$** first.
- **Mode A (Primary — Single Close Breakout + Inside Exit):**
  - Long entry: $\text{close}_t > \text{upper}_t \land \text{close}_{t-1} \le \text{upper}_{t-1}$
  - Exit: $\text{close}_t < \text{upper}_t$ (or $\text{close}_t \le \text{mid}_t$, or ATR stop)
- **Mode B (Secondary — Two Consecutive Closes Breakout):**
  - Long entry: $\text{close}_t > \text{upper}_t \land \text{close}_{t-1} > \text{upper}_{t-1}$
  - Exit: $\text{close}_t < \text{upper}_t$ (or ATR stop)
- **Exit:**
  - Inside reclaim $\text{close} < \text{upper}$; ATR trailing stop.

### 6.2 Locked Parameter Space
- $N \in \{14, 20, 30\}$
- $k \in \{3.0, 4.0\}$
- Primary grid:
  1. `mode_a|(N20,k4.0)` (prefer first)
  2. `mode_a|(N20,k3.0)`
  3. `mode_a|(N14,k4.0)`
  4. `mode_a|(N30,k4.0)`
  5. `mode_b|(N20,k4.0)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: Keltner/BB/Donchian substitute; ATR%ile graft; 15m $N=5$ spam; ER/AO/PGO graft. Prefer Mode A $N=20, k=4$, 1H+.
- **sol_retention_note:** After ETH, if SOL $n$ collapses to single digits, try Mode A before kill (not per-coin retune); if still silent, try $k=3$ same $N$.
- **bnb_smoke:** Kill if: different $(N, k)$ than SOL; Mode B shorts ungated; no ATR. Prefer identical params; long-only.
- **Forbidden:** Keltner; BB-squeeze; Donchian; ATR%ile; Chandelier-primary; ER-gate; AO/ROC/WMA/PGO.

---

## 7. Execution Matrix Summary

| Strategy ID | Family | Primary Parameters | Mode A Trigger | Mode B Trigger | Exit | Smoke / Kill |
|---|---|---|---|---|---|---|
| `psy-midline-fifty-cross-v1` | Count Oscillator | $N \in \{10, 12, 13, 20\}$, def $12$ | $\text{crossover}(\text{PSY}, 50)$ | $\text{crossover}(\text{PSY}, 25)$ | $\text{crossunder}(\text{PSY}, 50)$ / ATR | $\ne$ RSI/Stoch; $n > 5$ |
| `disparity-sma-zero-cross-v1` | % Distance SMA | $N \in \{10, 14, 20, 30\}$, def $20$ | $\text{crossover}(\text{DI}, 0)$ | $\text{crossover}(\text{DI}, -2.0)$ | $\text{crossunder}(\text{DI}, 0)$ / ATR | $\ne$ ROC/PGO/WMA; $n > 5$ |
| `wavetrend-wt1-wt2-cross-v1` | HLC3 Norm Dual-Line | $(10, 21, 4) \pm$, factor $0.015$ | $\text{crossover}(\text{wt}_1, \text{wt}_2)$ | $\text{cross} \land \text{wt}_1 < -53$ | $\text{crossunder}(\text{wt}_1, \text{wt}_2)$ / ATR | $\ne$ CCI/Stoch; $0.015$ locked; $n > 5$ |
| `rmi-midline-fifty-cross-v1` | Altman Momentum RMI | $(20, 5) \pm$, $m \ge 3$ hard | $\text{crossover}(\text{RMI}, 50)$ | $\text{crossover}(\text{RMI}, 30)$ | $\text{crossunder}(\text{RMI}, 50)$ / ATR | $\ne$ RSI ($m \ge 3$ hard); $n > 5$ |
| `accel-bands-break-inside-exit-v1` | Headley Range Envelope | $N \in \{14, 20, 30\}$, $k \in \{3, 4\}$, def $(20, 4)$ | 1-bar close $> \text{upper}$ | 2-bar close $> \text{upper}$ | $\text{close} < \text{upper}$ / ATR | $\ne$ Keltner/BB/Donchian; $n > 5$ |
