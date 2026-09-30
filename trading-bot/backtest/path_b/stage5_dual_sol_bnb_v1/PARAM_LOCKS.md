# stage5-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-17  
**Research ID:** `stage5-dual-sol-bnb-v1`  
**Authoritative Briefs:** `CODING_KICK_762f.md` & `stage5-dual-sol-bnb-briefs-2026-09-17_dc21.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce the **DUAL-SURVIVAL** paradigm across SOL and BNB per Path B Stage 5 directives:
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- All indicator mathematical forms, parameter grids, and scale conventions are locked **before** scoring any assets on the stop-ladder (BTC → ETH → SOL → BNB).
- **Stop-ladder rule:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Dual Smokes:** Each strategy must satisfy its dedicated `sol_smoke` and `bnb_smoke` constraints. Failed smoke conditions disqualify parameter sets from promotion.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe levels are tracked via running state machines or same-TF longer lookbacks on the execution timeframe.
- **Costs:** 0.1%/side fee + 5 bps slippage (consistent with Path B standard harness).
- **No burned filters or grafts:** Excludes all stage 1–4 IDs, Decycler, ITrend, PVO, P4H, Roofing filter (HP+SS), BB/stdev bands, Donchian, KAMA, SMA200, EMA ribbons, ADX/DMI, ConnorsRSI, OBV, CMF, and other burned items.

---

## 2. Locked Strategy 1 (`cti-fast-slow-threshold-v1`)

### 2.1 Formulation
- **Ehlers Correlation Trend Indicator (CTI, TASC May 2020):**
  Pearson correlation coefficient $r$ between close prices and an ideal rising straight line over lookback $L$:
  $$X_i = \text{close}[t - L + 1 + i], \quad Y_i = i, \quad \text{for } i \in \{0, \dots, L-1\}$$
  $$S_x = \sum_{i=0}^{L-1} X_i, \quad S_y = \sum_{i=0}^{L-1} Y_i = \frac{L(L-1)}{2}$$
  $$S_{xx} = \sum_{i=0}^{L-1} X_i^2, \quad S_{yy} = \sum_{i=0}^{L-1} Y_i^2 = \frac{(L-1)L(2L-1)}{6}$$
  $$S_{xy} = \sum_{i=0}^{L-1} X_i Y_i$$
  $$\text{CTI}(L)_t = \frac{L \cdot S_{xy} - S_x \cdot S_y}{\sqrt{(L \cdot S_{xx} - S_x^2) \cdot (L \cdot S_{yy} - S_y^2)}} \in [-1.0, +1.0]$$
  If denominator $\le 0$, $\text{CTI} = 0.0$.
- **Mode A (Primary):**
  - Long entry: $\text{crossover}(\text{ctiFast}, \text{buyTh})$ (onset of linear trend).
  - Exit / flat: $\text{crossunder}(\text{ctiSlow}, \text{sellTh})$ (trend exhaustion / breakdown).
  - Defaults: $\text{fastL}=20, \text{slowL}=40, \text{buyTh}=0.5, \text{sellTh}=0.0$.
- **Mode B (Denser):**
  - Long while $\text{ctiFast} > 0.0$; exit when $\text{ctiFast} < 0.0$. Mode A first.
- **Dead-Bar Skip:**
  - Skip bar if $(\text{high} - \text{low}) / \text{close} < \text{atrPctFloor}$ (dead bar filter, default $0.001$).
- **Exit:**
  - Mode A sell rule or optional ATR trailing stop.

### 2.2 Locked Parameter Space
- $(\text{fastL}, \text{slowL}) \in \{(10, 20), (20, 40)\}$
- $\text{buyTh} \in \{0.3, 0.5\}$; $\text{sellTh} = 0.0$
- Modes: Mode A, Mode B
- Execution Timeframes: 1H, 4H

### 2.3 Smoke Constraints
- **sol_smoke:** Kill if Mode B ungated on 15m; $L=10$ without dead-bar skip; treating CTI as cycle extractor. Prefer 1H+, Mode A (20/40, 0.5/0), skip dead bars.
- **bnb_smoke:** Kill if different thresholds than SOL; $\text{slowL} \ge 60$ on 4H; short every zero-cross without buyTh asymmetry. Prefer identical params; long-only first.

---

## 3. Locked Strategy 2 (`atrpct-percentile-sma-cross-v1`)

### 3.1 Formulation
- **ATR% Percentile Regime Band:**
  $$\text{atrVal}_t = \text{ATR}(14)_t$$
  $$\text{atrPct}_t = 100 \times \frac{\text{atrVal}_t}{\text{close}_t}$$
  $$\text{rank}_t = \text{percentrank}(\text{atrPct}, W)_t, \quad W \in \{100, 150\}$$
  Percentile rank measures volatility compression vs expansion on a $[0, 100]$ scale.
- **Regime Gate:**
  Entries are permitted if and only if $lo \le \text{rank}_t \le hi$.
  Skips dead compression ($< lo$) and manic blow-offs ($> hi$, when $hi < 100$).
- **Mode A (Primary):**
  - $\text{fast} = \text{SMA}(\text{close}, f), \quad \text{slow} = \text{SMA}(\text{close}, s)$.
  - $(f, s) \in \{(10, 30), (20, 50)\}$ — **strictly NOT 200**.
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$ while $lo \le \text{rank}_t \le hi$.
  - Short entry: $\text{crossunder}(\text{fast}, \text{slow})$ while $lo \le \text{rank}_t \le hi$.
- **Mode B:**
  - $\text{close} \times \text{SMA}(\text{len})$ while regime is active ($\text{len} \in \{20, 50\}$).
- **Exit:**
  - Opposite cross OR regime leave ($\text{rank}_t < lo$) + ATR trailing stop.

### 3.2 Locked Parameter Space
- $(lo, hi) \in \{(25, 85), (30, 100), (40, 80)\}$
- Lookback window $W \in \{100, 150\}$
- SMA pairs: $(10, 30)$ and $(20, 50)$ (Mode A); $\text{len} \in \{20, 50\}$ (Mode B)
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints
- **sol_smoke:** Kill if squeeze-breakout framing; EMA/RSI grafts; SMA200; 15m with $W=100$. Prefer 1H+, $(20, 50)$, $lo=25$, try $hi=100$ if under-firing.
- **bnb_smoke:** Kill if regime off / $lo=0$ (ungated SMA risk). Prefer $lo \ge 25$, `exit_on_regime_leave = True`, identical band to SOL.

---

## 4. Locked Strategy 3 (`mad-channel-break-rvol-v1`)

### 4.1 Formulation
- **Median / MAD Bands (≠ Bollinger Bands):**
  $$\text{med}_t = \text{median}(\text{close}, N)_t, \quad N \in \{20, 34\}$$
  $$\text{MAD}_t = \text{median}(|\text{close}_i - \text{med}_t| \text{ for } i \in [t-N+1, t])$$
  $$\text{madSigma}_t = 1.4826 \times \text{MAD}_t$$
  $$\text{upper}_t = \text{med}_t + k \cdot \text{madSigma}_t, \quad \text{lower}_t = \text{med}_t - k \cdot \text{madSigma}_t, \quad k \in \{1.5, 2.0, 2.5\}$$
  $1.4826 \approx 1/\Phi^{-1}(0.75)$ is the asymptotic normal consistency factor. Unlike sample standard deviation $\sigma$, MAD is outlier-robust and immune to single wick explosions.
- **Mode A (Primary — Trend Breakout):**
  - Long entry: $\text{close}_t > \text{upper}_t$ after prior $\text{close}_{t-1} \le \text{upper}_{t-1}$ (**close-beyond only, strictly NOT wick-only**).
  - Short entry: $\text{close}_t < \text{lower}_t$ after prior $\text{close}_{t-1} \ge \text{lower}_{t-1}$.
- **Light RVOL Participation Gate (ON by default for dual smoke):**
  - $\text{RVOL}_t = \frac{\text{volume}_t}{\text{SMA}(\text{volume}, 20)_t} \ge k_r$, with $k_r \in \{1.0, 1.2\}$ required on the breakout bar.
- **Mode B (Secondary — Mean Revert):**
  - Fade outer touches back to $\text{med}$ (secondary, only if Mode A fails).
- **Exit:**
  - Close back through $\text{med}_t$ (Mode A) or opposite band; ATR trailing stop.

### 4.2 Locked Parameter Space
- $N \in \{20, 34\}$
- $k \in \{1.5, 2.0, 2.5\}$, prefer $2.0$
- $k_r \in \{1.0, 1.2\}$ (ON by default)
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints
- **sol_smoke:** Kill if BB/stdev implementation; Mode B first; $N < 15$; wick-only (must close beyond). Prefer Mode A, $N=20, k=2.0, k_r=1.0$.
- **bnb_smoke:** Kill if RVOL off + 15m; Mode B; $k=1.0$. Prefer 1H+, $k_r \ge 1.2$, Mode A only, identical $N/k$ to SOL.

---

## 5. Locked Strategy 4 (`vidya-dual-or-close-cross-v1`)

### 5.1 Formulation
- **Chande Variable Index Dynamic Average (VIDYA):**
  $$\text{cmo}_t = \text{CMO}(\text{close}, \text{cmoLen})_t \in [-100, +100]$$
  $$F = \frac{2}{\text{emaLen} + 1}$$
  $$\alpha_t = F \times \frac{|\text{cmo}_t|}{100.0} \in [0, F]$$
  $$\text{VIDYA}_t = \alpha_t \cdot \text{close}_t + (1 - \alpha_t) \cdot \text{VIDYA}_{t-1}$$
- **CMO Scale Convention Lock:**
  Chande's CMO is defined as $100 \times \frac{S_u - S_d}{S_u + S_d}$. The scale is strictly normalized to $[0, 1]$ via $|\text{cmo}| / 100.0$.
  When momentum dies ($|\text{cmo}| \to 0$), $\alpha \to 0$ and VIDYA flattens out.
  When momentum reaches maximum ($|\text{cmo}| \to 100$), $\alpha \to F$ (standard EMA speed).
- **Mode A (Primary — Dual VIDYA):**
  - Fast VIDYA: $\text{emaLen}=9, \text{cmoLen}=12$.
  - Slow VIDYA: $\text{emaLen}=20, \text{cmoLen}=50$.
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$.
  - Short entry: $\text{crossunder}(\text{fast}, \text{slow})$.
- **Mode B (Close × VIDYA):**
  - Long entry: $\text{crossover}(\text{close}, \text{VIDYA}(20, 9))$.
- **Slope Filter (`slopeMin`, ON for BNB smoke):**
  - Requires non-flat slope: $\frac{|\text{VIDYA}_t - \text{VIDYA}_{t-1}|}{\text{close}_t} > \text{slopeMin}$ (default $0.0003$).
- **Exit:**
  - Opposite cross; ATR trailing stop.

### 5.2 Locked Parameter Space
- Mode A: $(9, 12) \times (20, 50)$
- Mode B: $\text{close} \times \text{VIDYA}(20, 9)$
- $\text{slopeMin} \in \{0.0\text{ (off)}, 0.0003, 0.0006\}$
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints
- **sol_smoke:** Kill if CMO-zero entry (stage 2 ID); KAMA implementation; envelope bands; 15m dual soup. Prefer Mode A fixed $(9/12) \times (20/50)$, 1H+.
- **bnb_smoke:** Kill if no `slopeMin` / flat-trade filter. Prefer `slopeMin` ON; Mode A; identical to SOL.

---

## 6. Locked Strategy 5 (`supersmoother-dual-cross-v1`)

### 6.1 Formulation
- **Ehlers 2-Pole SuperSmoother Filter (Strictly NO High-Pass / ≠ Roofing):**
  Per John Ehlers (*Cybernetic Analysis for Stocks and Futures*, Ch. 13):
  $$\theta = \frac{\sqrt{2} \cdot \pi}{L} \text{ radians}$$
  $$a_1 = \exp(-\theta)$$
  $$b_1 = 2 \cdot a_1 \cdot \cos(\theta)$$
  $$c_2 = b_1, \quad c_3 = -a_1^2, \quad c_1 = 1 - c_2 - c_3$$
  $$\text{filt}_t = c_1 \cdot \frac{\text{price}_t + \text{price}_{t-1}}{2} + c_2 \cdot \text{filt}_{t-1} + c_3 \cdot \text{filt}_{t-2}$$
  **Critical Distinction:** This is a pure low-lag 2-pole IIR lowpass smoother. It has **NO high-pass filter** stage and is **strictly NOT** the excluded Roofing filter (`roofing-filter-zero`).
- **Mode A (Primary — Dual SS Cross):**
  - $\text{fast} = \text{SS}(\text{close}, L_f), \quad \text{slow} = \text{SS}(\text{close}, L_s)$.
  - $(L_f, L_s) \in \{(8, 16), (10, 30), (12, 24)\}$. Prefer $(10, 30)$ first.
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$.
  - Short entry: $\text{crossunder}(\text{fast}, \text{slow})$.
- **Mode B (Secondary):**
  - $\text{price} \times \text{SS}(L_s)$ crossover.
- **Optional Volatility Gate (from Brief 2):**
  - Allow entry only if $\text{rank}(\text{atrPct}, 100) \ge 25$ to filter low-vol chop on BNB.
- **Exit:**
  - Opposite cross; ATR trailing stop.

### 6.2 Locked Parameter Space
- Length pairs: $(8, 16), (10, 30), (12, 24)$
- Modes: Mode A, Mode B
- ATR% rank gate: OFF vs $lo \ge 25$
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints
- **sol_smoke:** Kill if Roofing / HP added; 15m; length soup. Prefer fixed $(10, 30)$, 1H+, no HP.
- **bnb_smoke:** Kill if retuning lengths per coin; no regime/ATR% gate on first BNB pass after SOL-looking equity. Prefer add atrPct $lo \ge 25$; keep lengths shared.
- **Forbidden:** High-pass / Roofing / CyberCycle / Decycler / ITrend / ALMA / T3 / ZLEMA.
