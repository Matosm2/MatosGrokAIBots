"""ehlers-uo2025-hpdiff-zero — Ehlers Ultimate Oscillator (2025) dual-HighPass / RMS zero-cross.

LOCKED ENCODE ORDER #2 (BNB-SURVIVAL CRITICAL + DUAL-HP BAND DAMP WITHOUT SS).
Thesis:
  Stage14 TTF BNB quiet-wipe + stage12 SS/FIR ban.
  Ehlers 2025 Ultimate Oscillator (TASC Apr 2025) is the difference of two HighPass filters divided by RMS —
  band-emphasis WITHOUT SuperSmoother (!= Roofing, != Cybernetic, != Elegant Osc, != Trendflex).
  != Larry Williams Ultimate Oscillator (burned UO).
  Dual-HP band damps BNB micro-noise while staying responsive on BTC/ETH majors.
  Close-only -> identical (BandEdge, Bandwidth) across coins.

Formula:
  HighPass(src, P):
    a1 = exp(-1.414 * pi / P)
    c2 = 2 * a1 * cos(1.414 * pi / P)
    c3 = -a1^2
    c1 = (1 + c2 - c3) / 4
    hp = c1*(src - 2*src[1] + src[2]) + c2*hp[1] + c3*hp[2]
  sig = HP(src, BandEdge * Bandwidth) - HP(src, BandEdge)
  rms = sqrt(sum(sig^2, 100) / 100)
  uo = sig / rms if rms != 0 else 0
  Prefer BandEdge=20, Bandwidth=2.

Mode A (BTC->ETH-PRIMARY dense zero — prefer first):
  long: crossover(uo, 0)
  exit: crossunder(uo, 0) or ATR stop.

Mode B (BNB-quiet / quality hold):
  long: crossover(uo, 0.5) (or quality hold)
  exit: crossunder(uo, 0) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if BandEdge/Bandwidth inflate until n collapses; Kill SS graft after HP; Kill Williams UO substitute.
  Prefer Mode A (20, 2), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears >=1.2x then ETH wipes; Kill params retuned only on ETH; Kill Roofing/SS substitute.
  Prefer identical (20, 2) on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if Williams UO / Roofing / SS labeled Ehlers-UO2025; 15m BandEdge=5 spam; stage12-14.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (BandEdge, Bandwidth); Mode B shorts ungated; no ATR; per-coin retune.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs params != SOL.

Forbidden: Williams UO; SuperSmoother/Roofing/Cybernetic/Elegant; TTF/PFE/ASH/APZ/Nadaraya; stage12-13; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_uo2025

STRATEGY_ID = "ehlers-uo2025-hpdiff-zero"


@dataclass(frozen=True)
class Uo2025Params:
    mode: str = "mode_a"  # "mode_a" (uo cross 0) | "mode_b" (uo cross 0.5 / quality)
    band_edge: int = 20
    bandwidth: float = 2.0
    quality_threshold: float = 0.5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: Uo2025Params, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.band_edge > 35:
        return False, f"btc_smoke: band_edge={params.band_edge} > 35 collapses BTC n"
    if params.band_edge not in {14, 20, 28}:
        return False, f"btc_smoke: band_edge={params.band_edge} not in locked set {{14, 20, 28}}"
    if params.bandwidth not in {1.4, 2.0, 2.5}:
        return False, f"btc_smoke: bandwidth={params.bandwidth} not in locked set {{1.4, 2.0, 2.5}}"
    return True, "PASS"


def validate_eth_smoke(params: Uo2025Params, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.band_edge not in {14, 20, 28} or params.bandwidth not in {1.4, 2.0, 2.5}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: Uo2025Params, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.band_edge <= 5:
        return False, "sol_smoke: 15m band_edge<=5 forbidden (spam)"
    if params.band_edge not in {14, 20, 28} or params.bandwidth not in {1.4, 2.0, 2.5}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: Uo2025Params, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.band_edge <= 0 or params.bandwidth <= 0.0:
        return False, "bnb_smoke: invalid parameters"
    if params.band_edge > 35:
        return False, "bnb_smoke: band_edge too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: Uo2025Params | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-uo2025-hpdiff-zero."""
    params = params or Uo2025Params()
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
    uo, _ = ehlers_uo2025(closes, band_edge=params.band_edge, bandwidth=params.bandwidth)

    zero_line = [0.0] * n
    qual_line = [params.quality_threshold] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_a":
            cross_up = crossover(uo, zero_line, i)
            cross_dn = crossunder(uo, zero_line, i)
        else:  # mode_b: quality threshold cross
            cross_up = crossover(uo, qual_line, i)
            cross_dn = crossunder(uo, zero_line, i)

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
