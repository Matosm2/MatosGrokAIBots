# stage12-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage12-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage11 (Pee TDI SOL→BNB wipe). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_616a.md` & `stage12-dual-sol-bnb-briefs-2026-09-18_fe53.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BNB-survival-CRITICAL** and dual SOL+BNB identical parameters per Path B Stage 12 directives:
- **BNB-Survival-CRITICAL Bias:** Stage 10 lesson (TII) + Stage 11 lesson (Pee TDI furthest dual-wave BTC→ETH→SOL then BNB −1.263× wipe): SOL-clear then BNB-kill is the hard choke. Strategies are designed for denser majors events that still travel to quieter BNB without per-coin retuning.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin after SOL clear is strictly prohibited.
- **Denser BTC Density Bias ($n \gg 9$):** Dual-line, lag-cross, and triple-smoothed events that fire continuously on 1H majors.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Dual Smokes:**
  - `sol_smoke`: Enforce motif anti-burns, timeframe sanity, parameter validity, and retention check (after ETH, SOL $n$ must stay multi-dozen class on 6m 1H).
  - `bnb_smoke`: **CRITICAL after SOL before declaring BNB fail**; stresses BNB-after-SOL kill conditions (identical parameters across coins, no volume microstructure graft, no ungated shorts, long-only spot first, identical Mode across coins).
- **SOL Retention After ETH Clear:** After ETH clear, log explicit SOL retention diagnostics before declaring a SOL failure.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–11 IDs (all), including Pee TDI/Direction, TrendScore, NetLead, GMMA osc, VQI, TII, Rainbow, Dorsey, TCF, DEMA. Parked this cycle: Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow Osc, Dorsey RelVol, TCF, DEMA dual, Pee TDI class, TrendScore, NetLead×EMA, GMMA osc, VQI. Burned motifs: ER-gate; AO; ROC zero-cross; WMA dual; PGO clones; PSY/RMI/TII/Dorsey midline-50; Disparity; WaveTrend; AccelBands; Rainbow; TCF; DEMA; Pee TDI class; TrendScore; NetLead; GMMA osc; VQI. Also never: Decycler, ITrend, PVO, P4H, MAD, SuperSmoother, FRAMA, HMA, McGinley, CTI, VIDYA, ATR%ile-primary, ALMA, T3, ZLEMA, VWMA×SMA, CG, Roofing, CMO-zero, KAMA, Alligator, Gann HiLo.

---

## 2. Locked Strategy 1 (`blau-csi-ergodic-signal-cross-v1`)

### 2.1 Formulation
- **Blau Candlestick Index (William Blau, Momentum, Direction, and Divergence / MQL5):**
  $$\text{cmtm}_t = \text{close}_t - \text{open}_{t-(q-1)}$$
  $$\text{rng}_t = \max_{0 \le i < q}(\text{high}_{t-i}) - \min_{0 \le i < q}(\text{low}_{t-i})$$
  $$\text{num}_t = \text{EMA}(\text{EMA}(\text{EMA}(\text{cmtm}, r), s), u)$$
  $$\text{den}_t = \text{EMA}(\text{EMA}(\text{EMA}(\text{rng}, r), s), u)$$
  $$\text{CSI}_t = \begin{cases} 100 \cdot \frac{\text{num}_t}{\text{den}_t} & \text{if } \text{den}_t \ne 0 \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{Signal}_t = \text{EMA}(\text{CSI}, ul)$$
  Defaults: $q=1, r=20, s=5, u=3, ul=3$.
- **Mode A (Primary — Dense Ergodic×Signal Cross):**
  - Long entry: $\text{crossover}(\text{CSI}, \text{Signal})$
  - Exit: $\text{crossunder}(\text{CSI}, \text{Signal})$ (or ATR stop)
- **Mode B (Secondary — BNB-Quiet Quality):**
  - Long entry: $\text{crossover}(\text{CSI}, \text{Signal}) \land \text{CSI} > 0$
  - Exit: $\text{crossunder}(\text{CSI}, \text{Signal}) \lor \text{CSI} < 0$ (or ATR stop)
  - Evaluated with identical params across all coins.

