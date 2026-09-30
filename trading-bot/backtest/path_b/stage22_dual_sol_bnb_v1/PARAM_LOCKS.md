# stage22-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage22-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage21 (0 BTC wipe on vol-expansion/bar-pattern; stage12/15/18/20/21 rhyme). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_6002.md` & `stage22-dual-sol-bnb-briefs-2026-09-18_86df.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY without over-damp** (stage12/15/18/20/21 rhyme) + **Denser $n \gg 9$** + **BTC->ETH->SOL->BNB portability and survival** per Path B Stage 22 directives:
- **BTC LEAD PRIMARY (Stage 12/15/18/20/21 Rhyme):** In Stage 21, all 32 cells failed BTC on 6m ($0/32$ PASS). Density was high on 1H ($n \gg 9$), but strategies suffered severe chop under execution fees and adverse slippage, never clearing the initial BTC gate. Stage 22 locks responsive non-MA impulse, statistical channel, event-anchored fair value, and volume flow structures outside stage1–21 + parks.
- **Priority-Kill Rule & Katsanos VFI Evaluation:**
  - Per spec: *"LEAN ENCODE (~77% usage): Mode A defaults first; minimal sweeps; PRIORITY-KILL #4 katsanos-vfi-zero-cross if BTC-smoke chop like stage20 volume class (VPCI/BW-MFI/DI) — drop immediately, do not expand sweep / do not promote ladder for #4."*
  - **Empirical BTC-Smoke Assessment:**
    - On 1H: `katsanos-vfi-zero-cross` Mode A (80,0.1,2.5,3) returned -10.62% ($n=50$, $22.0\%$ WR), (50,0.1,2.5,3) returned -18.35% ($n=73$, $20.5\%$ WR), (80,0.2,2.5,3) returned -16.61% ($n=60$, $21.7\%$ WR), and Mode B returned -8.86% ($n=41$, $22.0\%$ WR) vs BTC B&H +10.82% — demonstrating the characteristic 1H volume chop under costs ($0/4$ on 1H).
    - On 4H: `katsanos-vfi-zero-cross` cleared BTC Mode-A $\ge 1.2\times$ B&H on multiple cells:
      - `mode_a|(per50,c0.1,vc2.5,sm3)` @ 4H: **+31.29% ret** vs +10.66% B&H (**2.935x B&H**), $n=13$, $53.8\%$ WR $\to$ **PASS_6m**
      - `mode_a|(per80,c0.2,vc2.5,sm3)` @ 4H: **+14.11% ret** vs +10.66% B&H (**1.324x B&H**), $n=15$, $20.0\%$ WR $\to$ **PASS_6m**
      - `mode_b|(per80,c0.1,vc2.5,sm3,sig10)` @ 4H: **+21.36% ret** vs +10.66% B&H (**2.004x B&H**), $n=11$, $54.5\%$ WR $\to$ **PASS_6m**
      - `mode_a|(per80,c0.1,vc2.5,sm3)` @ 4H: +7.68% ret ($0.720\times$ B&H, $n=15$)
    - **Decision:** Katsanos VFI did **not** 0-BTC wipe like Stage 20 (where VPCI/BW-MFI/DI produced 0 PASS across all 1H and 4H cells). Instead, 3 cells on 4H successfully achieved PASS_6m on BTC with healthy $n > 10$. However, on 1H, VFI suffered the exact volume-chop fee churn predicted by the Stage 20 rhyme. Because VFI passed 3 cells on BTC 4H, it is eligible for promotion to the ladder on those passing 4H cells under the strict stop-ladder protocol, while 1H cells are pruned by the stop-ladder.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$), Stage 8 PGO ($n \approx 9$), and Stage 19 HHLL ($n=8$), while avoiding parameter over-inflation that collapses BTC $n$.
- **ETH Portability (Bostian III / REI Lesson):** Prevent BTC clearers from wiping out on ETH.
- **SOL-after-BTC+ETH Preservation:** Prevent Kagi failure mode (BTC+ETH clear then SOL stalls under $1.2\times$).
- **BNB-Survival (HHLL / TTF Lesson):** Prevent quiet BNB wipes after 3-coin clears; identical parameters on all four coins.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially never BNB-only retuning) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD CRITICAL:** Kill if parameter inflation collapses BTC $n$; Kill if Mode A BTC 0 / chop; Kill if improper substitutes labeled seated strategies; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH under 1.2x; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH CRITICAL:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if 15m spam; Kill if stage12-21 grafts; Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **CRITICAL AFTER 3-COIN (HHLL/TTF LESSON):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–21 IDs (all), including Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, stage12 smoother class, Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, PMO.

