# stage10-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage10-dual-sol-bnb-v1`  
**Authoritative Briefs:** `CODING_KICK_1797.md` & `stage10-dual-sol-bnb-briefs-2026-09-18_0c55.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce the **DUAL SOL+BNB survival + density** paradigm across SOL and BNB per Path B Stage 10 directives:
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- **Density Bias (Anti-Stage7 ER Tiny-n & Stage8 PGO n≈9):** Stage 7 wiped due to sparse coincidence ($n \approx 2$). Stage 8 wiped AO/ROC/WMA (0 BTC passes) and parked PGO ($n=9$ on BTC, ETH fail). Stage 9 wiped PSY/Disparity/WT/RMI/AccelBands. Stage 10 selects unburned midline-cross, zero-cross, sign-flip, and lag-reduced dual-MA events that fire frequently on 1H–4H majors.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **SOL Retention After ETH Clear:** After ETH clear, run explicit SOL retention diagnostics before declaring a SOL failure (ensuring trade density does not collapse to single digits, oscillator flips respond to moves, and filters do not stay frozen/stuck).
- **Mandatory Dual Smokes:** Each strategy must satisfy its dedicated `sol_smoke` and `bnb_smoke` constraints. Failed smoke conditions disqualify parameter sets.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness).
- **Hard Excludes:** All stage 1–9 IDs (all). Parked this cycle: Super Passband, RWI, Reverse EMA, PGO motif, PSY midline, Disparity, WaveTrend, RMI midline, AccelBands. Burned motifs: ER-gate clones, AO primary, ROC zero-cross primary, WMA fast×slow primary, PGO / ATR-normalized oscillator clones, PSY/RMI midline-50 clones, Disparity zero-cross clones, WaveTrend WT1×WT2, AccelBands break. Also never: Decycler, ITrend, PVO, P4H, MAD, SuperSmoother, FRAMA, HMA, McGinley, CTI, VIDYA, ATR%ile-primary, ALMA, T3, ZLEMA, VWMA×SMA, CG, Roofing, CMO-zero, KAMA, and all previous burns.

---

## 2. Locked Strategy 1 (`tii-midline-fifty-cross-v1`)

### 2.1 Formulation
- **Trend Intensity Index (TII — M.H. Pee):**
  $$\text{MA} = \text{SMA}(\text{close}, \text{major})$$
  $$\text{SD}^+ = \sum_{i=1}^{\text{minor}} \max(\text{close}_i - \text{MA}, 0)$$
  $$\text{SD}^- = \sum_{i=1}^{\text{minor}} \max(\text{MA} - \text{close}_i, 0)$$
  $$\text{TII} = 100 \times \frac{\text{SD}^+}{\text{SD}^+ + \text{SD}^-}$$
  $(\text{major}, \text{minor}) \in \{(60, 30), (40, 20), (50, 25)\}$; prefer **$(60, 30)$** first (Pee default).
- **Mode A (Primary — Dense Midline-50 Cross):**
  - Long entry: $\text{crossover}(\text{TII}, 50)$
  - Exit: $\text{crossunder}(\text{TII}, 50)$ (or ATR stop)
- **Mode B (Secondary — Classic Extremes):**
  - Long entry: $\text{crossover}(\text{TII}, 80)$
  - Exit: $\text{crossunder}(\text{TII}, 50)$ (or ATR stop)
- **Exit:**
  - Opposite 50-cross; ATR trailing stop (`atr_trail_mult=0.0` default long-only spot).

### 2.2 Locked Parameter Space
- $(\text{major}, \text{minor}) \in \{(60, 30), (40, 20), (50, 25)\}$
- Primary grid:
  1. `mode_a|(60,30)` (prefer first)
  2. `mode_a|(40,20)`
  3. `mode_a|(50,25)`
  4. `mode_b|(60,30,ob80)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: RSI/PSY/RMI labeled TII; 15m major$\le$10 spam; ER/AO/PGO graft; Mode B 80-only with single-digit $n$. Prefer Mode A (60,30), 1H+.
