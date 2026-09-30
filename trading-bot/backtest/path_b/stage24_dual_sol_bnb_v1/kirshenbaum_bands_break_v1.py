"""kirshenbaum-bands-break — Kirshenbaum Bands EMA mid ± k·LinReg stderr break.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage23 ATR-corridor near-miss / 0 BTC — need statistical band-break that can
  clear BTC trends without cloning BB / STARC / percentile / SEB.
  Kirshenbaum Bands (Paul Kirshenbaum):
    mid = ta.ema(close, emaLen)
    LinReg residual stderr over regLen
    upper = mid + k * stderr
    lower = mid - k * stderr
  Mid MUST be EMA — kill if LinReg mid (SEB).
  Mode A:
    long crossover(close, upper)
    exit crossunder(close, mid)
  Mode B:
    require stderr percentrank > sMin — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (20, 20, 1.75) Mode A.
  != Bollinger (stdev vs stderr) / != SEB (LinReg mid) / != STARC.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x;
  Kill k/emaLen inflate until n collapses;
  Kill BB/SEB/LinReg-mid/STARC substitute. Prefer Mode A (20,20,1.75), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH;
  Kill LinReg-mid labeled Kirshenbaum. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill emaLen/k retuned only on SOL;
  BB/percentile graft; stage12-23 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: LinReg-as-mid (SEB); BB stdev substitute; STARC/Keltner/percentile;
request.security; stage12-23 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, kirshenbaum_bands, percentrank

STRATEGY_ID = "kirshenbaum-bands-break"


@dataclass(frozen=True)
class KirshenbaumParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    ema_len: int = 20           # 20, 30
    reg_len: int = 20           # 20 (locked)
    k: float = 1.75             # 1.75, 2.25
    s_min: float = 50.0         # Mode B stderr percentrank min (e.g. 50.0)
    pr_len: int = 50
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: KirshenbaumParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.ema_len not in {20, 30}:
        return False, f"btc_smoke: ema_len={params.ema_len} not in {{20, 30}}"
    if params.reg_len != 20:
        return False, f"btc_smoke: reg_len={params.reg_len} != 20"
    if params.k not in {1.75, 2.25}:
        return False, f"btc_smoke: k={params.k} not in {{1.75, 2.25}}"
    return True, "PASS"


def validate_eth_smoke(params: KirshenbaumParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.ema_len not in {20, 30} or params.reg_len != 20 or params.k not in {1.75, 2.25}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: KirshenbaumParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.ema_len not in {20, 30} or params.reg_len != 20 or params.k not in {1.75, 2.25}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: KirshenbaumParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.ema_len not in {20, 30} or params.reg_len != 20 or params.k not in {1.75, 2.25}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KirshenbaumParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for kirshenbaum-bands-break."""
    params = params or KirshenbaumParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    upper, mid, lower, stderr_series = kirshenbaum_bands(
        closes, ema_len=params.ema_len, reg_len=params.reg_len, k=params.k
    )

    stderr_clean = [s if s is not None else 0.0 for s in stderr_series]
    stderr_pr = percentrank(stderr_clean, params.pr_len)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        cp = closes[i - 1]
        h = highs[i]

        cur_u = upper[i]
        prev_u = upper[i - 1]
        cur_m = mid[i]
        prev_m = mid[i - 1]

        if not in_pos:
            # Entry: crossover(close, upper)
            if cur_u is not None and prev_u is not None:
                cross_up = (cp <= prev_u) and (c > cur_u)
                if cross_up:
                    can_enter = True
                    if params.mode == "mode_b":
                        pr = stderr_pr[i]
                        if pr is None or pr < params.s_min:
                            can_enter = False
                    if can_enter:
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

            # Exit: crossunder(close, mid)
            cross_exit = False
            if cur_m is not None and prev_m is not None:
                cross_exit = (cp >= prev_m) and (c < cur_m)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
