"""vwap-utc-sigma-v1 — UTC 00:00 session VWAP ±σ MR. ≠ Bollinger."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import session_vwap_bands

STRATEGY_ID = "vwap-utc-sigma-v1"

MS_DAY = 86_400_000


@dataclass(frozen=True)
class VwapUtcSigmaParams:
    # mode_a = tag −2σ then reclaim; mode_b = close reclaim above VWAP
    mode: str = "mode_a"
    one_trade_per_day: bool = True


def _utc_day_start_ms(open_time_ms: int) -> int:
    return (open_time_ms // MS_DAY) * MS_DAY


def compute_signals(
    bars: list[Bar],
    params: VwapUtcSigmaParams | None = None,
) -> tuple[list[bool], list[bool]]:
    """
    Session VWAP resets at UTC midnight. σ from volume-weighted variance of TP.

    Mode A: tag −2σ (low ≤ lower) then reclaim (close > lower) toward VWAP.
    Mode B: close reclaim above VWAP (crossover close vs VWAP from below).
    Exit: VWAP touch (close ≥ VWAP for A; close ≤ VWAP for B) or EOD UTC flat.
    ≠ Bollinger (SMA±σ of close); no RSI/SMA200 grafts.
    """
    params = params or VwapUtcSigmaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    if n == 0:
        return buys, sells

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]
    day_ids = [_utc_day_start_ms(b.open_time_ms) for b in bars]
    vwap, lo2, _hi2 = session_vwap_bands(highs, lows, closes, volumes, day_ids)

    mode = params.mode.lower()
    cur_day = -1
    traded = False
    in_pos = False
    tagged = False  # Mode A: saw a −2σ tag this session (or same-bar)

    for i, bar in enumerate(bars):
        day = day_ids[i]
        is_last = i == n - 1 or day_ids[i + 1] != day

        if day != cur_day:
            cur_day = day
            traded = False
            tagged = False
            if in_pos:
                sells[i] = True
                in_pos = False

        vw = vwap[i]
        lower = lo2[i]
        if vw is None or lower is None:
            continue

        if in_pos:
            if mode == "mode_a":
                # VWAP touch = mean-reversion target
                if bar.close >= vw or is_last:
                    sells[i] = True
                    in_pos = False
            else:
                if bar.close <= vw or is_last:
                    sells[i] = True
                    in_pos = False
            continue

        if params.one_trade_per_day and traded:
            continue

        if mode == "mode_a":
            # Same-bar tag+reclaim, or multi-bar: tag then later reclaim
            if bar.low <= lower:
                tagged = True
            if tagged and bar.close > lower:
                buys[i] = True
                traded = True
                in_pos = True
                tagged = False
        else:
            # Mode B: reclaim above VWAP (was at/below, now above)
            if i < 1 or vwap[i - 1] is None:
                continue
            prev_c = bars[i - 1].close
            prev_vw = vwap[i - 1]
            assert prev_vw is not None
            if prev_c <= prev_vw and bar.close > vw:
                buys[i] = True
                traded = True
                in_pos = True

    return buys, sells
