# stage17-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage17-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage16 (Kagi BTC->ETH clear -> SOL 0.807x under-gate fail). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_cfcc.md` & `stage17-dual-sol-bnb-briefs-2026-09-18_5d0e.md`

---

## 1. Governance & Methodological Hygiene

To enforce **SOL >= 1.2x after BTC->ETH clear PRIMARY** + **Denser $n \gg 9$** + **BNB-Survival after 3-coin clear** per Path B Stage 17 directives:
- **SOL >= 1.2x PRIMARY CHOKE (Kagi Lesson):** In Stage 16, `nison-kagi-yang-yin-flip` achieved the cleanest BTC->ETH portability seen across recent stages (BTC 1.202x -> ETH 2.099x), but then stalled at SOL 0.807x (under the 1.2x gate). Prior failure modes: Stage 12/15 over-damp (0 BTC); Stage 13 BTC clear then ETH wipe; Stage 14 TTF 3-coin clear then BNB quiet wipe; Stage 16 BTC+ETH clear then SOL choke. Stage 17 prioritizes responsive candle-bias, deviation-oscillator, double-smoothed stochastic, intensity-flow, and predictive-trigger encodes that avoid structure-clone stalls on impulsive SOL.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$) and Stage 8 PGO ($n \approx 9$), without stage12/15 over-damp collapse.
- **BTC->ETH Portability Preservation:** Strategies must demonstrate cross-coin portability on ETH without per-coin retuning.
- **BNB-Survival (CRITICAL after 3-coin clear):** Withstand quieter BNB regime without quiet wipe (Stage 14 TTF lesson). Mode B parameters or ATR protection must prevent quiet wipes without breaking BTC/ETH/SOL.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially lengthening lookback only on BNB after SOL) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD — Kagi choke) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if parameter inflation collapses BTC $n$; Kill if HA-streak N>=3 or raw Stoch or free WMA dual substituted; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH wipes (stage13 REI pattern); Kill if parameters or mode retuned only on ETH; Kill if CSI/CLV/Stoch graft.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH CRITICAL (Kagi lesson):** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if 15m spam; Kill if stage12-16 grafts; Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **CRITICAL after BTC+ETH+SOL (TTF lesson):** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; per-coin volume/length retune. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–16 IDs (all), including BandPass/2pole-HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, stage12 smoother class, Super Passband, RWI, Reverse EMA, PGO, PSY, Disparity, WaveTrend, RMI, AccelBands, TII, Rainbow, Dorsey RelVol, TCF, DEMA dual, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian, PMO.

---

## 2. Locked Strategy 1 (`heikin-ashi-bias-flip`)

### 2.1 Formulation
- **Heikin-Ashi Bias Flip (Candle-transform polarity rule):**
  - $\text{HA\_Close} = (\text{Open} + \text{High} + \text{Low} + \text{Close}) / 4$
  - $\text{HA\_Open} = (\text{HA\_Open}[1] + \text{HA\_Close}[1]) / 2$ (seed: $(\text{Open}[0] + \text{Close}[0]) / 2$)
  - $\text{bull} = \text{HA\_Close} > \text{HA\_Open}$
  - Recurse on closed OHLC (`var`) — do NOT switch chart type as data source.
- **Mode A (BTC-LEAD + SOL-dense PRIMARY — prefer first):**
  - Long entry: $\text{bull} \land \neg\text{bull}[1]$ ($\text{confirm}=1$)
  - Exit: $\neg\text{bull} \land \text{bull}[1]$ (or ATR trail stop)
- **Mode B (BNB quiet / SOL chatter):**
  - Long entry: 2 consecutive bull bars ($\text{confirm}=2$)
  - Exit: 2 consecutive bear bars
  - Only if Mode A over-whips; identical confirm ($\ne$ HA-streak $N \ge 3$ as Mode A).

