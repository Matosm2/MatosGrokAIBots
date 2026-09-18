# stage21-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage21-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage20 (0 BTC chop under costs; stage12/15/18/20 rhyme). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_dc32.md` & `stage21-dual-sol-bnb-briefs-2026-09-18_b3f9.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY without over-damp** (stage12/15/18/20 rhyme) + **Denser $n \gg 9$** + **BTC->ETH->SOL->BNB portability and survival** per Path B Stage 21 directives:
- **BTC LEAD PRIMARY (Stage 12/15/18/20 Rhyme):** In Stage 20, all 40 cells failed BTC on 6m ($0/40$ PASS). Density was high on 1H ($n \gg 9$), but strategies suffered severe chop under execution fees and adverse slippage, never clearing the initial BTC gate. Stage 21 locks responsive non-MA impulse, vol-expansion, and candle-polarity structures capable of catching real BTC impulse expansions without volume-confirmation oscillator chop (VPCI/BW-MFI/DI), without recursive estimate cross (Kalman), and without threshold-on-spread chatter (RAVI).
- **Redundancy Rule & Parkinson Drop Decision:**
  - Per spec: *"After BTC smoke on #1+#4: if Parkinson BTC behavior ≈ Chaikin (same cells / same chop), DROP #4 — do not encode both. Prefer keep Chaikin if tie."*
  - **Empirical BTC Smoke Comparison:**
    - `chaikin-volatility-dir` Mode A (10,10,1) @ 1H: 816 trades, -89.27% ret, 17.2% WR, 3943 signals.
    - `parkinson-vol-expansion-dir` Mode A (10,1) @ 1H: 771 trades, -88.91% ret, 15.3% WR, 3751 signals.
    - Signal overlap: **75.2% joint buy signals** on 1H (2967 joint / 3943 Chaikin), **78.4% joint buy signals** on 4H (766 joint / 977 Chaikin). Both strategies suffer near-identical fee churn under chop.
    - **Decision: Parkinson (#4) is officially DROPPED from ladder scoring** due to BTC-smoke redundancy with Chaikin (#1). Chaikin (#1) is retained as the locked range-vol expansion seat.
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
  - `sol_smoke`: **SOL-AFTER-BTC+ETH CRITICAL:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if 15m spam; Kill if stage12-20 grafts; Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **CRITICAL AFTER 3-COIN (HHLL/TTF LESSON):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–20 IDs (all), including VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, stage12 smoother class, Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, PMO.

---

## 2. Locked Strategy 1 (`chaikin-volatility-dir`)

### 2.1 Formulation
- **Marc Chaikin Volatility — Expansion $\times$ Close-Direction:**
  - $\text{hl} = \text{high} - \text{low}$
  - $\text{emaHL} = \text{ta.ema}(\text{hl}, \text{emaLen})$
  - $\text{cv} = \text{emaHL}[\text{rocLen}] == 0 ? 0 : 100 \cdot (\text{emaHL} - \text{emaHL}[\text{rocLen}]) / \text{emaHL}[\text{rocLen}]$
  - $\text{expand} = \text{cv} > \text{cv}[1]$
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - Prefer **$(\text{emaLen}=10, \text{rocLen}=10, \text{dirLen}=1)$**.
  - $\ne$ ATR%ile / $\ne$ Mass Index / $\ne$ VPCI / $\ne$ ATR-slope-alone.
- **Mode A (BTC-LEAD lean):**
  - Long entry: rising edge of $(\text{expand} \land \text{bull})$ (i.e. $\text{expand} \land \text{bull} \land \neg(\text{expand}[1] \land \text{bull}[1])$)
  - Exit: when $\neg(\text{expand} \land \text{bull})$ (or ATR trail stop)
- **Mode B (Positive Volatility Filter):**
  - Require $\text{cv} > 0 \land \text{expand} \land \text{bull}$ — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep: $\text{emaLen} \in \{10, 14\}$, $\text{rocLen} \in \{5, 10\}$, $\text{dirLen} \in \{1, 3\}$
- Primary grid:
  1. `mode_a|(ema10,roc10,dir1)` (preferred)
  2. `mode_a|(ema14,roc10,dir1)`
  3. `mode_a|(ema10,roc5,dir1)`
  4. `mode_b|(ema10,roc10,dir1,cv0)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{emaLen} \in \{10, 14\}$, $\text{rocLen} \in \{5, 10\}$, $\text{dirLen} \in \{1, 3\}$; $\text{emaLen} > 25$ forbidden (over-damp). ATR%ile / Mass / Chandelier substitute fails. Prefer Mode A (10,10,1), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $\text{emaLen} \le 3$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`outside-bar-polarity`)

### 3.1 Formulation
- **Outside Bar — Quantified Range-Engulf Polarity:**
  - $\text{outside} = \text{high} > \text{high}[1] \land \text{low} < \text{low}[1]$
  - $\text{mid} = \text{low} + \text{midFrac} \cdot (\text{high} - \text{low})$ (default $0.5 \to (\text{high} + \text{low}) / 2$)
  - $\text{bullOut} = \text{outside} \land \text{close} > \text{mid}$
  - $\text{bearOut} = \text{outside} \land \text{close} < \text{mid}$
  - Prefer **raw Mode A**.
  - $\ne$ Heikin-Ashi bias / $\ne$ HHLL multi-pivot BOS / $\ne$ body-engulfing.
- **Mode A (BTC-LEAD lean):**
  - Long entry: rising edge of $\text{bullOut}$ (i.e. $\text{bullOut} \land \neg\text{bullOut}[1]$)
  - Exit: on $\text{bearOut} \lor (\text{outside} \land \text{close} \le \text{mid})$ (or ATR trail stop)
- **Mode B (Follow-through Filter):**
  - Require $\text{close} > \text{high}[1]$ follow-through on bull outside — only if Mode A over-whips; identical params across all four coins.

### 3.2 Locked Parameter Space
- Sweep: $\text{midFrac} \in \{0.5, 0.6\}$, $\text{confirmBars} \in \{1, 2\}$
- Primary grid:
  1. `mode_a|(mid0.5,conf1)` (preferred)
  2. `mode_a|(mid0.6,conf1)`
  3. `mode_a|(mid0.5,conf2)`
  4. `mode_b|(mid0.5,conf1,follth)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{midFrac} \in \{0.5, 0.6\}$, $\text{confirmBars} \in \{1, 2\}$; $\text{confirmBars} > 3$ forbidden. HA / HHLL / body-engulf substitute fails. Prefer Mode A raw bullOut, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m outside spam forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`ulcer-index-recover-dir`)