- **sol_retention_note:** After ETH pass, SOL Mode-A $n$ must stay multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if: different $(\text{major}, \text{minor})$ than SOL; Mode B shorts ungated; no ATR. Prefer identical params; long-only; ATR exit.
- **Forbidden:** RSI/PSY/RMI substitute; ADX/DMI graft; SMA200; ER-gate; AO/ROC/WMA/PGO; Disparity/WT; request.security.

---

## 3. Locked Strategy 2 (`rainbow-osc-zero-cross-v1`)

### 3.1 Formulation
- **Rainbow Oscillator (Mel Widner):**
  $$\text{ave}_1 = \text{SMA}(\text{close}, p)$$
  $$\text{ave}_2 = \text{SMA}(\text{ave}_1, p), \quad \dots, \quad \text{ave}_{10} = \text{SMA}(\text{ave}_9, p)$$
  $$\text{ave}_A = \frac{1}{\text{depth}} \sum_{k=1}^{\text{depth}} \text{ave}_k$$
  $$\text{range}_C = \max_{k \in [0, \text{depth}]}(\text{close}_{t-k}) - \min_{k \in [0, \text{depth}]}(\text{close}_{t-k})$$
  $$\text{RO} = 100 \times \frac{\text{close} - \text{ave}_A}{\text{range}_C}$$
  $$\text{RB} = 100 \times \frac{\max(\text{ave}_1 \dots \text{ave}_{10}) - \min(\text{ave}_1 \dots \text{ave}_{10})}{\text{range}_C}$$
  Prefer **$p=2, \text{depth}=10$**.
- **Mode A (Primary — Consensus Zero-Cross):**
  - Long entry: $\text{crossover}(\text{RO}, 0)$
  - Exit: $\text{crossunder}(\text{RO}, 0)$ (or ATR stop)
- **Mode B (Secondary — Bandwidth Filter):**
  - Long entry: $\text{crossover}(\text{RO}, 0)$ and $\text{RB} < \text{thr}$ with $\text{thr}=38.0$
  - Exit: $\text{crossunder}(\text{RO}, 0)$ (or ATR stop)

### 3.2 Locked Parameter Space
- $(p, \text{depth}) \in \{(2, 10), (2, 8), (3, 10)\}$
- Primary grid:
  1. `mode_a|(p2,d10)` (prefer first)
  2. `mode_a|(p2,d8)`
  3. `mode_a|(p3,d10)`
  4. `mode_b|(p2,d10,rb38)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: WMA/Disparity substitute; missing rangeC guard; 15m depth$\le$3 spam; ER/AO/PGO graft. Prefer Mode A $p=2, \text{depth}=10$, 1H+.
- **sol_retention_note:** After ETH pass, SOL zero-cross $n$ must not collapse to single digits.
- **bnb_smoke:** Kill if: different $(p, \text{depth})$ than SOL; Mode B shorts ungated; no ATR. Prefer identical params; long-only; ATR exit.
- **Forbidden:** WMA dual; Disparity; BB-squeeze; HMA/ZLEMA; ER-gate; PSY/RMI; request.security.

---

## 4. Locked Strategy 3 (`dorsey-relvol-midline-fifty-v1`)

### 4.1 Formulation
- **Dorsey Relative Volatility Index (Donald Dorsey — Refined 1995):**
  $$s_H = \text{stdev}(\text{high}, \text{stdevLen}), \quad s_L = \text{stdev}(\text{low}, \text{stdevLen})$$
  $$u_H = \begin{cases} s_H & \text{if } \text{high}_t > \text{high}_{t-1} \\ 0 & \text{otherwise} \end{cases}, \quad u_L = \begin{cases} s_L & \text{if } \text{low}_t > \text{low}_{t-1} \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{rvi}_H = 100 \times \frac{\text{RMA}(u_H, \text{avgLen})}{\text{RMA}(s_H, \text{avgLen})}, \quad \text{rvi}_L = 100 \times \frac{\text{RMA}(u_L, \text{avgLen})}{\text{RMA}(s_L, \text{avgLen})}$$
  $$\text{RelVol} = \frac{\text{rvi}_H + \text{rvi}_L}{2.0}$$
  Defaults $\text{stdevLen}=10, \text{avgLen}=14$.
  **CRITICAL NAMING LOCK:** Never label as Relative Vigor Index.
- **Mode A (Primary — Midline-50 Cross):**
  - Long entry: $\text{crossover}(\text{RelVol}, 50)$
  - Exit: $\text{crossunder}(\text{RelVol}, 50)$ (or ATR stop)
- **Mode B (Secondary — Classic Extremes):**
  - Long entry: $\text{crossover}(\text{RelVol}, 60)$
  - Exit: $\text{crossunder}(\text{RelVol}, 40)$ (or ATR stop)

### 4.2 Locked Parameter Space
- $(\text{stdevLen}, \text{avgLen}) \in \{(10, 14), (8, 14), (14, 14), (10, 10)\}$
- Primary grid:
  1. `mode_a|(10,14)` (prefer first)
  2. `mode_a|(8,14)`
  3. `mode_a|(14,14)`
  4. `mode_a|(10,10)`
  5. `mode_b|(10,14,os40_ob60)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: Relative Vigor formula used; RSI labeled RelVol; 15m stdevLen$\le$3 spam; ER/AO/PGO/ADX graft. Prefer Mode A (10, 14), 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must stay multi-dozen-class.
