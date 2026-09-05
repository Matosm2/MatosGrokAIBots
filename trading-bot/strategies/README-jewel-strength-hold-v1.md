# Jewel Strength Hold v1 (RESEARCH)

**strategy_id:** `jewel-strength-hold-v1`  
**Script:** [`jewel-strength-hold-v1.pine`](./jewel-strength-hold-v1.pine)  
**Status:** Paper-research harness only — **do not** enable paper/live webhook wiring.

Inverts the failed Fast×Slow OS/OB reading of The Jewel. Uses **Jewel Slow + High
plots only** (no RSI/Stoch proxy, not bolted onto ema-rsi). See
`knowledge/claude-trading/claude__jewel-patterns.md` for the momentum table that
motivated this brief; **this README + Pine rules win** if they disagree.

## Universe

| Role | Symbol / TF |
|------|-------------|
| Primary | BTCUSDT **Daily** |
| OOS | ETHUSDT **Daily**, **unchanged** thresholds |

Spot **long-only**, `process_orders_on_close=true`, pyramiding **0**.

## Rules

| Signal | Logic |
|--------|--------|
| **Entry A** | `crossover(Slow, 70)` |
| **Entry B** | `crossover(High, 80)` AND `Slow >= 70` |
| **Exit** | `Slow < 70` AND `High <= 80` |

### Variants (Pine input **Exit variant**)

| Mode | Exit |
|------|------|
| **V-zone** | Zone exit only (no hard stop) |
| **V-wide** | Zone exit **OR** `close < entry − 3 × ATR(14)` (ATR frozen at entry) |

## Costs (offline + Strategy Tester)

- Commission: **0.10% per side**
- Slippage: **≥ 5 bps** adverse vs close
- Size: **Mode A 100%** (gate vs B&H) / **Mode B 2.5%** (ops); full close on exit

## Wire Jewel Slow / High on the chart

1. Open BINANCE:BTCUSDT (or ETHUSDT) on **1D**.
2. Add **The Jewel** (invite-only) so its plots are on the chart.
3. Add `jewel-strength-hold-v1.pine`.
4. In strategy inputs, set:
   - **Jewel Slow (external plot)** → The Jewel’s **Slow** plot
   - **Jewel High (external plot)** → The Jewel’s **High** plot  
   (Defaults are `close` placeholders — must be rewired or results are meaningless.)
5. Choose **V-zone** or **V-wide**. Set TV slippage ≥ 5 bps.
6. Run Strategy Tester. **Do not** create bot webhooks / `alert()` for this script.

Exposed Jewel plots (for reference):  
`GodModeAlert, DI-, DI+, ADX, Fast, Slow, High, Fib, …` — this harness uses **Slow** and **High** only.

## Path B CSV replay (offline)

Module: `trading-bot/backtest/jewel_replay/`

Export or build a CSV with columns:

```text
time,open,high,low,close,volume,Slow,jewel_high
```

- `time`: ISO-8601 or epoch ms (UTC)
- `Slow` / `jewel_high`: Jewel plot values aligned to each daily bar (no lookahead)
- Prefer `jewel_high` (not `High`) so Jewel High does not collide with OHLC `high`

```bash
cd trading-bot
source .venv/bin/activate
# Dual sizing (Mode A 100% gate / Mode B 2.5% ops) + full + last-6m tables
python -m backtest.jewel_replay path/to/jewel-btc-daily.csv path/to/jewel-eth-daily.csv --window both
python -m backtest.jewel_replay backtest/jewel_replay/fixtures/synthetic_jewel_btc_daily.csv --window both
```

Reports per symbol/variant/window:
**n | WR | Mode-A | Mode-B (ops) | B&H | Mode-A/B&H | PASS/FAIL**
for **both** V-zone and V-wide. Synthetic fixture keeps CI free of real Jewel data.

## Gate before any paper consideration

Promote toward paper **only if**, on the agreed window (Mode A = 100% equity):

1. **Mode-A** MTM/equity return **≥ 1.2 × buy & hold** on the same sample,

for the primary (BTC Daily) run — then re-check ETH Daily OOS with **unchanged**
thresholds. **Win rate is informational only** (not a pass/fail leg).

**B&H ≤ 0:** PASS only if Mode-A > 0; Mode-A/B&H ratio = n/a.

Mode B (2.5%) is the ops sizing column only. Until then: research only.

## What this is not

- Not ema-rsi-trend / Fast×Slow OS/OB reuse
- Not a live bot strategy_id for webhooks
- Not a claim that The Jewel’s discretionary method is validated — mechanical Slow/High
  strength hold only
