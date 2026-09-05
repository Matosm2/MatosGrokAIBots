"""TV-free offline research sketches (not paper/live)."""

__all__ = ["STRATEGY_IDS", "NEW_STRATEGY_IDS"]

STRATEGY_IDS = (
    "daily-adx-trend-hold-v1",
    "macd-hist-regime-v1",
    "htf-ema-pullback-wide-v1",
    "close-above-ema20-hold-v1",
    "donchian-20-10-spot-v1",
)

# Default CLI target for this PR (ema20 + donchian dual-sizing runs).
NEW_STRATEGY_IDS = (
    "close-above-ema20-hold-v1",
    "donchian-20-10-spot-v1",
)
