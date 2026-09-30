# stage8-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage8-dual-sol-bnb-v1`  
**Authoritative Briefs:** `CODING_KICK_eb28.md` & `stage8-dual-sol-bnb-briefs-2026-09-18_813b.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce the **DUAL SOL+BNB survival + density** paradigm across SOL and BNB per Path B Stage 8 directives:
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- **Density Bias (Anti-Stage7 ER Tiny-n):** Stage 7 wiped due to sparse coincidence (ER > thr ∩ SMA-cross -> n ≈ 2 on BTC, failing ETH). Stage 8 selects unburned zero-cross and short-lookback dual-line oscillators that fire frequently on 1H–4H majors.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \lesssim 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified).
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **SOL Retention After ETH Clear:** After ETH clear, run explicit SOL retention diagnostics before declaring a SOL failure (ensuring trade density does not collapse, momentum flips respond to dumps, and oscillators do not stay frozen/stuck).
- **Mandatory Dual Smokes:** Each strategy must satisfy its dedicated `sol_smoke` and `bnb_smoke` constraints. Failed smoke conditions disqualify parameter sets.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness).
- **Hard Excludes:** All stage 1–7 IDs (all). Parked: Super Passband, RWI, Reverse EMA (any primary). Burned: ER-gate / ER×SMA / Kaufman-ER clones. Also never: Decycler, ITrend, PVO, P4H, MAD, SuperSmoother, FRAMA, HMA, McGinley, CTI, VIDYA, ATR%ile-primary, ALMA, T3, ZLEMA, VWMA×SMA, CG, Roofing, CMO-zero, KAMA, and all previous burns.

---

## 2. Locked Strategy 1 (`ao-median-zero-cross-v1`)

### 2.1 Formulation
- **Awesome Oscillator (Bill Williams):**
  $$\text{med}_t = \frac{\text{high}_t + \text{low}_t}{2}$$
  $$\text{AO}_t = \text{ta.sma}(\text{med}, A_f) - \text{ta.sma}(\text{med}, A_s)$$
  **Explicitly NOT close-SMA labeled AO.** $A_f < A_s$.
  $(A_f, A_s) \in \{(5, 34), (5, 21), (8, 34)\}$; **default $(5, 34)$**.
- **Mode A (Primary — Article Zero-Cross):**
  - Long entry: $\text{crossover}(\text{AO}, 0)$
  - Exit: $\text{crossunder}(\text{AO}, 0)$ (or ATR stop)
- **Mode B (Secondary denser — Williams Saucer above zero):**
  - Long entry: $\text{AO}_{t-2} > \text{AO}_{t-1} \land \text{AO}_t > \text{AO}_{t-1} \land \text{AO}_t > 0$
  - Exit: $\text{crossunder}(\text{AO}, 0)$ (or ATR stop)
- **Exit:**
  - Opposite zero-cross; optional ATR stop (`atr_trail_mult=0.0` default long-only spot).

### 2.2 Locked Parameter Space
- $(A_f, A_s) \in \{(5, 34), (5, 21), (8, 34)\}$
- Primary grid:
  1. `mode_a|(5,34)` (default)
  2. `mode_a|(5,21)`
  3. `mode_a|(8,34)`
  4. `mode_b|(5,34)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: Fractals/Alligator grafted; close-SMA dual labeled AO; 15m $A_f=3$ spam; ER/ADX graft. Prefer Mode A $(5,34)$, 1H+.
- **sol_retention_note:** After ETH pass, SOL Mode-A $n$ must remain multi-dozen-class on 6m 1H. Silence $\implies A_s$ too long or median construction wrong.
- **bnb_smoke:** Kill if: different $(A_f, A_s)$ than SOL; Mode B saucer-only shorts ungated; no ATR. Prefer identical params; long-only; ATR exit.
- **Forbidden:** Fractals; Alligator jaws/teeth/lips; Gann HiLo; ER-gate; ADX; RSI; FRAMA/HMA/McGinley; request.security; close-SMA(5,34) labeled AO.

---

## 3. Locked Strategy 2 (`pgo-threshold-zeroexit-v1`)

### 3.1 Formulation
- **Pretty Good Oscillator (Mark Johnson):**
  $$\text{sma}_t = \text{ta.sma}(\text{close}, N)$$
  $$\text{tr}_t = \text{ta.tr}(\text{true})$$
  $$\text{den}_t = \text{ta.ema}(\text{tr}, N)$$
  $$\text{PGO}_t = \frac{\text{close}_t - \text{sma}_t}{\text{den}_t} \quad (\text{guard } \text{den}_t > 0)$$
  $N \in \{14, 21, 34\}$; $\text{thr} \in \{2.0, 2.5, 3.0\}$; prefer **$N=14, \text{thr}=2.5$** first.
- **Mode A (Primary — Johnson Breakout + Zero Return):**
  - Long entry: $\text{crossover}(\text{PGO}, \text{thr})$
  - Exit: $\text{crossunder}(\text{PGO}, 0) \lor \text{PGO} \le 0$ (or ATR stop)
- **Mode B (Secondary denser):**
  - Long while $\text{PGO} > \text{thr} \times 0.5 \land \text{close} > \text{sma}$ — only if Mode A under-fires SOL.
  - Exit: $\text{crossunder}(\text{PGO}, 0) \lor \text{PGO} \le 0$ (or ATR stop)
- **Exit:**
  - Zero return; ATR trailing stop.

