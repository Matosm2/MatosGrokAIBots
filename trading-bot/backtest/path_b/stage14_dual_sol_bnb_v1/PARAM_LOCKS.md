# stage14-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage14-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage13 (REI BTC 1.530x -> ETH -1.201x wipe). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_9dda.md` & `stage14-dual-sol-bnb-briefs-2026-09-18_d5c4.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC->ETH Portability PRIMARY** + **BNB-portable SECONDARY** per Path B Stage 14 directives:
- **BTC->ETH Portability PRIMARY Bias:** Stage 13 lesson: `demark-rei-zero-cross` cleared BTC with 1.530x at 4H Mode B n=15, but catastrophically wiped on ETH at -1.201x. Stage 12 lesson: over-smoothing killed BTC lead entirely (0/40 never left BTC). Strategies must clear BTC first with dense Mode-A trade count $n \gg 9$ on 1H–4H majors and demonstrate direct portability to ETH liquidity without param retuning.
- **BNB-Portable SECONDARY Bias:** After BTC+ETH+SOL clear, BNB survival remains mandatory (Stage 10/11 lesson). However, never sacrifice BTC lead or over-smooth/damp to accommodate quiet BNB.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Parameter retuning per coin after a clear is strictly prohibited.
- **Density & Anti-Over-Smooth Policy:** Prefer responsive zero-cross, signed-event, range-location, band-break, causal kernel architectures. Never use stage12-class multipole/Gaussian, ultimate smoother duals, EDCF FIR-lag, or CSI-PMO signal-cross grafts.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if CSI/PMO/Gaussian/US damp grafted; Kill if parameter inflation collapses BTC $n$; Kill if Mode B forced while Mode A BTC $n$ healthy.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH wipes (stage13 REI pattern); Kill if parameters or mode retuned only on ETH; Kill if REI/DeMark overlap substitute. Prefer identical params; ETH $n$ multi-dozen.
  - `sol_smoke`: Enforce motif anti-burns, timeframe sanity, parameter validity, and retention check (after ETH, SOL $n$ must stay multi-dozen class on 6m 1H).
  - `bnb_smoke`: **CRITICAL after BTC+ETH+SOL:** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; volume graft; per-coin retuning. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–13 IDs (all), including DeMark REI / REI-zero / +-60 reclaim, PZO, TMO Main zero, Donovan Range Filter flip, CLV-SMA, Pee TDI/Direction, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, Swenlin PMO.

---

## 2. Locked Strategy 1 (`pee-ttf-zero-cross`)

