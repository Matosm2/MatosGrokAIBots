"""gmma-osc-zero-cross-v1 — Guppy Multiple Moving Average group-mean oscillator zero-cross.

LOCKED ENCODE ORDER #4 (BNB-SURVIVAL-FIRST + DENSITY: SOL + BNB survival).
Thesis:
  Stage10 wiped DEMA; stage8 wiped WMA dual; dual-mom / EMA+RSI burned.
  Guppy GMMA is a 12-EMA ribbon (short group 3/5/8/10/12/15 vs long 30/35/40/45/50/60)
  as trader vs investor proxy — group-mean %-gap oscillator zero-cross is != dual-momentum
  absolute/relative ranking, != single fast x slow DEMA/WMA, != EMA+RSI stack.
  Zero-cross of (meanShort - meanLong)/meanLong is dense on 1H; close-only EMAs -> BNB-portable
  identical groups.

Formula:
  s = mean(EMA(close, {3,5,8,10,12,15}))
  l = mean(EMA(close, {30,35,40,45,50,60}))
  gmmaO = 100 * (s - l) / l

Mode A (primary / dense zero-cross):
  long: crossover(gmmaO, 0)
  exit: crossunder(gmmaO, 0) or ATR stop.

Mode B (signal quality / BNB quiet):
  sig = ema(gmmaO, sig_len) (default 15)
  long: crossover(gmmaO, sig) and gmmaO > 0
  exit: crossunder(gmmaO, sig) or ATR stop.

sol_smoke:
  Kill if: dual-mom / EMA+RSI / DEMA/WMA dual labeled GMMA; 15m stripped to 2 EMAs; ER/AO/PGO graft.
  Prefer Mode A classic 12 lengths, 1H+.
  Retention check: after ETH, SOL zero-cross n must not collapse to single digits.

bnb_smoke:
  Kill if: different group lengths than SOL; Mode B only on BNB while SOL Mode A;
  ungated shorts; no ATR; per-coin length retune. Prefer identical; long-only; ATR exit.

Forbidden: dual-mom ranking; EMA+RSI; WMA/DEMA/HMA dual disguise; SMA200; ER-gate; AO/ROC/PGO;
TII/Rainbow/TCF; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ema, gmma_oscillator

STRATEGY_ID = "gmma-osc-zero-cross-v1"


@dataclass(frozen=True)
class GmmaOscParams:
    mode: str = "mode_a"  # "mode_a" (gmmaO cross 0) | "mode_b" (gmmaO cross sig and gmmaO > 0)
    sig_len: int = 15
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_sol_smoke(params: GmmaOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.sig_len <= 3:
        return False, "sol_smoke: 15m sig_len<=3 forbidden (spam)"
    if params.sig_len not in {10, 15}:
        return False, f"sol_smoke: sig_len={params.sig_len} not in locked set {{10, 15}}"
    return True, "PASS"


def validate_bnb_smoke(params: GmmaOscParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation."""
    if params.sig_len <= 0 or params.sig_len > 50:
        return False, "bnb_smoke: sig_len must be in (0, 50]"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: GmmaOscParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for gmma-osc-zero-cross-v1."""
    params = params or GmmaOscParams()
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
    gmma_o = gmma_oscillator(closes)

    zeroes: list[float | None] = [0.0] * n

    # Mode B signal line
    sig_series: list[float | None] = [None] * n
    if params.mode == "mode_b":
        first_valid = -1
        for i in range(n):
            if gmma_o[i] is not None:
                first_valid = i
                break
        if first_valid != -1:
            valid_o = [float(gmma_o[i]) for i in range(first_valid, n)]
            inner_sig = ema(valid_o, params.sig_len)
            for i, val in enumerate(inner_sig):
                sig_series[first_valid + i] = val

    in_pos = False
    highest_since_entry = 0.0
    stop_level: float | None = None

    for i in range(n):
        c = closes[i]
        h = highs[i]

        # Update trailing stop if in position
        if in_pos and params.atr_trail_mult > 0.0:
            if h > highest_since_entry:
                highest_since_entry = h
                if atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
            stops[i] = stop_level

        # Check exits first
        if in_pos:
            exit_signal = False
            if params.mode == "mode_a":
                if crossunder(gmma_o, zeroes, i):
                    exit_signal = True
            elif params.mode == "mode_b":
                if crossunder(gmma_o, sig_series, i):
                    exit_signal = True

            # Stop hit check
            if stop_level is not None and c < stop_level:
                exit_signal = True

            if exit_signal:
                sells[i] = True
                in_pos = False
                highest_since_entry = 0.0
                stop_level = None
                continue

        # Check entries if flat
        if not in_pos and i > 0:
            enter_signal = False
            if params.mode == "mode_a":
                if crossover(gmma_o, zeroes, i):
                    enter_signal = True
            elif params.mode == "mode_b":
                # Mode B: crossover(gmmaO, sig) and gmmaO > 0
                if crossover(gmma_o, sig_series, i):
                    go_val = gmma_o[i]
                    if go_val is not None and go_val > 0.0:
                        enter_signal = True

            if enter_signal:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stop_level = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                    stops[i] = stop_level

    return buys, sells, stops