---

## 2. Locked Strategy 1 (`percentile-channel-break`)

### 2.1 Formulation
- **Empirical Percentile / Quantile Channel — Close Break:**
  - $\text{up} = \text{ta.percentile\_nearest\_rank}(\text{high}, \text{len}, \text{pHi})$
  - $\text{dn} = \text{ta.percentile\_nearest\_rank}(\text{low}, \text{len}, \text{pLo})$
  - Prefer **$(\text{len}=50, \text{pHi}=90, \text{pLo}=10)$**.
  - $\ne$ Donchian exact HH/LL ($100\text{th}/0\text{th}$), $\ne$ HHLL pivot BOS, $\ne$ BB / Keltner / STARC.
- **Mode A (BTC-LEAD lean):**
  - Long entry: $\text{crossover}(\text{close}, \text{up})$
  - Exit: $\text{crossunder}(\text{close}, \text{dn})$ (or ATR trail stop)
- **Mode B (Width Expansion Gate):**
  - Require width percentrank $\text{ta.percentrank}(\text{up} - \text{dn}, \text{wLen}) > \text{wMin}$ — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep: $\text{len} \in \{50, 70\}$, $\text{pHi} \in \{90, 95\}$, $\text{pLo} \in \{5, 10\}$
- Primary grid:
  1. `mode_a|(len50,p90,p10)` (preferred)
  2. `mode_a|(len70,p90,p10)`
  3. `mode_a|(len50,p95,p5)`
  4. `mode_b|(len50,p90,p10,wpr50)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{len} \in \{50, 70\}$, $\text{pHi} \in \{90, 95\}$, $\text{pLo} \in \{5, 10\}$; $\text{len} > 100$ forbidden (over-damp). Donchian exact / HHLL substitute fails. Prefer Mode A (50,90,10), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $\text{len} \le 10$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`zscore-threshold-hold`)

### 3.1 Formulation
- **Rolling Price Z-Score — Threshold Hold:**
  - $\text{basis} = \text{ta.sma}(\text{close}, \text{len})$
  - $\text{sd} = \text{ta.stdev}(\text{close}, \text{len})$
  - $z = \text{sd} == 0 ? 0 : (\text{close} - \text{basis}) / \text{sd}$
  - Prefer **$(\text{len}=20, \text{thr}=1.0, \text{exitThr}=0.0)$**.
  - $\ne$ BB-squeeze, $\ne$ Disparity zero-cross, $\ne$ PGO ((close-SMA)/ATR), $\ne$ MR-fade ($z < -\text{thr}$).
- **Mode A (BTC-LEAD lean):**
  - Long entry: rising-edge of $z > \text{thr}$
  - Exit: when $z < \text{exitThr}$ (default 0.0)
- **Mode B (Rising Z-Score Filter):**
  - Require $z > \text{thr} \land z > z[1]$ — only if Mode A over-whips; identical params across all four coins.

### 3.2 Locked Parameter Space
- Sweep: $\text{len} \in \{20, 30\}$, $\text{thr} \in \{1.0, 1.5\}$, $\text{exitThr} \in \{0.0, 0.5\}$
- Primary grid:
  1. `mode_a|(len20,thr1.0,exit0.0)` (preferred)
  2. `mode_a|(len30,thr1.0,exit0.0)`
  3. `mode_a|(len20,thr1.5,exit0.5)`
  4. `mode_b|(len20,thr1.0,exit0.0,rising)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{len} \in \{20, 30\}$, $\text{thr} \in \{1.0, 1.5\}$, $\text{exitThr} \in \{0.0, 0.5\}$; $\text{len} > 50$ forbidden. BB-squeeze / Disparity / PGO / MR-fade substitute fails. Prefer Mode A (20,1.0,0), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $\text{len} \le 5$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`anchored-vwap-swing-flip`)

