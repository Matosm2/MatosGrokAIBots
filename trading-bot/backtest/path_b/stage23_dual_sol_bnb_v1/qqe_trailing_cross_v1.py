"""qqe-trailing-cross — Quantitative Qualitative Estimation Fast x Slow trailing cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage22 cleared BTC->ETH then SOL 0.922x under gate (percentile) — need denser
  oscillator participation on SOL without cloning percentile/z/AVWAP/VFI.
  QQE (Livshin) = EMA-smoothed RSI + double-smoothed ATR-of-RSI trailing band (x4.236).
  Mode A:
    long crossover(qqeFast, qqeSlow)
    exit crossunder(qqeFast, qqeSlow)
  Mode B:
    require qqeFast > 50 — only if Mode A over-whips; identical params across all four coins.
  Prefer (14, 5, 4.236) Mode A.
  != raw RSI 70/30 / != Schaff / != WaveTrend / != ConnorsRSI.

btc_smoke:
  Kill Mode A BTC 0/chop; Kill rsiLen/SF/WT inflate until n collapses;
  Kill raw RSI/Schaff/WaveTrend labeled QQE. Prefer Mode A (14,5,4.236), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill params retuned only on ETH. Prefer identical.

sol_smoke:
  CRITICAL: Kill BTC+ETH clear then SOL under 1.2x (Kagi / 0.922x);
  Kill params retuned only on SOL; 15m rsiLen=5; stage12-22 grafts.
  Prefer denser n >> 9. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: raw RSI labeled QQE; Schaff/WaveTrend/Connors graft; request.security;
stage12-22 grafts; SOL-only retune to close 0.922x.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, qqe

STRATEGY_ID = "qqe-trailing-cross"


@dataclass(frozen=True)
class QqeParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    rsi_len: int = 14     # 14, 21
    sf: int = 5           # 5, 8
    wt: float = 4.236     # 4.236, 5.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: QqeParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.rsi_len not in {14, 21}:
        return False, f"btc_smoke: rsi_len={params.rsi_len} not in locked sweep {{14, 21}}"
    if params.sf not in {5, 8}:
        return False, f"btc_smoke: sf={params.sf} not in locked sweep {{5, 8}}"
    if params.wt not in {4.236, 5.0}:
        return False, f"btc_smoke: wt={params.wt} not in locked sweep {{4.236, 5.0}}"
    if params.rsi_len > 30 or params.sf > 15:
        return False, "btc_smoke: parameter inflation collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: QqeParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.rsi_len not in {14, 21} or params.sf not in {5, 8} or params.wt not in {4.236, 5.0}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: QqeParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH PRIMARY CRITICAL)."""
    if tf == "15m" and params.rsi_len <= 5:
        return False, "sol_smoke: 15m rsi_len<=5 forbidden (spam)"
    if params.rsi_len not in {14, 21} or params.sf not in {5, 8} or params.wt not in {4.236, 5.0}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: QqeParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.rsi_len not in {14, 21} or params.sf not in {5, 8} or params.wt not in {4.236, 5.0}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: QqeParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for qqe-trailing-cross."""
    params = params or QqeParams()
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
    fast_vals, slow_vals = qqe(
        closes, rsi_len=params.rsi_len, sf=params.sf, wt=params.wt
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        f_cur = fast_vals[i]
        s_cur = slow_vals[i]

        if not in_pos:
            # crossover(qqeFast, qqeSlow)
            if crossover(fast_vals, slow_vals, i):
                can_enter = True
                if params.mode == "mode_b":
                    if f_cur is None or f_cur <= 50.0:
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

            # exit crossunder(qqeFast, qqeSlow)
            cross_exit = crossunder(fast_vals, slow_vals, i)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
