# stage4-bnb-first-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-17  
**Research ID:** `stage4-bnb-first-v1`  
**Authoritative Briefs:** `CODING_KICK_9e48.md` & `stage4-bnb-first-briefs-2026-09-17_4fe4.md`

---

## 1. Governance & Methodological Hygiene

To prevent post-hoc curve fitting and enforce BNB-survival-FIRST hygiene per Path B Stage 4 directives:
- All indicator mathematical forms, symbol-specific constants, and parameter grids are locked **before** scoring any assets on the stop-ladder (BTC → ETH → SOL → BNB).
- **Stop-ladder rule:** BTC first; PASS_6m Mode-A return $\ge 1.2\times$ B&H $\to$ ETH $\to$ SOL (HARD) $\to$ BNB (HARD).
- **Mandatory BNB smoke test:** Each strategy must satisfy its dedicated BNB smoke constraints before parameter cells are promoted or evaluated on the BNB ladder. Any failed smoke condition is logged with explicit reasons.
- **Closed-bar execution only** (`process_orders_on_close = True`).
- **No `request.security`:** Higher timeframe levels (such as 4H boundaries) are tracked via running session-reset state machines on the execution timeframe.
- **No burned filters or grafts:** Excludes Donchian, ConnorsRSI, OBV, CMF, MFI, Chaikin Osc, Klinger, VWMA, MACD/PPO primary, EMA ribbon, SMA200, PDH/PDL, PWH/PWL, PHH/PHL, Session ORB, ALMA, T3, Hull, Decycler, and ITrend.

---

## 2. Locked Strategy 1 (`rvol-pivot-structure-break-v1`)

### 2.1 Formulation
- **RVOL:**
  $$\text{RVOL}_t = \frac{\text{Volume}_t}{\text{SMA}(\text{Volume}, \text{volLen})_t}, \quad \text{volLen} \in \{20, 50\}$$
- **Structure Mode A (Preferred):**
  - Confirmed swing pivots: $\text{pivothigh}(\text{high}, lb, rb)$ and $\text{pivotlow}(\text{low}, lb, rb)$ with $lb = rb \in \{2, 3\}$.
  - Confirmation occurs after $rb$ bars. The active reference level is the most recently confirmed pivot high.
  - Long entry: $\text{close}_t > \text{pivot\_high}$ and $\text{close}_{t-1} \le \text{pivot\_high}$ and $\text{RVOL}_t \ge k$.
  - Short entry: symmetric below confirmed pivot low.
- **Structure Mode B (Denser Lookback-Close Break):**
  - Long entry: $\text{close}_t > \text{close}_{t-L}$ and $\text{close}_{t-1} \le \text{close}_{t-L}$ and $\text{RVOL}_t \ge k$, with $L \in \{5, 10, 20\}$.
  - Distinct from Donchian channel: strictly tests $\text{close} > \text{close}[L]$, **not** $\text{ta.highest}(\text{high}, n)$.
- **Execution Timeframes:** 1H and 4H.
- **Exit:**
  - Close back through structure level or opposite signal, with optional ATR trail stop.

### 2.2 Locked Parameter Space
- $k \in \{1.2, 1.5, 2.0\}$
- $\text{volLen} \in \{20, 50\}$
- Structure modes: Mode A ($lb=rb=2, 3$) and Mode B ($L \in \{5, 10, 20\}$)
- Timeframes: 1H, 4H

### 2.3 BNB Smoke Constraints (Mandatory)
- **RVOL Floor:** $k \ge 1.5$ required on BNB.
- **ATR% Floor:** Skip breakout if bar range $(\text{high} - \text{low}) < 0.15 \times \text{ATR}(14)$ or bar range $/ \text{close} < 0.002$.
- **Zero-Volume Filter:** Skip bars where $\text{volume} == 0$.
- **Timeframe:** 1H+ only (no 15m on BNB).
- **Mode B restriction:** Mode B with $L < 10$ is rejected on BNB smoke due to noise flood.

---

## 3. Locked Strategy 2 (`emv-zero-rvol-atr-gate-v1`)

### 3.1 Formulation
- **Ease of Movement (Arms EMV / `ta.eom`):**
  $$\text{DistanceMoved}_t = \frac{\text{high}_t + \text{low}_t}{2} - \frac{\text{high}_{t-1} + \text{low}_{t-1}}{2}$$
  $$\text{BoxRatio}_t = \frac{\text{Volume}_t / \text{div}}{\text{high}_t - \text{low}_t}$$
  $$\text{EMV\_Raw}_t = \frac{\text{DistanceMoved}_t}{\text{BoxRatio}_t}$$
  $$\text{EMV}_t = \text{SMA}(\text{EMV\_Raw}, \text{eomLen})_t$$