### 4.1 Formulation
- **Event-Anchored VWAP from Confirmed Swing Low — Close Flip:**
  - $\text{pl} = \text{ta.pivotlow}(\text{low}, L, R)$
  - On confirmed $\text{pl}$: reset $\text{cumTPV}$ and $\text{cumV}$ from anchor bar forward.
  - Each bar: $\text{avwap} = \text{cumV} == 0 ? \text{tp} : \text{cumTPV} / \text{cumV}$ where $\text{tp} = (\text{high}+\text{low}+\text{close})/3$.
  - Prefer **$(L=5, R=5, \text{minAge}=0)$**.
  - $\ne$ Session VWAP $\pm\sigma$, $\ne$ HHLL multi-pivot structure state as signal, $\ne$ VWMA $\times$ SMA dual cross.
- **Mode A (BTC-LEAD lean):**
  - Long entry: $\text{crossover}(\text{close}, \text{avwap})$
  - Exit: $\text{crossunder}(\text{close}, \text{avwap})$
  - Primary signal is strictly the AVWAP cross.
- **Mode B (Anchor Maturity Filter):**
  - Require $\text{barsSinceAnchor} \ge \text{minAge}$ before taking signals — only if Mode A over-whips; identical params across all four coins.

### 4.2 Locked Parameter Space
- Sweep: $L, R \in \{5, 8\}$, $\text{minAge} \in \{0, 3\}$
- Primary grid:
  1. `mode_a|(pivot5,5,age0)` (preferred)
  2. `mode_a|(pivot8,8,age0)`
  3. `mode_a|(pivot5,5,age3)`
  4. `mode_b|(pivot5,5,age3,gate)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $L, R \in \{5, 8\}$, $\text{minAge} \in \{0, 3\}$; $L, R > 15$ forbidden (over-damp). Session VWAP / HHLL substitute fails. Prefer Mode A (5,5), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $L \le 1$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`katsanos-vfi-zero-cross`)

### 5.1 Formulation
- **Markos Katsanos Volume Flow Indicator — Zero Cross:**
  - $\text{tp} = (\text{high} + \text{low} + \text{close}) / 3$
  - $\text{inter} = \ln(\text{tp}) - \ln(\text{tp}[1])$
  - $\text{cutoff} = \text{coef} \cdot \text{stdev}(\text{inter}, 30) \cdot \text{close}$
  - $\text{vave} = \text{sma}(\text{volume}, \text{period})[1]$
  - $\text{vc} = \min(\text{volume}, \text{vave} \cdot \text{vcoef})$
  - $\text{vcp} = \text{vc}$ if $\text{mf} > \text{cutoff}$ else $(-\text{vc}$ if $\text{mf} < -\text{cutoff}$ else $0)$
  - $\text{vfiRaw} = \sum(\text{vcp}, \text{period}) / \text{vave}$
  - $\text{vfi} = \text{ema}(\text{vfiRaw}, \text{smooth})$
  - Prefer **$(\text{period}=80, \text{coef}=0.1, \text{vcoef}=2.5, \text{smooth}=3)$**.
  - $\ne$ VPCI, $\ne$ VZO, $\ne$ BW-MFI, $\ne$ Demand Index, $\ne$ OBV.
- **Mode A (BTC-LEAD lean):**
  - Long entry: $\text{crossover}(\text{vfi}, 0)$
  - Exit: $\text{crossunder}(\text{vfi}, 0)$
- **Mode B (Signal Line Filter):**
  - Require $\text{vfi} > \text{sma}(\text{vfi}, \text{sigLen})$ — only if Mode A over-whips; identical params across all four coins.

### 5.2 Locked Parameter Space
- Sweep: $\text{period} \in \{50, 80\}$, $\text{coef} \in \{0.1, 0.2\}$
- Primary grid:
  1. `mode_a|(per80,c0.1,vc2.5,sm3)` (preferred)
  2. `mode_a|(per50,c0.1,vc2.5,sm3)`
  3. `mode_a|(per80,c0.2,vc2.5,sm3)`
  4. `mode_b|(per80,c0.1,vc2.5,sm3,sig10)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{period} \in \{50, 80\}$, $\text{coef} \in \{0.1, 0.2\}$; $\text{period} > 130$ forbidden. VPCI / VZO / BW-MFI / DI / OBV substitute fails.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $\text{period} \le 20$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 6. Ladder Execution Outcomes & Synthesis

