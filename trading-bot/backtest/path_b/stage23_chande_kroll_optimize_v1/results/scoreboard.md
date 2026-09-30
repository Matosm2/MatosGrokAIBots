# Scoreboard: stage23-chande-kroll-optimize-v1

_Generated: 2026-09-21 21:59:09 UTC_

## Summary
- **Strategy ID:** `chande-kroll-stop-flip`
- **Total Configurations Tested:** 160
- **Banked Baseline Evaluated:** (p=10, x=1.0, q=9) across 1H and 4H
- **BTC PASS_6m Count (>=1.20x B&H, n > 5):** 0
- **Full Ladder PASS_6m Count (BTC->ETH->SOL->BNB):** 0

## Baseline vs Banked Near-Miss (~1.194x)
| TF | Params (p,x,q) | BTC n | BTC Ret% | BTC B&H% | x B&H | BTC Smoke | PASS 6m | Notes |
|---|---|---|---|---|---|---|---|---|
| 4h | (10, 1.0, 9) | 26 | +8.17% | +23.52% | 0.348x | FAIL: lag B&H (0.348x) | NO | BANKED_BASELINE_(10,1.0,9); denser_n(26>>9) |
| 1h | (10, 1.0, 9) | 104 | -7.58% | +26.77% | -0.283x | KILL: negative ret | NO | BANKED_BASELINE_(10,1.0,9); denser_n(104>>9) |

## Top 20 Configurations by BTC Performance
| Rank | TF | Params (p,x,q) | BTC n | BTC Ret% | BTC B&H% | x B&H | ETH xB&H | SOL xB&H | BNB xB&H | Full Ladder | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1h | (14, 1.0, 9) | 72 | +24.09% | +26.77% | 0.900x | 0.556x | 0.446x | 0.125x | FAIL | denser_n(72>>9) |
| 2 | 1h | (8, 1.0, 14) | 75 | +23.90% | +26.77% | 0.893x | 0.185x | 0.159x | 0.152x | FAIL | denser_n(75>>9) |
| 3 | 1h | (14, 1.0, 11) | 67 | +21.93% | +26.77% | 0.819x | 0.654x | 0.513x | 0.148x | FAIL | denser_n(67>>9) |
| 4 | 1h | (8, 0.8, 14) | 69 | +21.71% | +26.77% | 0.811x | 0.437x | 0.177x | 0.212x | FAIL | denser_n(69>>9) |
| 5 | 4h | (10, 1.2, 14) | 20 | +18.80% | +23.52% | 0.799x | 0.368x | 0.490x | 0.244x | FAIL | denser_n(20>>9) |
| 6 | 4h | (8, 1.2, 14) | 23 | +17.92% | +23.52% | 0.762x | 0.736x | 0.674x | 0.321x | FAIL | denser_n(23>>9) |
| 7 | 4h | (12, 1.0, 11) | 20 | +17.43% | +23.52% | 0.741x | 0.410x | 0.461x | 0.428x | FAIL | denser_n(20>>9) |
| 8 | 4h | (12, 1.2, 5) | 33 | +17.29% | +23.52% | 0.735x | 0.273x | 0.789x | 0.280x | FAIL | denser_n(33>>9) |
| 9 | 4h | (8, 1.5, 9) | 40 | +17.17% | +23.52% | 0.730x | -0.014x | 0.376x | 0.243x | FAIL | denser_n(40>>9) |
| 10 | 4h | (14, 1.2, 9) | 22 | +16.79% | +23.52% | 0.714x | 0.624x | 0.550x | 0.201x | FAIL | denser_n(22>>9) |
| 11 | 1h | (14, 0.8, 9) | 68 | +18.78% | +26.77% | 0.702x | 0.560x | 0.182x | 0.315x | FAIL | denser_n(68>>9) |
| 12 | 4h | (12, 1.2, 14) | 18 | +16.32% | +23.52% | 0.694x | 0.423x | 0.557x | 0.164x | FAIL | denser_n(18>>9) |
| 13 | 4h | (14, 1.2, 14) | 16 | +16.31% | +23.52% | 0.694x | 0.319x | 0.431x | 0.115x | FAIL | denser_n(16>>9) |
| 14 | 4h | (14, 1.2, 11) | 19 | +16.06% | +23.52% | 0.683x | 0.430x | 0.833x | 0.296x | FAIL | denser_n(19>>9) |
| 15 | 4h | (14, 1.0, 14) | 15 | +16.04% | +23.52% | 0.682x | 0.518x | 0.708x | 0.032x | FAIL | denser_n(15>>9) |
| 16 | 1h | (10, 1.0, 14) | 71 | +18.14% | +26.77% | 0.678x | 0.667x | 0.185x | 0.266x | FAIL | denser_n(71>>9) |
| 17 | 4h | (14, 0.8, 7) | 20 | +15.70% | +23.52% | 0.667x | 0.396x | 0.560x | 0.294x | FAIL | denser_n(20>>9) |
| 18 | 4h | (12, 1.2, 11) | 22 | +15.63% | +23.52% | 0.665x | 0.673x | 0.570x | 0.093x | FAIL | denser_n(22>>9) |
| 19 | 1h | (12, 1.0, 11) | 74 | +17.63% | +26.77% | 0.659x | 0.569x | 0.182x | 0.053x | FAIL | denser_n(74>>9) |
| 20 | 1h | (12, 0.8, 11) | 68 | +17.55% | +26.77% | 0.656x | 0.568x | 0.141x | 0.305x | FAIL | denser_n(68>>9) |

## Full Ladder PASS_6m Candidates
Total configurations passing all 4 coins: **0**

None of the swept configurations achieved Mode-A >= 1.20x B&H simultaneously across all four coins (BTC, ETH, SOL, BNB) with n > 5.

## Complete Sweep Results (All 80 Parameter Sets x 2 Timeframes)
See `scoreboard.csv` for the full dataset.
