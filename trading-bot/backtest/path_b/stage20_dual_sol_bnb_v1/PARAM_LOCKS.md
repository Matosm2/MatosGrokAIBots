# stage20-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage20-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage19 (HHLL 3-coin -> BNB -0.726x quiet wipe; TTF rhyme). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_7b4f.md` & `stage20-dual-sol-bnb-briefs-2026-09-18_5852.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BNB-survival CRITICAL after 3-coin clear** (stage14 TTF + stage19 HHLL rhyme) + **Denser $n \gg 9$** + **BTC->ETH->SOL portability** per Path B Stage 20 directives:
- **BNB-SURVIVAL PRIMARY CHOKE (Stage 14 TTF & Stage 19 HHLL Rhyme):** In Stage 14, Pee TTF cleared 3 coins then suffered a quiet wipe on BNB. In Stage 19, HHLL cleared BTC 2.336× -> ETH 1.646× -> SOL 1.214× then suffered a quiet wipe on BNB (-0.726×). Stage 20 explicitly locks five volume-price pressure, confirmation, facilitation, adaptive estimate, and trend-intensity threshold families outside stage1–19 + parks that can survive quieter BNB without quiet wipe, while keeping denser $n \gg 9$ and BTC->ETH->SOL clearability.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$), Stage 8 PGO ($n \approx 9$), and Stage 19 HHLL ($n=8$), without stage12/15/18 over-damp collapse (0 BTC).
- **ETH Portability (Bostian III / REI Lesson):** Avoid Stage 17 failure mode where dense BTC clear wiped out on ETH due to venue-specific volume microstructure.
- **SOL-after-BTC+ETH Preservation:** Avoid Stage 16 Kagi failure mode (BTC+ETH cleared then SOL stalled under 1.2x).
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially never BNB-only retuning) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD) $\to$ BNB (HARD — TTF/HHLL choke).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC CLEARABILITY:** Kill if parameter inflation collapses BTC $n$; Kill if Mode A BTC 0 / chop; Kill if improper substitutes labeled seated strategies; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH under 1.2x; Kill if parameters retuned only on ETH; Kill if improper substitutes labeled seated strategies. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH CRITICAL:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if 15m spam; Kill if stage12-19 grafts; Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **CRITICAL AFTER 3-COIN (HHLL/TTF LESSON):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–19 IDs (all), including HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, stage12 smoother class, Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, PMO.

---

## 2. Locked Strategy 1 (`vpci-zero-cross`)

### 2.1 Formulation
- **Volume Price Confirmation Indicator (Buff Dormeier TASC / Dow Award):**
  - $\text{vpc} = \text{vwma}(\text{close}, \text{longLen}) - \text{sma}(\text{close}, \text{longLen})$
  - $\text{vpr} = \text{vwma}(\text{close}, \text{shortLen}) / \text{sma}(\text{close}, \text{shortLen})$
  - $\text{vm} = \text{sma}(\text{volume}, \text{shortLen}) / \text{sma}(\text{volume}, \text{longLen})$
  - $\text{vpci} = \text{vpc} \times \text{vpr} \times \text{vm}$
  - Prefer **$(\text{shortLen}=5, \text{longLen}=20)$**.
  - $\ne$ VZO (stage 19 EXIT signed-volume EMA ratio), $\ne$ Bostian III (stage 17 EXIT), $\ne$ CMF / OBV, $\ne$ NVI (stage 19 EXIT), $\ne$ VWMA $\times$ SMA dual-cross primary.
- **Mode A (Prefer (5, 20)):**
  - Long entry: $\text{crossover}(\text{vpci}, 0)$
  - Exit: $\text{crossunder}(\text{vpci}, 0)$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Optional $\text{sig} = \text{sma}(\text{vpci}, \text{sigLen})$ and require VPCI $\times$ sig cross instead of $\times 0$ — only if Mode A over-whips; identical params on all four.

