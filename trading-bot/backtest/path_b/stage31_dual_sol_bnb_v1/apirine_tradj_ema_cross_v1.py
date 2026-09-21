"""apirine-tradj-ema-cross — Vitali Apirine True Range Adjusted EMA x EMA cross.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage30 Apirine MAB thin-n band-break wipe; need volatility-adjusted EMAxEMA impulse
  denser than band-break n=8, != VIDYA/KAMA, != Track-B ATR corridor.
  TRAdj EMA (Vitali Apirine TASC Jan 2023; Traders Tips / PineCodersTASC):
    TR = TrueRange(High, Low, Close)
    TRAdj = (TR - LLV(TR, Pds)) / (HHV(TR, Pds) - LLV(TR, Pds))
    Rate = (2 / (Periods + 1)) * (1 + TRAdj * Mltp)
    TRAdjEMA = TRAdjEMA[1] + Rate * (Close - TRAdjEMA[1])
  Mode A:
    long crossover(tradjEma, ema(close, Periods))
    exit crossunder(tradjEma, ema(close, Periods))
  Mode B:
    require close > ema(close, Periods) gate on entry —
    only if Mode A over-whips; identical across all four.
  Prefer (Periods=20, Pds=20, Mltp=5) Mode A.
  != Apirine MAB / != VIDYA / != KAMA / != BB / != Track-B.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill Periods inflated until BTC n collapses; Kill MAB/BB/VIDYA/KAMA/Track-B substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A (20, 20, 5), 1H+.

eth_smoke:
  Kill params retuned only on ETH; Kill MAB labeled TRAdj. Prefer identical params.

sol_smoke:
  Kill params retuned only on SOL; 15m spam; stage1-30 grafts.

bnb_smoke:
  Kill params retuned only on BNB; Mode B only on BNB; ungated shorts.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import apirine_tradj_ema, atr, crossover, crossunder

STRATEGY_ID = "apirine-tradj-ema-cross"


@dataclass(frozen=True)
class ApirineTradjEmaParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    periods: int = 20             # 10, 20, 40
    pds: int = 20                 # 10, 20, 40
    mltp: float = 5.0             # 5.0, 8.0, 10.0
    close_gate: bool = False      # Mode B close > emaRef
    atr_trail_mult: float = 0.0   # 0.0 (off)
    atr_len: int = 14


def validate_btc_smoke(params: ApirineTradjEmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.periods not in {10, 20, 40}:
        return False, f"btc_smoke: periods={params.periods} not in {{10, 20, 40}}"
    if params.pds not in {10, 20, 40}:
        return False, f"btc_smoke: pds={params.pds} not in {{10, 20, 40}}"
    if params.mltp not in {5.0, 8.0, 10.0}:
        return False, f"btc_smoke: mltp={params.mltp} not in {{5.0, 8.0, 10.0}}"
    return True, "PASS"


def validate_eth_smoke(params: ApirineTradjEmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation."""
    if params.periods not in {10, 20, 40} or params.pds not in {10, 20, 40} or params.mltp not in {5.0, 8.0, 10.0}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ApirineTradjEmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.periods not in {10, 20, 40} or params.pds not in {10, 20, 40} or params.mltp not in {5.0, 8.0, 10.0}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ApirineTradjEmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.periods not in {10, 20, 40} or params.pds not in {10, 20, 40} or params.mltp not in {5.0, 8.0, 10.0}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ApirineTradjEmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for apirine-tradj-ema-cross."""
    params = params or ApirineTradjEmaParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    tradj_ema_vals, ema_ref_vals = apirine_tradj_ema(
        highs=highs,
        lows=lows,
        closes=closes,
        periods=params.periods,
        pds=params.pds,
        mltp=params.mltp,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(tradj_ema_vals, ema_ref_vals, i)
        cross_dn = crossunder(tradj_ema_vals, ema_ref_vals, i)

        c_val = closes[i]
        ref_val = ema_ref_vals[i]
        close_above = (ref_val is not None and c_val > ref_val)

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and (close_above or not params.close_gate)
            exit_cond = cross_dn
        else:
            entry_cond = cross_up
            exit_cond = cross_dn

        atr_stop_hit = False
        if in_pos and params.atr_trail_mult > 0.0:
            if highs[i] > highest_since_entry:
                highest_since_entry = highs[i]
            atr_v = atr_vals[i]
            if atr_v is not None:
                stop_level = highest_since_entry - params.atr_trail_mult * atr_v
                stops[i] = stop_level
                if closes[i] < stop_level:
                    atr_stop_hit = True

        if not in_pos:
            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = highs[i]
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = highest_since_entry - params.atr_trail_mult * atr_vals[i]
        else:
            if exit_cond or atr_stop_hit:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0

    return buys, sells, stops
