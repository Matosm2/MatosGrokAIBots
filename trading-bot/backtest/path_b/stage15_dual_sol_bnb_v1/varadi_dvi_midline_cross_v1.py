"""varadi-dvi-midline-cross — Varadi DV Intermediate Oscillator midline-0.5 cross.

LOCKED ENCODE ORDER #5 (OPTIONAL 5TH SEAT — MAGNITUDE + STRETCH VOTE FOR BNB DAMP).
Thesis:
  Stage14 TTF quiet-BNB death; need vote/stretch damp without SS.
  Varadi DVI blends smoothed return magnitude + up/down-bar stretch then percent-rank —
  Mode A = DVI cross 0.5 (trend when composite rank elevated).
  Stretch vote may hold quieter BNB with fewer micro-flips than TTF zero;
  explicit thin-n watch on BTC if n too large (stage12 rhyme).
  != PSY/RMI/TII raw midline-50 (distinct percent-rank composite construction);
  != Dorsey RelVol; != TTF.
  Close-only -> identical params across all coins.

Formula:
  r = close / SMA(close, 3) - 1
  mag = SMA((SMA(r, 5) + SMA(r, 100) / 10) / 2, 5)
  b = +-1 by up/down bar
  str = SMA((runSum(b, 10) + runSum(b, 100) / 10) / 2, 2)
  dvi = mag_weight * PercentRank(mag, n) + str_weight * PercentRank(str, n)
  (scaled 0..1, midline 0.5)
  Prefer n=168, mag_weight=0.8, str_weight=0.2.

Mode A (BTC->ETH-PRIMARY dense midline — prefer first):
  long: crossover(dvi, 0.5)
  exit: crossunder(dvi, 0.5) or ATR stop.

Mode B (BNB-quiet / stretch-heavier):
  long: crossover(dvi, 0.55) (or stretch-heavier wts=(0.6, 0.4))
  exit: crossunder(dvi, 0.5) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if n/wts/smoothing inflate until BTC trade count collapses (thin-n risk);
  Kill SMA200 CSS graft; Kill Mode B forced while Mode A already thin.
  Prefer Mode A n=168, 1H+. Explicit thin-n watch.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears >=1.2x then ETH wipes; Kill n/wts retuned only on ETH; Kill PSY midline-50 substitute.
  Prefer identical params on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if PSY/RMI/TII/Dorsey labeled DVI; 15m n=20 spam; stage12-14.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different n/wts; Mode B shorts ungated; no ATR; SMA200 graft; per-coin retune.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs params != SOL.

Forbidden: PSY/RMI/TII labeled DVI; SMA200 CSS graft; TTF/PFE/ASH/APZ/Nadaraya; stage12 SS; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, varadi_dvi

STRATEGY_ID = "varadi-dvi-midline-cross"


@dataclass(frozen=True)
class VaradiDviParams:
    mode: str = "mode_a"  # "mode_a" (dvi cross 0.5) | "mode_b" (dvi cross 0.55 / stretch-heavier)
    n: int = 168
    mag_weight: float = 0.8
    str_weight: float = 0.2
    entry_threshold: float = 0.5
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: VaradiDviParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n > 300:
        return False, f"btc_smoke: n={params.n} > 300 collapses BTC trade count"
    if params.n not in {100, 168, 252}:
        return False, f"btc_smoke: n={params.n} not in locked set {{100, 168, 252}}"
    if (params.mag_weight, params.str_weight) not in {(0.8, 0.2), (0.6, 0.4)}:
        return False, "btc_smoke: weights not in locked set"
    return True, "PASS"


def validate_eth_smoke(params: VaradiDviParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.n not in {100, 168, 252} or (params.mag_weight, params.str_weight) not in {(0.8, 0.2), (0.6, 0.4)}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VaradiDviParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.n <= 20:
        return False, "sol_smoke: 15m n<=20 forbidden (spam)"
    if params.n not in {100, 168, 252} or (params.mag_weight, params.str_weight) not in {(0.8, 0.2), (0.6, 0.4)}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: VaradiDviParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.n <= 0 or params.mag_weight < 0.0 or params.str_weight < 0.0:
        return False, "bnb_smoke: invalid parameters"
    if params.n > 300:
        return False, "bnb_smoke: n too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VaradiDviParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for varadi-dvi-midline-cross."""
    params = params or VaradiDviParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    dvi, _, _ = varadi_dvi(
        closes,
        n=params.n,
        mag_weight=params.mag_weight,
        str_weight=params.str_weight,
    )

    mid_line = [0.5] * count
    entry_line = [params.entry_threshold if params.mode == "mode_b" else 0.5] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(dvi, entry_line, i)
        cross_dn = crossunder(dvi, mid_line, i)

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
