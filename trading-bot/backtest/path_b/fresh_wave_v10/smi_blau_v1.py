"""smi-blau-v1 — Blau SMI N=13 smooth 3/3 signal 3; OB/OS ±40. Forbidden Stoch/Connors/RSI."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import crossover, crossunder, smi_blau
from backtest.path_b.engine import apply_position_gate
from backtest.path_b.fresh_wave_v10 import (
    SMI_LENGTH,
    SMI_OB,
    SMI_OS,
    SMI_SIGNAL,
    SMI_SMOOTH1,
    SMI_SMOOTH2,
)

STRATEGY_ID = "smi-blau-v1"


@dataclass(frozen=True)
class SmiBlauParams:
    length: int = SMI_LENGTH
    smooth1: int = SMI_SMOOTH1
    smooth2: int = SMI_SMOOTH2
    signal_len: int = SMI_SIGNAL
    ob: float = SMI_OB
    os: float = SMI_OS
    # mode_a = SMI×signal cross OR cross above 0; mode_b = OS reclaim >−40
    mode: str = "mode_a"


def compute_raw(
    bars: list[Bar],
    params: SmiBlauParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Mode A: crossover(SMI, signal) OR crossover(SMI, 0).
    Mode B: was ≤ OS (−40) then cross > OS.
    Exit: crossunder(SMI, signal) OR crossunder(SMI, 0) OR SMI ≥ OB (+40).
    Forbidden: classic Stoch / Connors RSI / RSI grafts.
    """
    params = params or SmiBlauParams()
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    if n == 0:
        return raw_long, raw_exit

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    smi, sig = smi_blau(
        highs,
        lows,
        closes,
        length=params.length,
        smooth1=params.smooth1,
        smooth2=params.smooth2,
        signal_len=params.signal_len,
    )
    zero: list[float | None] = [0.0] * n
    os_line: list[float | None] = [params.os] * n
    mode = params.mode.lower()

    for i in range(n):
        if smi[i] is None:
            continue
        if mode == "mode_a":
            if crossover(smi, sig, i) or crossover(smi, zero, i):
                raw_long[i] = True
        else:
            # Mode B: reclaim from ≤ OS
            if crossover(smi, os_line, i):
                raw_long[i] = True
            elif i >= 1 and smi[i - 1] is not None:
                prev = smi[i - 1]
                assert prev is not None
                if prev <= params.os < smi[i]:  # type: ignore[operator]
                    raw_long[i] = True

        # Shared exits
        if crossunder(smi, sig, i) or crossunder(smi, zero, i):
            raw_exit[i] = True
        elif smi[i] is not None and smi[i] >= params.ob:  # type: ignore[operator]
            raw_exit[i] = True

    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: SmiBlauParams | None = None,
) -> tuple[list[bool], list[bool]]:
    return apply_position_gate(*compute_raw(bars, params))
