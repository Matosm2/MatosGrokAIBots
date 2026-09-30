"""nhnl-oscillator-zero — Single-asset New-High / New-Low rolling oscillator zero-cross.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage24 0-BTC / 1.113x near-miss — need published single-asset new-high vs new-low
  rate that can clear BTC without cloning HHLL structure-flip / Donchian / Aroon.
  NHNL (single-symbol):
    Over lookback L:
      isNH = high >= highest(high, L)[1]
      isNL = low <= lowest(low, L)[1]
    Over window W:
      nhRate = sum(isNH, W)
      nlRate = sum(isNL, W)
      osc = nhRate - nlRate
  Mode A:
    long crossover(osc, 0)
    exit crossunder(osc, 0)
  Mode B:
    require osc > thr (thr in {1.0, 2.0}) — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (L=20, W=10) Mode A.
  != HHLL (confirmed pivot BOS) / != Donchian (channel break) / != Aroon / != percentile.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x / ~1.113x;
  Kill L/W inflate until n collapses;
  Kill HHLL/Donchian/Aroon/percentile labeled NHNL. Prefer Mode A (20,10), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill L/W retuned only on SOL;
  15m L=5 spam; stage12-24 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe (HHLL rhyme — watch); Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: HHLL/pivot-BOS/Donchian/Aroon/breadth multi-name labeled NHNL;
request.security; stage12-24 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, nhnl_osc

STRATEGY_ID = "nhnl-oscillator-zero"


@dataclass(frozen=True)
class NhnlParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    l: int = 20                 # 14, 20, 30
    w: int = 10                 # 5, 10, 14
    thr: float = 1.0            # Mode B entry thr: 1.0, 2.0
    atr_trail_mult: float = 0.0 # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: NhnlParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.l not in {14, 20, 30}:
        return False, f"btc_smoke: l={params.l} not in {{14, 20, 30}}"
    if params.w not in {5, 10, 14}:
        return False, f"btc_smoke: w={params.w} not in {{5, 10, 14}}"
    return True, "PASS"


def validate_eth_smoke(params: NhnlParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.l not in {14, 20, 30} or params.w not in {5, 10, 14}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: NhnlParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.l not in {14, 20, 30} or params.w not in {5, 10, 14}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: NhnlParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.l not in {14, 20, 30} or params.w not in {5, 10, 14}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: NhnlParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for nhnl-oscillator-zero."""
    params = params or NhnlParams()
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
    osc_vals = nhnl_osc(highs, lows, params.l, params.w)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_osc = osc_vals[i]
        prev_osc = osc_vals[i - 1]

        if cur_osc is None or prev_osc is None:
            continue

        co_zero = (prev_osc <= 0.0) and (cur_osc > 0.0)
        cu_zero = (prev_osc >= 0.0) and (cur_osc < 0.0)

        # Long entry logic
        if not in_pos:
            entry_cond = co_zero
            if params.mode == "mode_b":
                entry_cond = entry_cond and (cur_osc > params.thr)

            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * atr_vals[i]
        else:
            if h > highest_since_entry:
                highest_since_entry = h

            # ATR trailing stop
            atr_stop_hit = False
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                cur_stop = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                stops[i] = cur_stop
                if c < cur_stop:
                    atr_stop_hit = True

            exit_cond = cu_zero or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