### 2.2 Locked Parameter Space
- Sweep: $\text{confirm} \in \{1, 2\}$, optional ATR trail mult $\in \{0.0, 2.0\}$
- Primary grid:
  1. `mode_a|(confirm1)` (preferred)
  2. `mode_b|(confirm2)`
  3. `mode_a|(confirm1,atr2.0)`
  4. `mode_b|(confirm2,atr2.0)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $\text{confirm} \in \{1, 2\}$; $\text{confirm} \ge 3$ is forbidden HA-streak. Mode B forced while Mode A BTC healthy fails. Prefer Mode A $\text{confirm}=1$, 1H+.
- **eth_smoke:** $\text{confirm} \in \{1, 2\}$; retuning only on ETH fails. Kagi/3LB substitute fails.
- **sol_smoke:** 15m spam forbidden. $\text{confirm} \in \{1, 2\}$; retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical confirm across all coins. Mode B shorts ungated fails.

---

## 3. Locked Strategy 2 (`blau-ergodic-mdi-signal-cross`)

### 3.1 Formulation
- **Blau Ergodic Mean Deviation Index (Ergodic MDI x Signal):**
  - $md = \text{close} - \text{ema}(\text{close}, r)$
  - $mdi = \text{ema}(\text{ema}(md, s), u)$
  - $sig = \text{ema}(mdi, ul)$
  - Prefer **$(r=20, s=5, u=3, ul=3)$**.
  - Distinct Blau mean-deviation family: $\ne$ CSI (stage 12), $\ne$ TSI (burned).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(mdi, sig)$
  - Exit: $\text{crossunder}(mdi, sig)$ (or ATR stop)
- **Mode B (BNB quiet / Mode A+ zero-bias):**
  - Long entry: $\text{crossover}(mdi, sig) \land mdi > 0$
  - Exit: $\text{crossunder}(mdi, sig)$ (or ATR stop)

### 3.2 Locked Parameter Space
- Sweep: $r \in \{14, 20, 28\}$, $s \in \{3, 5\}$, $ul \in \{3, 5\}$ (fixed $u=3$)
- Primary grid:
  1. `mode_a|(r20,s5,u3,ul3)` (preferred)
  2. `mode_a|(r14,s5,u3,ul3)`
  3. `mode_a|(r28,s5,u3,ul3)`
  4. `mode_b|(r20,s5,u3,ul3)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $r \in \{14, 20, 28\}$; $r > 35$ collapses BTC $n$. CSI/TSI substitute fails. Mode B forced while Mode A BTC healthy fails. Prefer Mode A $(20, 5, 3, 3)$, 1H+.
- **eth_smoke:** Retuning only on ETH fails; CSI graft fails.
- **sol_smoke:** 15m $r \le 5$ spam fails; CSI/TSI/BandPass labeled MDI fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Different $(r, s, u, ul)$ than SOL fails; per-coin retune fails.

---

## 4. Locked Strategy 3 (`dss-bressert-trigger-cross`)

### 4.1 Formulation
- **Double Smoothed Stochastic (DSS Bressert x Trigger):**
  - $pre = \text{ema}(\text{stoch}(\text{close}, \text{high}, \text{low}, PDS), EMAlen)$
  - $dss = \text{ema}(\text{stoch}(pre, pre, pre, PDS), EMAlen)$
  - $trig = \text{ema}(dss, TriggerLen)$
  - Prefer **$(PDS=10, EMAlen=9, TriggerLen=5)$**.
  - Double-smoothed stochastic of a stochastic: $\ne$ raw Stoch K/D, $\ne$ SMI, $\ne$ TMO, $\ne$ Dorsey RelVol.
