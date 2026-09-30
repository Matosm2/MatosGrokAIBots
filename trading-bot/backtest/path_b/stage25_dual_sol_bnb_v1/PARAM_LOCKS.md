# stage25-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage25-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage24 (BTC PASS 0/32; Kirshenbaum ~1.113× near-miss; stage23 Chande-Kroll ~1.194×). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_c6a1.md` & `stage25-dual-sol-bnb-briefs-2026-09-18_2b4d.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY CRITICAL** (push past Chande-Kroll ~1.194× / Kirshenbaum ~1.113× near-misses without over-damp) + **Denser $n \gg 9$** + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **BNB-survival after 3-coin** per Path B Stage 25 directives:
- **BTC LEAD PRIMARY (Chande-Kroll ~1.194× / Kirshenbaum ~1.113× Near-Miss Reclaim):** In Stage 23 and 24, all cells failed on BTC (0/32 each stage), with Chande-Kroll Stop Flip at 1H reaching ~1.194× and Kirshenbaum Bands at 4H reaching ~1.113× (just under the $\ge 1.2\times$ threshold). In Stage 25, we lock responsive cycle-in-phase, single-asset extreme-rate, volume rate of change, and volatility thermometer cool-entry families outside stage 1–24 + parks that can clear dense BTC $\ge 1.2\times$ without over-damp and without cloning stage 23–24 EXIT IDs.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$), Stage 8 PGO ($n \approx 9$), and thin $n \le 5$ structure stalls, while avoiding parameter over-inflation that collapses BTC $n$.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD, `sol_smoke`) $\to$ BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (push past ~1.194× / ~1.113× / no stage23–24 0-BTC):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past ~1.194× / ~1.113× neighborhood; Kill if parameters inflated until BTC $n$ collapses; Kill if improper substitutes labeled seated strategies; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY:** Kill if BTC clears $\ge 1.2\times$ dense then ETH under 1.2×; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–24 grafts. Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL:** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–24 IDs (all), including Guppy-CBL/Kirshenbaum/IMI/Williams-AD, QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV, Pee TDI, stage12 smoother class.

---

## 2. Locked Strategy 1 (`ehlers-dsp-zero-cross`)

### 2.1 Formulation
- **Ehlers Detrended Synthetic Price (DSP):**
  - `price = (high + low) / 2`
  - $\alpha = 2 / (\text{Length} + 1)$
  - $\alpha_2 = \alpha / 2$
  - $\text{EMA}_1 = \alpha \cdot \text{price} + (1 - \alpha) \cdot \text{EMA}_1[1]$
  - $\text{EMA}_2 = \alpha_2 \cdot \text{price} + (1 - \alpha_2) \cdot \text{EMA}_2[1]$
  - $\text{DSP} = \text{EMA}_1 - \text{EMA}_2$
  - Prefer **`Length = 7`** (Ehlers published).
  - $\ne$ DPO (close - displaced SMA), $\ne$ Decycler (HP residual dual), $\ne$ BandPass (IIR bandpass zero), $\ne$ CyberCycle, $\ne$ EBSW.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(dsp, 0)`
  - Exit: `crossunder(dsp, 0)`
- **Mode B (Rising Quality Filter):**
  - Require `dsp > dsp[1]` on entry — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep (LEAN): `Length` $\in \{5, 7, 9, 14\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(len7)` (preferred)
  2. `mode_a|(len5)`
  3. `mode_a|(len9)`
  4. `mode_a|(len14)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `Length` $\in \{5, 7, 9, 14\}$ locked. Parameter inflation collapses BTC $n$ forbidden. Prefer Mode A len=7, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`nhnl-oscillator-zero`)

### 3.1 Formulation
- **Single-Asset New-High / New-Low (NH-NL) Rolling Oscillator:**
  - Over lookback $L$:
    - $\text{isNH} = \text{high} \ge \text{highest}(\text{high}, L)[1]$
    - $\text{isNL} = \text{low} \le \text{lowest}(\text{low}, L)[1]$
  - Over window $W$:
    - $\text{nhRate} = \sum(\text{isNH}, W)$
    - $\text{nlRate} = \sum(\text{isNL}, W)$
    - $\text{osc} = \text{nhRate} - \text{nlRate}$
  - Prefer **$(L=20, W=10)$**.
  - Single-asset only — not breadth.
  - $\ne$ HHLL (confirmed pivot BOS), $\ne$ Donchian (channel break), $\ne$ Aroon (% bars since extreme), $\ne$ percentile.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(osc, 0)`
  - Exit: `crossunder(osc, 0)`
