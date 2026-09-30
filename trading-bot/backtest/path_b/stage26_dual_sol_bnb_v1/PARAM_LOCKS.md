# stage26-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-21  
**Research ID:** `stage26-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage25 (NHNL BTC 1.687× → ETH 1.085× FAIL; n=8 THIN). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_6c0b.md` & `stage26-dual-sol-bnb-briefs-2026-09-21_2f64.md`

---

## 1. Governance & Methodological Hygiene

To enforce **ETH-after-BTC PRIMARY CRITICAL** (BTC clear $\ge 1.20$ without over-damp PLUS ETH $\ge 1.2\times$ with denser $n \gg 9$; stage25 NHNL BTC 1.687× $\to$ ETH 1.085× FAIL on $n=8$ thin) + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **SOL-after-BTC+ETH** + **BNB-survival after 3-coin** per Path B Stage 26 directives:
- **ETH-after-BTC PRIMARY CRITICAL (Denser $n \gg 9$ Portability):** In Stage 25, `nhnl-oscillator-zero` cleared BTC at 1.687× but collapsed on ETH to 1.085× FAIL because its participatory trade count ($n=8$) was too thin to survive across majors (rhyming with Stage 13 REI and Stage 17 Bostian III). In Stage 26, we lock responsive volume-hybrid, folded-segment convolution, Hilbert adaptive trendline, and adverse-penetration trailing stop families outside stage 1–25 + parks that can clear BTC $\ge 1.20$ without over-damp and port to ETH $\ge 1.2\times$ with multi-dozen trade density ($n \gg 9$).
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 25 NHNL ($n=8$), Stage 14 TTF ($n=6..10$), Stage 8 PGO ($n \approx 9$), and thin $n \le 5$ structure stalls, while avoiding parameter over-inflation that collapses BTC $n$.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD, `eth_smoke` CRITICAL) $\to$ SOL (HARD, `sol_smoke`) $\to$ BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (clear past 1.20 without over-damp / no 0-BTC):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past 1.20; Kill if parameters inflated until BTC $n$ collapses; Kill if improper substitutes labeled seated strategies; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **ETH-after-BTC PRIMARY CRITICAL (no NHNL 1.687× $\to$ 1.085× wipe / no thin $n \approx 8$):** Kill if BTC clears $\ge 1.2\times$ dense then ETH under 1.2×; Kill if ETH $n$ stays thin ~8; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH $n$ multi-dozen ($n \gg 9$).
  - `sol_smoke`: **SOL-AFTER-BTC+ETH:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–25 grafts. Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL:** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–25 IDs (all), including DSP/NHNL/VROC/Elder-thermo, Guppy-CBL/Kirshenbaum/IMI/Williams-AD, QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV.

---

## 2. Locked Strategy 1 (`katsanos-fve-zero-cross`)

### 2.1 Formulation
- **Katsanos Finite Volume Elements (FVE):**
  - $\text{TP} = (\text{high} + \text{low} + \text{close}) / 3$
  - $\text{intra} = \ln(\text{high}) - \ln(\text{low})$
  - $\text{VINTRA} = \text{stdev}(\text{intra}, \text{Samples})$
  - $\text{inter} = \ln(\text{TP}) - \ln(\text{TP}[1])$
  - $\text{VINTER} = \text{stdev}(\text{inter}, \text{Samples})$
  - $\text{CutOff} = (\text{CINTRA} \cdot \text{VINTRA} + \text{CINTER} \cdot \text{VINTER}) \cdot \text{close}$
  - $\text{MF} = (\text{close} - (\text{high} + \text{low}) / 2) + (\text{TP} - \text{TP}[1])$
  - $\text{FveFactor} = +1.0 \text{ if } \text{MF} > \text{CutOff} \text{ else } -1.0 \text{ if } \text{MF} < -\text{CutOff} \text{ else } 0.0$
  - $\text{VA} = \text{SMA}(\text{volume}, \text{Samples})$
  - $\text{FVE} = 100.0 \cdot \sum(\text{volume} \cdot \text{FveFactor}, \text{Samples}) / (\text{VA} \cdot \text{Samples})$
  - Prefer **$\text{Samples} = 22, \text{CINTRA} = 0.1, \text{CINTER} = 0.1$** (Katsanos published).
  - $\ne$ VFI (interday MF + volume cap / vave), $\ne$ VPCI, $\ne$ VZO, $\ne$ Bostian-III, $\ne$ AccDist, $\ne$ CLV×vol.
- **Mode A (ETH-Density Lean):**
  - Long entry: `crossover(fve, 0)`
  - Exit: `crossunder(fve, 0)`
- **Mode B (Rising/Quality Filter):**
  - Require `fve > sma(fve, mal)` $\text{mal} \in \{10, 20\}$ — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep (LEAN): $\text{Samples} \in \{14, 18, 22, 30\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(samples22)` (preferred)
  2. `mode_a|(samples14)`
  3. `mode_a|(samples18)`
  4. `mode_a|(samples30)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{Samples} \in \{14, 18, 22, 30\}$ locked. Parameter inflation collapses BTC $n$ forbidden. VFI/VPCI/VZO/AccDist substitute forbidden. Prefer Mode A Samples=22, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`ehlers-convolution-zero`)

