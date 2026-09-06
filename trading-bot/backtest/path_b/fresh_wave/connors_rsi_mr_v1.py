"""connors-rsi-mr-v1 — Connors RSI mean-reversion (classic CRSI(3,2,100))."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import connors_rsi
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "connors-rsi-mr-v1"


@dataclass(frozen=True)
class ConnorsRsiParams:
    """Classic Connors RSI CRSI(3,2,100); entry <10; exit >90 or hold≥5 bars."""

    rsi_len: int = 3
    streak_rsi_len: int = 2
    percent_rank_len: int = 100
    entry_below: float = 10.0
    exit_above: float = 90.0
    max_hold_bars: int = 5


def compute_raw(
    bars: list[Bar],
    params: ConnorsRsiParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Entry (flat): CRSI < 10.
    Exit: CRSI > 90 OR bars held ≥ 5 (enforced in compute_signals via hold clock).

    Raw exit only encodes CRSI > 90; max-hold is applied in compute_signals.
    """
    params = params or ConnorsRsiParams()
    closes = [b.close for b in bars]
    crsi = connors_rsi(
        closes, params.rsi_len, params.streak_rsi_len, params.percent_rank_len
    )
    n = len(bars)
    raw_long = [False] * n
    raw_exit = [False] * n
    for i in range(n):
        c = crsi[i]
        if c is None:
            continue
        raw_long[i] = c < params.entry_below
        raw_exit[i] = c > params.exit_above
    return raw_long, raw_exit


def compute_signals(
    bars: list[Bar],
    params: ConnorsRsiParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """Position-gated signals with max-hold exit (bars since entry ≥ max_hold_bars)."""
    params = params or ConnorsRsiParams()
    raw_long, raw_exit = compute_raw(bars, params)
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    in_pos = False
    entry_i = -1
    for i in range(n):
        if not in_pos and raw_long[i]:
            buys[i] = True
            in_pos = True
            entry_i = i
        elif in_pos:
            held = i - entry_i
            if raw_exit[i] or held >= params.max_hold_bars:
                sells[i] = True
                in_pos = False
                entry_i = -1
    return buys, sells
