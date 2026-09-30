"""donovan-range-filter-flip-v1 — DonovanWall Range Filter trend flip.

LOCKED ENCODE ORDER #4 (BTC-CLEARING PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage12 wiped MA/smoother duals and FIR-lag (0 BTC). DonovanWall Range Filter gates price
  against a smoothed absolute-change range (ratchet): filter only moves when price exceeds prior
  filter +- range — != SuperTrend (ATR*mult mid), != Chandelier (ATR from extreme), != Keltner,
  != MA dual-cross, != EDCF FIR.
  Mode A locks filter direction flip (bull when filter rises) for responsive majors structure —
  BTC-clearing trail events without multipole damp.
  hl2/close + identical (period, mult) on SOL+BNB.

Formula:
  src = close (or hl2)
  av_chg = ema(ema(abs(src - src[1]), period), 2*period - 1)
  rng = av_chg * mult
  ratchet filt:
    if src - rng > filt[1]: filt = src - rng
    else if src + rng < filt[1]: filt = src + rng
    else filt = filt[1]
  dir = filt > filt[1] ? 1 : filt < filt[1] ? -1 : dir[1]
  Prefer period=20, mult=1.618.

Mode A (BTC-PRIMARY):
  long when dir flips to +1 (dir == 1 and dir[1] != 1)
  exit when dir flips to -1 (dir == -1 and dir[1] != -1) or ATR stop.

Mode B (BNB quiet):
  long when dir flips to +1 and src > filt
  exit when dir flips to -1 or src < filt or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if period/mult inflated until BTC flips collapse;
  Kill if ATR-SuperTrend formula substituted; Kill if dual-MA/stage12 damp grafted.
  Prefer Mode A (20, 1.618), 1H+.

sol_smoke:
  Kill if SuperTrend/Chandelier labeled RF; 15m period=5 spam; ER/AO/PGO/stage12 graft.
  Retention check: after ETH, SOL flip n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+SOL: different (period,mult) than SOL; Mode B shorts ungated; no ATR; per-coin retune.
  Prefer identical params; long-only; ATR exit.

Forbidden: SuperTrend/Chandelier/Keltner/SSL labeled RF; ATR-band substitute; stage12 smoother duals; ER-gate.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, donovan_range_filter

STRATEGY_ID = "donovan-range-filter-flip-v1"


@dataclass(frozen=True)
class DonovanRangeFilterParams:
    mode: str = "mode_a"  # "mode_a" (dir flip +1) | "mode_b" (dir flip +1 and src > filt)
    period: int = 20
    mult: float = 1.618
    use_hl2: bool = False
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: DonovanRangeFilterParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period > 40 or params.mult > 3.0:
        return False, "btc_smoke: period/mult inflated (collapses BTC flips)"
    if params.period not in {14, 20, 28}:
        return False, f"btc_smoke: period={params.period} not in locked set {{14, 20, 28}}"
    return True, "PASS"


def validate_sol_smoke(params: DonovanRangeFilterParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period <= 5:
        return False, "sol_smoke: 15m period<=5 forbidden (spam)"
    if params.period not in {14, 20, 28}:
        return False, f"sol_smoke: period={params.period} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DonovanRangeFilterParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+SOL)."""
    if params.period <= 0 or params.mult <= 0:
        return False, "bnb_smoke: period and mult must be > 0"
    if params.period > 50:
        return False, "bnb_smoke: period too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DonovanRangeFilterParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for donovan-range-filter-flip-v1."""
    params = params or DonovanRangeFilterParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    filt, dirs = donovan_range_filter(
        highs,
        lows,
        closes,
        period=params.period,
        mult=params.mult,
        use_hl2=params.use_hl2,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        curr_dir = dirs[i]
        prev_dir = dirs[i - 1]
        curr_filt = filt[i]

        dir_flip_up = (curr_dir == 1 and prev_dir != 1)
        dir_flip_dn = (curr_dir == -1 and prev_dir != -1)

        src_val = (highs[i] + lows[i]) / 2.0 if params.use_hl2 else c

        if not in_pos:
            entry_cond = dir_flip_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_filt is not None and src_val > curr_filt)

            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * float(atr_vals[i])
        else:
            highest_since_entry = max(highest_since_entry, h)
            stop_hit = False

            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                new_stop = highest_since_entry - params.atr_trail_mult * float(atr_vals[i])
                prev_stop = stops[i - 1]
                if prev_stop is not None and new_stop < prev_stop:
                    new_stop = prev_stop
                stops[i] = new_stop
                if lows[i] <= new_stop:
                    stop_hit = True

            exit_cond = dir_flip_dn
            if params.mode == "mode_b":
                exit_cond = exit_cond or (curr_filt is not None and src_val < curr_filt)

            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
