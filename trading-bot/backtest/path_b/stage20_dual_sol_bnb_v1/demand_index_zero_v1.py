"""demand-index-zero — James Sibbet Demand Index zero-cross.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage19 HHLL cleared 3-coin then BNB quiet wipe; STARC/VZO/NVI/FDI 0 BTC.
  Demand Index (James Sibbet) builds Buy Power vs Sell Power from weighted price
  (H+L+2C), volume/avg-volume, and range-scaled exponential:
    Mode A = DI x 0 cross.
  Intended BNB-survival pressure polarity (not structure flips) with identical
  (nBS, nSmooth) on all four.
  Lock Sierra Chart published form.
  != VZO / != Bostian III / != CMF / != OBV / != PZO.

Mode A (prefer (10,10)):
  long: crossover(di, 0)
  exit: crossunder(di, 0)

Mode B (BNB quiet / chatter):
  require DI hold above +band / below -band for N bars after cross — only if
  Mode A over-whips; identical params.

btc_smoke:
  Kill nBS/nSmooth inflate until n collapses;
  Kill Mode A BTC 0 / chop; Kill VZO/III/CMF labeled DI.
  Prefer Mode A (10,10), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x;
  Kill params retuned only on ETH; Kill III/VZO labeled DI.
  Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x;
  15m nBS=3 spam; stage12-19 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL: Kill 3-coin clear then BNB quiet wipe;
  Kill nBS/nSmooth retuned only on BNB; Kill Mode B only on BNB;
  structure/BOS graft; ungated shorts; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: VZO/III/CMF/OBV/PZO labeled DI; mix PureBytes+Sierra mid-encode;
HHLL/STARC; request.security; stage12-19 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, demand_index

STRATEGY_ID = "demand-index-zero"


@dataclass(frozen=True)
class DemandIndexParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    n_bs: int = 10
    n_smooth: int = 10
    hold_bars: int = 0
    band_level: float = 0.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: DemandIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n_bs not in {8, 10, 14}:
        return False, f"btc_smoke: n_bs={params.n_bs} not in locked sweep {{8, 10, 14}}"
    if params.n_smooth not in {5, 10, 14}:
        return False, f"btc_smoke: n_smooth={params.n_smooth} not in locked sweep {{5, 10, 14}}"
    if params.n_smooth > 25:
        return False, f"btc_smoke: n_smooth={params.n_smooth} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: DemandIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.n_bs not in {8, 10, 14} or params.n_smooth not in {5, 10, 14}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: DemandIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.n_bs <= 3:
        return False, "sol_smoke: 15m n_bs<=3 forbidden (spam)"
    if params.n_bs not in {8, 10, 14} or params.n_smooth not in {5, 10, 14}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DemandIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.n_bs not in {8, 10, 14} or params.n_smooth not in {5, 10, 14}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DemandIndexParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for demand-index-zero."""
    params = params or DemandIndexParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    di_vals = demand_index(highs, lows, closes, volumes, n_bs=params.n_bs, n_smooth=params.n_smooth)
    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    bars_since_cross = 999

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(di_vals, zero_line, i)
        cross_dn = crossunder(di_vals, zero_line, i)

        if cross_up:
            bars_since_cross = 0
        else:
            bars_since_cross += 1

        entry_trigger = False
        if params.mode == "mode_b" and params.hold_bars > 0:
            val = di_vals[i]
            if bars_since_cross == params.hold_bars and val is not None and val > params.band_level:
                entry_trigger = True
        else:
            entry_trigger = cross_up

        if not in_pos:
            if entry_trigger:
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
