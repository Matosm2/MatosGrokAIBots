"""dpo-zero-cross — Detrended Price Oscillator zero-cross.

LOCKED ENCODE ORDER #1 (BTC LEAD + ETH-PORTABLE PRIMARY).
Thesis:
  Stage17 Bostian III cleared dense BTC then ETH HARD FAIL (volume-intensity overfit).
  DPO is a close-only displaced-SMA deviation (price-path):
    displace = floor(X/2) + 1
    smaX = sma(close, X)
    dpo = close[displace] - smaX (StockCharts displace).
  Mode A = DPO x 0 cross.
  Intended ETH-portable cycle-mid polarity without BTC-volume microstructure,
  without Decycler/BandPass/Cyber Cycle EXIT adjacency, and without stage17 III class.
  Identical period on all four coins.
  != Decycler (stage3).
  != BandPass (stage16).
  != Cyber Cycle.
  != Bostian III (stage17).

Formula:
  smaX = sma(close, X)
  dpo = close[floor(X/2)+1] - smaX (StockCharts displace).
  Prefer X = 20. Do NOT right-shift to defeat cycle purpose on first pass.

Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer):
  long: crossover(dpo, 0)
  exit: crossunder(dpo, 0)

Mode B (BNB quiet / ETH chatter):
  require |dpo| hold or threshold / longer X — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill X inflate until n collapses;
  Kill Decycler/BandPass substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A X=20, 1H+.

eth_smoke:
  BTC->ETH PRIMARY CRITICAL: Kill if BTC clears >=1.2x then ETH under 1.2x;
  Kill X retuned only on ETH; Kill III/volume or Decycler/BandPass labeled DPO.
  Prefer identical X=20; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  15m X=5; stage12-17 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different X; Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: Decycler/BandPass/Cyber Cycle labeled DPO; III/volume grafts; right-shift Disparity clone; stage12-17.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, detrended_price_oscillator

STRATEGY_ID = "dpo-zero-cross"


@dataclass(frozen=True)
class DpoParams:
    mode: str = "mode_a"  # "mode_a" (dpo x 0) | "mode_b" (|dpo| threshold / hold)
    length: int = 20
    hold_bars: int = 0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: DpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {14, 20, 28}:
        return False, f"btc_smoke: length={params.length} not in locked sweep {{14, 20, 28}}"
    if params.length > 50:
        return False, f"btc_smoke: length={params.length} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: DpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PRIMARY CRITICAL)."""
    if params.length not in {14, 20, 28}:
        return False, f"eth_smoke: length={params.length} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: DpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m length<=5 forbidden (spam)"
    if params.length not in {14, 20, 28}:
        return False, "sol_smoke: length not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: DpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.length not in {14, 20, 28}:
        return False, "bnb_smoke: length not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: DpoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for dpo-zero-cross."""
    params = params or DpoParams()
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
    dpo_vals = detrended_price_oscillator(closes, length=params.length)
    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0
    bars_since_cross = 999

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(dpo_vals, zero_line, i)
        cross_dn = crossunder(dpo_vals, zero_line, i)

        if cross_up:
            bars_since_cross = 0
        else:
            bars_since_cross += 1

        entry_trigger = False
        if params.mode == "mode_b" and params.hold_bars > 0:
            # Mode B: trigger entry on the bar that fulfills hold_bars requirement
            dpo_val = dpo_vals[i]
            if bars_since_cross == params.hold_bars and dpo_val is not None and dpo_val > 0:
                entry_trigger = True
        else:
            entry_trigger = cross_up

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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