### 4.1 Formulation
- **Peter Martin Ulcer Index — Recover $\times$ Close-Direction:**
  - $\text{hh} = \text{ta.highest}(\text{close}, \text{uiLen})$
  - $\text{pd} = \text{hh} == 0 ? 0 : 100 \cdot (\text{close} - \text{hh}) / \text{hh}$
  - $\text{ui} = \sqrt{\text{ta.sma}(\text{pd}^2, \text{uiLen})}$
  - $\text{recover} = \text{ui} < \text{ui}[1]$
  - $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - Prefer **$(\text{uiLen}=14, \text{dirLen}=1)$**.
  - $\ne$ Mass Index / $\ne$ ATR%ile / $\ne$ VHF / $\ne$ RAVI.
- **Mode A (Pain-Easing Recovery Lean):**
  - Long entry: rising edge of $(\text{recover} \land \text{bull})$ (i.e. $\text{recover} \land \text{bull} \land \neg(\text{recover}[1] \land \text{bull}[1])$)
  - Exit: when $\neg(\text{recover} \land \text{bull}) \lor \text{ui} > \text{ui}[1]$ (or ATR trail stop)
- **Mode B (UI $\times$ SMA Crossunder):**
  - $\text{sig} = \text{ta.sma}(\text{ui}, \text{smaLen})$; long on $\text{crossunder}(\text{ui}, \text{sig}) \land \text{bull}$ — only if Mode A over-whips; identical params across all four coins.

