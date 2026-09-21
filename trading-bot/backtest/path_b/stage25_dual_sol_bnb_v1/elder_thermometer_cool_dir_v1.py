"""elder-thermometer-cool-dir — Elder Market Thermometer cool × close direction.

LOCKED ENCODE ORDER #4.
Thesis:
  Stage24 0-BTC / stage21 vol-expansion*dir 0-BTC — need published cool-entry
  volatility thermometer (not rising-vol*dir) that can clear dense BTC >= 1.2x.
  Elder Market Thermometer (Come Into My Trading Room):
    thermo = max(abs(H - H[1]), abs(L[1] - L))
    tma = ema(thermo, emaLen)
    cool = thermo < tma
    bull = close > close[dirLen]
    hot = thermo > k * tma
  Mode A:
    long crossunder(thermo, tma) and bull (cool rising-edge)
    exit hot or crossover(thermo, tma)
  Mode B:
    require cool for confirmBars in {2, 3} — only if Mode A over-whips;
    identical params across all four coins.
  Prefer (emaLen=22, k=3.0, dirLen=1) Mode A.
  != Chaikin / Parkinson rising*dir / != Mass / != ATR-SAR / != Wilder-VS / != Chande-Kroll.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past ~1.194x / ~1.113x;
  Kill emaLen/k inflate until n collapses;
  Kill Chaikin/Parkinson rising*dir / Mass / ATR-SAR labeled thermo. Prefer Mode A (22,3.0), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill emaLen/k retuned only on SOL;
  15m emaLen=5 spam; stage12-24 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: Chaikin/Parkinson rising*dir / Mass / ATR-SAR / Wilder-VS / Chande-Kroll / CBL labeled thermo;
request.security; stage12-24 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, elder_thermometer

STRATEGY_ID = "elder-thermometer-cool-dir"


@dataclass(frozen=True)
class ElderThermometerParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    ema_len: int = 22           # 14, 20, 22
    k: float = 3.0              # 2.5, 3.0, 3.5
    dir_len: int = 1            # 1 (locked)
    confirm_bars: int = 2       # Mode B confirm bars: 2, 3
    atr_trail_mult: float = 0.0 # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: ElderThermometerParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.ema_len not in {14, 20, 22}:
        return False, f"btc_smoke: ema_len={params.ema_len} not in {{14, 20, 22}}"
    if params.k not in {2.5, 3.0, 3.5}:
        return False, f"btc_smoke: k={params.k} not in {{2.5, 3.0, 3.5}}"
    if params.dir_len != 1:
        return False, f"btc_smoke: dir_len={params.dir_len} != 1"
    return True, "PASS"


def validate_eth_smoke(params: ElderThermometerParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.ema_len not in {14, 20, 22} or params.k not in {2.5, 3.0, 3.5} or params.dir_len != 1:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ElderThermometerParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.ema_len not in {14, 20, 22} or params.k not in {2.5, 3.0, 3.5} or params.dir_len != 1:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ElderThermometerParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.ema_len not in {14, 20, 22} or params.k not in {2.5, 3.0, 3.5} or params.dir_len != 1:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ElderThermometerParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for elder-thermometer-cool-dir."""
    params = params or ElderThermometerParams()
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
    thermo_vals, tma_vals = elder_thermometer(highs, lows, params.ema_len)

    in_pos = False
    highest_since_entry = 0.0
    cool_consecutive = 0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_t = thermo_vals[i]
        prev_t = thermo_vals[i - 1]
        cur_tma = tma_vals[i]
        prev_tma = tma_vals[i - 1]

        if cur_t is None or prev_t is None or cur_tma is None or prev_tma is None:
            continue

        if i < params.dir_len:
            continue

        bull = c > closes[i - params.dir_len]
        cu_tma = (prev_t >= prev_tma) and (cur_t < cur_tma)
        co_tma = (prev_t <= prev_tma) and (cur_t > cur_tma)
        hot = cur_t > params.k * cur_tma

        if cur_t < cur_tma:
            cool_consecutive += 1
        else:
            cool_consecutive = 0

        # Long entry logic
        if not in_pos:
            entry_cond = cu_tma and bull
            if params.mode == "mode_b":
                entry_cond = (cool_consecutive >= params.confirm_bars) and bull

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

            exit_cond = hot or co_tma or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
