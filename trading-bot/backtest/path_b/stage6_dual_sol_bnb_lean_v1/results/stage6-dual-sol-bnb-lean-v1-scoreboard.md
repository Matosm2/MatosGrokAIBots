# stage6-dual-sol-bnb-lean-v1 scoreboard (DUAL-SURVIVAL + SOL RETENTION: SOL + BNB)

Generated (UTC): 2026-09-17T05:26:35.381499+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with >=1 trade -> `PASS_6m Y/N`. WR informational.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH -> SOL -> BNB. **SOL and BNB are hard filters**.
- **Dual-Survival Constraint:** Identical parameter sets across SOL and BNB (strictly no per-coin retuning).
- **Mandatory Smoke & Retention Tests:** Both sol_smoke and bnb_smoke logged; sol_retention_note checked post-ETH.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-5 IDs, no Decycler/ITrend/PVO/P4H/MAD/SS, no Roofing, no EMA/RSI, SMA200, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Ehlers FRAMA (`frama-fast-slow-cross-v1`):** Fractal dimension alpha from N1/N2/N3 halves. Locked pairs (16,32), (10,20), (12,24) (Mode A) and frama20 (Mode B). N even.
- **Hull Moving Average (`hma-dual-cross-v1`):** Low-lag WMA(2*WMA(n/2) - WMA(n), sqrt(n)). Locked pairs (9,16), (10,30), (16,36) (Mode A) and hma30 (Mode B).
- **McGinley Dynamic (`mcginley-close-slope-cross-v1`):** Adaptive speed hug via (close/MD)^4 denominator. N in {10, 14, 20} (Mode A close x MD + MD rising) and Mode B state.

## PASS_6m cells (LEAD)

_none_

## All Scored Cells by Strategy

### frama-fast-slow-cross-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | sol_retention | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|(16,32) | Y | Y | — | FAIL | -30.34% | 7.10% | -4.276x | 37.9% | 169 | FAIL | -2.528x | 645 | -0.86% | -3.91% |  |
| BTCUSDT | 1h | mode_a|(10,20) | Y | Y | — | FAIL | -46.58% | 7.10% | -6.563x | 33.7% | 187 | FAIL | -2.723x | 735 | -1.52% | -4.90% |  |
| BTCUSDT | 1h | mode_a|(12,24) | Y | Y | — | FAIL | -42.92% | 7.10% | -6.048x | 37.2% | 199 | FAIL | -2.837x | 764 | -1.35% | -5.72% |  |
| BTCUSDT | 1h | mode_b|frama20 | Y | Y | — | FAIL | -67.64% | 7.10% | -9.531x | 17.3% | 376 | FAIL | -3.079x | 1572 | -2.74% | -11.05% |  |
| BTCUSDT | 4h | mode_a|(16,32) | Y | Y | — | FAIL | -6.01% | 7.56% | -0.796x | 43.6% | 39 | FAIL | -1.331x | 154 | -0.13% | -1.14% |  |
| BTCUSDT | 4h | mode_a|(10,20) | Y | Y | — | FAIL | -24.84% | 7.56% | -3.288x | 43.5% | 46 | FAIL | -1.221x | 188 | -0.67% | -0.98% |  |
| BTCUSDT | 4h | mode_a|(12,24) | Y | Y | — | FAIL | -29.43% | 7.56% | -3.896x | 45.1% | 51 | FAIL | -1.284x | 184 | -0.83% | -1.05% |  |
| BTCUSDT | 4h | mode_b|frama20 | Y | Y | — | FAIL | -31.77% | 7.56% | -4.205x | 17.9% | 95 | FAIL | -1.908x | 371 | -0.89% | -2.01% |  |
| ETHUSDT | 1h | mode_a|(16,32) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_a|(10,20) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_a|(12,24) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_b|frama20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|(16,32) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|(10,20) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|(12,24) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_b|frama20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|(16,32) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|(10,20) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|(12,24) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_b|frama20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|(16,32) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|(10,20) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|(12,24) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_b|frama20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|(16,32) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|(10,20) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|(12,24) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_b|frama20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|(16,32) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|(10,20) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|(12,24) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_b|frama20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |

