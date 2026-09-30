"""apirine-ma-bands-break — Vitali Apirine Moving Average Bands break-accept.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage29 CPR 0.750x under + need published structure impulse
  != CPR TC/BC, HHLL, Track-B ATR corridor, BB/Keltner/%Envelopes.
  MAB (Vitali Apirine TASC Aug 2021; Financial Hacker / Traders' Tips):
    MA1 = EMA(Close, P1)
    MA2 = EMA(Close, P2)
    Dst = MA1 - MA2
    Dv = SMA(Dst^2, P2)
    Dev = Mltp * sqrt(Dv)
    Upper = MA1 + Dev
    Lower = MA1 - Dev
  Mode A:
    long crossover(ma2, upper)
    exit crossunder(ma2, lower)
  Mode B:
    require prior narrow width 100*(upper-lower)/ma1 < widthThr before Upper break —
    only if Mode A over-whips; identical across all four.
  Prefer (P1=50, P2=10, Mltp=1.0) Mode A.
  != BB / != Keltner / != Kirshenbaum / != CPR / != %Envelopes / != STARC.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill P1 inflate until n collapses; Kill BB/Keltner/Kirshenbaum/CPR/Envelopes labeled MAB;
  Kill Track-B CK graft. Prefer Mode A (50, 10, 1.0), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill BB labeled MAB. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill P2 retuned only on SOL;
  15m spam; stage12-29 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Kill Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: BB / Keltner / Kirshenbaum / CPR / %Envelopes / STARC labeled MAB; Track-B four; stage12-29.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import apirine_ma_bands, atr, crossover, crossunder

STRATEGY_ID = "apirine-ma-bands-break"


@dataclass(frozen=True)
class ApirineMaBandsParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    p1: int = 50                  # 34, 50, 100, 200
    p2: int = 10                  # 8, 10, 20, 50
    mltp: float = 1.0             # 0.75, 1.0, 1.5
    narrow_thr: float = 1.5       # Mode B narrow width % threshold
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: ApirineMaBandsParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.p1 not in {34, 50, 100, 200}:
        return False, f"btc_smoke: p1={params.p1} not in {{34, 50, 100, 200}}"
    if params.p2 not in {8, 10, 20, 50}:
        return False, f"btc_smoke: p2={params.p2} not in {{8, 10, 20, 50}}"
    if params.mltp not in {0.75, 1.0, 1.5}:
        return False, f"btc_smoke: mltp={params.mltp} not in {{0.75, 1.0, 1.5}}"
    return True, "PASS"


def validate_eth_smoke(params: ApirineMaBandsParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.p1 not in {34, 50, 100, 200} or params.p2 not in {8, 10, 20, 50} or params.mltp not in {0.75, 1.0, 1.5}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: ApirineMaBandsParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.p1 not in {34, 50, 100, 200} or params.p2 not in {8, 10, 20, 50} or params.mltp not in {0.75, 1.0, 1.5}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: ApirineMaBandsParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.p1 not in {34, 50, 100, 200} or params.p2 not in {8, 10, 20, 50} or params.mltp not in {0.75, 1.0, 1.5}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: ApirineMaBandsParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for apirine-ma-bands-break."""
    params = params or ApirineMaBandsParams()
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
    ma2, upper, lower, ma1 = apirine_ma_bands(
        closes=closes,
        p1=params.p1,
        p2=params.p2,
        mltp=params.mltp,
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(ma2, upper, i)
        cross_dn = crossunder(ma2, lower, i)

        narrow_ok = True
        if params.mode == "mode_b" and i > 0:
            m1 = ma1[i - 1]
            u1 = upper[i - 1]
            l1 = lower[i - 1]
            if m1 is not None and u1 is not None and l1 is not None and m1 > 1e-12:
                width_pct = 100.0 * (u1 - l1) / m1
                narrow_ok = width_pct < params.narrow_thr
            else:
                narrow_ok = False

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and narrow_ok
            exit_cond = cross_dn
        else:
            entry_cond = cross_up
            exit_cond = cross_dn

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
