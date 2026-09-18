"""volume-roc-dir — Volume Rate of Change × close direction.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage24 0-BTC; Stage-22 VFI cleared BTC->ETH then SOL failed — need raw volume ROC
  (not VFI/PVO/OBV) gated by close direction for dense BTC >= 1.2x.
  VROC (Investopedia / TrendSpider / Barchart):
    vroc = 100 * (volume - volume[n]) / volume[n] (guard volume[n]=0)
    bull = close > close[dirLen]
  Mode A:
    long crossover(vroc, 0) and bull
    exit crossunder(vroc, 0) or not bull
  Mode B:
    require vroc > thr (thr in {10.0, 20.0}) — only if Mode A over-whips;
    identical params across all four coins.
  Prefer n=14, dirLen=1 Mode A.
  != price ROC / != PVO (EMA volume % osc) / != vol-expansion*dir / != VFI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x / ~1.113x;
  Kill n inflate until n collapses;
  Kill PVO/price-ROC/vol-exp*dir/VFI labeled VROC. Prefer Mode A n=14, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill n retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill n retuned only on SOL;
  15m n=3 spam; stage12-24 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe (volume-shape CRITICAL); Kill n retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: PVO/price-ROC/Chaikin-vol*dir/OBV/VFI labeled VROC;
request.security; stage12-24 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, volume_roc

STRATEGY_ID = "volume-roc-dir"


@dataclass(frozen=True)
class VolumeRocParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    n: int = 14                 # 10, 14, 20, 25
    dir_len: int = 1            # 1, 3
    thr: float = 10.0           # Mode B entry thr: 10.0, 20.0
    atr_trail_mult: float = 0.0 # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: VolumeRocParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {10, 14, 20, 25}:
        return False, f"btc_smoke: n={params.n} not in {{10, 14, 20, 25}}"
    if params.dir_len not in {1, 3}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in {{1, 3}}"
    return True, "PASS"


def validate_eth_smoke(params: VolumeRocParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.n not in {10, 14, 20, 25} or params.dir_len not in {1, 3}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VolumeRocParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {10, 14, 20, 25} or params.dir_len not in {1, 3}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: VolumeRocParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.n not in {10, 14, 20, 25} or params.dir_len not in {1, 3}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VolumeRocParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for volume-roc-dir."""
    params = params or VolumeRocParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    vroc_vals = volume_roc(volumes, params.n)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_vroc = vroc_vals[i]
        prev_vroc = vroc_vals[i - 1]

        if cur_vroc is None or prev_vroc is None:
            continue

        if i < params.dir_len:
            continue

        bull = c > closes[i - params.dir_len]
        co_zero = (prev_vroc <= 0.0) and (cur_vroc > 0.0)
        cu_zero = (prev_vroc >= 0.0) and (cur_vroc < 0.0)

        # Long entry logic
        if not in_pos:
            entry_cond = co_zero and bull
            if params.mode == "mode_b":
                entry_cond = entry_cond and (cur_vroc > params.thr)

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

            exit_cond = cu_zero or (not bull) or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
