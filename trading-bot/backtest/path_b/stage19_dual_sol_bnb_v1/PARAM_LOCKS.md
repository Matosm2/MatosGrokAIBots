# stage19-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage19-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage18 (0/40 BTC LEAD — stage12/15 rhyme). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_6d02.md` & `stage19-dual-sol-bnb-briefs-2026-09-18_0817.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY without over-damp** (stage12/15/18 rhyme) + **Denser $n \gg 9$** + **ETH portability** + **SOL-after-BTC+ETH** + **BNB-Survival after 3-coin clear** per Path B Stage 19 directives:
- **BTC LEAD PRIMARY CHOKE (Stage 12/15/18 Rhyme):** In Stage 18, all 40 cells on BTC scored 0 PASS, rhyming with Stage 12 and Stage 15 where denser mid-cycle seats never left BTC due to chop under costs and over-damp edge erasure. Stage 19 explicitly locks five responsive structure, impulse channel, volume-zone, smart-money cumulative, and path-fractal families outside stage1–18 + parks to achieve dense BTC participation ($n \gg 9$) that clears the $\ge 1.2\times$ B&H requirement first, then ports cleanly across ETH $\to$ SOL $\to$ BNB without per-coin retuning.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$) and Stage 8 PGO ($n \approx 9$), without stage12/15/18 over-damp collapse (0 BTC).
- **ETH Portability (Bostian III / REI Lesson):** Avoid Stage 17 failure mode where dense BTC clear wiped out on ETH due to venue-specific volume microstructure.
- **SOL-after-BTC+ETH Preservation:** Avoid Stage 16 Kagi failure mode (BTC+ETH cleared then SOL stalled under 1.2x).
- **BNB-Survival (CRITICAL after 3-coin clear):** Withstand quieter BNB regime without quiet wipe (Stage 14 TTF lesson).
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially never ETH-only or BNB-only retuning) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if parameter inflation collapses BTC $n$; Kill if Mode A BTC 0 / chop; Kill if Kagi/3LB/ZigZag/Keltner/BB/PZO/OBV/FRAMA/VHF substitute; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH wipes; Kill if parameters retuned only on ETH; Kill if improper substitutes labeled seated strategies. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH CRITICAL:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if 15m spam; Kill if stage12-18 grafts; Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **CRITICAL after BTC+ETH+SOL (TTF lesson):** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; per-coin retune. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–18 IDs (all), including DPO/PPO/VHF/FOSC/PO, HA/Blau MDI/DSS/Bostian III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, stage12 smoother class, Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, PMO.

---

## 2. Locked Strategy 1 (`hhll-structure-flip`)

