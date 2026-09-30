"""hannula-pfe-zero-cross — Hannula Polarized Fractal Efficiency EMA zero-cross.

LOCKED ENCODE ORDER #2 (BTC->ETH PORTABILITY PRIMARY + BNB-PORTABLE SECONDARY).
Thesis:
  Stage7 burned ER-as-gate; stage13 deferred thr-gated PFE/VHF/RAVI.
  Hannula PFE is a signed path-efficiency oscillator (-100..+100): straight-line vs jagged close path,
  polarized by net direction — encode class is EMA(PFE) x 0, != ER-gate, != VHF-thr, != RWI, != REI.
  Close-only -> identical (period, smooth) on BTC/ETH/SOL/BNB — designed for ETH liquidity portability.

Formula:
  For bar t >= period:
    path = sum(sqrt((close[i] - close[i-1])^2 + 1) for i in [t-period+1 .. t])
    straight = sqrt((close[t] - close[t-period])^2 + period^2)
    sign = 1 if close[t] > close[t-period] else -1 if close[t] < close[t-period] else 0
    raw = 100 * sign * straight / path if path != 0 else 0
  pfe = ema(raw, smooth)
  Prefer period=10, smooth=5.

Mode A (BTC->ETH-PRIMARY):
  long: crossover(pfe, 0)
  exit: crossunder(pfe, 0) or ATR stop.

Mode B (BNB quiet / quality hold):
  long: crossover(pfe, 0) and pfe > 20 (or pfe > 0 quality hold)
  exit: crossunder(pfe, 0) or ATR stop.
  (identical params across coins. NOT |PFE|>50 thr as Mode A).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if smooth raised into stage12-damp territory; Kill if Mode A becomes |PFE|>50 thr-gate; Kill if ERxSMA graft.
  Prefer Mode A (10,5), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears then ETH wipes (stage13 REI pattern); Kill if period/smooth retuned only on ETH; Kill if REI substitute.
  Prefer identical (10,5) on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if ER-gate/VHF labeled PFE; 15m period=3; stage12-13.
  Retention check: after ETH, SOL n multi-dozen-class.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (period,smooth) than SOL; Mode B shorts ungated; no ATR.
  Prefer identical params; long-only; ATR exit.

Forbidden: ER-gate; VHF/RAVI thr Mode A; REI/PZO/TMO/RF/CLV; stage12 duals; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, hannula_pfe

STRATEGY_ID = "hannula-pfe-zero-cross"


@dataclass(frozen=True)
class HannulaPfeParams:
    mode: str = "mode_a"  # "mode_a" (pfe cross 0) | "mode_b" (pfe cross 0 and pfe > 20)
    period: int = 10
    smooth: int = 5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: HannulaPfeParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.smooth > 15:
        return False, f"btc_smoke: smooth={params.smooth} > 15 enters stage12-damp"
    if params.period not in {8, 10, 14} or params.smooth not in {3, 5, 8}:
        return False, f"btc_smoke: ({params.period},{params.smooth}) not in locked sweep grid"
    return True, "PASS"


def validate_eth_smoke(params: HannulaPfeParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.period not in {8, 10, 14} or params.smooth not in {3, 5, 8}:
        return False, f"eth_smoke: ({params.period},{params.smooth}) retuned away from locked grid"
    return True, "PASS"


def validate_sol_smoke(params: HannulaPfeParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period <= 3:
        return False, "sol_smoke: 15m period<=3 forbidden (spam)"
    if params.period not in {8, 10, 14} or params.smooth not in {3, 5, 8}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: HannulaPfeParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.period <= 0 or params.smooth <= 0:
        return False, "bnb_smoke: period and smooth must be > 0"
    if params.smooth > 15:
        return False, "bnb_smoke: smooth too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: HannulaPfeParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for hannula-pfe-zero-cross."""
    params = params or HannulaPfeParams()
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
    pfe = hannula_pfe(closes, period=params.period, smooth=params.smooth)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(pfe, zero_line, i)
        cross_dn = crossunder(pfe, zero_line, i)

        pfe_val = pfe[i] if pfe[i] is not None else 0.0

        if params.mode == "mode_b":
            entry_cond = cross_up and pfe_val > 20.0
        else:
            entry_cond = cross_up

        if not in_pos:
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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
