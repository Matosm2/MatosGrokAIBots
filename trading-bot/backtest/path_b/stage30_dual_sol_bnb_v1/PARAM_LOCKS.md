# stage30-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-21  
**Research ID:** `stage30-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage29 wipe (closest DVS@4h Mode B 1.093×; still short of 1.20; BTC 0/32 FAIL LEAD). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_c1fe.md` & `stage30-dual-sol-bnb-briefs-2026-09-21_0449.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY CRITICAL** (clear past DVS 1.093× / FVE 1.055× / Vervoort 0.832× to ≥ 1.20 without over-damp) + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **ETH denser n ≫ 9 portability** + **SOL-after-BTC+ETH** + **BNB-survival after 3-coin** per Path B Stage 30 directives:
- **BTC LEAD PRIMARY CRITICAL:** In Stage 29, `varadi-dvs-stretch-midline` reached 1.093× @ 4h Mode B (n=34), but was still short of 1.20, while Stiffness (~0.883×), CPR (0.750×), and HVR (BTC FAIL) failed, leaving BTC 0/32 FAIL LEAD across the pack. In Stage 30, we lock four distinct, non-clone published families outside stage 1–29 + remaining parks:
  1. `blau-dti-zero-cross` (Composite H/L momentum normalized triple-EMA × 0)
  2. `arms-vama-dual-cross` (Volume-increment MA fast×slow cross, causal rolling AvgVol)
  3. `apirine-ma-bands-break` (Vitali Apirine Moving Average Bands break-accept)
  4. `ehlers-recursive-median-osc-zero` (Ehlers Recursive Median Oscillator × 0)
- **Track B Hard Ban Honored:** Do NOT encode or clone Chande-Kroll, QQE, MAMA×FAMA, or Wilder Volatility System (ARC-SAR), which are owned by parallel Track B optimize (`stage23-chande-kroll-optimize-v1`).
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser n ≫ 9 Policy:** Ensure trade density remains well above the thin counts of Stage 25 NHNL (n=8), Stage 14 TTF (n=6..10), Stage 8 PGO (n ≈ 9), and thin n ≤ 5 structure stalls, while avoiding parameter over-inflation that collapses BTC n.
- **Tiny-n Policy (Critical):** If Mode-A BTC n ≤ 5 on 6m -> FAIL that cell even if ×B&H ≥ 1.2 (hard-fail cell as over-gated / under-specified). Also flag n ≈ 9 (in range [6..10]) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return ≥ 1.2× B&H -> ETH (HARD, `eth_smoke`) -> SOL (HARD, `sol_smoke`) -> BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (clear past 1.093× / ≥ 1.20 / no 0-BTC / no VR 0.698× regress):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past 1.20 (DVS/FVE/Vervoort rhyme); Kill if parameters inflated until BTC n collapses; Kill if ADX/TSI/CSI/MDI labeled DTI; Kill if VWMA/Vervoort/EC labeled VAMA; Kill if BB/Keltner/Kirshenbaum/CPR/Envelopes labeled MAB; Kill if BandPass/naked-HP/DSP/CorrCycle labeled RMO; Kill if Track-B grafts. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **ETH-after-BTC (no NHNL 1.687× -> 1.085× wipe / no thin n ≈ 8):** Kill if BTC clears ≥ 1.2× then ETH under 1.2×; Kill if ETH n stays thin ~8; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH n multi-dozen (n ≫ 9).
  - `sol_smoke`: **SOL-AFTER-BTC+ETH (no Kagi / percentile 0.922× fail):** Kill if BTC+ETH clear ≥ 1.2× then SOL under 1.2×; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–29 grafts. Retention check: after ETH, SOL n must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL (no TTF / HHLL quiet wipe):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–29 IDs (all), including Stiffness/CPR/DVS/HVR, EC/Vervoort/ZL-FIR/DV2, Qstick/Klinger/%Envelopes/Schwager-VR, FVE/Convolution/HT_TRENDLINE/SafeZone, DSP/NHNL/VROC/Elder-thermo, Guppy-CBL/Kirshenbaum/IMI/Williams-AD, QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV, ZLEMA, EDCF filt*lag.

---

## 2. Locked Strategy 1 (`blau-dti-zero-cross`)

### 2.1 Formulation
- **Blau Directional Trend Index (DTI):**
  - William Blau (*Momentum, Direction, and Divergence*, 1995; MQL5 Blau_DTI / Blau_HLM):
  - `HMU = max(High − High[q−1], 0)`
  - `LMD = max(Low[q−1] − Low, 0)`
  - `HLM = HMU − LMD`
  - `num = EMA(EMA(EMA(HLM, r), s), u)`
  - `den = EMA(EMA(EMA(|HLM|, r), s), u)`
  - `DTI = 100 · num / den` (if den $\ne$ 0 else 0)
  - Prefer **(q=2, r=20, s=5, u=3)**.
  - $\ne$ ADX/DMI (Wilder +DI/-DI/DX), $\ne$ TSI (close momentum normalize), $\ne$ Blau CSI / Ergodic MDI, $\ne$ RAVI.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(dti, 0)`
  - Exit: `crossunder(dti, 0)`
