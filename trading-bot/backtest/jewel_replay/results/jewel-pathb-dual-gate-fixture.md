# Path B dual-sizing gate: jewel-strength-hold-v1

_Generated: 2026-09-05 22:20 UTC_

## Framing

- **strategy_id:** `jewel-strength-hold-v1`
- Path B CSV replay — **not** paper/live webhook-enabled
- **Mode A (gate):** `buy_qty_pct=100` — 100% equity when in; compared to buy & hold
- **Mode B (ops):** `buy_qty_pct=2.5` — ops column only
- Costs: 0.10%/side + 5 bps slip; V-zone and V-wide
- **PASS** iff `Mode-A MTM/equity ≥ 1.2 × B&H` (same window). **WR is informational only** (not a pass/fail leg).
- **B&H ≤ 0:** PASS only if Mode-A > 0; Mode-A/B&H ratio shown as **n/a** (multiple undefined for non-positive B&H).
- **Return basis:** Mode-A/B columns are **MTM/equity** (include unrealised open long). Closed-trade PnL/initial is in Detail. WR is closed-trades only; **n/a** when n=0 (not 0%).

## Data

- `backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv`

### Sample prep (Claude caveats)

- synthetic_jewel_btc_daily.csv: Dropped last open/partial bar 2023-12-23 UTC (closed-bar fidelity).
- synthetic_jewel_btc_daily.csv: Sample start cut to 2017-12-31 UTC (jewel_high warm-up; removed 0 early bars).

> **Waiting for real CSVs:** Expected on CM700 at `C:\temp\GrokBOTandclaudToHATrading\outbox\jewel-btc-daily.csv` and `jewel-eth-daily.csv` (also check `/workspace/uploads/jewel*.csv`). This report may be fixture-only scaffolding until those land.

## Gate table — Full window (`full`)

| Symbol | Variant | n | WR | Mode-A MTM | Mode-B (ops) MTM | B&H | Mode-A/B&H | Closed-A / init | Open long | PASS/FAIL |
|--------|---------|---|----|------------|------------------|-----|-----------|----------------|-----------|-----------|
| BTCUSDT | V-zone | 2 | 50.0% | -10.19% | -0.25% | -8.60% | n/a | -10.19% | no | **FAIL** |
| BTCUSDT | V-wide | 2 | 50.0% | -9.20% | -0.23% | -8.60% | n/a | -9.20% | no | **FAIL** |

## Gate table — Last 6 months (`last_6m`)

| Symbol | Variant | n | WR | Mode-A MTM | Mode-B (ops) MTM | B&H | Mode-A/B&H | Closed-A / init | Open long | PASS/FAIL |
|--------|---------|---|----|------------|------------------|-----|-----------|----------------|-----------|-----------|
| BTCUSDT | V-zone | 2 | 50.0% | -10.19% | -0.25% | -8.60% | n/a | -10.19% | no | **FAIL** |
| BTCUSDT | V-wide | 2 | 50.0% | -9.20% | -0.23% | -8.60% | n/a | -9.20% | no | **FAIL** |

## Detail

### BTCUSDT — V-zone — full

- Bars: 39 (2023-11-14 → 2023-12-22 UTC)
- Source: `backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv`
- Gate: **FAIL** (n=2, WR=50.0% info, Mode-A MTM -10.19% / B&H -8.60% = ratio n/a; need ≥1.2× when B&H>0; closed-A/init -10.19%)
- Open long at window end (Mode A): no
- Mode-A max DD 15.87%; Mode-B max DD 0.42%
- Wins/Losses (closed, Mode A): 1 / 1

### BTCUSDT — V-wide — full

- Bars: 39 (2023-11-14 → 2023-12-22 UTC)
- Source: `backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv`
- Gate: **FAIL** (n=2, WR=50.0% info, Mode-A MTM -9.20% / B&H -8.60% = ratio n/a; need ≥1.2× when B&H>0; closed-A/init -9.20%)
- Open long at window end (Mode A): no
- Mode-A max DD 14.94%; Mode-B max DD 0.39%
- Wins/Losses (closed, Mode A): 1 / 1

### BTCUSDT — V-zone — last_6m

- Bars: 39 (2023-11-14 → 2023-12-22 UTC)
- Source: `backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv`
- Gate: **FAIL** (n=2, WR=50.0% info, Mode-A MTM -10.19% / B&H -8.60% = ratio n/a; need ≥1.2× when B&H>0; closed-A/init -10.19%)
- Open long at window end (Mode A): no
- Mode-A max DD 15.87%; Mode-B max DD 0.42%
- Wins/Losses (closed, Mode A): 1 / 1

### BTCUSDT — V-wide — last_6m

- Bars: 39 (2023-11-14 → 2023-12-22 UTC)
- Source: `backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv`
- Gate: **FAIL** (n=2, WR=50.0% info, Mode-A MTM -9.20% / B&H -8.60% = ratio n/a; need ≥1.2× when B&H>0; closed-A/init -9.20%)
- Open long at window end (Mode A): no
- Mode-A max DD 14.94%; Mode-B max DD 0.39%
- Wins/Losses (closed, Mode A): 1 / 1

## Caveats

- strategy_id jewel-strength-hold-v1 — RESEARCH Path B replay.
- Bar-close fills; Jewel Slow/High from CSV (no RSI/Stoch proxy).
- Mode A = 100% equity (gate: MTM ≥ 1.2× B&H); Mode B = 2.5% equity (ops).
- Closed-trade WR uses completed exits only (informational); WR=n/a when n=0.
- If B&H≤0: PASS only if Mode-A>0; Mode-A/B&H ratio = n/a.
- Dropped last open/partial daily bar; full sample starts 2017-12-31 (jewel_high warm-up).
- V-wide ATR stop uses ATR frozen at entry; threshold vs entry bar close.
- Not wired to paper/live webhooks.
- **Repaint / non-realtime risk:** Path B assumes bar-close Slow/High as exported.
- **Invite-only Jewel:** Slow/High from invite-only indicator; harness cannot reconstruct without exported series.

