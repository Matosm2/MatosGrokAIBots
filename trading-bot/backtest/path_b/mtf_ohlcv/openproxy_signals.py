"""Open-proxy M1–M4 signals for arbitrary LTF (owned-tf-sweep-v1).

M1/M3: regime/strength on the decision TF bars.
M2/M4: LTF = decision TF; HTF = frozen M2_M4_HTF[ltf] via #12 no-lookahead join.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.jewel_mtf_hub.join import map_htf_onto_ltf
from backtest.jewel_mtf_hub.proxies import compute_regime, compute_ribbon, compute_strength
from backtest.path_b.mtf_ohlcv.timeframes import htf_for, normalize_tf


@dataclass(frozen=True)
class SweepSignalFrame:
    variant: str
    ltf: str
    htf: str | None
    bars: list[Bar]
    buys: list[bool]
    sells: list[bool]
    notes: list[str]


def _gate_position(raw_long: list[bool], raw_exit: list[bool]) -> tuple[list[bool], list[bool]]:
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


def signals_m1(bars: list[Bar], ltf: str, *, allow_ema21_cross: bool = True) -> SweepSignalFrame:
    ltf = normalize_tf(ltf)
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
    return SweepSignalFrame(
        variant="openproxy-M1",
        ltf=ltf,
        htf=None,
        bars=bars,
        buys=buys,
        sells=sells,
        notes=[
            f"M1 on {ltf}: flip→green or (green + close×EMA21); exit leave green",
            "regime ADX≥20 +DI (frozen #13)",
        ],
    )


def signals_m3(bars: list[Bar], ltf: str) -> SweepSignalFrame:
    ltf = normalize_tf(ltf)
    st = compute_strength([b.close for b in bars])
    buys, sells = _gate_position(st.enter_cross, st.exit_below)
    return SweepSignalFrame(
        variant="openproxy-M3",
        ltf=ltf,
        htf=None,
        bars=bars,
        buys=buys,
        sells=sells,
        notes=[f"M3 on {ltf}: RSI cross 60 / exit RSI<50 (frozen #13)"],
    )


def signals_m2(ltf_bars: list[Bar], htf_bars: list[Bar], ltf: str) -> SweepSignalFrame:
    ltf = normalize_tf(ltf)
    htf = htf_for(ltf)
    d_reg = compute_regime(
        [b.high for b in htf_bars],
        [b.low for b in htf_bars],
        [b.close for b in htf_bars],
    )
    h_reg = compute_regime(
        [b.high for b in ltf_bars],
        [b.low for b in ltf_bars],
        [b.close for b in ltf_bars],
    )
    mapped_regime = map_htf_onto_ltf(
        ltf_open_ms=[b.open_time_ms for b in ltf_bars],
        ltf_tf=ltf,
        htf_open_ms=[b.open_time_ms for b in htf_bars],
        htf_values=d_reg.regime,
        htf_tf=htf,
    )
    mapped_leave = map_htf_onto_ltf(
        ltf_open_ms=[b.open_time_ms for b in ltf_bars],
        ltf_tf=ltf,
        htf_open_ms=[b.open_time_ms for b in htf_bars],
        htf_values=d_reg.leave_green,
        htf_tf=htf,
    )
    n = len(ltf_bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        htf_r = mapped_regime[i]
        if htf_r is None:
            continue
        raw_long[i] = h_reg.flip_to_green[i] and htf_r == 1
        leave = bool(mapped_leave[i]) if mapped_leave[i] is not None else False
        if htf_r != 1:
            leave = True
        raw_exit[i] = leave
    buys, sells = _gate_position(raw_long, raw_exit)
    return SweepSignalFrame(
        variant="openproxy-M2",
        ltf=ltf,
        htf=htf,
        bars=ltf_bars,
        buys=buys,
        sells=sells,
        notes=[
            f"M2: {ltf} flip→green while joined {htf} regime=+1; exit {htf} leaves green",
            "HTF map frozen owned-tf-sweep-v1; join #12 no lookahead",
        ],
    )


def signals_m4(ltf_bars: list[Bar], htf_bars: list[Bar], ltf: str) -> SweepSignalFrame:
    ltf = normalize_tf(ltf)
    htf = htf_for(ltf)
    d_st = compute_strength([b.close for b in htf_bars])
    h_st = compute_strength([b.close for b in ltf_bars])
    mapped_rsi = map_htf_onto_ltf(
        ltf_open_ms=[b.open_time_ms for b in ltf_bars],
        ltf_tf=ltf,
        htf_open_ms=[b.open_time_ms for b in htf_bars],
        htf_values=d_st.rsi,
        htf_tf=htf,
    )
    n = len(ltf_bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        hr = mapped_rsi[i]
        if hr is None:
            continue
        raw_long[i] = h_st.enter_cross[i] and hr >= 60.0
        raw_exit[i] = hr < 50.0
    buys, sells = _gate_position(raw_long, raw_exit)
    return SweepSignalFrame(
        variant="openproxy-M4",
        ltf=ltf,
        htf=htf,
        bars=ltf_bars,
        buys=buys,
        sells=sells,
        notes=[
            f"M4: {ltf} RSI cross 60 while joined {htf} RSI≥60; exit joined {htf} RSI<50",
            "HTF map frozen owned-tf-sweep-v1; join #12 no lookahead",
        ],
    )
