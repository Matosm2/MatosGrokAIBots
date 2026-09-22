"""pdh-pdl-accept-break-v1 — Prior UTC day high/low accept-break (+ optional retest).

Levels:
  PDH = prior UTC day high
  PDL = prior UTC day low

Mode A (accept-break):
  Long when close > PDH after prior close <= PDH.
Mode B (break+retest):
  After Mode A trigger occurs, wait for pullback tag of PDH (bar.low <= PDH)
  then closed-bar hold in break direction (bar.close >= PDH).

Optional RVOL gate: volume > k * SMA(volume, 20) on break bar (k in {off/0.0, 1.0, 1.5, 2.0}).
Exit: close back inside prior day range (close < PDH); or ATR trail / opposite.

≠ Camarilla / Woodie; ≠ Session ORB; ≠ ICT FVG-only primary.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, sma

STRATEGY_ID = "pdh-pdl-accept-break-v1"
MS_DAY = 86_400_000


@dataclass(frozen=True)
class PdhPdlParams:
    mode: str = "mode_a"  # "mode_a" (accept-break) | "mode_b" (break+retest hold)
    rvol_k: float = 0.0  # 0.0 = off, else volume > k * SMA(volume, 20)
    atr_trail_mult: float = 0.0  # 0.0 = exit on close < PDH; >0 = ATR trail stop
    atr_len: int = 14
    vol_len: int = 20
    one_trade_per_day: bool = True


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def compute_signals(
    bars: list[Bar],
    params: PdhPdlParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pdh-pdl-accept-break-v1."""
    params = params or PdhPdlParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    # Precompute running prior day high/low
    day_ohlc: dict[int, tuple[float, float, float]] = {}
    cur = -1
    dh = dl = dc = 0.0
    for b in bars:
        d = _utc_day_start_ms(b.open_time_ms)
        if d != cur:
            if cur >= 0:
                day_ohlc[cur] = (dh, dl, dc)
            cur = d
            dh, dl, dc = b.high, b.low, b.close
        else:
            dh = max(dh, b.high)
            dl = min(dl, b.low)
            dc = b.close
    if cur >= 0:
        day_ohlc[cur] = (dh, dl, dc)

    vols = [b.volume for b in bars]
    vol_sma = sma(vols, params.vol_len) if params.rvol_k > 0.0 else [None] * n

    atr_vals: list[float | None] = [None] * n
    if params.atr_trail_mult > 0.0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    mode = params.mode.lower()
    cur_day = -1
    pdh: float | None = None
    pdl: float | None = None
    traded = False
    in_pos = False
    waiting_retest = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i, bar in enumerate(bars):
        day = _utc_day_start_ms(bar.open_time_ms)
        is_last_in_day = i == n - 1 or _utc_day_start_ms(bars[i + 1].open_time_ms) != day

        if day != cur_day:
            cur_day = day
            traded = False
            waiting_retest = False
            prior = day - MS_DAY
            if prior in day_ohlc:
                pdh, pdl, _ = day_ohlc[prior]
            else:
                pdh = pdl = None
            if in_pos:
                # EOD flat
                sells[i] = True
                in_pos = False
                stop_level = None

        if pdh is None or pdl is None:
            continue

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, bar.close)

            # Exit rule:
            # 1. Back inside prior day range: close < PDH (or stop_level)
            # 2. Or ATR trail: close < highest - atr * mult
            # 3. Or session close
            exit_signal = False
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or pdh, trail_stop)
                stops[i] = stop_level
                if bar.close < stop_level:
                    exit_signal = True
            else:
                if bar.close < pdh:
                    exit_signal = True

            if is_last_in_day:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if params.one_trade_per_day and traded:
            continue

        # Volume gate check
        vol_ok = True
        if params.rvol_k > 0.0:
            v_ref = vol_sma[i]
            vol_ok = v_ref is not None and v_ref > 0 and bar.volume >= params.rvol_k * v_ref

        prev_c = bars[i - 1].close if i > 0 else bar.open
        break_up = bar.close > pdh and prev_c <= pdh

        if mode == "mode_a":
            if break_up and vol_ok:
                buys[i] = True
                traded = True
                in_pos = True
                highest_since_entry = bar.close
                stop_level = pdh
                stops[i] = stop_level
        else:
            # Mode B: break + retest hold
            if not waiting_retest:
                if break_up and vol_ok:
                    waiting_retest = True
            else:
                # Retest: touched PDH (low <= PDH) and held (close >= PDH)
                if bar.low <= pdh and bar.close >= pdh:
                    buys[i] = True
                    traded = True
                    in_pos = True
                    waiting_retest = False
                    highest_since_entry = bar.close
                    stop_level = pdh
                    stops[i] = stop_level
                elif bar.close < pdh:
                    # Retest failed, broke down back inside
                    waiting_retest = False

    return buys, sells, stops
