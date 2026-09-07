"""woodie-utc-v1 — prior UTC-day Woodie pivots. ≠ Camarilla; ≠ Session ORB."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar

STRATEGY_ID = "woodie-utc-v1"

MS_DAY = 86_400_000


@dataclass(frozen=True)
class WoodieParams:
    # mode_a = fade S1 long (SL beyond S2); mode_b = close > R1
    mode: str = "mode_a"
    one_trade_per_day: bool = True


@dataclass(frozen=True)
class WoodieLevels:
    p: float
    r1: float
    r2: float
    s1: float
    s2: float


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def levels_from_ohlc(h: float, lo: float, c: float) -> WoodieLevels:
    """Woodie: P=(H+L+2C)/4; R1=2P−L; S1=2P−H; R2=P+(H−L); S2=P−(H−L)."""
    p = (h + lo + 2.0 * c) / 4.0
    r1 = 2.0 * p - lo
    s1 = 2.0 * p - h
    r2 = p + (h - lo)
    s2 = p - (h - lo)
    return WoodieLevels(p=p, r1=r1, r2=r2, s1=s1, s2=s2)


def compute_signals(
    bars: list[Bar],
    params: WoodieParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    Prior UTC calendar day H/L/C → Woodie levels (freeze at day open).

    Mode A: fade S1 long — touch/reclaim (low≤S1 and close≥S1); SL=S2; exit P or R1.
    Mode B: close > R1; exit ≤ P or EOD UTC.
    One-trade/day default. ≠ Camarilla multipliers; ≠ Session ORB first-N-min box.
    """
    params = params or WoodieParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    day_ohlc: dict[int, tuple[float, float, float]] = {}
    cur = -1
    dh = dl = dc = 0.0
    for b in bars:
        day = _utc_day_start_ms(b.open_time_ms)
        if day != cur:
            if cur >= 0:
                day_ohlc[cur] = (dh, dl, dc)
            cur = day
            dh, dl, dc = b.high, b.low, b.close
        else:
            dh = max(dh, b.high)
            dl = min(dl, b.low)
            dc = b.close
    if cur >= 0:
        day_ohlc[cur] = (dh, dl, dc)

    mode = params.mode.lower()
    cur_day = -1
    lv: WoodieLevels | None = None
    traded = False
    in_pos = False
    stop_level: float | None = None

    for i, bar in enumerate(bars):
        day = _utc_day_start_ms(bar.open_time_ms)
        is_last = i == n - 1 or _utc_day_start_ms(bars[i + 1].open_time_ms) != day

        if day != cur_day:
            cur_day = day
            traded = False
            prior = day - MS_DAY
            if prior in day_ohlc:
                ph, plo, pc = day_ohlc[prior]
                lv = levels_from_ohlc(ph, plo, pc)
            else:
                lv = None
            if in_pos:
                sells[i] = True
                in_pos = False
                stop_level = None

        if lv is None:
            continue

        if in_pos:
            stops[i] = stop_level
            if mode == "mode_a":
                hit_tgt = bar.close >= lv.p or bar.close >= lv.r1
                if hit_tgt or is_last:
                    sells[i] = True
                    in_pos = False
                    stop_level = None
            else:
                if bar.close <= lv.p or is_last:
                    sells[i] = True
                    in_pos = False
                    stop_level = None
            continue

        if params.one_trade_per_day and traded:
            continue

        if mode == "mode_a":
            if bar.low <= lv.s1 and bar.close >= lv.s1:
                buys[i] = True
                traded = True
                in_pos = True
                stop_level = lv.s2
                stops[i] = stop_level
        else:
            if bar.close > lv.r1:
                buys[i] = True
                traded = True
                in_pos = True
                stop_level = lv.p
                stops[i] = stop_level

    return buys, sells, stops
