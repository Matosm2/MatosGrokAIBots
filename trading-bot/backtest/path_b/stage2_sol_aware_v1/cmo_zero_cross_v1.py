"""cmo-zero-cross-v1 — Chande Momentum Oscillator Zero-Cross / Signal-MA Flip.

LOCKED SPEC:
strategy_id MUST be exactly cmo-zero-cross-v1 (NEVER cmo-zone-v1).
Formula:
  CMO(Length) = 100 * (Su - Sd) / (Su + Sd) from close deltas.
  Default Length 20 (sweep {14, 20, 25}).

Entry Mode A (primary — distinct from failed zone burn):
  Long: CMO crosses above 0 (crossover(CMO, 0)).

Entry Mode B (signal-line cross):
  Long: CMO crosses above SMA(CMO, 9).

Do NOT encode:
  Leave -50 oversold zone / exit-at-0 zone (failed weekly encode).

Exit:
  Opposite cross (Mode A: CMO crosses below 0; Mode B: CMO crosses below SMA(CMO, 9));
  or optional ATR trail stop.

≠ RSI graft; ≠ zone-50 primary; ≠ ConnorsRSI; ≠ DeMarker.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, cmo, crossover, crossunder, sma

STRATEGY_ID = "cmo-zero-cross-v1"


@dataclass(frozen=True)
class CmoZeroCrossParams:
    length: int = 20  # {14, 20, 25}
    mode: str = "mode_a"  # "mode_a" (zero cross) | "mode_b" (cmo x sma9)
    signal_len: int = 9  # For mode_b
    atr_trail_mult: float = 0.0  # 0.0 = opposite cross only; >0 = ATR trail stop
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: CmoZeroCrossParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for cmo-zero-cross-v1."""
    params = params or CmoZeroCrossParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    cmo_vals = cmo(closes, params.length)

    signal_line: list[float | None] = [None] * n
    if params.mode.lower() == "mode_b":
        # SMA of CMO
        valid_cmo = [v if v is not None else 0.0 for v in cmo_vals]
        signal_line = sma(valid_cmo, params.signal_len)
        for i in range(n):
            if cmo_vals[i] is None:
                signal_line[i] = None

    zero_line: list[float | None] = [0.0] * n

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        if cmo_vals[i] is None:
            continue

        if params.mode.lower() == "mode_b":
            if signal_line[i] is None:
                continue
            cross_up = crossover(cmo_vals, signal_line, i)
            cross_down = crossunder(cmo_vals, signal_line, i)
        else:
            # Mode A: zero cross
            cross_up = crossover(cmo_vals, zero_line, i)
            cross_down = crossunder(cmo_vals, zero_line, i)

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, bars[i].close)

            exit_hit = False
            if cross_down:
                exit_hit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if bars[i].close < stop_level:
                    exit_hit = True

            if exit_hit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if cross_up:
            buys[i] = True
            in_pos = True
            highest_since_entry = bars[i].close
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = bars[i].close - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level
            else:
                stop_level = None

    return buys, sells, stops
