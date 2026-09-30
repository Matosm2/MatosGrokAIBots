"""wilder-swing-index-zero — Wilder Swing Index raw zero-cross with ATR proxy.

LOCKED ENCODE ORDER #4 (BTC LEAD PRIMARY — RAW SIGNED BAR STRENGTH ZERO-CROSS).
Thesis:
  Stage1 burned ASI dual-break (cumsum SI + price dual break).
  Raw Swing Index is a signed OHLC bar strength (-...+ ) that zero-crosses without cumulative lag
  or dual-structure gate — responsive majors density without stage12/15 over-damp and without stage13 CLV*SMA.
  Crypto has no exchange limit-move -> identical ATR proxy for T on all four coins.
  != ASI dual-break (cumsum ASI / trendline break).
  != CLV (Close Location Value).
  != BoP (Balance of Power).

Formula:
  N = (C - C1) + 0.5*(C - O) + 0.25*(C1 - O1)
  K = max(|H - C1|, |L - C1|)
  R from Wilder three-case largest excursion:
    diff_hc = |H - C1|, diff_lc = |L - C1|, diff_hl = H - L
    if diff_hc largest: R = diff_hc - 0.5*diff_lc + 0.25*(C1 - O1)
    elif diff_lc largest: R = diff_lc - 0.5*diff_hc + 0.25*(C1 - O1)
    else: R = diff_hl + 0.25*(C1 - O1)
  T = ta.atr(atrLen) proxy (guard R != 0 and T != 0)
  SI = 50 * (N / R) * (K / T)
  Prefer atrLen=14. Do not cumsum to ASI for Mode A.

Mode A (BTC-LEAD PRIMARY — prefer first):
  long: crossover(si, 0)
  exit: crossunder(si, 0) or ATR stop.

Mode B (BNB quiet):
  long: crossover(si, 0) and abs(si) > threshold (or SI SMA(3) cross 0)
  exit: crossunder(si, 0) or ATR stop.
  (identical params across coins; NOT ASI dual-break).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if T-proxy/smoothing inflated until BTC n collapses;
  Kill if Mode A becomes ASI dual-break (stage1);
  Kill if CLV substitute.
  Prefer Mode A SI*0 ATR14, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill if BTC clears then ETH wipes.
  Kill if T-proxy retuned only on ETH; Kill if ASI dual-break graft.
  Prefer identical ATR14 on ETH; retention n multi-dozen-class.

sol_smoke:
  Kill if ASI dual-break / CLV / BoP labeled SI-zero; 15m ATR=2 spam; stage12-15 grafts.
  Retention check: after ETH, SOL n multi-dozen-class on 6m 1H.

bnb_smoke:
  BNB-after-BTC+ETH+SOL quiet-wipe CRITICAL:
  different T-proxy than SOL; Mode B shorts ungated; no ATR exit; per-coin retune.
  Prefer identical params; long-only; ATR exit.

Forbidden: ASI dual-break / ASI trendline as Mode A; CLV*SMA; BoP;
Spearman/UO2025/CorrCycle/NET/DVI; TTF/PFE/ASH/APZ/Nadaraya; stage12-13; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, wilder_swing_index

STRATEGY_ID = "wilder-swing-index-zero"


@dataclass(frozen=True)
class SwingIndexParams:
    mode: str = "mode_a"  # "mode_a" (raw si cross 0) | "mode_b" (si quality/smooth)
    atr_len: int = 14
    quality_threshold: float = 0.0
    atr_trail_mult: float = 0.0


def validate_btc_smoke(params: SwingIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.atr_len > 30:
        return False, f"btc_smoke: atr_len={params.atr_len} > 30 collapses BTC n"
    if params.atr_len not in {10, 14, 20}:
        return False, f"btc_smoke: atr_len={params.atr_len} not in locked set {{10, 14, 20}}"
    return True, "PASS"


def validate_eth_smoke(params: SwingIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.atr_len not in {10, 14, 20}:
        return False, f"eth_smoke: atr_len={params.atr_len} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: SwingIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.atr_len <= 3:
        return False, "sol_smoke: 15m atr_len<=3 forbidden (spam)"
    if params.atr_len not in {10, 14, 20}:
        return False, f"sol_smoke: atr_len={params.atr_len} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: SwingIndexParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.atr_len <= 0:
        return False, "bnb_smoke: atr_len must be > 0"
    if params.atr_len > 30:
        return False, "bnb_smoke: atr_len too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: SwingIndexParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for wilder-swing-index-zero."""
    params = params or SwingIndexParams()
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
    si = wilder_swing_index(opens, highs, lows, closes, atr_len=params.atr_len)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(si, zero_line, i)
        cross_dn = crossunder(si, zero_line, i)

        if params.mode == "mode_b":
            si_val = si[i]
            if si_val is None or si_val <= params.quality_threshold:
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
