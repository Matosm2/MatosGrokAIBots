# stage31-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND INDEPENDENT SCORING  
**Date (UTC):** 2026-09-22  
**Research ID:** `stage31-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage30 wipe (`apirine-ma-bands-break` @4h Mode A BTC 1.520× thin-n=8 -> ETH wipe). Track 2 Discord OFF-LIMITS.  
**Authoritative Kick:** `CODING_KICK.md` (uploads/CODING_KICK_86a8.md)  
**Formula Briefs:** `stage31-dual-sol-bnb-briefs-2026-09-22.md` (uploads/stage31-dual-sol-bnb-briefs-2026-09-22_1577.md)  
**Mid-Encode Gate Patch (Strategy Bot / Nuno):** Denser floor tightened from n≥20 to n≥40.

---

## 1. NEW PER-COIN GATE (Nuno 2026-09-22 + Mid-Encode Patch)

Replaces full-ladder PASS requirement for paper eligibility:
- **Score BTC / ETH / SOL / BNB independently.**
- **Coin PASS (paper-eligible) iff Mode-A ≥ 1.2× B&H on that coin AND denser sample n ≥ 40.**
- **Thin n < 40 → ineligible for paper even if × ≥ 1.2 (flag THIN clearly).**
- Multiple strategies OK — best eligible per coin.
- **Do NOT kill a seat only because it fails another coin** (e.g. BTC PASS + ETH FAIL still reports BTC PASS).
- Full-ladder no longer required for paper.
- Prefer dense BTC lead when ranking / sweep priority, but **per-coin scoring is authoritative**.
- LIVE still NO. No merge / no paper / no live. Hold open draft PR.

---

## 2. Governance & Methodological Hygiene

- **4 Locked Strategies (Non-Clone Families):**
  1. `apirine-sdo-zero-cross` (Vitali Apirine Stochastic Distance Oscillator zero-cross)
  2. `ehlers-madh-zero-cross` (John Ehlers Moving Average Difference Hann zero-cross)
  3. `premier-stochastic-osc-zero` (Lee Leibfarth Premier Stochastic Oscillator zero-cross)
  4. `apirine-tradj-ema-cross` (Vitali Apirine True Range Adjusted EMA × same-length EMA cross)
- **Track B Hard Ban Honored:** Do NOT encode or clone Chande-Kroll, QQE, MAMA×FAMA, or Wilder Volatility System (ARC-SAR), which are owned by parallel Track B optimize (`stage23-chande-kroll-optimize-v1`).
- **Hard Excludes:** All stage 1–30 IDs (all), including stage30 DTI/VAMA/MAB/RMO, stage29 Stiffness/CPR/DVS/HVR, stage28 EC/Vervoort/ZL-FIR/DV2, stage27 Qstick/Klinger/%Envelopes/Schwager-VR, stage26 FVE/Convolution/HT_TRENDLINE/SafeZone, stage25 DSP/NHNL/VROC/Elder-thermo, and earlier stages.
- **Execution:** Closed-bar only (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Data:** Autonomous offline OHLCV via Binance Spot public klines (1h and 4h).

---

## 3. Locked Strategy 1 (`apirine-sdo-zero-cross`)

### 3.1 Formulation
- Vitali Apirine (*Stochastic Distance Oscillator*, TASC Jun 2023):
  - `Dist = |Close − Close[n]|`
  - `%D = (Dist − LLV(Dist, LB)) / (HHV(Dist, LB) − LLV(Dist, LB)) · 100`
  - `signed = Close > Close[n] ? %D : Close < Close[n] ? −%D : 0`
  - `SDO = EMA(signed, Pds)`
  - Mode A: `crossover(sdo, 0)` long, `crossunder(sdo, 0)` exit.
  - Mode B: require `sdo > sdo[1]` rising on entry.
  - Preferred default: **(n=14, LB=100, Pds=3)** Mode A.
  - $\ne$ classic Stoch (close vs HH/LL range), $\ne$ Apirine MAB band-break, $\ne$ RMI/TII.

### 3.2 Locked Parameter Space
- Sweep: $n \in \{8, 14, 20, 40\}$; $LB \in \{50, 100, 200\}$; $Pds \in \{3, 5, 6\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(n14,lb100,pds3)` (preferred default)
  2. `mode_a|(n8,lb50,pds3)`
  3. `mode_a|(n14,lb50,pds3)`
  4. `mode_a|(n20,lb100,pds5)`
  5. `mode_a|(n40,lb200,pds6)`
  6. `mode_b|(n14,lb100,pds3,rising)`

---

## 4. Locked Strategy 2 (`ehlers-madh-zero-cross`)

