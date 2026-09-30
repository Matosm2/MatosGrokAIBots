# stage29-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-21  
**Research ID:** `stage29-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage28 wipe (closest Vervoort@4h 0.832x; still short of FVE 1.055x / 1.20; BTC 0/32 FAIL LEAD). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_21ca.md` & `stage29-dual-sol-bnb-briefs-2026-09-21_423f.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY CRITICAL** (clear past Vervoort 0.832x / FVE 1.055x to >= 1.20 without over-damp) + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **ETH denser n >> 9 portability** + **SOL-after-BTC+ETH** + **BNB-survival after 3-coin** per Path B Stage 29 directives:
- **BTC LEAD PRIMARY CRITICAL:** In Stage 28, `vervoort-zlha-typ-cross` reached 0.832x @ 4h, still short of Stage 26 FVE's 1.055x and 1.20 gate, while EC/FIR/DV2 suffered cost chop, leaving BTC 0/32 FAIL LEAD across the pack. In Stage 29, we lock four distinct, non-clone published families outside stage 1–28 + remaining parks (Katsanos Stiffness, Central Pivot Range break-accept, Varadi DVS stretch midline reclaim, Historical Volatility Ratio expand x dir) that can clear BTC Mode-A >= 1.20 without over-damping to 0-BTC.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser n >> 9 Policy:** Ensure trade density remains well above the thin counts of Stage 25 NHNL (n=8), Stage 14 TTF (n=6..10), Stage 8 PGO (n ≈ 9), and thin n <= 5 structure stalls, while avoiding parameter over-inflation that collapses BTC n.
- **Tiny-n Policy (Critical):** If Mode-A BTC n <= 5 on 6m -> FAIL that cell even if xB&H >= 1.2 (hard-fail cell as over-gated / under-specified). Also flag n ≈ 9 (in range [6..10]) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return >= 1.2x B&H -> ETH (HARD, `eth_smoke`) -> SOL (HARD, `sol_smoke`) -> BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (clear past 0.832x / 1.055x / >= 1.20 / no 0-BTC / no VR 0.698x regress):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past 1.20 (FVE/Vervoort rhyme); Kill if parameters inflated until BTC n collapses; Kill if FVE/VFI/CHOP/ADX/floor-R1/Woodie/Camarilla/DVI/DV2/Parkinson/Schwager-VR substitute labeled seated strategies; Kill if Mode B forced while Mode A BTC n healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **ETH-after-BTC (no NHNL 1.687x -> 1.085x wipe / no thin n ≈ 8):** Kill if BTC clears >= 1.2x then ETH under 1.2x; Kill if ETH n stays thin ~8; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH n multi-dozen (n >> 9).
  - `sol_smoke`: **SOL-AFTER-BTC+ETH (no Kagi / percentile 0.922x fail):** Kill if BTC+ETH clear >= 1.2x then SOL under 1.2x; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–28 grafts. Retention check: after ETH, SOL n must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL (no TTF / HHLL quiet wipe):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–28 IDs (all), including EC/Vervoort/ZL-FIR/DV2, Qstick/Klinger/%Envelopes/Schwager-VR, FVE/Convolution/HT_TRENDLINE/SafeZone, DSP/NHNL/VROC/Elder-thermo, Guppy-CBL/Kirshenbaum/IMI/Williams-AD, QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV, ZLEMA, EDCF filt*lag.

---

## 2. Locked Strategy 1 (`katsanos-stiffness-threshold`)

### 2.1 Formulation
- **Katsanos Stiffness (TASC Nov 2018):**
  - Markos Katsanos (*Stiffness Indicator*, TASC Nov 2018; mkatsanos.com; Thinkorswim; Traders' Tips Nov 2018).
  - `ma = SMA(Close, MAB)`
  - `sd = StDev(Close, MAB)`
  - `ma2 = ma - NSTD * sd`
  - `above = Close > ma2 ? 1.0 : 0.0`
  - `stif = 100.0 * Sum(above, Period) / Period`
  - `stiffness = EMA(stif, SM)`
  - Prefer **(MAB=100, Period=60, NSTD=0.2, SM=3, BuyThr=90, SellThr=50)**.
  - $\ne$ FVE (volume MF), $\ne$ VFI, $\ne$ CHOP, $\ne$ ADX, $\ne$ Qstick.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(stiffness, BuyThr)`
  - Exit: `crossunder(stiffness, SellThr)`