### 2.2 Locked Parameter Space
- Sweep: $\text{shortLen} \in \{5, 8\}$, $\text{longLen} \in \{20, 25\}$, $\text{sigLen} \in \{0, 10\}$
- Primary grid:
  1. `mode_a|(s5,l20)` (preferred)
  2. `mode_a|(s8,l20)`
  3. `mode_a|(s5,l25)`
  4. `mode_b|(s5,l20,sig10)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{shortLen} \in \{5, 8\}$, $\text{longLen} \in \{20, 25\}$; $\text{longLen} > 40$ forbidden. Mode B forced while Mode A BTC healthy fails. Prefer Mode A (5, 20), 1H+.
- **eth_smoke:** $\text{shortLen} \in \{5, 8\}$, $\text{longLen} \in \{20, 25\}$; retuning only on ETH fails. VZO/III/CMF substitute fails.
- **sol_smoke:** 15m $\text{shortLen} \le 2$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** **CRITICAL:** Identical params across all coins. Retuning short/long only on BNB fails. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`bw-mfi-green-fade-flip`)

### 3.1 Formulation
- **Bill Williams Market Facilitation Index Green/Fade Polarity Flip:**
  - $\text{mfi} = \text{volume} == 0 ? 0 : (\text{high} - \text{low}) / \text{volume}$
  - $\text{green} = \text{mfi} > \text{mfi}[1] \land \text{volume} > \text{volume}[1]$ (both up)
  - $\text{fade} = \text{mfi} < \text{mfi}[1] \land \text{volume} < \text{volume}[1]$ (both down)
  - $\text{bull} = \text{close} > \text{close}[1]$
  - Prefer **$\text{confirmBars}=1$**.
  - $\ne$ Awesome Oscillator (AO) / Accelerator / Alligator, $\ne$ Money Flow Index (typical-price volume RSI), $\ne$ VZO.
- **Mode A (BNB-survival lean):**
  - Long entry: rising edge of $(\text{green} \land \text{bull})$ (i.e. $\text{green} \land \text{bull} \land \neg(\text{green}[1] \land \text{bull}[1])$)
  - Exit: on $\text{fade}$ (or $\neg\text{green}$) (or ATR trail stop)
- **Mode B (Consecutive Green):**
  - Require $\text{confirmBars} \in \{2, 3\}$ consecutive Green before entry — only if Mode A over-whips; identical params on all four.

### 3.2 Locked Parameter Space
- Sweep: $\text{confirmBars} \in \{1, 2, 3\}$
- Primary grid:
  1. `mode_a|(conf1)` (preferred)
  2. `mode_a|(conf2)`
  3. `mode_a|(conf3)`
  4. `mode_b|(conf1,notgreen)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{confirmBars} \in \{1, 2, 3\}$; $\text{confirmBars} > 5$ forbidden. Prefer Mode A confirmBars=1, 1H+.
- **eth_smoke:** Retuning only on ETH fails. AO/MoneyFlow/HHLL substitute fails.
- **sol_smoke:** 15m $\text{confirmBars} \le 1$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** **CRITICAL:** Identical params across all coins. Mode B only on BNB fails. If Green still overtrades quiet BNB $\to$ confirmBars=2 everywhere, else kill.

---

## 4. Locked Strategy 3 (`demand-index-zero`)

### 4.1 Formulation
- **James Sibbet Demand Index Zero-Cross (Sierra Chart Locked Form):**
  - $P = \text{high} + \text{low} + 2 \cdot \text{close}$
  - $\text{rng2} = \text{highest}(\text{high}, 2) - \text{lowest}(\text{low}, 2)$
  - $\text{avgRng} = \text{ema}(\text{rng2}, nBS)$
  - $\text{avgV} = \text{ema}(\text{volume}, nBS)$
  - $VR = \text{avgV} == 0 ? 0 : \text{volume} / \text{avgV}$
  - Rising/falling on $P$ vs $P[1]$ assign BP/SP with $\exp(0.375 \cdot \dots)$ factor per Sierra Chart
  - $\text{bpS} = \text{ema}(BP, nSmooth)$, $\text{spS} = \text{ema}(SP, nSmooth)$
  - $DI = 100 \cdot (1 - \text{spS} / \text{bpS})$ if $\text{bpS} \ge \text{spS}$ else $100 \cdot (\text{bpS} / \text{spS} - 1)$
  - Prefer **$(nBS=10, nSmooth=10)$**.
  - $\ne$ VZO (stage 19 EXIT), $\ne$ Bostian III (stage 17 EXIT), $\ne$ CMF / OBV / PZO.
