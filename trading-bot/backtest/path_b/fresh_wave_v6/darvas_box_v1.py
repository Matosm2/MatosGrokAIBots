"""darvas-box-v1 — Stateful Darvas box (NOT Donchian).

Lookback new-high seed → confirm bars for top then bottom → buy close > box top;
trail exit on close < box floor. Distinct from rolling Donchian(N).
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "darvas-box-v1"


@dataclass(frozen=True)
class DarvasBoxParams:
    lookback: int = 90
    confirm: int = 3


def compute_raw(
    bars: list[Bar],
    params: DarvasBoxParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    State machine (bar-close, no lookahead):

    SEEK_HIGH: bar high is highest of last `lookback` → candidate top, CONFIRM_TOP.
    CONFIRM_TOP: `confirm` bars without a higher high → SEEK_BOTTOM.
                 New high resets candidate.
    SEEK_BOTTOM / CONFIRM_BOTTOM: track lowest low since top confirmed;
                 `confirm` bars without a lower low → BOX_READY (top, bottom).
                 Break above top before bottom confirmed → restart SEEK_HIGH.
    BOX_READY: close > top → long; invalidate if close < bottom.
    While conceptually long, new completed boxes raise the trail floor;
    exit when close < active floor.
    """
    params = params or DarvasBoxParams()
    n = len(bars)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    raw_long = [False] * n
    raw_exit = [False] * n

    LOOKBACK = params.lookback
    CONF = params.confirm

    state = "SEEK_HIGH"
    cand_top = 0.0
    cand_bottom = 0.0
    confirm_count = 0
    box_top: float | None = None
    box_bottom: float | None = None
    trail_floor: float | None = None

    for i in range(n):
        h, lo, c = highs[i], lows[i], closes[i]

        # Exit check against trail / box floor (always)
        if trail_floor is not None and c < trail_floor:
            raw_exit[i] = True
            trail_floor = None
            # keep box state; may re-enter on later breakout

        if state == "SEEK_HIGH":
            if i + 1 >= LOOKBACK:
                window_high = max(highs[i - LOOKBACK + 1 : i + 1])
                if h >= window_high and h == window_high:
                    cand_top = h
                    confirm_count = 0
                    state = "CONFIRM_TOP"

        elif state == "CONFIRM_TOP":
            if h > cand_top:
                cand_top = h
                confirm_count = 0
            else:
                confirm_count += 1
                if confirm_count >= CONF:
                    cand_bottom = lo
                    confirm_count = 0
                    state = "CONFIRM_BOTTOM"

        elif state == "CONFIRM_BOTTOM":
            if h > cand_top:
                # Broke above before bottom confirmed — new high seed
                cand_top = h
                confirm_count = 0
                state = "CONFIRM_TOP"
            elif lo < cand_bottom:
                cand_bottom = lo
                confirm_count = 0
            else:
                confirm_count += 1
                if confirm_count >= CONF:
                    box_top = cand_top
                    box_bottom = cand_bottom
                    state = "BOX_READY"
                    if trail_floor is not None and box_bottom > trail_floor:
                        trail_floor = box_bottom

        elif state == "BOX_READY":
            assert box_top is not None and box_bottom is not None
            if c > box_top:
                raw_long[i] = True
                trail_floor = box_bottom
                # After breakout, seek a new higher box (classic Darvas pyramid of boxes)
                state = "SEEK_HIGH"
                confirm_count = 0
            elif c < box_bottom:
                # Box invalidated without entry
                box_top = None
                box_bottom = None
                state = "SEEK_HIGH"
                confirm_count = 0
            else:
                # Still inside box — also watch for new high that starts next box
                if i + 1 >= LOOKBACK:
                    window_high = max(highs[i - LOOKBACK + 1 : i + 1])
                    if h >= window_high and h > box_top:
                        cand_top = h
                        confirm_count = 0
                        state = "CONFIRM_TOP"

        # If we are seeking a new box after entry, completed boxes raise trail
        if state == "CONFIRM_BOTTOM" and confirm_count >= CONF:
            # handled above when transitioning to BOX_READY
            pass

        # When a new box becomes ready while we have a trail, raise floor
        if (
            state == "BOX_READY"
            and box_bottom is not None
            and trail_floor is not None
            and box_bottom > trail_floor
            and not raw_long[i]
        ):
            trail_floor = box_bottom

    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: DarvasBoxParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
