# stage18-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage18-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage17 (Bostian III dense BTC clear -> ETH HARD FAIL). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_a014.md` & `stage18-dual-sol-bnb-briefs-2026-09-18_2f5a.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC->ETH portability PRIMARY** (Bostian III / DeMark REI lesson) + **Denser $n \gg 9$** + **SOL-after-BTC+ETH** + **BNB-Survival after 3-coin clear** per Path B Stage 18 directives:
- **BTC->ETH Portability PRIMARY CHOKE (Bostian/REI Lesson):** In Stage 17, `bostian-iii-sma-zero` produced dense BTC clears (~1.412–2.468x, $n=31..40$) but wiped out completely on ETH (~0.255–0.639x), rhyming directly with Stage 13 `demark-rei-zero-cross`. The failure mode stemmed from volume-intensity overfitting to BTC-specific microstructure. Stage 18 explicitly locks five price-path / percentage-deviation / regime-direction / forecast-deviation / projection-trigger families outside stage1–17 + parks designed to achieve dense BTC participation ($n \gg 9$) that port cleanly to ETH ($\ge 1.2\times$ B&H) without per-coin retuning.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$) and Stage 8 PGO ($n \approx 9$), without stage12/15 over-damp collapse (0 BTC).
- **SOL-after-BTC+ETH Preservation:** Avoid Stage 16 Kagi failure mode (BTC+ETH cleared then SOL stalled at 0.807x).
- **BNB-Survival (CRITICAL after 3-coin clear):** Withstand quieter BNB regime without quiet wipe (Stage 14 TTF lesson).
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially never ETH-only or BNB-only retuning) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD — Bostian/REI choke) $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if parameter inflation collapses BTC $n$; Kill if Decycler/BandPass/PVO/Stoch/LinReg-channel substitute; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY PRIMARY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH wipes; Kill if parameters retuned only on ETH; Kill if III/volume-intensity or Decycler/BandPass labeled DPO/PPO/PO. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH CRITICAL:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if 15m spam; Kill if stage12-17 grafts; Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **CRITICAL after BTC+ETH+SOL (TTF lesson):** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; per-coin retune. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–17 IDs (all), including HA/Blau MDI/DSS/Bostian III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, stage12 smoother class, Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, PMO.

---

## 2. Locked Strategy 1 (`dpo-zero-cross`)

### 2.1 Formulation
- **Detrended Price Oscillator (DPO x 0):**
  - $\text{displace} = \lfloor X/2 \rfloor + 1$
  - $\text{smaX} = \text{sma}(\text{close}, X)$
  - $\text{dpo} = \text{close}[\text{displace}] - \text{smaX}$ (StockCharts displacement convention)
  - Prefer **$X=20$**. Do **not** right-shift to defeat cycle purpose on first pass.
  - $\ne$ Decycler (stage 3), $\ne$ BandPass (stage 16), $\ne$ Cyber Cycle, $\ne$ Bostian III (stage 17).
- **Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{dpo}, 0)$
  - Exit: $\text{crossunder}(\text{dpo}, 0)$ (or ATR trail stop)
- **Mode B (BNB quiet / ETH chatter):**
  - Hold requirement: $\text{dpo} > 0$ held for $\ge 1$ bar after crossover
  - Only if Mode A over-whips; identical params.

