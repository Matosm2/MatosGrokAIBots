# jewel_replay — Path B research harness

Offline CSV replay for **`jewel-strength-hold-v1`**. Separate from the ema-rsi
`backtest/` signal stack; reuses only shared helpers (e.g. `max_drawdown_pct`).

See [`../../strategies/README-jewel-strength-hold-v1.md`](../../strategies/README-jewel-strength-hold-v1.md).

## Dual sizing + windows

| Mode | `buy_qty_pct` | Role |
|------|---------------|------|
| **A (gate)** | 100 | Full equity when in — return compared to buy & hold |
| **B (ops)** | 2.5 | Ops sizing column only |

**PASS** iff `n>0` AND `WR ≥ 60%` AND `Mode-A return > B&H` on the same window.

Windows: `--window all|6m|both` (default `both` → full + last 6 calendar months
from the last bar).

Costs: 0.10%/side + 5 bps. Variants: V-zone and V-wide. **No** paper/webhook wiring.

## CLI

```bash
cd trading-bot
source .venv/bin/activate

# Dual Mode A/B + full + 6m tables (one or more CSVs)
python -m backtest.jewel_replay path/to/jewel-btc-daily.csv path/to/jewel-eth-daily.csv \
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

## Expected real CSVs (not in git)

- CM700: `C:\temp\GrokBOTandclaudToHATrading\outbox\jewel-btc-daily.csv`
- CM700: `C:\temp\GrokBOTandclaudToHATrading\outbox\jewel-eth-daily.csv`
- Or box: `/workspace/uploads/jewel*.csv`

Until those exist, run the synthetic fixture and keep `--waiting-real-csvs`.
