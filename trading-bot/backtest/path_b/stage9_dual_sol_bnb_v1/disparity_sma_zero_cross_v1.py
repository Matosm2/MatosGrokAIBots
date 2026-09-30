"""disparity-sma-zero-cross-v1 — Disparity Index SMA zero-cross.

LOCKED ENCODE ORDER #2 (DUAL-SURVIVAL + DENSITY: SOL + BNB survival).
Thesis:
  Nison % distance of close from SMA: DI = 100 * (Close - SMA) / SMA.
  Zero-cross ≡ close x SMA polarity — dense MA-touch class on 1H majors.
  Explicitly != burned ROC (lookback close ratio), != parked PGO ((Close-SMA)/EMA(TR)),
  != WMA fast x slow dual.
  Close+SMA portable; identical N on SOL+BNB.

Formula:
  ma = ta.sma(close, N); guard ma > 0.
  di = 100.0 * (close - ma) / ma
  N in {10, 14, 20, 30}; prefer 20 (common DI default).

Mode A (primary / zero-line):
  long: ta.crossover(di, 0)
  exit: ta.crossunder(di, 0) or ATR stop.

Mode B (secondary OS reclaim):
  long: ta.crossover(di, -ext) where ext in {1.0, 2.0, 3.0}; default ext=2.0.
  exit: ta.crossunder(di, 0) or ATR stop.

sol_smoke:
  Kill if: ROC/PGO substitute; WMA dual disguise; 15m N=5 spam; ER graft.
  Prefer Mode A N=20, 1H+.
  Retention: SOL n after ETH should stay dense; if DI stuck positive through dumps without exit, check ma warmup.

bnb_smoke:
  Kill if: different N than SOL; Mode B extremes-only shorts ungated; no ATR.
  Prefer identical N; long-only; ATR exit.

Forbidden: ROC primary; PGO/ATR-denom; WMA dual; HMA/ZLEMA/VWMA; ER-gate; EMA-DI unlabeled.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, disparity_index

STRATEGY_ID = "disparity-sma-zero-cross-v1"


@dataclass(frozen=True)
class DisparitySmaParams:
    mode: str = "mode_a"  # "mode_a" (crossover 0) | "mode_b" (reclaim from -ext)
    length: int = 20
    oversold_ext: float = 2.0  # ext in {1.0, 2.0, 3.0}
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: DisparitySmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m N<=5 forbidden (spam)"
    if params.length not in {10, 14, 20, 30}:
        return False, f"sol_smoke: N={params.length} not in locked set {{10, 14, 20, 30}}"
    return True, "PASS"


def validate_bnb_smoke(params: DisparitySmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DisparitySmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for disparity-sma-zero-cross-v1."""
    params = params or DisparitySmaParams()
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
    di_vals = disparity_index(closes, params.length)

    zeros: list[float | None] = [0.0] * n
    neg_ext_levels: list[float | None] = [-params.oversold_ext] * n

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
            # Exit on crossunder 0
            if crossunder(di_vals, zeros, i):
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
                # Mode A: crossover(di, 0)
                if crossover(di_vals, zeros, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(di, -ext)
                if crossover(di_vals, neg_ext_levels, i):
                    enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
