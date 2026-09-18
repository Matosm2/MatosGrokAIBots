# stage15-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage15-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage14 (Pee TTF BTC->ETH->SOL 2.257x clear -> BNB 0.093x quiet wipe). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_04f1.md` & `stage15-dual-sol-bnb-briefs-2026-09-18_364a.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BNB-Survival CRITICAL after 3-coin clear** + **Keep BTC->ETH Portability** + **Denser $n \gg 9$** per Path B Stage 15 directives:
- **BNB-Survival CRITICAL Bias:** Stage 14 lesson: `pee-ttf-zero-cross` cleared BTC, ETH, and SOL (2.257x at 4H Mode B n=8) but suffered a catastrophic quiet wipe on BNB (0.093x vs +15.36% B&H). BNB survival after a 3-coin clear is the central choke point of Stage 15. Strategies must withstand BNB's quieter, lower-volatility regime without over-whipping or under-trading.
- **BTC->ETH Portability Preservation:** Stage 13 lesson: `demark-rei-zero-cross` cleared BTC with 1.530x but wiped on ETH at -1.201x. While solving the BNB choke, strategies must not regress on ETH portability. BTC and ETH must clear first.
- **Denser $n \gg 9$ Policy:** Stage 14 TTF seats were thin ($n=6..10$ on 4H). Stage 15 targets continuous rank, dual-HP, correlation cycle, concordance, and composite rank architectures designed to generate multi-dozen trades per 6m on 1H majors.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially lengthening lookback only on BNB after SOL) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if parameter inflation collapses BTC $n$; Kill if SuperSmoother/NET grafted "to quiet"; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH wipes (stage13 REI pattern); Kill if parameters or mode retuned only on ETH; Kill if CTI Pearson-ramp or Wilder RSI substitute.
  - `sol_smoke`: Enforce motif anti-burns, timeframe sanity, parameter validity, and retention check (after ETH, SOL $n$ must stay multi-dozen class on 6m 1H).
  - `bnb_smoke`: **CRITICAL after BTC+ETH+SOL (TTF lesson):** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; volume graft; per-coin "BNB-only" lengthen. Prefer identical params; long-only; ATR exit. Kill if BNB needs params $\ne$ SOL to survive.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–14 IDs (all), including TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian multipole, Swenlin PMO.

---

## 2. Locked Strategy 1 (`ehlers-spearman-rank-zero`)