### 2.2 Locked Parameter Space
- Sweep: $X \in \{14, 20, 28\}$, hold $\in \{0, 1\}$
- Primary grid:
  1. `mode_a|(len20)` (preferred)
  2. `mode_a|(len14)`
  3. `mode_a|(len28)`
  4. `mode_b|(len20,hold1)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $X \in \{14, 20, 28\}$; $X > 50$ forbidden. Mode B forced while Mode A BTC healthy fails. Prefer Mode A $X=20$, 1H+.
- **eth_smoke:** $X \in \{14, 20, 28\}$; retuning only on ETH fails. Decycler/BandPass/III substitute fails.
- **sol_smoke:** 15m $X \le 5$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 3. Locked Strategy 2 (`ppo-ema-signal-cross`)

### 3.1 Formulation
- **Percentage Price Oscillator (PPO x Signal):**
  - $\text{fastE} = \text{ema}(\text{close}, \text{fast})$
  - $\text{slowE} = \text{ema}(\text{close}, \text{slow})$
  - $\text{ppo} = 100 \times (\text{fastE} - \text{slowE}) / \text{slowE}$
  - $\text{sig} = \text{ema}(\text{ppo}, \text{sigLen})$
  - Prefer **$(\text{fast}=12, \text{slow}=26, \text{sig}=9)$**.
  - Distinct %-normalized spread: $\ne$ PVO (volume stage 4), $\ne$ absolute MACD dual-mom, $\ne$ free EMA dual.
- **Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{ppo}, \text{sig})$
  - Exit: $\text{crossunder}(\text{ppo}, \text{sig})$ (or ATR trail stop)
- **Mode B (BNB quiet / Mode A+ zero-bias):**
  - Long entry: $\text{crossover}(\text{ppo}, \text{sig}) \land \text{ppo} > 0$
  - Exit: $\text{crossunder}(\text{ppo}, \text{sig})$ (or ATR trail stop)
  - Only if Mode A over-whips; identical params.

### 3.2 Locked Parameter Space
- Sweep: $\text{fast} \in \{8, 12\}$, $\text{slow} \in \{21, 26\}$, $\text{sig} \in \{5, 9\}$
- Primary grid:
  1. `mode_a|(fast12,slow26,sig9)` (preferred)
  2. `mode_a|(fast8,slow21,sig5)`
  3. `mode_a|(fast12,slow21,sig9)`
  4. `mode_b|(fast12,slow26,sig9,pos)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{fast} \in \{8, 12\}$, $\text{slow} \in \{21, 26\}$, $\text{sig} \in \{5, 9\}$. Mode B forced while Mode A BTC healthy fails. Prefer Mode A (12, 26, 9), 1H+.
- **eth_smoke:** Retuning only on ETH fails. PVO/III/absolute-MACD substitute fails.
- **sol_smoke:** 15m (5, 13, 3) forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 4. Locked Strategy 3 (`vhf-threshold-close-dir`)

### 4.1 Formulation
- **Vertical Horizontal Filter x Close Direction:**
  - $\text{num} = \max(\text{close}, n) - \min(\text{close}, n)$
  - $\text{den} = \sum_{j=0}^{n-1} |\text{close}_{t-j} - \text{close}_{t-j-1}|$
  - $\text{vhf} = \text{num} / \text{den}$ (guard $\text{den} == 0$)
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - $\text{longCond} = \text{vhf} > \text{thr} \land \text{bull}$
  - Prefer **$(n=28, \text{thr}=0.35, \text{dirLen}=3)$**.
  - Distinct close-path regime x direction: $\ne$ CHOP, $\ne$ ADX/DMI, $\ne$ RWI.
- **Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer first):**
  - Long entry: $\text{longCond} \land \neg\text{longCond}[1]$ (rising edge)
  - Exit: $\neg\text{longCond}$ (falling edge or ATR trail stop)
- **Mode B (BNB quiet):**
  - Raise threshold: $\text{thr}=0.40$ / longer $n$
  - Only if Mode A over-whips; identical params.

