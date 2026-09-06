# fresh-wave-v4 scoreboard

Generated (UTC): 2026-09-06T21:17:42.198756+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes of prior families.**

## Scoring

- **LEAD gate:** 6m Mode-A ≥ **1.2×** B&H → `PASS/FAIL_6m`
- **Also:** full(~2y) Mode-A ≥ **1.2×** B&H → `PASS/FAIL_full` (informational)
- Costs: 0.10%/side fee + 5 bps slip; Mode-A **100%** + Mode-B ops **2.5%** (ops not scored)
- Symbol: BTCUSDT only. Agg: 5m→sub-daily; 1d native; 2d=2×1d. Bar-close; long-only Spot. Single-TF (no HTF filter).
- Params frozen (no spray): Fisher len10 Fish×Trigger prior Fish<0; Coppock ROC14+11/WMA10 (1d/2d only); UTC midnight OR 30m, skip OR>2×ATR14, vol filter OFF, one trade/session.
- Cell scope: Fisher = 16 TF; Coppock = 1d+2d (N/A elsewhere); ORB = one primary `orb-utc` cell from 5m.

## Strategy rules (documented)

1. **ehlers-fisher-v1** — Ehlers Fisher len **10** on HL2. Enter crossover(Fish, Trigger) AND prior Fish < 0; exit crossunder(Fish, Trigger).
2. **coppock-curve-v1** — Coppock = WMA(**10**, ROC(**14**)+ROC(**11**)). Enter trough-turn while <0 OR crossover(0) after ≥10 bars below 0; exit turn-down while >0 OR crossunder(0). **1d/2d only.**
3. **session-orb-v1** — UTC midnight OR first **30m** from **5m** bars. Enter close > OR high after window; exit target 1× OR height, opposite OR edge (stop), or 23:59 UTC flat. Skip if OR height > **2×ATR(14)** on OR close bar. One trade/session. Vol filter OFF.

## Scoreboard LEAD 6m PASS/FAIL_6m (ratio)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ehlers-fisher-v1 | FAIL(-5.26) | FAIL(-5.19) | FAIL(-5.08) | FAIL(-4.34) | FAIL(-2.41) | FAIL(-3.56) | FAIL(-1.45) | FAIL(-0.84) | FAIL(-0.46) | FAIL(-0.52) | FAIL(0.25) | FAIL(-0.32) | FAIL(0.77) | FAIL(0.54) | FAIL(0.45) | FAIL(1.13) |
| coppock-curve-v1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | FAIL(0.50) | FAIL(0.38) |
| session-orb-v1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

_`session-orb-v1` primary cell is `orb-utc` (5m→UTC midnight OR), not a 16-TF spray — see ORB section below._

## Scoreboard full(~2y) PASS/FAIL_full (ratio)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ehlers-fisher-v1 | FAIL(-2.30) | FAIL(-2.31) | FAIL(-2.32) | FAIL(-2.32) | FAIL(-2.05) | FAIL(-2.31) | FAIL(-1.98) | FAIL(-1.49) | FAIL(-0.82) | FAIL(-0.65) | FAIL(-0.64) | FAIL(-0.50) | FAIL(0.01) | FAIL(0.65) | FAIL(1.07) | FAIL(-0.63) |
| coppock-curve-v1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | FAIL(0.61) | FAIL(0.07) |
| session-orb-v1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Combined (6m LEAD | full)

| strategy \ tf | 5m | 10m | 15m | 30m | 90m | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 9h | 12h | 1d | 2d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ehlers-fisher-v1 | F-5.26|F-2.30 | F-5.19|F-2.31 | F-5.08|F-2.32 | F-4.34|F-2.32 | F-2.41|F-2.05 | F-3.56|F-2.31 | F-1.45|F-1.98 | F-0.84|F-1.49 | F-0.46|F-0.82 | F-0.52|F-0.65 | F0.25|F-0.64 | F-0.32|F-0.50 | F0.77|F0.01 | F0.54|F0.65 | F0.45|F1.07 | F1.13|F-0.63 |
| coppock-curve-v1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | F0.50|F0.61 | F0.38|F0.07 |
| session-orb-v1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

_Legend: P=PASS F=FAIL; `P6m|Pfull` compact ratios._

## session-orb-v1 primary cell (BTCUSDT)

- `session-orb-v1` @ `orb-utc`: **6m=FAIL** ret=-7.03% bh=19.02% ratio=-0.369 wr=21.7% n=23 | full=FAIL ratio=-0.680 n=99 | ops_6m=-0.18% ops_full=-0.87%

## PASS_6m cells (LEAD)

_none_

## PASS_full cells (informational; not LEAD)

_none_

## Cell detail (Mode-A gate; both windows)

