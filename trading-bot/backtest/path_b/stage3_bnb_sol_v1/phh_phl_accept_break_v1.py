"""phh-phl-accept-break-v1 — Prior UTC clock-hour high/low accept-break (+ optional retest).

LOCKED SPEC:
Levels:
  PHH = prior UTC clock-hour high
  PHL = prior UTC clock-hour low
  Tracked via UTC wall-clock hour boundary tracker on exec TF without request.security.

Entry Mode A (accept-break):
  Long: bar.close > PHH after prior close <= PHH.
  (Lead is long-only first pass).

Entry Mode B (break + retest):
  After Mode A break occurs, wait for pullback tag of broken PHH (bar.low <= PHH)
  then closed-bar hold in break direction (bar.close >= PHH).

Optional RVOL gate:
  volume > k * SMA(volume, 20) on break bar; k in {0.0 (off), 1.0, 1.5}.

Exit:
  Close back inside prior hour range (bar.close < PHH); or ATR trail stop; or opposite level.

≠ PDH/PDL; ≠ PWH/PWL; ≠ Session ORB; ≠ Donchian-branded; ≠ floor/Camarilla/Woodie.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, sma

STRATEGY_ID = "phh-phl-accept-break-v1"
MS_HOUR = 3_600_000


@dataclass(frozen=True)
class PhhPhlParams:
    mode: str = "mode_a"  # "mode_a" (accept-break) | "mode_b" (break+retest hold)
    rvol_k: float = 0.0  # 0.0 = off, else volume > k * SMA(volume, 20)
    atr_trail_mult: float = 0.0  # 0.0 = exit on close < PHH; >0 = ATR trail stop
    atr_len: int = 14
    vol_len: int = 20
    one_trade_per_hour: bool = True


def _utc_hour_start_ms(open_time_ms: int) -> int:
    """Return UTC wall-clock hour start in ms."""
    return (open_time_ms // MS_HOUR) * MS_HOUR


def compute_signals(
    bars: list[Bar],
    params: PhhPhlParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for phh-phl-accept-break-v1."""
    params = params or PhhPhlParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    # Precompute high and low for each UTC hour
    hour_ohlc: dict[int, tuple[float, float, float]] = {}
    ordered_hours: list[int] = []
    cur_hr = -1
    hh = hl = hc = 0.0

    for b in bars:
        hr = _utc_hour_start_ms(b.open_time_ms)
        if hr != cur_hr:
            if cur_hr >= 0:
                hour_ohlc[cur_hr] = (hh, hl, hc)
            cur_hr = hr
            if cur_hr not in hour_ohlc:
                ordered_hours.append(cur_hr)
            hh, hl, hc = b.high, b.low, b.close
        else:
            hh = max(hh, b.high)
            hl = min(hl, b.low)
            hc = b.close
    if cur_hr >= 0:
        hour_ohlc[cur_hr] = (hh, hl, hc)

    # Map each hour to its prior hour high and low
    prior_hour_map: dict[int, tuple[float, float]] = {}
    for idx in range(1, len(ordered_hours)):
        prev_hr = ordered_hours[idx - 1]
        curr_hr = ordered_hours[idx]
        if prev_hr in hour_ohlc:
            prior_hour_map[curr_hr] = (hour_ohlc[prev_hr][0], hour_ohlc[prev_hr][1])

    vols = [b.volume for b in bars]
    vol_sma = sma(vols, params.vol_len) if params.rvol_k > 0.0 else [None] * n

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    mode = params.mode.lower()
    active_hour: int | None = None
    phh: float | None = None
    phl: float | None = None
    entry_phh: float | None = None
    traded = False
    in_pos = False
    waiting_retest = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i, bar in enumerate(bars):
        hr = _utc_hour_start_ms(bar.open_time_ms)

        if hr != active_hour:
            active_hour = hr
            traded = False
            waiting_retest = False
            if hr in prior_hour_map:
                phh, phl = prior_hour_map[hr]
            else:
                phh = phl = None

        if phh is None or phl is None:
            continue

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, bar.close)

            # Exit conditions:
            # 1. Close back inside prior hour range (bar.close < entry_phh)
            # 2. Or ATR trailing stop
            exit_signal = False
            ref_level = entry_phh or phh
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or ref_level, trail_stop)
                stops[i] = stop_level
                if bar.close < stop_level:
                    exit_signal = True
            else:
                if bar.close < ref_level:
                    exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                stop_level = None
                entry_phh = None
            continue

        if params.one_trade_per_hour and traded:
            continue

        # RVOL volume gate check on break bar
        vol_ok = True
        if params.rvol_k > 0.0:
            v_ref = vol_sma[i]
            vol_ok = v_ref is not None and v_ref > 0 and bar.volume >= params.rvol_k * v_ref

        prev_c = bars[i - 1].close if i > 0 else bar.open
        break_up = bar.close > phh and prev_c <= phh

        if mode == "mode_a":
            if break_up and vol_ok:
                buys[i] = True
                in_pos = True
                traded = True
                entry_phh = phh
                highest_since_entry = bar.close
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = bar.close - atr_vals[i] * params.atr_trail_mult
                    stops[i] = stop_level
                else:
                    stop_level = phh
                    stops[i] = stop_level

        elif mode == "mode_b":
            # Mode B: break occurs, wait for pullback tag (low <= phh) then hold (close >= phh)
            if not waiting_retest:
                if break_up and vol_ok:
                    waiting_retest = True
            else:
                # Retest bar: dipped to or below broken PHH and closed above or at PHH
                tagged = bar.low <= phh
                held = bar.close >= phh
                if tagged and held:
                    buys[i] = True
                    in_pos = True
                    traded = True
                    waiting_retest = False
                    entry_phh = phh
                    highest_since_entry = bar.close
                    if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                        stop_level = bar.close - atr_vals[i] * params.atr_trail_mult
                        stops[i] = stop_level
                    else:
                        stop_level = phh
                        stops[i] = stop_level
                elif bar.close < phh:
                    # Retest failed — invalidates setup
                    waiting_retest = False

    return buys, sells, stops
