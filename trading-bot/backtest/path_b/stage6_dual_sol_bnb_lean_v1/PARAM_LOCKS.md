# stage6-dual-sol-bnb-lean-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-17  
**Research ID:** `stage6-dual-sol-bnb-lean-v1`  
**Authoritative Briefs:** `CODING_KICK_6458.md` & `stage6-dual-sol-bnb-lean-2026-09-17_06f8.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce the **DUAL-SURVIVAL + SOL RETENTION** paradigm across SOL and BNB per Path B Stage 6 directives:
- **Dual-Survival Rule (Identical Params):** All strategies are evaluated using strictly identical parameters across both SOL and BNB. Parameter retuning per coin to force a pass is strictly prohibited.
- **SOL Retention After ETH Clear:** Stage 5 cleared ETH then died on SOL due to over-smoothing or over-gating. For any strategy cell advancing past ETH, a qualitative and quantitative SOL retention check is performed (verifying trade density $\ge$ rough ETH density, no collapse in trend-leg capture, and indicator hugging rather than lagging flat).
- Indicator mathematical forms, parameter grids, and scale conventions are locked **before** scoring any assets on the stop-ladder (BTC → ETH → SOL → BNB).
- **Stop-ladder rule:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory Dual Smokes:** Each strategy must satisfy its dedicated `sol_smoke` and `bnb_smoke` constraints. Failed smoke conditions disqualify parameter sets from promotion.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe logic via bar aggregation or same-TF longer lookbacks on the execution timeframe.
- **Costs:** 0.1%/side fee + 5 bps slippage (consistent with Path B standard harness).
- **No burned filters or grafts:** Excludes all stage 1–5 IDs, Decycler, ITrend, PVO, P4H, MAD, SuperSmoother, Roofing filter (HP+SS), BB/stdev bands, Donchian, KAMA, SMA200, EMA ribbons, ADX/DMI, ConnorsRSI, OBV, CMF, ALMA, T3, ZLEMA, CTI, ATR%ile-as-primary, VIDYA, and other burned items.
- **If full-ladder PASS_6m = 0 for all three:** Explicitly signal Path B pause cue for CoS / Nuno usage.

---

## 2. Locked Strategy 1 (`frama-fast-slow-cross-v1`)

### 2.1 Formulation
- **Ehlers Fractal Adaptive Moving Average (FRAMA, S&C Oct 2005 / MESA):**
  Window of length $N$ ($N$ even) split into two halves of length $\text{half} = N / 2$:
  $$N_1 = \frac{\max(\text{highs}_{1\text{st half}}) - \min(\text{lows}_{1\text{st half}})}{\text{half}}$$
  $$N_2 = \frac{\max(\text{highs}_{2\text{nd half}}) - \min(\text{lows}_{2\text{nd half}})}{\text{half}}$$
  $$N_3 = \frac{\max(\text{highs}_{\text{full window}}) - \min(\text{lows}_{\text{full window}})}{N}$$
  $$\text{FD} = \frac{\ln(N_1 + N_2) - \ln(N_3)}{\ln(2.0)}, \quad \text{clamped to } [1.0, 2.0]$$
  $$\alpha = \exp(-4.6 \cdot (\text{FD} - 1.0)), \quad \text{clamped to } [0.01, 1.0]$$
  $$\text{FRAMA}_t = \alpha \cdot \text{close}_t + (1 - \alpha) \cdot \text{FRAMA}_{t-1}$$
  Seed: $\text{close}[N-1]$.
- **Mode A (Primary):**
  - $\text{fast} = \text{FRAMA}(\text{close}, N_f)$
  - $\text{slow} = \text{FRAMA}(\text{close}, N_s)$
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ or optional ATR trailing stop.
  - Locked pairs $(N_f, N_s) \in \{(16, 32), (10, 20), (12, 24)\}$ — $N$ even.
- **Mode B (Secondary):**
  - $\text{close} \times \text{FRAMA}(N)$ — evaluated only if Mode A SOL under-trades.
- **Exit:**
  - Opposite crossover / crossunder; ATR trailing stop.

### 2.2 Locked Parameter Space
- $(N_f, N_s) \in \{(16, 32), (10, 20), (12, 24)\}$
- Modes: Mode A (primary), Mode B (secondary, $N=20$)
- Execution Timeframes: 1H, 4H

### 2.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: KAMA/ER $\alpha$; VIDYA/CMO $\alpha$; SuperTrend graft; Mode B-only on 15m; odd $N$ without even halves. Prefer Mode A (16,32) or (10,20), 1H+.
- **sol_retention_note:** After ETH pass, verify SOL Mode-A trade count and trend-leg capture do not collapse vs ETH; if FRAMA remains flat during SOL impulse legs, flag as over-smoothed.
- **bnb_smoke:** Kill if: retuning $N$ per coin; $N_f=6$ on 1H; no ATR exit (when stop enabled). Prefer identical lengths; long-only first.

---

## 3. Locked Strategy 2 (`hma-dual-cross-v1`)

### 3.1 Formulation
- **Hull Moving Average (Alan Hull / ta.hma):**
  $$\text{HMA}(n) = \text{WMA}\left(2 \cdot \text{WMA}\left(\text{close}, \lfloor n/2 \rfloor\right) - \text{WMA}(\text{close}, n), \text{round}(\sqrt{n})\right)$$
  Where WMA weights the most recent bar by length down to 1.
- **Mode A (Primary):**
  - $\text{fast} = \text{HMA}(L_f)$
  - $\text{slow} = \text{HMA}(L_s)$
  - Long entry: $\text{crossover}(\text{fast}, \text{slow})$
  - Exit: $\text{crossunder}(\text{fast}, \text{slow})$ or ATR trailing stop.
  - Locked pairs $(L_f, L_s) \in \{(9, 16), (10, 30), (16, 36)\}$.
- **Mode B (Secondary):**
  - $\text{close} \times \text{HMA}(L_s)$ — evaluated only if Mode A SOL under-fires.
- **Exit:**
  - Opposite cross; ATR trailing stop.

### 3.2 Locked Parameter Space
- $(L_f, L_s) \in \{(9, 16), (10, 30), (16, 36)\}$
- Modes: Mode A (primary), Mode B (secondary, $L_s=30$)
- Execution Timeframes: 1H, 4H

### 3.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: ZLEMA/ALMA/T3 substitute; 15m length soup; EMA ribbon. Prefer Mode A (9,16) or (10,30), 1H+.
- **sol_retention_note:** SOL trade density after ETH must stay roughly $\ge$ ETH density under identical parameters; if HMA dual goes silent on SOL while ETH traded, flag as retention failure.
- **bnb_smoke:** Kill if: per-coin length retune; $L_f \le 5$; no ATR exit (when stop enabled). Prefer identical $(L_f, L_s)$; long-only.
- **Forbidden:** ALMA, T3, ZLEMA, KAMA, SuperSmoother, EMA ribbon, SMA200, RSI graft.

---

## 4. Locked Strategy 3 (`mcginley-close-slope-cross-v1`)

### 4.1 Formulation
- **McGinley Dynamic (John R. McGinley / Investopedia Standard):**
  $$\text{MD}_t = \text{MD}_{t-1} + \frac{\text{close}_t - \text{MD}_{t-1}}{k \cdot N \cdot (\text{close}_t / \text{MD}_{t-1})^4}$$
  Seed: $\text{MD}_0 = \text{close}_0$; guarded with $\text{MD}_{t-1} \neq 0$.
  $k = 1.0$ locked (Investopedia $N$-only standard).
  $N \in \{10, 14, 20\}$.
- **Mode A (Primary):**
  - Long entry: $\text{crossover}(\text{close}, \text{MD}) \land (\text{MD}_t > \text{MD}_{t-1})$
  - Exit: $\text{crossunder}(\text{close}, \text{MD}) \lor (\text{MD}_t < \text{MD}_{t-1})$ or ATR trailing stop.
- **Mode B (Secondary):**
  - Long while $\text{close}_t > \text{MD}_t \land \text{MD}_t > \text{MD}_{t-1}$. Mode A first.
- **Exit:**
  - Mode A exit rule; ATR trailing stop.

### 4.2 Locked Parameter Space
- $N \in \{10, 14, 20\}$
- $k = 1.0$
- Modes: Mode A (primary), Mode B (secondary)
- Execution Timeframes: 1H, 4H

### 4.3 Smoke Constraints & Retention Rules
- **sol_smoke:** Kill if: KAMA implementation; VIDYA/CMO; McGinley+T3 hybrid; 15m $N=6$. Prefer Mode A, $N=14$, 1H+.
- **sol_retention_note:** MD must hug SOL impulse (not flat while close runs away for many bars); verify hugging behavior before declaring dual failure.
- **bnb_smoke:** Kill if: different $N$ than SOL; Mode B ungated shorts; T3/ADX grafts. Prefer identical $N$; long-only; ATR exit.
- **Forbidden:** KAMA, VIDYA, SuperTrend, ADX, RSI, McGinley+T3 hybrid.

---

## 5. Summary of Locked Sweep Grid (3 Strategies)

| Strategy ID | Primary Mode | Parameter Grid | Timeframes |
|---|---|---|---|
| `frama-fast-slow-cross-v1` | Mode A (fast×slow) | $(16,32), (10,20), (12,24)$, Mode B ($N=20$) | 1H, 4H |
| `hma-dual-cross-v1` | Mode A (fast×slow) | $(9,16), (10,30), (16,36)$, Mode B ($Ls=30$) | 1H, 4H |
| `mcginley-close-slope-cross-v1` | Mode A (close×MD + slope) | $N \in \{10, 14, 20\}$, Mode B ($N=14$) | 1H, 4H |

Total parameter variations per asset: 4 (FRAMA) + 4 (HMA) + 4 (McGinley) = 12 cells across 2 timeframes = 24 cells per asset.
Ladder progression: BTC (24 cells) $\to$ ETH (passed cells) $\to$ SOL (passed cells + retention checks) $\to$ BNB (passed cells).
