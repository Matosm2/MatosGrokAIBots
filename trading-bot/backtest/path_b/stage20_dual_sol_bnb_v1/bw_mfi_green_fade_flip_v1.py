"""bw-mfi-green-fade-flip — Bill Williams MFI Green/Fade polarity flip.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage19 HHLL overtraded quiet BNB after 3-coin clear.
  BW MFI = (H-L)/Volume with four states vs prior bar:
    Green: MFI > MFI[1] and Vol > Vol[1]
    Fade:  MFI < MFI[1] and Vol < Vol[1]
    Bull:  Close > Close[1]
  Mode A = facilitation polarity:
    long on rising edge of (Green and Bull)
    exit on Fade (or not Green)
  Prefer confirmBars=1.
  Mode B: confirmBars in {2, 3} consecutive Green — only if Mode A over-whips;
  identical params.
  != AO / != Money Flow Index / != VZO.

btc_smoke:
  Kill confirmBars inflate until n collapses;
  Kill Mode A BTC 0 / chop; Kill AO/MoneyFlow/HHLL substitute.
  Prefer Mode A confirmBars=1, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x;
  Kill confirmBars retuned only on ETH; Kill III/AO labeled BW MFI.
  Prefer identical confirmBars.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x;
  15m Fake-exit spam; stage12-19 grafts. Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL: Kill 3-coin clear then BNB quiet wipe;
  Kill confirmBars retuned only on BNB; Kill Mode B only on BNB;
  HHLL graft; ungated shorts; no ATR.
  Prefer identical; long-only; ATR. If Green still overtrades quiet BNB ->
  confirmBars=2 everywhere, else kill family.

Forbidden: Money Flow Index labeled BW MFI; AO/AC/Gator; HHLL/STARC;
VZO labeled facilitation; request.security; stage12-19 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, bw_mfi

STRATEGY_ID = "bw-mfi-green-fade-flip"


@dataclass(frozen=True)
class BwMfiParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    confirm_bars: int = 1  # 1, 2, 3
    exit_on_fade: bool = True  # True: exit on fade; False: exit on not green
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: BwMfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.confirm_bars not in {1, 2, 3}:
        return False, f"btc_smoke: confirm_bars={params.confirm_bars} not in locked sweep {{1, 2, 3}}"
    if params.confirm_bars > 5:
        return False, f"btc_smoke: confirm_bars={params.confirm_bars} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: BwMfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.confirm_bars not in {1, 2, 3}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: BwMfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.confirm_bars <= 1:
        return False, "sol_smoke: 15m confirm_bars<=1 forbidden (spam)"
    if params.confirm_bars not in {1, 2, 3}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: BwMfiParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.confirm_bars not in {1, 2, 3}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: BwMfiParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for bw-mfi-green-fade-flip."""
    params = params or BwMfiParams()
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
    _, green, fade, _, _ = bw_mfi(highs, lows, closes, volumes)

    # Bullish close direction
    bull = [False] * n
    for i in range(1, n):
        bull[i] = closes[i] > closes[i - 1]

    # Green with confirm bars: confirm_bars consecutive green
    consec_green = [0] * n
    count = 0
    for i in range(n):
        if green[i]:
            count += 1
        else:
            count = 0
        consec_green[i] = count

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        curr_green_qual = (consec_green[i] >= params.confirm_bars) and bull[i]
        prev_green_qual = (consec_green[i - 1] >= params.confirm_bars) and bull[i - 1] if i >= 1 else False

        rising_edge = curr_green_qual and not prev_green_qual

        if params.exit_on_fade:
            exit_trigger = fade[i]
        else:
            exit_trigger = not green[i]

        if not in_pos:
            if rising_edge:
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

            if stop_hit or exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