- **Mode B (Rising Confirmation Filter):**
  - Require rising DTI `dti > dti[1]` on entry — only if Mode A over-whips; identical across all four coins — still not $\pm 25$ fade-MR primary.

### 2.2 Locked Parameter Space
- Sweep (LEAN): $q \in \{1, 2, 3\}$; $r \in \{10, 20, 32\}$; $s \in \{3, 5\}$; $u \in \{1, 3\}$; TF 1H vs 4H. Mode A defaults first.
- Primary grid:
  1. `mode_a|(q2,r20,s5,u3)` (preferred default)
  2. `mode_a|(q1,r10,s3,u1)`
  3. `mode_a|(q3,r32,s5,u3)`
  4. `mode_b|(q2,r20,s5,u3,rising)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $q \in \{1, 2, 3\}$, $r \in \{10, 20, 32\}$, $s \in \{3, 5\}$, $u \in \{1, 3\}$ locked. ADX/TSI/CSI/MDI substitute forbidden. Prefer Mode A (2, 20, 5, 3), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`arms-vama-dual-cross`)

### 3.1 Formulation
- **Arms Volume Adjusted Moving Average (VAMA):**
  - Richard W. Arms, Jr. (Equivolume / NeuroShell / Fidelity Technical Indicator Guide):
  - `AvgVol = SMA(volume, SampleN)` (causal rolling window — not full-chart non-causal average)
  - `VolInc = AvgVol * factor` (default factor = 0.67)
  - At each bar $i$, walk backward $j = i, i-1, \dots$ accumulating volume units `volume[j] / VolInc[i]` and price until target Length (fastLen or slowLen) is reached:
    `VAMA = CumSum(Price * Units) / Length`.
  - Prefer **(fastLen=8, slowLen=55, SampleN=100, factor=0.67)**.
  - $\ne$ VWMA ($\sum(P\cdot V)/\sum V$), $\ne$ Vervoort ZL-TEMA, $\ne$ EC. **Forbidden:** `ta.vwma` labeled VAMA.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(vamaFast, vamaSlow)`
  - Exit: `crossunder(vamaFast, vamaSlow)`
- **Mode B (Trend Gate Filter):**
  - Require `close > vamaSlow` on entry — only if Mode A over-whips; identical across all four coins.

### 3.2 Locked Parameter Space
- Sweep (LEAN): $fast \in \{5, 8, 13\}$; $slow \in \{34, 55, 89\}$; $SampleN \in \{50, 100, 200\}$; TF 1H vs 4H. Mode A defaults first.
- Primary grid:
  1. `mode_a|(f8,s55,sn100)` (preferred default)
  2. `mode_a|(f5,s34,sn50)`
  3. `mode_a|(f13,s89,sn200)`
  4. `mode_b|(f8,s55,sn100,trend_close)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $fast \in \{5, 8, 13\}$, $slow \in \{34, 55, 89\}$, $SampleN \in \{50, 100, 200\}$ locked. VWMA / Vervoort / EC substitute forbidden. Non-causal full-chart AvgVol forbidden. Prefer Mode A (8, 55, 100), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`apirine-ma-bands-break`)

### 4.1 Formulation
- **Vitali Apirine Moving Average Bands (MAB):**
  - Vitali Apirine (*Moving Average Bands*, TASC Aug 2021; Financial Hacker):
  - `MA1 = EMA(Close, P1)`
  - `MA2 = EMA(Close, P2)`
  - `Dst = MA1 − MA2`
  - `Dv = SMA(Dst², P2)`
  - `Dev = Mltp · √Dv`
  - `Upper = MA1 + Dev`
  - `Lower = MA1 − Dev`
  - Prefer **(P1=50, P2=10, Mltp=1.0)**.
  - $\ne$ Bollinger Bands (stdev of price), $\ne$ Keltner (ATR), $\ne$ Kirshenbaum (LinReg stderr), $\ne$ %Envelopes, $\ne$ CPR, $\ne$ STARC.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(ma2, upper)`
  - Exit: `crossunder(ma2, lower)`
