# stage27-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-21  
**Research ID:** `stage27-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage26 (FVE dense n=40 @1.055x FAIL LEAD; Convolution/HT/SafeZone 0 BTC). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_8a9d.md` & `stage27-dual-sol-bnb-briefs-2026-09-21_609d.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY CRITICAL** (push past FVE 1.055x to >= 1.20 without over-damp) + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **ETH denser n >> 9 portability** + **SOL-after-BTC+ETH** + **BNB-survival after 3-coin** per Path B Stage 27 directives:
- **BTC LEAD PRIMARY CRITICAL:** In Stage 26, `katsanos-fve-zero-cross` achieved dense trade count (n=40 on 4H) but delivered only 1.055x BTC B&H (failing the >= 1.20x LEAD gate), while the other three strategies produced 0 BTC. In Stage 27, we unpark and lock four distinct, non-clone impulse, volume-force, %-envelope, and Schwager-VR+breakout families outside stage 1–26 + remaining parks that can push past FVE 1.055x to >= 1.20x without over-damping to 0-BTC.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser n >> 9 Policy:** Ensure trade density remains well above the thin counts of Stage 25 NHNL (n=8), Stage 14 TTF (n=6..10), Stage 8 PGO (n ≈ 9), and thin n <= 5 structure stalls, while avoiding parameter over-inflation that collapses BTC n.
- **Tiny-n Policy (Critical):** If Mode-A BTC n <= 5 on 6m -> FAIL that cell even if xB&H >= 1.2 (hard-fail cell as over-gated / under-specified). Also flag n ≈ 9 (in range [6..10]) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return >= 1.2x B&H -> ETH (HARD, `eth_smoke`) -> SOL (HARD, `sol_smoke`) -> BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (clear past 1.055x / >= 1.20 / no 0-BTC):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past 1.20 (FVE rhyme); Kill if parameters inflated until BTC n collapses; Kill if RVI/CMO/ROC/AO/FVE/VFI/VROC/BB/Keltner/JP-VR substitute labeled seated strategies; Kill if Mode B forced while Mode A BTC n healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **ETH-after-BTC (no NHNL 1.687x -> 1.085x wipe / no thin n ≈ 8):** Kill if BTC clears >= 1.2x then ETH under 1.2x; Kill if ETH n stays thin ~8; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH n multi-dozen (n >> 9).
  - `sol_smoke`: **SOL-AFTER-BTC+ETH (no Kagi / percentile 0.922x fail):** Kill if BTC+ETH clear >= 1.2x then SOL under 1.2x; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–26 grafts. Retention check: after ETH, SOL n must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL (no TTF / HHLL quiet wipe):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–26 IDs (all), including FVE/Convolution/HT_TRENDLINE/SafeZone, DSP/NHNL/VROC/Elder-thermo, Guppy-CBL/Kirshenbaum/IMI/Williams-AD, QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV.

---

## 2. Locked Strategy 1 (`qstick-sma-zero`)

### 2.1 Formulation
- **Chande Qstick Indicator:**
  - Tushar Chande / Stanley Kroll (*The New Technical Trader* 1994; Tulip / FM Labs / TeleTrader).
  - `body = close - open` (unnormalized candle bodies).
  - `qstick = sma(body, N)`.
  - Prefer **N=8** (densest; also N=10, 14, 20).
  - $\ne$ RVI (Relative Vigor = (C - O)/(H - L) range-normalized), $\ne$ CMO-zero, $\ne$ ROC-zero, $\ne$ AO-zero, $\ne$ TSI, $\ne$ stage26 FVE.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(qstick, 0)`
  - Exit: `crossunder(qstick, 0)`
- **Mode B (Rising/Quality Filter):**
  - Require `qstick > sma(qstick, sig)` where `sig in {3, 5}` — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep (LEAN): $N \in \{8, 10, 14, 20\}$; TF 1H vs 4H. Mode A defaults first.
- Primary grid:
  1. `mode_a|(N8)` (preferred)
  2. `mode_a|(N10)`
  3. `mode_a|(N14)`
  4. `mode_a|(N20)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $N \in \{8, 10, 14, 20\}$ locked. Parameter inflation collapses BTC $n$ forbidden. RVI/CMO/ROC/AO/TSI substitute forbidden. Prefer Mode A N=8, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`klinger-signal-cross`)

### 3.1 Formulation
- **Stephen Klinger Volume Oscillator (KVO):**
  - Full Volume Force (VF) formulation (Capital.com / Investopedia / CQG / thinkorswim):
    - `hlc = high + low + close`
    - `trend = +1.0 if hlc > hlc[1] else -1.0`
    - `dm = high - low`
    - `cm = cm[1] + dm if trend == trend[1] else dm[1] + dm` (with guard `cm > 0`)
    - `vf = volume * abs(2.0 * ((dm / cm) - 1.0)) * trend * 100.0`
    - `kvo = ema(vf, fast) - ema(vf, slow)`
    - `sig = ema(kvo, signalLen)`
  - Prefer **(fast=34, slow=55, signalLen=13)**.
  - $\ne$ FVE (intra+inter MF cutoff signed volume), $\ne$ VFI, $\ne$ VROC, $\ne$ VPCI, $\ne$ Chaikin Osc, $\ne$ PVO, $\ne$ OBV, $\ne$ MACD-of-price.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(kvo, sig)`
  - Exit: `crossunder(kvo, sig)`