### 4.1 Formulation
- John Ehlers (*Moving Average Difference Hann*, TASC Nov 2021):
  - Hann weights: $w(i) = 1 − \cos(2\pi i / (L + 1))$ for $i = 1 \dots L$
  - $Filt1 = \sum(w \cdot Close) / \sum(w)$ over $ShortLength$
  - $LongLength = \lfloor ShortLength + DominantCycle / 2 \rfloor$
  - $Filt2 = \sum(w \cdot Close) / \sum(w)$ over $LongLength$
  - $MADH = 100 \cdot (Filt1 − Filt2) / Filt2$
  - Mode A: `crossover(madh, 0)` long, `crossunder(madh, 0)` exit.
  - Mode B: require `madh > madh[1]` rising on entry.
  - Preferred default: **(ShortLength=8, DominantCycle=27)** Mode A ($LongLength=21$).
  - $\ne$ MACD (EMA−EMA), $\ne$ ZL-FIR×price, $\ne$ BandPass, $\ne$ RMO, $\ne$ PPO.

### 4.2 Locked Parameter Space
- Sweep: $Short \in \{6, 8, 10\}$; $Dom \in \{20, 27, 34\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(s8,dom27)` (preferred default)
  2. `mode_a|(s6,dom20)`
  3. `mode_a|(s8,dom20)`
  4. `mode_a|(s10,dom34)`
  5. `mode_b|(s8,dom27,rising)`

---

## 5. Locked Strategy 3 (`premier-stochastic-osc-zero`)

### 5.1 Formulation
- Lee Leibfarth (*Premier Stochastic Oscillator*, TASC Aug 2008):
  - $Stoch = 100 \cdot (Close − LLV(Low, Period)) / (HHV(High, Period) − LLV(Low, Period))$
  - $N = 0.1 \cdot (Stoch − 50)$
  - $S = EMA(EMA(N, Smooth), Smooth)$
  - $PSO = (\exp(S) − 1) / (\exp(S) + 1)$
  - Mode A: `crossover(pso, 0)` long, `crossunder(pso, 0)` exit.
  - Mode B: require prior $PSO < -0.20$ within 5 bars before crossing up through 0.
  - Preferred default: **(Period=8, Smooth=5)** Mode A.
  - $\ne$ classic Stoch %K/%D, $\ne$ InverseFisherRSI, $\ne$ QQE, $\ne$ SMI.

### 5.2 Locked Parameter Space
- Sweep: $Period \in \{5, 8, 14\}$; $Smooth \in \{3, 5, 8\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(per8,sm5)` (preferred default)
  2. `mode_a|(per5,sm3)`
  3. `mode_a|(per8,sm3)`
  4. `mode_a|(per14,sm8)`
  5. `mode_b|(per8,sm5,dip-0.2)`

---

## 6. Locked Strategy 4 (`apirine-tradj-ema-cross`)

### 6.1 Formulation
- Vitali Apirine (*True Range Adjusted EMA*, TASC Jan 2023):
  - $TR = TrueRange(High, Low, Close)$
  - $TRAdj = (TR − LLV(TR, Pds)) / (HHV(TR, Pds) − LLV(TR, Pds))$
  - $Rate = (2 / (Periods + 1)) \cdot (1 + TRAdj \cdot Mltp)$
  - $TRAdjEMA = TRAdjEMA[1] + Rate \cdot (Close − TRAdjEMA[1])$
  - Reference EMA: $EMA(Close, Periods)$
  - Mode A: `crossover(tradjEma, emaRef)` long, `crossunder(tradjEma, emaRef)` exit.
  - Mode B: require `close > emaRef` on entry.
  - Preferred default: **(Periods=20, Pds=20, Mltp=5)** Mode A.
  - $\ne$ Apirine MAB, $\ne$ VIDYA, $\ne$ KAMA, $\ne$ BB, $\ne$ Track-B.

### 6.2 Locked Parameter Space
- Sweep: $Periods \in \{10, 20, 40\}$; $Pds \in \{10, 20, 40\}$; $Mltp \in \{5, 8, 10\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(p20,pds20,m5)` (preferred default)
  2. `mode_a|(p10,pds10,m5)`
  3. `mode_a|(p20,pds10,m8)`
  4. `mode_a|(p40,pds40,m10)`
  5. `mode_b|(p20,pds20,m5,close_gate)`

---

## 7. Scoring & Evaluation Matrix

- **Autonomous Independent Scoring:** Every strategy cell is scored across all 4 coins (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT) on 1H and 4H timeframes.
- **PASS_coin:** $Mode\text{-}A \ge 1.2\times B\&H$ on that coin **AND** $n \ge 40$.
- **THIN Flag:** If $\times \ge 1.2$ but $n < 40$, marked as `THIN` (ineligible for paper).
- **Full(~2y) & Ops 2.5%:** Reported alongside 6m Mode-A for complete operational visibility.
