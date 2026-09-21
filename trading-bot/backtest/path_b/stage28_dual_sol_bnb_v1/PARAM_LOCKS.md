# stage28-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-21  
**Research ID:** `stage28-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage27 wipe (closest Schwager-VR 0.698x regress vs FVE 1.055x; BTC 0/32 FAIL LEAD). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_97ff.md` & `stage28-dual-sol-bnb-briefs-2026-09-21_cf61.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY CRITICAL** (clear past FVE 1.055x / VR 0.698x regress to >= 1.20 without over-damp) + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **ETH denser n >> 9 portability** + **SOL-after-BTC+ETH** + **BNB-survival after 3-coin** per Path B Stage 28 directives:
- **BTC LEAD PRIMARY CRITICAL:** In Stage 27, `schwager-vr-breakout` regressed to 0.698x vs Stage 26 FVE's 1.055x, leaving BTC 0/32 FAIL LEAD across the pack. In Stage 28, we lock four distinct, non-clone published families outside stage 1–27 + remaining parks (EC x EMA, Vervoort ZL-HA x Typ, Ehlers Zero-Lag FIR, Varadi DV2 midline) that can clear BTC Mode-A >= 1.20 without over-damping to 0-BTC.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser n >> 9 Policy:** Ensure trade density remains well above the thin counts of Stage 25 NHNL (n=8), Stage 14 TTF (n=6..10), Stage 8 PGO (n ≈ 9), and thin n <= 5 structure stalls, while avoiding parameter over-inflation that collapses BTC n.
- **Tiny-n Policy (Critical):** If Mode-A BTC n <= 5 on 6m -> FAIL that cell even if xB&H >= 1.2 (hard-fail cell as over-gated / under-specified). Also flag n ≈ 9 (in range [6..10]) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return >= 1.2x B&H -> ETH (HARD, `eth_smoke`) -> SOL (HARD, `sol_smoke`) -> BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (clear past 1.055x / >= 1.20 / no 0-BTC / no VR 0.698x regress):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past 1.20 (FVE rhyme); Kill if parameters inflated until BTC n collapses; Kill if ZLEMA/EDCF/US/HA-color-flip/DVI substitute labeled seated strategies; Kill if Mode B forced while Mode A BTC n healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **ETH-after-BTC (no NHNL 1.687x -> 1.085x wipe / no thin n ≈ 8):** Kill if BTC clears >= 1.2x then ETH under 1.2x; Kill if ETH n stays thin ~8; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH n multi-dozen (n >> 9).
  - `sol_smoke`: **SOL-AFTER-BTC+ETH (no Kagi / percentile 0.922x fail):** Kill if BTC+ETH clear >= 1.2x then SOL under 1.2x; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–27 grafts. Retention check: after ETH, SOL n must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL (no TTF / HHLL quiet wipe):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–27 IDs (all), including Qstick/Klinger/%Envelopes/Schwager-VR, FVE/Convolution/HT_TRENDLINE/SafeZone, DSP/NHNL/VROC/Elder-thermo, Guppy-CBL/Kirshenbaum/IMI/Williams-AD, QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV, ZLEMA, EDCF filt*lag.

---

## 2. Locked Strategy 1 (`ehlers-ec-ema-cross`)

### 2.1 Formulation
- **Ehlers–Way Error-Correcting Zero-Lag EC:**
  - John Ehlers & Ric Way (*Zero Lag (Well, Almost)*, S&C Nov 2010; MESA ZeroLag.pdf; Wealth-Lab TASC Nov 2010).
  - `alpha = 2.0 / (Length + 1.0)`
  - `ema = alpha * close + (1.0 - alpha) * ema[1]`
  - Search Gain in `[-GainLimit/10 .. +GainLimit/10]` step 1 minimizing `|close - trial_ec|`:
    `trial_ec = alpha * (ema + g * (close - ec[1])) + (1.0 - alpha) * ec[1]`
  - Finalize EC:
    `ec = alpha * (ema + BestGain * (close - ec[1])) + (1.0 - alpha) * ec[1]`
  - `least_error_pct = 100.0 * min_error / close`
  - Prefer **(Length=20, GainLimit=50, Thresh=0.0)**.
  - $\ne$ ZLEMA (EMA(2P - P[lag])), $\ne$ EDCF filt*lag, $\ne$ Ultimate Smoother dual, $\ne$ PMA.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(ec, ema)`
  - Exit: `crossunder(ec, ema)`
- **Mode B (Least Error Threshold Filter):**
  - Require `least_error_pct > Thresh` where `Thresh in {0.5, 0.75}` — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep (LEAN): $Length \in \{12, 20, 32\}$; $GainLimit \in \{22, 50\}$; $Thresh \in \{0.0, 0.5, 0.75\}$; TF 1H vs 4H. Mode A defaults first.
- Primary grid:
  1. `mode_a|(len20,gain50,thr0)` (preferred)
  2. `mode_a|(len12,gain22,thr0)`
  3. `mode_a|(len32,gain50,thr0)`
  4. `mode_b|(len20,gain50,thr0.75)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $Length \in \{12, 20, 32\}$, $GainLimit \in \{22, 50\}$ locked. Parameter inflation collapses BTC $n$ forbidden. ZLEMA/EDCF/US substitute forbidden. Prefer Mode A (20, 50, 0), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`vervoort-zlha-typ-cross`)

### 3.1 Formulation
- **Sylvain Vervoort Zero-Lag TEMA(haC) x Zero-Lag TEMA(Typ):**
  - Sylvain Vervoort (*The Quest for Reliable Crossovers*, S&C May 2008; Traders' Tips May 2008; STOCATA):
    - `haOpen = (haOpen[1] + haClose[1]) / 2` (seed: `(open[0] + close[0]) / 2`)
    - `haClose = ((O + H + L + C) / 4 + haOpen + max(H, haOpen) + min(L, haOpen)) / 4`
    - `Typ = (H + L + C) / 3`
    - `ZL(x, N) = TEMA(x, N) + (TEMA(x, N) - TEMA(TEMA(x, N), N))`
    - `zlHa = ZL(haClose, N)`
    - `zlTyp = ZL(Typ, N)`
  - Prefer **N=34**.
  - $\ne$ Heikin-Ashi color-flip (stage 17 bias-flip), $\ne$ TEMA dual-of-close, $\ne$ ZLEMA, $\ne$ DEMA dual.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(zlTyp, zlHa)`
  - Exit: `crossunder(zlTyp, zlHa)`
