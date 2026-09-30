"""classic-floor-pivots-utc-v1 — Classic floor pivots PP/R1/S1/R2/S2 (UTC session).

Levels (prior UTC day or week H/L/C):
  PP = (H + L + C) / 3
  R1 = 2 * PP - L
  S1 = 2 * PP - H
  R2 = PP + (H - L)
  S2 = PP - (H - L)

≠ Woodie (P=(H+L+2C)/4); ≠ Camarilla multipliers; ≠ Session ORB; ≠ VWAP±σ grafts.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr

STRATEGY_ID = "classic-floor-pivots-utc-v1"
MS_DAY = 86_400_000
MS_WEEK = 7 * MS_DAY


@dataclass(frozen=True)
class ClassicFloorPivotsParams:
    mode: str = "mode_a"  # "mode_a" (fade S1 bounce) | "mode_b" (break R1)
    period: str = "day"  # "day" | "week"
    one_trade_per_day: bool = True
    atr_buffer_k: float = 0.0  # 0.0 (beyond S2 for fade / past break level for break) or >0 (atr*k buffer)
    atr_len: int = 14


@dataclass(frozen=True)
class FloorPivotLevels:
    pp: float
    r1: float
    s1: float
    r2: float
    s2: float


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def _utc_week_start_ms(open_time_ms: int) -> int:
    # 1970-01-01 was a Thursday (day 4).
    # (day_index + 4) % 7 == 0 on Monday UTC.
    day_idx = open_time_ms // MS_DAY
    # Monday is offset (day_idx - ((day_idx + 3) % 7))
    # Thursday: (0 + 3)%7 = 3 -> day_idx - 3 = day -3 (Monday Dec 29 1969)
    # Check: day_idx=4 (Monday Jan 5 1970): (4+3)%7 = 0 -> day_idx - 0 = 4 (Monday)
    mon_day_idx = day_idx - ((day_idx + 3) % 7)
    return mon_day_idx * MS_DAY


def floor_pivots_from_hlc(h: float, lo: float, c: float) -> FloorPivotLevels:
    """Classic floor pivots: PP=(H+L+C)/3, R1=2PP-L, S1=2PP-H, R2=PP+(H-L), S2=PP-(H-L)."""
    pp = (h + lo + c) / 3.0
    r1 = 2.0 * pp - lo
    s1 = 2.0 * pp - h
    r2 = pp + (h - lo)
    s2 = pp - (h - lo)
    return FloorPivotLevels(pp=pp, r1=r1, s1=s1, r2=r2, s2=s2)


def compute_signals(
    bars: list[Bar],
    params: ClassicFloorPivotsParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute entry buys, exit sells, and active stop levels.

    Mode A (fade):
      Long on closed bar: touched <= S1 and close > S1 (or close >= S1).
      Stop: beyond S2 (or S1 - atr*k).
      Target: PP then R1/R2 (exit if close >= PP or EOD UTC).
    Mode B (break):
      Long on closed bar: close > R1 after prior close <= R1.
      Stop: PP (or R1 - atr*k).
      Target: R2 (exit if close >= R2 or close <= PP or EOD UTC).
    """
    params = params or ClassicFloorPivotsParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    period_is_week = params.period.lower() == "week"
    bucket_fn = _utc_week_start_ms if period_is_week else _utc_day_start_ms
    bucket_dur = MS_WEEK if period_is_week else MS_DAY

    # Pre-aggregate prior bucket H/L/C
    bucket_ohlc: dict[int, tuple[float, float, float]] = {}
    cur = -1
    bh = blo = bc = 0.0
    for b in bars:
        bkt = bucket_fn(b.open_time_ms)
        if bkt != cur:
            if cur >= 0:
                bucket_ohlc[cur] = (bh, blo, bc)
            cur = bkt
            bh, blo, bc = b.high, b.low, b.close
        else:
            bh = max(bh, b.high)
            blo = min(blo, b.low)
            bc = b.close
    if cur >= 0:
        bucket_ohlc[cur] = (bh, blo, bc)

    atr_vals: list[float | None] = [None] * n
    if params.atr_buffer_k > 0:
        highs = [b.high for b in bars]
        lows = [b.low for b in bars]
        closes = [b.close for b in bars]
        atr_vals = atr(highs, lows, closes, params.atr_len)

    mode = params.mode.lower()
    cur_bucket = -1
    lv: FloorPivotLevels | None = None
    traded = False
    in_pos = False
    stop_level: float | None = None

    for i, bar in enumerate(bars):
        bkt = bucket_fn(bar.open_time_ms)
        is_last_in_bkt = i == n - 1 or bucket_fn(bars[i + 1].open_time_ms) != bkt

        if bkt != cur_bucket:
            cur_bucket = bkt
            traded = False
            prior = bkt - bucket_dur
            if prior in bucket_ohlc:
                ph, plo, pc = bucket_ohlc[prior]
                lv = floor_pivots_from_hlc(ph, plo, pc)
            else:
                lv = None
            if in_pos:
                # EOD/EOW flat
                sells[i] = True
                in_pos = False
                stop_level = None

        if lv is None:
            continue

        if in_pos:
            stops[i] = stop_level
            if mode == "mode_a":
                # Exit target PP or R1, or session close
                hit_tgt = bar.close >= lv.pp or is_last_in_bkt
                if hit_tgt:
                    sells[i] = True
                    in_pos = False
                    stop_level = None
            else:
                # Mode B target R2 or back below PP or session close
                hit_tgt = bar.close >= lv.r2 or bar.close <= lv.pp or is_last_in_bkt
                if hit_tgt:
                    sells[i] = True
                    in_pos = False
                    stop_level = None
            continue

        if params.one_trade_per_day and traded:
            continue

        a_buf = (atr_vals[i] * params.atr_buffer_k) if (atr_vals[i] is not None and params.atr_buffer_k > 0) else 0.0

        if mode == "mode_a":
            # Rejection bounce: touched <= S1 and close > S1
            if bar.low <= lv.s1 and bar.close > lv.s1:
                buys[i] = True
                traded = True
                in_pos = True
                stop_level = (lv.s1 - a_buf) if params.atr_buffer_k > 0 else lv.s2
                stops[i] = stop_level
        else:
            # Mode B break: close > R1 after prior close <= R1
            prev_c = bars[i - 1].close if i > 0 else bar.open
            if bar.close > lv.r1 and prev_c <= lv.r1:
                buys[i] = True
                traded = True
                in_pos = True
                stop_level = (lv.r1 - a_buf) if params.atr_buffer_k > 0 else lv.pp
                stops[i] = stop_level

    return buys, sells, stops