- **bnb_smoke:** Kill if: different $(\text{stdevLen}, \text{avgLen})$ than SOL; Mode B shorts ungated; no ATR. Prefer identical params; long-only; ATR exit.
- **Forbidden:** Relative Vigor; RSI primary; Stoch; PSY/RMI; ConnorsRSI; ER-gate; AO/ROC/WMA/PGO; ADX graft; request.security.

---

## 5. Locked Strategy 4 (`tcf-plus-sign-flip-v1`)

### 5.1 Formulation
- **Trend Continuation Factor (M.H. Pee):**
  $$\text{Change} = \text{close}_t - \text{close}_{t-1}$$
  $$+\text{Change} = \max(\text{Change}, 0), \quad -\text{Change} = \max(-\text{Change}, 0)$$
  $$+\text{CF}_t = \begin{cases} 0 & \text{if } +\text{Change}_t = 0 \\ +\text{Change}_t + +\text{CF}_{t-1} & \text{otherwise} \end{cases}$$
  $$-\text{CF}_t = \begin{cases} 0 & \text{if } -\text{Change}_t = 0 \\ -\text{Change}_t + -\text{CF}_{t-1} & \text{otherwise} \end{cases}$$
  $$+\text{TCF} = \sum_{k=0}^{N-1} (+\text{Change}_{t-k} - -\text{CF}_{t-k})$$
  $$-\text{TCF} = \sum_{k=0}^{N-1} (-\text{Change}_{t-k} - +\text{CF}_{t-k})$$
  $N \in \{20, 25, 35\}$; prefer **$N=35$** first.
- **Mode A (Primary — +TCF Zero Sign Flip):**
  - Long entry: $\text{crossover}(+\text{TCF}, 0)$
  - Exit: $\text{crossunder}(+\text{TCF}, 0)$ or $-\text{TCF} > 0$ (or ATR stop)
- **Mode B (Secondary — Dual Cross):**
  - Long entry: $\text{crossover}(+\text{TCF}, -\text{TCF})$ and $+\text{TCF} > 0$
  - Exit: $\text{crossunder}(+\text{TCF}, -\text{TCF})$ (or ATR stop)

