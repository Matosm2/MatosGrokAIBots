"""percent-envelopes-break — MA Percent Envelopes breakout.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage26 FVE under-1.2x + 0-BTC siblings — need published price-vs-SMA+-% impulse break
  denser than SafeZone/HT over-damp, without cloning BB/Keltner/Kirshenbaum/STARC/Disparity EXIT.
  % Envelopes (StockCharts ChartSchool; Fidelity MAE):
    mid = sma(close, Len)
    upper = mid * (1 + pct)
    lower = mid * (1 - pct)
  Mode A:
    long crossover(close, upper)
    exit crossunder(close, mid)
  Mode B:
    require mid > mid[1] rising on entry — only if Mode A over-whips;
    identical across all four coins.
  Prefer (Len=20, pct=0.025) Mode A.
  != BB (stdev) / != Keltner (ATR) / != Kirshenbaum (LinReg stderr) / != STARC / != Disparity.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill pct inflate until n collapses; Kill BB/Keltner/Kirshenbaum/STARC/Disparity labeled Envelopes.
  Prefer Mode A (20, 0.025), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill Disparity/BB labeled Envelopes. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill pct retuned only on SOL;
  15m Len=5 spam; BB graft; stage12-26 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: BB/Keltner/Kirshenbaum/STARC/Disparity labeled Envelopes;
request.security; stage12-26 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, percent_envelopes

STRATEGY_ID = "percent-envelopes-break"


@dataclass(frozen=True)
class PercentEnvelopesParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    length: int = 20              # 14, 20, 30
    pct: float = 0.025            # 0.015, 0.025, 0.04, 0.05
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: PercentEnvelopesParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.length not in {14, 20, 30}:
        return False, f"btc_smoke: length={params.length} not in {{14, 20, 30}}"
    if params.pct not in {0.015, 0.025, 0.04, 0.05}:
        return False, f"btc_smoke: pct={params.pct} not in {{0.015, 0.025, 0.04, 0.05}}"
    return True, "PASS"


def validate_eth_smoke(params: PercentEnvelopesParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.length not in {14, 20, 30} or params.pct not in {0.015, 0.025, 0.04, 0.05}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: PercentEnvelopesParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.length not in {14, 20, 30} or params.pct not in {0.015, 0.025, 0.04, 0.05}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: PercentEnvelopesParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.length not in {14, 20, 30} or params.pct not in {0.015, 0.025, 0.04, 0.05}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PercentEnvelopesParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for percent-envelopes-break."""
    params = params or PercentEnvelopesParams()
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
    mids, uppers, lowers = percent_envelopes(closes, length=params.length, pct=params.pct)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        mid_cur = mids[i]
        mid_prev = mids[i - 1]
        up_cur = uppers[i]
        up_prev = uppers[i - 1]
        c_cur = closes[i]
        c_prev = closes[i - 1]

        if mid_cur is None or mid_prev is None or up_cur is None or up_prev is None:
            continue

        crossover_upper = c_prev <= up_prev and c_cur > up_cur
        crossunder_mid = c_prev >= mid_prev and c_cur < mid_cur

        if params.mode == "mode_a":
            entry_cond = crossover_upper
            exit_cond = crossunder_mid
        elif params.mode == "mode_b":
            entry_cond = crossover_upper and (mid_cur > mid_prev)
            exit_cond = crossunder_mid
        else:
            entry_cond = crossover_upper
            exit_cond = crossunder_mid

        # ATR trailing check
        atr_stop_hit = False
        if in_pos and params.atr_trail_mult > 0.0:
            if highs[i] > highest_since_entry:
                highest_since_entry = highs[i]
            atr_v = atr_vals[i]
            if atr_v is not None:
                stop_level = highest_since_entry - params.atr_trail_mult * atr_v
                stops[i] = stop_level
                if closes[i] < stop_level:
                    atr_stop_hit = True

        if not in_pos:
            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = highs[i]
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = highest_since_entry - params.atr_trail_mult * atr_vals[i]
        else:
            if exit_cond or atr_stop_hit:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0

    return buys, sells, stops
