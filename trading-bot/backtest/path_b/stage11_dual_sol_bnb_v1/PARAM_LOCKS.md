# stage11-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage11-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage10 (TII SOL→BNB wipe). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_9d9a.md` & `stage11-dual-sol-bnb-briefs-2026-09-18_8191.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BNB-survival-FIRST** and dual SOL+BNB identical parameters per Path B Stage 11 directives:
- **BNB-Survival-FIRST Bias:** Stage 10 lesson: SOL-clear then BNB-wipe is the primary choke. Strategies are designed for denser majors events that still travel to quieter BNB without per-coin retuning.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- **Denser BTC Density Bias ($n \gg 9$):** Zero-cross, dual-line, and short-lookback signed events that fire continuously on 1H majors.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Dual Smokes:**
  - `sol_smoke`: Enforce motif anti-burns, timeframe sanity, and parameter validity.
  - `bnb_smoke`: Mandatory after any SOL clear before declaring BNB fail; stresses BNB-after-SOL kill conditions (identical parameters across coins, no volume microstructure graft, no ungated shorts, long-only spot first).
- **SOL Retention After ETH Clear:** After ETH clear, run explicit SOL retention diagnostics before declaring a SOL failure (ensuring trade density stays multi-dozen class on 6m 1H, oscillator flips respond to moves).
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–10 IDs (all), including TII, Rainbow Osc, Dorsey RelVol, TCF, DEMA dual. Parked this cycle: Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual. Burned motifs: ER-gate clones; AO; ROC; WMA dual; PGO clones; PSY/RMI/TII/Dorsey midline-50; Disparity; WaveTrend; AccelBands; Rainbow zero-cross; TCF sign; DEMA fast×slow. Also never: Decycler, ITrend, PVO, P4H, MAD, SuperSmoother, FRAMA, HMA, McGinley, CTI, VIDYA, ATR%ile-primary, ALMA, T3, ZLEMA, VWMA×SMA, CG, Roofing, CMO-zero, KAMA, Gann HiLo/SSL-as-HiLo.

---

## 2. Locked Strategy 1 (`chande-trendscore-zero-cross-v1`)

### 2.1 Formulation
- **Chande TrendScore (Tushar Chande, S&C Sep 1993):**
  Signed discrete rating sum of $W$ comparisons of close vs historical closes from lag $L$ to $L + W - 1$:
  $$\text{ts}_t = \sum_{i=L}^{L + W - 1} \left( \begin{cases} +1 & \text{if } \text{close}_t \ge \text{close}_{t-i} \\ -1 & \text{if } \text{close}_t < \text{close}_{t-i} \end{cases} \right)$$
  Classic $(L=11, W=10) \implies \text{ts} \in [-10 \dots +10]$.
- **Mode A (Primary — Dense Zero-Line Polarity):**
  - Long entry: $\text{crossover}(\text{ts}, 0)$
  - Exit: $\text{crossunder}(\text{ts}, 0)$ (or ATR stop)
- **Mode B (Secondary — BNB-Quiet EMA Smooth):**
  - $\text{ts}_E = \text{EMA}(\text{ts}, 5)$
  - Long entry: $\text{crossover}(\text{ts}_E, 0)$
  - Exit: $\text{crossunder}(\text{ts}_E, 0)$ (or ATR stop)
  - Evaluated with identical params across all coins.

