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

- `backtest/jewel_replay/data/jewel-btc-daily.csv`
- `backtest/jewel_replay/data/jewel-eth-daily.csv`

### Sample prep (Claude caveats)

- jewel-btc-daily.csv: Dropped last open/partial bar 2026-09-05 UTC (closed-bar fidelity).
- jewel-btc-daily.csv: Sample start cut to 2017-12-31 UTC (jewel_high warm-up; removed 136 early bars).
- jewel-eth-daily.csv: Dropped last open/partial bar 2026-09-05 UTC (closed-bar fidelity).
- jewel-eth-daily.csv: Sample start cut to 2017-12-31 UTC (jewel_high warm-up; removed 136 early bars).

## Gate table — Full window (`full`)

| Symbol | Variant | n | WR | Mode-A MTM | Mode-B (ops) MTM | B&H | Mode-A/B&H | Closed-A / init | Open long | PASS/FAIL |
|--------|---------|---|----|------------|------------------|-----|-----------|----------------|-----------|-----------|
| BTCUSDT | V-zone | 29 | 55.2% | +541.18% | +5.89% | +480.77% | 1.126 | +537.01% | yes | **FAIL** |
| BTCUSDT | V-wide | 29 | 55.2% | +541.18% | +5.89% | +480.77% | 1.126 | +537.01% | yes | **FAIL** |
| ETHUSDT | V-zone | 28 | 57.1% | +515.42% | +6.01% | +234.59% | 2.197 | +522.98% | yes | **PASS** |
| ETHUSDT | V-wide | 28 | 57.1% | +515.42% | +6.01% | +234.59% | 2.197 | +522.98% | yes | **PASS** |

## Gate table — Last 6 months (`last_6m`)

| Symbol | Variant | n | WR | Mode-A MTM | Mode-B (ops) MTM | B&H | Mode-A/B&H | Closed-A / init | Open long | PASS/FAIL |
|--------|---------|---|----|------------|------------------|-----|-----------|----------------|-----------|-----------|
| BTCUSDT | V-zone | 2 | 0.0% | -0.67% | -0.02% | +9.62% | -0.069 | -1.31% | yes | **FAIL** |
| BTCUSDT | V-wide | 2 | 0.0% | -0.67% | -0.02% | +9.62% | -0.069 | -1.31% | yes | **FAIL** |
| ETHUSDT | V-zone | 0 | n/a | -1.21% | -0.03% | +15.45% | -0.079 | +0.00% | yes | **FAIL** |
| ETHUSDT | V-wide | 0 | n/a | -1.21% | -0.03% | +15.45% | -0.079 | +0.00% | yes | **FAIL** |

## Detail

### BTCUSDT — V-zone — full

- Bars: 3170 (2017-12-31 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-btc-daily.csv`
- Gate: **FAIL** (n=29, WR=55.2% info, Mode-A MTM +541.18% / B&H +480.77% = ratio 1.126; need ≥1.2× when B&H>0; closed-A/init +537.01%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 42.25%; Mode-B max DD 1.76%
- Wins/Losses (closed, Mode A): 16 / 13

### BTCUSDT — V-wide — full

- Bars: 3170 (2017-12-31 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-btc-daily.csv`
- Gate: **FAIL** (n=29, WR=55.2% info, Mode-A MTM +541.18% / B&H +480.77% = ratio 1.126; need ≥1.2× when B&H>0; closed-A/init +537.01%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 42.25%; Mode-B max DD 1.76%
- Wins/Losses (closed, Mode A): 16 / 13

### BTCUSDT — V-zone — last_6m

- Bars: 185 (2026-03-04 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-btc-daily.csv`
- Gate: **FAIL** (n=2, WR=0.0% info, Mode-A MTM -0.67% / B&H +9.62% = ratio -0.069; need ≥1.2× when B&H>0; closed-A/init -1.31%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 7.25%; Mode-B max DD 0.19%
- Wins/Losses (closed, Mode A): 0 / 2

### BTCUSDT — V-wide — last_6m

- Bars: 185 (2026-03-04 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-btc-daily.csv`
- Gate: **FAIL** (n=2, WR=0.0% info, Mode-A MTM -0.67% / B&H +9.62% = ratio -0.069; need ≥1.2× when B&H>0; closed-A/init -1.31%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 7.25%; Mode-B max DD 0.19%
- Wins/Losses (closed, Mode A): 0 / 2

### ETHUSDT — V-zone — full

- Bars: 3170 (2017-12-31 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-eth-daily.csv`
- Gate: **PASS** (n=28, WR=57.1% info, Mode-A MTM +515.42% / B&H +234.59% = ratio 2.197; need ≥1.2× when B&H>0; closed-A/init +522.98%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 43.19%; Mode-B max DD 1.68%
- Wins/Losses (closed, Mode A): 16 / 12

### ETHUSDT — V-wide — full

- Bars: 3170 (2017-12-31 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-eth-daily.csv`
- Gate: **PASS** (n=28, WR=57.1% info, Mode-A MTM +515.42% / B&H +234.59% = ratio 2.197; need ≥1.2× when B&H>0; closed-A/init +522.98%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 43.19%; Mode-B max DD 1.68%
- Wins/Losses (closed, Mode A): 16 / 12

### ETHUSDT — V-zone — last_6m

- Bars: 185 (2026-03-04 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-eth-daily.csv`
- Gate: **FAIL** (n=0, WR=n/a info, Mode-A MTM -1.21% / B&H +15.45% = ratio -0.079; need ≥1.2× when B&H>0; closed-A/init +0.00%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 4.74%; Mode-B max DD 0.12%
- Wins/Losses (closed, Mode A): 0 / 0

### ETHUSDT — V-wide — last_6m

- Bars: 185 (2026-03-04 → 2026-09-04 UTC)
- Source: `backtest/jewel_replay/data/jewel-eth-daily.csv`
- Gate: **FAIL** (n=0, WR=n/a info, Mode-A MTM -1.21% / B&H +15.45% = ratio -0.079; need ≥1.2× when B&H>0; closed-A/init +0.00%)
- Open long at window end (Mode A): yes — MTM includes unrealised
- Mode-A max DD 4.74%; Mode-B max DD 0.12%
- Wins/Losses (closed, Mode A): 0 / 0

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