### 2.2 Locked Parameter Space
- Defaults: $q=1, s=5, u=3$
- $(r, ul) \in \{(20, 3), (14, 3), (25, 3), (20, 5)\}$
- Primary grid:
  1. `mode_a|(r20,ul3)` (prefer first)
  2. `mode_a|(r14,ul3)`
  3. `mode_a|(r25,ul3)`
  4. `mode_b|(r20,ul3)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: TSI/BoP/RVI/Pee TDI labeled CSI; 15m $r=3$ spam; ER/AO/PGO graft. Prefer Mode A (20,3), 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must stay multi-dozen-class on 6m 1H.
- **bnb_smoke (CRITICAL after SOL):** Kill if: different $(r, ul)$ than SOL; Mode B only on BNB while SOL Mode A; no ATR; volume graft. Kill if BNB needs larger $r$ than SOL. Prefer identical params; long-only; ATR exit.
- **Forbidden:** TSI/SMI/BoP/RVI substitute; Pee TDI/Direction; TrendScore; ER-gate; AO/ROC/WMA/PGO; request.security.

---

## 3. Locked Strategy 2 (`ehlers-edcf-filt-lag-cross-v1`)

### 3.1 Formulation
- **Ehlers Distance Coefficient Filter (John Ehlers, S&C V.19:4 / MESA):**
  Nonlinear FIR filter weighting $\text{hl2}$ by squared price distances:
  $$\text{price}_t = \frac{\text{high}_t + \text{low}_t}{2}$$
  For $\text{count} = 0 \dots \text{Length}-1$:
  $$\text{Coef}[\text{count}] = \sum_{k=1}^{\text{Length}-1} (\text{price}_{t-\text{count}} - \text{price}_{t-((\text{count}+k)\bmod\text{Length})})^2$$
  $$\text{filt}_t = \begin{cases} \frac{\sum_{\text{count}=0}^{\text{Length}-1} \text{Coef}[\text{count}] \cdot \text{price}_{t-\text{count}}}{\sum \text{Coef}} & \text{if } \sum \text{Coef} \ne 0 \\ \text{price}_t & \text{otherwise} \end{cases}$$
  Prefer $\text{Length}=15, \text{lag}=2$.
- **Mode A (Primary / BNB-Critical — Filt×Filt[lag] Cross):**
  - Long entry: $\text{crossover}(\text{filt}, \text{filt}[\text{lag}])$
  - Exit: $\text{crossunder}(\text{filt}, \text{filt}[\text{lag}])$ (or ATR stop)
- **Mode B (Secondary — Price×Filt Cross):**
  - Long entry: $\text{crossover}(\text{price}, \text{filt})$
  - Exit: $\text{crossunder}(\text{price}, \text{filt})$ (or ATR stop)
  - Evaluated with identical params across all coins.

### 3.2 Locked Parameter Space
- $(\text{Length}, \text{lag}) \in \{(15, 2), (10, 2), (20, 2), (15, 3)\}$
- Primary grid:
  1. `mode_a|(L15,lag2)` (prefer first)
  2. `mode_a|(L10,lag2)`
  3. `mode_a|(L20,2)`
  4. `mode_b|(L15,price)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: SuperSmoother/DEMA/NetLead labeled EDCF; 15m $\text{Length}=5$ spam; ER/AO/PGO graft; Mode B forced while Mode A BTC $n$ already dense. Prefer Mode A (15,2), 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must stay multi-dozen-class.
- **bnb_smoke (CRITICAL after SOL):** Kill if: different $(\text{Length}, \text{lag})$ than SOL; Mode B only on BNB while SOL Mode A; no ATR. Prefer identical; long-only; ATR exit.
- **Forbidden:** SuperSmoother/DEMA/NetLead/WMA/HMA/ZLEMA substitute; ER-gate; AO/ROC/PGO; Pee TDI/TrendScore/GMMA/VQI; request.security.

---

## 4. Locked Strategy 3 (`ehlers-ultimate-smoother-dual-cross-v1`)

