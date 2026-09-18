"""er-sma-gate-cross-v1 — Kaufman ER gate + SMA fast×slow crossover (ER as filter only).

LOCKED ENCODE ORDER #1 (DUAL-SURVIVAL: SOL + BNB survival).
Thesis:
  Stage6 wiped adaptive MA primaries (FRAMA/HMA/McGinley). ER alone is a path-efficiency
  regime sensor (0–1), not an adaptive average: Direction/Volatility over n — used ONLY as
  a gate so SMA dual-cross fires in efficient legs and stands aside in chop.
  Explicitly != burned KAMA (no SC mapping, no recursive KAMA line).
  Close-only -> majors-portable; identical (N_er, thr, Lf, Ls) on SOL+BNB.

Formula:
  er = abs(close - close[N]) / sum(abs(close - close[1]), N); denom=0 -> 0.
  N in {10, 14, 20}. thr in {0.30, 0.35, 0.40}.

Mode A (primary):
  fast = ta.sma(close, Lf); slow = ta.sma(close, Ls)
  long: ta.crossover(fast, slow) and er > thr
  exit: ta.crossunder(fast, slow) or ATR stop.
  (Lf, Ls) in {(9, 21), (10, 30), (12, 26)}.

Mode B (secondary denser):
  long while close > slow and er > thr — only if Mode A SOL under-fires.

sol_smoke:
  Kill if: KAMA/SC disguised as ER; thr retuned per coin; 15m thr=0.15.
  Prefer Mode A, N=10, thr=0.35, (10,30), 1H+.
  Retention check: SOL trade count must not collapse vs ETH under same params.

bnb_smoke:
  Kill if: different thr/N than SOL; Mode B ungated shorts; ADX grafted.
  Prefer identical params; long-only; ATR.

Forbidden: KAMA recursive, VIDYA, FRAMA, HMA, McGinley, ADX, ATR%ile gate, RSI.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, efficiency_ratio, sma

STRATEGY_ID = "er-sma-gate-cross-v1"


@dataclass(frozen=True)
class ErSmaParams:
    mode: str = "mode_a"  # "mode_a" (crossover + ER gate) | "mode_b" (close > slow & ER gate)
    er_len: int = 10
    er_threshold: float = 0.35
    fast_len: int = 10
    slow_len: int = 30
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: ErSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.er_threshold <= 0.15:
        return False, "sol_smoke: 15m thr<=0.15 forbidden (spam)"
    if params.er_len not in {10, 14, 20}:
        return False, f"sol_smoke: N={params.er_len} not in locked set {{10, 14, 20}}"
    if params.er_threshold not in {0.30, 0.35, 0.40}:
        return False, f"sol_smoke: thr={params.er_threshold} not in locked set {{0.30, 0.35, 0.40}}"
    if params.mode == "mode_a" and (params.fast_len, params.slow_len) not in {
        (9, 21),
        (10, 30),
        (12, 26),
    }:
        return False, f"sol_smoke: (Lf, Ls)=({params.fast_len}, {params.slow_len}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ErSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.fast_len >= params.slow_len:
        return False, "bnb_smoke: fast_len >= slow_len invalid"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ErSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for er-sma-gate-cross-v1."""
    params = params or ErSmaParams()
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
    er_vals = efficiency_ratio(closes, params.er_len)
    fast_sma = sma(closes, params.fast_len)
    slow_sma = sma(closes, params.slow_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

        # Trailing stop update if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False
            if crossunder(fast_sma, slow_sma, i):
                exit_signal = True

            # Mode B exit if close drops below slow
            if params.mode == "mode_b" and slow_sma[i] is not None and c < slow_sma[i]:
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
        if not in_pos and i > 0 and slow_sma[i] is not None and slow_sma[i - 1] is not None and er_vals[i] is not None:
            enter_signal = False
            er_ok = er_vals[i] > params.er_threshold

            if params.mode == "mode_a":
                if crossover(fast_sma, slow_sma, i) and er_ok:
                    enter_signal = True
            elif params.mode == "mode_b":
                if c > slow_sma[i] and er_ok:
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = c - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
