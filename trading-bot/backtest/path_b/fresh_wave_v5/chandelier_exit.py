"""chandelier-exit helper — ATR(22)×3 trail (module/tests only; not a primary seat)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import chandelier_exit_long

HELPER_ID = "chandelier-exit"


@dataclass(frozen=True)
class ChandelierParams:
    atr_length: int = 22
    mult: float = 3.0


def compute_long_stops(
    bars: list[Bar],
    params: ChandelierParams | None = None,
) -> list[float | None]:
    """Return long chandelier stop levels aligned to bars (None until warm)."""
    params = params or ChandelierParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    return chandelier_exit_long(
        highs, lows, closes, params.atr_length, params.mult
    )