- **Mode A (Prefer (10, 10)):**
  - Long entry: $\text{crossover}(DI, 0)$
  - Exit: $\text{crossunder}(DI, 0)$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Require DI hold above +band / below -band for N bars after cross — only if Mode A over-whips; identical params.

### 4.2 Locked Parameter Space
- Sweep: $nBS \in \{8, 10, 14\}$, $nSmooth \in \{5, 10, 14\}$
- Primary grid:
  1. `mode_a|(bs10,sm10)` (preferred)
  2. `mode_a|(bs8,sm5)`
  3. `mode_a|(bs14,sm14)`
  4. `mode_b|(bs10,sm10,hold1)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $nBS \in \{8, 10, 14\}$, $nSmooth \in \{5, 10, 14\}$; $nSmooth > 25$ forbidden. Prefer Mode A (10, 10), 1H+.
- **eth_smoke:** Retuning only on ETH fails. VZO/III/CMF substitute fails.
- **sol_smoke:** 15m $nBS \le 3$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** **CRITICAL:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`kalman-estimate-cross`)

### 5.1 Formulation
- **Simple 1D Kalman Filter Price $\times$ Estimate Cross:**
  - $\text{prediction} = \text{estimate}$
  - $\text{gain} = \text{error\_est} / (\text{error\_est} + \text{error\_meas})$
  - $\text{estimate} = \text{prediction} + \text{gain} \cdot (\text{close} - \text{prediction})$
  - $\text{error\_est} = (1 - \text{gain}) \cdot \text{error\_est} + Q / \text{length}$
  - $\text{error\_meas} = R \cdot \text{length}$
  - Prefer **$(\text{length}=20, R=0.01, Q=0.1)$**.
  - $\ne$ Nadaraya-RQ (stage 14 EXIT), $\ne$ Ehlers PMA (stage 17 EXIT), $\ne$ SuperSmoother / dual-MA.
- **Mode A (Prefer (20, 0.01, 0.1)):**
  - Long entry: $\text{crossover}(\text{close}, \text{estimate})$
  - Exit: $\text{crossunder}(\text{close}, \text{estimate})$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Require estimate slope $\text{estimate} > \text{estimate}[\text{slopeLen}]$ for long hold — only if Mode A over-whips; identical params.

### 5.2 Locked Parameter Space
- Sweep: $\text{length} \in \{14, 20, 30\}$, $R \in \{0.01, 0.02\}$, $Q \in \{0.05, 0.1\}$
- Primary grid:
  1. `mode_a|(len20,r0.01,q0.1)` (preferred)
  2. `mode_a|(len14,r0.01,q0.05)`
  3. `mode_a|(len30,r0.02,q0.1)`
  4. `mode_b|(len20,r0.01,q0.1,slope3)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{length} \in \{14, 20, 30\}$, $R \in \{0.01, 0.02\}$, $Q \in \{0.05, 0.1\}$; $\text{length} > 50$ forbidden. Prefer Mode A (20, 0.01, 0.1), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Nadaraya/PMA/SS substitute fails.
- **sol_smoke:** 15m $\text{length} \le 5$ or $Q \ge 1.0$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** **CRITICAL:** Identical params across all coins. Mode B slope only on BNB fails.

---

## 6. Locked Strategy 5 (`ravi-threshold-dir`)

