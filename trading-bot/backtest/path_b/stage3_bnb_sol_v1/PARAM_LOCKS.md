# stage3-bnb-sol-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-17  
**Research ID:** `stage3-bnb-sol-v1`  
**Authoritative Briefs:** `CODING_KICK_3ec4.md` & `stage3-bnb-sol-briefs-2026-09-17_29bd.md`

---

## 1. Governance & Anti-Curve-Fitting Rule

To prevent post-hoc curve fitting and ensure strict methodological hygiene per Path B Stage 3 guidelines, all critical parameter spaces for Strategy 3 (`t3-dual-cross-v1`) and Strategy 5 (`itrend-trigger-v1`), as well as the filter definitions for Strategy 1, 2, and 4, are documented and locked **before** scoring any assets on the stop-ladder (BTC -> ETH -> SOL -> BNB).

---

## 2. Strategy 3 (`t3-dual-cross-v1`) Parameter Locks

### Tillson T3 Moving Average Specification
Tim Tillson, *Smoothing Techniques For More Accurate Signals* (TASC Jan 1998):
The Generalized DEMA (GD) operator with volume factor $v$ is defined as:
$$\text{GD}(x, \text{len}, v) = (1 + v) \cdot \text{EMA}(x, \text{len}) - v \cdot \text{EMA}(\text{EMA}(x, \text{len}), \text{len})$$
The T3 moving average is the triple composition of GD:
$$\text{T3}(x, \text{len}, v) = \text{GD}(\text{GD}(\text{GD}(x, \text{len}, v), \text{len}, v), \text{len}, v)$$
Equivalently, expanding into a 6-EMA cascade:
$$e_1 = \text{EMA}(x), \quad e_2 = \text{EMA}(e_1), \quad e_3 = \text{EMA}(e_2), \quad e_4 = \text{EMA}(e_3), \quad e_5 = \text{EMA}(e_4), \quad e_6 = \text{EMA}(e_5)$$
$$c_1 = -v^3$$
$$c_2 = 3v^2 + 3v^3$$
$$c_3 = -6v^2 - 3v - 3v^3$$
$$c_4 = 1 + 3v + v^3 + 3v^2$$
$$\text{T3} = c_1 \cdot e_6 + c_2 \cdot e_5 + c_3 \cdot e_4 + c_4 \cdot e_3$$

### Locked Parameters Before Scoring
1. **Volume Factor ($vFactor$):**
   - **Primary Lock:** $vFactor = \mathbf{0.7}$ (standard Tillson/TradingView default, locked prior to length sweep).
   - **Alternative Lock:** $vFactor = \mathbf{0.5}$ (lower overshoot setting).
   - No arbitrary intermediate values are permitted.
2. **Dual Moving Average Length Pairs (Fast, Slow):**
   - Locked pair 1: `(5, 15)` (rapid turns)
   - Locked pair 2: `(8, 21)` (intermediate trend)
   - Locked pair 3: `(10, 30)` (macro swing)
3. **Timeframes:** 1H and 4H primary (emphasizing SOL+BNB touch density).
4. **Mode:** Mode A (Fast T3 crossover / crossunder Slow T3).
5. **Forbidden Grafts:** No ALMA, EMA ribbon/stack, Hull primary, or SMA200/RSI filters.

---

## 3. Strategy 5 (`itrend-trigger-v1`) Parameter Locks

### Simplified Ehlers Instantaneous Trendline Specification
The implementation strictly follows the simplified Pine/Ehlers IIR form (blackcat / LazyBear / LuxAlgo) with price $hl2 = (\text{high} + \text{low})/2$, **NOT** the 2002 MESA elliptic/notch DLL form:

1. **Seed / Warmup (first 7 bars):**
   For $t < 2$: $\text{ITrend}[t] = \text{Price}[t]$
   For $2 \le t < 7$:
   $$\text{ITrend}[t] = \frac{\text{Price}[t] + 2 \cdot \text{Price}[t-1] + \text{Price}[t-2]}{4}$$

2. **IIR Recursion ($t \ge 7$):**
   $$\text{ITrend}[t] = \left(\alpha - \frac{\alpha^2}{4}\right) \text{Price}[t] + \frac{\alpha^2}{2} \text{Price}[t-1] - \left(\alpha - \frac{3\alpha^2}{4}\right) \text{Price}[t-2] + 2(1 - \alpha) \text{ITrend}[t-1] - (1 - \alpha)^2 \text{ITrend}[t-2]$$

