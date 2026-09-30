"""pee-tdi-direction-zero-v1 — Trend Detection Index Direction Indicator zero-cross.

LOCKED ENCODE ORDER #2 (BNB-SURVIVAL-FIRST + DENSITY: SOL + BNB survival).
Thesis:
  Stage10 parked gated TDI as sparse-n risk and wiped TII/TCF. Pee Direction Indicator = sum of
  N-bar momenta over last N — signed momentum polarity != TII SMA-deviation share, != TCF
  recursive continuation, != ADX.
  Mode A locks Direction zero-cross alone for density (addresses stage10 sparse gate);
  Mode B restores classic TDI>0 and Direction>0 for quality if Mode A over-whips BNB.
  Close-only -> BNB-portable identical N.

Formula:
  mom = close - close[N]
  absMom = abs(mom)
  dir = sum(mom, N)
  av = abs(dir)
  sumAM2 = sum(absMom, 2*N)
  sumAM1 = sum(absMom, N)
  tdi = av - (sumAM2 - sumAM1)

Mode A (prefer / dense Direction zero):
  long: crossover(dir, 0)
  exit: crossunder(dir, 0) or ATR stop.
  N in {14, 20, 25}; prefer 20.

Mode B (classic quality / BNB quiet):
  long: crossover(dir, 0) and tdi > 0
  exit: crossunder(dir, 0) or tdi < 0 or ATR stop.

sol_smoke:
  Kill if: TII/TCF formula used; ADX labeled TDI; Traders Dynamic Index RSI stack;
  15m N=5 spam; ER/PGO graft. Prefer Mode A N=20, 1H+.
  Retention check: after ETH, SOL Mode-A n must stay multi-dozen-class.

bnb_smoke:
  Kill if: different N than SOL; Mode B shorts ungated; no ATR; forcing Mode B only on BNB
  while SOL stays Mode A. Prefer identical N+Mode; long-only; ATR exit.

Forbidden: TII/TCF; ADX/DMI; ER-gate; RSI "Traders Dynamic Index"; AO/ROC/WMA/PGO; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, pee_tdi_direction

STRATEGY_ID = "pee-tdi-direction-zero-v1"


@dataclass(frozen=True)
class PeeTdiDirectionParams:
    mode: str = "mode_a"  # "mode_a" (dir cross 0) | "mode_b" (dir cross 0 and tdi > 0, exit on crossunder or tdi < 0)
    n_len: int = 20
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: PeeTdiDirectionParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.n_len <= 5:
        return False, "sol_smoke: 15m N<=5 forbidden (spam)"
    if params.n_len not in {14, 20, 25}:
        return False, f"sol_smoke: N={params.n_len} not in locked set {{14, 20, 25}}"
    return True, "PASS"


def validate_bnb_smoke(params: PeeTdiDirectionParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.n_len <= 0:
        return False, "bnb_smoke: N must be > 0"
    if params.n_len > 50:
        return False, "bnb_smoke: N too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PeeTdiDirectionParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pee-tdi-direction-zero-v1."""
    params = params or PeeTdiDirectionParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    dir_vals, tdi_vals = pee_tdi_direction(closes, n_len=params.n_len)

    zeroes: list[float | None] = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

        # Update trailing stop if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False
            # Exit on direction crossunder 0
            if crossunder(dir_vals, zeroes, i):
                exit_signal = True

            # In Mode B, exit also if tdi < 0
            if params.mode == "mode_b" and tdi_vals[i] is not None and tdi_vals[i] < 0.0:
                exit_signal = True

            # Stop hit check
            if stop_level is not None and c < stop_level:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0
                stop_level = None
                continue

        # Check entries if flat
        if not in_pos and i > 0:
            enter_signal = False
            if params.mode == "mode_a":
                if crossover(dir_vals, zeroes, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(dir, 0) and tdi > 0
                if crossover(dir_vals, zeroes, i):
                    if tdi_vals[i] is not None and tdi_vals[i] > 0.0:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
