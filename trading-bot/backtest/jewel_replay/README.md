# jewel_replay — Path B research harness

Offline CSV replay for **`jewel-strength-hold-v1`**. Separate from the ema-rsi
`backtest/` signal stack; reuses only shared helpers (e.g. `max_drawdown_pct`).

See [`../../strategies/README-jewel-strength-hold-v1.md`](../../strategies/README-jewel-strength-hold-v1.md).

## Dual sizing + windows

| Mode | `buy_qty_pct` | Role |
|------|---------------|------|
| **A (gate)** | 100 | Full equity when in — **MTM/equity** return compared to buy & hold |
| **B (ops)** | 2.5 | Ops sizing column only |

**PASS** iff `Mode-A MTM return ≥ 1.2 × B&H` on the same window.
**WR is informational only** (not a pass/fail leg). WR is closed-trades only; **n/a**
when `n=0` (not 0%). Closed-trade PnL/initial is reported separately from MTM
(open longs include unrealised).

**B&H ≤ 0:** PASS only if Mode-A > 0; Mode-A/B&H ratio shown as **n/a** (the 1.2×
multiple is undefined for non-positive B&H).

Windows: `--window all|6m|both` (default `both` → full + last 6 calendar months
from the last **closed** bar after prep).

Costs: 0.10%/side + 5 bps. Variants: V-zone and V-wide. **No** paper/webhook wiring.

## Sample prep (Claude caveats, on by default)

Before Mode-A rescore / windowing the CLI:

1. Drops the last row (still-open / partial daily bar) for closed-bar fidelity.
2. Cuts sample start to **2017-12-31** (jewel_high warm-up; Slow from 2017-10-24).

Use `--no-prep` only for debugging.

## CLI

```bash
cd trading-bot
source .venv/bin/activate

# Dual Mode A/B + full + 6m tables (real Jewel exports)
python -m backtest.jewel_replay \
  backtest/jewel_replay/data/jewel-btc-daily.csv \
  backtest/jewel_replay/data/jewel-eth-daily.csv \
  --window both

# Fixture / CI
python -m backtest.jewel_replay backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv \
  --window both --waiting-real-csvs

# Legacy single sizing
python -m backtest.jewel_replay fixtures/...csv --buy-qty-pct 2.5 --window all

pytest tests/test_jewel_replay.py -q
```

Symbol is inferred from the filename (`btc` → BTCUSDT, `eth` → ETHUSDT) unless
`--symbol` is set.

## Real CSVs (gitignored under `data/`)

- Box: `trading-bot/backtest/jewel_replay/data/jewel-{btc,eth}-daily.csv`
- CM700 outbox: `C:\temp\GrokBOTandclaudToHATrading\outbox\jewel-*-daily.csv`

Gate results: `results/jewel-pathb-dual-gate.md` (force-add to PR; `*.md` gitignored by default).