| strategy | tf | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ret% | full_bh% | full_ratio | full_wr% | full_n | ops_6m% | ops_full% | error |
|----------|----|----|---------|--------|----------|--------|------|------|-----------|----------|------------|----------|--------|---------|-----------|-------|
| ehlers-fisher-v1 | 2d | FAIL | 15.44 | 13.72 | 1.126 | 60.0 | 5 | FAIL | -25.19 | 39.93 | -0.631 | 44.0 | 25 | 0.39 | -0.57 |  |
| ehlers-fisher-v1 | 1d | FAIL | 7.52 | 16.73 | 0.449 | 33.3 | 9 | FAIL | 51.04 | 47.49 | 1.075 | 47.6 | 42 | 0.24 | 1.24 |  |
| ehlers-fisher-v1 | 12h | FAIL | 11.50 | 21.14 | 0.544 | 33.3 | 24 | FAIL | 31.45 | 48.10 | 0.654 | 31.9 | 91 | 0.35 | 0.95 |  |
| ehlers-fisher-v1 | 9h | FAIL | 14.31 | 18.61 | 0.769 | 30.3 | 33 | FAIL | 0.58 | 50.40 | 0.012 | 33.6 | 131 | 0.41 | 0.23 |  |
| ehlers-fisher-v1 | 7h | FAIL | -6.20 | 19.69 | -0.315 | 42.9 | 35 | FAIL | -24.13 | 48.24 | -0.500 | 39.6 | 154 | -0.14 | -0.54 |  |
| ehlers-fisher-v1 | 6h | FAIL | 4.77 | 18.91 | 0.252 | 46.2 | 39 | FAIL | -30.65 | 47.85 | -0.641 | 37.4 | 174 | 0.13 | -0.76 |  |
| ehlers-fisher-v1 | 5h | FAIL | -9.59 | 18.33 | -0.523 | 32.7 | 49 | FAIL | -30.83 | 47.36 | -0.651 | 35.4 | 212 | -0.23 | -0.77 |  |
| ehlers-fisher-v1 | 4h | FAIL | -8.45 | 18.24 | -0.463 | 37.1 | 62 | FAIL | -39.19 | 47.71 | -0.821 | 36.6 | 265 | -0.19 | -1.05 |  |
| ehlers-fisher-v1 | 3h | FAIL | -15.37 | 18.34 | -0.838 | 34.9 | 83 | FAIL | -68.67 | 45.98 | -1.494 | 31.5 | 368 | -0.39 | -2.70 |  |
| ehlers-fisher-v1 | 2h | FAIL | -25.96 | 17.95 | -1.446 | 34.1 | 135 | FAIL | -84.42 | 42.56 | -1.984 | 29.3 | 556 | -0.71 | -4.36 |  |
| ehlers-fisher-v1 | 1h | FAIL | -66.44 | 18.69 | -3.555 | 24.1 | 291 | FAIL | -97.72 | 42.23 | -2.314 | 26.2 | 1163 | -2.65 | -8.84 |  |
| ehlers-fisher-v1 | 90m | FAIL | -44.03 | 18.30 | -2.406 | 26.8 | 183 | FAIL | -87.44 | 42.68 | -2.049 | 28.0 | 751 | -1.41 | -4.90 |  |
| ehlers-fisher-v1 | 30m | FAIL | -82.36 | 18.97 | -4.342 | 20.7 | 590 | FAIL | -99.74 | 42.96 | -2.322 | 22.5 | 2289 | -4.21 | -15.42 |  |
| ehlers-fisher-v1 | 15m | FAIL | -96.78 | 19.04 | -5.083 | 15.9 | 1185 | FAIL | -100.00 | 43.03 | -2.324 | 17.6 | 4604 | -8.20 | -28.74 |  |
| ehlers-fisher-v1 | 10m | FAIL | -99.49 | 19.15 | -5.194 | 14.6 | 1762 | FAIL | -100.00 | 43.30 | -2.310 | 15.2 | 6946 | -12.33 | -40.46 |  |
| ehlers-fisher-v1 | 5m | FAIL | -100.00 | 19.02 | -5.258 | 10.1 | 3548 | FAIL | -100.00 | 43.39 | -2.304 | 10.9 | 13985 | -23.34 | -64.90 |  |
| coppock-curve-v1 | 5m | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 10m | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 15m | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 30m | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 90m | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 1h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 2h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 3h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 4h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 5h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 6h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 7h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 9h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 12h | N/A | — | — | — | — | — | N/A | — | — | — | — | — | — | — | Coppock frozen to 1d/2d only (kick) |
| coppock-curve-v1 | 1d | FAIL | 8.30 | 16.73 | 0.496 | 60.0 | 5 | FAIL | 29.08 | 47.49 | 0.612 | 57.9 | 19 | 0.30 | 0.82 |  |
| coppock-curve-v1 | 2d | FAIL | 5.20 | 13.72 | 0.379 | 50.0 | 2 | FAIL | 2.61 | 39.93 | 0.065 | 50.0 | 8 | 0.15 | 0.15 |  |
| session-orb-v1 | orb-utc | FAIL | -7.03 | 19.02 | -0.369 | 21.7 | 23 | FAIL | -29.51 | 43.39 | -0.680 | 19.2 | 99 | -0.18 | -0.87 |  |

## Caveats

- LEAD = 6m Mode-A only. full(~2y) is reported for context, not paper clearance.
- Mode-B ops 2.5% is parallel / informational only.
- No param spray / SMA200/RSI/BB/ST grafts. Excluded: owned, v1, v2, v3 IDs, Jewel/Hub, Black Skull, research rejects (Stoch, Keltner, MACD-hist div, Inverse Fisher-RSI, HA hybrids, ATR-squeeze).
- No OOS (ETH/SOL/BNB) in this PR — parent runs after BTC PASS_6m.
- Hold prior PRs #15–#21 unmerged; this PR is additive fresh-wave-v4 only.

