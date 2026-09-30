# stage13-dual-sol-bnb-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-18  
**Research ID:** `stage13-dual-sol-bnb-v1`  
**Track:** Track 1 Path B after stage12 (0/40 BTC LEAD wipe). Track 2 Discord OFF-LIMITS.  
**Authoritative Briefs:** `CODING_KICK_ba1d.md` & `stage13-dual-sol-bnb-briefs-2026-09-18_8142.md`

---

## 1. Governance & Methodological Hygiene

To enforce **BTC-clearing PRIMARY** + **BNB-portable SECONDARY** per Path B Stage 13 directives:
- **BTC-Clearing PRIMARY Bias:** Stage 12 lesson (0/40 never left BTC — over-smoothed / multipole / FIR-lag / CSI-PMO signal-cross class EXIT). Strategies must clear BTC first with dense Mode-A trade count $n \gg 9$ on 1H–4H majors.
- **BNB-Portable SECONDARY Bias:** After BTC+SOL clear, BNB survival remains mandatory (Stage 10/11 lesson). However, never sacrifice BTC lead or over-smooth/damp to accommodate quiet BNB.
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin after SOL clear is strictly prohibited.
- **Density & Anti-Over-Smooth Policy:** Prefer responsive zero-cross, signed-event, vote-count, range-ratchet architectures. Never use stage12-class multipole/Gaussian, ultimate smoother duals, EDCF FIR-lag, or CSI-PMO signal-cross grafts.
- **Tiny-n Policy (Critical):** If Mode-A BTC $n \le 5$ on 6m $\to$ FAIL that cell even if $\times\text{B\&H} \ge 1.2$ (hard-fail cell as over-gated / under-specified). Also flag $n \approx 9$ (in range $[6..10]$) as thin.
- **Stop-Ladder Sequence:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Smokes:**
  - `btc_smoke`: **BTC-LEAD CRITICAL:** Kill if CSI/PMO/Gaussian/US damp grafted; Kill if parameter inflation collapses BTC $n$; Kill if Mode B forced while Mode A BTC $n$ healthy.
  - `sol_smoke`: Enforce motif anti-burns, timeframe sanity, parameter validity, and retention check (after ETH, SOL $n$ must stay multi-dozen class on 6m 1H).
  - `bnb_smoke`: **CRITICAL after BTC+SOL:** Kill if different parameters than SOL; Mode B shorts ungated; no ATR; volume graft; per-coin retuning. Prefer identical params; long-only; ATR exit.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on execution timeframe.
- **Costs:** 0.10%/side fee + 5 bps slippage (consistent with Path B standard harness). Mode-A 100% equity; ops 2.5% equity.
- **Hard Excludes:** All stage 1–12 IDs (all), including Pee TDI/Direction, TrendScore, NetLead, GMMA osc, VQI, TII, Rainbow, Dorsey, TCF, DEMA, Blau CSI, EDCF, Ultimate Smoother, Gaussian, Swenlin PMO.

---

## 2. Locked Strategy 1 (`demark-rei-zero-cross-v1`)

### 2.1 Formulation
- **DeMark Range Expansion Index (Thomas DeMark, New Science of Technical Analysis / S&C V.15:8):**
  $$s_t = (\text{high}_t - \text{high}_{t-2}) + (\text{low}_t - \text{low}_{t-2})$$
  $$v_t = \begin{cases} 1 & \text{if } ((\text{high}_{t-2} \ge \text{close}_{t-7} \lor \text{high}_{t-2} \ge \text{close}_{t-8} \lor \text{high}_t \ge \text{close}_{t-5} \lor \text{high}_t \ge \text{close}_{t-6}) \\ & \quad \land (\text{low}_{t-2} \le \text{close}_{t-7} \lor \text{low}_{t-2} \le \text{close}_{t-8} \lor \text{low}_t \le \text{close}_{t-5} \lor \text{low}_t \le \text{close}_{t-6})) \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{num}_t = \sum_{i=0}^{L-1} v_{t-i} \cdot s_{t-i}$$
  $$\text{den}_t = \sum_{i=0}^{L-1} (|\text{high}_{t-i} - \text{high}_{t-i-2}| + |\text{low}_{t-i} - \text{low}_{t-i-2}|)$$
  $$\text{REI}_t = \begin{cases} 100 \cdot \frac{\text{num}_t}{\text{den}_t} & \text{if } \text{den}_t \ne 0 \\ 0 & \text{otherwise} \end{cases}$$
  Prefer **$L=8$**.