- **Pre-Scoring Symbol Divisor Lock:**
  To maintain comparable scale across symbols with vastly different price and volume ranges, `div` is locked per symbol prior to length sweeps:
  - `BTCUSDT`: $\text{div} = 10,000,000$ ($10^7$)
  - `ETHUSDT`: $\text{div} = 10,000,000$ ($10^7$)
  - `SOLUSDT`: $\text{div} = 100,000,000$ ($10^8$)
  - `BNBUSDT`: $\text{div} = 10,000,000$ ($10^7$) — rescaled to prevent box ratio saturation.
- **Entry Mode A (Zero Cross):**
  - Long: $\text{crossover}(\text{EMV}, 0)$ **and** $\text{RVOL} \ge k$ **and** $(\text{high} - \text{low}) / \text{close} \ge \text{atrPctMin}$.
  - Short: $\text{crossunder}(\text{EMV}, 0)$ **and** same participation gates.
- **Entry Mode B (Signal Line Cross):**
  - $\text{EMV} \times \text{SMA}(\text{EMV}, 9)$ crossover with same participation gates.
- **Exit:**
  - Opposite gated cross or ATR trailing stop.

### 3.2 Locked Parameter Space
- $\text{eomLen} \in \{10, 14, 20\}$
- $k \in \{1.0, 1.5\}$
- $\text{atrPctMin} \in \{0.0\text{ (off)}, 0.002, 0.004\}$
- Timeframes: 1H, 4H

### 3.3 BNB Smoke Constraints (Mandatory)
- **Never ungated:** Ungated zero-crosses are strictly banned.
- **Divisor verification:** Divisor must be verified per symbol; copying BTC divisor without verifying BNB scale fails smoke.
- **RVOL floor:** $k \ge 1.5$ required on BNB.
- **ATR% floor:** $\text{atrPctMin} \ge 0.002$ required on BNB.
- **Zero-Volume Filter:** Skip bars where $\text{volume} == 0$.
- **Timeframe:** 1H+ required.

---

## 4. Locked Strategy 3 (`pvo-gate-sma-mom-v1`)

### 4.1 Formulation
- **Percentage Volume Oscillator (PVO):**
  $$\text{fastV}_t = \text{EMA}(\text{Volume}, 12)_t, \quad \text{slowV}_t = \text{EMA}(\text{Volume}, 26)_t$$
  $$\text{PVO}_t = 100 \times \frac{\text{fastV}_t - \text{slowV}_t}{\text{slowV}_t}$$
  $$\text{Signal}_t = \text{EMA}(\text{PVO}, 9)_t$$
- **Participation Gates:**
  - Gate 1 (Primary): $\text{PVO}_t > 0$
  - Gate 2 (Alternative): $\text{PVO}_t > \text{PVO}_{t-1}$ and $\text{PVO}_t > \text{Signal}_t$
- **Momentum Entry Mode A (Price Cross):**
  - Long: $\text{crossover}(\text{close}, \text{SMA}(\text{close}, \text{len}))$ while Gate is True.
- **Momentum Entry Mode B (State Entry):**
  - Long: $\text{close} > \text{SMA}(\text{close}, \text{len})$ and Gate is True (first bar condition becomes true).
- **Moving Average Length:**
  - $\text{len} \in \{10, 20, 34\}$ — length 200 is strictly excluded (SMA200 burned).
- **Exit Rules:**
  - Opposite momentum cross OR **Gate Loss** ($\text{crossunder}(\text{PVO}, 0)$).
  - `exit_on_gate_loss = True` is **mandatory** for BNB smoke.

### 4.2 Locked Parameter Space
- Gate variants: `pvo > 0` vs `pvo > sig`
- $\text{len} \in \{10, 20, 34\}$
- Modes: Mode A (crossover) vs Mode B (state entry)
- Timeframes: 1H, 4H

### 4.3 BNB Smoke Constraints (Mandatory)
- **`exit_on_gate_loss = True`** is mandatory on BNB.
- **Price momentum required:** PVO cannot be used as sole directional entry.
- **Length bound:** $\text{len} \le 34$ (no SMA 200).
- **Timeframe:** 1H+ required.
- **Zero-Volume Filter:** Skip bars where $\text{volume} == 0$.

---

