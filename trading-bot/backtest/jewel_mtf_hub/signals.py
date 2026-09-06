"""M1–M4 long-only signal matrix (open-proxy edition).

Public-indicator names only. HTF state via no-lookahead join
(htf_close_time <= ltf_bar_time / LTF close).
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.jewel_mtf_hub.aggregate import aggregate_1d_to_2d
from backtest.jewel_mtf_hub.join import map_htf_onto_ltf
from backtest.jewel_mtf_hub.proxies import (
    compute_regime,
    compute_ribbon,
    compute_strength,
)


@dataclass(frozen=True)
class SignalFrame:
    variant: str
    bars: list[Bar]  # decision / fill TF
    buys: list[bool]
    sells: list[bool]
    notes: list[str]


def _gate_position(raw_long: list[bool], raw_exit: list[bool]) -> tuple[list[bool], list[bool]]:
    """Pyramiding 0: buy first raw_long while flat; sell on raw_exit while long."""
    n = len(raw_long)
    buys = [False] * n
    sells = [False] * n
    in_pos = False
    for i in range(n):
        if not in_pos and raw_long[i]:
            buys[i] = True
            in_pos = True
        elif in_pos and raw_exit[i]:
            sells[i] = True
            in_pos = False
    return buys, sells


def signals_m1(daily: list[Bar], *, allow_ema21_cross: bool = True) -> SignalFrame:
    """
    M1 TF=2D:
      entry = flip→green OR (green AND close cross above EMA21)  [EMA21 default ON]
      exit  = leave green
    """
    bars = aggregate_1d_to_2d(daily)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    reg = compute_regime(highs, lows, closes)
    rib = compute_ribbon(closes)
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        r = reg.regime[i]
        if r is None:
            continue
        green = r == 1
        entry = reg.flip_to_green[i]
        if allow_ema21_cross and green and rib.close_cross_ema_fast[i]:
            entry = True
        raw_long[i] = entry
        raw_exit[i] = reg.leave_green[i]
    buys, sells = _gate_position(raw_long, raw_exit)
    return SignalFrame(
        variant="M1",
        bars=bars,
        buys=buys,
        sells=sells,
        notes=[
            "M1: 2D ADX/DI regime; entry flip→green or (green + close×EMA21); exit leave green",
            f"allow_ema21_cross={allow_ema21_cross}",
        ],
    )


def signals_m2(daily: list[Bar], bars_4h: list[Bar]) -> SignalFrame:
    """
    M2 HTF=1D regime=+1, LTF=4H:
      entry = 4H flip→green while mapped 1D regime == +1
      exit  = mapped 1D leave green (prior +1 → not +1 on completed 1D)
    """
    d_h = [b.high for b in daily]
    d_l = [b.low for b in daily]
    d_c = [b.close for b in daily]
    d_reg = compute_regime(d_h, d_l, d_c)

    h_h = [b.high for b in bars_4h]
    h_l = [b.low for b in bars_4h]
    h_c = [b.close for b in bars_4h]
    h_reg = compute_regime(h_h, h_l, h_c)

    ltf_open = [b.open_time_ms for b in bars_4h]
    htf_open = [b.open_time_ms for b in daily]
    mapped_regime = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_values=d_reg.regime,
        htf_tf="1D",
    )
    mapped_leave = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_values=d_reg.leave_green,
        htf_tf="1D",
    )

    n = len(bars_4h)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        htf_r = mapped_regime[i]
        if htf_r is None:
            continue
        raw_long[i] = h_reg.flip_to_green[i] and htf_r == 1
        # Exit when completed 1D just left green — flag is True on that 1D bar;
        # once mapped, it stays True only for LTF bars that see that HTF bar.
        # leave_green is a pulse on the HTF bar; after map it is True on LTF
        # bars whose latest completed HTF is that leave bar. Also exit if
        # mapped regime is no longer +1 while we would otherwise hold — but
        # brief says exit = 1D leave green. Use mapped leave pulse OR mapped
        # regime != +1 after having been in (gated below via raw_exit while long).
        leave = bool(mapped_leave[i]) if mapped_leave[i] is not None else False
        # Persist exit while HTF not green: once 1D left green, regime≠+1
        if htf_r != 1:
            leave = True
        raw_exit[i] = leave

    buys, sells = _gate_position(raw_long, raw_exit)
    return SignalFrame(
        variant="M2",
        bars=bars_4h,
        buys=buys,
        sells=sells,
        notes=[
            "M2: 4H flip→green while joined 1D regime=+1; exit when joined 1D leaves green",
            "HTF join: htf_close <= ltf_close (no lookahead)",
        ],
    )


def signals_m3(daily: list[Bar]) -> SignalFrame:
    """
    M3 TF=2D:
      entry = RSI cross above 60
      exit  = RSI < 50
    """
    bars = aggregate_1d_to_2d(daily)
    closes = [b.close for b in bars]
    st = compute_strength(closes)
    buys, sells = _gate_position(st.enter_cross, st.exit_below)
    return SignalFrame(
        variant="M3",
        bars=bars,
        buys=buys,
        sells=sells,
        notes=["M3: 2D RSI(14); entry crossover(RSI,60); exit RSI<50"],
    )


def signals_m4(daily: list[Bar], bars_4h: list[Bar]) -> SignalFrame:
    """
    M4 HTF=1D RSI≥60, LTF=4H:
      entry = 4H RSI cross 60 while joined 1D RSI ≥ 60
      exit  = joined 1D RSI < 50
    """
    d_st = compute_strength([b.close for b in daily])
    h_st = compute_strength([b.close for b in bars_4h])

    ltf_open = [b.open_time_ms for b in bars_4h]
    htf_open = [b.open_time_ms for b in daily]
    mapped_rsi = map_htf_onto_ltf(
        ltf_open_ms=ltf_open,
        ltf_tf="4H",
        htf_open_ms=htf_open,
        htf_values=d_st.rsi,
        htf_tf="1D",
    )

    n = len(bars_4h)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        hr = mapped_rsi[i]
        if hr is None:
            continue
        raw_long[i] = h_st.enter_cross[i] and hr >= 60.0
        raw_exit[i] = hr < 50.0

    buys, sells = _gate_position(raw_long, raw_exit)
    return SignalFrame(
        variant="M4",
        bars=bars_4h,
        buys=buys,
        sells=sells,
        notes=[
            "M4: 4H RSI cross 60 while joined 1D RSI≥60; exit joined 1D RSI<50",
            "HTF join: htf_close <= ltf_close (no lookahead)",
        ],
    )


def build_all_signals(
    daily: list[Bar],
    bars_4h: list[Bar],
    *,
    m1_ema21: bool = True,
) -> dict[str, SignalFrame]:
    return {
        "M1": signals_m1(daily, allow_ema21_cross=m1_ema21),
        "M2": signals_m2(daily, bars_4h),
        "M3": signals_m3(daily),
        "M4": signals_m4(daily, bars_4h),
    }