### 2.2 Locked Parameter Space
- $(L, W) \in \{(11, 10), (8, 8), (15, 7)\}$
- Primary grid:
  1. `mode_a|(11,10)` (prefer first)
  2. `mode_a|(8,8)`
  3. `mode_a|(15,7)`
  4. `mode_b|(11,10,ema5)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: TII/PSY labeled TrendScore; ADX graft; 15m width=3 spam; ER/AO/PGO graft. Prefer Mode A (11,10), 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must stay multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if: different $(L, W)$ than SOL; Mode B only on BNB while SOL Mode A; no ATR; volume graft. Prefer identical; long-only; ATR exit.
- **Forbidden:** ADX/DMI/VHF substitute; TII/PSY/RMI midline; TCF; ER-gate; AO/ROC/WMA/PGO; request.security.

---

## 3. Locked Strategy 2 (`pee-tdi-direction-zero-v1`)

### 3.1 Formulation
- **Trend Detection Index — Direction Indicator (M.H. Pee, S&C Oct 2001):**
  $$\text{Mom}_t = \text{close}_t - \text{close}_{t-N}$$
  $$\text{AbsMom}_t = |\text{Mom}_t|$$
  $$\text{Direction}_t = \sum_{k=0}^{N-1} \text{Mom}_{t-k}$$
  $$\text{AbsDir}_t = |\text{Direction}_t|$$
  $$\text{TDI}_t = \text{AbsDir}_t - \left( \sum_{k=0}^{2N-1} \text{AbsMom}_{t-k} - \sum_{k=0}^{N-1} \text{AbsMom}_{t-k} \right)$$
  Prefer $N=20$; also 14, 25.
- **Mode A (Primary — Dense Direction Zero-Cross):**
  - Long entry: $\text{crossover}(\text{Direction}, 0)$
  - Exit: $\text{crossunder}(\text{Direction}, 0)$ (or ATR stop)
- **Mode B (Secondary — Classic TDI Trend Gate):**
  - Long entry: $\text{crossover}(\text{Direction}, 0) \land \text{TDI} > 0$
  - Exit: $\text{crossunder}(\text{Direction}, 0) \lor \text{TDI} < 0$ (or ATR stop)
  - Identical $N$ across coins.

### 3.2 Locked Parameter Space
- $N \in \{20, 14, 25\}$
- Primary grid:
  1. `mode_a|(N20)` (prefer first)
  2. `mode_a|(N14)`
  3. `mode_a|(N25)`
  4. `mode_b|(N20)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: TII/TCF/ADX labeled TDI; RSI "Traders Dynamic Index"; 15m $N=5$ spam; ER/PGO graft. Prefer Mode A $N=20$, 1H+.
- **sol_retention_note:** After ETH pass, SOL Mode-A $n$ must stay multi-dozen-class.
- **bnb_smoke:** Kill if: different $N$ than SOL; Mode B only on BNB while SOL Mode A; ungated shorts; no ATR. Prefer identical $N$ + Mode; long-only; ATR exit.
- **Forbidden:** TII/TCF; ADX/DMI; ER-gate; AO/ROC/WMA/PGO; Traders Dynamic Index RSI stack; request.security.

---

## 4. Locked Strategy 3 (`ehlers-leading-netlead-ema-v1`)

### 4.1 Formulation
- **Ehlers Leading Indicator (John Ehlers, Cybernetic Analysis Ch. 16 / S&C):**
  $$\text{price}_t = \frac{\text{high}_t + \text{low}_t}{2}$$
  $$\text{Lead}_t = 2 \cdot \text{price}_t + (\alpha_1 - 2) \cdot \text{price}_{t-1} + (1 - \alpha_1) \cdot \text{Lead}_{t-1}$$
  $$\text{NetLead}_t = \alpha_2 \cdot \text{Lead}_t + (1 - \alpha_2) \cdot \text{NetLead}_{t-1}$$
  $$\text{EMA}_t = 0.5 \cdot \text{price}_t + 0.5 \cdot \text{EMA}_{t-1}$$
  Prefer $(\alpha_1=0.25, \alpha_2=0.50)$.
- **Mode A (Primary — Dual-Line Cross):**
  - Long entry: $\text{crossover}(\text{NetLead}, \text{EMA})$
  - Exit: $\text{crossunder}(\text{NetLead}, \text{EMA})$ (or ATR stop)
- **Mode B (Secondary — NetLead Rising Confirmation):**
  - Long entry: $\text{crossover}(\text{NetLead}, \text{NetLead}_{t-1}) \land \text{NetLead} > \text{EMA}$
  - Exit: $\text{crossunder}(\text{NetLead}, \text{EMA})$ (or ATR stop)