### 3.1 Formulation
- **Ehlers Convolution Fold-Correlation:**
  - Cycle Analytics ch. 13 (SwamiCharts Convolution).
  - Prefilter price with HighPass ($\text{period} = 48$) and SuperSmoother ($\text{period} = 10$).
  - For given $\text{Lookback} = 2 \cdot \text{half}$: fold segments about the midpoint: $S_1[i] = \text{filt}[i]$ for $i \in [0..\text{half}-1]$, $S_2[i] = \text{filt}[\text{Lookback}-1 - i]$.
  - $\text{conv} = \text{Pearson correlation}(S_1, S_2)$.
  - Prefer **$\text{Lookback} = 18, \text{thr} = 0.05$** (half-lag $\approx 9$).
  - $\ne$ CorrCycle Real×0, $\ne$ Spearman, $\ne$ BandPass×0, $\ne$ DSP×0, $\ne$ CyberCycle, $\ne$ EBSW.
- **Mode A (ETH-Density Lean):**
  - Long entry: `crossover(conv, thr)` (thr-reclaim)
  - Exit: `crossunder(conv, thr)` or peak-fade (`conv < conv[1] and conv[1] >= conv[2] and conv[1] > thr`)
- **Mode B (Rising Quality Filter):**
  - Require `conv > conv[1]` on entry — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep (LEAN): $\text{Lookback} \in \{13, 18, 26, 39\}$; $\text{thr} \in \{0.0, 0.05, 0.10\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(lb18,thr0.05)` (preferred)
  2. `mode_a|(lb13,thr0.05)`
  3. `mode_a|(lb26,thr0.05)`
  4. `mode_a|(lb18,thr0.0)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{Lookback} \in \{13, 18, 26, 39\}$, $\text{thr} \in \{0.0, 0.05, 0.10\}$. CorrCycle/BandPass/DSP substitute forbidden. Prefer Mode A (18, 0.05), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`hilbert-inst-trendline-cross`)

### 4.1 Formulation
- **Hilbert Transform Instantaneous Trendline:**
  - TA-Lib `HT_TRENDLINE` / Ehlers *Rocket Science for Traders*.
  - Hilbert transform dominant cycle period measurement via quadrature / in-phase even/odd arrays.
  - $\text{SMA}(\text{price}, \text{DCPeriodInt})$ smoothed by 4-bar WMA:
    $\text{ht}[t] = (4 \cdot \text{sma}[t] + 3 \cdot \text{sma}[t-1] + 2 \cdot \text{sma}[t-2] + \text{sma}[t-3]) / 10$.
  - No free Length (DC adaptive).
  - Prefer **`source = "close"`**.
  - $\ne$ `itrend-trigger-a007` (fixed $\alpha=0.07$ IIR + Trigger), $\ne$ Predictive MA, $\ne$ Decycler, $\ne$ MAMA×FAMA, $\ne$ SuperSmoother residual.
- **Mode A (ETH-Density Lean):**
  - Long entry: `crossover(price, ht)`
  - Exit: `crossunder(price, ht)`
- **Mode B (Rising Quality Filter):**
  - Require `ht > ht[1]` on entry — only if Mode A over-whips; identical across all four coins.

### 4.2 Locked Parameter Space
- Sweep (LEAN): `source` $\in \{\text{"close"}, \text{"hl2"}\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(close)` (preferred)
  2. `mode_a|(hl2)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `source` $\in \{\text{"close"}, \text{"hl2"}\}$. ITrend-Trigger/PMA/MAMA/SuperTrend substitute forbidden. Watch over-damp: kill if $n \le 5$. Prefer Mode A close×HT, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`elder-safezone-trail-flip`)

### 5.1 Formulation
- **Elder SafeZone Adverse-Penetration Trailing Stop Flip:**
  - Dr. Alexander Elder, *Come Into My Trading Room* (pp. 173–180).
  - $\text{EMA} = \text{EMA}(\text{hl2}, \text{emaLen})$
  - $\text{uptrend} = \text{EMA} > \text{EMA}[3]$ (trend context)
  - $\text{penDown} = \max(\text{low}[1] - \text{low}, 0.0)$
  - $\text{AvgPen} = \text{sum}(\text{penDown}, N) / \max(1, \text{count}(\text{penDown} > 0, N))$
  - $\text{rawStop} = \text{low}[1] - k \cdot \text{AvgPen}$
  - $\text{longStop} = \max(\text{rawStop}[t], \text{rawStop}[t-1], \text{rawStop}[t-2], \text{rawStop}[t-3])$ (ratchet)
  - Prefer **$(\text{emaLen}=22, N=10, k=2.5)$**.
  - Swap for Dual Differentiator (Dual Diff is DC period estimate, not tradeable×0).
  - $\ne$ Wilder VS (ATR·factor SAR), $\ne$ Chande-Kroll (two-stage ATR corridor), $\ne$ Guppy CBL (count-back), $\ne$ SuperTrend.
- **Mode A (ETH-Density Lean):**
  - Long entry: `uptrend and crossover(close, longStop)`
  - Exit: `crossunder(close, longStop)`
- **Mode B (Trend Confirmation Filter):**
  - Require $\text{uptrend}$ for $\text{confirmBars} \in \{2, 3\}$ — only if Mode A over-whips; identical across all four coins.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $\text{emaLen} \in \{14, 22, 30\}$; $N \in \{8, 10, 15\}$; $k \in \{2.0, 2.5, 3.0\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(ema22,N10,k2.5)` (preferred)
  2. `mode_a|(ema14,N10,k2.5)`
  3. `mode_a|(ema22,N8,k2.0)`
  4. `mode_a|(ema22,N15,k3.0)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{emaLen} \in \{14, 22, 30\}$, $N \in \{8, 10, 15\}$, $k \in \{2.0, 2.5, 3.0\}$. Wilder-VS/Chande-Kroll/CBL/SuperTrend substitute forbidden. Prefer Mode A (22, 10, 2.5), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.