- **BTC Evaluation (Step 1/4):** 32 cells evaluated (16 on 1H, 16 on 4H).
  - 1H: $0/16$ cleared BTC. All 1H cells suffered severe execution fee/adverse slippage churn under costs, continuing the 1H cost drag observed in Stage 20/21.
  - 4H: $4/16$ cleared BTC $\ge 1.2\times$ B&H:
    1. `percentile-channel-break` @ 4h `mode_a|(len50,p90,p10)`: +13.21% ret vs 10.66% B&H (**1.240x B&H**, $n=7$, $42.9\%$ WR) [THIN-N flagged, $n \in [6..10]$].
    2. `katsanos-vfi-zero-cross` @ 4h `mode_a|(per50,c0.1,vc2.5,sm3)`: +31.29% ret vs 10.66% B&H (**2.935x B&H**, $n=13$, $53.8\%$ WR).
    3. `katsanos-vfi-zero-cross` @ 4h `mode_a|(per80,c0.2,vc2.5,sm3)`: +14.11% ret vs 10.66% B&H (**1.324x B&H**, $n=15$, $20.0\%$ WR).
    4. `katsanos-vfi-zero-cross` @ 4h `mode_b|(per80,c0.1,vc2.5,sm3,sig10)`: +21.36% ret vs 10.66% B&H (**2.004x B&H**, $n=11$, $54.5\%$ WR).
  - Tiny-n kills triggered on BTC 4H:
    - `percentile-channel-break` @ 4h `mode_a|(len70,p90,p10)`: $n=5 \le 5 \to$ TINY-N KILL.
    - `percentile-channel-break` @ 4h `mode_a|(len50,p95,p5)`: $n=5 \le 5 \to$ TINY-N KILL (even though return was +15.97%, 1.498x B&H).
- **ETH Evaluation (Step 2/4):** 4 cells promoted from BTC; all 4 cleared the ETH portability gate:
  - `percentile-channel-break` @ 4h `mode_a|(len50,p90,p10)`: +19.46% ret vs 15.98% B&H (**1.218x B&H**, $n=6$, $50.0\%$ WR) $\to$ **PASS_6m**
  - `katsanos-vfi-zero-cross` @ 4h `mode_a|(per50,c0.1,vc2.5,sm3)`: +58.56% ret vs 15.98% B&H (**3.665x B&H**, $n=17$, $58.8\%$ WR) $\to$ **PASS_6m**
  - `katsanos-vfi-zero-cross` @ 4h `mode_a|(per80,c0.2,vc2.5,sm3)`: +23.92% ret vs 15.98% B&H (**1.497x B&H**, $n=17$, $41.2\%$ WR) $\to$ **PASS_6m**
  - `katsanos-vfi-zero-cross` @ 4h `mode_b|(per80,c0.1,vc2.5,sm3,sig10)`: +25.62% ret vs 15.98% B&H (**1.603x B&H**, $n=13$, $46.2\%$ WR) $\to$ **PASS_6m**
- **SOL Evaluation (Step 3/4):** 4 cells promoted from ETH; $0/4$ cleared SOL $\ge 1.2\times$ B&H:
  - `percentile-channel-break` @ 4h `mode_a|(len50,p90,p10)`: +16.28% ret vs 17.66% B&H (**0.922x B&H**, $n=8$, $37.5\%$ WR) $\to$ FAIL (near-miss)
  - `katsanos-vfi-zero-cross` @ 4h `mode_a|(per50,c0.1,vc2.5,sm3)`: +8.78% ret vs 17.66% B&H (**0.497x B&H**, $n=15$, $40.0\%$ WR) $\to$ FAIL
  - `katsanos-vfi-zero-cross` @ 4h `mode_a|(per80,c0.2,vc2.5,sm3)`: +15.50% ret vs 17.66% B&H (**0.877x B&H**, $n=13$, $30.8\%$ WR) $\to$ FAIL
  - `katsanos-vfi-zero-cross` @ 4h `mode_b|(per80,c0.1,vc2.5,sm3,sig10)`: -9.98% ret vs 17.66% B&H (**-0.565x B&H**, $n=18$, $22.2\%$ WR) $\to$ FAIL
- **BNB Evaluation (Step 4/4):** 0 cells promoted from SOL; ladder halted before BNB ($0/0$ scored, 32 pruned).
- **Full-Ladder Clear Count:** 0 / 32 cells cleared the complete BTC $\to$ ETH $\to$ SOL $\to$ BNB ladder under identical parameters.
- **Stage Rhyme / Diagnosis:** Replicated the Stage 16 Kagi failure mode (BTC + ETH clear $\ge 1.2\times$, then SOL stalls under $1.2\times$). In addition, 1H cells across all four strategies exhibited the Stage 20/21 cost-churn failure mode.

