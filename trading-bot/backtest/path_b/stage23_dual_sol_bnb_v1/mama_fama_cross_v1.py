"""mama-fama-cross — Ehlers MAMA x FAMA adaptive MA cross.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage22 SOL 0.922x after majors — need adaptive dual-line flip that participates
  on SOL without cloning percentile channel.
  MAMA/FAMA (Ehlers): alpha from Hilbert phase rate-of-change;
  mama = alpha * price + (1 - alpha) * mama[1]
  fama = 0.5 * alpha * mama + (1 - 0.5 * alpha) * fama[1]
  Mode A:
    long crossover(mama, fama)
    exit crossunder(mama, fama)
  Mode B:
    require mama > mama[1] rising — only if Mode A over-whips; identical across all four.
  Prefer (0.5, 0.05) Mode A.
  Do NOT trade Period / SmoothPeriod / Sine / LeadSine.
  != MESA-primary dominant period / != Sinewave / != PMA / != FRAMA / != HMA.

btc_smoke:
  Kill Mode A BTC 0/chop (alpha chatter); Kill limits inflate until n collapses;
  Kill MESA-primary/Sinewave/Homodyne-as-signal substitute. Prefer Mode A (0.5, 0.05), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill limits retuned only on ETH. Prefer identical.

sol_smoke:
  CRITICAL: Kill BTC+ETH clear then SOL under 1.2x; Kill limits retuned only on SOL;
  MESA-primary / structure-stall substitute; 15m spam; stage12-22 grafts.
  Prefer denser n >> 9. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill limits retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: MESA-primary / Sinewave / Homodyne-as-signal labeled this ID;
FRAMA/HMA/McGinley/PMA graft; request.security; stage12-22 grafts; SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, mama_fama

STRATEGY_ID = "mama-fama-cross"


@dataclass(frozen=True)
class MamaFamaParams:
    mode: str = "mode_a"        # "mode_a" | "mode_b"
    fast_limit: float = 0.5     # 0.5, 0.7
    slow_limit: float = 0.05    # 0.05, 0.08
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: MamaFamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.fast_limit not in {0.5, 0.7}:
        return False, f"btc_smoke: fast_limit={params.fast_limit} not in locked sweep {{0.5, 0.7}}"
    if params.slow_limit not in {0.05, 0.08}:
        return False, f"btc_smoke: slow_limit={params.slow_limit} not in locked sweep {{0.05, 0.08}}"
    if params.slow_limit > 0.15:
        return False, "btc_smoke: limits inflate until BTC n collapses"
    return True, "PASS"


def validate_eth_smoke(params: MamaFamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.fast_limit not in {0.5, 0.7} or params.slow_limit not in {0.05, 0.08}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: MamaFamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH PRIMARY CRITICAL)."""
    if params.fast_limit not in {0.5, 0.7} or params.slow_limit not in {0.05, 0.08}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: MamaFamaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.fast_limit not in {0.5, 0.7} or params.slow_limit not in {0.05, 0.08}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: MamaFamaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for mama-fama-cross."""
    params = params or MamaFamaParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    hl2 = [(b.high + b.low) / 2.0 for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    mama_vals, fama_vals = mama_fama(
        hl2, fast_limit=params.fast_limit, slow_limit=params.slow_limit
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        m_cur = mama_vals[i]
        m_prev = mama_vals[i - 1]

        if not in_pos:
            # crossover(mama, fama)
            if crossover(mama_vals, fama_vals, i):
                can_enter = True
                if params.mode == "mode_b":
                    if m_cur is None or m_prev is None or m_cur <= m_prev:
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

            # exit crossunder(mama, fama)
            cross_exit = crossunder(mama_vals, fama_vals, i)

            exit_trigger = stop_hit or cross_exit
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
