# stage7-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage7-dual-sol-bnb-v1`  
**Authoritative Briefs:** `CODING_KICK_f02a.md` & `stage7-dual-sol-bnb-briefs-2026-09-18_012a.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce the **DUAL SOL+BNB survival** paradigm across SOL and BNB per Path B Stage 7 directives:
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **SOL Retention After ETH Clear:** After ETH clear, run explicit SOL retention diagnostics before declaring a SOL failure (evaluating trade density, impulse capture, whether ER / SPB / RWI / Reverse EMA are over-gating or over-smoothing on SOL).
- **Mandatory Dual Smokes:** Each strategy must satisfy its dedicated `sol_smoke` and `bnb_smoke` constraints. Failed smoke conditions disqualify parameter sets.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on the execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness).
- **Hard Excludes:** All stage 1–6 IDs (all), including FRAMA, HMA, McGinley, CTI, VIDYA, SuperSmoother, PVO, P4H, MAD, Roofing, Decycler, ITrend, ALMA, T3, ZLEMA, VWMA×SMA, CG, CMO-zero, ATR%ile-primary. Parked: Klinger, VR+breakout, % Envelopes, Qstick. Burns: KAMA recursive, SuperTrend, Donchian, ADX/DMI, Laguerre, RSI, etc.

---

## 2. Locked Strategy 1 (`er-sma-gate-cross-v1`)

### 2.1 Formulation
- **Kaufman Efficiency Ratio (ER as gate ONLY, $\neq$ recursive KAMA line):**
  $$\text{ER}_t = \frac{|\text{close}_t - \text{close}_{t-N}|}{\sum_{j=0}^{N-1} |\text{close}_{t-j} - \text{close}_{t-j-1}|}$$
  Denom $= 0 \implies \text{ER} = 0$. $N \in \{10, 14, 20\}$, $\text{thr} \in \{0.30, 0.35, 0.40\}$.
- **Mode A (Primary):**
  - $\text{fast} = \text{ta.sma}(\text{close}, L_f)$
  - $\text{slow} = \text{ta.sma}(\text{close}, L_s)$
  - Long entry: $\text{crossover}(\text{fast}, \text{slow}) \land \text{ER} > \text{thr}$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ (or soft decay: $\text{ER} < \text{thr} \times 0.7$; locked convention: opposite cross with ATR stop)
  - Locked pairs $(L_f, L_s) \in \{(9, 21), (10, 30), (12, 26)\}$.
- **Mode B (Secondary denser):**
  - Long while $\text{close} > \text{slow} \land \text{ER} > \text{thr}$ — only if Mode A SOL under-fires.
- **Exit:**
  - Opposite cross / ATR trailing stop.

### 2.2 Locked Parameter Space
- $N \in \{10, 14, 20\}$
- $\text{thr} \in \{0.30, 0.35, 0.40\}$
- $(L_f, L_s) \in \{(9, 21), (10, 30), (12, 26)\}$
- Primary grid: Mode A $(L_f, L_s)=(10,30)$ with $N=10, \text{thr}=0.35$; $(9,21)$ with $N=14, \text{thr}=0.30$; $(12,26)$ with $N=20, \text{thr}=0.40$; Mode B secondary with $(10,30), N=10, \text{thr}=0.35$.
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: KAMA/SC disguised as ER; thr retuned per coin; 15m thr=0.15. Prefer Mode A, $N=10$, thr=0.35, $(10,30)$, 1H+.
- **sol_retention_note:** After ETH pass, SOL trade count must not collapse vs ETH under same params. If ER stuck low during SOL impulse legs, flag as over-gating.
- **bnb_smoke:** Kill if: different thr/$N$ than SOL; Mode B ungated shorts; ADX grafted. Prefer identical params; long-only; ATR.

---

## 3. Locked Strategy 2 (`ehlers-super-passband-rms-v1`)

### 3.1 Formulation
- **Ehlers Super Passband Filter (S&C Jul 2016):**
  $\alpha_1 = 5.0 / P_1$, $\alpha_2 = 5.0 / P_2$ (distinct from standard $\alpha = 2/(N+1)$).
  $$\text{PB}_t = (\alpha_1 - \alpha_2)\text{close}_t + [\alpha_2(1-\alpha_1) - \alpha_1(1-\alpha_2)]\text{close}_{t-1} + [(1-\alpha_1) + (1-\alpha_2)]\text{PB}_{t-1} - (1-\alpha_1)(1-\alpha_2)\text{PB}_{t-2}$$
- **Root Mean Square (RMS):**
  $$\text{RMS}_t = \sqrt{\text{ta.sma}(\text{PB}^2, \text{rmsLen})}$$
  $\text{rmsLen} \in \{40, 50\}$.
- **Mode A (Primary / Article Rules):**
  - Long entry: $\text{crossover}(\text{PB}, -\text{RMS})$
  - Exit: $\text{crossunder}(\text{PB}, \text{RMS}) \lor \text{crossunder}(\text{PB}, -\text{RMS})$ or ATR stop.
  - Locked pairs $(P_1, P_2) \in \{(20, 40), (30, 50), (40, 60)\}$ with $P_1 < P_2$.
- **Mode B (Secondary):**
  - PB zero-cross only — secondary if Mode A under-trades SOL.
- **Exit:**
  - Article exits; ATR trailing stop.

### 3.2 Locked Parameter Space
- $(P_1, P_2) \in \{(20, 40), (30, 50), (40, 60)\}$
- $\text{rmsLen} \in \{40, 50\}$
- Primary grid: Mode A $(40,60), \text{rmsLen}=50$; Mode A $(30,50), \text{rmsLen}=50$; Mode A $(20,40), \text{rmsLen}=40$; Mode B $(30,50)$ zero-cross.
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: Roofing substitute; MACD(12,26,9) labeled passband; 15m $P_1=10$. Prefer Mode A $(40,60)$ or $(30,50)$, $\text{rmsLen}=50$, 1H+.
- **sol_retention_note:** SOL Mode-A $n$ after ETH must not go silent. If PB never clears $-\text{RMS}$ on SOL impulses, flag as over-smoothed.
- **bnb_smoke:** Kill if: retune $P_1/P_2$ per coin; Mode B-only ungated shorts; no ATR. Prefer identical periods; long-only.
- **Forbidden:** Roofing/HP; SuperSmoother; Decycler; ITrend; FRAMA/HMA/McGinley; classic MACD substitute.

---

## 4. Locked Strategy 3 (`rwi-high-low-threshold-v1`)

### 4.1 Formulation
- **Mike Poulos Random Walk Index (RWI High / Low):**
  For each $i \in [2, \text{period}]$:
  $$\text{RWI\_High}(i) = \frac{\text{High}_t - \text{Low}_{t-i}}{\text{ATR}(i) \cdot \sqrt{i}}$$
  $$\text{RWI\_Low}(i) = \frac{\text{High}_{t-i} - \text{Low}_t}{\text{ATR}(i) \cdot \sqrt{i}}$$
  $\text{RWI\_High} = \max_i \text{RWI\_High}(i)$, $\text{RWI\_Low} = \max_i \text{RWI\_Low}(i)$.
  Guard: $\text{ATR}(i) > 0$.
- **Mode A (Poulos Dual-Horizon):**
  - $\text{rwiH\_L} = \max_{i \le L} \text{RWI\_High}(i)$ (Long-term High displacement)
  - $\text{rwiL\_S} = \max_{i \le S} \text{RWI\_Low}(i)$ (Short-term Low displacement)
  - Long entry: $\text{rwiH\_L} > \text{thr} \land \text{rwiL\_S} > \text{thr} \land \text{rwiL\_S}_t > \text{rwiL\_S}_{t-1}$ (Short-term pullback confirm during long-term uptrend).
  - Exit: $\text{rwiH\_L} < \text{thr} \lor \text{rwiL\_L} > \text{rwiH\_L}$ or ATR stop.
  - Locked pairs $(S, L) \in \{(5, 40), (7, 64), (8, 48)\}$. Threshold locked at $\text{thr}=1.0$ first.
- **Mode B (Secondary denser):**
  - Long while $\text{rwiH\_L} > 1.0 \land \text{rwiH\_L} > \text{rwiL\_L}$.
- **Exit:**
  - Mode A exit; ATR trailing stop.

### 4.2 Locked Parameter Space
- $(S, L) \in \{(5, 40), (7, 64), (8, 48)\}$
- $\text{thr} \in \{1.0, 1.2\}$ (1.0 default)
- Primary grid: Mode A $(7,64), \text{thr}=1.0$; Mode A $(5,40), \text{thr}=1.0$; Mode A $(8,48), \text{thr}=1.0$; Mode B $(7,64), \text{thr}=1.0$.
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: ATR%ile percentile grafted as entry; Donchian/SuperTrend substitute; $S=2$ on 15m. Prefer Mode A $(7,64)$ or $(5,40)$, 1H+.
- **sol_retention_note:** SOL must produce ST Low peaks during LT uptrend after ETH; silence after ETH = over-long $L$ or thr too high.
- **bnb_smoke:** Kill if: per-coin $(S,L)$ retune; thr lowered only on BNB; no ATR. Prefer identical params; long-only.
- **Forbidden:** ATR%ile-primary; SuperTrend; Donchian primary; ADX; FRAMA/HMA/McGinley.

---

## 5. Locked Strategy 4 (`ehlers-reverse-ema-trend-cycle-v1`)

### 5.1 Formulation
- **Ehlers Reverse EMA Wave (TASC Sep 2017):**
  $CC = 1 - \alpha$, $\text{EMA} = \alpha \cdot \text{close} + CC \cdot \text{EMA}_{t-1}$.
  $$\text{RE}_1 = CC \cdot \text{EMA} + \text{EMA}_{t-1}$$
  $$\text{RE}_k = CC^{2^{k-1}} \cdot \text{RE}_{k-1} + \text{RE}_{k-1, t-1} \quad (k=2 \dots 8)$$
  $$\text{Wave}(\alpha) = \text{EMA} - \alpha \cdot \text{RE}_8$$
- **Mode A (Article Strategy):**
  - $\text{trend} = \text{Wave}(\alpha_t)$
  - $\text{cycle} = \text{Wave}(\alpha_c)$
  - Long entry: $\text{trend} > 0 \land \text{crossover}(\text{cycle}, 0)$
  - Exit: $\text{crossunder}(\text{trend}, 0) \lor \text{crossunder}(\text{cycle}, 0)$ or ATR stop.
  - Locked pairs $(\alpha_t, \alpha_c) \in \{(0.05, 0.30), (0.08, 0.25), (0.05, 0.20)\}$ with $\alpha_t < \alpha_c$.
- **Mode B (Secondary denser):**
  - Single $\text{Wave}(\alpha=0.10)$ zero-cross only — if Mode A under-fires SOL.
- **Exit:**
  - Article exits; ATR trailing stop.

### 5.2 Locked Parameter Space
- $(\alpha_t, \alpha_c) \in \{(0.05, 0.30), (0.08, 0.25), (0.05, 0.20)\}$
- Primary grid: Mode A $(0.05, 0.30)$; Mode A $(0.08, 0.25)$; Mode A $(0.05, 0.20)$; Mode B $(\alpha=0.10)$.
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: Laguerre/Roofing substitute; plain EMA×EMA labeled reverse; 15m $\alpha_c=0.5$. Prefer Mode A $(0.05, 0.30)$, 1H+.
- **sol_retention_note:** Cycle crosses must fire on SOL while Trend>0 after ETH; if Trend stuck $\le 0$ through SOL up-legs $\to$ kill.
- **bnb_smoke:** Kill if: different $\alpha$ than SOL; Mode B shorts ungated; SuperSmoother graft. Prefer identical $\alpha$; long-only; ATR.
- **Forbidden:** Laguerre; Roofing; SuperSmoother; Decycler; ITrend; FRAMA/HMA/McGinley; RSI.

---

## 6. Summary of Locked Sweep Grid (4 Strategies)

| Strategy ID | Primary Mode | Parameter Grid | Timeframes |
|---|---|---|---|
| `er-sma-gate-cross-v1` | Mode A (SMA×SMA + ER gate) | $(10,30,N10,\text{thr}0.35), (9,21,N14,\text{thr}0.30), (12,26,N20,\text{thr}0.40)$, Mode B $(10,30,N10,\text{thr}0.35)$ | 1H, 4H |
| `ehlers-super-passband-rms-v1` | Mode A (PB $\times$ -RMS) | $(40,60,\text{rms}50), (30,50,\text{rms}50), (20,40,\text{rms}40)$, Mode B $(30,50)$ zero-cross | 1H, 4H |
| `rwi-high-low-threshold-v1` | Mode A (Poulos LT High + ST Low peak) | $(7,64,\text{thr}1.0), (5,40,\text{thr}1.0), (8,48,\text{thr}1.0)$, Mode B $(7,64,\text{thr}1.0)$ | 1H, 4H |
| `ehlers-reverse-ema-trend-cycle-v1` | Mode A (Trend>0 + Cycle zero-cross) | $(\alpha_t 0.05,\alpha_c 0.30), (\alpha_t 0.08,\alpha_c 0.25), (\alpha_t 0.05,\alpha_c 0.20)$, Mode B $(\alpha=0.10)$ | 1H, 4H |

Total parameter variations per asset: 4 (ER-SMA) + 4 (SuperPassband) + 4 (RWI) + 4 (ReverseEMA) = 16 cells across 2 timeframes = 32 cells per asset.  
Stop-ladder progression: BTC (32 cells) $\to$ ETH (passed cells) $\to$ SOL (passed cells + retention checks) $\to$ BNB (passed cells).
