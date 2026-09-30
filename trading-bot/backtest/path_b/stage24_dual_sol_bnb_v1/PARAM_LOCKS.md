# stage24-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND LADDER SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage24-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage23 (BTC PASS 0/32; Chande-Kroll ~1.194× near-miss). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_0bbe.md` & `stage24-dual-sol-bnb-briefs-2026-09-18_1184.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC LEAD PRIMARY CRITICAL** (push past Chande-Kroll ~1.194× near-miss without over-damp) + **Denser $n \gg 9$** + **Dual Survival (identical params across BTC/ETH/SOL/BNB)** + **BNB-survival after 3-coin** per Path B Stage 24 directives:
- **BTC LEAD PRIMARY (Chande-Kroll ~1.194× Near-Miss Reclaim):** In Stage 23, all 32 cells failed on BTC, with Chande-Kroll Stop Flip at 1H reaching ~1.194× near-miss (just under the $\ge 1.2\times$ threshold). In Stage 24, we lock responsive non-MA impulse, trend-hold, statistical-break, and published count-back SAR families outside stage 1–23 + parks that can clear dense BTC $\ge 1.2\times$ without cloning stage 23 ATR corridor or stage 22 percentile/z/AVWAP/VFI.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across all four coins (BTC, ETH, SOL, BNB). Retuning parameters per coin after a clear is strictly forbidden.
- **Denser $n \gg 9$ Policy:** Ensure trade density remains well above the thin counts of Stage 14 TTF ($n=6..10$), Stage 8 PGO ($n \approx 9$), and thin $n \le 5$ structure stalls, while avoiding parameter over-inflation that collapses BTC $n$.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first (`btc_smoke` CRITICAL); PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH (HARD) $\to$ SOL (HARD, `sol_smoke`) $\to$ BNB (HARD, `bnb_smoke`).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC LEAD PRIMARY CRITICAL (push past ~1.194× / no stage23 0-BTC):** Kill if Mode A BTC 0 / chop under costs; Kill if fail past ~1.194× neighborhood; Kill if parameters inflated until BTC $n$ collapses; Kill if improper substitutes labeled seated strategies; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A defaults, 1H+.
  - `eth_smoke`: **BTC->ETH PORTABILITY:** Kill if BTC clears $\ge 1.2\times$ dense then ETH under 1.2×; Kill if parameters retuned only on ETH. Prefer identical defaults; ETH $n$ multi-dozen.
  - `sol_smoke`: **SOL-AFTER-BTC+ETH:** Kill family if BTC+ETH clear $\ge 1.2\times$ then SOL under $1.2\times$; Kill if parameters retuned only on SOL; Kill if 15m spam; Kill if stage 1–23 grafts. Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
  - `bnb_smoke`: **BNB-SURVIVAL (HHLL/TTF LESSON):** Kill if 3-coin clear then BNB quiet wipe; Kill if parameters retuned only on BNB; Kill Mode B only on BNB; ungated shorts; no ATR. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–23 IDs (all), including QQE/MAMA/Wilder/Chande-Kroll, percentile/zscore/AVWAP/VFI, Chaikin/outside/Ulcer/Parkinson/inside, VPCI/BW-MFI/DI/Kalman/RAVI, HHLL/STARC/VZO/NVI/FDI, DPO/PPO/VHF/FOSC/PO, HA/MDI/DSS/III/PMA, BandPass/HP/3LB/SI/Kagi, Spearman/UO2025/CorrCycle/NET/DVI, TTF/PFE/ASH/APZ/Nadaraya, REI/PZO/TMO/RF/TwinRF/CLV, Pee TDI, stage12 smoother class.

---

## 2. Locked Strategy 1 (`guppy-countback-line-flip`)

### 2.1 Formulation
- **Guppy Count Back Line — close × CBL SAR Flip:**
  - From most recent significant high: count 3 successively lower lows $\to$ `cblLong` (never lower existing on long).
  - From most recent significant low: count 3 successively higher highs $\to$ `cblShort` (never raise existing on short).
  - Prefer **`countDepth = 3`** (Guppy published).
  - $\ne$ Wilder VS (ARC = factor * ATR), $\ne$ Chande-Kroll (two-stage ATR), $\ne$ SuperTrend (HL2 ratchet), $\ne$ PSAR (AF parabola).
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(close, cblShort)`
  - Exit: `crossunder(close, cblLong)`
- **Mode B (Confirmation / Hygiene):**
  - Require min bars since CBL update $\ge kConfirm$ or optional ATR exit mult $\in \{1.5, 2.0\}$ — only if Mode A over-whips; identical params across all four coins.

### 2.2 Locked Parameter Space
- Sweep (LEAN): `countDepth = 3` locked; TF 1H vs 4H; optional ATR exit mult $\in \{0.0, 1.5, 2.0\}$.
- Primary grid:
  1. `mode_a|(cd3,atr0.0)` (preferred)
  2. `mode_a|(cd3,atr1.5)`
  3. `mode_a|(cd3,atr2.0)`
  4. `mode_b|(cd3,kconf2)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `countDepth = 3` locked. Parameter inflation collapses BTC $n$ forbidden. Prefer Mode A cd=3, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 3. Locked Strategy 2 (`kirshenbaum-bands-break`)

