"""p4h-hl-accept-break-v1 — Prior UTC 4-Hour High/Low Closed-Bar Accept-Break.

LOCKED ENCODE ORDER #4 (BNB-survival-FIRST).
Thesis:
  4H extremes sit between stage3 PHH (very dense/hour noise) and stage1 PDH (sparse/wipe).
  Enough touches for SOL 1H-4H n, fewer thin-hour false tags than PHH.
  Optional RVOL on the break bar hardens BNB after level-family adjacency risk.

Levels:
  Track running high/low within current UTC 4H bucket (00:00, 04:00, 08:00, 12:00, 16:00, 20:00).
  On UTC 4H boundary (time_ms // 14_400_000 advances), freeze prior bucket -> P4H_High / P4H_Low.
  NO request.security; session-reset var trackers on execution timeframe.

Mode A (accept-break):
  Long: close > P4H_High after prior close <= P4H_High (+ RVOL gate if enabled).
  Short / Flat: close < P4H_Low.

Mode B (break + retest):
  After Mode A break, pullback tag within 0.2% of level then closed-bar hold above level.

RVOL:
  volume > k * ta.sma(volume, 20) on break bar (ON by default for BNB smoke, k >= 1.5).

Exit:
  Close back inside prior-4H range (close < P4H_High), or opposite level, or ATR trail.

BNB Smoke Rules:
  Kill if: (1) RVOL off on BNB; (2) wick-accept (must be close beyond); (3) 15m without k >= 1.5;
  (4) tiny range skip ((P4H_High - P4H_Low)/close < 0.002).
  Prefer 1H exec, k=1.5, Mode A first, one-trade-per-level.

Distinct from: PDH/PDL, PWH/PWL, PHH/PHL, Session ORB, Donchian.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, rvol

STRATEGY_ID = "p4h-hl-accept-break-v1"
FOUR_HOURS_MS = 14_400_000  # 4 * 3600 * 1000


@dataclass(frozen=True)
class P4HParams:
    mode: str = "mode_a"  # "mode_a" (accept-break) | "mode_b" (break + retest)
    rvol_k: float = 1.5  # RVOL multiplier (0.0 = off)
    vol_len: int = 20
    one_trade_per_bucket: bool = True
    min_range_pct: float = 0.002  # min (P4H_High - P4H_Low) / close
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: P4HParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for p4h-hl-accept-break-v1."""
    params = params or P4HParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]

    rvol_vals = rvol(vols, params.vol_len)
    atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    # Track 4H buckets via UTC wall-clock timestamp
    current_bucket_id = -1
    curr_high = -1.0
    curr_low = float("inf")
    p4h_high: float | None = None
    p4h_low: float | None = None

    traded_bucket_id = -1
    mode_b_broken = False  # for Mode B retest tracking

    for i, bar in enumerate(bars):
        c = closes[i]
        h = highs[i]
        l = lows[i]
        v = vols[i]
        bucket_id = bar.open_time_ms // FOUR_HOURS_MS

        if bucket_id != current_bucket_id:
            # 4H boundary crossed: freeze prior bucket
            if current_bucket_id != -1 and curr_high > 0 and curr_low < float("inf"):
                p4h_high = curr_high
                p4h_low = curr_low
                mode_b_broken = False
            current_bucket_id = bucket_id
            curr_high = h
            curr_low = l
        else:
            curr_high = max(curr_high, h)
            curr_low = min(curr_low, l)

        if p4h_high is None or p4h_low is None or v == 0:
            if in_pos:
                stops[i] = stop_level
            continue

        # Min range check
        range_pct = (p4h_high - p4h_low) / c if c > 0 else 0.0
        range_ok = range_pct >= params.min_range_pct

        # RVOL check
        rv = rvol_vals[i]
        rvol_ok = (rv is not None and rv >= params.rvol_k) if params.rvol_k > 0 else True

        bucket_allowed = (not params.one_trade_per_bucket) or (bucket_id != traded_bucket_id)

        prev_c = closes[i - 1] if i > 0 else c
        entry_sig = False
        exit_sig = False

        if params.mode == "mode_a":
            # Closed bar beyond prior 4H high
            if prev_c <= p4h_high and c > p4h_high and rvol_ok and range_ok and bucket_allowed:
                entry_sig = True
            elif in_pos and (c < p4h_high or c < p4h_low):
                exit_sig = True
        else:  # mode_b: break + retest
            if prev_c <= p4h_high and c > p4h_high:
                mode_b_broken = True
            # Retest: price pulled back to tag within 0.2% of p4h_high and closed above
            retest_tagged = l <= p4h_high * 1.002
            if mode_b_broken and retest_tagged and c > p4h_high and rvol_ok and range_ok and bucket_allowed:
                entry_sig = True
                mode_b_broken = False
            elif in_pos and (c < p4h_high or c < p4h_low):
                exit_sig = True

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, c)

            hit_exit = False
            if exit_sig:
                hit_exit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if c < stop_level:
                    hit_exit = True

            if hit_exit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if entry_sig:
            buys[i] = True
            in_pos = True
            traded_bucket_id = bucket_id
            highest_since_entry = c
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = c - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level

    return buys, sells, stops
