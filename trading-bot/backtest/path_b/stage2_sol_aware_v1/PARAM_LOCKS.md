# stage2-sol-aware-v1 — Parameter Locks Specification

**Status:** LOCKED BEFORE STRATEGY EXECUTION AND SCORING  
**Date (UTC):** 2026-09-17  
**Research ID:** `stage2-sol-aware-v1`  
**Authoritative Briefs:** `CODING_KICK_187d.md` & `stage2-sol-aware-briefs-2026-09-17_6837.md`

---

## 1. Governance & Anti-Curve-Fitting Rule

To avoid post-hoc overfitting and ensure strict methodological hygiene per Path B Stage 2 guidelines, all critical parameter spaces for Strategy 3 (`alma-fast-slow-cross-v1`) and Strategy 5 (`ehlers-roofing-zero-cross-v1`) are locked **before** scoring any assets on the ladder.

---

## 2. Strategy 3 (`alma-fast-slow-cross-v1`) Parameter Locks

### Gaussian Filter Specification (FIR Fallback)
ALMA (Arnaud Legoux Moving Average) is computed using a Gaussian filter distribution:
$$\text{weight}_i = \exp\left(-\frac{(i - m)^2}{2 s^2}\right)$$
where:
- $m = \text{offset} \times (\text{len} - 1)$ (controls lag vs responsiveness, shifting weight center towards the latest bar)
- $s = \text{len} / \text{sigma}$ (controls Gaussian curve width / smoothing degree)
- $\text{ALMA} = \frac{\sum_{i=0}^{\text{len}-1} \text{weight}_i \cdot \text{price}[i]}{\sum_{i=0}^{\text{len}-1} \text{weight}_i}$

### Locked Parameters
1. **Sigma:** Fixed at **`6.0`** across all primary runs (canonical LuxAlgo / TradingView Arnaud Legoux default).
2. **Offset:** Primary baseline locked at **`0.85`** (sweep alternative locked at **`0.90`**).
3. **Dual MA Pairs (Fast, Slow):**
   - Locked pair 1: `(9, 21)` (fast turn capture)
   - Locked pair 2: `(20, 50)` (intermediate swing)
   - Locked pair 3: `(60, 120)` (macro trend)
4. **Timeframes:** 1H and 4H primary (emphasizing SOL touch density).
5. **Mode:** Mode A (Fast ALMA crossover / crossunder Slow ALMA).

---

## 3. Strategy 5 (`ehlers-roofing-zero-cross-v1`) Parameter Locks

### Transfer Function Specification (2-Pole HighPass + 2-Pole SuperSmoother IIR)
Per John Ehlers (*Cycle Analytics for Traders*, MESA Papers):
1. **2-Pole HighPass Filter (`hp_period`):**
   Removes spectral dilation and trend cycles longer than `hp_period`:
   $$\alpha_1 = \frac{\cos(0.707 \cdot 2\pi / \text{hp}) + \sin(0.707 \cdot 2\pi / \text{hp}) - 1}{\cos(0.707 \cdot 2\pi / \text{hp})}$$
   $$c_1 = (1 - \alpha_1 / 2)^2$$
   $$c_2 = 2 (1 - \alpha_1)$$
   $$c_3 = -(1 - \alpha_1)^2$$
   $$\text{HP}[t] = c_1 \cdot (\text{price}[t] - 2\text{price}[t-1] + \text{price}[t-2]) + c_2 \cdot \text{HP}[t-1] + c_3 \cdot \text{HP}[t-2]$$

2. **2-Pole SuperSmoother Filter (`ss_period`):**
   Attenuates high-frequency aliasing noise on the high-passed series:
   $$a_1 = \exp(-\sqrt{2}\pi / \text{ss})$$
   $$b_1 = 2 a_1 \cos(\sqrt{2}\pi / \text{ss})$$
   $$c_2 = b_1, \quad c_3 = -a_1^2, \quad c_1 = 1 - c_2 - c_3$$
   $$\text{Roofing}[t] = c_1 \cdot \frac{\text{HP}[t] + \text{HP}[t-1]}{2} + c_2 \cdot \text{Roofing}[t-1] + c_3 \cdot \text{Roofing}[t-2]$$

### Locked (hp, ss) Pairs Before Full Ladder
The three discrete parameter pairs are locked prior to ladder execution:
1. **Lead Default:** `(hp=48, ss=10)` (canonical Ehlers / MESA / QuantWave specification)
2. **Alternative Fast:** `(hp=40, ss=10)` (denser cycle capture)
3. **Alternative Wide:** `(hp=80, ss=40)` (Stonehill confirmation configuration)

No other (hp, ss) combinations are permitted during the ladder sweep.
- **Timeframes:** 1H and 4H primary.
- **Mode:** Mode A (closed-bar zero-line cross: long when Roofing > 0 and prior <= 0; short/flat when Roofing < 0).

---

## 4. Other Strategy Parameter Locks

### 1. `pwh-pwl-accept-break-v1`
- **Week Definition:** Strict Monday 00:00 UTC to next Monday 00:00 UTC.
- **RVOL:** `volume > k * SMA(volume, 20)` with $k \in \{0.0\text{ (off)}, 1.0, 1.5\}$.
- **Execution TF:** 15m and 1H.
- **Modes:** Mode A (accept-break) and Mode B (break + retest hold).

### 2. `ehlers-cg-osc-trigger-v1`
- **FIR Formula:** $Price = hl2$; $\text{CG} = -\sum_{i=0}^{\text{len}-1} (1 + i) \cdot Price[i] / \sum_{i=0}^{\text{len}-1} Price[i]$
- **Trigger:** $\text{CG}[1]$ (1-bar delayed trigger)
- **Lengths:** $L \in \{8, 10, 14, 20\}$, default $L=10$.
- **Timeframes:** 1H and 4H.

### 4. `cmo-zero-cross-v1`
- **Formula:** $\text{CMO} = 100 \times (S_u - S_d) / (S_u + S_d)$ over $L$ bars (sum of positive and negative close deltas).
- **Strategy ID:** Strictly `cmo-zero-cross-v1` (≠ `cmo-zone-v1`).
- **Lengths:** $L \in \{14, 20, 25\}$, default $L=20$.
- **Modes:** Mode A (cross above/below 0) and Mode B (cross above/below SMA(CMO, 9)).
- **Rule:** Do NOT encode leave -50 oversold zone.
