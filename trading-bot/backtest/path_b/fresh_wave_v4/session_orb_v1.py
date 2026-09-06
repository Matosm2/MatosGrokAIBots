"""session-orb-v1 — UTC midnight opening-range breakout (30m OR from 5m bars)."""

from __future__ import annotations

from dataclasses import dataclass
from backtest.data import Bar
from backtest.indicators import atr

STRATEGY_ID = "session-orb-v1"

MS_DAY = 86_400_000
MS_MINUTE = 60_000


@dataclass(frozen=True)
class SessionOrbParams:
    or_minutes: int = 30
    atr_len: int = 14
    max_or_atr_mult: float = 2.0
    # Vol filter frozen OFF this wave.
    vol_filter: bool = False


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def _minutes_from_midnight(open_time_ms: int) -> int:
    return int((open_time_ms % MS_DAY) // MS_MINUTE)


def compute_signals(
    bars: list[Bar],
    params: SessionOrbParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    UTC midnight session ORB on 5m (or any sub-daily) bars.

    OR window: first `or_minutes` after 00:00 UTC.
    Skip session if OR height > max_or_atr_mult × ATR(atr_len) on OR close bar.
    One trade/session. Entry: close > OR high after window closes.
    Exit: close >= OR_high + OR_height, close < OR_low (stop), or last bar of UTC day.
    Vol filter OFF (frozen).
    """
    params = params or SessionOrbParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    atr_s = atr(highs, lows, closes, params.atr_len)

    # Session state
    cur_day = -1
    or_high: float | None = None
    or_low: float | None = None
    or_complete = False
    or_skip = False
    traded = False
    in_pos = False
    stop_level: float | None = None
    target_level = 0.0

    for i, bar in enumerate(bars):
        day = _utc_day_start_ms(bar.open_time_ms)
        mins = _minutes_from_midnight(bar.open_time_ms)
        is_last_bar_of_day = (
            i == n - 1
            or _utc_day_start_ms(bars[i + 1].open_time_ms) != day
        )

        if day != cur_day:
            # New UTC session
            cur_day = day
            or_high = None
            or_low = None
            or_complete = False
            or_skip = False
            traded = False
            # Force flat across session boundary if somehow still long
            if in_pos:
                sells[i] = True
                in_pos = False
                stop_level = None

        # Build OR during window [0, or_minutes)
        if mins < params.or_minutes:
            if or_high is None:
                or_high = highs[i]
                or_low = lows[i]
            else:
                or_high = max(or_high, highs[i])
                or_low = min(or_low, lows[i])  # type: ignore[arg-type]
            # On last bar of OR window, evaluate skip filter
            next_mins = (
                params.or_minutes
                if i == n - 1
                else _minutes_from_midnight(bars[i + 1].open_time_ms)
            )
            day_next = day if i == n - 1 else _utc_day_start_ms(bars[i + 1].open_time_ms)
            if next_mins >= params.or_minutes or day_next != day:
                or_complete = True
                a = atr_s[i]
                if (
                    or_high is not None
                    and or_low is not None
                    and a is not None
                    and (or_high - or_low) > params.max_or_atr_mult * a
                ):
                    or_skip = True
            if in_pos:
                stops[i] = stop_level
            continue

        # After OR window
        if not or_complete and or_high is not None:
            # Edge: bars start mid-session without OR build (incomplete history)
            or_complete = True

        if in_pos:
            stops[i] = stop_level
            hit_target = closes[i] >= target_level
            if hit_target or is_last_bar_of_day:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if (
            or_complete
            and not or_skip
            and not traded
            and or_high is not None
            and or_low is not None
            and closes[i] > or_high
        ):
            height = or_high - or_low
            buys[i] = True
            traded = True
            in_pos = True
            stop_level = or_low
            target_level = or_high + height
            stops[i] = stop_level

    return buys, sells, stops
