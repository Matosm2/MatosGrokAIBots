"""vervoort-zlha-typ-cross — Vervoort Zero-Lag TEMA(haC) x Zero-Lag TEMA(Typ) cross.

LOCKED ENCODE ORDER #2.
Thesis:
  Stage27 wipe + FVE under-lead — need published dual-line impulse denser than VR 0.698x
  without cloning HA color flip EXIT.
  Vervoort (S&C May 2008 "Quest for Reliable Crossovers"; Traders' Tips May 2008; STOCATA):
    haOpen = (ref((O+H+L+C)/4, -1) + PREV) / 2
    haC = ((O+H+L+C)/4 + haOpen + Max(H, haOpen) + Min(L, haOpen)) / 4
    Typ = (H+L+C) / 3
    ZLHA = TEMA(haC, N) + (TEMA(haC, N) - TEMA(TEMA(haC, N), N))
    ZLTyp = TEMA(Typ, N) + (TEMA(Typ, N) - TEMA(TEMA(Typ, N), N))
  Mode A:
    long crossover(zlTyp, zlHa)
    exit crossunder(zlTyp, zlHa)
  Mode B:
    require zlTyp > zlTyp[1] rising — only if Mode A over-whips;
    identical params across all four coins.
  Prefer N=34 Mode A.
  != HA color-flip / != TEMA-close-dual / != ZLEMA / != DEMA dual.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill N inflate until n collapses; Kill HA-color-flip / TEMA-close-dual / ZLEMA labeled Vervoort.
  Prefer Mode A N=34, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill HA color-flip labeled Vervoort. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill N retuned only on SOL;
  stage12-27 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill params retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR.

Forbidden: HA color-flip / TEMA dual of close / ZLEMA / DEMA dual labeled Vervoort;
stage12-27 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, vervoort_zlha_typ

STRATEGY_ID = "vervoort-zlha-typ-cross"


@dataclass(frozen=True)
class VervoortZlhaParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    n: int = 34                   # 21, 34, 55
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: VervoortZlhaParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.n not in {21, 34, 55}:
        return False, f"btc_smoke: n={params.n} not in {{21, 34, 55}}"
    return True, "PASS"


def validate_eth_smoke(params: VervoortZlhaParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.n not in {21, 34, 55}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: VervoortZlhaParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.n not in {21, 34, 55}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: VervoortZlhaParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.n not in {21, 34, 55}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: VervoortZlhaParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for vervoort-zlha-typ-cross."""
    params = params or VervoortZlhaParams()
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
    zl_typ, zl_ha = vervoort_zlha_typ(opens, highs, lows, closes, params.n)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        crossover_typ_ha = crossover(zl_typ, zl_ha, i)
        crossunder_typ_ha = crossunder(zl_typ, zl_ha, i)

        if params.mode == "mode_a":
            entry_cond = crossover_typ_ha
            exit_cond = crossunder_typ_ha
        elif params.mode == "mode_b":
            rising_ok = (
                zl_typ[i] is not None
                and zl_typ[i - 1] is not None
                and zl_typ[i] > zl_typ[i - 1]
            )
            entry_cond = crossover_typ_ha and rising_ok
            exit_cond = crossunder_typ_ha
        else:
            entry_cond = crossover_typ_ha
            exit_cond = crossunder_typ_ha

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