- **Mode A (BTC-LEAD + SOL-dense PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(dss, trig)$
  - Exit: $\text{crossunder}(dss, trig)$ (or ATR stop)
- **Mode B (BNB quiet / 20-80 band):**
  - Long entry: $\text{crossover}(dss, trig) \land dss < 20$
  - Exit: $\text{crossunder}(dss, trig) \lor dss > 80$

### 4.2 Locked Parameter Space
- Sweep: $PDS \in \{8, 10, 14\}$, $TriggerLen \in \{3, 5\}$ (fixed $EMAlen=9$)
- Primary grid:
  1. `mode_a|(PDS10,EMA9,Trig5)` (preferred)
  2. `mode_a|(PDS8,EMA9,Trig5)`
  3. `mode_a|(PDS14,EMA9,Trig5)`
  4. `mode_b|(PDS10,EMA9,Trig5)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $PDS \in \{8, 10, 14\}$; $PDS > 20$ collapses BTC $n$. Raw Stoch substitute fails. Mode B 20/80 forced while Mode A BTC healthy fails. Prefer Mode A $(10, 9, 5)$, 1H+.
- **eth_smoke:** Retuning only on ETH fails; Stoch K/D graft fails.
- **sol_smoke:** 15m $PDS \le 3$ spam fails; Stoch/SMI/TMO labeled DSS fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Different $PDS/EMA/Trigger$ than SOL fails; Mode B shorts ungated fails.

---

## 5. Locked Strategy 4 (`bostian-iii-sma-zero`)

### 5.1 Formulation
- **Bostian Intraday Intensity Index (III SMA Zero-Cross):**
  - $rng = \text{high} - \text{low}$
  - $iii = 0.0$ if $rng == 0$ else $((2\cdot\text{close} - \text{high} - \text{low}) / rng) \cdot \text{volume}$
  - $iiiS = \text{sma}(iii, smaLen)$
  - Prefer **$smaLen=21$**.
  - Signed close-location $\times$ volume: $\ne$ CMF, $\ne$ OBV, $\ne$ CLV $\times$ SMA (stage 13), $\ne$ AccDist (stage 1).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(iiiS, 0)$
  - Exit: $\text{crossunder}(iiiS, 0)$ (or ATR stop)
- **Mode B (BNB quiet / quality hold):**
  - Long entry: $\text{crossover}(iiiS, 0) \land iiiS > 0$
  - Exit: $\text{crossunder}(iiiS, 0)$ (or ATR stop)

### 5.2 Locked Parameter Space
- Sweep: $smaLen \in \{10, 14, 21, 34\}$
- Primary grid:
  1. `mode_a|(sma21)` (preferred)
  2. `mode_a|(sma14)`
  3. `mode_a|(sma34)`
  4. `mode_b|(sma21)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $smaLen \in \{10, 14, 21, 34\}$; $smaLen > 50$ collapses BTC $n$. CMF/OBV/CLV substitute fails. Mode B forced while Mode A BTC healthy fails. Prefer Mode A $smaLen=21$, 1H+.
- **eth_smoke:** Retuning only on ETH fails; CLV graft fails.
- **sol_smoke:** Per-coin volume retune fails; CMF/OBV/CLV labeled III fails; 15m $smaLen \le 3$ spam fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Different $smaLen$ than SOL fails; per-coin volume retune fails.

---

## 6. Locked Strategy 5 (`ehlers-predictive-ma-cross`)

### 6.1 Formulation
- **Ehlers Predictive Moving Average (Fixed 7/7/4 Predict x Trigger):**
  - $w_1 = \text{wma}(src, 7)$
  - $w_2 = \text{wma}(w_1, 7)$
  - $predict = 2\cdot w_1 - w_2$
  - $trigger = \text{wma}(predict, 4)$
  - Prefer **close + 7/7/4 locked**.
  - Fixed Rocket-Science construction: $\ne$ free WMA dual (stage 8), $\ne$ ZLEMA $\times$ SMA (stage 4).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(predict, trigger)$
  - Exit: $\text{crossunder}(predict, trigger)$ (or ATR stop)
- **Mode B (BNB quiet / 2-bar hold):**
  - Long entry: $\text{crossover}(predict, trigger) \land (predict > trigger \text{ hold 2 bars})$
  - Exit: $\text{crossunder}(predict, trigger)$ (or ATR stop)

### 6.2 Locked Parameter Space
- Sweep: $src \in \{\text{close}, \text{hl2}\}$, optional $triggerLen \in \{3, 4, 5\}$
- Primary grid:
  1. `mode_a|(close,7/7/4)` (preferred)
  2. `mode_a|(hl2,7/7/4)`
  3. `mode_a|(close,7/7/3)`
  4. `mode_b|(close,7/7/4)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $wmaLen=7$ locked; $triggerLen \in \{3, 4, 5\}$; $src \in \{\text{close}, \text{hl2}\}$. Free WMA dual fails. Mode B forced while Mode A BTC healthy fails. Prefer Mode A 7/7/4 close, 1H+.
- **eth_smoke:** Lengths retuned only on ETH fails; WMA dual graft fails.
- **sol_smoke:** Free WMA dual / ZLEMA labeled PMA fails; 15m WMA(3) spam fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Different lengths than SOL fails; per-coin retune fails.

---

## 7. Complete Grid Matrix & Stop-Ladder Execution

### 7.1 Grid Topology
- 5 strategies $\times$ 4 parameter sets $\times$ 2 timeframes (1H, 4H) = **40 cells per symbol**.
- 4 symbols in sequence: **BTCUSDT $\to$ ETHUSDT $\to$ SOLUSDT $\to$ BNBUSDT** (160 total cells).
- Only cells that achieve `gate_6m == "PASS"` ($\text{return} \ge 1.2\times\text{B\&H}$ and $n > 5$) on the current symbol are promoted to the next symbol in the ladder.
- All non-promoted cells on subsequent symbols are recorded with status `N/A` and marked as pruned by the stop ladder.
- Dual-survival requirement: identical parameter specifications across all evaluated symbols.

---
*Signed and locked before scoring: 2026-09-18 (Track 1 Path B)*
