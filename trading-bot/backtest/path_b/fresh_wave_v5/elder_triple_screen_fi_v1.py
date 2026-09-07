"""elder-triple-screen-fi-v1 — HTF MACD-hist tide + FI EMA pullback + buy-stop."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import ema, force_index, macd_hist
from backtest.path_b.engine import apply_position_gate
from backtest.path_b.fresh_wave_v5.mtf_join import map_htf_onto_ltf

STRATEGY_ID = "elder-triple-screen-fi-v1"


@dataclass(frozen=True)
class ElderTripleScreenParams:
    fi_ema: int = 2
    cancel_bars: int = 2
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9


def _tide_hist_rising(tide_bars: list[Bar], params: ElderTripleScreenParams) -> list[bool]:
    closes = [b.close for b in tide_bars]
    _m, _s, hist = macd_hist(closes, params.macd_fast, params.macd_slow, params.macd_signal)
    n = len(tide_bars)
    rising = [False] * n
    for i in range(1, n):
        h, h1 = hist[i], hist[i - 1]
        if h is None or h1 is None:
            continue
        rising[i] = h > h1
    return rising


def compute_raw(
    entry_bars: list[Bar],
    tide_bars: list[Bar],
    entry_tf: str,
    tide_tf: str,
    params: ElderTripleScreenParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    Screen1: tide MACD-hist rising (long-only bias).
    Screen2: EMA(FI, fi_ema) < 0 (pullback).
    Screen3: arm buy-stop at prior bar high; fill on close >= stop within cancel_bars;
             cancel if not filled.
    Exit: tide hist not rising OR EMA(FI) > 0 (opposite FI).
    Returns raw_long, raw_exit, stop_prices (entry stop unused by engine for entry).
    """
    params = params or ElderTripleScreenParams()
    n = len(entry_bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0 or not tide_bars:
        return raw_long, raw_exit, stops

    tide_rising = _tide_hist_rising(tide_bars, params)
    mapped_rising = map_htf_onto_ltf(
        ltf_open_ms=[b.open_time_ms for b in entry_bars],
        ltf_tf=entry_tf,
        htf_open_ms=[b.open_time_ms for b in tide_bars],
        htf_values=tide_rising,
        htf_tf=tide_tf,
    )

    closes = [b.close for b in entry_bars]
    volumes = [b.volume for b in entry_bars]
    highs = [b.high for b in entry_bars]
    fi_raw = force_index(closes, volumes)
    # Dense FI for EMA (skip leading None)
    fi_dense: list[float] = []
    fi_idx: list[int] = []
    for i, v in enumerate(fi_raw):
        if v is None:
            continue
        fi_dense.append(v)
        fi_idx.append(i)
    fi_ema_s: list[float | None] = [None] * n
    if len(fi_dense) >= params.fi_ema:
        smoothed = ema(fi_dense, params.fi_ema)
        for j, i in enumerate(fi_idx):
            fi_ema_s[i] = smoothed[j]

    # Arm state for buy-stop
    armed = False
    arm_level = 0.0
    bars_left = 0

    for i in range(n):
        tide_ok = mapped_rising[i] is True
        fi_v = fi_ema_s[i]
        fi_pullback = fi_v is not None and fi_v < 0.0
        fi_opposite = fi_v is not None and fi_v > 0.0

        # Exit while would-be in position handled by gate; emit exit conditions always
        if (mapped_rising[i] is False) or fi_opposite:
            raw_exit[i] = True

        if armed:
            bars_left -= 1
            if closes[i] >= arm_level:
                raw_long[i] = True
                stops[i] = arm_level  # informational; engine uses exit stops only
                armed = False
                bars_left = 0
            elif bars_left <= 0:
                armed = False
            continue

        # Setup: tide rising AND FI EMA < 0 → arm buy-stop at prior high
        if tide_ok and fi_pullback and i >= 1:
            armed = True
            arm_level = highs[i - 1]
            bars_left = params.cancel_bars
            # Same-bar fill if close already through prior high
            if closes[i] >= arm_level:
                raw_long[i] = True
                stops[i] = arm_level
                armed = False
                bars_left = 0

    return raw_long, raw_exit, stops


def compute_signals(
    entry_bars: list[Bar],
    tide_bars: list[Bar],
    entry_tf: str,
    tide_tf: str,
    params: ElderTripleScreenParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    raw_long, raw_exit, _stops = compute_raw(
        entry_bars, tide_bars, entry_tf, tide_tf, params
    )
    buys, sells = apply_position_gate(raw_long, raw_exit)
    # Rebuild stops only on buy bars (prior-high informational; no engine entry stop)
    stops: list[float | None] = [None] * len(entry_bars)
    return buys, sells, stops
