"""ehlers-net-myrsi-zero — Ehlers Noise Elimination Technology on MyRSI zero-cross.

LOCKED ENCODE ORDER #4 (BNB-SURVIVAL CRITICAL + KENDALL CONCORDANCE NOISE STRIP).
Thesis:
  Stage2 burned CMO-zero; stage14 burned ASH; Wilder RSI burned.
  Ehlers MyRSI = (CU - CD) / (CU + CD) in [-1, +1] is CMO-class raw — forbidden as Mode A alone.
  Path-B Mode A locks NET(MyRSI) — Kendall concordance of MyRSI vs time-slope — nonlinear noise strip
  WITHOUT laggy FIR/SS.
  Designed to clarify noisy vote oscillators -> damps BNB micro-flips after SOL clear while keeping
  denser majors trade count than TTF thin seats.
  Identical (rsi_length, net_length) across all coins.

Formula:
  MyRSI:
    CU = sum of up deltas over rsi_length
    CD = sum of down deltas over rsi_length
    my = (CU - CD) / (CU + CD) if (CU + CD) != 0 else 0
  NET:
    Kendall concordance of MyRSI vs time-slope over net_length:
    net = sum_{i<j} sign(X[j] - X[i]) / (0.5 * N * (N - 1))
  Prefer (rsi_length=14, net_length=14).

Mode A (BTC->ETH-PRIMARY dense zero — prefer first):
  long: crossover(net, 0)
  exit: crossunder(net, 0) or ATR stop.

Mode B (BNB-quiet / quality hold):
  long: crossover(net, 0.2)
  exit: crossunder(net, 0) or ATR stop.
  (identical params across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if lengths raised into stage12-damp until BTC n collapses;
  Kill Mode A as raw CMO/MyRSI zero (stage2 burn); Kill SS graft.
  Prefer Mode A (14, 14), 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears >=1.2x then ETH wipes; Kill lengths retuned only on ETH; Kill Wilder RSI OB/OS.
  Prefer identical (14, 14) on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if CMO/RSI/ASH labeled NET-MyRSI; 15m length=3 spam; stage12-14.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL: different (rsi_length, net_length); Mode B shorts ungated; no ATR; per-coin retune.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs params != SOL.

Forbidden: Raw MyRSI/CMO/Wilder RSI zero as Mode A; SS/Laguerre "instead of NET"; TTF/PFE/ASH/APZ/Nadaraya; stage12-13; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_net_myrsi

STRATEGY_ID = "ehlers-net-myrsi-zero"


@dataclass(frozen=True)
class NetMyRsiParams:
    mode: str = "mode_a"  # "mode_a" (net cross 0) | "mode_b" (net cross 0.2 / quality)
    rsi_length: int = 14
    net_length: int = 14
    quality_threshold: float = 0.2
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: NetMyRsiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.rsi_length > 30 or params.net_length > 30:
        return False, "btc_smoke: lengths > 30 collapse BTC n"
    if params.rsi_length not in {10, 14, 20} or params.net_length not in {10, 14, 20}:
        return False, "btc_smoke: lengths not in locked set {10, 14, 20}"
    return True, "PASS"


def validate_eth_smoke(params: NetMyRsiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.rsi_length not in {10, 14, 20} or params.net_length not in {10, 14, 20}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: NetMyRsiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and (params.rsi_length <= 3 or params.net_length <= 3):
        return False, "sol_smoke: 15m length<=3 forbidden (spam)"
    if params.rsi_length not in {10, 14, 20} or params.net_length not in {10, 14, 20}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: NetMyRsiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.rsi_length <= 0 or params.net_length <= 0:
        return False, "bnb_smoke: invalid parameters"
    if params.rsi_length > 30 or params.net_length > 30:
        return False, "bnb_smoke: lengths too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: NetMyRsiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-net-myrsi-zero."""
    params = params or NetMyRsiParams()
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
    net, _ = ehlers_net_myrsi(closes, rsi_length=params.rsi_length, net_length=params.net_length)

    zero_line = [0.0] * n
    qual_line = [params.quality_threshold] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_a":
            cross_up = crossover(net, zero_line, i)
            cross_dn = crossunder(net, zero_line, i)
        else:  # mode_b: quality threshold cross
            cross_up = crossover(net, qual_line, i)
            cross_dn = crossunder(net, zero_line, i)

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
