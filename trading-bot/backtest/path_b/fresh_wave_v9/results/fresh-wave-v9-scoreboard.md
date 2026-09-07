# fresh-wave-v9 scoreboard

Generated (UTC): 2026-09-07T09:06:39.149083+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring

- **LEAD gate:** 6m Mode-A ≥ **1.2×** B&H → `PASS/FAIL_6m` (≥1 trade). WR informational.
- **Also:** full(~2y) Mode-A ≥ **1.2×** B&H → `PASS/FAIL_full` (informational)
- Costs: 0.10%/side fee + 5 bps slip; Mode-A **100%** + Mode-B ops **2.5%** (ops not scored)
- Symbol: BTCUSDT only (no ETH OOS in this PR). Agg: 5m→sub-daily; 1d native; 2d=2×1d.
- Camarilla UTC: prior UTC day H/L/C; `adj=(H−L)×1.1`; Mode A fade L3 (SL beyond L4); Mode B close>H4. TF 15m–1h. ≠ Session ORB.
- MESA Sine: DominantCycle=**15** Advance=**45**; Sine×LeadSine cross; prefer 1h–4h; full 16 OK. No Fisher/RSI.
- Funding fade: Binance USDT-M fundingRate; Mode A ≤ −0.10%/8h long; Mode B z≤−2 vs ~30d; exit neutral / 2 settlements; Spot 1h–4h. If fetch blocked → ERROR (no invented rates).
- Watchlist (no paper): ema-rsi@9h, schaff@2d. v8 OOS hard-stop 0 survivors. Hold #15–#26 unmerged.

## Strategy rules (documented)

1. **camarilla-utc-v1** — Mode A: fade L3 long, SL=L4, exit mid/H3; Mode B: close>H4, exit <H3 or EOD UTC.
2. **mesa-sine-v1** — crossover(Sine, LeadSine) / crossunder(Sine, LeadSine).
3. **funding-fade-v1** — long-only fade of extreme negative funding; skip short side.

## PASS_6m cells (LEAD)

_none_

## PASS_full cells (informational; not LEAD)

_none_

## Funding ERROR cells

_none_

## LEAD 6m by family (all scored cells)

### camarilla-utc-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 1h|mode_a|fadeL3|adj1.1 | FAIL(-1.18) | -21.65 | 18.30 | -1.183 | 48.4 | 95 | FAIL(-1.25) | -1.246 | 391 | -0.60 | -2.23 |  |
| 1h|mode_b|breakH4|adj1.1 | FAIL(-0.59) | -10.74 | 18.30 | -0.587 | 28.8 | 59 | FAIL(-0.83) | -0.825 | 225 | -0.27 | -1.21 |  |
| 30m|mode_a|fadeL3|adj1.1 | FAIL(-1.13) | -21.65 | 19.24 | -1.125 | 48.5 | 101 | FAIL(-1.41) | -1.405 | 412 | -0.60 | -2.73 |  |
| 30m|mode_b|breakH4|adj1.1 | FAIL(-0.81) | -15.67 | 19.24 | -0.815 | 28.1 | 64 | FAIL(-0.89) | -0.894 | 239 | -0.41 | -1.33 |  |
| 15m|mode_a|fadeL3|adj1.1 | FAIL(-1.12) | -21.23 | 18.96 | -1.120 | 52.5 | 101 | FAIL(-1.44) | -1.440 | 419 | -0.58 | -2.95 |  |
| 15m|mode_b|breakH4|adj1.1 | FAIL(-0.92) | -17.43 | 18.96 | -0.919 | 25.8 | 66 | FAIL(-0.84) | -0.835 | 248 | -0.46 | -1.23 |  |