- **Mode A (BTC-PRIMARY dense zero — prefer first):**
  - Long entry: $\text{crossover}(\text{REI}, 0)$
  - Exit: $\text{crossunder}(\text{REI}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet / DeMark classic ±60 reclaim):**
  - Long entry: $\text{crossover}(\text{REI}, -60)$
  - Exit: $\text{crossunder}(\text{REI}, 60)$ (or ATR stop)
  - Evaluated with identical $L$ across all coins only if Mode A over-whips BNB.

### 2.2 Locked Parameter Space
- Sweep: $L \in \{5, 8, 13\}$
- Primary grid:
  1. `mode_a|(L8)` (preferred)
  2. `mode_a|(L5)`
  3. `mode_a|(L13)`
  4. `mode_b|(L8)`
- Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if CSI/PMO/Gaussian/US damp grafted; Kill if $L \gg 13$ collapses BTC $n$; Kill if Mode B forced while Mode A BTC $n$ healthy. Prefer Mode A $L=8$, 1H+.
- **sol_smoke:** Kill if RSI/CMO/ROC/DeMarker labeled REI; 15m $L=3$ spam; ER/AO/PGO/stage12 graft. Retention check: after ETH, SOL $n$ must stay multi-dozen class on 6m 1H.
- **bnb_smoke:** Kill if different $L$ than SOL; Mode B shorts ungated; no ATR; volume graft. Kill if BNB needs $L \ne \text{SOL}$. Prefer identical params; long-only; ATR exit.
- **Forbidden:** RSI/CMO/ROC/CSI/PMO; ADX; ER-gate; AO/WMA/PGO; stage12 smoother duals.

---

## 3. Locked Strategy 2 (`khalil-pzo-zero-cross-v1`)

### 3.1 Formulation
- **Price Zone Oscillator (Khalil & Steckler, TASC Jun 2011 / thinkorswim):**
  $$\text{signed}_t = \begin{cases} \text{close}_t & \text{if } \text{close}_t > \text{close}_{t-1} \\ -\text{close}_t & \text{if } \text{close}_t < \text{close}_{t-1} \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{CP}_t = \text{EMA}(\text{signed}, n)$$
  $$\text{TC}_t = \text{EMA}(\text{close}, n)$$
  $$\text{PZO}_t = \begin{cases} 100 \cdot \frac{\text{CP}_t}{\text{TC}_t} & \text{if } \text{TC}_t \ne 0 \\ 0 & \text{otherwise} \end{cases}$$
  Prefer **$n=14$**.
- **Mode A (BTC-PRIMARY):**
  - Long entry: $\text{crossover}(\text{PZO}, 0)$
  - Exit: $\text{crossunder}(\text{PZO}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet quality):**
  - Long entry: $\text{crossover}(\text{PZO}, 0) \land \text{PZO} > 0$ (or $\text{PZO} > 15$)
  - Exit: $\text{crossunder}(\text{PZO}, 0) \lor \text{PZO} < 0$ (or ATR stop)
  - Identical $n$ across coins.

### 3.2 Locked Parameter Space
- Sweep: $n \in \{10, 14, 20\}$
- Primary grid:
  1. `mode_a|(n14)` (preferred)
  2. `mode_a|(n10)`
  3. `mode_a|(n20)`
  4. `mode_b|(n14,pzo0)`
- Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $n$ raised aggressively to damp until BTC $n$ collapses; Kill if PMO×signal/CSI/ADX/EMA60 graft. Prefer Mode A $n=14$, 1H+.
- **sol_smoke:** Kill if VZO/ROC/PSY labeled PZO; 15m $n=3$; stage12 grafts. Retention check: after ETH, SOL $n$ multi-dozen class.
- **bnb_smoke:** Kill if different $n$ than SOL; Mode B shorts ungated; no ATR; volume/VZO graft. Prefer identical params; long-only; ATR exit.
- **Forbidden:** VZO/volume primary; ADX/DMI; EMA60 trend graft; ROC-zero labeled PZO; PMO×signal; CSI; stage12 duals.

---

## 4. Locked Strategy 3 (`mobius-tmo-main-zero-v1`)

