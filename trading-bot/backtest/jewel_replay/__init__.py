"""Path B offline replay for strategy_id jewel-strength-hold-v1 (research).

Loads CSV with OHLCV + Jewel Slow/High columns. Does not proxy Jewel with RSI/Stoch
and does not reuse ema-rsi Fast×Slow OS/OB logic.
"""

from backtest.jewel_replay.engine import ReplayResult, Trade, run_replay
from backtest.jewel_replay.signals import JewelParams, Variant, compute_signals

__all__ = [
    "JewelParams",
    "ReplayResult",
    "Trade",
    "Variant",
    "compute_signals",
    "run_replay",
]