- **Mode B (Rising ZLTyp Filter):**
  - Require `zlTyp > zlTyp[1]` on entry — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep (LEAN): $N \in \{21, 34, 55\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(N34)` (preferred)
  2. `mode_a|(N21)`
  3. `mode_a|(N55)`
  4. `mode_b|(N34_rising)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $N \in \{21, 34, 55\}$ locked. HA color-flip / TEMA close-dual / ZLEMA substitute forbidden. Prefer Mode A N=34, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`ehlers-fir-zl-price-cross`)

### 4.1 Formulation
- **John Ehlers Zero-Lag FIR Filter x Price Cross:**
  - John Ehlers (*Zero-Lag Data Smoothers*, S&C V.20:7 July 2002; MesaSoftware; TV everget).
  - Mode A (7-tap locked Zero-Lag FIR /9.5):
    - `zlFir = (P + 4.5*P[1] + 5.5*P[2] + 3.0*P[3] - 0.5*P[4] - 1.5*P[5] - 2.5*P[6]) / 9.5`
  - Mode B (6-tap favorite FIR /12):
    - `fir12 = (P + 2.0*P[1] + 3.0*P[2] + 3.0*P[3] + 2.0*P[4] + P[5]) / 12.0`
  - Source: `src in {'close', 'hl2'}` (prefer `close`).
  - Prefer **src=close Mode A /9.5**.
  - $\ne$ EDCF filt*lag (nonlinear distance coeff), $\ne$ ZLEMA, $\ne$ SuperSmoother, $\ne$ Roofing filter.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(close, zlFir)`
  - Exit: `crossunder(close, zlFir)`
- **Mode B (Favorite FIR /12 Filter):**
  - Use `/12` coefficients instead of `/9.5` — only if Mode A over-whips; identical across all four coins.

### 4.2 Locked Parameter Space
- Sweep (LEAN): $src \in \{\text{'close'}, \text{'hl2'}\}$; $denom \in \{\text{'9.5'}, \text{'12'}\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(src_close_zl9.5)` (preferred)
  2. `mode_a|(src_hl2_zl9.5)`
  3. `mode_b|(src_close_fir12)`
  4. `mode_b|(src_hl2_fir12)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). EDCF / ZLEMA / SuperSmoother substitute forbidden. Prefer Mode A src=close /9.5, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`dv2-varadi-midline`)

### 5.1 Formulation
- **David Varadi DV2 Percent-Rank Midline Reclaim:**
  - David Varadi (CSS Analytics 2009 *Differential DV2 Calculation*; Quantitativo *A Different Indicator*).
  - `r = close / (high + low)` (guard $high + low > 0$)
  - `dv_raw = (r + r[1]) / 2.0`
  - `dv2 = 100.0 * percentrank(dv_raw, rankLen)`
    where `percentrank = count(val in window <= current) / rankLen`
  - Trend-port mid-reclaim — **not** classic DV2 < 10 mean-reversion fade.
  - Prefer **(rankLen=100, mid=50.0)**.
  - $\ne$ DVI (magnitude + stretch vote), $\ne$ RSI2, $\ne$ PSY, $\ne$ IMI.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(dv2, 50.0)`
  - Exit: `crossunder(dv2, 50.0)`
- **Mode B (Pullback Reclaim Filter):**
  - Long entry on reclaim through 40 (`crossover(dv2, 40)`), exit at 50 (`crossunder(dv2, 50)`) — identical across all four coins.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $rankLen \in \{63, 100, 126, 252\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(rank100_mid50)` (preferred)
  2. `mode_a|(rank63_mid50)`
  3. `mode_a|(rank126_mid50)`
  4. `mode_b|(rank100_reclaim40)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). DVI / RSI2 / PSY / IMI substitute forbidden. Watch MR chop under costs. Prefer Mode A rankLen=100 mid=50, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 6. Execution Grid Summary

| Strategy ID | TF | Primary Parameter Grid | Mode |
|---|---|---|---|
| `ehlers-ec-ema-cross` | 1H, 4H | (20,50,0), (12,22,0), (32,50,0), (20,50,0.75) | Mode A / Mode B |
| `vervoort-zlha-typ-cross` | 1H, 4H | N=34, N=21, N=55, N=34-rising | Mode A / Mode B |
| `ehlers-fir-zl-price-cross` | 1H, 4H | (close,9.5), (hl2,9.5), (close,12), (hl2,12) | Mode A / Mode B |
| `dv2-varadi-midline` | 1H, 4H | (100,50), (63,50), (126,50), (100,40) | Mode A / Mode B |

Total candidate cells per coin: $4 \text{ strategies} \times 2 \text{ TFs} \times 4 \text{ parameter configs} = 32 \text{ cells}$.  
Total potential ladder cells across 4 coins: $32 \times 4 = 128 \text{ cells}$ (subject to stop-ladder pruning).