- **Mode B (Narrow Width Compression Gate):**
  - Require prior narrow width `100 * (upper - lower) / ma1 < widthThr` (e.g. 1.5%) before Upper break — only if Mode A over-whips; identical across all four.

### 4.2 Locked Parameter Space
- Sweep (LEAN): $P1 \in \{34, 50, 100, 200\}$; $P2 \in \{8, 10, 20, 50\}$; $Mltp \in \{0.75, 1.0, 1.5\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(p1_50,p2_10,mltp1.0)` (preferred default)
  2. `mode_a|(p1_34,p2_8,mltp0.75)`
  3. `mode_a|(p1_100,p2_20,mltp1.5)`
  4. `mode_b|(p1_50,p2_10,mltp1.0,narrow1.5)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $P1 \in \{34, 50, 100, 200\}$, $P2 \in \{8, 10, 20, 50\}$, $Mltp \in \{0.75, 1.0, 1.5\}$ locked. BB/Keltner/Kirshenbaum/CPR/Envelopes substitute forbidden. Track-B CK graft forbidden. Prefer Mode A (50, 10, 1.0), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`ehlers-recursive-median-osc-zero`)

### 5.1 Formulation
- **Ehlers Recursive Median Oscillator (RMO):**
  - John Ehlers (*Recursive Median Filters*, TASC Mar 2018; ProRealCode / MQL5 mladen):
  - `med = Median(Close, medLen=5)`
  - $\alpha_1 = (\cos(2\pi/LP) + \sin(2\pi/LP) - 1.0) / \cos(2\pi/LP)$
  - $RM = \alpha_1 \cdot med + (1 - \alpha_1) \cdot RM[1]$
  - $\alpha_2 = (\cos(0.707 \cdot 2\pi/HP) + \sin(0.707 \cdot 2\pi/HP) - 1.0) / \cos(0.707 \cdot 2\pi/HP)$
  - $RMO = (1 - \alpha_2/2)^2 \cdot (RM - 2\cdot RM[1] + RM[2]) + 2(1 - \alpha_2)\cdot RMO[1] - (1 - \alpha_2)^2 \cdot RMO[2]$
  - Prefer **(LP=12, HP=30, medLen=5)**.
  - $\ne$ BandPass, $\ne$ naked-HP-of-price, $\ne$ DSP, $\ne$ CorrCycle, $\ne$ RSI.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(rmo, 0)`
  - Exit: `crossunder(rmo, 0)`
- **Mode B (Rising Confirmation Filter):**
  - Require rising RMO `rmo > rmo[1]` on entry — only if Mode A over-whips; identical across all four.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $LP \in \{8, 12, 16\}$; $HP \in \{20, 30, 40\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(lp12,hp30,med5)` (preferred default)
  2. `mode_a|(lp8,hp20,med5)`
  3. `mode_a|(lp16,hp40,med5)`
  4. `mode_b|(lp12,hp30,med5,rising)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $LP \in \{8, 12, 16\}$, $HP \in \{20, 30, 40\}$ locked. BandPass / naked-HP-of-price / DSP / CorrCycle substitute forbidden. Track-B graft forbidden. Prefer Mode A (12, 30), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 6. Execution Grid & Summary Matrix

| Strategy ID | Family | Primary Parameters | Timeframes | Primary Gate Metric |
| :--- | :--- | :--- | :--- | :--- |
| `blau-dti-zero-cross` | Blau composite H/L momentum DTI×0 | q=2, r=20, s=5, u=3 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |
| `arms-vama-dual-cross` | Arms volume-increment VAMA dual | fast=8, slow=55, SampleN=100 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |
| `apirine-ma-bands-break` | Vitali Apirine Moving Average Bands break | P1=50, P2=10, Mltp=1.0 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |
| `ehlers-recursive-median-osc-zero` | Ehlers recursive median oscillator RMO×0 | LP=12, HP=30, medLen=5 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |

**Ladder Protocol:**
1. Execute BTCUSDT across all 4 strategies and grid configurations (LEAN Mode A first).
2. If BTC Mode-A 6m fails $\ge 1.2\times$ B&H or $n \le 5$, mark BTC FAIL and ladder stops for that strategy cell.
3. If BTC passes, advance the EXACT SAME parameter set to ETHUSDT, then SOLUSDT, then BNBUSDT.
4. Tiny-n check: BTC Mode-A $n \le 5 \implies$ FAIL. Flag $n \in [6..10]$ as thin.
5. All results logged to `stage30-dual-sol-bnb-v1-scoreboard.csv` and `.md`.
