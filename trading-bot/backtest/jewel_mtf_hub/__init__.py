"""Multi-TF OHLCV join utilities for research_id jewel-mtf-hub-regime-v1.

Scaffold only: map higher-timeframe (HTF) series onto lower-timeframe (LTF) bars
with **no lookahead** (HTF values available only after HTF bar close).

Signal scoring (M1–M4 / Hub / Jewel Slow×70) is **parked** — awaiting an open
proxy map. This package does not invent Jewel/Hub values or thresholds.
"""

from backtest.jewel_mtf_hub.join import (
    TF_MS,
    assert_no_lookahead_sample,
    bar_close_ms,
    map_htf_indices_onto_ltf,
    map_htf_onto_ltf,
    normalize_tf,
)
from backtest.jewel_mtf_hub.ohlcv import JoinedBar, join_htf_ohlcv_onto_ltf

__all__ = [
    "TF_MS",
    "JoinedBar",
    "assert_no_lookahead_sample",
    "bar_close_ms",
    "join_htf_ohlcv_onto_ltf",
    "map_htf_indices_onto_ltf",
    "map_htf_onto_ltf",
    "normalize_tf",
]

RESEARCH_ID = "jewel-mtf-hub-regime-v1"