### 4.1 Formulation
- **Ehlers Ultimate Smoother (John Ehlers, TASC Apr 2024 / MESA):**
  AllPass − HighPass filter with zero lag in passband:
  $$a_1 = \exp\left(-\frac{\sqrt{2}\pi}{\text{Period}}\right)$$
  $$c_2 = 2 a_1 \cos\left(\frac{\sqrt{2}\pi}{\text{Period}}\right)$$
  $$c_3 = -a_1^2$$
  $$c_1 = \frac{1 + c_2 - c_3}{4}$$
  $$\text{US}_t = (1 - c_1)\text{price}_t + (2 c_1 - c_2)\text{price}_{t-1} - (c_1 + c_3)\text{price}_{t-2} + c_2 \text{US}_{t-1} + c_3 \text{US}_{t-2}$$
  $\text{fast} = \text{US}(\text{close}, Pf)$, $\text{slow} = \text{US}(\text{close}, Ps)$.
  Prefer $(Pf=10, Ps=30)$.
- **Mode A (Primary — Fast×Slow Cross):**
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
- **Mode B (Secondary — Close > Slow Gate):**
  - Long entry: $\text{crossover}(\text{fast}, \text{slow}) \land \text{close} > \text{slow}$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
  - Identical params across coins.

### 4.2 Locked Parameter Space
- $(Pf, Ps) \in \{(10, 30), (8, 24), (12, 40)\}$
- Primary grid:
  1. `mode_a|(10,30)` (prefer first)
  2. `mode_a|(8,24)`
  3. `mode_a|(12,40)`
  4. `mode_b|(10,30,close_gate)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: SuperSmoother/DEMA/NetLead labeled US; 15m $Pf=3$ spam; ER/AO/PGO graft. Prefer Mode A (10,30), 1H+.
- **sol_retention_note:** After ETH pass, if SOL $n$ huge with poor structure, try (12,40) same Mode A before family fail (still identical params).
- **bnb_smoke (CRITICAL after SOL):** Kill if: different $(Pf, Ps)$ than SOL; Mode B only on BNB; no ATR; kill if BNB needs $Ps \gg \text{SOL}$. Prefer identical; long-only; ATR exit.
- **Forbidden:** SuperSmoother/DEMA/NetLead/ZLEMA/HMA/TEMA substitute; ER-gate; AO/ROC/WMA/PGO; Pee TDI/TrendScore/GMMA/VQI; request.security.

---

## 5. Locked Strategy 4 (`ehlers-gaussian-fast-slow-cross-v1`)

### 5.1 Formulation
- **Ehlers N-Pole Gaussian Filter (John Ehlers, MESA / "Gaussian and Other Low Lag Filters"):**
  $$\omega = \frac{2\pi}{P}$$
  $$\beta = \frac{1 - \cos(\omega)}{1.414^{2/N} - 1}$$
  $$\alpha = -\beta + \sqrt{\beta^2 + 2\beta}$$
  $N=2$ pole recurrence:
  $$f_t = \alpha^2 \text{price}_t + 2(1 - \alpha) f_{t-1} - (1 - \alpha)^2 f_{t-2}$$
  $N=4$ pole recurrence (binomial expansion).
  $\text{fast} = \text{gauss}(\text{close}, Pf, N)$, $\text{slow} = \text{gauss}(\text{close}, Ps, N)$.
  Prefer $(Pf=10, Ps=30, N=2)$.
- **Mode A (Primary — Fast×Slow Cross N=2):**
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
- **Mode B (Secondary — N=4 Multipole Damping):**
  - $N=4$ same periods $(Pf=10, Ps=30)$
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or ATR stop)
  - Identical $N$ and periods across coins.

### 5.2 Locked Parameter Space
- $(Pf, Ps) \in \{(10, 30), (8, 24), (12, 40)\}$; $N \in \{2, 4\}$
- Primary grid:
  1. `mode_a|(10,30,N2)` (prefer first)
  2. `mode_a|(8,24,N2)`
  3. `mode_a|(12,40,N2)`
  4. `mode_b|(10,30,N4)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: SuperSmoother/EMA dual labeled Gaussian; 15m $Pf=3$ spam; ER/AO/PGO graft. Prefer Mode A (10,30,N=2), 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must not collapse to PGO-class single digits.
- **bnb_smoke (CRITICAL after SOL):** Kill if: different $(Pf, Ps, N)$ than SOL; Mode B only on BNB; no ATR; kill if BNB needs $N=4$ while SOL only survives $N=2$. Prefer identical params; long-only; ATR exit.
- **Forbidden:** SuperSmoother/DEMA/EMA-dual-mom/NetLead/HMA substitute; ER-gate; AO/ROC/WMA/PGO; Pee TDI/TrendScore/GMMA/VQI; request.security.

