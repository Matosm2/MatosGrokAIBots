"""katsanos-vfi-zero-cross — Markos Katsanos Volume Flow Indicator zero cross.

LOCKED ENCODE ORDER #4 — PRIORITY KILL IF BTC CHOP (stage20 volume rhyme).
Thesis:
  Stage21 0 BTC; remaining public non-clone seats scarce.
  VFI (Katsanos, S&C June 2004) = capped directional volume / avg volume
  with volatility cutoff.
  Formula:
    tp = (h + l + c) / 3
    inter = log(tp) - log(tp[1])
    cutoff = coef * stdev(inter, 30) * close
    vave = sma(volume, period)[1]
    vc = min(volume, vave * vcoef)
    vcp = +vc if mf > cutoff else (-vc if mf < -cutoff else 0)
    vfiRaw = sum(vcp, period) / vave
    vfi = ema(vfiRaw, smooth)
  Mode A:
    long crossover(vfi, 0)
    exit crossunder(vfi, 0)
  Mode B:
    require vfi > sma(vfi, sigLen) — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (80, 0.1, 2.5, 3) Mode A intraday.
  != VPCI / != VZO / != BW-MFI / != Demand Index / != OBV.

EARLY-KILL RULE:
  After BTC smoke: if Mode A BTC 0 / chop under costs like stage20 VPCI/BW-MFI/DI
  -> DROP #4 immediately; do not expand sweep / do not promote ladder.

btc_smoke:
  CRITICAL + stage20 volume-chop risk: Kill Mode A BTC 0/chop;
  Kill period inflate until n collapses; Kill VPCI/VZO/OBV/DI substitute.
  Prefer Mode A (80,0.1,2.5,3), 1H+. Priority kill if volume-chop rhyme.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill period retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m period=20; stage12-21 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill period retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR.

Forbidden: VPCI/VZO/BW-MFI/DI/OBV labeled VFI; ungated OBV; request.security; stage12-21 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, katsanos_vfi, sma

STRATEGY_ID = "katsanos-vfi-zero-cross"


@dataclass(frozen=True)
class VfiParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    period: int = 80      # 50, 80
    coef: float = 0.1     # 0.1, 0.2
    vcoef: float = 2.5    # 2.5
    smooth: int = 3       # 3
    sig_len: int = 10     # Mode B signal SMA length
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: VfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period not in {50, 80}:
        return False, f"btc_smoke: period={params.period} not in locked sweep {{50, 80}}"
    if params.coef not in {0.1, 0.2}:
        return False, f"btc_smoke: coef={params.coef} not in locked sweep {{0.1, 0.2}}"
    if params.period > 130:
        return False, f"btc_smoke: period={params.period} collapses BTC n (over-damp)"
    return True, "PASS"


def validate_eth_smoke(params: VfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.period not in {50, 80} or params.coef not in {0.1, 0.2}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.period <= 20:
        return False, "sol_smoke: 15m period<=20 forbidden (spam)"
    if params.period not in {50, 80} or params.coef not in {0.1, 0.2}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: VfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.period not in {50, 80} or params.coef not in {0.1, 0.2}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VfiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for katsanos-vfi-zero-cross."""
    params = params or VfiParams()
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
    vfi_vals = katsanos_vfi(
        highs,
        lows,
        closes,
        volumes,
        period=params.period,
        coef=params.coef,
        vcoef=params.vcoef,
        smooth=params.smooth,
    )

    sig_vals: list[float | None] = [None] * n
    if params.mode == "mode_b":
        valid_vfi = [0.0 if x is None else float(x) for x in vfi_vals]
        sig_vals = sma(valid_vfi, params.sig_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        vfi_cur = vfi_vals[i]
        vfi_prev = vfi_vals[i - 1]

        if not in_pos:
            # crossover(vfi, 0)
            if vfi_cur is not None and vfi_prev is not None:
                cross_up = (vfi_prev <= 0.0) and (vfi_cur > 0.0)
                if params.mode == "mode_b":
                    sig = sig_vals[i]
                    if sig is None or vfi_cur <= sig:
                        cross_up = False
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

            # exit crossunder(vfi, 0)
            cross_down = False
            if vfi_cur is not None and vfi_prev is not None:
                cross_down = (vfi_prev >= 0.0) and (vfi_cur < 0.0)

            exit_trigger = stop_hit or cross_down
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