### 4.1 Formulation
- **Mobius True Momentum Oscillator (Mobius @ ThinkScript Lounge / useThinkScript):**
  $$\text{vote}_t = \sum_{i=0}^{\text{length}-1} \begin{cases} 1 & \text{if } \text{close}_t > \text{open}_{t-i} \\ -1 & \text{if } \text{close}_t < \text{open}_{t-i} \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{EMA1}_t = \text{EMA}(\text{vote}, \text{calcLength})$$
  $$\text{Main}_t = \text{EMA}(\text{EMA1}, \text{smoothLength})$$
  $$\text{Signal}_t = \text{EMA}(\text{Main}, \text{smoothLength})$$
  Prefer $(\text{length}=14, \text{calcLength}=5, \text{smoothLength}=3)$.
- **Mode A (BTC-PRIMARY):**
  - Long entry: $\text{crossover}(\text{Main}, 0)$
  - Exit: $\text{crossunder}(\text{Main}, 0)$ (or ATR stop)
  - **Do NOT** use Main×Signal as Mode A (PMO-class EXIT).
- **Mode B (BNB-quiet quality):**
  - Long entry: $\text{crossover}(\text{Main}, 0) \land \text{Main} > 0$
  - Exit: $\text{crossunder}(\text{Main}, 0) \lor \text{Main} < 0$ (or ATR stop)
  - Evaluated with identical params across coins.

### 4.2 Locked Parameter Space
- Sweep: $\text{length} \in \{10, 14, 21\}$, keep $\text{calcLength}=5, \text{smoothLength}=3$ short.
- Primary grid:
  1. `mode_a|(len14,c5,s3)` (preferred)
  2. `mode_a|(len10,c5,s3)`
  3. `mode_a|(len21,c5,s3)`
  4. `mode_b|(len14,c5,s3)`
- Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if smooth/calc raised into stage12-damp territory until BTC $n$ collapses; Kill if Mode A becomes Main×Signal (PMO EXIT clone); Kill if HTF security agg. Prefer Mode A (14,5,3), 1H+.
- **sol_smoke:** Kill if ROC/AO/PMO labeled TMO; 15m length=3 spam; ER/stage12 graft. Retention check: after ETH, SOL $n$ multi-dozen class.
- **bnb_smoke:** Kill if different (length,calc,smooth) than SOL; Main×Signal only on BNB; no ATR; volume graft. Prefer identical params; long-only; ATR exit.
- **Forbidden:** ROC/AO/PSY/PMO×signal labeled TMO; HTF `request.security`; stage12 duals; ER-gate.

---

## 5. Locked Strategy 4 (`donovan-range-filter-flip-v1`)

### 5.1 Formulation
- **DonovanWall Range Filter (TradingView 'Range Filter [DW]'):**
  $$\text{src}_t = \text{close}_t$$
  $$\text{av\_chg}_t = \text{EMA}(\text{EMA}(|\text{src}_t - \text{src}_{t-1}|, \text{period}), 2 \cdot \text{period} - 1)$$
  $$\text{rng}_t = \text{av\_chg}_t \cdot \text{mult}$$
  Ratchet $\text{filt}_t$:
  $$\text{filt}_t = \begin{cases} \text{src}_t - \text{rng}_t & \text{if } \text{src}_t - \text{rng}_t > \text{filt}_{t-1} \\ \text{src}_t + \text{rng}_t & \text{if } \text{src}_t + \text{rng}_t < \text{filt}_{t-1} \\ \text{filt}_{t-1} & \text{otherwise} \end{cases}$$
  Direction $\text{dir}_t$:
  $$\text{dir}_t = \begin{cases} 1 & \text{if } \text{filt}_t > \text{filt}_{t-1} \\ -1 & \text{if } \text{filt}_t < \text{filt}_{t-1} \\ \text{dir}_{t-1} & \text{otherwise} \end{cases}$$
  Prefer $(\text{period}=20, \text{mult}=1.618)$.
- **Mode A (BTC-PRIMARY):**
  - Long entry: $\text{dir}$ flips to $+1$ ($\text{dir}_t == 1 \land \text{dir}_{t-1} \ne 1$)
  - Exit: $\text{dir}$ flips to $-1$ ($\text{dir}_t == -1 \land \text{dir}_{t-1} \ne -1$) (or ATR stop)
