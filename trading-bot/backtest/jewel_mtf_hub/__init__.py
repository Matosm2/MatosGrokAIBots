"""jewel-mtf-hub-regime-v1 — open-proxy edition.

Multi-TF OHLCV join (no lookahead) + M1–M4 matrix using public indicators
(ADX/DI regime, RSI strength, EMA ribbon). Not Jewel. Not Hub.
"""

from backtest.jewel_mtf_hub.aggregate import aggregate_1d_to_2d
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
    "aggregate_1d_to_2d",
    "assert_no_lookahead_sample",
    "bar_close_ms",
    "join_htf_ohlcv_onto_ltf",
    "map_htf_indices_onto_ltf",
    "map_htf_onto_ltf",
    "normalize_tf",
]

RESEARCH_ID = "jewel-mtf-hub-regime-v1"
EDITION = "open-proxy"
