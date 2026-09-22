"""blau-csi-ergodic-signal-cross-v1 — Blau Candlestick Index Ergodic × signal-line cross.

LOCKED ENCODE ORDER #1 (BNB-SURVIVAL-CRITICAL + DENSITY: SOL + BNB survival).
Thesis:
  Stage11 wiped Pee TDI Direction (BNB -1.263x after SOL) and TrendScore. Blau CSI normalizes
  triple-smoothed (Close - Open) by triple-smoothed (HH - LL) — candlestick body/range polarity
  != TSI (close-close), != BoP single-bar, != RVI, != Pee Direction sum-mom.
  Ergodic CSI x short EMA signal is dense on 1H; OHLC-only -> majors-liquid portable to quieter
  BNB with identical (q, r, s, u, ul). BNB-survival-CRITICAL: triple EMA damp + signal-cross
  (not raw zero) reduces quiet-BNB micro-flips vs ungated Direction-zero.

Formula:
  cmtm = close - open[q-1]
  rng = ta.highest(high, q) - ta.lowest(low, q)
  num = ema(ema(ema(cmtm, r), s), u)
  den = ema(ema(ema(rng, r), s), u)
  csi = den != 0 ? 100 * num / den : 0
  sig = ema(csi, ul)
  Defaults: q=1, r=20, s=5, u=3, ul=3.

Mode A (prefer / dense Ergodic x signal):
  long: crossover(csi, sig)
  exit: crossunder(csi, sig) or ATR stop.

Mode B (BNB-quiet quality):
  long: crossover(csi, sig) and csi > 0
  exit: crossunder(csi, sig) or csi < 0 or ATR stop.
  (identical Mode across coins).

sol_smoke:
  Kill if: TSI/BoP/RVI/Pee TDI labeled CSI; 15m r=3 spam; ER/AO/PGO graft.
  Prefer Mode A (20, 3), 1H+.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  BNB-after-SOL kill (CRITICAL): different (r, ul) than SOL; Mode B only on BNB while SOL Mode A;
  no ATR; volume graft. Prefer identical params; long-only; ATR exit.
  Kill if BNB needs larger r than SOL.

Forbidden: TSI/SMI/BoP/RVI substitute; Pee TDI/Direction; TrendScore; ER-gate; AO/ROC/WMA/PGO; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, blau_csi_ergodic, crossover, crossunder

STRATEGY_ID = "blau-csi-ergodic-signal-cross-v1"


@dataclass(frozen=True)
class BlauCsiParams:
    mode: str = "mode_a"  # "mode_a" (csi cross sig) | "mode_b" (csi cross sig and csi > 0)
    q: int = 1
    r: int = 20
    s: int = 5
    u: int = 3
    ul: int = 3
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: BlauCsiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.r <= 3:
        return False, "sol_smoke: 15m r<=3 forbidden (spam)"
    if (params.r, params.ul) not in {(20, 3), (14, 3), (25, 3), (20, 5)}:
        return False, f"sol_smoke: (r,ul)=({params.r},{params.ul}) not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: BlauCsiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after SOL)."""
    if params.r <= 0 or params.ul <= 0:
        return False, "bnb_smoke: r and ul must be > 0"
    if params.r > 50:
        return False, "bnb_smoke: r too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: BlauCsiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for blau-csi-ergodic-signal-cross-v1."""
    params = params or BlauCsiParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    csi, sig = blau_csi_ergodic(
        opens,
        highs,
        lows,
        closes,
        q=params.q,
        r=params.r,
        s=params.s,
        u=params.u,
        ul=params.ul,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]
        curr_csi = csi[i]
        curr_sig = sig[i]

        cross_up = crossover(csi, sig, i)
        cross_dn = crossunder(csi, sig, i)

        if not in_pos:
            entry_cond = cross_up
            if params.mode == "mode_b":
                entry_cond = entry_cond and (curr_csi is not None and curr_csi > 0.0)

            if entry_cond:
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

            exit_cond = cross_dn
            if params.mode == "mode_b":
                exit_cond = exit_cond or (curr_csi is not None and curr_csi < 0.0)

            if stop_hit or exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