### 2.1 Formulation
- **Ehlers Spearman Rank Correlation (John Ehlers, TASC Jul 2020 / Traders' Tips):**
  - Ranks closes over window $L$ against time rank $i \in [1..L]$.
  - $d_i = \text{time\_rank}_i - \text{price\_rank}_i$
  - $\rho = 1 - \frac{6 \sum d_i^2}{L (L^2 - 1)}$
  - $\text{sig} = 2\rho - 1$
  - Prefer **$L=20$**.
- **Mode A (BTC->ETH-PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(\rho, 0)$
  - Exit: $\text{crossunder}(\rho, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / quality hold):**
  - Long entry: $\text{crossover}(\rho, 0.2)$
  - Exit: $\text{crossunder}(\rho, 0)$ (or ATR stop)
  - Evaluated with identical $L$ across all coins only if Mode A over-whips BNB.

### 2.2 Locked Parameter Space
- Sweep: $L \in \{14, 20, 28\}$
- Primary grid:
  1. `mode_a|(L20)` (preferred)
  2. `mode_a|(L14)`
  3. `mode_a|(L28)`
  4. `mode_b|(L20)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $L > 35$ collapses BTC $n$; Kill if SS/NET grafted; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A $L=20$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes (stage13 REI pattern); Kill if $L$ or Mode retuned only on ETH; Kill if CTI Pearson graft.
- **sol_smoke:** Kill if CTI/CMO/TTF labeled Spearman; 15m $L \le 5$ spam. Retention check: SOL $n$ multi-dozen.
- **bnb_smoke:** CRITICAL after 3-coin clear: different $L$; Mode B shorts ungated; no ATR; BNB-only lengthen. Kill if BNB needs $L \ne \text{SOL}$.

---

## 3. Locked Strategy 2 (`ehlers-uo2025-hpdiff-zero`)

### 3.1 Formulation
- **Ehlers Ultimate Oscillator (2025) (John Ehlers, TASC Apr 2025 / Traders' Tips):**
  - HighPass filter of period $P$:
    $$\alpha_1 = \exp\left(-\frac{1.414\pi}{P}\right), \quad c_2 = 2\alpha_1 \cos\left(\frac{1.414\pi}{P}\right), \quad c_3 = -\alpha_1^2, \quad c_1 = \frac{1 + c_2 - c_3}{4}$$
    $$\text{hp}_t = c_1 (s_t - 2s_{t-1} + s_{t-2}) + c_2 \text{hp}_{t-1} + c_3 \text{hp}_{t-2}$$
  - $\text{sig} = \text{HP}(s, \text{BandEdge} \cdot \text{Bandwidth}) - \text{HP}(s, \text{BandEdge})$
  - $\text{rms} = \sqrt{\frac{1}{100} \sum_{i=0}^{99} \text{sig}_{t-i}^2}$
  - $\text{uo} = \frac{\text{sig}}{\text{rms}}$ if $\text{rms} \ne 0$ else $0$.
  - Prefer **$\text{BandEdge}=20, \text{Bandwidth}=2.0$**.
- **Mode A (BTC->ETH-PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(\text{uo}, 0)$
  - Exit: $\text{crossunder}(\text{uo}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / quality hold):**
  - Long entry: $\text{crossover}(\text{uo}, 0.5)$
  - Exit: $\text{crossunder}(\text{uo}, 0)$ (or ATR stop)
  - Identical parameters across all coins.

### 3.2 Locked Parameter Space
- Sweep: $\text{BandEdge} \in \{14, 20, 28\}$, $\text{Bandwidth} \in \{1.4, 2.0, 2.5\}$
- Primary grid:
  1. `mode_a|(p20,bw2.0)` (preferred)
  2. `mode_a|(p14,bw2.0)`
  3. `mode_a|(p28,bw2.0)`
  4. `mode_b|(p20,bw2.0)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if BandEdge/Bandwidth inflate until $n$ collapses; Kill SS graft after HP; Kill Williams UO substitute. Prefer Mode A (20, 2), 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill params retuned only on ETH; Kill Roofing/SS substitute. Prefer identical (20, 2).
- **sol_smoke:** Kill if Williams UO / Roofing / SS labeled Ehlers-UO2025; 15m BandEdge $\le 5$ spam. Retention check: SOL $n$ multi-dozen.
- **bnb_smoke:** CRITICAL after 3-coin clear: different (BandEdge, Bandwidth) than SOL; Mode B shorts ungated; no ATR. Kill if BNB needs params $\ne \text{SOL}$.

---

## 4. Locked Strategy 3 (`ehlers-corr-cycle-real-zero`)

### 4.1 Formulation
- **Ehlers Correlation Cycle Real (John Ehlers, TASC Jun 2020 / Traders' Tips):**
  - $\text{Real} = \text{corr}(\text{close}[0..P-1], \cos(2\pi i / P))$
  - $\text{Imag} = \text{corr}(\text{close}[0..P-1], -\sin(2\pi i / P))$
  - $\text{Angle} = \text{atan2}(-\text{Imag}, \text{Real})$ in degrees $[0..360]$
  - $\Delta\text{Angle} = \text{Angle}_t - \text{Angle}_{t-1}$ (wrapped to $[-180, 180]$)
  - $\text{state} = +1$ if $|\Delta\text{Angle}| < \text{Threshold}$ and $\text{Real} > 0$ else $(-1$ if $|\Delta\text{Angle}| < \text{Threshold}$ and $\text{Real} < 0$ else $0)$.
  - Prefer **$\text{period}=20, \text{threshold}=9.0$**.
- **Mode A (BTC->ETH-PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(\text{Real}, 0)$
  - Exit: $\text{crossunder}(\text{Real}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / state trend-gate):**
  - Long entry: $\text{crossover}(\text{Real}, 0)$ and $\text{state} \ne 0$
  - Exit: $\text{crossunder}(\text{Real}, 0)$ (or ATR stop)
  - Identical (period, threshold) across all coins.

### 4.2 Locked Parameter Space
- Sweep: $\text{period} \in \{14, 20, 28\}$, $\text{threshold} \in \{6.0, 9.0, 12.0\}$
- Primary grid:
  1. `mode_a|(p20,th9)` (preferred)
  2. `mode_a|(p14,th9)`
  3. `mode_a|(p28,th9)`
  4. `mode_b|(p20,th9)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if period/threshold inflate until Real $n$ collapses; Kill Mode B forced while Mode A BTC healthy; Kill CTI/SS graft. Prefer Mode A period=20, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill period/threshold retuned only on ETH; Kill CTI dual-thr substitute. Prefer identical (20, 9).
- **sol_smoke:** Kill if CTI/CyberCycle/Roofing labeled CCY-Real; 15m period $\le 5$ spam. Retention check: SOL $n$ multi-dozen.
- **bnb_smoke:** CRITICAL after 3-coin clear: different (period, threshold); Mode B shorts ungated; Mode B only on BNB; no ATR. Kill if BNB needs params $\ne \text{SOL}$.

---

## 5. Locked Strategy 4 (`ehlers-net-myrsi-zero`)

### 5.1 Formulation
- **Ehlers Noise Elimination Technology on MyRSI (John Ehlers, Mesa Software):**
  - $\text{CU} = \sum \max(\Delta\text{close}, 0)$ over $\text{rsi\_length}$
  - $\text{CD} = \sum \max(-\Delta\text{close}, 0)$ over $\text{rsi\_length}$
  - $\text{MyRSI} = \frac{\text{CU} - \text{CD}}{\text{CU} + \text{CD}}$ in $[-1, +1]$
  - Kendall concordance of MyRSI vs time-slope over $\text{net\_length}$:
    $$\text{NET} = \frac{\sum_{i < j} \text{sign}(X_j - X_i)}{0.5 \cdot N (N - 1)}$$
  - Prefer **$\text{rsi\_length}=14, \text{net\_length}=14$**.
- **Mode A (BTC->ETH-PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(\text{NET}, 0)$
  - Exit: $\text{crossunder}(\text{NET}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / quality hold):**
  - Long entry: $\text{crossover}(\text{NET}, 0.2)$
  - Exit: $\text{crossunder}(\text{NET}, 0)$ (or ATR stop)
  - Identical lengths across all coins.

### 5.2 Locked Parameter Space
- Sweep: $\text{rsi\_length}, \text{net\_length} \in \{10, 14, 20\}$
- Primary grid:
  1. `mode_a|(rsi14,net14)` (preferred)
  2. `mode_a|(rsi10,net14)`
  3. `mode_a|(rsi20,net14)`
  4. `mode_b|(rsi14,net14)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if lengths raised into stage12-damp until BTC $n$ collapses; Kill Mode A as raw CMO/MyRSI zero (stage2 burn); Kill SS graft. Prefer Mode A (14, 14), 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill lengths retuned only on ETH; Kill Wilder RSI OB/OS. Prefer identical (14, 14).
- **sol_smoke:** Kill if CMO/RSI/ASH labeled NET-MyRSI; 15m length $\le 3$ spam. Retention check: SOL $n$ multi-dozen.
- **bnb_smoke:** CRITICAL after 3-coin clear: different (rsi_length, net_length); Mode B shorts ungated; no ATR; per-coin retune. Kill if BNB needs params $\ne \text{SOL}$.

---

## 6. Locked Strategy 5 (`varadi-dvi-midline-cross`) — Optional 5th

### 6.1 Formulation
- **Varadi DV Intermediate Oscillator (David Varadi / CSS Analytics / TTR DVI):**
  - $r = \frac{\text{close}}{\text{SMA}(\text{close}, 3)} - 1$
  - $\text{mag} = \text{SMA}\left(\frac{\text{SMA}(r, 5) + \text{SMA}(r, 100)/10}{2}, 5\right)$
  - $b = +1$ if $\text{close} > \text{close}[1]$ else $(-1$ if $\text{close} < \text{close}[1]$ else $0)$
  - $\text{str} = \text{SMA}\left(\frac{\text{runSum}(b, 10) + \text{runSum}(b, 100)/10}{2}, 2\right)$
  - $\text{DVI} = \text{mag\_weight} \cdot \text{PercentRank}(\text{mag}, n) + \text{str\_weight} \cdot \text{PercentRank}(\text{str}, n)$
  - Scaled $[0..1]$, midline $0.5$.
  - Prefer **$n=168, \text{mag\_weight}=0.8, \text{str\_weight}=0.2$**.
- **Mode A (BTC->ETH-PRIMARY dense midline — prefer first):**
  - Long entry: $\text{crossover}(\text{DVI}, 0.5)$
  - Exit: $\text{crossunder}(\text{DVI}, 0.5)$ (or ATR stop)
- **Mode B (BNB-quiet / stretch-heavier):**
  - Long entry: $\text{crossover}(\text{DVI}, 0.55)$
  - Exit: $\text{crossunder}(\text{DVI}, 0.5)$ (or ATR stop)
  - Identical parameters across all coins.

### 6.2 Locked Parameter Space
- Sweep: $n \in \{100, 168, 252\}$, weights $(0.8, 0.2)$ (optional $(0.6, 0.4)$)
- Primary grid:
  1. `mode_a|(n168,w0.8)` (preferred)
  2. `mode_a|(n100,w0.8)`
  3. `mode_a|(n252,w0.8)`
  4. `mode_b|(n168,w0.8)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $n$/weights/smoothing inflate until BTC trade count collapses (thin-n risk); Kill SMA200 CSS graft; Kill Mode B forced while Mode A already thin. Prefer Mode A $n=168$, 1H+. Explicit thin-n watch.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill $n$/weights retuned only on ETH; Kill PSY midline-50 substitute. Prefer identical.
- **sol_smoke:** Kill if PSY/RMI/TII/Dorsey labeled DVI; 15m $n \le 20$ spam. Retention check: SOL $n$ multi-dozen.
- **bnb_smoke:** CRITICAL after 3-coin clear: different $n$/weights; Mode B shorts ungated; no ATR; SMA200 graft. Kill if BNB needs params $\ne \text{SOL}$.

---

## 7. Stop-Ladder Execution Protocol

1. **BTC Sweep (40 cells):** 5 strategies $\times$ 4 parameter sets $\times$ 2 timeframes (1H, 4H).
   - Evaluate Mode-A return vs Buy & Hold over last 6 months.
   - Enforce tiny-n policy ($n \le 5 \to \text{FAIL}$; $n \in [6..10] \to \text{THIN-N FLAG}$).
   - Cells with $\text{gate\_6m} == \text{"PASS"}$ ($\text{ratio} \ge 1.2$ and $n > 5$) advance to ETH.
2. **ETH Portability Test (HARD):** Run promoted cells on ETHUSDT with identical parameters.
   - Cells with $\text{gate\_6m} == \text{"PASS"}$ advance to SOL.
3. **SOL Liquidity Test (HARD):** Run promoted cells on SOLUSDT with identical parameters.
   - Cells with $\text{gate\_6m} == \text{"PASS"}$ advance to BNB.
4. **BNB Survival Test (HARD — Stage 14 TTF Choke):** Run promoted cells on BNBUSDT with identical parameters.
   - Stresses quiet BNB behavior after 3-coin clear.
   - Cells with $\text{gate\_6m} == \text{"PASS"}$ achieve full-ladder pass.