- **Mode B (Quality / Rising Confirmation Filter):**
  - Raise BuyThr (e.g. 95) and/or require rising stiffness `stiffness > stiffness[1]` — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep (LEAN): $MAB \in \{50, 100\}$; $Period \in \{40, 60, 80\}$; $BuyThr \in \{75, 90, 95\}$; $SellThr \in \{40, 50, 60\}$; TF 1H vs 4H. Mode A defaults first.
- Primary grid:
  1. `mode_a|(mab100,p60,nstd0.2,sm3,buy90,sell50)` (preferred)
  2. `mode_a|(mab50,p40,nstd0.2,sm3,buy90,sell50)`
  3. `mode_a|(mab100,p80,nstd0.2,sm3,buy90,sell50)`
  4. `mode_b|(mab100,p60,buy95,sell50)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $MAB \in \{50, 100\}$, $Period \in \{40, 60, 80\}$, $BuyThr \in \{75, 90, 95\}$, $SellThr \in \{40, 50, 60\}$ locked. Parameter inflation collapses BTC $n$ forbidden. FVE/VFI/CHOP/ADX substitute forbidden. Prefer Mode A (100, 60, 0.2, 3, 90, 50), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`cpr-range-break-accept`)

### 3.1 Formulation
- **Same-TF Lookback Central Pivot Range (CPR):**
  - Frank Ochoa (*Secrets of a Pivot Boss*); Quantzee; Groww; StockManiacs.
  - Rolling N lookback (no `request.security`):
    - `ph = highest(H, N)[1]`
    - `pl = lowest(L, N)[1]`
    - `pc = close[1]`
    - `P = (ph + pl + pc) / 3.0`
    - `BC = (ph + pl) / 2.0`
    - `TC = 2.0 * P - BC`
    - If `TC < BC`: swap(TC, BC) so TC >= BC
    - `cprW = TC - BC`
  - Prefer **N=24**.
  - $\ne$ Classic floor R1/S1 ladder ($R1=2P-L, S1=2P-H$), $\ne$ Camarilla, $\ne$ Woodie, $\ne$ HHLL BOS.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(close, TC)`
  - Exit: `crossunder(close, BC)`
- **Mode B (Narrow CPR Gate):**
  - Require narrow CPR (`cprW / P < narrowPct` where `narrowPct in {0.001, 0.002, 0.005}`) before TC break — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep (LEAN): $N \in \{12, 24, 48\}$; $narrowPct \in \{0.001, 0.002, 0.005\}$ if Mode B; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(N24)` (preferred)
  2. `mode_a|(N12)`
  3. `mode_a|(N48)`
  4. `mode_b|(N24,narrow0.002)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $N \in \{12, 24, 48\}$ locked. Floor R1/S1 / Camarilla / Woodie / HHLL substitute forbidden. Prefer Mode A N=24, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`varadi-dvs-stretch-midline`)