### 4.2 Locked Parameter Space
- $(\alpha_1, \alpha_2) \in \{(0.25, 0.50), (0.20, 0.50), (0.25, 0.33), (0.33, 0.50)\}$
- Primary grid:
  1. `mode_a|(a1_0.25,a2_0.50)` (prefer first)
  2. `mode_a|(a1_0.20,a2_0.50)`
  3. `mode_a|(a1_0.25,a2_0.33)`
  4. `mode_a|(a1_0.33,a2_0.50)`
  5. `mode_b|(a1_0.25,a2_0.50)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: DEMA/ITrend/ReverseEMA labeled ELI; 15m $\alpha$ spam; ER/AO/PGO graft; Keltner as entry gate. Prefer Mode A $(0.25, 0.50)$, 1H+.
- **sol_retention_note:** After ETH pass, if SOL $n$ huge with poor structure, try $\alpha_1=0.20$ same Mode A before family fail — still identical params.
- **bnb_smoke:** Kill if: different $(\alpha_1, \alpha_2)$ than SOL; per-coin $\alpha$ retune after SOL clear; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Forbidden:** ITrend; ReverseEMA; Laguerre; DEMA/TEMA/ZLEMA; ER-gate; AO/ROC/WMA/PGO; TII/TCF; request.security.

---

## 5. Locked Strategy 4 (`gmma-osc-zero-cross-v1`)

### 5.1 Formulation
- **Guppy Multiple Moving Average Oscillator (Daryl Guppy / Leon Wilson):**
  12 Classic Guppy EMAs:
  - Short group: $\{3, 5, 8, 10, 12, 15\}$
  - Long group: $\{30, 35, 40, 45, 50, 60\}$
  $$\text{shortMean}_t = \frac{1}{6} \sum_{k \in \{3,5,8,10,12,15\}} \text{EMA}(\text{close}, k)_t$$
  $$\text{longMean}_t = \frac{1}{6} \sum_{m \in \{30,35,40,45,50,60\}} \text{EMA}(\text{close}, m)_t$$
  $$\text{gmmaO}_t = 100 \times \frac{\text{shortMean}_t - \text{longMean}_t}{\text{longMean}_t}$$
- **Mode A (Primary — Ribbon Consensus Zero-Cross):**
  - Long entry: $\text{crossover}(\text{gmmaO}, 0)$
  - Exit: $\text{crossunder}(\text{gmmaO}, 0)$ (or ATR stop)
- **Mode B (Secondary — Signal EMA Filter):**
  - $\text{sig}_t = \text{EMA}(\text{gmmaO}, 15)$
  - Long entry: $\text{crossover}(\text{gmmaO}, \text{sig}) \land \text{gmmaO} > 0$
  - Exit: $\text{crossunder}(\text{gmmaO}, \text{sig})$ (or ATR stop)

### 5.2 Locked Parameter Space
- Classic Guppy 12 lengths locked.
- Primary grid:
  1. `mode_a|(classic12)` (prefer first)
  2. `mode_b|(classic12,sig15)`
  3. `mode_b|(classic12,sig10)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: dual-mom / EMA+RSI / DEMA/WMA dual labeled GMMA; 15m stripped to 2 EMAs; ER/AO/PGO graft. Prefer Mode A classic 12 lengths, 1H+.
- **sol_retention_note:** After ETH pass, SOL zero-cross $n$ must not collapse to single digits.
- **bnb_smoke:** Kill if: different group lengths than SOL; Mode B only on BNB while SOL Mode A; ungated shorts; no ATR; per-coin length retune. Prefer identical; long-only; ATR exit.
- **Forbidden:** dual-mom ranking; EMA+RSI; WMA/DEMA/HMA dual disguise; SMA200; ER-gate; AO/ROC/PGO; TII/Rainbow/TCF; request.security.

