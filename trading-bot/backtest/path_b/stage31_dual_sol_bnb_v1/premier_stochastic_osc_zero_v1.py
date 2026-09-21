"""premier-stochastic-osc-zero — Lee Leibfarth Premier Stochastic Oscillator zero-cross.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage30 wipe + need published bounded impulse oscillator.
  PSO (Lee Leibfarth TASC Aug 2008; Traders Tips / LazyBear):
    %K = 100 * (Close - LLV) / (HHV - LLV) length Period
    N = 0.1 * (%K - 50)
    S = EMA(EMA(N, Smooth), Smooth)
    PSO = (exp(S) - 1) / (exp(S) + 1)
  Mode A:
    long crossover(pso, 0)
    exit crossunder(pso, 0)
  Mode B:
    require prior pso < -0.20 within recent bars then cross up through 0 —
    only if Mode A over-whips; identical across all four.
  Prefer (Period=8, Smooth=5) Mode A.
  != classic Stoch / != InverseFisherRSI / != QQE / != SMI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill Smooth inflated until BTC n collapses; Kill Stoch/InverseFisherRSI/QQE substitute;
  Kill Track-B graft. Prefer Mode A (8, 5), 1H+.

eth_smoke:
  Kill params retuned only on ETH; Kill Stoch labeled PSO. Prefer identical params.

sol_smoke:
  Kill params retuned only on SOL; 15m spam; stage1-30 grafts.

bnb_smoke:
  Kill params retuned only on BNB; Mode B only on BNB; ungated shorts.

Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, premier_stochastic_oscillator

STRATEGY_ID = "premier-stochastic-osc-zero"


@dataclass(frozen=True)
class PremierStochParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    period: int = 8               # 5, 8, 14
    smooth: int = 5               # 3, 5, 8
    oversold_dip_bars: int = 5    # Mode B dip lookback
    atr_trail_mult: float = 0.0   # 0.0 (off)
    atr_len: int = 14


def validate_btc_smoke(params: PremierStochParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period not in {5, 8, 14}:
        return False, f"btc_smoke: period={params.period} not in {{5, 8, 14}}"
    if params.smooth not in {3, 5, 8}:
        return False, f"btc_smoke: smooth={params.smooth} not in {{3, 5, 8}}"
    return True, "PASS"


def validate_eth_smoke(params: PremierStochParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation."""
    if params.period not in {5, 8, 14} or params.smooth not in {3, 5, 8}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: PremierStochParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.period not in {5, 8, 14} or params.smooth not in {3, 5, 8}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: PremierStochParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.period not in {5, 8, 14} or params.smooth not in {3, 5, 8}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PremierStochParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for premier-stochastic-osc-zero."""
    params = params or PremierStochParams()
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
    pso = premier_stochastic_oscillator(
        highs=highs,
        lows=lows,
        closes=closes,
        period=params.period,
        smooth=params.smooth,
    )
    zero_line = [0.0] * count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        cross_up = crossover(pso, zero_line, i)
        cross_dn = crossunder(pso, zero_line, i)

        dip_ok = True
        if params.mode == "mode_b":
            lb = min(i, params.oversold_dip_bars)
            dip_ok = any(
                pso[i - k] is not None and pso[i - k] < -0.20
                for k in range(1, lb + 1)
            )

        if params.mode == "mode_a":
            entry_cond = cross_up
            exit_cond = cross_dn
        elif params.mode == "mode_b":
            entry_cond = cross_up and dip_ok
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