### 4.1 Formulation
- **Varadi DVS (Directional Volatility Stretch) Percent-Rank Midline Reclaim:**
  - David Varadi, CSS Analytics (July 31, 2009; Nov 2009), *DVI Part 1: The Stretch Indicator (DVS)*:
    - `ds = close > close[1] ? 1.0 : (close < close[1] ? -1.0 : 0.0)`
    - `sumDS = sum(ds, sumLen)`
    - `raw = 0.5 * (sumDS + sumDS[1])`
    - `dvs = 100.0 * percentrank(raw, rankLen)`
  - Prefer **sumLen=20, rankLen=100, mid=50.0**.
  - Trend-port mid-reclaim — not fade DVS < 20.
  - $\ne$ DVI (composite magnitude+stretch), $\ne$ DV2 (close/(high+low)), $\ne$ PSY midline.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(dvs, 50)`
  - Exit: `crossunder(dvs, 50)`
- **Mode B (Reclaim Through 40 Filter):**
  - Long entry: reclaim through 40 (`crossover(dvs, 40)`), exit at 50 (`crossunder(dvs, 50)`) — only if Mode A under-fires; identical across all four — still not fade-short primary.

### 4.2 Locked Parameter Space
- Sweep (LEAN): $sumLen \in \{10, 20, 40\}$; $rankLen \in \{63, 100, 126, 252\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(sum20,rank100,mid50)` (preferred)
  2. `mode_a|(sum10,rank63,mid50)`
  3. `mode_a|(sum40,rank126,mid50)`
  4. `mode_b|(sum20,rank100,rec40_exit50)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $sumLen \in \{10, 20, 40\}$, $rankLen \in \{63, 100, 126, 252\}$ locked. DVI/DV2/PSY substitute forbidden. Mode B fade-shorts forced forbidden. Prefer Mode A sumLen=20 rankLen=100 mid-50, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`historical-volatility-ratio-expand-dir`)

### 5.1 Formulation
- **Close-to-Close Historical Volatility Ratio Expand x Close Direction:**
  - TC2000 / Sierra Chart / Investopedia Historical Volatility literature:
    - `lr = ln(close / close[1])`
    - `hvS = stdev(lr, shortLen)`
    - `hvL = stdev(lr, longLen)`
    - `hvr = hvS / hvL`
  - Prefer **(short=10, long=100, ExpandThr=0.5, dirLen=5)**.
  - $\ne$ Schwager VR (Japanese True-Range VR / Donchian), $\ne$ Parkinson ln(H/L) RMS, $\ne$ Chaikin Volatility (% change EMA(H-L)), $\ne$ ATR-ratio.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(hvr, ExpandThr) and close > close[dirLen]`
  - Exit: `crossunder(hvr, ExpandThr) or close < close[dirLen]`
- **Mode B (Prior Compression Filter):**
  - Require prior compression `hvr[1] < CompThr` (e.g. 0.5) before expand crossover — only if Mode A over-whips; identical across all four.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $shortLen \in \{6, 10, 14\}$; $longLen \in \{50, 100\}$; $ExpandThr \in \{0.4, 0.5, 0.6\}$; $dirLen \in \{3, 5, 8\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(s10,l100,exp0.5,dir5)` (preferred)
  2. `mode_a|(s6,l50,exp0.4,dir3)`
  3. `mode_a|(s14,l100,exp0.6,dir8)`
  4. `mode_b|(s10,l100,exp0.5,dir5,comp0.5)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $shortLen \in \{6, 10, 14\}$, $longLen \in \{50, 100\}$, $ExpandThr \in \{0.4, 0.5, 0.6\}$, $dirLen \in \{3, 5, 8\}$ locked. Schwager VR / Parkinson / Chaikin / ATR-ratio substitute forbidden. Prefer Mode A (10, 100, 0.5, 5), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail. Denser $n \gg 9$ required.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 6. Execution Grid & Summary Matrix

| Strategy ID | Family | Primary Parameters | Timeframes | Primary Gate Metric |
| :--- | :--- | :--- | :--- | :--- |
| `katsanos-stiffness-threshold` | Trend-quality stiffness count | MAB=100, Period=60, NSTD=0.2, SM=3, BuyThr=90, SellThr=50 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |
| `cpr-range-break-accept` | Central Pivot Range TC/BC accept | N=24, Mode A (TC break) | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |
| `varadi-dvs-stretch-midline` | DVS stretch percent-rank reclaim | sumLen=20, rankLen=100, mid=50.0 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |
| `historical-volatility-ratio-expand-dir` | Close-to-close HVR expand $\times$ dir | short=10, long=100, ExpandThr=0.5, dirLen=5 | 1H, 4H | 6m Mode-A $\ge 1.2\times$ B&H, $n > 5$ |

**Ladder Protocol:**
1. Execute BTCUSDT across all 4 strategies and grid configurations (LEAN Mode A first).
2. If BTC Mode-A 6m fails $\ge 1.2\times$ B&H or $n \le 5$, mark BTC FAIL and ladder stops for that strategy cell.
3. If BTC passes, advance the EXACT SAME parameter set to ETHUSDT, then SOLUSDT, then BNBUSDT.
4. Tiny-n check: BTC Mode-A $n \le 5 \implies$ FAIL. Flag $n \in [6..10]$ as thin.
5. All results logged to `stage29-dual-sol-bnb-v1-scoreboard.csv` and `.md`.
