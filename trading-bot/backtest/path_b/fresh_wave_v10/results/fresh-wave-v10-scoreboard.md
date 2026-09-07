# fresh-wave-v10 scoreboard

Generated (UTC): 2026-09-07T09:26:22.537203+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring

- **LEAD gate:** 6m Mode-A ≥ **1.2×** B&H → `PASS/FAIL_6m` (≥1 trade). WR informational.
- **Also:** full(~2y) Mode-A ≥ **1.2×** B&H → `PASS/FAIL_full` (informational)
- Costs: 0.10%/side fee + 5 bps slip; Mode-A **100%** + Mode-B ops **2.5%** (ops not scored)
- Symbol: BTCUSDT only (no ETH OOS in this PR). **SOL is the hard OOS filter** — deferred; BTC scoreboard first.
- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Reuse `mtf_ohlcv`.
- VWAP UTC σ: reset 00:00 UTC; ±2σ bands; Mode A tag −2σ reclaim; Mode B reclaim above VWAP; exit VWAP/EOD. TF 15m–1h. ≠ BB.
- SMI Blau: N=**13** smooth **3/3** sig **3**; OB/OS ±**40**; Mode A ×sig/0; Mode B OS reclaim. TF 15m–4h. Forbidden Stoch/Connors/RSI.
- Woodie UTC: prior UTC day P=(H+L+2C)/4; Mode A fade S1 (SL S2); Mode B close>R1. TF 5m–1h. ≠ Camarilla; ≠ Session ORB.
- Chaikin Osc: EMA(**3**)−EMA(**10**) of ADL zero-cross. TF 15m–4h. Forbidden CMF/OBV/MFI twin.
- Laguerre price: γ=**0.8** on close; price×filter cross. TF 1h–4h. Forbidden Laguerre RSI / EMA×RSI.
- Parked: Klinger, VR+breakout, % Envelopes — not this wave.
- Watchlist (no paper): ema-rsi@9h, schaff@2d. v9 hard-stop 0 PASS_6m. Hold #15–#27 unmerged.

## Strategy rules (documented)

1. **vwap-utc-sigma-v1** — Mode A: tag −2σ then reclaim toward VWAP; Mode B: close reclaim above VWAP; exit VWAP touch / EOD UTC.
2. **smi-blau-v1** — Mode A: crossover(SMI, signal) OR cross above 0; Mode B: was ≤−40 then cross >−40; exit ×signal / mid-0 / ≥+40.
3. **woodie-utc-v1** — Mode A: fade S1 long SL=S2 exit P/R1; Mode B: close>R1 exit ≤P or EOD.
4. **chaikin-osc-v1** — crossover(Osc, 0) / crossunder(Osc, 0).
5. **laguerre-price-v1** — close crossover above Laguerre / crossunder below.

## PASS_6m cells (LEAD)

_none_

## PASS_full cells (informational; not LEAD)

_none_

## LEAD 6m by family (all scored cells)

### vwap-utc-sigma-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 1h|mode_a|tag-2sig|sig2 | FAIL(-2.39) | -42.90 | 17.97 | -2.387 | 19.1 | 183 | FAIL(-1.88) | -1.884 | 731 | -1.38 | -5.68 |  |
| 1h|mode_b|reclaim-vwap|sig2 | FAIL(-2.41) | -43.35 | 17.97 | -2.413 | 14.5 | 173 | FAIL(-1.79) | -1.789 | 700 | -1.40 | -4.71 |  |
| 30m|mode_a|tag-2sig|sig2 | FAIL(-2.05) | -38.79 | 18.93 | -2.049 | 12.6 | 183 | FAIL(-1.82) | -1.822 | 731 | -1.22 | -4.95 |  |
| 30m|mode_b|reclaim-vwap|sig2 | FAIL(-2.13) | -40.34 | 18.93 | -2.131 | 14.1 | 177 | FAIL(-1.77) | -1.769 | 716 | -1.27 | -4.50 |  |
| 15m|mode_a|tag-2sig|sig2 | FAIL(-2.11) | -39.88 | 18.91 | -2.109 | 10.4 | 183 | FAIL(-1.82) | -1.821 | 731 | -1.26 | -5.23 |  |
| 15m|mode_b|reclaim-vwap|sig2 | FAIL(-2.36) | -44.62 | 18.91 | -2.360 | 10.5 | 181 | FAIL(-1.82) | -1.819 | 728 | -1.46 | -5.19 |  |