- **Mode B (Threshold Quality Filter):**
  - Require `osc > thr` ($\text{thr} \in \{1.0, 2.0\}$) — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep (LEAN): $L \in \{14, 20, 30\}$; $W \in \{5, 10, 14\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(L20,W10)` (preferred)
  2. `mode_a|(L14,W5)`
  3. `mode_a|(L20,W14)`
  4. `mode_a|(L30,W10)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $L \in \{14, 20, 30\}$, $W \in \{5, 10, 14\}$. HHLL/Donchian/Aroon substitute forbidden. Prefer Mode A (20,10), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`volume-roc-dir`)

### 4.1 Formulation
- **Volume Rate of Change $\times$ Close Direction:**
  - $\text{vroc} = 100 \cdot (\text{volume} - \text{volume}[n]) / \text{volume}[n]$ (guard $\text{volume}[n]=0$)
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - Prefer **$n=14, \text{dirLen}=1$**.
  - $\ne$ PVO (EMA volume % osc), $\ne$ price ROC, $\ne$ vol-expansion*dir, $\ne$ VFI.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(vroc, 0) and bull`
  - Exit: `crossunder(vroc, 0) or not bull`
- **Mode B (Threshold Quality Filter):**
  - Require `vroc > thr` ($\text{thr} \in \{10.0, 20.0\}$) — only if Mode A over-whips; identical across all four coins.

### 4.2 Locked Parameter Space
- Sweep (LEAN): $n \in \{10, 14, 20, 25\}$; $\text{dirLen} \in \{1, 3\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(n14,dir1)` (preferred)
  2. `mode_a|(n10,dir1)`
  3. `mode_a|(n20,dir1)`
  4. `mode_a|(n14,dir3)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $n \in \{10, 14, 20, 25\}$, $\text{dirLen} \in \{1, 3\}$. PVO/price-ROC/VFI substitute forbidden. Prefer Mode A n=14, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`elder-thermometer-cool-dir`)

### 5.1 Formulation
- **Elder Market Thermometer Cool $\times$ Close Direction:**
  - $\text{thermo} = \max(|\text{high} - \text{high}[1]|, |\text{low}[1] - \text{low}|)$
  - $\text{tma} = \text{ta.ema}(\text{thermo}, \text{emaLen})$
  - $\text{cool} = \text{thermo} < \text{tma}$
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - $\text{hot} = \text{thermo} > k \cdot \text{tma}$
  - Prefer **$(\text{emaLen}=22, k=3.0, \text{dirLen}=1)$**.
  - $\ne$ Chaikin / Parkinson rising*dir (opposite polarity — cool entry), $\ne$ Mass, $\ne$ ATR-SAR, $\ne$ Wilder-VS, $\ne$ Chande-Kroll.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossunder(thermo, tma) and bull` (cool rising-edge)
  - Exit: `hot or crossover(thermo, tma)`
- **Mode B (Consecutive Cool Filter):**
  - Require $\text{cool}$ for $\text{confirmBars} \in \{2, 3\}$ — only if Mode A over-whips; identical across all four coins.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $\text{emaLen} \in \{14, 20, 22\}$; $k \in \{2.5, 3.0, 3.5\}$; $\text{dirLen} = 1$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(ema22,k3.0)` (preferred)
  2. `mode_a|(ema14,k3.0)`
  3. `mode_a|(ema20,k2.5)`
  4. `mode_a|(ema22,k3.5)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{emaLen} \in \{14, 20, 22\}$, $k \in \{2.5, 3.0, 3.5\}$, $\text{dirLen}=1$. Chaikin/Parkinson rising*dir/Mass/ATR-SAR substitute forbidden. Prefer Mode A (22,3.0), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.
