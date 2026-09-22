"""ehlers-twopole-hp-zero — Ehlers Two-Pole HighPass zero-cross.

LOCKED ENCODE ORDER #2 (BTC LEAD PRIMARY — SINGLE HP RESIDUAL ZERO-CROSS).
Thesis:
  Stage15 dual-HP/RMS (UO2025) and rank/NET over-damped BTC to 0 PASS.
  A SINGLE two-pole HighPass (remove long cycles only) leaves a signed residual that zero-crosses responsively —
  simpler than dual-HP-band or CorrCycle,
  no SuperSmoother after HP (!= Roofing),
  != UO2025 (HP1-HP2)/RMS,
  != Precision Trend HP250-HP40 dual.
  Intended BTC-lead density without stage12/15 over-damp.
  Close-only -> identical Period across coins.

Formula:
  a1 = exp(-1.414*pi / P)
  c2 = 2 * a1 * cos(1.414*pi / P)
  c3 = -a1^2
  c1 = (1 + c2 - c3) / 4
  HP = c1 * (src - 2*src[1] + src[2]) + c2 * HP[1] + c3 * HP[2]
  Prefer P=40. SINGLE HP only — no SS after.

Mode A (BTC-LEAD PRIMARY — prefer first):
  long: crossover(hp, 0)
  exit: crossunder(hp, 0) or ATR stop.

Mode B (BNB quiet):
  long: crossover(hp, 0) and hp > epsilon
  exit: crossunder(hp, 0) or ATR stop.
  (identical Period; only if Mode A over-whips BNB).

btc_smoke:
  BTC-LEAD CRITICAL: Kill if P raised until BTC n collapses;
  Kill if SS grafted after HP (Roofing);
  Kill if dual-HP UO2025 substitute.
  Prefer Mode A P=40, 1H+.

eth_smoke:
  BTC->ETH PORTABILITY CRITICAL: Kill if BTC clears >=1.2x then ETH wipes.
  Kill if P retuned only on ETH; Kill if Roofing/SS substitute.
  Prefer identical P=40 on ETH; ETH n multi-dozen.

sol_smoke:
  Kill if Roofing / UO2025 / Cyber Cycle labeled single-HP; 15m P=5 spam; stage12-15 grafts.
  Retention check: after ETH, SOL n multi-dozen-class on 6m 1H.

bnb_smoke:
  BNB-after-BTC+ETH+SOL quiet-wipe CRITICAL:
  different P than SOL; Mode B shorts ungated; no ATR; per-coin retune.
  Prefer identical params; long-only; ATR exit.

Forbidden: Roofing (HP+SS); UO2025 dual-HP/RMS; Precision dual-HP Trend as this seat;
SuperSmoother graft; Spearman/CorrCycle/NET/DVI; TTF/PFE/ASH/APZ/Nadaraya; stage12-13; request.security.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_twopole_hp

STRATEGY_ID = "ehlers-twopole-hp-zero"


@dataclass(frozen=True)
class TwopoleHpParams:
    mode: str = "mode_a"  # "mode_a" (hp cross 0) | "mode_b" (hp cross 0 + quality hold)
    period: int = 40
    quality_threshold: float = 0.0
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: TwopoleHpParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.period > 80:
        return False, f"btc_smoke: period={params.period} > 80 collapses BTC n"
    if params.period not in {28, 40, 48, 60}:
        return False, f"btc_smoke: period={params.period} not in locked set {{28, 40, 48, 60}}"
    return True, "PASS"


def validate_eth_smoke(params: TwopoleHpParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY CRITICAL)."""
    if params.period not in {28, 40, 48, 60}:
        return False, f"eth_smoke: period={params.period} retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: TwopoleHpParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation."""
    if tf == "15m" and params.period <= 5:
        return False, "sol_smoke: 15m period<=5 forbidden (spam)"
    if params.period not in {28, 40, 48, 60}:
        return False, f"sol_smoke: period={params.period} not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: TwopoleHpParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after BTC+ETH+SOL)."""
    if params.period <= 0:
        return False, "bnb_smoke: period must be > 0"
    if params.period > 80:
        return False, "bnb_smoke: period too large"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: TwopoleHpParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-twopole-hp-zero."""
    params = params or TwopoleHpParams()
    n = len(bars)
    buys = [False] * n
    sells = [False] * n
    stops: list[float | None] = [None] * n
    if n == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    hp = ehlers_twopole_hp(closes, period=params.period)

    zero_line = [0.0] * n

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(hp, zero_line, i)
        cross_dn = crossunder(hp, zero_line, i)

        if params.mode == "mode_b":
            hp_val = hp[i]
            if hp_val is None or hp_val <= params.quality_threshold:
                cross_up = False

        if not in_pos:
            if cross_up:
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
