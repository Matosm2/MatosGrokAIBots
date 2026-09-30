"""ehlers-bandpass-zero — Ehlers BandPass Filter zero-cross.

LOCKED ENCODE ORDER #1 (BTC LEAD PRIMARY — DENSE ZERO CROSS).
Thesis:
  Stage15 rank/HP-band-RMS/corr/NET/DVI over-damped BTC to 0 PASS (stage12 rhyme).
  Stage14 TTF thin-n then BNB wipe.
  Classic Ehlers BandPass (Cycle Analytics / Cybernetic Analysis second-order IIR centered on Period P with Bandwidth delta)
  isolates mid-band cycle and is explicitly used via zero crossings for cycle timing —
  denser responsive events than TTF thin seats / ER-gate / PGO,
  without SuperSmoother/FIR stage12 damp and without stage15 over-damp class.
  != Super Passband (stage7 park: dual-EMA diff + RMS).
  != Cyber Cycle (burned).
  != UO2025 dual-HP/RMS (stage15 EXIT).

Formula:
  beta = cos(2*pi / P)
  gamma = 1 / cos(4*pi*delta / P)
  alpha = gamma - sqrt(gamma^2 - 1)
  BP = 0.5 * (1 - alpha) * (price - price[2]) + beta * (1 + alpha) * BP[1] - alpha * BP[2]
  Prefer P=20, delta=0.3.

Mode A (BTC-LEAD PRIMARY dense zero — prefer first):
  long: crossover(bp, 0)
  exit: crossunder(bp, 0) or ATR stop.

Mode B (BNB-quiet / quality hold):
  long: crossover(bp, 0) and abs(bp) > epsilon (or bp quality hold)
  exit: crossunder(bp, 0) or ATR stop.
  (identical params across coins; only if Mode A over-whips BNB).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if P/delta inflated until BTC 6m 1H n collapses;
  Kill if SuperSmoother/Roofing grafted "to quiet BP";
  Kill if Super Passband substitute;
  Kill if Mode B forced while Mode A BTC n already healthy.
  Prefer Mode A (20, 0.3), 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill family if BTC clears >=1.2x then ETH wipes (stage13 REI pattern).
  Kill if P/delta retuned only on ETH; Kill if Cyber Cycle / Roofing graft.
  Prefer identical Mode A (20, 0.3) on ETH; retention n multi-dozen-class.

sol_smoke:
  Kill if Super Passband / Cyber Cycle / UO2025 labeled BandPass; 15m P=5 spam; stage12-15 grafts.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  BNB-after-BTC+ETH+SOL quiet-wipe (TTF lesson) CRITICAL:
  different (P, delta) than SOL; Mode B shorts ungated; no ATR; per-coin "BNB-only" lengthen.
  Prefer identical params; long-only; ATR exit.
  Kill family if BNB needs P != SOL to survive after 3-coin clear.

Forbidden: Super Passband; Cyber Cycle; Roofing/SS; UO2025 dual-HP; Spearman/CorrCycle/NET/DVI;
TTF/PFE/ASH/APZ/Nadaraya; stage12-13; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_bandpass

STRATEGY_ID = "ehlers-bandpass-zero"


@dataclass(frozen=True)
class BandpassParams:
    mode: str = "mode_a"  # "mode_a" (bp cross 0) | "mode_b" (bp cross 0 + quality hold)
    period: int = 20
    bandwidth: float = 0.3
    quality_threshold: float = 0.0  # Mode B threshold if used
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: BandpassParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period > 40:
        return False, f"btc_smoke: period={params.period} > 40 collapses BTC n"
    if params.period not in {14, 20, 28}:
        return False, f"btc_smoke: period={params.period} not in locked set {{14, 20, 28}}"
    if params.bandwidth not in {0.1, 0.3, 0.5}:
        return False, f"btc_smoke: bandwidth={params.bandwidth} not in locked set {{0.1, 0.3, 0.5}}"
    return True, "PASS"


def validate_eth_smoke(params: BandpassParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.period not in {14, 20, 28} or params.bandwidth not in {0.1, 0.3, 0.5}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: BandpassParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period <= 5:
        return False, "sol_smoke: 15m period<=5 forbidden (spam)"
    if params.period not in {14, 20, 28} or params.bandwidth not in {0.1, 0.3, 0.5}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: BandpassParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.period <= 0 or params.bandwidth <= 0.0:
        return False, "bnb_smoke: invalid parameters"
    if params.period > 40:
        return False, "bnb_smoke: period too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: BandpassParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-bandpass-zero."""
    params = params or BandpassParams()
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
    bp = ehlers_bandpass(closes, period=params.period, bandwidth=params.bandwidth)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(bp, zero_line, i)
        cross_dn = crossunder(bp, zero_line, i)

        if params.mode == "mode_b":
            # Mode B: require bp[i] > quality_threshold or |bp| hold
            bp_val = bp[i]
            if bp_val is None or bp_val <= params.quality_threshold:
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
