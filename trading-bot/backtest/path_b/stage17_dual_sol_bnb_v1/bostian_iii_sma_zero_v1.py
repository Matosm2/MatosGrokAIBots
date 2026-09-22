"""bostian-iii-sma-zero — Bostian Intraday Intensity Index (III) SMA Zero-Cross.

LOCKED ENCODE ORDER #4 (BTC LEAD PRIMARY).
Thesis:
  Stage16 pure-price structure/cycle failed SOL after BTC+ETH.
  Intraday Intensity (Bostian) = ((2C - H - L)/(H - L)) * Volume — signed close-location x volume.
  Mode A = SMA(III) zero-cross.
  Adds identical volume-flow polarity that may densify SOL participation vs Kagi under-flip,
  staying OHLC x volume portable across majors (no venue microstructure primary).
  != CMF.
  != OBV.
  != CLV x SMA stage13.
  != AccDist stage1.

Formula:
  rng = high - low
  iii = rng == 0 ? 0.0 : ((2*close - high - low) / rng) * volume
  iiiS = sma(iii, smaLen)
  Prefer smaLen = 21.

Mode A (BTC-LEAD PRIMARY — prefer):
  long: crossover(iiiS, 0)
  exit: crossunder(iiiS, 0)

Mode B (BNB quiet / quality hold):
  long: crossover(iiiS, 0) and iiiS > 0 (or hold)
  exit: crossunder(iiiS, 0)

btc_smoke:
  BTC-LEAD CRITICAL: Kill if smaLen inflated until BTC n collapses;
  Kill if CMF/OBV/CLV substitute;
  Kill if Mode B forced while Mode A BTC healthy. Prefer Mode A smaLen=21, 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill BTC-clear->ETH-wipe;
  Kill smaLen retuned only on ETH; Kill CLV graft.
  Prefer identical smaLen=21; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  Kill per-coin volume retune; Kill CMF/OBV/CLV labeled III;
  15m smaLen=3 spam; stage12-16 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different smaLen; Mode B shorts ungated; no ATR; per-coin volume retune.
  Prefer identical; long-only; ATR.

Forbidden: CMF/OBV/CLV/AccDist labeled III; BandPass/HP/3LB/SI/Kagi; stage12-16.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, bostian_iii, crossover, crossunder

STRATEGY_ID = "bostian-iii-sma-zero"


@dataclass(frozen=True)
class BostianIiiParams:
    mode: str = "mode_a"  # "mode_a" (iiiS x 0) | "mode_b" (iiiS x 0 + quality hold)
    sma_len: int = 21
    quality_threshold: float = 0.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: BostianIiiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.sma_len not in {10, 14, 21, 34}:
        return False, f"btc_smoke: sma_len={params.sma_len} not in locked set {{10, 14, 21, 34}}"
    if params.sma_len > 50:
        return False, f"btc_smoke: sma_len={params.sma_len} > 50 collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: BostianIiiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH CRITICAL)."""
    if params.sma_len not in {10, 14, 21, 34}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: BostianIiiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.sma_len <= 3:
        return False, "sol_smoke: 15m sma_len<=3 forbidden (spam)"
    if params.sma_len not in {10, 14, 21, 34}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: BostianIiiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.sma_len not in {10, 14, 21, 34}:
        return False, "bnb_smoke: params not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: BostianIiiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for bostian-iii-sma-zero."""
    params = params or BostianIiiParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    _, iii_s = bostian_iii(highs, lows, closes, volumes, sma_len=params.sma_len)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(iii_s, zero_line, i)
        cross_dn = crossunder(iii_s, zero_line, i)

        if params.mode == "mode_b":
            # Mode B: require iii_s > quality_threshold on entry
            val = iii_s[i]
            if val is None or val <= params.quality_threshold:
                cross_up = False

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