### 4.2 Locked Parameter Space
- Sweep: $n \in \{18, 28\}$, $\text{thr} \in \{0.30, 0.35, 0.40\}$, $\text{dirLen} \in \{1, 3, 5\}$
- Primary grid:
  1. `mode_a|(n28,thr0.35,dir3)` (preferred)
  2. `mode_a|(n18,thr0.30,dir1)`
  3. `mode_a|(n28,thr0.40,dir5)`
  4. `mode_b|(n28,thr0.40,dir3)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $n \in \{18, 28\}$, $\text{thr} \in \{0.30, 0.35, 0.40\}$, $\text{dirLen} \in \{1, 3, 5\}$. $n > 60$ or $\text{thr} > 0.60$ collapses entries $\to$ fails. Prefer Mode A (28, 0.35, 3), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Direction-blind VHF or ADX/CHOP/III substitute fails.
- **sol_smoke:** 15m $n \le 5$, $\text{thr} \le 0.10$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 5. Locked Strategy 4 (`forecast-oscillator-zero`)

### 5.1 Formulation
- **Forecast Oscillator (FOSC x 0):**
  - Over window $\text{len}$: linear regression fit $y = a + b \cdot x$
  - $\text{lrc} = a + b \cdot (\text{len} - 1)$ (LinReg endpoint at bar 0)
  - $\text{lrs} = b$ (LinReg slope)
  - $\text{tsf} = \text{lrc} + \text{lrs} = a + b \cdot \text{len}$ (1 bar ahead Time Series Forecast)
  - $\text{fosc} = 100 \times (\text{close} - \text{tsf}[1]) / \text{close}$
  - Prefer **$\text{len}=14$**.
  - Distinct %-deviation vs forecast: $\ne$ LinReg channel-break, $\ne$ LinReg-slope-zero, $\ne$ PMA 7/7/4 (stage 17), $\ne$ NetLead (stage 11).
- **Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{fosc}, 0)$
  - Exit: $\text{crossunder}(\text{fosc}, 0)$ (or ATR trail stop)
- **Mode B (BNB quiet):**
  - Signal cross: $\text{fosc}$ vs $\text{sma}(\text{fosc}, \text{sigLen})$ ($\text{sigLen}=5$)
  - Only if Mode A over-whips; identical params.

### 5.2 Locked Parameter Space
- Sweep: $\text{len} \in \{10, 14, 21\}$, $\text{sigLen}=5$
- Primary grid:
  1. `mode_a|(len14)` (preferred)
  2. `mode_a|(len10)`
  3. `mode_a|(len21)`
  4. `mode_b|(len14,sig5)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{len} \in \{10, 14, 21\}$; $\text{len} > 50$ collapses BTC $n$ $\to$ fails. Prefer Mode A $\text{len}=14$, 1H+.
- **eth_smoke:** Retuning only on ETH fails. LinReg-channel / PMA / III substitute fails.
- **sol_smoke:** 15m $\text{len} \le 3$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 6. Locked Strategy 5 (`projection-oscillator-trigger-cross`)

### 6.1 Formulation
- **Mel Widner Projection Oscillator x Trigger:**
  - Over window $\text{len}$: OLS regression slopes of `high` ($\text{slopeH}$) and `low` ($\text{slopeL}$)
  - For each bar $k \in \{0..\text{len}-1\}$ bars ago:
    - $\text{upperCand}[k] = \text{high}[t-k] + k \cdot \text{slopeH}$
    - $\text{lowerCand}[k] = \text{low}[t-k] - k \cdot \text{slopeL}$
  - $\text{upperProj} = \max(\text{upperCand})$; $\text{lowerProj} = \min(\text{lowerCand})$
  - $\text{po} = 100 \times (\text{close} - \text{lowerProj}) / (\text{upperProj} - \text{lowerProj})$ (guard $\text{upper} \ne \text{lower}$)
  - $\text{trig} = \text{ema}(\text{po}, \text{trigLen})$
  - Prefer **$(\text{len}=14, \text{trigLen}=3)$**.
  - Distinct slope-adjusted stochastic: $\ne$ raw Stoch K/D (burned), $\ne$ DSS Bressert (stage 17), $\ne$ LinReg channel-break, $\ne$ SMI.
- **Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(\text{po}, \text{trig})$
  - Exit: $\text{crossunder}(\text{po}, \text{trig})$ (or ATR trail stop)
- **Mode B (BNB quiet):**
  - Oversold/overbought filter: cross while $\text{po} < 30$, exit while $\text{po} > 70$
  - Only if Mode A over-whips; identical levels.