### 5.2 Locked Parameter Space
- $N \in \{20, 25, 35\}$
- Primary grid:
  1. `mode_a|(N35)` (prefer first)
  2. `mode_a|(N25)`
  3. `mode_a|(N20)`
  4. `mode_b|(N35)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: ADX labeled TCF; AO/ROC substitute; 15m $N\le 5$ spam; ER/PGO graft. Prefer Mode A $N=35$, 1H+.
- **sol_retention_note:** After ETH pass, if SOL $n$ collapses, test $N=25$ under identical cross-coin params before declaring failure.
- **bnb_smoke:** Kill if: different $N$ than SOL; Mode B shorts ungated; no ATR. Prefer identical $N$; long-only; ATR exit.
- **Forbidden:** ADX/DMI; AO/ROC/WMA/PGO; ER-gate; PSY/RMI/Disparity/WT; request.security.

---

## 6. Locked Strategy 5 (`dema-fast-slow-cross-v1` — OPTIONAL LAST)

### 6.1 Formulation
- **Double Exponential Moving Average (Patrick Mulloy):**
  $$\text{DEMA}(x, n) = 2 \times \text{EMA}(x, n) - \text{EMA}(\text{EMA}(x, n), n)$$
  $$\text{fast} = \text{DEMA}(\text{close}, L_f), \quad \text{slow} = \text{DEMA}(\text{close}, L_s)$$
  $(L_f, L_s) \in \{(10, 30), (5, 35), (8, 21), (12, 26)\}$; prefer **$(10, 30)$** or **$(5, 35)$**.
- **Mode A (Primary — Fast × Slow Cross):**
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
- **Mode B (Secondary — Close × Slow):**
  - Long entry: $\text{crossover}(\text{close}, \text{slow})$
  - Exit: $\text{crossunder}(\text{close}, \text{slow})$ (or ATR stop)

### 6.2 Locked Parameter Space
- $(L_f, L_s) \in \{(10, 30), (5, 35), (8, 21), (12, 26)\}$
- Primary grid:
  1. `mode_a|(10,30)` (prefer first)
  2. `mode_a|(5,35)`
  3. `mode_a|(8,21)`
  4. `mode_a|(12,26)`
  5. `mode_b|(close,30)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: plain EMA dual labeled DEMA; WMA/HMA/ZLEMA substitute; 15m (3,8) spam; ER/AO/PGO graft. Prefer Mode A (10,30), 1H+.
- **sol_retention_note:** After ETH pass, if SOL $n$ is huge with poor structure, evaluate (10,30) with identical params.
- **bnb_smoke:** Kill if: different $(L_f, L_s)$ than SOL; Mode B shorts ungated; no ATR. Prefer identical params; long-only; ATR exit.
- **Forbidden:** plain EMA dual labeled DEMA; WMA dual; HMA; ZLEMA; TEMA; FRAMA/McGinley; SMA200; ER-gate; AO/ROC/PGO; PSY/RMI/Disparity/WT/AccelBands; request.security.

---

## 7. Execution Grid Summary

| Strategy ID | Indicator | Primary Params | Sweep Variations | Timeframes |
|---|---|---|---|---|
| `tii-midline-fifty-cross-v1` | Trend Intensity Index | Mode A (60, 30) | (40, 20), (50, 25), Mode B (60, 30, ob80) | 1H, 4H |
| `rainbow-osc-zero-cross-v1` | Rainbow Oscillator | Mode A (p=2, depth=10) | (2, 8), (3, 10), Mode B (2, 10, rb38) | 1H, 4H |
| `dorsey-relvol-midline-fifty-v1` | Dorsey Relative Volatility | Mode A (10, 14) | (8, 14), (14, 14), (10, 10), Mode B (10, 14) | 1H, 4H |
| `tcf-plus-sign-flip-v1` | Trend Continuation Factor | Mode A (N=35) | N=25, N=20, Mode B (N=35) | 1H, 4H |
| `dema-fast-slow-cross-v1` | Double EMA Fast×Slow | Mode A (10, 30) | (5, 35), (8, 21), (12, 26), Mode B (close, 30) | 1H, 4H |