---

## 6. Locked Strategy 5 (`vqi-sum-sma-cross-v1` — OPTIONAL 5TH)

### 6.1 Formulation
- **Volatility Quality Index Cumulative Sum × SMA Cross (Jack L. Stridsman, S&C Aug 2002):**
  $$\text{TR}_t = \max(\text{high}_t, \text{close}_{t-1}) - \min(\text{low}_t, \text{close}_{t-1})$$
  $$\text{HL}_t = \text{high}_t - \text{low}_t$$
  Guard $\text{TR}_t > 0$ and $\text{HL}_t > 0$.
  $$\text{vqiRaw}_t = 0.5 \times \left( \frac{\text{close}_t - \text{close}_{t-1}}{\text{TR}_t} + \frac{\text{close}_t - \text{open}_t}{\text{HL}_t} \right)$$
  $$\text{vqiBar}_t = |\text{vqiRaw}_t| \times 0.5 \times \left( (\text{close}_t - \text{close}_{t-1}) + (\text{close}_t - \text{open}_t) \right)$$
  $$\text{vqiSum}_t = \text{vqiSum}_{t-1} + \text{vqiBar}_t$$
  $$\text{fast}_t = \text{SMA}(\text{vqiSum}, \text{smaFast})$$
  Prefer $\text{smaFast}=9$; also 5, 14. OHLC-only (no volume).
- **Mode A (Primary — Cumulative Volatility Dual-Line Cross):**
  - Long entry: $\text{crossover}(\text{vqiSum}, \text{fast})$
  - Exit: $\text{crossunder}(\text{vqiSum}, \text{fast})$ (or ATR stop)
- **Mode B (Secondary — Slow Baseline Confirmation):**
  - Long entry: $\text{crossover}(\text{vqiSum}, \text{fast}) \land \text{vqiSum} > \text{SMA}(\text{vqiSum}, 200)$
  - Exit: $\text{crossunder}(\text{vqiSum}, \text{fast})$ (or ATR stop)

### 6.2 Locked Parameter Space
- $\text{smaFast} \in \{9, 5, 14\}$
- Primary grid:
  1. `mode_a|(fast9)` (prefer first)
  2. `mode_a|(fast5)`
  3. `mode_a|(fast14)`
  4. `mode_b|(fast9,slow200)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: RelVol/CMF/Chaikin labeled VQI; invented formula without Stridsman match; 15m $\text{smaFast}=2$ spam; ER/AO/PGO graft. Prefer Mode A $\text{smaFast}=9$, 1H+.
- **sol_retention_note:** After ETH pass, SOL $n$ must stay multi-dozen-class.
- **bnb_smoke:** Kill if: different $\text{smaFast}$ than SOL; Mode B shorts ungated; no ATR; volume graft "to help BNB". Prefer identical params; long-only; ATR exit.
- **Forbidden:** RelVol/RVI/CMF/Chaikin Osc/ATR%ile; volume graft; ER-gate; AO/ROC/WMA/PGO; TII/Rainbow/TCF/DEMA; request.security.

---

## 7. Stop-Ladder Summary Matrix

| Step | Symbol | Role | Condition to Advance |
|---|---|---|---|
| 1 | `BTCUSDT` | Baseline filter | Mode-A last-6m return $\ge 1.2\times$ B&H AND $n > 5$. Flag $n \in [6..10]$ as thin. |
| 2 | `ETHUSDT` | Majors transfer | Mode-A last-6m return $\ge 1.2\times$ B&H AND $n > 5$. |
| 3 | `SOLUSDT` | High-volatility HARD gate | Mode-A last-6m return $\ge 1.2\times$ B&H AND $n > 5$. Execute `sol_retention_note`. |
| 4 | `BNBUSDT` | Liquidity HARD gate (BNB-survival-FIRST) | Mode-A last-6m return $\ge 1.2\times$ B&H AND $n > 5$. Execute `bnb_smoke` mandatory after SOL clear. |
