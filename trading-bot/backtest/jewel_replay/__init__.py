"""Path B offline replay for strategy_id jewel-strength-hold-v1 (research).

Loads CSV with OHLCV + Jewel Slow/High columns. Does not proxy Jewel with RSI/Stoch
and does not reuse ema-rsi Fast×Slow OS/OB logic.

Dual sizing: Mode A (100% equity) for gate vs buy&hold; Mode B (2.5%) ops column.
"""

from backtest.jewel_replay.engine import ReplayResult, Trade, run_replay
from backtest.jewel_replay.report import MODE_A_PCT, MODE_B_PCT, DualModeRow
from backtest.jewel_replay.signals import JewelParams, Variant, compute_signals
from backtest.jewel_replay.window import WindowMode, apply_window, filter_bars_last_months

__all__ = [
    "DualModeRow",
    "JewelParams",
    "MODE_A_PCT",
    "MODE_B_PCT",
    "ReplayResult",
    "Trade",
    "Variant",
    "WindowMode",
    "apply_window",
    "compute_signals",
    "filter_bars_last_months",
    "run_replay",
]