## 5. Locked Strategy 4 (`p4h-hl-accept-break-v1`)

### 5.1 Formulation
- **UTC 4-Hour Bucket Boundaries:**
  - 4H buckets reset at UTC 00:00, 04:00, 08:00, 12:00, 16:00, 20:00.
  - Tracking mechanism: running high and low are accumulated on the execution timeframe bar-by-bar.
  - When crossing a 4H UTC boundary (`floor(time_ms / 14_400_000)` advances), the completed bucket's high and low are frozen into `P4H_High` and `P4H_Low`.
  - **No `request.security`:** Fully compliant with closed-bar execution and intra-timeframe state tracking.
- **Entry Mode A (Accept-Break):**
  - Long: $\text{close}_t > \text{P4H\_High}$ and $\text{close}_{t-1} \le \text{P4H\_High}$.
  - Must be a full **closed bar** beyond the level (wick-only accept is invalid).
  - Optional RVOL gate: $\text{volume}_t > k \times \text{SMA}(\text{volume}, 20)_t$.
- **Entry Mode B (Break + Retest):**
  - After Mode A trigger, price pulls back to tag within 0.2% of `P4H_High`, then closes above with hold.
- **Exit Rules:**
  - Bar close falls back inside prior 4H range ($\text{close} < \text{P4H\_High}$), or opposite level hit, or ATR trailing stop.

### 5.2 Locked Parameter Space
- Modes: Mode A (accept-break) vs Mode B (break + retest)
- RVOL $k \in \{0.0\text{ (off)}, 1.2, 1.5\}$
- One-trade-per-4H-bucket: True / False
- Execution Timeframes: 15m, 1H (prefer 1H for BNB)

### 5.3 BNB Smoke Constraints (Mandatory)
- **RVOL ON by default:** $k \ge 1.5$ required on BNB.
- **Closed-bar beyond only:** Wick breaks strictly rejected.
- **Timeframe:** Prefer 1H execution on BNB; 15m requires $k \ge 1.5$.
- **ATR% floor:** Skip if $(\text{P4H\_High} - \text{P4H\_Low}) / \text{close} < 0.002$.

---

## 6. Locked Strategy 5 (`zlema-sma-cross-v1`)

### 6.1 Formulation
- **Lag-Compensated Zero-Lag EMA (Canonical Form):**
  $$\text{lag} = \text{round}\left(\frac{\text{len} - 1}{2}\right)$$
  $$\text{src\_comp}_t = \text{close}_t + (\text{close}_t - \text{close}_{t - \text{lag}})$$
  $$\text{ZLEMA}_t = \text{EMA}(\text{src\_comp}, \text{len})_t$$
  - **Strict exclusion:** This is the canonical lag-compensation form, **NOT** the 2010 Ehlers-Way Error-Correction (EC) gain-search form $\text{EMA} + (\text{EMA} - \text{EMA}(\text{EMA}))$.
- **Slow Line:** Simple Moving Average $\text{SMA}(\text{close}, \text{lenS})$.
- **Entry Mode A (ZLEMA × SMA Cross):**
  - Long: $\text{crossover}(\text{ZLEMA}, \text{SMA})$.
  - Short / Flat: $\text{crossunder}(\text{ZLEMA}, \text{SMA})$.
- **Entry Mode B (Dual ZLEMA):**
  - $\text{crossover}(\text{ZLEMA}_{\text{fast}}, \text{ZLEMA}_{\text{slow}})$ (deferred until after Mode A baseline).
- **RVOL Gate:**
  - $\text{volume}_t \ge k \times \text{SMA}(\text{volume}, 20)_t$ on cross bar.
  - **Mandatory on BNB smoke** ($k \ge 1.2$).
- **Exit:**
  - Opposite crossover or ATR trailing stop.

### 6.2 Locked Parameter Space
- Length Pairs $(\text{lenZ}, \text{lenS}) \in \{(10, 30), (20, 50), (34, 89)\}$
- Preferred baseline before sweep: `(20, 50)`
- RVOL $k \in \{0.0\text{ (off)}, 1.2, 1.5\}$ (BNB requires $k \ge 1.2$)
- Timeframes: 1H, 4H

### 6.3 BNB Smoke Constraints (Mandatory)
- **RVOL Gate Required:** $k \ge 1.2$ mandatory on BNB.
- **Timeframe:** 1H+ required (no 15m).
- **Form:** Strictly lag-compensation form (no EC gain forms).
- **Length pair baseline:** (20, 50) evaluated first.