### smi-blau-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 4h|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-0.70) | -14.35 | 20.35 | -0.705 | 40.7 | 81 | FAIL(-1.34) | -1.335 | 342 | -0.36 | -2.33 |  |
| 4h|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(0.09) | 1.87 | 20.35 | 0.092 | 63.6 | 33 | FAIL(-0.78) | -0.784 | 130 | 0.06 | -1.08 |  |
| 3h|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-1.55) | -31.59 | 20.41 | -1.548 | 35.9 | 117 | FAIL(-1.71) | -1.705 | 486 | -0.92 | -3.96 |  |
| 3h|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(-0.33) | -6.68 | 20.41 | -0.327 | 42.5 | 40 | FAIL(-0.84) | -0.841 | 170 | -0.16 | -1.20 |  |
| 2h|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-1.70) | -31.49 | 18.47 | -1.705 | 36.3 | 179 | FAIL(-1.85) | -1.850 | 721 | -0.91 | -4.87 |  |
| 2h|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(-1.28) | -23.55 | 18.47 | -1.275 | 38.1 | 63 | FAIL(-1.26) | -1.257 | 269 | -0.65 | -2.13 |  |
| 1h|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-3.76) | -67.57 | 17.97 | -3.760 | 26.6 | 383 | FAIL(-2.05) | -2.052 | 1480 | -2.74 | -10.04 |  |
| 1h|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(-1.81) | -32.47 | 17.97 | -1.807 | 33.9 | 124 | FAIL(-1.54) | -1.541 | 524 | -0.96 | -3.24 |  |
| 90m|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-2.82) | -51.11 | 18.14 | -2.817 | 29.8 | 248 | FAIL(-1.91) | -1.907 | 949 | -1.74 | -5.47 |  |
| 90m|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(-0.91) | -16.53 | 18.14 | -0.911 | 43.8 | 80 | FAIL(-1.19) | -1.192 | 346 | -0.43 | -1.97 |  |
| 30m|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-4.58) | -86.79 | 18.93 | -4.585 | 24.7 | 740 | FAIL(-2.09) | -2.093 | 2941 | -4.91 | -19.48 |  |
| 30m|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(-3.08) | -58.31 | 18.93 | -3.080 | 27.9 | 269 | FAIL(-2.03) | -2.033 | 1074 | -2.15 | -8.40 |  |
| 15m|mode_a|xsig-or-0|n13|sm3/3|sig3|ob40 | FAIL(-5.20) | -98.30 | 18.91 | -5.199 | 18.5 | 1441 | FAIL(-2.06) | -2.058 | 5963 | -9.66 | -35.38 |  |
| 15m|mode_b|os-40-reclaim|n13|sm3/3|sig3|ob40 | FAIL(-4.27) | -80.71 | 18.91 | -4.268 | 19.7 | 605 | FAIL(-2.06) | -2.056 | 2243 | -4.01 | -15.40 |  |

### woodie-utc-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 1h|mode_a|fadeS1 | FAIL(-1.26) | -22.58 | 17.97 | -1.257 | 47.5 | 61 | FAIL(-1.16) | -1.157 | 255 | -0.62 | -1.94 |  |
| 1h|mode_b|breakR1 | FAIL(-0.19) | -3.42 | 17.97 | -0.190 | 35.4 | 65 | FAIL(-0.71) | -0.714 | 244 | -0.07 | -0.97 |  |
| 30m|mode_a|fadeS1 | FAIL(-1.44) | -27.28 | 18.93 | -1.441 | 40.6 | 64 | FAIL(-1.29) | -1.287 | 267 | -0.78 | -2.28 |  |
| 30m|mode_b|breakR1 | FAIL(-0.47) | -8.91 | 18.93 | -0.471 | 33.8 | 68 | FAIL(-0.75) | -0.754 | 259 | -0.22 | -1.02 |  |
| 15m|mode_a|fadeS1 | FAIL(-1.41) | -26.74 | 18.91 | -1.414 | 43.8 | 64 | FAIL(-1.34) | -1.336 | 273 | -0.76 | -2.51 |  |
| 15m|mode_b|breakR1 | FAIL(-0.45) | -8.49 | 18.91 | -0.449 | 32.4 | 71 | FAIL(-0.80) | -0.803 | 270 | -0.20 | -1.13 |  |
| 10m|mode_a|fadeS1 | FAIL(-1.47) | -27.69 | 18.80 | -1.473 | 41.8 | 67 | FAIL(-1.20) | -1.203 | 273 | -0.80 | -2.09 |  |
| 10m|mode_b|breakR1 | FAIL(-0.57) | -10.74 | 18.80 | -0.571 | 31.9 | 72 | FAIL(-0.65) | -0.653 | 272 | -0.27 | -0.85 |  |
| 5m|mode_a|fadeS1 | FAIL(-1.52) | -28.49 | 18.71 | -1.523 | 42.0 | 69 | FAIL(-1.40) | -1.400 | 285 | -0.82 | -2.71 |  |
| 5m|mode_b|breakR1 | FAIL(-0.51) | -9.53 | 18.71 | -0.509 | 31.1 | 74 | FAIL(-0.74) | -0.743 | 279 | -0.23 | -1.01 |  |

