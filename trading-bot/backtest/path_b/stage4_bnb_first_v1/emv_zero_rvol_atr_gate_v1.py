"""emv-zero-rvol-atr-gate-v1 — Arms Ease of Movement Zero-Cross with RVOL + ATR% Gates.

LOCKED ENCODE ORDER #2 (BNB-survival-FIRST).
Thesis:
  EMV encodes distance-moved / box-ratio(volume). Moves requiring heavy volume score near zero (hard),
  easy moves on light volume score large. On thinner BNB, ungated EMV whipsaws;
  gating zero-crosses with RVOL >= k and min ATR% keeps only "easy move + real participation" flips.

Indicators:
  emv = ta.eom(eomLen, div); eomLen in {10, 14, 20}.
  Symbol divisor locked before length sweep:
    BTC: 1e7, ETH: 1e7, SOL: 1e8, BNB: 1e7 (rescaled).

Signal Mode A:
  Long: ta.crossover(emv, 0) and rvol >= k and (high - low)/close >= atrPctMin (or range >= 0.15*ATR).
  Short: crossunder with same gates.

Signal Mode B:
  EMV x SMA(EMV, signalLen=9) cross instead of raw zero with same gates.

BNB Smoke Rules:
  Kill if: (1) ungated zero-crosses; (2) divisor copied from BTC without BNB rescale;
  (3) no RVOL floor (require k >= 1.5 on BNB); (4) no skip when volume=0; (5) 15m;
  (6) atrPctMin off on BNB (require atrPctMin >= 0.002).

Distinct from: Ungated EMV, CMF, OBV, MFI, Chaikin Osc, Klinger.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, eom, rvol, sma

STRATEGY_ID = "emv-zero-rvol-atr-gate-v1"

# Divisor locked per symbol before length sweep
SYMBOL_DIVISORS: dict[str, float] = {
    "BTCUSDT": 10_000_000.0,
    "ETHUSDT": 10_000_000.0,
    "SOLUSDT": 100_000_000.0,
    "BNBUSDT": 10_000_000.0,
}


@dataclass(frozen=True)
class EmvGateParams:
    mode: str = "mode_a"  # "mode_a" (zero cross) | "mode_b" (signal cross)
    eom_len: int = 14
    divisor: float = 10_000_000.0
    rvol_k: float = 1.0  # RVOL gate multiplier
    vol_len: int = 20
    atr_pct_min: float = 0.002  # min (high - low) / close
    atr_trail_mult: float = 0.0
    atr_len: int = 14
    signal_len: int = 9  # for Mode B


def compute_signals(
    bars: list[Bar],
    params: EmvGateParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for emv-zero-rvol-atr-gate-v1."""
    params = params or EmvGateParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]

    emv_vals = eom(highs, lows, vols, length=params.eom_len, divisor=params.divisor)
    zero_line = [0.0] * n
    sig_line = sma([v if v is not None else 0.0 for v in emv_vals], params.signal_len) if params.mode == "mode_b" else None

    rvol_vals = rvol(vols, params.vol_len)
    atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]
        l = lows[i]
        v = vols[i]
        ev = emv_vals[i]

        if ev is None or v == 0:
            if in_pos:
                stops[i] = stop_level
            continue

        # Participation gates
        bar_range_pct = (h - l) / c if c > 0 else 0.0
        atr_ok = bar_range_pct >= params.atr_pct_min
        rv = rvol_vals[i]
        rvol_ok = (rv is not None and rv >= params.rvol_k) if params.rvol_k > 0 else True
        gates_passed = atr_ok and rvol_ok

        entry_sig = False
        exit_sig = False

        if params.mode == "mode_a":
            # Zero-cross
            if crossover(emv_vals, zero_line, i) and gates_passed:
                entry_sig = True
            elif crossunder(emv_vals, zero_line, i):
                exit_sig = True
        else:  # mode_b
            if sig_line is not None:
                if crossover(emv_vals, sig_line, i) and gates_passed:
                    entry_sig = True
                elif crossunder(emv_vals, sig_line, i):
                    exit_sig = True

        if in_pos:
            stops[i] = stop_level
            highest_since_entry = max(highest_since_entry, c)

            hit_exit = False
            if exit_sig:
                hit_exit = True
            elif params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                trail_stop = highest_since_entry - atr_vals[i] * params.atr_trail_mult
                stop_level = max(stop_level or trail_stop, trail_stop)
                stops[i] = stop_level
                if c < stop_level:
                    hit_exit = True

            if hit_exit:
                sells[i] = True
                in_pos = False
                stop_level = None
            continue

        if entry_sig:
            buys[i] = True
            in_pos = True
            highest_since_entry = c
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                stop_level = c - atr_vals[i] * params.atr_trail_mult
                stops[i] = stop_level

    return buys, sells, stops