### hma-dual-cross-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | sol_retention | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|(9,16) | Y | Y | — | FAIL | -70.88% | 7.10% | -9.988x | 23.0% | 344 | FAIL | -3.052x | 1357 | -2.99% | -9.44% |  |
| BTCUSDT | 1h | mode_a|(10,30) | Y | Y | — | FAIL | -51.29% | 7.10% | -7.227x | 27.4% | 230 | FAIL | -2.894x | 889 | -1.74% | -6.27% |  |
| BTCUSDT | 1h | mode_a|(16,36) | Y | Y | — | FAIL | -41.78% | 7.10% | -5.887x | 33.5% | 176 | FAIL | -2.753x | 688 | -1.30% | -5.07% |  |
| BTCUSDT | 1h | mode_b|hma30 | Y | Y | — | FAIL | -73.98% | 7.10% | -10.425x | 21.0% | 391 | FAIL | -3.069x | 1522 | -3.26% | -10.32% |  |
| BTCUSDT | 4h | mode_a|(9,16) | Y | Y | — | FAIL | -12.63% | 7.56% | -1.672x | 37.0% | 81 | FAIL | -2.004x | 338 | -0.28% | -2.21% |  |
| BTCUSDT | 4h | mode_a|(10,30) | Y | Y | — | FAIL | -11.67% | 7.56% | -1.545x | 35.1% | 57 | FAIL | -1.348x | 226 | -0.27% | -1.15% |  |
| BTCUSDT | 4h | mode_a|(16,36) | Y | Y | — | FAIL | -5.17% | 7.56% | -0.684x | 39.0% | 41 | FAIL | 0.299x | 162 | -0.06% | 0.44% |  |
| BTCUSDT | 4h | mode_b|hma30 | Y | Y | — | FAIL | -25.15% | 7.56% | -3.329x | 33.0% | 88 | FAIL | -1.800x | 347 | -0.68% | -1.82% |  |
| ETHUSDT | 1h | mode_a|(9,16) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_a|(10,30) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_a|(16,36) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_b|hma30 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|(9,16) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|(10,30) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|(16,36) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_b|hma30 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|(9,16) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|(10,30) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|(16,36) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_b|hma30 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|(9,16) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|(10,30) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|(16,36) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_b|hma30 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|(9,16) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|(10,30) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|(16,36) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_b|hma30 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|(9,16) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|(10,30) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|(16,36) | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_b|hma30 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |

### mcginley-close-slope-cross-v1

| symbol | tf | mode/params | sol_smoke | bnb_smoke | sol_retention | 6m PASS | 6m_ret% | 6m_bh% | ×B&H | 6m_wr% | 6m_n | full PASS | full_×B&H | full_n | ops_6m% | ops_full% | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | mode_a|N14 | Y | Y | — | FAIL | -53.53% | 7.10% | -7.543x | 15.1% | 251 | FAIL | -2.932x | 1005 | -1.84% | -6.74% |  |
| BTCUSDT | 1h | mode_a|N10 | Y | Y | — | FAIL | -59.95% | 7.10% | -8.447x | 15.3% | 294 | FAIL | -3.030x | 1197 | -2.19% | -8.66% |  |
| BTCUSDT | 1h | mode_a|N20 | Y | Y | — | FAIL | -44.37% | 7.10% | -6.252x | 16.4% | 201 | FAIL | -2.777x | 804 | -1.40% | -5.24% |  |
| BTCUSDT | 1h | mode_b|N14 | Y | Y | — | FAIL | -53.53% | 7.10% | -7.543x | 15.1% | 251 | FAIL | -2.932x | 1005 | -1.84% | -6.74% |  |
| BTCUSDT | 4h | mode_a|N14 | Y | Y | — | FAIL | -1.16% | 7.56% | -0.153x | 22.0% | 50 | FAIL | -1.092x | 223 | 0.04% | -0.72% |  |
| BTCUSDT | 4h | mode_a|N10 | Y | Y | — | FAIL | -8.43% | 7.56% | -1.115x | 21.3% | 61 | FAIL | -1.144x | 270 | -0.15% | -0.75% |  |
| BTCUSDT | 4h | mode_a|N20 | Y | Y | — | FAIL | 5.09% | 7.56% | 0.674x | 23.3% | 43 | FAIL | -0.274x | 177 | 0.19% | 0.07% |  |
| BTCUSDT | 4h | mode_b|N14 | Y | Y | — | FAIL | -1.16% | 7.56% | -0.153x | 22.0% | 50 | FAIL | -1.092x | 223 | 0.04% | -0.72% |  |
| ETHUSDT | 1h | mode_a|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_a|N10 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_a|N20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 1h | mode_b|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|N10 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_a|N20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| ETHUSDT | 4h | mode_b|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|N10 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_a|N20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 1h | mode_b|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|N10 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_a|N20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| SOLUSDT | 4h | mode_b|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|N10 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_a|N20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 1h | mode_b|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|N10 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_a|N20 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |
| BNBUSDT | 4h | mode_b|N14 | Y | Y | — | FAIL | — | — | — | — | — | FAIL | — | — | — | — | Pruned by ladder |

## Dual-Survival & Ladder Analysis

1. **Stop-Ladder Attrition:**
   - BTC PASS_6m: 0
   - ETH PASS_6m: 0
   - SOL PASS_6m: 0 (HARD FILTER)
   - BNB PASS_6m: 0 (HARD FILTER)

2. **Smoke & Retention Outcomes:**
   - All cells verified against mandatory sol_smoke and bnb_smoke rules.
   - Dual identical parameter constraint strictly preserved across all symbols.
   - SOL retention diagnostics logged after ETH evaluation.

3. **Path B Pause / Next Actions:**
   - **FULL-LADDER PASS_6m = 0** across all 3 locked strategies.
   - **ACTION:** Cue Path B pause for CoS / Nuno usage.
