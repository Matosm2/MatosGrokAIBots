# stage16-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage16-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage15 (0/40 BTC LEAD wipe — stage12 rhyme). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_acb2.md` & `stage16-dual-sol-bnb-briefs-2026-09-18_21c7.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY** + **Denser $n \gg 9$** + **BTC->ETH Portability** + **BNB-Survival after 3-coin clear** per Path B Stage 16 directives:
- **BTC LEAD PRIMARY Bias:** Stage 15 rank/HP-band-RMS/corr/NET/DVI collapsed trade counts and produced a 0/40 BTC wipe (rhyming with Stage 12). Stage 16 prioritizes responsive signed cycle / bar-strength / close-only structure flips that clear BTC first without over-damp collapse.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$) and Stage 8 PGO ($n \approx 9$).
- **BTC->ETH Portability Preservation:** Stage 13 lesson: `demark-rei-zero-cross` cleared BTC with 1.530x but wiped on ETH at -1.201x. Strategies must demonstrate cross-coin portability on ETH without per-coin retuning.
- **BNB-Survival (CRITICAL after 3-coin clear):** Stage 14 lesson: TTF cleared BTC->ETH->SOL then wiped on quieter BNB (0.093x vs +15.36% B&H). Mode B parameters or structure stability must prevent quiet wipes without breaking BTC/ETH.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear (especially lengthening lookback only on BNB after SOL) is strictly forbidden.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if parameter inflation collapses BTC $n$; Kill if SuperSmoother/Roofing grafted "to quiet"; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY CRITICAL:** Kill if BTC clears $\ge 1.2\times$ then ETH wipes (stage13 REI pattern); Kill if parameters or mode retuned only on ETH; Kill if Cyber Cycle / Roofing substitute.
  - `sol_smoke`: Enforce motif anti-burns, timeframe sanity, parameter validity, and retention check (after ETH, SOL $n$ must stay multi-dozen class on 6m 1H).
  - `bnb_smoke`: **CRITICAL after BTC+ETH+SOL (TTF lesson):** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; volume graft; per-coin "BNB-only" lengthen. Prefer identical params; long-only; ATR exit. Kill if BNB needs params $\ne$ SOL to survive.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–15 IDs (all), including Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/CLV, Pee TDI, TrendScore, NetLead, GMMA osc, VQI, Blau CSI, EDCF, Ultimate Smoother, Gaussian multipole, Swenlin PMO.

---

## 2. Locked Strategy 1 (`ehlers-bandpass-zero`)

### 2.1 Formulation
- **Ehlers Band-Pass Filter (Cycle Analytics for Traders / Cybernetic Analysis):**
  - $\beta = \cos(2\pi / P)$
  - $\gamma = 1 / \cos(4\pi \delta / P)$
  - $\alpha = \gamma - \sqrt{\gamma^2 - 1}$
  - $BP = 0.5(1 - \alpha)(\text{src} - \text{src}[2]) + \beta(1 + \alpha)BP[1] - \alpha BP[2]$
  - Prefer **$P=20, \delta=0.3$**.
