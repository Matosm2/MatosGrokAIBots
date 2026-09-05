# jewel_mtf_hub — multi-TF OHLCV join (scaffold)

**research_id:** `jewel-mtf-hub-regime-v1`  
**Status:** join utility only — **signal scoring parked**

Maps higher-timeframe (HTF) series onto lower-timeframe (LTF) bars with
**no lookahead**: an HTF value is available only after that HTF bar closes
(`htf_close <= ltf_close`).

This is **not** a Jewel/Hub replay and does **not** implement M1–M4 scoring,
Hub columns, or Slow×70 rules under the Jewel name. Invite-only Jewel plots
have no open formula here; do not invent proxies or thresholds. Existing
`jewel_replay/data/*.csv` exports are **archival only** — not this research path.

## Rule

```text
for each LTF bar i:
  decision_time = LTF open_time + LTF duration
  use latest HTF bar j where (HTF open_time + HTF duration) <= decision_time
  else None
```

Supported TFs: **4H**, **1D**, **2D** (UTC continuous crypto sessions).

## Usage

```bash
cd trading-bot
source .venv/bin/activate
pytest tests/test_jewel_mtf_hub_join.py -q
python -m backtest.jewel_mtf_hub   # synthetic join smoke print
```

```python
from backtest.jewel_mtf_hub import map_htf_onto_ltf, join_htf_ohlcv_onto_ltf
from backtest.jewel_mtf_hub.ohlcv import OhlcvBar

# Map any HTF series (e.g. close) onto LTF timestamps:
mapped = map_htf_onto_ltf(
    ltf_open_ms=[...],
    ltf_tf="4H",
    htf_open_ms=[...],
    htf_values=[...],  # same length as htf_open_ms
    htf_tf="1D",
)

# Or join full OHLCV snapshots:
joined = join_htf_ohlcv_onto_ltf(
    ltf_bars=[OhlcvBar(...)],
    ltf_tf="4H",
    htf_bars=[OhlcvBar(...)],
    htf_tf="1D",
)
```

OHLCV for live research should come from public Binance klines
(`backtest.data.fetch_klines` / cache) — not from archival Jewel CSVs.

## Parked: future signal matrix (M1–M4)

Documented for when an **open proxy map** exists. **Not implemented** in this PR.

| ID | Intent (parked) |
|----|-----------------|
| M1 | 2D Hub green filter + Hub/ribbon long; exit leaves green / stress |
| M2 | 1D Hub green + 4H Hub flip; exit 1D leaves green |
| M3 | 2D Slow≥70 + Slow cross 70; exit Slow\<70 AND High≤80 |
| M4 | 1D Slow≥70 + 4H Slow cross while 1D≥70; exit 1D Slow\<70 |

## Future CSV schema (when formulas/proxies exist)

Per TF file (`…-4h.csv`, `…-1d.csv`, `…-2d.csv`), columns TBD by proxy map:

```text
time,open,high,low,close,volume
# plus only columns backed by an open formula or owned indicator —
# do not invent jewel_slow / hub_* placeholders labeled as real Jewel/Hub
```

## What this is not

- Not paper/webhook wiring
- Not a retune of `jewel-strength-hold-v1` / Path B `jewel_replay`
- Not fake Hub or Jewel Slow/High under those names