### 3.2 Locked Parameter Space
- $N \in \{14, 21, 34\}$
- $\text{thr} \in \{2.0, 2.5, 3.0\}$
- Primary grid:
  1. `mode_a|(N14,thr2.5)` (prefer first)
  2. `mode_a|(N14,thr2.0)`
  3. `mode_a|(N21,thr2.5)`
  4. `mode_b|(N14,thr2.5)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: ATR%ile gate; Keltner/BB substitute; $N=89$ on 15m; ER graft. Prefer Mode A $N=14, \text{thr}=2.5$, 1H+.
- **sol_retention_note:** SOL must still print thr crosses after ETH (try $\text{thr}=2.5$ before kill if $\text{thr}=3.0$ silent — same $N$, not per-coin).
- **bnb_smoke:** Kill if: per-coin $\text{thr}/N$; Mode B shorts ungated; no ATR. Prefer identical params; long-only.
- **Forbidden:** ATR%ile-primary; Keltner; BB-squeeze; ER-gate; SMA$\pm k\cdot$ATR labeled PGO.

---

## 4. Locked Strategy 3 (`roc-zero-cross-v1`)

### 4.1 Formulation
- **Rate of Change (StockCharts):**
  $$\text{ROC}_t = 100 \times \left(\frac{\text{close}_t}{\text{close}_{t-N}} - 1\right)$$
  $N \in \{9, 12, 14, 21\}$; prefer **$N=12$** (StockCharts ChartSchool default).
- **Mode A (Primary — Centerline Zero Cross):**
  - Long entry: $\text{crossover}(\text{ROC}, 0)$
  - Exit: $\text{crossunder}(\text{ROC}, 0)$ (or ATR stop)
- **Mode B (Secondary — Oversold Reclaim):**
  - Long entry: $\text{crossover}(\text{ROC}, -\text{ext})$ where $\text{ext} \in \{5, 8, 10\}$ (locked $\text{ext}=8$)
  - Exit: $\text{crossunder}(\text{ROC}, 0)$ (or ATR stop)
- **Exit:**
  - Opposite zero-cross; ATR trailing stop.

### 4.2 Locked Parameter Space
- $N \in \{9, 12, 14, 21\}$
- Primary grid:
  1. `mode_a|(N12)` (prefer first)
  2. `mode_a|(N9)`
  3. `mode_a|(N14)`
  4. `mode_b|(N12,ext8)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: KST/TRIX/Coppock; dual-mom rank; SMA200; 15m $N=3$. Prefer Mode A $N=12$, 1H+.
- **sol_retention_note:** SOL must exit on dump (zero-cross); stuck-positive without exit $\implies$ bug / lookahead.
- **bnb_smoke:** Kill if: different $N$ than SOL; Mode B ungated shorts; no ATR. Prefer identical $N$; long-only.
- **Forbidden:** dual-mom; KST; TRIX; Coppock; ER-gate; ROC-of-ROC; SMA200 filter.

---

## 5. Locked Strategy 4 (`wma-fast-slow-cross-v1`)

### 5.1 Formulation
- **Linear Weighted Moving Average (Investopedia / Fidelity):**
  $$\text{WMA}_N(t) = \frac{\sum_{i=0}^{N-1} (N - i) \cdot \text{close}_{t-i}}{\sum_{j=1}^N j}$$
  Linear arithmetic weights only. $L_f < L_s$.
  $(L_f, L_s) \in \{(9, 21), (10, 30), (12, 26), (5, 20)\}$; prefer **$(10, 30)$** or **$(9, 21)$**.
- **Mode A (Primary — Fast $\times$ Slow Cross):**
  - $\text{fast}_t = \text{ta.wma}(\text{close}, L_f)$
  - $\text{slow}_t = \text{ta.wma}(\text{close}, L_s)$
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
- **Mode B (Secondary — State Filter):**
  - Long while $\text{close} > \text{slow} \land \text{fast} > \text{slow}$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
- **Exit:**
  - Opposite cross; ATR trailing stop.

### 5.2 Locked Parameter Space
- $(L_f, L_s) \in \{(9, 21), (10, 30), (12, 26), (5, 20)\}$
- Primary grid:
  1. `mode_a|(10,30)` (prefer first)
  2. `mode_a|(9,21)` (prefer first)
  3. `mode_a|(12,26)`
  4. `mode_b|(10,30)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: HMA/ZLEMA/VWMA substitute; ER/ATR%ile gate; 15m $(3,8)$; Hull disguise. Prefer Mode A $(10,30)/(9,21)$, 1H+.
- **sol_retention_note:** After ETH, SOL cross $n$ must not collapse; if stuck in one-side trend without exit cross, check WMA allowlist/warmup.
- **bnb_smoke:** Kill if: different $(L_f, L_s)$ than SOL; Mode B ungated shorts; no ATR. Prefer identical params; long-only.
- **Forbidden:** HMA; ZLEMA; VWMA×SMA; FRAMA; McGinley; ALMA; T3; ER-gate; SMA200; WMA-of-WMA Hull.

---

## 6. Stop-Ladder & Tiny-N Execution Flow

```
[All 4 Strategies: 4 params x 2 TFs = 8 cells each = 32 cells total]
                 │
                 ▼
       ┌───────────────────┐
       │     BTCUSDT       │ Mode-A 6m >= 1.2x B&H AND n > 5
       └───────────────────┘ (Tiny-n Policy: n <= 5 -> FAIL)
                 │ PASS
                 ▼
       ┌───────────────────┐
       │     ETHUSDT       │ Mode-A 6m >= 1.2x B&H
       └───────────────────┘
                 │ PASS
                 ▼
       ┌───────────────────┐
       │  SOLUSDT (HARD)   │ Mode-A 6m >= 1.2x B&H + sol_retention checks
       └───────────────────┘
                 │ PASS
                 ▼
       ┌───────────────────┐
       │  BNBUSDT (HARD)   │ Mode-A 6m >= 1.2x B&H + identical params
       └───────────────────┘
                 │ PASS
                 ▼
       [Review + CoS Gate]
```
