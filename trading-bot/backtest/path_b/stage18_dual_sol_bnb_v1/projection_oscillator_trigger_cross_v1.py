"""projection-oscillator-trigger-cross — Projection Oscillator (Widner) x trigger cross.

LOCKED ENCODE ORDER #5 (BTC LEAD + ETH-PORTABLE PRIMARY).
Thesis:
  Stage17 DSS Bressert 0 BTC; raw Stoch burned; LinReg channel burned.
  Projection Oscillator (Mel Widner) is a slope-adjusted stochastic:
    PO = 100 * (close - lowerProj) / (upperProj - lowerProj)
    where bands project highs/lows along regression slopes over window len:
      slopeHigh, slopeLow from highs/lows
      upper = max(high[i-k] + k * slopeHigh)
      lower = min(low[i-k] - k * slopeLow)
    trig = ema(po, trigLen)
  Mode A = pure PO x trigger cross (no mandatory 20/80 first — density).
  Price-path / OHLC portable — intended ETH-after-BTC without volume-intensity III
  and without DSS/Stoch primary. Identical (len, trigLen) on all four coins.
  != raw Stoch K/D (burned).
  != DSS Bressert (stage17).
  != LinReg channel break (burned).
  != SMI (burned).

Formula:
  Over window len: OLS slopes of high/low;
  upper = max(high[i-k] + k * slopeHigh);
  lower = min(low[i-k] - k * slopeLow);
  po = 100 * (close - lower) / (upper - lower);
  trig = ema(po, trigLen).
  Prefer (14, 3). Guard upper != lower. Mode A PO x trig.

Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer):
  long: crossover(po, trig)
  exit: crossunder(po, trig)

Mode B (BNB quiet):
  cross while po < 30 / exit while po > 70 — only if Mode A over-whips; identical levels.

btc_smoke:
  BTC-LEAD CRITICAL: Kill len/trig inflate until n collapses;
  Kill Stoch/DSS/LinReg-channel substitute;
  Kill Mode B 20/80 forced while Mode A BTC healthy. Prefer Mode A (14,3), 1H+.

eth_smoke:
  BTC->ETH PRIMARY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill params retuned only on ETH; Kill Stoch/DSS/III labeled PO.
  Prefer identical (14,3); ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  Kill Stoch/DSS labeled PO; 15m len=5 spam; stage12-17 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different (len,trigLen); Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: Raw Stoch/DSS/SMI labeled PO; LinReg channel-break primary; III/volume; stage12-17.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, projection_oscillator

STRATEGY_ID = "projection-oscillator-trigger-cross"


@dataclass(frozen=True)
class ProjectionOscParams:
    mode: str = "mode_a"  # "mode_a" (po x trig) | "mode_b" (po < 30 entry, po > 70 exit)
    length: int = 14
    trig_len: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ProjectionOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {10, 14, 20}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{10, 14, 20}}"
    if params.trig_len not in {3, 5}:
        return False, f"btc_smoke: trig_len={params.trig_len} not in locked sweep {{3, 5}}"
    if params.length > 50:
        return False, f"btc_smoke: length={params.length} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: ProjectionOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PRIMARY CRITICAL)."""
    if params.length not in {10, 14, 20} or params.trig_len not in {3, 5}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ProjectionOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m length<=5 forbidden (spam)"
    if params.length not in {10, 14, 20} or params.trig_len not in {3, 5}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ProjectionOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.length not in {10, 14, 20} or params.trig_len not in {3, 5}:
        return False, "bnb_smoke: params not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ProjectionOscParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for projection-oscillator-trigger-cross."""
    params = params or ProjectionOscParams()
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
    po_vals, trig_vals = projection_oscillator(
        highs, lows, closes, length=params.length, trigger_length=params.trig_len
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(po_vals, trig_vals, i)
        cross_dn = crossunder(po_vals, trig_vals, i)

        if params.mode == "mode_b":
            # Mode B: require cross while po < 30, exit while po > 70
            val = po_vals[i]
            if val is None or val >= 30.0:
                cross_up = False
            if val is not None and val > 70.0:
                cross_dn = True

        if not in_pos:
            if cross_up:
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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
