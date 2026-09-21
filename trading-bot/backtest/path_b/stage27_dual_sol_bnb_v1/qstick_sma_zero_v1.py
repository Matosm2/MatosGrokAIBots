"""qstick-sma-zero — Chande Qstick SMA(close - open) zero-cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage26 FVE dense n=40 but BTC only 1.055x FAIL LEAD + Convolution/HT/SafeZone 0 BTC —
  need published denser open-close impulse that can push BTC past FVE's under-1.2x neighborhood
  without cloning FVE money-flow or stage8 ROC/AO.
  Qstick (Tushar Chande / Stanley Kroll, The New Technical Trader 1994):
    body = close - open
    qstick = sma(body, N)
  Mode A:
    long crossover(qstick, 0)
    exit crossunder(qstick, 0)
  Mode B:
    require qstick > sma(qstick, sig) sig in {3, 5} — only if Mode A over-whips;
    identical params across all four coins.
  Prefer N=8 Mode A.
  != RVI ((C-O)/(H-L) range-normalized) / != CMO / != ROC / != AO / != TSI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill N inflate until n collapses; Kill RVI/CMO/ROC/AO labeled Qstick.
  Prefer Mode A N=8, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill RVI labeled Qstick. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill N retuned only on SOL;
  15m spam; stage12-26 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill N retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: RVI/CMO/ROC/AO/TSI labeled Qstick; FVE grafts;
request.security; stage12-26 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, qstick, sma

STRATEGY_ID = "qstick-sma-zero"


@dataclass(frozen=True)
class QstickParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    n: int = 8                    # 8, 10, 14, 20
    sig: int = 3                  # for mode_b
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: QstickParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {8, 10, 14, 20}:
        return False, f"btc_smoke: n={params.n} not in {{8, 10, 14, 20}}"
    return True, "PASS"


def validate_eth_smoke(params: QstickParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.n not in {8, 10, 14, 20}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: QstickParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {8, 10, 14, 20}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: QstickParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.n not in {8, 10, 14, 20}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: QstickParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for qstick-sma-zero."""
    params = params or QstickParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    q_vals = qstick(opens, closes, params.n)

    q_clean = [q if q is not None else 0.0 for q in q_vals]
    q_sig = sma(q_clean, params.sig) if params.mode == "mode_b" else None

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        q_cur = q_vals[i]
        q_prev = q_vals[i - 1]

        if q_cur is None or q_prev is None:
            continue

        crossover_zero = q_prev <= 0.0 and q_cur > 0.0
        crossunder_zero = q_prev >= 0.0 and q_cur < 0.0

        if params.mode == "mode_a":
            entry_cond = crossover_zero
            exit_cond = crossunder_zero
        elif params.mode == "mode_b":
            sig_ok = q_sig is not None and q_sig[i] is not None and q_cur > q_sig[i]
            entry_cond = crossover_zero and sig_ok
            exit_cond = crossunder_zero
        else:
            entry_cond = crossover_zero
            exit_cond = crossunder_zero

        # Check ATR stop if enabled and in position
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