- **Mode B (Above-Zero Quality Filter):**
  - Require `kvo > 0` on entry — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep (LEAN): $(fast, slow) \in \{(21, 34), (34, 55), (55, 89)\}$; $signalLen \in \{9, 13\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(34,55,13)` (preferred)
  2. `mode_a|(21,34,13)`
  3. `mode_a|(34,55,9)`
  4. `mode_a|(55,89,13)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). Parameter inflation collapses BTC $n$ forbidden. FVE/VFI/VROC/VPCI/PVO/Chaikin Osc substitute forbidden. Prefer Mode A (34, 55, 13), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`percent-envelopes-break`)

### 4.1 Formulation
- **Moving Average Percent Envelopes (StockCharts / Fidelity MAE):**
  - `mid = sma(close, Len)`
  - `upper = mid * (1.0 + pct)`
  - `lower = mid * (1.0 - pct)`
  - Prefer **(Len=20, pct=0.025)** (2.5% envelope).
  - $\ne$ Bollinger Bands (stdev bands), $\ne$ Keltner Bands (ATR bands), $\ne$ Kirshenbaum Bands (LinReg stderr bands), $\ne$ STARC Bands, $\ne$ Disparity zero-cross.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(close, upper)`
  - Exit: `crossunder(close, mid)`
- **Mode B (Rising Mid Quality Filter):**
  - Require `mid > mid[1]` on entry — only if Mode A over-whips; identical across all four coins.

### 4.2 Locked Parameter Space
- Sweep (LEAN): $Len \in \{14, 20, 30\}$; $pct \in \{0.015, 0.025, 0.04, 0.05\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(len20,pct0.025)` (preferred)
  2. `mode_a|(len14,pct0.015)`
  3. `mode_a|(len20,pct0.04)`
  4. `mode_a|(len30,pct0.025)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). Over-wide pct collapsing $n$ forbidden. BB/Keltner/Kirshenbaum/STARC/Disparity substitute forbidden. Prefer Mode A (20, 0.025), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`schwager-vr-breakout`)

### 5.1 Formulation
- **Jack Schwager Volatility Ratio + Directional Structure Breakout:**
  - Jack Schwager (*Schwager on Futures: Technical Analysis* / Incredible Charts / Wickra).
  - **Not** Japanese up/down Volume Ratio (scout-wave4 swap enforced).
  - True Range: `tr = max(high - low, abs(high - close[1]), abs(low - close[1]))`
  - Prior TR EMA (current bar excluded per Wickra):
    `ema_prior = ema(tr[1], n)`
  - Volatility Ratio: `vr = tr / ema_prior` (guard `ema_prior == 0`)
  - Prior M-bar high / low:
    `prior_high = highest(high, M)[1]`
    `prior_low = lowest(low, M)[1]`
  - Prefer **(n=14, thr=2.0, M=20)**. Denser fallback: **(n=14, thr=1.5, M=10)**.
  - $\ne$ Japanese Volume Ratio, $\ne$ ATR-ratio x dir alone, $\ne$ Chaikin/Parkinson vol x dir without structure, $\ne$ naked Donchian without VR gate, $\ne$ BB-squeeze.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `vr > thr and crossover(close, prior_high)`
  - Exit: `crossunder(close, prior_low) or crossunder(close, sma(close, M))`
- **Mode B (Confirmed VR Persistence):**
  - Require `vr > thr` confirmed on entry — identical across all four coins.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $n \in \{10, 14, 20\}$; $thr \in \{1.5, 2.0, 2.5\}$; $M \in \{10, 20\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(n14,thr2.0,M20)` (preferred)
  2. `mode_a|(n14,thr1.5,M10)` (denser fallback)
  3. `mode_a|(n10,thr1.5,M20)`
  4. `mode_a|(n20,thr2.0,M10)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). Event sparsity check: watch thin $n$; kill if $n \le 5$; flag if $n \in [6..10]$. Japanese Volume Ratio / naked Donchian / ATR-ratio x dir substitutes forbidden. Prefer Mode A (14, 2.0, 20) or (14, 1.5, 10).
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Lowering thr only on BNB forbidden. Mode B only on BNB fails.

---

## 6. Execution Grid Summary

| Strategy ID | TF | Primary Parameter Grid | Mode |
|---|---|---|---|
| `qstick-sma-zero` | 1H, 4H | N=8, N=10, N=14, N=20 | Mode A |
| `klinger-signal-cross` | 1H, 4H | (34,55,13), (21,34,13), (34,55,9), (55,89,13) | Mode A |
| `percent-envelopes-break` | 1H, 4H | (20,0.025), (14,0.015), (20,0.04), (30,0.025) | Mode A |
| `schwager-vr-breakout` | 1H, 4H | (14,2.0,20), (14,1.5,10), (10,1.5,20), (20,2.0,10) | Mode A |

Total candidate cells per coin: $4 \text{ strategies} \times 2 \text{ TFs} \times 4 \text{ parameter configs} = 32 \text{ cells}$.  
Total potential ladder cells across 4 coins: $32 \times 4 = 128 \text{ cells}$ (subject to stop-ladder pruning).