### 3.1 Formulation
- **Kirshenbaum Bands — EMA Mid $\pm k \cdot \text{LinReg stderr}$ Break:**
  - `mid = ta.ema(close, emaLen)`
  - LinReg residual stderr over `regLen`: standard error of closes about a linear regression line of length `regLen`.
  - `upper = mid + k * stderr`
  - `lower = mid - k * stderr`
  - Prefer **`(20, 20, 1.75)`**.
  - **Mid MUST be EMA — kill if LinReg mid (SEB).**
  - $\ne$ Bollinger Bands (stdev of price), $\ne$ SEB (LinReg mid), $\ne$ STARC (SMA $\pm k \cdot \text{ATR}$).
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(close, upper)`
  - Exit: `crossunder(close, mid)`
- **Mode B (Stderr Percentrank Filter):**
  - Require `stderr_percentrank > 50` — only if Mode A over-whips; identical across all four.

### 3.2 Locked Parameter Space
- Sweep (LEAN): `emaLen` $\in \{20, 30\}$; `regLen` $\in \{20\}$; $k \in \{1.75, 2.25\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(ema20,reg20,k1.75)` (preferred)
  2. `mode_a|(ema30,reg20,k1.75)`
  3. `mode_a|(ema20,reg20,k2.25)`
  4. `mode_b|(ema20,reg20,k1.75,pr50)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). `emaLen` $\in \{20, 30\}$, `regLen = 20`, $k \in \{1.75, 2.25\}$. Stderr LinReg mid forbidden. Prefer Mode A (20,20,1.75), 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. BB/percentile graft fails. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 4. Locked Strategy 3 (`imi-midline-fifty`)

### 4.1 Formulation
- **Intraday Momentum Index — Body Impulse $\times 50$ Midline:**
  - `up = max(close - open, 0)`
  - `dn = max(open - close, 0)`
  - `imi = 100 * sum(up, n) / (sum(up, n) + sum(dn, n))` (guard denom=0 $\to 50.0$)
  - Prefer **`n = 14`**.
  - $\ne$ PSY (% of up closes), $\ne$ RMI (momentum lookback RSI), $\ne$ TII (SMA intensity), $\ne$ raw RSI (close-to-close), $\ne$ QQE (ATR-of-RSI trail).
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(imi, 50)`
  - Exit: `crossunder(imi, 50)`
- **Mode B (Quality Impulse Filter):**
  - Require `imi > 55` entry threshold — only if Mode A over-whips; identical across all four.

### 4.2 Locked Parameter Space
- Sweep (LEAN): $n \in \{10, 14, 21\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(n14)` (preferred)
  2. `mode_a|(n10)`
  3. `mode_a|(n21)`
  4. `mode_b|(n14,thr55)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $n \in \{10, 14, 21\}$. Raw RSI or PSY labeled IMI forbidden. Prefer Mode A n=14, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. 15m $n=3$ spam forbidden. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 5. Locked Strategy 4 (`williams-ad-sma-cross`)

### 5.1 Formulation
- **Williams Accumulation/Distribution — WAD $\times$ SMA Cross:**
  - `wad` cumulative:
    - if $C > C[1]$: $WAD += C - \min(L, C[1])$
    - if $C < C[1]$: $WAD += C - \max(H, C[1])$
    - else: unchanged
  - **No volume.**
  - `sig = ta.sma(wad, m)`
  - Prefer **`m = 21`**.
  - $\ne$ AccDist (CLV $\times$ vol cumulative), $\ne$ ASI (Wilder swing accum), $\ne$ CLV $\times$ SMA, $\ne$ OBV, $\ne$ VFI.
- **Mode A (BTC-LEAD Lean):**
  - Long entry: `crossover(wad, sig)`
  - Exit: `crossunder(wad, sig)`
- **Mode B (Rising WAD Filter):**
  - Require `wad > wad[1]` — only if Mode A over-whips; identical across all four.

### 5.2 Locked Parameter Space
- Sweep (LEAN): $m \in \{14, 21, 34\}$; TF 1H vs 4H.
- Primary grid:
  1. `mode_a|(m21)` (preferred)
  2. `mode_a|(m14)`
  3. `mode_a|(m34)`
  4. `mode_b|(m21,rising)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** 15m forbidden (1H+ required). $m \in \{14, 21, 34\}$. Volume graft into WAD forbidden. Prefer Mode A m=21, 1H+.
- **eth_smoke:** Retuning only on ETH fails. Parameters not in locked set fail.
- **sol_smoke:** Retuning away from BTC/ETH fails. AccDist / VFI graft forbidden. Retention: SOL $n$ multi-dozen-class.
- **bnb_smoke:** Identical params across all coins. Mode B only on BNB fails.

---

## 6. Matrix & Stop-Ladder Execution Plan

Each strategy has 4 parameter variants across 2 timeframes (1H, 4H) = 8 cells per strategy.
Across 4 strategies, total candidate parameter configurations per coin = 32 cells.

- **Step 1: BTCUSDT (32 cells evaluated)**
  - Mandatory: Check `btc_smoke` and tiny-$n$ ($n \le 5 \to$ FAIL; flag $n \in [6..10]$).
  - Measure last-6m Mode-A return vs B&H ($\ge 1.2\times$ required for PASS_6m).
  - Only cells passing gate advance to Step 2.
- **Step 2: ETHUSDT (Only BTC PASS promoted)**
  - If 0 cells pass BTC, ladder stops here; all subsequent coins recorded as pruned.
  - Verify `eth_smoke` (identical params, no per-coin retuning).
- **Step 3: SOLUSDT (Only ETH PASS promoted)**
  - Verify `sol_smoke`.
- **Step 4: BNBUSDT (Only SOL PASS promoted)**
  - Verify `bnb_smoke`.
