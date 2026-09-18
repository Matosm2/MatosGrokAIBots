"""nison-kagi-yang-yin-flip — Nison Kagi chart Yang/Yin reversal structure flip.

LOCKED ENCODE ORDER #5 (OPTIONAL 5TH SEAT — REVERSAL AMOUNT STRUCTURE FLIP).
Thesis:
  Twin structure seat to Three Line Break but reversal-amount based (Nison/StockCharts Kagi):
  continue line with close;
  reverse direction when close moves against current leg by >= R;
  Yang (thick line) when rising line breaks prior peak;
  Yin (thin line) when falling line breaks prior trough.
  Mode A = buy new Yang (Yin->Yang flip) / exit on new Yin (Yang->Yin flip).
  No smoother / rank / dual-HP — responsive structure density for BTC lead;
  identical R on all four coins.
  != 3LB (break of N prior lines vs breakout of prior peak/trough).
  != Donchian channel break.
  != Range Filter flip.
  != Renko (brick size) if R is ATR/pct of close path.

Formula:
  var Kagi state (direction, extreme, prior_peak, prior_trough, yang_yin) on closed close.
  Reverse when adverse move >= R.
  Yang when up-line breaks prior peak; Yin when down-line breaks prior trough.
  Prefer R = 1.0 * ATR(14).

Mode A (BTC-LEAD PRIMARY — prefer first):
  long on Yin->Yang flip;
  exit on Yang->Yin flip (or ATR stop).

Mode B (BNB quiet):
  larger R (e.g. 1.5 * ATR or 2%) — only if Mode A over-whips;
  identical R across coins.

btc_smoke:
  BTC-LEAD CRITICAL: Kill if R inflated until BTC flips collapse;
  Kill if Mode B forced while Mode A BTC already healthy;
  Kill if Donchian substitute.
  Prefer Mode A ATR*1, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill if BTC clears then ETH wipes.
  Kill if R retuned only on ETH; Kill if 3LB/Donchian substitute.
  Prefer identical R on ETH; retention n multi-dozen-class.

sol_smoke:
  Kill if Renko / Donchian / 3LB labeled Kagi; 15m R=0.1% spam; stage12-15 grafts.
  Retention check: after ETH, SOL n multi-dozen-class on 6m 1H.

bnb_smoke:
  BNB-after-BTC+ETH+SOL quiet-wipe CRITICAL:
  different R than SOL; Mode B shorts ungated; no ATR exit; per-coin retune.
  Prefer identical params; long-only; ATR exit.

Forbidden: Donchian; 3LB mislabel; RangeFilter; Renko mislabel;
MTF Kagi via request.security; stage12-15 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, nison_kagi

STRATEGY_ID = "nison-kagi-yang-yin-flip"


@dataclass(frozen=True)
class KagiParams:
    mode: str = "mode_a"  # "mode_a" (ATR*1 standard) | "mode_b" (ATR*1.5 quiet)
    atr_mult: float = 1.0
    atr_len: int = 14
    pct_reversal: float | None = None
    atr_trail_mult: float = 0.0


def validate_btc_smoke(params: KagiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.atr_mult > 3.0:
        return False, f"btc_smoke: atr_mult={params.atr_mult} > 3.0 collapses BTC n"
    if params.atr_mult not in {0.75, 1.0, 1.5}:
        return False, f"btc_smoke: atr_mult={params.atr_mult} not in locked set {{0.75, 1.0, 1.5}}"
    return True, "PASS"


def validate_eth_smoke(params: KagiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.atr_mult not in {0.75, 1.0, 1.5}:
        return False, f"eth_smoke: atr_mult={params.atr_mult} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: KagiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.atr_mult <= 0.2:
        return False, "sol_smoke: 15m atr_mult<=0.2 forbidden (spam)"
    if params.atr_mult not in {0.75, 1.0, 1.5}:
        return False, f"sol_smoke: atr_mult={params.atr_mult} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: KagiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.atr_mult <= 0.0:
        return False, "bnb_smoke: atr_mult must be > 0"
    if params.atr_mult > 3.0:
        return False, "bnb_smoke: atr_mult too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KagiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for nison-kagi-yang-yin-flip."""
    params = params or KagiParams()
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
    _, _, yang_flips, yin_flips = nison_kagi(
        closes,
        highs=highs,
        lows=lows,
        atr_mult=params.atr_mult,
        atr_len=params.atr_len,
        pct_reversal=params.pct_reversal,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        y_entry = yang_flips[i]
        y_exit = yin_flips[i]

        if not in_pos:
            if y_entry:
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

            if stop_hit or y_exit:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
