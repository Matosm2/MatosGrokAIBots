"""pee-ttf-zero-cross — Pee Trend Trigger Factor zero-cross (Mode A) / ±100 reclaim (Mode B).

LOCKED ENCODE ORDER #1 (BTC->ETH PORTABILITY PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage13 wiped REI (BTC 1.530x -> ETH -1.201x wipe) and parked Pee TDI.
  Pee TTF is a dual-window H/L buy-power vs sell-power oscillator (-inf..+inf, commonly +-100 thr) —
  != TDI, != REI, != RWI, != Donchian.
  Mode A locks TTF zero-cross for BTC+ETH clearing density; Mode B = classic Pee +-100 reclaim only if
  Mode A over-whips quieter BNB — identical Length across coins.

Formula:
  buy = highest(high, L) - lowest(low[L], L)
  sell = highest(high[L], L) - lowest(low, L)
  den = 0.5 * (buy + sell)
  ttf = 100 * (buy - sell) / den if den != 0 else 0
  Prefer L=15.

Mode A (BTC->ETH-PRIMARY dense zero — prefer first):
  long: crossover(ttf, 0)
  exit: crossunder(ttf, 0) or ATR stop.

Mode B (BNB-quiet / Pee classic):
  long: crossover(ttf, 100)
  exit: crossunder(ttf, -100) or ATR stop.
  (identical L across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if CSI/PMO/Gaussian damp; Kill if L >> 20 n collapses; Kill if Mode B forced while Mode A BTC n healthy.
  Prefer Mode A L=15, 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears >=1.2x then ETH wipes (stage13 REI pattern); Kill if L or Mode retuned only on ETH; Kill if REI graft.
  Prefer identical Mode A L=15 on ETH after BTC; ETH n multi-dozen.

sol_smoke:
  Kill if TDI/REI/RWI/Donchian labeled TTF; 15m L=5 spam; ER/AO/PGO/stage12-13.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different L; Mode B shorts ungated; no ATR; volume graft.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs L != SOL.

Forbidden: Pee TDI/Direction; REI/PZO/TMO/RF/CLV; RWI; Donchian; ADX; ER-gate; stage12 duals; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, pee_ttf

STRATEGY_ID = "pee-ttf-zero-cross"


@dataclass(frozen=True)
class PeeTtfParams:
    mode: str = "mode_a"  # "mode_a" (ttf cross 0) | "mode_b" (ttf cross 100, exit crossunder -100)
    length: int = 15
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: PeeTtfParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length > 25:
        return False, f"btc_smoke: L={params.length} > 25 collapses BTC n"
    if params.length not in {10, 15, 20}:
        return False, f"btc_smoke: L={params.length} not in locked set {{10, 15, 20}}"
    return True, "PASS"


def validate_eth_smoke(params: PeeTtfParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.length not in {10, 15, 20}:
        return False, f"eth_smoke: L={params.length} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: PeeTtfParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m L<=5 forbidden (spam)"
    if params.length not in {10, 15, 20}:
        return False, f"sol_smoke: L={params.length} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: PeeTtfParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    if params.length > 25:
        return False, "bnb_smoke: length too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PeeTtfParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pee-ttf-zero-cross."""
    params = params or PeeTtfParams()
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
    ttf = pee_ttf(highs, lows, length=params.length)

    zero_line = [0.0] * n
    pos100_line = [100.0] * n
    neg100_line = [-100.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_a":
            cross_up = crossover(ttf, zero_line, i)
            cross_dn = crossunder(ttf, zero_line, i)
        else:  # mode_b: classic Pee +100/-100
            cross_up = crossover(ttf, pos100_line, i)
            cross_dn = crossunder(ttf, neg100_line, i)

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
