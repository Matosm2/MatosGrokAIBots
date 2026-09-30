"""blau-ergodic-mdi-signal-cross — Blau Ergodic Mean Deviation Index MDI x Signal.

LOCKED ENCODE ORDER #2 (BTC LEAD PRIMARY).
Thesis:
  Stage16 oscillators (BandPass/HP/SI) chopped; CSI Ergodic x signal stage12 over-damped BTC.
  Ergodic MDI is a distinct Blau mean-deviation family:
  md = price - EMA(price, r)
  Ergodic_MDI = EMA(EMA(md, s), u)
  signal = EMA(Ergodic_MDI, ul)
  Mode A = MDI x signal cross (optional zero bias).
  Intended denser majors+SOL participation without CSI/TSI EXIT class and without Kagi SOL stall.
  != stage12 blau-csi-ergodic-signal-cross.
  != burned TSI / Ergodic-TSI.

Formula:
  md = close - ema(close, r)
  mdi = ema(ema(md, s), u)
  sig = ema(mdi, ul)
  Prefer (20, 5, 3, 3).

Mode A (BTC-LEAD PRIMARY — prefer):
  long: crossover(mdi, sig)
  exit: crossunder(mdi, sig)

Mode B (BNB quiet / Mode A+ zero-bias):
  long: crossover(mdi, sig) and mdi > 0 (Mode A+ zero-bias)
  exit: crossunder(mdi, sig)

btc_smoke:
  BTC-LEAD CRITICAL: Kill if (r, s, u) inflated until BTC n collapses;
  Kill if CSI/TSI substitute;
  Kill if Mode B forced while Mode A BTC healthy. Prefer Mode A (20, 5, 3, 3), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill BTC-clear->ETH-wipe;
  Kill params retuned only on ETH; Kill CSI graft.
  Prefer identical; ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  Kill CSI/TSI/BandPass labeled MDI; 15m r=5 spam; stage12-16 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different (r, s, u, ul); Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: CSI / TSI / Ergodic-TSI labeled MDI; Spearman/UO2025/CorrCycle/NET/DVI;
BandPass/HP/3LB/SI/Kagi; stage12-16.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, blau_ergodic_mdi, crossover, crossunder

STRATEGY_ID = "blau-ergodic-mdi-signal-cross"


@dataclass(frozen=True)
class BlauMdiParams:
    mode: str = "mode_a"  # "mode_a" (mdi x sig) | "mode_b" (mdi x sig + mdi > 0 bias)
    r: int = 20
    s: int = 5
    u: int = 3
    ul: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: BlauMdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.r not in {14, 20, 28}:
        return False, f"btc_smoke: r={params.r} not in locked set {{14, 20, 28}}"
    if params.s not in {3, 5}:
        return False, f"btc_smoke: s={params.s} not in locked set {{3, 5}}"
    if params.ul not in {3, 5}:
        return False, f"btc_smoke: ul={params.ul} not in locked set {{3, 5}}"
    if params.r > 35:
        return False, f"btc_smoke: r={params.r} > 35 collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: BlauMdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH CRITICAL)."""
    if params.r not in {14, 20, 28} or params.s not in {3, 5} or params.ul not in {3, 5}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: BlauMdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and params.r <= 5:
        return False, "sol_smoke: 15m r<=5 forbidden (spam)"
    if params.r not in {14, 20, 28} or params.s not in {3, 5} or params.ul not in {3, 5}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: BlauMdiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.r not in {14, 20, 28} or params.s not in {3, 5} or params.ul not in {3, 5}:
        return False, "bnb_smoke: params retuned away from locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: BlauMdiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for blau-ergodic-mdi-signal-cross."""
    params = params or BlauMdiParams()
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
    mdi, sig = blau_ergodic_mdi(closes, r=params.r, s=params.s, u=params.u, ul=params.ul)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(mdi, sig, i)
        cross_dn = crossunder(mdi, sig, i)

        if params.mode == "mode_b":
            # Mode B / Mode A+: require mdi > 0 on entry
            mdi_val = mdi[i]
            if mdi_val is None or mdi_val <= 0.0:
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