### 6.1 Formulation
- **Chande Range Action Verification Index (RAVI) Threshold $\times$ Close Direction:**
  - $s = \text{sma}(\text{close}, \text{shortLen})$
  - $l = \text{sma}(\text{close}, \text{longLen})$
  - $\text{ravi} = |100 \cdot (s - l) / l|$
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - $\text{longCond} = \text{ravi} > \text{thr} \land \text{bull}$
  - Prefer **$(7, 65, 3.0, 3)$**; if $n$ thin on 1H prefer $\text{longLen}=40$ identical.
  - $\ne$ SMA dual-cross primary, $\ne$ ADX burn, $\ne$ VHF (stage 18 EXIT), $\ne$ FDI (stage 19 EXIT).
- **Mode A:**
  - Long entry: rising edge of $\text{longCond}$ ($\text{longCond} \land \neg\text{longCond}[1]$)
  - Exit: on $\neg\text{longCond}$ (or ATR trail stop)
- **Mode B (BNB quiet / chatter):**
  - Slightly higher thr / longer dirLen — only if Mode A over-whips; identical params.

### 6.2 Locked Parameter Space
- Sweep: $\text{shortLen} \in \{5, 7\}$, $\text{longLen} \in \{40, 65\}$, $\text{thr} \in \{2.0, 3.0, 4.0\}$, $\text{dirLen} \in \{1, 3, 5\}$
- Primary grid:
  1. `mode_a|(s7,l65,thr3.0,dir3)` (preferred)
  2. `mode_a|(s7,l40,thr3.0,dir3)` (density prefer if 65 thin)
  3. `mode_a|(s5,l40,thr2.0,dir1)`
  4. `mode_b|(s7,l65,thr4.0,dir5)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{shortLen} \in \{5, 7\}$, $\text{longLen} \in \{40, 65\}$, $\text{thr} \in \{2.0, 3.0, 4.0\}$, $\text{dirLen} \in \{1, 3, 5\}$. $\text{longLen} > 100$ or $\text{thr} > 6.0$ forbidden. Prefer Mode A (7, 65, 3.0, 3) or (7, 40, 3.0, 3), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Direction-blind RAVI or VHF/FDI/III substitute fails.
- **sol_smoke:** 15m $\text{shortLen} \le 3$ or $\text{thr} \le 1.0$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** **CRITICAL:** Identical params across all coins. Mode B higher thr only on BNB fails.

---

## 7. Execution Matrix Summary

| Strategy ID | Class / Foundation | Mode A Trigger | Mode B Variant | Primary Sweep Grid |
| :--- | :--- | :--- | :--- | :--- |
| `vpci-zero-cross` | Dormeier VPCI | VPCI $\times 0$ cross up | VPCI $\times$ SMA(10) signal cross | short $\in \{5, 8\}$, long $\in \{20, 25\}$ |
| `bw-mfi-green-fade-flip` | Bill Williams MFI | Green $\land$ Bull edge | not-green exit / conf=2,3 | confirmBars $\in \{1, 2, 3\}$ |
| `demand-index-zero` | Sibbet / Sierra DI | DI $\times 0$ cross up | DI $> +5$ hold 1 bar | nBS $\in \{8, 10, 14\}$, nSmooth $\in \{5, 10, 14\}$ |
| `kalman-estimate-cross` | 1D Kalman filter | Close $\times$ Est cross up | Est slope gate (slopeLen=3) | length $\in \{14, 20, 30\}$, R $\in \{0.01, 0.02\}$, Q $\in \{0.05, 0.1\}$ |
| `ravi-threshold-dir` | Chande RAVI | RAVI $> \text{thr} \land \text{bull}$ edge | Higher thr / longer dirLen | short $\in \{5, 7\}$, long $\in \{40, 65\}$, thr $\in \{2.0, 3.0, 4.0\}$, dir $\in \{1, 3, 5\}$ |

Total Evaluation Space: 5 strategies $\times$ 2 timeframes (1H, 4H) $\times$ 4 parameter combinations = 40 cells per coin on the stop-ladder (BTC $\to$ ETH $\to$ SOL $\to$ BNB).
