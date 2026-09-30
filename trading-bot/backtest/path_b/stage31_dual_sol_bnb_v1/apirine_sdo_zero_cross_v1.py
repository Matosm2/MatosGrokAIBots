"""apirine-sdo-zero-cross — Vitali Apirine Stochastic Distance Oscillator zero-cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage30 Apirine MAB BTC 1.520x thin-n=8 -> ETH wipe; need published dense Mode-A oscillator
  participating often enough on BTC (n >= 40) without band-break thin-n.
  SDO (Vitali Apirine TASC Jun 2023; Traders Tips / PineCodersTASC):
    Dist = |Close - Close[n]|
    %D = (Dist - LLV(Dist, LB)) / (HHV(Dist, LB) - LLV(Dist, LB)) * 100
    signed = Close > Close[n] ? %D : Close < Close[n] ? -%D : 0
    SDO = EMA(signed, Pds)
  Mode A:
    long crossover(sdo, 0)
    exit crossunder(sdo, 0)
  Mode B:
    require rising confirm sdo > sdo[1] on entry —
    only if Mode A over-whips; identical across all four.
  Prefer (n=14, LB=100, Pds=3) Mode A.
  != classic Stoch / != Apirine MAB band-break / != RMI / != TII.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill n/LB inflate until n collapses; Kill classic Stoch / MAB labeled SDO;
  Kill Track-B CK/QQE/MAMA/Wilder-VS graft. Prefer Mode A (14, 100, 3), 1H+.

eth_smoke:
  Kill params retuned only on ETH; Kill Stoch labeled SDO. Prefer identical params.

sol_smoke:
  Kill params retuned only on SOL; 15m spam; stage1-30 grafts.

bnb_smoke:
  Kill params retuned only on BNB; Mode B only on BNB; ungated shorts.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import apirine_sdo, atr, crossover, crossunder

STRATEGY_ID = "apirine-sdo-zero-cross"


@dataclass(frozen=True)
class ApirineSdoParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    n: int = 14                   # 8, 14, 20, 40
    lb: int = 100                 # 50, 100, 200
    pds: int = 3                  # 3, 5, 6
    rising_req: bool = False      # Mode B rising confirm
    atr_trail_mult: float = 0.0   # 0.0 (off)
    atr_len: int = 14


def validate_btc_smoke(params: ApirineSdoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {8, 14, 20, 40}:
        return False, f"btc_smoke: n={params.n} not in {{8, 14, 20, 40}}"
    if params.lb not in {50, 100, 200}:
        return False, f"btc_smoke: lb={params.lb} not in {{50, 100, 200}}"
    if params.pds not in {3, 5, 6}:
        return False, f"btc_smoke: pds={params.pds} not in {{3, 5, 6}}"
    return True, "PASS"


def validate_eth_smoke(params: ApirineSdoParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation."""
    if params.n not in {8, 14, 20, 40} or params.lb not in {50, 100, 200} or params.pds not in {3, 5, 6}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ApirineSdoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {8, 14, 20, 40} or params.lb not in {50, 100, 200} or params.pds not in {3, 5, 6}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ApirineSdoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.n not in {8, 14, 20, 40} or params.lb not in {50, 100, 200} or params.pds not in {3, 5, 6}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ApirineSdoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for apirine-sdo-zero-cross."""
    params = params or ApirineSdoParams()
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
    sdo = apirine_sdo(
        closes=closes,
        n=params.n,
        lb=params.lb,
        pds=params.pds,
    )
    zero_line = [0.0] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(sdo, zero_line, i)
        cross_dn = crossunder(sdo, zero_line, i)

        sdo_cur = sdo[i]
        sdo_prev = sdo[i - 1]
        rising = (sdo_cur is not None and sdo_prev is not None and sdo_cur > sdo_prev)

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and (rising or not params.rising_req)
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
