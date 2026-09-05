"""bb-squeeze-breakout-v1 — Daily BB squeeze breakout (Path B research)."""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, bollinger, sma
from backtest.path_b.engine import apply_position_gate

STRATEGY_ID = "bb-squeeze-breakout-v1"
INTERVAL = "1d"


@dataclass(frozen=True)
class BbSqueezeParams:
    bb_len: int = 20
    bb_mult: float = 2.0
    width_lookback: int = 100
    width_percentile: float = 20.0  # ≤ 20th pct of prior 100 widths
    vol_sma_len: int = 20
    atr_len: int = 14
    atr_stop_mult: float = 2.5


def _percentile_rank_threshold(values: list[float], pct: float) -> float:
    """Return the pct-th percentile of values (0-100), linear sorted."""
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    k = (pct / 100.0) * (len(s) - 1)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] + (s[c] - s[f]) * (k - f)


def compute_raw(
    bars: list[Bar],
    params: BbSqueezeParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """
    Squeeze: BB width(20,2) ≤ 20th pct of prior 100 bars (no lookahead).
    Entry: (prior bar in squeeze OR squeeze true) AND close > upper BB
           AND volume > SMA(volume, 20)
    Exit: close < middle BB OR close < entry − 2.5×ATR(14) (ATR frozen at entry;
          stop returned separately for engine freeze).
    """
    params = params or BbSqueezeParams()
    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]
    mid, upper, _lower, width = bollinger(closes, params.bb_len, params.bb_mult)
    vol_sma = sma(vols, params.vol_sma_len)
    atr_s = atr(highs, lows, closes, params.atr_len)
    n = len(bars)
    squeeze = [False] * n
    for i in range(n):
        if width[i] is None:
            continue
        # prior 100 widths strictly before i
        hist: list[float] = []
        for j in range(max(0, i - params.width_lookback), i):
            if width[j] is not None:
                hist.append(width[j])  # type: ignore[arg-type]
        if len(hist) < params.width_lookback:
            continue
        thr = _percentile_rank_threshold(hist, params.width_percentile)
        squeeze[i] = width[i] <= thr

    raw_long = [False] * n
    raw_exit = [False] * n
    entry_stop: list[float | None] = [None] * n
    for i in range(n):
        if upper[i] is None or mid[i] is None or vol_sma[i] is None:
            continue
        prior_sq = squeeze[i - 1] if i > 0 else False
        sq_ok = prior_sq or squeeze[i]
        vol_ok = vols[i] > vol_sma[i]
        raw_long[i] = sq_ok and closes[i] > upper[i] and vol_ok
        # signal exit on mid; ATR stop handled by engine via entry_stop
        raw_exit[i] = closes[i] < mid[i]
        if atr_s[i] is not None:
            entry_stop[i] = closes[i] - params.atr_stop_mult * atr_s[i]
    return raw_long, raw_exit, entry_stop


def compute_signals(
    bars: list[Bar],
    params: BbSqueezeParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    raw_long, raw_exit, entry_stop = compute_raw(bars, params)
    buys, sells = apply_position_gate(raw_long, raw_exit)
    # freeze stop at entry for engine
    stops: list[float | None] = [None] * len(bars)
    frozen: float | None = None
    in_pos = False
    for i in range(len(bars)):
        if buys[i]:
            in_pos = True
            frozen = entry_stop[i]
            stops[i] = frozen
        elif in_pos:
            stops[i] = frozen
            if sells[i]:
                in_pos = False
                frozen = None
    return buys, sells, stops