- **Mode A (BTC-LEAD PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(BP, 0)$
  - Exit: $\text{crossunder}(BP, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / quality hold):**
  - Long entry: $\text{crossover}(BP, 0)$ and $BP > \epsilon$
  - Exit: $\text{crossunder}(BP, 0)$ (or ATR stop)
  - Evaluated with identical $(P, \delta)$ across all coins only if Mode A over-whips BNB.

### 2.2 Locked Parameter Space
- Sweep: $P \in \{14, 20, 28\}$, $\delta \in \{0.1, 0.3, 0.5\}$
- Primary grid:
  1. `mode_a|(P20,d0.3)` (preferred)
  2. `mode_a|(P14,d0.3)`
  3. `mode_a|(P28,d0.3)`
  4. `mode_b|(P20,d0.3)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $P > 40$ collapses BTC $n$; Kill if SuperSmoother/Roofing grafted; Kill if Super Passband substitute; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A $(20, 0.3)$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if $(P, \delta)$ retuned only on ETH; Kill if Cyber Cycle / Roofing graft.
- **sol_smoke:** Kill if Super Passband / Cyber Cycle / UO2025 labeled BandPass; 15m $P \le 5$ spam. Retention: SOL $n$ multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if different $(P, \delta)$ than SOL; Mode B shorts ungated; no ATR; per-coin lengthen. Prefer identical params.

---

## 3. Locked Strategy 2 (`ehlers-twopole-hp-zero`)

### 3.1 Formulation
- **Ehlers Two-Pole HighPass Filter (Cycle Analytics / Mesa Software):**
  - $a_1 = \exp(-1.414\pi / P)$
  - $c_2 = 2 a_1 \cos(1.414\pi / P)$
  - $c_3 = -a_1^2$
  - $c_1 = (1 + c_2 - c_3) / 4$
  - $HP = c_1(\text{src} - 2\text{src}[1] + \text{src}[2]) + c_2 HP[1] + c_3 HP[2]$
  - Prefer **$P=40$**. SINGLE HP only — no SuperSmoother after ($\ne$ Roofing).
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(HP, 0)$
  - Exit: $\text{crossunder}(HP, 0)$ (or ATR stop)
- **Mode B (BNB quiet):**
  - Long entry: $\text{crossover}(HP, 0)$ and $HP > \epsilon$
  - Exit: $\text{crossunder}(HP, 0)$ (or ATR stop)
  - Evaluated with identical $P$ across all coins.

### 3.2 Locked Parameter Space
- Sweep: $P \in \{28, 40, 48, 60\}$
- Primary grid:
  1. `mode_a|(P40)` (preferred)
  2. `mode_a|(P28)`
  3. `mode_a|(P48)`
  4. `mode_b|(P40)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $P > 80$ collapses BTC $n$; Kill if SS grafted after HP (Roofing); Kill if dual-HP UO2025 substitute. Prefer Mode A $P=40$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if $P$ retuned only on ETH; Kill if Roofing/SS substitute.
- **sol_smoke:** Kill if Roofing / UO2025 / Cyber Cycle labeled single-HP; 15m $P \le 5$ spam. Retention: SOL $n$ multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if different $P$ than SOL; Mode B shorts ungated; no ATR; per-coin retune. Prefer identical params.

---

## 4. Locked Strategy 3 (`three-line-break-flip`)

### 4.1 Formulation
- **Three Line Break (Nison / StockCharts):**
  - Close-only structure rule evaluated on standard OHLC closes (not synthetic Line Break chart type).
  - Direction $+1$ (bullish) or $-1$ (bearish) maintained across bars (`var` state).
  - Bullish reversal: prior direction bearish AND $\text{close} > \text{highest high of last } N \text{ bearish lines}$.
  - Bearish reversal: prior direction bullish AND $\text{close} < \text{lowest low of last } N \text{ bullish lines}$.
  - Prefer **$N=3$**.
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry on bullish reversal
  - Exit on bearish reversal (or ATR stop)
- **Mode B (BNB quiet):**
  - $N=4$ or require 2 extension lines before arming reverse — only if Mode A over-whips; identical $N$ across coins.

### 4.2 Locked Parameter Space
- Sweep: $N \in \{2, 3, 4\}$
- Primary grid:
  1. `mode_a|(N3)` (preferred)
  2. `mode_a|(N2)`
  3. `mode_a|(N4)`
  4. `mode_b|(N3)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $N > 6$ collapses flips; Kill if Donchian/SuperTrend graft sparsifies; Kill if Mode B forced while Mode A BTC healthy. Prefer Mode A $N=3$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if $N$ retuned only on ETH; Kill if pivot-accept substitute.
- **sol_smoke:** Kill if Donchian / RangeFilter / TTF labeled 3LB; 15m $N \le 1$ spam. Retention: SOL $n$ multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if different $N$ than SOL; Mode B shorts ungated; no ATR; per-coin retune. Prefer identical params.

---

## 5. Locked Strategy 4 (`wilder-swing-index-zero`)

### 5.1 Formulation
- **Wilder Swing Index (J. Welles Wilder, New Concepts in Technical Trading Systems):**
  - $N = (C - C_1) + 0.5(C - O) + 0.25(C_1 - O_1)$
  - $K = \max(|H - C_1|, |L - C_1|)$
  - $R$ from Wilder three-case largest excursion:
    - If $|H - C_1| \ge |L - C_1|$ and $|H - C_1| \ge H - L$: $R = |H - C_1| - 0.5|L - C_1| + 0.25(C_1 - O_1)$
    - Else if $|L - C_1| \ge |H - C_1|$ and $|L - C_1| \ge H - L$: $R = |L - C_1| - 0.5|H - C_1| + 0.25(C_1 - O_1)$
    - Else: $R = (H - L) + 0.25(C_1 - O_1)$
  - $T = \text{ATR}(\text{atr\_len})$ limit-move proxy (guard $R \ne 0, T \ne 0$).
  - $SI = 50 (N / R) (K / T)$
  - Prefer **$\text{atr\_len}=14$**. Do NOT cumsum to ASI for Mode A.
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry: $\text{crossover}(SI, 0)$
  - Exit: $\text{crossunder}(SI, 0)$ (or ATR stop)
- **Mode B (BNB quiet):**
  - Long entry: $\text{crossover}(SI, 0)$ and $|SI| > \text{threshold}$
  - Exit: $\text{crossunder}(SI, 0)$ (or ATR stop)

### 5.2 Locked Parameter Space
- Sweep: $\text{atr\_len} \in \{10, 14, 20\}$
- Primary grid:
  1. `mode_a|(atr14)` (preferred)
  2. `mode_a|(atr10)`
  3. `mode_a|(atr20)`
  4. `mode_b|(atr14)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $T$-proxy smoothing inflated until BTC $n$ collapses; Kill if Mode A becomes ASI dual-break (stage1); Kill if CLV substitute. Prefer Mode A SI $\times 0$ ATR14, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if $T$-proxy retuned only on ETH; Kill if ASI dual-break graft.
- **sol_smoke:** Kill if ASI dual-break / CLV / BoP labeled SI-zero; 15m ATR $\le 3$ spam. Retention: SOL $n$ multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if different $T$-proxy than SOL; Mode B shorts ungated; no ATR exit; per-coin retune. Prefer identical params.

---

## 6. Locked Strategy 5 (`nison-kagi-yang-yin-flip`)

### 6.1 Formulation
- **Nison Kagi Chart (Nison / StockCharts):**
  - Reversal-amount structure tracking on closed bar closes.
  - Direction $+1$ (rising) or $-1$ (falling); extreme price of current leg; prior peak and prior trough.
  - Reverse direction when adverse move $\ge R$, where $R = \text{atr\_mult} \times \text{ATR}(14)$.
  - Yang (thick line) when rising leg breaks prior peak; Yin (thin line) when falling leg breaks prior trough.
  - Mode A = Buy on Yin $\to$ Yang flip; Exit on Yang $\to$ Yin flip.
  - Prefer **$R = 1.0 \times \text{ATR}(14)$**.
- **Mode A (BTC-LEAD PRIMARY — prefer first):**
  - Long entry on Yin $\to$ Yang flip
  - Exit on Yang $\to$ Yin flip (or ATR stop)
- **Mode B (BNB quiet):**
  - Larger $R$ ($1.5 \times \text{ATR}$) — only if Mode A over-whips BNB; identical $R$ across coins.

### 6.2 Locked Parameter Space
- Sweep: $\text{atr\_mult} \in \{0.75, 1.0, 1.5\}$
- Primary grid:
  1. `mode_a|(atr1.0)` (preferred)
  2. `mode_a|(atr0.75)`
  3. `mode_a|(atr1.5)`
  4. `mode_b|(atr1.0)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $R$ inflated until BTC flips collapse; Kill if Mode B forced while Mode A BTC already healthy; Kill if Donchian substitute. Prefer Mode A ATR $\times 1.0$, 1H+.
- **eth_smoke:** Kill if BTC clears then ETH wipes; Kill if $R$ retuned only on ETH; Kill if 3LB/Donchian substitute.
- **sol_smoke:** Kill if Renko / Donchian / 3LB labeled Kagi; 15m $R \le 0.2$ spam. Retention: SOL $n$ multi-dozen-class on 6m 1H.
- **bnb_smoke:** Kill if different $R$ than SOL; Mode B shorts ungated; no ATR exit; per-coin retune. Prefer identical params.

---

## 7. Execution Grid Matrix

Across 4 coins $\times$ 5 strategies $\times$ 2 timeframes (1H, 4H) $\times$ 4 param variants = **160 total evaluated cells** (with stop-ladder pruning applied after BTC, ETH, and SOL).
All parameters locked as specified above.