---

## 6. Locked Strategy 5 (`swenlin-pmo-signal-cross-v1`)

### 6.1 Formulation
- **DecisionPoint Price Momentum Oscillator (PMO) (Carl Swenlin, StockCharts):**
  $$\text{ROC1}_t = \left(\frac{\text{close}_t}{\text{close}_{t-1}} - 1\right) \cdot 100$$
  $$\text{customSmooth}(x, L): \text{prior} + (x - \text{prior}) \cdot \frac{2}{L}$$
  $$\text{sm1} = \text{customSmooth}(\text{ROC1}, s_1)$$
  $$\text{PMO} = \text{customSmooth}(10 \cdot \text{sm1}, s_2)$$
  $$\text{Signal} = \text{EMA}(\text{PMO}, \text{sigLen})$$
  Defaults: $s_1=35, s_2=20, \text{sigLen}=10$.
- **Mode A (Primary — PMO×Signal Cross):**
  - Long entry: $\text{crossover}(\text{PMO}, \text{Signal})$
  - Exit: $\text{crossunder}(\text{PMO}, \text{Signal})$ (or ATR stop)
- **Mode B (Secondary — PMO > 0 Confirmation):**
  - Long entry: $\text{crossover}(\text{PMO}, \text{Signal}) \land \text{PMO} > 0$
  - Exit: $\text{crossunder}(\text{PMO}, \text{Signal})$ (or ATR stop)
  - Identical params across coins.

### 6.2 Locked Parameter Space
- $(s_1, s_2, \text{sigLen}) \in \{(35, 20, 10), (25, 20, 10), (35, 15, 10), (35, 20, 8)\}$
- Primary grid:
  1. `mode_a|(35,20,10)` (prefer first)
  2. `mode_a|(25,20,10)`
  3. `mode_a|(35,15,10)`
  4. `mode_b|(35,20,10,pmo0)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: ROC-zero / MACD / PPO labeled PMO; 15m $s_1=5$ spam; ER/AO/PGO graft. Prefer Mode A (35,20,10), 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must stay multi-dozen-class.
- **bnb_smoke (CRITICAL after SOL):** Kill if: different $(s_1, s_2, \text{sigLen})$ than SOL; Mode B only on BNB; no ATR; kill if BNB needs longer $s_1$ than SOL. Prefer identical; long-only; ATR exit.
- **Forbidden:** ROC-zero primary; MACD/APO/PPO substitute; AO; WMA dual; ER-gate; Pee TDI/TrendScore/GMMA/VQI; request.security.

---

## 7. Execution Matrix Summary

| # | Strategy ID | Primary Mode A Entry | Primary Exit | Primary Parameter Set | Smoke Directives |
|---|---|---|---|---|---|
| 1 | `blau-csi-ergodic-signal-cross-v1` | `crossover(csi, sig)` | `crossunder(csi, sig)` | `q=1, r=20, s=5, u=3, ul=3` | $\ne$ TSI/BoP/RVI/Pee TDI; BNB CRITICAL |
| 2 | `ehlers-edcf-filt-lag-cross-v1` | `crossover(filt, filt[lag])` | `crossunder(filt, filt[lag])` | `Length=15, lag=2` | $\ne$ SS/DEMA/NetLead/WMA; BNB CRITICAL |
| 3 | `ehlers-ultimate-smoother-dual-cross-v1` | `crossover(fast, slow)` | `crossunder(fast, slow)` | `Pf=10, Ps=30` | $\ne$ SS/DEMA/NetLead/ZLEMA; BNB CRITICAL |
| 4 | `ehlers-gaussian-fast-slow-cross-v1` | `crossover(fast, slow)` | `crossunder(fast, slow)` | `Pf=10, Ps=30, N=2` | $\ne$ EMA-dual/SS/DEMA/NetLead; BNB CRITICAL |
| 5 | `swenlin-pmo-signal-cross-v1` | `crossover(pmo, sig)` | `crossunder(pmo, sig)` | `s1=35, s2=20, sigLen=10` | $\ne$ ROC-zero/MACD/PPO; BNB CRITICAL |
