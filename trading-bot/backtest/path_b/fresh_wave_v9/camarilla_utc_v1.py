"""camarilla-utc-v1 — prior UTC-day Camarilla L3 fade / H4 break. ≠ Session ORB."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar

STRATEGY_ID = "camarilla-utc-v1"

MS_DAY = 86_400_000


@dataclass(frozen=True)
class CamarillaParams:
    adj_mult: float = 1.1
    # mode_a = fade L3 (primary); mode_b = close > H4 breakout
    mode: str = "mode_a"
    one_trade_per_day: bool = True


@dataclass(frozen=True)
class CamarillaLevels:
    h4: float
    h3: float
    l3: float
    l4: float
    mid: float  # prior close C


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def levels_from_ohlc(h: float, lo: float, c: float, adj_mult: float = 1.1) -> CamarillaLevels:
    """Scott / LiteFinance family: adj=(H−L)×1.1; H3/H4/L3/L4 from C."""
    adj = (h - lo) * adj_mult
    return CamarillaLevels(
        h4=c + adj / 2.0,
        h3=c + adj / 4.0,
        l3=c - adj / 4.0,
        l4=c - adj / 2.0,
        mid=c,
    )


def compute_signals(
    bars: list[Bar],
    params: CamarillaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    Prior UTC calendar day H/L/C → Camarilla levels (freeze at day open).

    Mode A (primary): fade L3 long — touch/reclaim (low≤L3 and close≥L3);
      SL beyond L4 (stop=L4); exit toward mid (C) or H3.
    Mode B: close > H4; exit close < H3 or last bar of UTC day.
    One-trade/day default. ≠ Session ORB first-N-min box; ≠ Donchian.
    """
    params = params or CamarillaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    # Build prior-day OHLC map: day_start -> (H, L, C) of that UTC day
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
    lv: CamarillaLevels | None = None
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
                lv = levels_from_ohlc(ph, plo, pc, params.adj_mult)
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
                hit_tgt = bar.close >= lv.mid or bar.close >= lv.h3
                if hit_tgt or is_last:
                    sells[i] = True
                    in_pos = False
                    stop_level = None
            else:  # mode_b
                if bar.close < lv.h3 or is_last:
                    sells[i] = True
                    in_pos = False
                    stop_level = None
            continue

        if params.one_trade_per_day and traded:
            continue

        if mode == "mode_a":
            # Fade L3: pierce then reclaim on same bar (low ≤ L3, close ≥ L3)
            if bar.low <= lv.l3 and bar.close >= lv.l3:
                buys[i] = True
                traded = True
                in_pos = True
                stop_level = lv.l4
                stops[i] = stop_level
        else:
            if bar.close > lv.h4:
                buys[i] = True
                traded = True
                in_pos = True
                stop_level = lv.h3  # back inside band
                stops[i] = stop_level

    return buys, sells, stops
