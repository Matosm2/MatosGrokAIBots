"""vpci-zero-cross — Volume Price Confirmation Indicator zero-cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage19 volume seats (VZO/NVI) 0 BTC; HHLL quiet-BNB death.
  VPCI (Buff Dormeier TASC / Dow Award):
    vpc = vwma(close, long) - sma(close, long)
    vpr = vwma(close, short) / sma(close, short)
    vm = sma(volume, short) / sma(volume, long)
    vpci = vpc * vpr * vm
  Mode A = VPCI x 0 cross.
  Intended to confirm majors trends denser than thin TTF while whipsawing
  less on quiet BNB (volume-contradiction damps chatter) — identical (short, long).
  != VZO / != III / != CMF / != OBV / != NVI.
  != VWMA x SMA dual-cross primary.

Mode A (prefer (5,20)):
  long: crossover(vpci, 0)
  exit: crossunder(vpci, 0)

Mode B (BNB quiet / chatter):
  sig = sma(vpci, sig_len), cross VPCI x sig instead of 0 — identical params.

btc_smoke:
  Kill longLen inflate until n collapses;
  Kill Mode A BTC 0 / chop; Kill VZO/III/CMF labeled VPCI. Prefer Mode A (5,20), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x;
  Kill lengths retuned only on ETH; Kill III/VZO labeled VPCI. Prefer identical (5,20).

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x;
  15m short=2 spam; stage12-19 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL: Kill 3-coin clear then BNB quiet wipe;
  Kill short/long retuned only on BNB; Kill Mode B only on BNB;
  ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: VZO/III/CMF/OBV/NVI labeled VPCI; VWMA x SMA dual-cross labeled VPCI;
request.security; stage12-19 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, sma, vpci

STRATEGY_ID = "vpci-zero-cross"


@dataclass(frozen=True)
class VpciParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    short_len: int = 5
    long_len: int = 20
    sig_len: int = 0  # 0 = raw zero-cross
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: VpciParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.short_len not in {5, 8}:
        return False, f"btc_smoke: short_len={params.short_len} not in locked sweep {{5, 8}}"
    if params.long_len not in {20, 25}:
        return False, f"btc_smoke: long_len={params.long_len} not in locked sweep {{20, 25}}"
    if params.long_len > 40:
        return False, f"btc_smoke: long_len={params.long_len} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: VpciParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.short_len not in {5, 8} or params.long_len not in {20, 25}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VpciParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.short_len <= 2:
        return False, "sol_smoke: 15m short_len<=2 forbidden (spam)"
    if params.short_len not in {5, 8} or params.long_len not in {20, 25}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: VpciParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.short_len not in {5, 8} or params.long_len not in {20, 25}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VpciParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vpci-zero-cross."""
    params = params or VpciParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    vpci_vals = vpci(closes, volumes, short_len=params.short_len, long_len=params.long_len)

    if params.mode == "mode_b" and params.sig_len > 0:
        clean_vpci = [v if v is not None else 0.0 for v in vpci_vals]
        ref_line = sma(clean_vpci, params.sig_len)
    else:
        ref_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(vpci_vals, ref_line, i)
        cross_dn = crossunder(vpci_vals, ref_line, i)

        entry_trigger = cross_up

        if not in_pos:
            if entry_trigger:
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

            if stop_hit or cross_dn:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