### 2.1 Formulation
- **Higher-High / Lower-Low Structure Flip:**
  - $\text{ph} = \text{pivothigh}(\text{high}, \text{lb}, \text{lb})$
  - $\text{pl} = \text{pivotlow}(\text{low}, \text{lb}, \text{lb})$
  - Maintain last two confirmed swing highs ($\text{sh0}, \text{sh1}$) and lows ($\text{sl0}, \text{sl1}$)
  - $\text{bullStruct} = (\text{sh1} > \text{sh0}) \land (\text{sl1} > \text{sl0})$ (requires $\ge 2$ confirmed swings each)
  - Prefer **$\text{lb}=3$**. Closed-bar only after right-confirm ($\text{lb}$ bars) — strictly **NO ZigZag look-ahead**.
  - $\ne$ Kagi / 3LB (stage 16), $\ne$ ZigZag look-ahead, $\ne$ PDH / PWH (stage 1/2).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{bullStruct} \land \neg\text{bullStruct}[1]$ (rising edge of structure polarity)
  - Exit: $\neg\text{bullStruct}$ (loss of bullish structure or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Optional BOS entry ($\text{close} > \text{sh1}$) or larger $\text{lb}$
  - Only if Mode A over-whips; identical params.

### 2.2 Locked Parameter Space
- Sweep: $\text{lb} \in \{2, 3, 5\}$
- Primary grid:
  1. `mode_a|(lb3)` (preferred)
  2. `mode_a|(lb2)`
  3. `mode_a|(lb5)`
  4. `mode_b|(lb3,bos)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{lb} \in \{2, 3, 5\}$; $\text{lb} > 10$ forbidden. Mode B forced while Mode A BTC healthy fails. Prefer Mode A $\text{lb}=3$, 1H+.
- **eth_smoke:** $\text{lb} \in \{2, 3, 5\}$; retuning only on ETH fails. Kagi/3LB/ZigZag substitute fails.
- **sol_smoke:** 15m $\text{lb} \le 1$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 3. Locked Strategy 2 (`starc-bands-break-flip`)

### 3.1 Formulation
- **Stoller Average Range Channel Bands Break-Flip:**
  - $\text{mid} = \text{sma}(\text{close}, \text{smaLen})$ (Center is strictly **SMA**, $\ne$ Keltner EMA)
  - $\text{atr} = \text{atr}(\text{atrLen})$
  - $\text{upper} = \text{mid} + k \cdot \text{atr}$
  - $\text{lower} = \text{mid} - k \cdot \text{atr}$
  - Prefer **$(\text{smaLen}=6, \text{atrLen}=15, k=2.0)$**.
  - $\ne$ Keltner (EMA center), $\ne$ Bollinger Bands (stdev bands), $\ne$ Donchian, $\ne$ AccelBands (stage 9).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{close}, \text{upper})$
  - Exit: $\text{crossunder}(\text{close}, \text{lower})$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Exit on cross under mid SMA ($\text{close} < \text{mid}$) or larger $k$ / longer $\text{smaLen}$
  - Only if Mode A over-whips; identical params.

### 3.2 Locked Parameter Space
- Sweep: $\text{smaLen} \in \{5, 6, 10\}$, $\text{atrLen} \in \{10, 15\}$, $k \in \{1.5, 2.0, 2.5\}$
- Primary grid:
  1. `mode_a|(sma6,atr15,k2.0)` (preferred)
  2. `mode_a|(sma5,atr10,k1.5)`
  3. `mode_a|(sma10,atr15,k2.5)`
  4. `mode_b|(sma6,atr15,k2.0,midexit)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{smaLen} \in \{5, 6, 10\}$, $\text{atrLen} \in \{10, 15\}$, $k \in \{1.5, 2.0, 2.5\}$; $k > 3.5$ forbidden. Prefer Mode A (6, 15, 2.0), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Keltner/BB/Donchian substitute fails.
- **sol_smoke:** 15m $\text{smaLen} \le 3$ or $k \le 1.0$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 4. Locked Strategy 3 (`vzo-zero-cross`)

### 4.1 Formulation
- **Volume Zone Oscillator Zero-Cross (Walid Khalil):**
  - $\text{signedVol} = \text{close} > \text{close}[1] ? \text{volume} : (\text{close} < \text{close}[1] ? -\text{volume} : 0)$
  - $\text{vp} = \text{ema}(\text{signedVol}, \text{len})$
  - $\text{tv} = \text{ema}(\text{volume}, \text{len})$
  - $\text{vzo} = 100 \times \text{vp} / \text{tv}$ ($0$ if $\text{tv} == 0$)
  - Prefer **$\text{len}=14$**.
  - $\ne$ PZO (Khalil price sibling signs price change, stage 13).
  - $\ne$ Bostian III / Intraday Intensity SMA-zero (stage 17).
  - $\ne$ CMF / OBV.
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{vzo}, 0)$
  - Exit: $\text{crossunder}(\text{vzo}, 0)$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Hold requirement: $\text{vzo} > 5$ held for $\ge 1$ bar after crossover
  - Only if Mode A over-whips; identical params.

### 4.2 Locked Parameter Space
- Sweep: $\text{len} \in \{10, 14, 21\}$
- Primary grid:
  1. `mode_a|(len14)` (preferred)
  2. `mode_a|(len10)`
  3. `mode_a|(len21)`
  4. `mode_b|(len14,hold1)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{len} \in \{10, 14, 21\}$; $\text{len} > 40$ forbidden. Prefer Mode A $\text{len}=14$, 1H+.
- **eth_smoke:** $\text{len} \in \{10, 14, 21\}$; retuning only on ETH fails. PZO/III/CMF substitute fails.
- **sol_smoke:** 15m $\text{len} \le 5$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 5. Locked Strategy 4 (`nvi-ema-cross`)

### 5.1 Formulation
- **Negative Volume Index x EMA Signal Cross (Paul Dysart / Norman Fosback):**
  - $\text{var nvi} = 1000.0$
  - $\text{nvi} := \text{volume} < \text{volume}[1] ? \text{nvi} \times (\text{close} / \text{close}[1]) : \text{nvi}$ (multiplicative Fosback)
  - $\text{sig} = \text{ema}(\text{nvi}, \text{sigLen})$
  - Prefer **$\text{sigLen}=50$ on 1H** (not 255-daily over-damp).
  - $\ne$ OBV (accumulates on all volume bars).
  - $\ne$ PVI (positive volume index).
  - $\ne$ CMF / III (stage 17).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{nvi}, \text{sig})$
  - Exit: $\text{crossunder}(\text{nvi}, \text{sig})$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Longer $\text{sigLen}$ or ATR trail stop
  - Only if Mode A over-whips; identical params.

### 5.2 Locked Parameter Space
- Sweep: $\text{sigLen} \in \{21, 50, 100\}$
- Primary grid:
  1. `mode_a|(sig50)` (preferred)
  2. `mode_a|(sig21)`
  3. `mode_a|(sig100)`
  4. `mode_b|(sig50,trail1.5)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{sigLen} \in \{21, 50, 100\}$; $\text{sigLen} > 200$ on 1H forbidden. Prefer Mode A $\text{sigLen}=50$, 1H+.
