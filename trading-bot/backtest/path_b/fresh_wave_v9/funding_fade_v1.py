"""funding-fade-v1 — perp funding extreme fade (long-only Spot fills). Signal-only funding."""

from __future__ import annotations

import math
from dataclasses import dataclass

from backtest.data import Bar
from backtest.path_b.fresh_wave_v9.funding_data import FundingPrint

STRATEGY_ID = "funding-fade-v1"


@dataclass(frozen=True)
class FundingFadeParams:
    # mode_a = abs threshold ≤ −0.10%/8h; mode_b = z ≤ −τ (~30d window)
    mode: str = "mode_a"
    thr: float = 0.001  # 0.10% in Binance decimal units
    z_tau: float = 2.0
    z_window: int = 90  # ~30d × 3 settlements/day
    exit_settlements: int = 2
    # Mode A exit when rate recovers above this (toward neutral)
    mode_a_neutral: float = -0.0005
    # Mode B exit when |z| < this
    mode_b_neutral_abs_z: float = 0.5


def _rolling_z(rates: list[float], window: int) -> list[float | None]:
    n = len(rates)
    out: list[float | None] = [None] * n
    if window < 2:
        return out
    for i in range(n):
        if i + 1 < window:
            continue
        w = rates[i + 1 - window : i + 1]
        mean = sum(w) / window
        var = sum((x - mean) ** 2 for x in w) / window
        sd = math.sqrt(var)
        if sd < 1e-12:
            out[i] = 0.0
        else:
            out[i] = (rates[i] - mean) / sd
    return out


def compute_signals(
    bars: list[Bar],
    funding: list[FundingPrint],
    params: FundingFadeParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Long-only: fade extreme *negative* funding (crowded shorts → bounce).

    Mode A: funding ≤ −thr (−0.10%/8h). Mode B: z ≤ −τ vs ~30d window.
    Entry: first bar with open_time_ms >= funding print time (bar-close fill).
    Exit: toward neutral OR after `exit_settlements` funding prints.
    Skip short side (positive-funding fade). No RSI/BB/SMA200 grafts.
    """
    params = params or FundingFadeParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    if n == 0 or not funding:
        return buys, sells

    rates = [p.rate for p in funding]
    mode = params.mode.lower()
    zscores = _rolling_z(rates, params.z_window) if mode == "mode_b" else [None] * len(funding)

    # Map each funding print -> first bar index with open_time >= print time
    bar_for_print: list[int | None] = [None] * len(funding)
    bi = 0
    for fi, p in enumerate(funding):
        while bi < n and bars[bi].open_time_ms < p.time_ms:
            bi += 1
        if bi < n:
            bar_for_print[fi] = bi

    entry_at_bar: dict[int, int] = {}  # bar_idx -> funding_idx (first wins)
    for fi, p in enumerate(funding):
        bidx = bar_for_print[fi]
        if bidx is None or bidx in entry_at_bar:
            continue
        if mode == "mode_a":
            ok = p.rate <= -params.thr
        else:
            z = zscores[fi]
            ok = z is not None and z <= -params.z_tau
        if ok:
            entry_at_bar[bidx] = fi

    in_pos = False
    entry_fi = -1
    for i in range(n):
        if in_pos:
            settlements_after = 0
            last_rate = funding[entry_fi].rate
            last_z = zscores[entry_fi]
            for fi in range(entry_fi + 1, len(funding)):
                if funding[fi].time_ms > bars[i].close_time_ms:
                    break
                settlements_after += 1
                last_rate = funding[fi].rate
                last_z = zscores[fi]
            if mode == "mode_a":
                neutral = last_rate >= params.mode_a_neutral
            else:
                neutral = last_z is not None and abs(last_z) < params.mode_b_neutral_abs_z
            if settlements_after >= params.exit_settlements or neutral:
                sells[i] = True
                in_pos = False
                entry_fi = -1
            continue

        if i in entry_at_bar:
            buys[i] = True
            in_pos = True
            entry_fi = entry_at_bar[i]

    return buys, sells
