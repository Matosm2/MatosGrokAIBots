# jewel-mtf-hub-regime-v1 — open-proxy edition (RESEARCH)

**research_id:** `jewel-mtf-hub-regime-v1`  
**Edition:** open-proxy  
**Module:** [`../backtest/jewel_mtf_hub/`](../backtest/jewel_mtf_hub/)

Multi-timeframe join + **M1–M4** matrix using public indicators only
(ADX/DI regime, RSI strength, EMA21/55 ribbon).

| Item | Status |
|------|--------|
| No-lookahead HTF join (4H / 1D / 2D) | **Implemented** (PR #12) |
| 2D aggregation from 1D pairs | **Implemented** |
| M1–M4 open-proxy signals + dual-size backtest | **Implemented** |
| Series named Jewel / Hub | **Not used** (honest ADX/RSI/EMA names) |
| Paper / webhook | **No** (gate hard-stop on FAIL) |

See [`../backtest/jewel_mtf_hub/README.md`](../backtest/jewel_mtf_hub/README.md).
