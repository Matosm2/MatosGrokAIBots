"""ultimate-oscillator-v1 — Williams UO classic divergence / Mode-B cross 30."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import ultimate_oscillator
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "ultimate-oscillator-v1"


@dataclass(frozen=True)
class UltimateOscParams:
    short: int = 7
    mid: int = 14
    long: int = 28
    mode: str = "classic"  # classic | B
    os_level: float = 30.0
    ob_level: float = 70.0
    mid_down: float = 45.0
    mid_up: float = 50.0
    lookback: int = 14  # divergence / interim high window


def compute_raw(
    bars: list[Bar],
    params: UltimateOscParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Classic: UO made low <30 with price lower-low / UO higher-low (bull div),
             then break above interim UO high since that UO low.
    Mode-B (simplified): cross up through 30.
    Exit: UO≥70, or after >50 then <45, or cross back below 30 (Mode-B opposite).
    """
    params = params or UltimateOscParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    uo = ultimate_oscillator(
        highs, lows, closes, params.short, params.mid, params.long
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    mode = params.mode.lower()

    # Track whether UO has been above mid_up since entry window (for exit rule)
    seen_above_50 = False

    if mode in ("b", "mode-b", "mode_b", "cross"):
        for i in range(1, n):
            cur, prev = uo[i], uo[i - 1]
            if cur is None or prev is None:
                continue
            if prev < params.os_level <= cur:
                raw_long[i] = True
            if cur >= params.ob_level:
                raw_exit[i] = True
            elif prev > params.mid_up:
                seen_above_50 = True
            if seen_above_50 and cur < params.mid_down:
                raw_exit[i] = True
            if cur < params.os_level and prev >= params.os_level:
                raw_exit[i] = True
        return raw_long, raw_exit

    # Classic divergence + break interim UO high
    # Find bullish divergence pivots in rolling lookback
    pending_interim_high: float | None = None
    div_uo_low_idx: int | None = None

    for i in range(1, n):
        cur = uo[i]
        if cur is None:
            continue

        # Exit rules always
        if cur >= params.ob_level:
            raw_exit[i] = True
            pending_interim_high = None
            div_uo_low_idx = None
        # Track mid exit via local state in gate path — approximate with series:
        if i >= 1 and uo[i - 1] is not None:
            if uo[i - 1] > params.mid_up and cur < params.mid_down:
                raw_exit[i] = True

        lb = params.lookback
        if i < lb + 2:
            continue

        # Detect: current UO is a local low < os_level; compare to prior UO low in window
        is_uo_local_low = (
            uo[i - 1] is not None
            and uo[i - 2] is not None
            and uo[i - 1] < uo[i - 2]
            and uo[i - 1] < cur
            and uo[i - 1] < params.os_level
        )
        if is_uo_local_low:
            j = i - 1
            # Find earlier UO low in [j-lookback, j)
            earlier = None
            for k in range(max(1, j - lb), j):
                if uo[k] is None:
                    continue
                if uo[k - 1] is None or uo[k + 1] is None:
                    continue
                if uo[k] < uo[k - 1] and uo[k] < uo[k + 1] and uo[k] < params.os_level:
                    earlier = k
            if earlier is not None and uo[j] is not None and uo[earlier] is not None:
                # Price LL, UO HL
                if lows[j] < lows[earlier] and uo[j] > uo[earlier]:
                    div_uo_low_idx = j
                    # Interim UO high = max UO from earlier to j
                    window_uo = [uo[t] for t in range(earlier, j + 1) if uo[t] is not None]
                    pending_interim_high = max(window_uo) if window_uo else None

        if pending_interim_high is not None and cur > pending_interim_high:
            raw_long[i] = True
            pending_interim_high = None
            div_uo_low_idx = None

    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: UltimateOscParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
