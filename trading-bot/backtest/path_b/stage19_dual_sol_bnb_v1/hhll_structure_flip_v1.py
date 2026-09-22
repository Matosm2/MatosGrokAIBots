"""hhll-structure-flip — Confirmed HH/LL market structure polarity flip.

LOCKED ENCODE ORDER #1 (BTC LEAD PRIMARY).
Thesis:
  Stage16 Kagi cleared BTC+ETH then stalled on SOL; Stage18 never left BTC.
  HH/LL structure flip uses confirmed pivot highs and pivot lows:
    ph = pivothigh(high, lb, lb)
    pl = pivotlow(low, lb, lb)
    bullStruct = sh1 > sh0 and sl1 > sl0 (>= 2 confirmed swings each).
  Closed-bar only after right-confirm (lb bars) — strictly NO ZigZag look-ahead.
  Mode A: flip long on transition to bullish structure (bullStruct and not bullStruct[1]).
  Exit when not bullStruct (structure lost / flipped bearish).
  Identical lb across all four coins.
  != Kagi / 3LB (stage16).
  != ZigZag (no unconfirmed look-ahead).
  != PDH / PWH (stage1/2).

Mode A (BTC-LEAD PRIMARY — prefer):
  long: bullStruct and not bullStruct[1]
  exit: not bullStruct

Mode B (BNB quiet / chatter):
  larger lb / BOS entry requirement — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill lb inflate until flips collapse;
  Kill Mode A BTC 0 / chop; Kill Kagi/3LB/ZigZag-look-ahead substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A lb=3, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill lb retuned only on ETH; Kill Kagi/3LB/III labeled HHLL.
  Prefer identical lb=3; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m lb=1; stage12-18 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different lb; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: ZigZag without right-confirm; Kagi/3LB/Renko/PnF labeled HHLL; stage12-18 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, hhll_structure

STRATEGY_ID = "hhll-structure-flip"


@dataclass(frozen=True)
class HhllParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    lb: int = 3
    bos_entry: bool = False
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: HhllParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.lb not in {2, 3, 5}:
        return False, f"btc_smoke: lb={params.lb} not in locked sweep {{2, 3, 5}}"
    if params.lb > 10:
        return False, f"btc_smoke: lb={params.lb} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: HhllParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.lb not in {2, 3, 5}:
        return False, f"eth_smoke: lb={params.lb} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: HhllParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.lb <= 1:
        return False, "sol_smoke: 15m lb<=1 forbidden (spam)"
    if params.lb not in {2, 3, 5}:
        return False, "sol_smoke: lb not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: HhllParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.lb not in {2, 3, 5}:
        return False, "bnb_smoke: lb not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: HhllParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for hhll-structure-flip."""
    params = params or HhllParams()
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
    bull_struct, bear_struct, sh_series, sl_series = hhll_structure(
        highs=highs, lows=lows, lb=params.lb
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        curr_bull = bull_struct[i]
        prev_bull = bull_struct[i - 1]

        rising_edge = curr_bull and not prev_bull

        entry_trigger = False
        if params.bos_entry:
            sh = sh_series[i]
            if curr_bull and sh is not None and c > sh:
                prev_sh = sh_series[i - 1]
                if not prev_bull or prev_sh is None or closes[i - 1] <= prev_sh:
                    entry_trigger = True
        else:
            entry_trigger = rising_edge

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

            exit_cond = not curr_bull
            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
