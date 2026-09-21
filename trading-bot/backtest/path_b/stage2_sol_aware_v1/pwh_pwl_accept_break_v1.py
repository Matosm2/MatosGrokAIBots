"""pwh-pwl-accept-break-v1 — Prior UTC week high/low accept-break (+ optional retest).

LOCKED SPEC:
Levels:
  PWH = prior UTC ISO-week high (Monday 00:00 UTC -> next Monday 00:00 UTC)
  PWL = prior UTC ISO-week low
  Tracked via session-reset trackers on exec TF without request.security.

Entry Mode A (accept-break):
  Long: bar.close > PWH after prior close <= PWH.
  (Lead is long-only first pass).

Entry Mode B (break + retest):
  After Mode A break occurs, wait for pullback tag of broken PWH (bar.low <= PWH)
  then closed-bar hold in break direction (bar.close >= PWH).

Optional RVOL gate:
  volume > k * SMA(volume, 20) on break bar; k in {0.0 (off), 1.0, 1.5}.

Exit:
  Close back inside prior week range (close < PWH); or ATR trail stop; or end of week.

≠ PDH/PDL encode; ≠ Session ORB; ≠ Camarilla/Woodie; ≠ Donchian channel; ≠ floor pivots.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from backtest.data import Bar
from backtest.indicators import atr, sma

STRATEGY_ID = "pwh-pwl-accept-break-v1"


@dataclass(frozen=True)
class PwhPwlParams:
    mode: str = "mode_a"  # "mode_a" (accept-break) | "mode_b" (break+retest hold)
    rvol_k: float = 0.0  # 0.0 = off, else volume > k * SMA(volume, 20)
    atr_trail_mult: float = 0.0  # 0.0 = exit on close < PWH; >0 = ATR trail stop
    atr_len: int = 14
    vol_len: int = 20
    one_trade_per_week: bool = True


def _utc_week_key(open_time_ms: int) -> tuple[int, int]:
    """Return (iso_year, iso_week) for Monday 00:00 UTC boundary."""
    dt = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc)
    isocal = dt.isocalendar()
    return (isocal[0], isocal[1])


def compute_signals(
    bars: list[Bar],
    params: PwhPwlParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pwh-pwl-accept-break-v1."""
    params = params or PwhPwlParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    # Precompute high and low for each ISO week
    week_ohlc: dict[tuple[int, int], tuple[float, float, float]] = {}
    ordered_weeks: list[tuple[int, int]] = []
    cur_wk: tuple[int, int] | None = None
    wh = wl = wc = 0.0

    for b in bars:
        wk = _utc_week_key(b.open_time_ms)
        if wk != cur_wk:
            if cur_wk is not None:
                week_ohlc[cur_wk] = (wh, wl, wc)
            cur_wk = wk
            if cur_wk not in week_ohlc:
                ordered_weeks.append(cur_wk)
            wh, wl, wc = b.high, b.low, b.close
        else:
            wh = max(wh, b.high)
            wl = min(wl, b.low)
            wc = b.close
    if cur_wk is not None:
        week_ohlc[cur_wk] = (wh, wl, wc)

    # Map each week to its prior week high and low
    prior_week_map: dict[tuple[int, int], tuple[float, float]] = {}
    for idx in range(1, len(ordered_weeks)):
        prev_wk = ordered_weeks[idx - 1]
        curr_wk = ordered_weeks[idx]
        if prev_wk in week_ohlc:
            prior_week_map[curr_wk] = (week_ohlc[prev_wk][0], week_ohlc[prev_wk][1])

    vols = [b.volume for b in bars]
    vol_sma = sma(vols, params.vol_len) if params.rvol_k > 0.0 else [None] * n

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    mode = params.mode.lower()
    active_week: tuple[int, int] | None = None
    pwh: float | None = None
    pwl: float | None = None
    traded = False
    in_pos = False
    waiting_retest = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i, bar in enumerate(bars):
        wk = _utc_week_key(bar.open_time_ms)
        is_last_in_week = i == n - 1 or _utc_week_key(bars[i + 1].open_time_ms) != wk

        if wk != active_week:
            active_week = wk
            traded = False
            waiting_retest = False
            if wk in prior_week_map:
                pwh, pwl = prior_week_map[wk]
            else:
                pwh = pwl = None
            if in_pos:
                # End of week closeout
                sells[i] = True
                in_pos = False
                stop_level = None

        if pwh is None or pwl is None:
            continue

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, bar.close)

            # Exit conditions:
            # 1. Close back inside prior week range (bar.close < PWH)
            # 2. Or ATR trailing stop
            # 3. Or end of week
            exit_signal = False
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or pwh, trail_stop)
                stops[i] = stop_level
                if bar.close < stop_level:
                    exit_signal = True
            else:
                if bar.close < pwh:
                    exit_signal = True

            if is_last_in_week:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if params.one_trade_per_week and traded:
            continue

        # RVOL volume gate check
        vol_ok = True
        if params.rvol_k > 0.0:
            v_ref = vol_sma[i]
            vol_ok = v_ref is not None and v_ref > 0 and bar.volume >= params.rvol_k * v_ref

        prev_c = bars[i - 1].close if i > 0 else bar.open
        break_up = bar.close > pwh and prev_c <= pwh

        if mode == "mode_a":
            if break_up and vol_ok:
                buys[i] = True
                traded = True
                in_pos = True
                highest_since_entry = bar.close
                stop_level = pwh
                stops[i] = stop_level
        else:
            # Mode B: break + retest hold
            if not waiting_retest:
                if break_up and vol_ok:
                    waiting_retest = True
            else:
                # Retest: price touched broken PWH (low <= PWH) and held above it on bar close (close >= PWH)
                if bar.low <= pwh and bar.close >= pwh:
                    buys[i] = True
                    traded = True
                    in_pos = True
                    waiting_retest = False
                    highest_since_entry = bar.close
                    stop_level = pwh
                    stops[i] = stop_level
                elif bar.close < pwh:
                    # Retest failed, broke down inside
                    waiting_retest = False

    return buys, sells, stops