### 4.2 Locked Parameter Space
- Sweep: $\text{uiLen} \in \{10, 14, 20\}$, $\text{dirLen} \in \{1, 3\}$, $\text{smaLen} \in \{0, 5\}$
- Primary grid:
  1. `mode_a|(ui14,dir1)` (preferred)
  2. `mode_a|(ui10,dir1)`
  3. `mode_a|(ui20,dir1)`
  4. `mode_b|(ui14,dir1,sma5)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{uiLen} \in \{10, 14, 20\}$, $\text{dirLen} \in \{1, 3\}$, $\text{smaLen} \in \{0, 5\}$; $\text{uiLen} > 35$ forbidden (over-damp). Mass / ATR%ile / VHF / RAVI substitute fails. Prefer Mode A (14,1), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $\text{uiLen} \le 5$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Dropped Strategy 4 (`parkinson-vol-expansion-dir`)

### 5.1 Formulation & Drop Decision Rationale
- **Formulation:**
  - $\text{lr2} = \ln(\text{high} / \text{low})^2$
  - $\text{park} = \sqrt{\text{ta.sma}(\text{lr2}, \text{nPark}) / (4 \ln 2)}$
  - $\text{expand} = \text{park} > \text{park}[1]$; $\text{bull} = \text{close} > \text{close}[\text{dirLen}]$
  - Mode A: rising edge of $(\text{expand} \land \text{bull})$
- **Drop Justification:**
  - Empirically compared on 2.5y BTCUSDT (1h and 4h) against Strategy 1 (`chaikin-volatility-dir`).
  - Both indicators measure range-volatility expansion coupled with close direction.
  - On 1H BTC: 75.2% buy signal overlap (2967 joint / 3943 Chaikin), 816 trades (-89.27% ret) vs 771 trades (-88.91% ret).
  - On 4H BTC: 78.4% buy signal overlap (766 joint / 977 Chaikin), 193 trades (-56.36% ret) vs 187 trades (-53.17% ret).
  - Both suffer from identical whipsaw under costs during chop.
  - **Verdict:** Per authoritative brief instruction, Strategy 4 is **DROPPED** to avoid dual encoding of redundant range-vol expansion behaviors. Strategy 1 (`chaikin-volatility-dir`) is kept.

---

## 6. Locked Strategy 5 (`inside-bar-breakout`)

### 6.1 Formulation
- **Inside Bar — Mother-Bar High/Low Close Breakout:**
  - $\text{inside} = \text{high} < \text{high}[1] \land \text{low} > \text{low}[1]$
  - On inside bar: $\text{motherH} = \text{high}[1]$, $\text{motherL} = \text{low}[1]$, $\text{armed} = \text{cancelBars}$
  - Each subsequent bar if $\text{armed} > 0$: $\text{armed} \leftarrow \text{armed} - 1$
  - Prefer **$\text{cancelBars}=5$**.
  - $\ne$ HHLL multi-pivot BOS / $\ne$ Donchian long-channel ($N \ge 20$) / $\ne$ NR7 / $\ne$ Heikin-Ashi.
- **Mode A (BTC-LEAD Compression Breakout Lean):**
  - Long entry: when $\text{armed} > 0 \land \text{close} > \text{motherH} \land \neg(\text{close}[1] > \text{motherH})$ (rising-edge break)
  - Exit: when $\text{close} < \text{motherL}$ (breakout failure) (or ATR trail stop). Clear arm after fill.
- **Mode B (Mother Range ATR Filter):**
  - Require mother range $(\text{motherH} - \text{motherL}) \ge k \cdot \text{ta.atr}(\text{atrLen})$ (skip tiny mothers) — only if Mode A over-whips; identical params across all four coins.

### 6.2 Locked Parameter Space
- Sweep: $\text{cancelBars} \in \{3, 5, 8\}$, $k \in \{0.0, 0.5\}$
- Primary grid:
  1. `mode_a|(cancel5,k0.0)` (preferred)
  2. `mode_a|(cancel3,k0.0)`
  3. `mode_a|(cancel8,k0.0)`
  4. `mode_b|(cancel5,k0.5)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{cancelBars} \in \{3, 5, 8\}$, $k \in \{0.0, 0.5\}$; $\text{cancelBars} > 15$ forbidden. HHLL / Donchian / NR7 / HA substitute fails. Prefer Mode A cancelBars=5, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** 15m $\text{cancelBars} \le 1$ forbidden. Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 7. Stop-Ladder Summary & Cell Count

With Parkinson (#4) dropped, the active ladder evaluates **4 strategies**:
- 4 strategies $\times$ 2 timeframes (1h, 4h) $\times$ 4 parameter sets = **32 candidate cells per coin**.
- BTC Step 1: 32 cells evaluated.
- ETH Step 2: only cells passing BTC (6m return $\ge 1.2\times$ B&H and $n > 5$) advance.
- SOL Step 3: only cells passing ETH advance.
- BNB Step 4: only cells passing SOL advance.