### mesa-sine-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 4h|dc15|adv45 | FAIL(0.14) | 2.89 | 20.65 | 0.140 | 41.5 | 41 | FAIL(0.23) | 0.228 | 167 | 0.14 | 0.51 |  |
| 3h|dc15|adv45 | FAIL(-0.07) | -1.41 | 20.90 | -0.067 | 36.5 | 52 | FAIL(-0.83) | -0.834 | 221 | 0.04 | -1.01 |  |
| 2h|dc15|adv45 | FAIL(-0.47) | -9.02 | 19.01 | -0.475 | 37.6 | 85 | FAIL(-0.96) | -0.963 | 336 | -0.19 | -1.30 |  |
| 1h|dc15|adv45 | FAIL(-1.10) | -20.05 | 18.30 | -1.096 | 29.1 | 172 | FAIL(-1.74) | -1.737 | 705 | -0.49 | -4.26 |  |
| 90m|dc15|adv45 | FAIL(-0.87) | -16.18 | 18.62 | -0.869 | 30.5 | 118 | FAIL(-1.45) | -1.448 | 469 | -0.38 | -2.66 |  |
| 1d|dc15|adv45 | FAIL(0.35) | 5.65 | 16.27 | 0.347 | 42.9 | 7 | FAIL(0.40) | 0.396 | 28 | 0.17 | 0.69 |  |
| 12h|dc15|adv45 | FAIL(1.10) | 20.50 | 18.56 | 1.105 | 53.3 | 15 | FAIL(0.07) | 0.070 | 64 | 0.54 | 0.31 |  |
| 2d|dc15|adv45 | FAIL(1.16) | 15.45 | 13.36 | 1.156 | 100.0 | 3 | FAIL(0.74) | 0.745 | 15 | 0.37 | 0.90 |  |
| 9h|dc15|adv45 | FAIL(-0.05) | -0.90 | 18.56 | -0.049 | 33.3 | 21 | FAIL(-0.52) | -0.522 | 87 | 0.04 | -0.44 |  |
| 7h|dc15|adv45 | FAIL(-0.56) | -11.52 | 20.74 | -0.555 | 26.9 | 26 | FAIL(-0.46) | -0.455 | 99 | -0.24 | -0.32 |  |
| 6h|dc15|adv45 | FAIL(-0.55) | -9.62 | 17.45 | -0.551 | 32.1 | 28 | FAIL(0.73) | 0.725 | 110 | -0.17 | 1.02 |  |
| 5h|dc15|adv45 | FAIL(-0.23) | -4.72 | 20.35 | -0.232 | 33.3 | 33 | FAIL(0.41) | 0.412 | 128 | -0.05 | 0.73 |  |
| 30m|dc15|adv45 | FAIL(-3.66) | -70.37 | 19.24 | -3.657 | 21.9 | 370 | FAIL(-2.04) | -2.041 | 1418 | -2.95 | -9.43 |  |
| 15m|dc15|adv45 | FAIL(-4.71) | -89.32 | 18.96 | -4.712 | 18.0 | 713 | FAIL(-2.04) | -2.040 | 2839 | -5.39 | -19.05 |  |
| 10m|dc15|adv45 | FAIL(-5.04) | -96.34 | 19.11 | -5.042 | 15.8 | 1077 | FAIL(-2.03) | -2.033 | 4256 | -7.98 | -26.69 |  |
| 5m|dc15|adv45 | FAIL(-5.28) | -99.84 | 18.91 | -5.278 | 12.5 | 2116 | FAIL(-2.02) | -2.022 | 8472 | -14.80 | -47.34 |  |

### funding-fade-v1

| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | full | full_ratio | full_n | ops_6m% | ops_full% | error |
|------|----|---------|--------|----------|--------|------|------|------------|--------|---------|-----------|-------|
| 4h|mode_a|thr-0.10pct|exit2 | FAIL(0.00) | 0.00 | 20.65 | 0.000 | 0.0 | 0 | FAIL(0.00) | 0.000 | 0 | 0.00 | 0.00 |  |
| 4h|mode_b|z2|w90|exit2 | FAIL(-0.23) | -4.74 | 20.65 | -0.230 | 33.3 | 12 | FAIL(-0.25) | -0.247 | 69 | -0.12 | -0.29 |  |
| 3h|mode_a|thr-0.10pct|exit2 | FAIL(0.00) | 0.00 | 20.90 | 0.000 | 0.0 | 0 | FAIL(0.00) | 0.000 | 0 | 0.00 | 0.00 |  |
| 3h|mode_b|z2|w90|exit2 | FAIL(-0.07) | -1.36 | 20.90 | -0.065 | 50.0 | 12 | FAIL(-0.17) | -0.170 | 73 | -0.03 | -0.20 |  |
| 2h|mode_a|thr-0.10pct|exit2 | FAIL(0.00) | 0.00 | 19.01 | 0.000 | 0.0 | 0 | FAIL(0.00) | 0.000 | 0 | 0.00 | 0.00 |  |
| 2h|mode_b|z2|w90|exit2 | FAIL(-0.18) | -3.38 | 19.01 | -0.178 | 41.7 | 12 | FAIL(-0.13) | -0.134 | 69 | -0.08 | -0.14 |  |
| 1h|mode_a|thr-0.10pct|exit2 | FAIL(0.00) | 0.00 | 18.30 | 0.000 | 0.0 | 0 | FAIL(0.00) | 0.000 | 0 | 0.00 | 0.00 |  |
| 1h|mode_b|z2|w90|exit2 | FAIL(-0.29) | -5.27 | 18.30 | -0.288 | 41.7 | 12 | FAIL(-0.31) | -0.310 | 69 | -0.13 | -0.38 |  |

## Caveats

- LEAD = 6m Mode-A sizing only. full(~2y) context only.
- No param retune on 6m after freeze. Scout-wave-3 parked seats.
- Hold prior PRs #15–#26 unmerged; this PR is additive fresh-wave-v9 only.
- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only.
- Watchlist (no paper): ema-rsi@9h, schaff@2d.
- v8 OOS hard-stop 0 survivors — do not revive without Strategy OK.
- Funding rates never invented; blocked fetch → ERROR cell.

## IDs frozen: camarilla-utc-v1, mesa-sine-v1, funding-fade-v1