- **Mode B (BNB-quiet quality):**
  - Long entry: $\text{dir}$ flips to $+1 \land \text{src} > \text{filt}$
  - Exit: $\text{dir}$ flips to $-1 \lor \text{src} < \text{filt}$ (or ATR stop)
  - Evaluated with identical params across coins.

### 5.2 Locked Parameter Space
- Sweep: $\text{period} \in \{14, 20, 28\}, \text{mult} \in \{1.0, 1.618, 2.0\}$
- Primary grid:
  1. `mode_a|(p20,m1.618)` (preferred)
  2. `mode_a|(p14,m1.618)`
  3. `mode_a|(p20,m2.0)`
  4. `mode_b|(p20,m1.618)`
- Timeframes: 1H, 4H

### 5.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if period/mult inflated until BTC flips collapse; Kill if ATR-SuperTrend substituted; Kill stage12 damp graft. Prefer Mode A (20, 1.618), 1H+.
- **sol_smoke:** Kill if SuperTrend/Chandelier/Keltner labeled RF; 15m period=5; ER/AO/PGO/stage12. Retention check: after ETH, SOL flip $n$ multi-dozen class.
- **bnb_smoke:** Kill if different (period,mult) than SOL; Mode B shorts ungated; no ATR; per-coin retune. Prefer identical params; long-only; ATR exit.
- **Forbidden:** SuperTrend/Chandelier/Keltner/SSL labeled RF; ATR-band substitute; stage12 smoother duals; ER-gate.

---

## 6. Locked Strategy 5 (`clv-sma-zero-cross-v1`) — Optional 5th Included

### 6.1 Formulation
- **Close Location Value SMA (Achelis / Investopedia / StockCharts):**
  $$\text{rng}_t = \text{high}_t - \text{low}_t$$
  $$\text{CLV}_t = \begin{cases} \frac{2 \cdot \text{close}_t - \text{high}_t - \text{low}_t}{\text{rng}_t} & \text{if } \text{rng}_t \ne 0 \\ 0 & \text{otherwise} \end{cases}$$
  $$\text{CLVS}_t = \text{SMA}(\text{CLV}, N)$$
  Prefer **$N=14$**. Volume-free.
- **Mode A (BTC-PRIMARY):**
  - Long entry: $\text{crossover}(\text{CLVS}, 0)$
  - Exit: $\text{crossunder}(\text{CLVS}, 0)$ (or ATR stop)
- **Mode B (BNB-quiet quality):**
  - Long entry: $\text{crossover}(\text{CLVS}, 0) \land \text{CLVS} > 0$
  - Exit: $\text{crossunder}(\text{CLVS}, 0) \lor \text{CLVS} < 0$ (or ATR stop)
  - Identical $N$ across coins.

### 6.2 Locked Parameter Space
- Sweep: $N \in \{8, 14, 21\}$
- Primary grid:
  1. `mode_a|(N14)` (preferred)
  2. `mode_a|(N8)`
  3. `mode_a|(N21)`
  4. `mode_b|(N14)`
- Timeframes: 1H, 4H

### 6.3 Smoke Constraints & Retention Rules
- **btc_smoke:** Kill if $N$ raised until BTC $n$ collapses; Kill AccDist×volume reintroduced; Kill CSI triple-EMA. Prefer Mode A $N=14$, 1H+.
- **sol_smoke:** Kill if AccDist/CMF/III/BoP labeled CLV-SMA; 15m $N=3$; stage12. Retention check: after ETH, SOL $n$ multi-dozen class.
- **bnb_smoke:** Kill if different $N$ than SOL; Mode B shorts ungated; no ATR; volume graft. Prefer identical params; long-only; ATR exit.
- **Forbidden:** AccDist/CMF/III/OBV/volume; BoP; CSI/PMO; stage12 duals.

---

## 7. Stop-Ladder Execution Protocol & Scoring Matrix

1. **Ladder Sequence:** BTCUSDT $\to$ ETHUSDT $\to$ SOLUSDT $\to$ BNBUSDT.
2. **Promotion Gate:** Only cells meeting last-6m Mode-A return $\ge 1.2\times$ B&H AND $n > 5$ on BTC are evaluated on subsequent symbols.
3. **Dual Rule:** Strict parameter identity on SOL and BNB.
4. **Scoreboard Output:** Markdown and CSV reports generated under `trading-bot/backtest/path_b/stage13_dual_sol_bnb_v1/results/`.