3. **Lead Trigger:**
   $$\text{Trigger}[t] = 2 \cdot \text{ITrend}[t] - \text{ITrend}[t-2]$$

### Locked Parameters Before Scoring
1. **Alpha ($\alpha$):**
   - **Primary Hard Lock:** $\alpha = \mathbf{0.07}$ locked before any scoring.
   - **Optional sweep:** $\alpha \in \{0.05, 0.07, 0.10\}$ permitted **only** after BTC smoke baseline.
2. **Entry Mode:** Mode A (closed-bar `ta.crossover(Trigger, ITrend)`; short/flat on `ta.crossunder(Trigger, ITrend)`). Mode B (4-bar WMA) deferred.
3. **Timeframes:** 1H and 4H primary.
4. **Forbidden Grafts:** No MESA DLL / dominant-cycle adaptive notch primary, SuperTrend, EMA grafts, Roofing, or CG.

---

## 4. Strategy 4 (`decycler-osc-fast-slow-v1`) Parameter Locks

### Ehlers Decycler Oscillator Specification (TASC Sep 2015)
1. **High-Pass Filter:**
   $$\alpha_1 = \frac{\cos(0.707 \cdot 2\pi / P) + \sin(0.707 \cdot 2\pi / P) - 1}{\cos(0.707 \cdot 2\pi / P)}$$
   $$\text{HP}[t] = (1 - \alpha_1/2)^2 (\text{Price}[t] - 2\text{Price}[t-1] + \text{Price}[t-2]) + 2(1 - \alpha_1)\text{HP}[t-1] - (1 - \alpha_1)^2\text{HP}[t-2]$$
   $$\text{Decycle}[t] = \text{Price}[t] - \text{HP}[t]$$

2. **Decycler Oscillator:**
   Second high-pass filter applied to $\text{Decycle}$ at cutoff $0.5 \cdot P$:
   $$\alpha_2 = \frac{\cos(0.707 \cdot 2\pi / (0.5 P)) + \sin(0.707 \cdot 2\pi / (0.5 P)) - 1}{\cos(0.707 \cdot 2\pi / (0.5 P))}$$
   $$\text{DecycleOsc}[t] = (1 - \alpha_2/2)^2 (\text{Decycle}[t] - 2\text{Decycle}[t-1] + \text{Decycle}[t-2]) + 2(1 - \alpha_2)\text{DecycleOsc}[t-1] - (1 - \alpha_2)^2\text{DecycleOsc}[t-2]$$
   $$\text{Osc}[t] = 100 \cdot K \cdot \frac{\text{DecycleOsc}[t]}{\text{Price}[t]}$$

### Locked Parameters Before Scoring
1. **Multiplier ($K$):** Locked pair $(K_{\text{fast}}=1.2, K_{\text{slow}}=1.0)$.
2. **Period Pairs $(P_{\text{fast}}, P_{\text{slow}})$:**
   - Canonical Ehlers: `(100, 125)`
   - Crypto 1H Scaled: `(50, 63)`
   - Crypto Rapid: `(40, 50)`
3. **Timeframes:** 1H and 4H primary.
4. **Mode:** Mode A (`crossover(fast_osc, slow_osc)`).

---

## 5. Strategy 1 (`vwma-sma-cross-v1`) Parameter Locks

1. **Indicator Definitions:**
   $$\text{VWMA}(close, L) = \frac{\sum_{i=0}^{L-1} close_i \cdot volume_i}{\sum_{i=0}^{L-1} volume_i}, \quad \text{SMA}(close, L) = \frac{1}{L} \sum_{i=0}^{L-1} close_i$$
2. **Lengths:**
   - Same-length pairs: $L \in \{10, 20, 34, 50\}$ (VWMA vs SMA of same length)
   - Fast/Slow pairs: $(L_v, L_s) \in \{(10, 20), (20, 50)\}$
3. **Modes:** Mode A (crossover) and Mode B (vwma > sma and close above both).
4. **Timeframes:** 1H and 4H.

---

## 6. Strategy 2 (`phh-phl-accept-break-v1`) Parameter Locks

1. **Levels:** Prior UTC clock-hour high (PHH) and low (PHL) tracked via UTC wall-clock hour boundary (`open_time_ms // 3_600_000 * 3_600_000`).
2. **Modes:** Mode A (accept-break: close > PHH after prior close <= PHH) and Mode B (break + retest hold).
3. **RVOL Gate:** $volume > k \cdot \text{SMA}(volume, 20)$ on break bar with $k \in \{0.0\text{ (off)}, 1.0, 1.5\}$.
4. **Execution Timeframes:** 15m and 1H.
