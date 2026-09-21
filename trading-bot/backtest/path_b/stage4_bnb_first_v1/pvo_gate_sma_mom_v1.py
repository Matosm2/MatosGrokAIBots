"""pvo-gate-sma-mom-v1 — Percentage Volume Oscillator Participation Gate + SMA Momentum.

LOCKED ENCODE ORDER #3 (BNB-survival-FIRST).
Thesis:
  PVO = % difference of fast vs slow volume EMAs (direction-blind volume-momentum).
  Pairing PVO > 0 (or rising) as a hard gate with a simple price SMA cross admits only
  volume-expanding momentum flips — BNB-hardening after price-only MA wipes while keeping SOL 1H-4H density.

Indicators:
  fastV = ta.ema(volume, 12); slowV = ta.ema(volume, 26); pvo = 100*(fastV - slowV)/slowV; sig = ta.ema(pvo, 9).
  SMA(close, len) with len in {10, 20, 34} (NOT 200).

Gate variants:
  Gate 1: pvo > 0
  Gate 2: pvo > pvo[1] and pvo > sig

Momentum Mode A:
  Long: ta.crossover(close, sma) while gate is True.

Momentum Mode B (state entry):
  Long while close > sma and gate is True (first bar becoming true).

Exit:
  Opposite momentum cross (close < sma or crossunder) OR gate lost (pvo < 0) + optional ATR.
  MANDATORY: exit_on_gate_loss=True for BNB smoke.

BNB Smoke Rules:
  Kill if: (1) PVO sole entry (no price mom); (2) no exit when PVO loses > 0;
  (3) 15m; (4) SMA len = 200; (5) volume == 0.
  Require exit_on_gate_loss=True, len <= 34, 1H+.

Distinct from: VWMA, MACD/PPO primary, EMA ribbon, SMA200.
Closed-bar only; long-only first pass; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, pvo, sma

STRATEGY_ID = "pvo-gate-sma-mom-v1"


@dataclass(frozen=True)
class PvoMomParams:
    mode: str = "mode_a"  # "mode_a" (crossover) | "mode_b" (state entry)
    gate_variant: str = "pvo_pos"  # "pvo_pos" (pvo > 0) | "pvo_sig" (pvo > pvo[1] & pvo > sig)
    sma_len: int = 20  # in {10, 20, 34}
    fast_len: int = 12
    slow_len: int = 26
    signal_len: int = 9
    exit_on_gate_loss: bool = True  # mandatory True for BNB smoke
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def compute_signals(
    bars: list[Bar],
    params: PvoMomParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for pvo-gate-sma-mom-v1."""
    params = params or PvoMomParams()
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

    pvo_vals, sig_vals = pvo(vols, params.fast_len, params.slow_len, params.signal_len)
    sma_vals = sma(closes, params.sma_len)
    close_lines = [float(c) for c in closes]
    atr_vals = atr(highs, lows, closes, params.atr_len)

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        v = vols[i]
        s = sma_vals[i]
        pv = pvo_vals[i]
        sg = sig_vals[i]

        if s is None or pv is None or v == 0:
            if in_pos:
                stops[i] = stop_level
            continue

        # Evaluate participation gate
        if params.gate_variant == "pvo_pos":
            gate_active = pv > 0.0
        else:  # pvo_sig
            prev_pv = pvo_vals[i - 1] if i > 0 else None
            gate_active = (prev_pv is not None and pv > prev_pv and sg is not None and pv > sg)

        entry_sig = False
        exit_sig = False

        if params.mode == "mode_a":
            # Crossover of close > SMA while gate is active
            if crossover(close_lines, sma_vals, i) and gate_active:
                entry_sig = True
            elif crossunder(close_lines, sma_vals, i):
                exit_sig = True
        else:  # mode_b: state entry
            prev_c = closes[i - 1] if i > 0 else 0.0
            prev_s = sma_vals[i - 1] if i > 0 else None
            prev_pv = pvo_vals[i - 1] if i > 0 else None
            prev_gate = False
            if prev_pv is not None:
                if params.gate_variant == "pvo_pos":
                    prev_gate = prev_pv > 0.0
                elif i > 1 and pvo_vals[i - 2] is not None and sig_vals[i - 1] is not None:
                    prev_gate = prev_pv > pvo_vals[i - 2] and prev_pv > sig_vals[i - 1]

            cond_now = c > s and gate_active
            cond_prev = prev_s is not None and prev_c > prev_s and prev_gate
            if cond_now and not cond_prev:
                entry_sig = True
            elif c < s:
                exit_sig = True

        # Gate loss exit (mandatory for BNB smoke)
        if params.exit_on_gate_loss and in_pos:
            if pv <= 0.0:
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
