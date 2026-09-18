"""vqi-sum-sma-cross-v1 — Stridsman Volatility Quality Index cumulative sum x SMA cross.

LOCKED ENCODE ORDER #5 (OPTIONAL 5TH: OHLC-only volatility quality).
Thesis:
  Stage10 wiped Dorsey RelVol; ATR%ile/CMF/Chaikin Osc burned. Stridsman VQI scores
  directional "quality" of bar volatility from OHLC+TR (no volume) then cumulates;
  Path-B Mode A = VQI-sum x short SMA cross — dense dual-line on 1H, != RelVol stdev-RSI shape,
  != Chaikin Osc AD-line, != ATR%ile rank gate. OHLC-only -> BNB-portable identical (sma_fast).

Formula:
  TR = max(H, C[1]) - min(L, C[1])
  HL = H - L
  guard TR > 0 and HL > 0
  vqiRaw = 0.5 * ((C - C[1]) / TR + (C - O) / HL)
  vqiBar = abs(vqiRaw) * 0.5 * ((C - C[1]) + (C - O))
  vqiSum = cumsum(vqiBar)
  fast = sma(vqiSum, sma_fast) (prefer 9; also 5, 14)

Mode A (primary / dense cross):
  long: crossover(vqiSum, fast)
  exit: crossunder(vqiSum, fast) or ATR stop.

Mode B (slow confirm):
  also require vqiSum > sma(vqiSum, 200) — if Mode A over-whips BNB.
  exit: crossunder(vqiSum, fast) or ATR stop.

sol_smoke:
  Kill if: RelVol/CMF/Chaikin labeled VQI; invented formula without Stridsman match;
  15m sma_fast=2 spam; ER/AO/PGO graft. Prefer Mode A sma_fast=9, 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class.

bnb_smoke:
  Kill if: different sma_fast than SOL; Mode B shorts ungated; no ATR; volume graft "to help BNB".
  Prefer identical params; long-only; ATR exit.

Forbidden: RelVol/RVI/CMF/Chaikin Osc/ATR%ile; volume graft; ER-gate; AO/ROC/WMA/PGO;
TII/Rainbow/TCF/DEMA; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, sma, stridsman_vqi

STRATEGY_ID = "vqi-sum-sma-cross-v1"


@dataclass(frozen=True)
class VqiSumSmaParams:
    mode: str = "mode_a"  # "mode_a" (vqiSum cross fast) | "mode_b" (vqiSum cross fast and vqiSum > slow)
    sma_fast: int = 9
    sma_slow: int = 200
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: VqiSumSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.sma_fast <= 2:
        return False, "sol_smoke: 15m sma_fast<=2 forbidden (spam)"
    if params.sma_fast not in {5, 9, 14}:
        return False, f"sol_smoke: sma_fast={params.sma_fast} not in locked set {{5, 9, 14}}"
    return True, "PASS"


def validate_bnb_smoke(params: VqiSumSmaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.sma_fast <= 0 or params.sma_fast > 100:
        return False, "bnb_smoke: sma_fast must be in (0, 100]"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VqiSumSmaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vqi-sum-sma-cross-v1."""
    params = params or VqiSumSmaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    vqi_sum, fast_vals = stridsman_vqi(opens, highs, lows, closes, sma_fast=params.sma_fast)

    slow_vals: list[float | None] = [None] * n
    if params.mode == "mode_b":
        # Calculate SMA(vqiSum, 200)
        first_valid = -1
        for i in range(n):
            if vqi_sum[i] is not None:
                first_valid = i
                break
        if first_valid != -1:
            valid_sums = [float(vqi_sum[i]) for i in range(first_valid, n)]
            inner_slow = sma(valid_sums, params.sma_slow)
            for i, val in enumerate(inner_slow):
                slow_vals[first_valid + i] = val

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
            if crossunder(vqi_sum, fast_vals, i):
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
                if crossover(vqi_sum, fast_vals, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(vqiSum, fast) and vqiSum > slow
                if crossover(vqi_sum, fast_vals, i):
                    v_val = vqi_sum[i]
                    s_val = slow_vals[i]
                    if v_val is not None and s_val is not None and v_val > s_val:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