- **eth_smoke:** $\text{sigLen} \in \{21, 50, 100\}$; retuning only on ETH fails. OBV/PVI/III substitute fails.
- **sol_smoke:** 15m $\text{sigLen} \le 5$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 6. Locked Strategy 5 (`fdi-low-trend-dir`)

### 6.1 Formulation
- **Fractal Dimension Index Low Trend x Close Direction:**
  - Matulich-corrected Carlos Sevcik FDI over window $n$ on close:
    - $\text{Length} = \sum_{k=1}^{n-1} \sqrt{(\text{diff}_k - \text{diff}_{k-1})^2 + (1/n)^2}$
    - $\text{fdi} = 1 + (\ln(\text{Length}) + \ln(2)) / \ln(2n)$
  - $\text{fdi} < \text{thr} \implies$ trending regime ($\text{Hurst} > 0.5$)
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - $\text{longCond} = \text{fdi} < \text{thr} \land \text{bull}$
  - Prefer **$(n=30, \text{thr}=1.50, \text{dirLen}=3)$**.
  - $\ne$ FRAMA (Ehlers adaptive MA).
  - $\ne$ CHOP (Choppiness Index).
  - $\ne$ VHF (stage 18).
  - $\ne$ RWI (stage 7).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{longCond} \land \neg\text{longCond}[1]$ (rising edge into condition)
  - Exit: $\neg\text{longCond}$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Lower threshold ($\text{thr}=1.45$) / longer $n$
  - Only if Mode A over-whips; identical params.

### 6.2 Locked Parameter Space
- Sweep: $n \in \{20, 30\}$, $\text{thr} \in \{1.40, 1.45, 1.50, 1.55\}$, $\text{dirLen} \in \{1, 3, 5\}$
- Primary grid:
  1. `mode_a|(n30,thr1.50,dir3)` (preferred)
  2. `mode_a|(n20,thr1.40,dir1)`
  3. `mode_a|(n30,thr1.55,dir5)`
  4. `mode_b|(n30,thr1.45,dir3)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $n \in \{20, 30\}$, $\text{thr} \in \{1.40, 1.45, 1.50, 1.55\}$, $\text{dirLen} \in \{1, 3, 5\}$; $\text{thr} < 1.20$ forbidden. Prefer Mode A (30, 1.50, 3), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Direction-blind FDI or FRAMA/CHOP/VHF substitute fails.
- **sol_smoke:** 15m $n \le 5$ or $\text{thr} \ge 1.8$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 7. Stop-Ladder Execution Protocol

1. **BTC Lead (40 cells):**
   - 5 strategies $\times$ 2 TFs (1h, 4h) $\times$ 4 parameter sets = 40 cells.
   - Lead Gate: last-6m Mode-A return $\ge 1.2\times$ B&H (same window) AND $n > 5$.
   - Any cell failing Lead Gate or $n \le 5$ is eliminated.
2. **ETH Portability (Active cells from BTC):**
   - Evaluated strictly using identical parameters from BTC.
   - Any cell with 6m return $< 1.2\times$ B&H on ETH is eliminated.
3. **SOL Hard Filter (Active cells from ETH):**
   - Evaluated strictly using identical parameters from BTC/ETH.
   - Must achieve $\ge 1.2\times$ B&H on SOL.
4. **BNB Quiet-Wipe Protection (Active cells from SOL):**
   - Evaluated strictly using identical parameters from BTC/ETH/SOL.
   - Must achieve $\ge 1.2\times$ B&H on BNB.
