"""khalil-pzo-zero-cross-v1 — Khalil & Steckler Price Zone Oscillator zero-cross.

LOCKED ENCODE ORDER #2 (BTC-CLEARING PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage12 wiped PMO×signal and CSI×signal (0 BTC). PZO assigns each close a sign (+close if up-close,
  -close if down-close), then PZO = 100 * EMA(signed, n) / EMA(close, n) — signed persistence oscillator,
  != VZO (volume), != raw ROC zero, != PSY count-frequency, != PMO custom-%ROC double-smooth×signal,
  != MA dual-cross.
  Mode A locks PZO zero-cross (responsive BTC polarity of up- vs down-close persistence).
  Close-only -> identical Length on SOL+BNB.
  Forbidden: ADX>18 / EMA60 grafts from TASC article (ADX burned).

Formula:
  signed = close > close[1] ? close : close < close[1] ? -close : 0.0
  cp = ema(signed, n)
  tc = ema(close, n)
  pzo = tc != 0 ? 100 * cp / tc : 0
  Prefer n=14.

Mode A (BTC-PRIMARY):
  long: crossover(pzo, 0)
  exit: crossunder(pzo, 0) or ATR stop.

Mode B (BNB quiet):
  long: crossover(pzo, 0) and pzo > 0
  exit: crossunder(pzo, 0) or pzo < 0 or ATR stop.
  (identical n across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if n raised aggressively to damp until BTC n collapses;
  Kill if PMO×signal/CSI/ADX/EMA60 graft. Prefer Mode A n=14, 1H+.

sol_smoke:
  Kill if VZO/ROC/PSY labeled PZO; 15m n=3; stage12 grafts. Retention check: after ETH, SOL n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+SOL: different n than SOL; Mode B shorts ungated; no ATR; volume/VZO graft.
  Prefer identical params; long-only; ATR exit.

Forbidden: VZO/volume primary; ADX/DMI; EMA60 trend graft; ROC-zero labeled PZO; PMO×signal; CSI; stage12 duals.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, khalil_pzo

STRATEGY_ID = "khalil-pzo-zero-cross-v1"


@dataclass(frozen=True)
class KhalilPzoParams:
    mode: str = "mode_a"  # "mode_a" (pzo cross 0) | "mode_b" (pzo cross 0 and pzo > 0)
    n_len: int = 14
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: KhalilPzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n_len > 30:
        return False, f"btc_smoke: n={params.n_len} > 30 collapses BTC n"
    if params.n_len not in {10, 14, 20}:
        return False, f"btc_smoke: n={params.n_len} not in locked set {{10, 14, 20}}"
    return True, "PASS"


def validate_sol_smoke(params: KhalilPzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.n_len <= 3:
        return False, "sol_smoke: 15m n<=3 forbidden (spam)"
    if params.n_len not in {10, 14, 20}:
        return False, f"sol_smoke: n={params.n_len} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: KhalilPzoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+SOL)."""
    if params.n_len <= 0:
        return False, "bnb_smoke: n_len must be > 0"
    if params.n_len > 40:
        return False, "bnb_smoke: n_len too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KhalilPzoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for khalil-pzo-zero-cross-v1."""
    params = params or KhalilPzoParams()
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
    pzo = khalil_pzo(closes, n_len=params.n_len)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        curr_pzo = pzo[i]
        cross_up = crossover(pzo, zero_line, i)
        cross_dn = crossunder(pzo, zero_line, i)

        if not in_pos:
            entry_cond = cross_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_pzo is not None and curr_pzo > 0.0)

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

            exit_cond = cross_dn
            if params.mode == "mode_b":
                exit_cond = exit_cond or (curr_pzo is not None and curr_pzo < 0.0)

            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