### 2.1 Formulation
- **Pee Trend Trigger Factor (M.H. Pee, TASC Dec 2004 / Traders' Tips):**
  $$\text{buy} = \text{highest}(\text{high}, L) - \text{lowest}(\text{low}[L], L)$$
  $$\text{sell} = \text{highest}(\text{high}[L], L) - \text{lowest}(\text{low}, L)$$
  $$\text{den} = 0.5 \cdot (\text{buy} + \text{sell})$$
  $$\text{TTF} = \begin{cases} 100 \cdot \frac{\text{buy} - \text{sell}}{\text{den}} & \text{if } \text{den} \ne 0 \\ 0 & \text{otherwise} \end{cases}$$
  Prefer **$L=15$**.
- **Mode A (BTC->ETH-PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(\text{TTF}, 0)$
  - Exit: $\text{crossunder}(\text{TTF}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / Pee classic):**
  - Long entry: $\text{crossover}(\text{TTF}, 100)$
  - Exit: $\text{crossunder}(\text{TTF}, -100)$ (or ATR stop)
  - Evaluated with identical $L$ across all coins only if Mode A over-whips BNB.

### 2.2 Locked Parameter Space
- Sweep: $L \in \{10, 15, 20\}$
- Primary grid:
  1. `mode_a|(L15)` (preferred)
  2. `mode_a|(L10)`
  3. `mode_a|(L20)`
  4. `mode_b|(L15)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if CSI/PMO/Gaussian damp grafted; Kill if $L > 25$ collapses BTC $n$; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A $L=15$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes (stage13 REI pattern); Kill if $L$ or Mode retuned only on ETH; Kill if REI substitute.
- **sol_smoke:** Kill if TDI/REI/RWI/Donchian labeled TTF; 15m $L \le 5$ spam; ER/AO/PGO/stage12-13. Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
- **bnb_smoke:** Kill if different $L$ than SOL; Mode B shorts ungated; no ATR; volume graft. Kill if BNB needs $L \ne \text{SOL}$. Prefer identical params; long-only; ATR exit.
- **Forbidden:** Pee TDI/Direction; REI/PZO/TMO/RF/CLV; RWI; Donchian; ADX; ER-gate; stage12 duals; request.security.

---

## 3. Locked Strategy 2 (`hannula-pfe-zero-cross`)

### 3.1 Formulation
- **Polarized Fractal Efficiency (Hans Hannula, TASC 1994):**
  $$\text{path} = \sum_{i=1}^{n} \sqrt{(\text{close}_i - \text{close}_{i-1})^2 + 1}$$
  $$\text{straight} = \sqrt{(\text{close}_t - \text{close}_{t-n})^2 + n^2}$$
  $$\text{raw} = \begin{cases} 100 \cdot \text{sign}(\text{close}_t - \text{close}_{t-n}) \cdot \frac{\text{straight}}{\text{path}} & \text{if } \text{path} \ne 0 \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{PFE} = \text{EMA}(\text{raw}, \text{smooth})$$
  Prefer **$\text{period}=10, \text{smooth}=5$**.
- **Mode A (BTC->ETH-PRIMARY):**
  - Long entry: $\text{crossover}(\text{PFE}, 0)$
  - Exit: $\text{crossunder}(\text{PFE}, 0)$ (or ATR stop)
- **Mode B (BNB quiet / quality hold):**
  - Long entry: $\text{crossover}(\text{PFE}, 0) \land \text{PFE} > 20$
  - Exit: $\text{crossunder}(\text{PFE}, 0)$ (or ATR stop)
  - NOT $|\text{PFE}| > 50$ threshold as Mode A.

### 3.2 Locked Parameter Space
- Sweep: $\text{period} \in \{8, 10, 14\}$, $\text{smooth} \in \{3, 5, 8\}$
- Primary grid:
  1. `mode_a|(p10,s5)` (preferred)
  2. `mode_a|(p8,s3)`
  3. `mode_a|(p14,s8)`
  4. `mode_b|(p10,s5)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if smooth raised into stage12-damp territory ($\text{smooth} > 15$); Kill if Mode A becomes $|\text{PFE}| > 50$ threshold; Kill if ER $\times$ SMA graft. Prefer Mode A $(10, 5)$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if period/smooth retuned only on ETH; Kill if REI substitute.
- **sol_smoke:** Kill if ER-gate/VHF labeled PFE; 15m $\text{period} \le 3$; stage12-13. Retention check: after ETH, SOL $n$ multi-dozen class.
- **bnb_smoke:** Kill if different $(\text{period}, \text{smooth})$ than SOL; Mode B shorts ungated; no ATR; volume graft.
- **Forbidden:** ER-gate; VHF/RAVI threshold Mode A; REI/PZO/TMO/RF/CLV; stage12 duals; request.security.

---

## 4. Locked Strategy 3 (`absolute-strength-hist-zero`)

### 4.1 Formulation
- **Absolute Strength Histogram (ASH RSI-method, SMA internals):**
  $$d_t = \text{close}_t - \text{close}_{t-1}$$
  $$\text{bulls}_t = 0.5 \cdot (|d_t| + d_t)$$
  $$\text{bears}_t = 0.5 \cdot (|d_t| - d_t)$$
  $$\text{avgB} = \text{SMA}(\text{bulls}, \text{length})$$
  $$\text{avgS} = \text{SMA}(\text{bears}, \text{length})$$
  $$\text{smB} = \text{SMA}(\text{avgB}, \text{smooth})$$
  $$\text{smS} = \text{SMA}(\text{avgS}, \text{smooth})$$
  $$\text{ASH} = \text{smB} - \text{smS}$$
  Prefer **$\text{length}=9, \text{smooth}=2$**. Use **SMA** internals (not WMA).
- **Mode A (BTC->ETH-PRIMARY):**
  - Long entry: $\text{crossover}(\text{ASH}, 0)$
  - Exit: $\text{crossunder}(\text{ASH}, 0)$ (or ATR stop)
- **Mode B (BNB quiet / quality hold):**
  - Long entry: $\text{crossover}(\text{ASH}, 0) \land \text{ASH} > 0$
  - Exit: $\text{crossunder}(\text{ASH}, 0)$ (or ATR stop)

### 4.2 Locked Parameter Space
- Sweep: $\text{length} \in \{7, 9, 14\}$, $\text{smooth} \in \{1, 2, 3\}$
- Primary grid:
  1. `mode_a|(len9,sm2)` (preferred)
  2. `mode_a|(len7,sm1)`
  3. `mode_a|(len14,sm3)`
  4. `mode_b|(len9,sm2)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if length/smooth raised into stage12-damp ($\text{smooth} > 10$); Kill if Wilder RSI substitute; Kill if TMO/PZO graft. Prefer Mode A $(9, 2)$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if params retuned only on ETH; Kill if RSI OB/OS replaces zero-cross.
- **sol_smoke:** Kill if RSI/Stoch/CMO/TMO labeled ASH; 15m $\text{length} \le 3$; stage12-13. Retention check: after ETH, SOL $n$ multi-dozen class.
- **bnb_smoke:** Kill if different $(\text{length}, \text{smooth})$ than SOL; Mode B shorts ungated; no ATR; volume graft.
- **Forbidden:** Wilder RSI; Stoch; CMO-zero; TMO/PZO/REI; WMA dual-price; stage12 duals; request.security.

---

## 5. Locked Strategy 4 (`leibfarth-apz-break-flip`)

### 5.1 Formulation
- **Adaptive Price Zone (Joe Leibfarth, TASC Sep 2006 / Traders' Tips):**
  $$\text{ds} = \text{EMA}(\text{EMA}(\text{close}, \text{period}), \text{period})$$
  $$\text{dsg} = \text{EMA}(\text{EMA}(\text{high} - \text{low}, \text{period}), \text{period})$$
  $$\text{up} = \text{ds} + \text{BandPct} \cdot \text{dsg}$$
  $$\text{dn} = \text{ds} - \text{BandPct} \cdot \text{dsg}$$
  Prefer **$\text{period}=20, \text{BandPct}=1.4$**. **No ADX.**
- **Mode A (BTC->ETH-PRIMARY break-flip):**
  - Long entry: $\text{crossover}(\text{close}, \text{up})$
  - Exit: $\text{crossunder}(\text{close}, \text{dn})$ (or ATR stop)
- **Mode B (BNB quiet / article-fade):**
  - Long entry: $\text{crossover}(\text{close}, \text{dn})$ (reclaim back inside lower band)
  - Exit: $\text{crossover}(\text{close}, \text{up})$ (or ATR stop)

### 5.2 Locked Parameter Space
- Sweep: $\text{period} \in \{14, 20, 30\}$, $\text{BandPct} \in \{1.2, 1.4, 1.8\}$
- Primary grid:
  1. `mode_a|(p20,b1.4)` (preferred)
  2. `mode_a|(p14,b1.2)`
  3. `mode_a|(p30,b1.8)`
  4. `mode_b|(p20,b1.4)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if period/BandPct inflated until flips collapse; Kill if ADX gate grafted; Kill if dual-MA cross replaces; Kill if stage12 damp grafted. Prefer Mode A $(20, 1.4)$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if period/BandPct retuned only on ETH; Kill if Keltner ATR substitute.
- **sol_smoke:** Kill if Keltner/SuperTrend/RF/AccelBands labeled APZ; 15m $\text{period} \le 5$; ADX/ER/stage12-13. Retention check: after ETH, SOL flip $n$ multi-dozen class.
- **bnb_smoke:** Kill if different $(\text{period}, \text{BandPct})$ than SOL; Mode B shorts ungated; no ATR; volume graft.
- **Forbidden:** ADX; Keltner/SuperTrend/Donchian/RF/AccelBands labeled APZ; REI/PZO/TMO/CLV; stage12 FIR/Gaussian; request.security.

---

## 6. Locked Strategy 5 (`nadaraya-rq-estimate-cross`)

### 6.1 Formulation
- **Causal Nadaraya-Watson Rational Quadratic Kernel (jdehorty / non-repainting endpoint):**
  $$w_i = \left(1 + \frac{i^2}{2 \cdot \alpha \cdot h^2}\right)^{-\alpha} \quad \text{for } i = 0 \dots (\text{lookback}-1)$$
  $$\hat{y}_t = \frac{\sum_{i=0}^{\text{lookback}-1} \text{close}_{t-i} \cdot w_i}{\sum_{i=0}^{\text{lookback}-1} w_i}$$
  Prefer **$\text{lookback}=8, \alpha=8.0$**. **Causal / non-repainting only** — no two-sided envelope.
- **Mode A (BTC->ETH-PRIMARY):**
  - Long entry: $\text{crossover}(\text{close}, \hat{y})$
  - Exit: $\text{crossunder}(\text{close}, \hat{y})$ (or ATR stop)
- **Mode B (BNB quiet / quality hold):**
  - Long entry: $\text{crossover}(\text{close}, \hat{y}) \land \text{slope}(\hat{y}) > 0$
  - Exit: $\text{crossunder}(\text{close}, \hat{y})$ (or ATR stop)

### 6.2 Locked Parameter Space
- Sweep: $\text{lookback} \in \{5, 8, 14\}$, $\alpha \in \{1.0, 8.0, 25.0\}$
- Primary grid:
  1. `mode_a|(lb8,a8)` (preferred)
  2. `mode_a|(lb5,a1)`
  3. `mode_a|(lb14,a25)`
  4. `mode_b|(lb8,a8)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if lookback/alpha inflated until $n$ collapses; Kill if repainting two-sided kernel used; Kill if Gaussian multipole / EDCF substitute. Prefer Mode A $(8, 8)$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if lookback/alpha retuned only on ETH; Kill if repaint envelope.
- **sol_smoke:** Kill if repaint NW / Gaussian / ALMA / EDCF labeled RQ; 15m $\text{lookback} \le 3$; stage12-13. Retention check: after ETH, SOL $n$ multi-dozen class.
- **bnb_smoke:** Kill if different $(\text{lookback}, \alpha)$ than SOL; Mode B shorts ungated; no ATR; volume graft.
- **Forbidden:** Repaint two-sided NW; Ehlers Gaussian multipole; ALMA/EDCF/SMA dual; REI/PZO/TMO/RF/CLV; request.security.
