"""three-line-break-flip — Three Line Break N-line reversal structure flip.

LOCKED ENCODE ORDER #3 (BTC LEAD PRIMARY — CLOSE-ONLY STRUCTURE REVERSAL).
Thesis:
  Stage12/15 over-damp killed BTC; Stage14 TTF quiet-wiped BNB.
  Three Line Break (Nison / StockCharts) is a close-only structure rule:
  continue same-color line on extension;
  reverse when close breaks the extreme of the prior N lines (classic N=3).
  No smoother, no rank, no dual-HP — intended BTC-lead responsive density
  with identical N on ETH/SOL/BNB.
  != Donchian channel break,
  != stage1-4 pivot accept-breaks,
  != Range Filter flip.
  Encode on standard OHLC closes (not synthetic Line Break chart type).

Formula:
  Maintain direction (+1/-1) and last N line extremes from closes only (var state).
  Bullish reverse: prior direction bearish AND close > highest of last N bearish-line highs.
  Bearish reverse: prior direction bullish AND close < lowest of last N bullish-line lows.
  Prefer N=3.

Mode A (BTC-LEAD PRIMARY — prefer first):
  long on bullish reversal;
  exit on bearish reversal (or ATR stop).

Mode B (BNB quiet):
  N=4 or require 2 extension lines before arm — only if Mode A over-whips;
  identical N across coins.

btc_smoke:
  BTC-LEAD CRITICAL: Kill if N inflated until flips collapse;
  Kill if Donchian/SuperTrend graft sparsifies;
  Kill if Mode B forced while Mode A BTC already healthy.
  Prefer Mode A N=3, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill if BTC clears then ETH wipes.
  Kill if N retuned only on ETH; Kill if pivot-accept substitute.
  Prefer identical N=3 on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if Donchian / RangeFilter / TTF labeled 3LB; 15m N=1 spam; stage12-15 grafts.
  Retention check: after ETH, SOL n multi-dozen-class on 6m 1H.

bnb_smoke:
  BNB-after-BTC+ETH+SOL quiet-wipe CRITICAL:
  different N than SOL; Mode B shorts ungated; no ATR; per-coin retune.
  Prefer identical params; long-only; ATR exit.

Forbidden: Donchian; SuperTrend; RangeFilter; pivot PDH/PWH grafts; request.security;
Line-Break chart TF as data source; stage12-15 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, three_line_break

STRATEGY_ID = "three-line-break-flip"


@dataclass(frozen=True)
class ThreeLineBreakParams:
    mode: str = "mode_a"  # "mode_a" (N=3 standard flip) | "mode_b" (N=4 or quiet)
    n_lines: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: ThreeLineBreakParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n_lines > 6:
        return False, f"btc_smoke: n_lines={params.n_lines} > 6 collapses BTC n"
    if params.n_lines not in {2, 3, 4}:
        return False, f"btc_smoke: n_lines={params.n_lines} not in locked set {{2, 3, 4}}"
    return True, "PASS"


def validate_eth_smoke(params: ThreeLineBreakParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.n_lines not in {2, 3, 4}:
        return False, f"eth_smoke: n_lines={params.n_lines} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ThreeLineBreakParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.n_lines <= 1:
        return False, "sol_smoke: 15m n_lines<=1 forbidden (spam)"
    if params.n_lines not in {2, 3, 4}:
        return False, f"sol_smoke: n_lines={params.n_lines} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: ThreeLineBreakParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.n_lines <= 0:
        return False, "bnb_smoke: n_lines must be > 0"
    if params.n_lines > 6:
        return False, "bnb_smoke: n_lines too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ThreeLineBreakParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for three-line-break-flip."""
    params = params or ThreeLineBreakParams()
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
    _, bull_flips, bear_flips = three_line_break(closes, n=params.n_lines)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        bull_rev = bull_flips[i]
        bear_rev = bear_flips[i]

        if not in_pos:
            if bull_rev:
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

            if stop_hit or bear_rev:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
