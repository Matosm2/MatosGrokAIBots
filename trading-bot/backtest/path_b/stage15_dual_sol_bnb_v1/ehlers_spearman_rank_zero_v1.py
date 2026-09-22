"""ehlers-spearman-rank-zero — Ehlers Spearman Rank Correlation zero-cross.

LOCKED ENCODE ORDER #1 (BNB-SURVIVAL CRITICAL + BTC->ETH PORTABILITY PRESERVED).
Thesis:
  Stage14 TTF cleared BTC->ETH->SOL (2.257x) then BNB quiet-wiped (0.093x); TTF seats were thin (n=6-10).
  Ehlers Spearman Rank (TASC Jul 2020) is a rank-order correlation of closes vs time ranks in [-1, +1] —
  != CTI Pearson dual-thr, != CMO, != TTF.
  Rank transform damps BNB micro-flips without SuperSmoother/FIR stage12 damp.
  Mode A locks rho zero-cross for BTC+ETH clearing density; Mode B = quality hold (rho > 0.2 after cross)
  only if Mode A over-whips BNB — identical L across coins.

Formula:
  Rank closes over L:
    d_i = time_rank - price_rank
    rho = 1 - 6 * sum(d^2) / (L * (L^2 - 1))
    sig = 2 * rho - 1
  Prefer L=20.

Mode A (BTC->ETH-PRIMARY dense zero — prefer first):
  long: crossover(rho, 0)
  exit: crossunder(rho, 0) or ATR stop.

Mode B (BNB-quiet / quality hold):
  long: crossover(rho, 0) and rho > 0.2 (or rho cross 0.2)
  exit: crossunder(rho, 0) or ATR stop.
  (identical L across coins).

btc_smoke:
  BTC-LEAD CRITICAL: Kill L >> 28 n collapse; Kill SS/NET graft "to quiet"; Kill Mode B forced while Mode A BTC healthy.
  Prefer Mode A L=20, 1H+.

eth_smoke:
  BTC->ETH CRITICAL: Kill if BTC clears >=1.2x then ETH wipes (stage13 REI pattern); Kill if L or Mode retuned only on ETH; Kill if CTI Pearson graft.
  Prefer identical Mode A L=20 on ETH after BTC; ETH n multi-dozen.

sol_smoke:
  Kill if CTI/CMO/TTF labeled Spearman; 15m L=5 spam; ER/AO/PGO/stage12-14.
  Retention check: after ETH, SOL n must stay multi-dozen-class on 6m 1H.

bnb_smoke:
  CRITICAL after BTC+ETH+SOL (TTF lesson): different L; Mode B shorts ungated; no ATR; BNB-only lengthen.
  Prefer identical params; long-only; ATR exit. Kill if BNB needs L != SOL.

Forbidden: CTI dual-thr; CMO/TTF/PFE/ASH/APZ/Nadaraya; SS/Roofing; REI/PZO/TMO/RF/CLV; stage12 duals; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_spearman

STRATEGY_ID = "ehlers-spearman-rank-zero"


@dataclass(frozen=True)
class SpearmanRankParams:
    mode: str = "mode_a"  # "mode_a" (rho cross 0) | "mode_b" (rho cross 0.2 / quality)
    length: int = 20
    quality_threshold: float = 0.2
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: SpearmanRankParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length > 35:
        return False, f"btc_smoke: L={params.length} > 35 collapses BTC n"
    if params.length not in {14, 20, 28}:
        return False, f"btc_smoke: L={params.length} not in locked set {{14, 20, 28}}"
    return True, "PASS"


def validate_eth_smoke(params: SpearmanRankParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (CRITICAL after BTC)."""
    if params.length not in {14, 20, 28}:
        return False, f"eth_smoke: L={params.length} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: SpearmanRankParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.length <= 5:
        return False, "sol_smoke: 15m L<=5 forbidden (spam)"
    if params.length not in {14, 20, 28}:
        return False, f"sol_smoke: L={params.length} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: SpearmanRankParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.length <= 0:
        return False, "bnb_smoke: length must be > 0"
    if params.length > 35:
        return False, "bnb_smoke: length too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: SpearmanRankParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-spearman-rank-zero."""
    params = params or SpearmanRankParams()
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
    rho, _ = ehlers_spearman(closes, length=params.length)

    zero_line = [0.0] * n
    qual_line = [params.quality_threshold] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        if params.mode == "mode_a":
            cross_up = crossover(rho, zero_line, i)
            cross_dn = crossunder(rho, zero_line, i)
        else:  # mode_b: quality threshold rho > 0.2
            cross_up = crossover(rho, qual_line, i)
            cross_dn = crossunder(rho, zero_line, i)

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
