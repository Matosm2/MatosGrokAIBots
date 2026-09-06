"""Aggregate 1D OHLCV into deterministic 2D bars.

Rule (unit-tested, frozen for this research_id):
- Input: sorted ascending daily bars (UTC open at 00:00).
- Pair consecutive days as (bars[0], bars[1]), (bars[2], bars[3]), …
- If the series length is odd, drop the final unpaired daily bar.
- For each pair (d0, d1):
  - open_time_ms = d0.open_time_ms
  - open = d0.open
  - high = max(d0.high, d1.high)
  - low = min(d0.low, d1.low)
  - close = d1.close
  - volume = d0.volume + d1.volume
  - close_time_ms = d1.close_time_ms
- Duration matches TF_MS['2D'] = 2 calendar days from open_time_ms.

No calendar alignment to even/odd Unix days — pairing is index-based from the
start of the provided series so results are reproducible given the same fetch
window.
"""

from __future__ import annotations

from backtest.data import Bar
from backtest.jewel_mtf_hub.join import TF_MS
from backtest.jewel_mtf_hub.ohlcv import OhlcvBar


def aggregate_1d_to_2d(daily: list[Bar]) -> list[Bar]:
    """Pair consecutive daily bars into 2D OHLCV (see module docstring)."""
    out: list[Bar] = []
    n = len(daily) - (len(daily) % 2)
    for i in range(0, n, 2):
        d0, d1 = daily[i], daily[i + 1]
        out.append(
            Bar(
                open_time_ms=d0.open_time_ms,
                open=d0.open,
                high=max(d0.high, d1.high),
                low=min(d0.low, d1.low),
                close=d1.close,
                volume=d0.volume + d1.volume,
                close_time_ms=d1.close_time_ms,
            )
        )
    return out


def bars_to_ohlcv(bars: list[Bar]) -> list[OhlcvBar]:
    """Convert backtest.data.Bar → OhlcvBar for join helpers."""
    return [
        OhlcvBar(
            open_time_ms=b.open_time_ms,
            open=b.open,
            high=b.high,
            low=b.low,
            close=b.close,
            volume=b.volume,
        )
        for b in bars
    ]


def assert_2d_duration(bars_2d: list[Bar]) -> None:
    """Sanity: each 2D open→nominal close spans TF_MS['2D']."""
    dur = TF_MS["2D"]
    for b in bars_2d:
        # Binance close_time_ms = last ms of bar → span +1 == duration
        if b.close_time_ms - b.open_time_ms + 1 != dur:
            raise AssertionError(
                f"2D bar open={b.open_time_ms} close_time={b.close_time_ms} "
                f"span != {dur}ms"
            )