### 6.2 Locked Parameter Space
- Sweep: $\text{len} \in \{10, 14, 20\}$, $\text{trigLen} \in \{3, 5\}$
- Primary grid:
  1. `mode_a|(len14,trig3)` (preferred)
  2. `mode_a|(len10,trig3)`
  3. `mode_a|(len20,trig5)`
  4. `mode_b|(len14,trig3,ob_os)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{len} \in \{10, 14, 20\}$, $\text{trigLen} \in \{3, 5\}$; $\text{len} > 50$ collapses BTC $n$ $\to$ fails. Prefer Mode A (14, 3), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Stoch/DSS/III substitute fails.
- **sol_smoke:** 15m $\text{len} \le 5$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B shorts ungated fails.

---

## 7. Master Parameter Locks Matrix

| # | Strategy ID | Key Parameters (Locked) | Mode A Definition | Mode B Definition | Timeframes | Primary Focus |
|---|-------------|-------------------------|-------------------|-------------------|------------|---------------|
| 1 | `dpo-zero-cross` | $X \in \{14, 20, 28\}$, hold $\in \{0, 1\}$ | $\text{dpo} \times 0$ cross | $\text{hold}=1$ bar | 1H, 4H | Price-path displaced SMA deviation |
| 2 | `ppo-ema-signal-cross` | fast $\in \{8, 12\}$, slow $\in \{21, 26\}$, sig $\in \{5, 9\}$ | $\text{ppo} \times \text{sig}$ cross | $\text{ppo} > 0$ bias | 1H, 4H | %-scaled EMA momentum spread |
| 3 | `vhf-threshold-close-dir` | $n \in \{18, 28\}$, thr $\in \{0.30, 0.35, 0.40\}$, dirLen $\in \{1, 3, 5\}$ | $\text{vhf} > \text{thr} \land \text{bull}$ edge | $\text{thr}=0.40$ | 1H, 4H | Regime gate $\times$ close direction |
| 4 | `forecast-oscillator-zero` | len $\in \{10, 14, 21\}$, sigLen $= 5$ | $\text{fosc} \times 0$ cross | $\text{fosc} \times \text{sma5}$ | 1H, 4H | %-deviation vs 1-bar LinReg forecast |
| 5 | `projection-oscillator-trigger-cross` | len $\in \{10, 14, 20\}$, trigLen $\in \{3, 5\}$ | $\text{po} \times \text{trig}$ cross | 30 / 70 filter | 1H, 4H | Widner slope-adjusted stochastic |

---

## 8. Smokes & Stop-Ladder Execution Protocol

1. **BTC Lead Evaluation:**
   - Execute all 40 parameter cells (5 strategies $\times$ 4 param sets $\times$ 2 timeframes).
   - Require Mode-A return $\ge 1.2\times$ B&H on last-6m window.
   - Enforce tiny-$n$ kill: if $n \le 5$, marked as FAIL cell.
   - Flag $n \in [6..10]$ as thin.
2. **ETH Portability Evaluation (HARD CHOKE — Bostian/REI Lesson):**
   - Only parameter cells that PASS BTC 6m advance to ETH.
   - Enforce identical parameters (no retuning on ETH).
   - Check retention: ETH trades $n \ge 25\%$ of BTC trades.
   - Require Mode-A return $\ge 1.2\times$ B&H on last-6m window.
3. **SOL Portability Evaluation (HARD):**
   - Only parameter cells that PASS ETH 6m advance to SOL.
   - Enforce identical parameters.
   - Check retention: SOL trades $n \ge 25\%$ of ETH trades.
   - Require Mode-A return $\ge 1.2\times$ B&H on last-6m window.
4. **BNB Survival Evaluation (HARD — TTF Lesson):**
   - Only parameter cells that PASS SOL 6m advance to BNB.
   - Enforce identical parameters.
   - Require Mode-A return $\ge 1.2\times$ B&H on last-6m window.