### chaikin-osc-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 4h|ema3-10|adl-zx | FAIL(-0.19) | -3.80 | 20.35 | -0.187 | 33.9 | 62 | FAIL(-0.90) | -0.903 | 248 | -0.03 | -1.06 |  |
| 3h|ema3-10|adl-zx | FAIL(-0.24) | -4.88 | 20.41 | -0.239 | 31.5 | 89 | FAIL(-1.17) | -1.167 | 340 | -0.07 | -1.71 |  |
| 2h|ema3-10|adl-zx | FAIL(-1.80) | -33.22 | 18.47 | -1.799 | 25.9 | 139 | FAIL(-1.75) | -1.750 | 523 | -0.93 | -4.02 |  |
| 1h|ema3-10|adl-zx | FAIL(-3.42) | -61.53 | 17.97 | -3.424 | 21.5 | 279 | FAIL(-2.01) | -2.012 | 1045 | -2.28 | -7.98 |  |
| 90m|ema3-10|adl-zx | FAIL(-1.75) | -31.77 | 18.14 | -1.751 | 25.1 | 175 | FAIL(-1.95) | -1.954 | 713 | -0.89 | -5.97 |  |
| 30m|ema3-10|adl-zx | FAIL(-4.36) | -82.49 | 18.93 | -4.358 | 19.4 | 547 | FAIL(-2.09) | -2.091 | 2078 | -4.21 | -15.16 |  |
| 15m|ema3-10|adl-zx | FAIL(-5.02) | -95.00 | 18.91 | -5.024 | 15.7 | 1024 | FAIL(-2.06) | -2.058 | 4182 | -7.16 | -28.21 |  |

### laguerre-price-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 4h|g0.8|price-x | FAIL(-0.42) | -8.48 | 20.35 | -0.417 | 21.7 | 46 | FAIL(-0.80) | -0.801 | 189 | -0.14 | -0.88 |  |
| 3h|g0.8|price-x | FAIL(-0.23) | -4.71 | 20.41 | -0.231 | 21.8 | 55 | FAIL(-0.79) | -0.791 | 236 | -0.05 | -0.91 |  |
| 2h|g0.8|price-x | FAIL(-0.83) | -15.31 | 18.47 | -0.829 | 21.4 | 98 | FAIL(-1.18) | -1.178 | 355 | -0.35 | -1.73 |  |
| 1h|g0.8|price-x | FAIL(-2.33) | -41.91 | 17.97 | -2.332 | 19.9 | 196 | FAIL(-1.85) | -1.854 | 789 | -1.29 | -5.17 |  |
| 90m|g0.8|price-x | FAIL(-1.43) | -26.03 | 18.14 | -1.435 | 18.0 | 139 | FAIL(-1.59) | -1.594 | 508 | -0.68 | -3.19 |  |

## Caveats

- LEAD = 6m Mode-A sizing only. full(~2y) context only.
- No param retune on 6m after freeze. Scout-wave-4 seats.
- Hold prior PRs #15–#27 unmerged; this PR is additive fresh-wave-v10 only.
- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only. **SOL = hard filter** when OOS runs.
- Watchlist (no paper): ema-rsi@9h, schaff@2d.
- v9 hard-stop 0 PASS_6m — do not revive without Strategy OK.
- Parked: Klinger, VR+breakout, % Envelopes.

## IDs frozen: vwap-utc-sigma-v1, smi-blau-v1, woodie-utc-v1, chaikin-osc-v1, laguerre-price-v1

