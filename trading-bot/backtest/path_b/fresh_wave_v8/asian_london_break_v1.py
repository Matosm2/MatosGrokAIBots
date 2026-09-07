"""asian-london-break-v1 — Asian box 00:00–07:00 UTC → London break. ≠ Session ORB / Donchian."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar

STRATEGY_ID = "asian-london-break-v1"

MS_DAY = 86_400_000
MS_MINUTE = 60_000


@dataclass(frozen=True)
class AsianLondonParams:
    box_start_min: int = 0  # 00:00 UTC
    box_end_min: int = 7 * 60  # 07:00 UTC (exclusive end of box window)
    flat_min: int = 16 * 60  # 16:00 UTC flat
    tp_mult: float = 1.0
    # mid = box midpoint; opposite = Asian low (long stop).
    stop_mode: str = "mid"


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def _minutes_from_midnight(open_time_ms: int) -> int:
    return int((open_time_ms % MS_DAY) // MS_MINUTE)


def compute_signals(
    bars: list[Bar],
    params: AsianLondonParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    Asian multi-hour box (00:00–07:00 UTC) then London liquidity break — NOT Session ORB.

    Box: H/L of bars whose open is in [00:00, 07:00) UTC.
    After 07:00: long when close > Asian high (one trade/day).
    Stop: mid-box (default) or opposite (Asian low).
    TP: Asian high + tp_mult × box height, OR flat at/after 16:00 UTC.
    Forbidden: first-N-min Session ORB encode; Donchian(N) substitute.
    """
    params = params or AsianLondonParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    cur_day = -1
    box_high: float | None = None
    box_low: float | None = None
    box_ready = False
    traded = False
    in_pos = False
    stop_level: float | None = None
    target_level = 0.0

    for i, bar in enumerate(bars):
        day = _utc_day_start_ms(bar.open_time_ms)
        mins = _minutes_from_midnight(bar.open_time_ms)

        if day != cur_day:
            cur_day = day
            box_high = None
            box_low = None
            box_ready = False
            traded = False
            if in_pos:
                sells[i] = True
                in_pos = False
                stop_level = None

        # Build Asian box during [box_start, box_end)
        if params.box_start_min <= mins < params.box_end_min:
            if box_high is None:
                box_high = highs[i]
                box_low = lows[i]
            else:
                box_high = max(box_high, highs[i])
                box_low = min(box_low, lows[i])  # type: ignore[arg-type]
            # Mark ready when next bar leaves the box window (or end of series).
            next_mins = (
                params.box_end_min
                if i == n - 1
                else _minutes_from_midnight(bars[i + 1].open_time_ms)
            )
            day_next = day if i == n - 1 else _utc_day_start_ms(bars[i + 1].open_time_ms)
            if next_mins >= params.box_end_min or day_next != day:
                box_ready = box_high is not None and box_low is not None
            if in_pos:
                stops[i] = stop_level
            continue

        # After box window
        if not box_ready and box_high is not None and box_low is not None:
            # Incomplete history starting mid-session — treat as ready once past end.
            if mins >= params.box_end_min:
                box_ready = True

        # 16:00 UTC flat (bar open at/after flat_min)
        at_or_after_flat = mins >= params.flat_min

        if in_pos:
            stops[i] = stop_level
            hit_target = closes[i] >= target_level
            if hit_target or at_or_after_flat:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if (
            box_ready
            and not traded
            and not at_or_after_flat
            and mins >= params.box_end_min
            and box_high is not None
            and box_low is not None
            and closes[i] > box_high
        ):
            height = box_high - box_low
            if height <= 0.0:
                continue
            buys[i] = True
            traded = True
            in_pos = True
            if params.stop_mode == "opposite":
                stop_level = box_low
            else:
                stop_level = (box_high + box_low) / 2.0
            target_level = box_high + params.tp_mult * height
            stops[i] = stop_level

    return buys, sells, stops
