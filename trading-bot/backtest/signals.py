"""ema-rsi-trend-v1.1 signal logic (mirrors Pine strategy)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.indicators import crossover, crossunder, ema, rsi


@dataclass(frozen=True)
class StrategyParams:
    fast_len: int = 20
    slow_len: int = 50
    rsi_len: int = 14
    rsi_buy_min: float = 50.0
    rsi_sell_level: float = 40.0
    cooldown_bars: int = 6


@dataclass
class SignalFrame:
    """Precomputed indicators + per-bar buy/sell flags (sell ignores position)."""

    ema_fast: list[float | None]
    ema_slow: list[float | None]
    rsi: list[float | None]
    ema_cross_up: list[bool]
    ema_cross_down: list[bool]
    rsi_cross_down: list[bool]
    raw_long: list[bool]  # crossover + RSI + close>=slow (no cooldown)
    raw_exit: list[bool]  # crossunder or RSI fade (no position gate)


def compute_indicators(closes: list[float], params: StrategyParams) -> SignalFrame:
    ef = ema(closes, params.fast_len)
    es = ema(closes, params.slow_len)
    r = rsi(closes, params.rsi_len)
    n = len(closes)
    ema_up = [False] * n
    ema_dn = [False] * n
    rsi_dn = [False] * n
    raw_long = [False] * n
    raw_exit = [False] * n

    # Build float|None list for RSI level crossunder
    sell_series: list[float | None] = [float(params.rsi_sell_level)] * n

    for i in range(n):
        ema_up[i] = crossover(ef, es, i)
        ema_dn[i] = crossunder(ef, es, i)
        rsi_dn[i] = crossunder(r, sell_series, i)
        ef_i, es_i, r_i = ef[i], es[i], r[i]
        if ef_i is None or es_i is None or r_i is None:
            continue
        raw_long[i] = (
            ema_up[i]
            and r_i >= params.rsi_buy_min
            and closes[i] >= es_i
        )
        raw_exit[i] = ema_dn[i] or rsi_dn[i]

    return SignalFrame(
        ema_fast=ef,
        ema_slow=es,
        rsi=r,
        ema_cross_up=ema_up,
        ema_cross_down=ema_dn,
        rsi_cross_down=rsi_dn,
        raw_long=raw_long,
        raw_exit=raw_exit,
    )


def apply_position_and_cooldown(
    frame: SignalFrame,
    params: StrategyParams,
) -> tuple[list[bool], list[bool]]:
    """
    Apply long-only position gate and post-exit cooldown.

    Returns (buy_signals, sell_signals) aligned to bars.
    Mirrors Pine: cooldown counts bars after exit before re-entry;
    sell only when in position; pyramiding=0.
    """
    n = len(frame.raw_long)
    buys = [False] * n
    sells = [False] * n
    in_pos = False
    last_exit_bar: int | None = None

    for i in range(n):
        cooldown_ok = (
            params.cooldown_bars == 0
            or last_exit_bar is None
            or (i - last_exit_bar) >= params.cooldown_bars
        )
        if not in_pos and frame.raw_long[i] and cooldown_ok:
            buys[i] = True
            in_pos = True
        elif in_pos and frame.raw_exit[i]:
            sells[i] = True
            in_pos = False
            last_exit_bar = i

    return buys, sells
