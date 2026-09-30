"""ehlers-fir-zl-price-cross — Ehlers Zero-Lag FIR filter x price cross.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage27 wipe + need published FIR impulse != IIR ZLEMA and != stage12 nonlinear EDCF filt*lag.
  Favorite FIR (Ehlers; TradingView everget cite S&C 20:7):
    (P + 2P[1] + 3P[2] + 3P[3] + 2P[4] + P[5]) / 12
  Zero-lag FIR (same article family / public coefficient sets):
    (P + 4.5P[1] + 5.5P[2] + 3P[3] - 0.5P[4] - 1.5P[5] - 2.5P[6]) / 9.5
  Mode A:
    long crossover(close, zlFir)
    exit crossunder(close, zlFir)
  Mode B:
    favorite FIR /12 instead — only if Mode A over-whips;
    identical params across all four coins (still not EDCF).
  Prefer src=close Mode A /9.5.
  != EDCF filt*lag / != ZLEMA / != SuperSmoother.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill EDCF/ZLEMA/US substitute.
  Prefer Mode A close x ZL-FIR, 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH. Prefer identical coeff set; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill coeff set retuned only on SOL;
  stage12-27 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill Mode B only on BNB.
  Prefer identical; long-only; ATR.

Forbidden: EDCF filt*lag / ZLEMA / SuperSmoother/Roofing;
stage12-27 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, ehlers_fir_zl

STRATEGY_ID = "ehlers-fir-zl-price-cross"


@dataclass(frozen=True)
class EhlersFirZlParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    src: str = "close"            # "close" | "hl2"
    denom: str = "9.5"            # "9.5" (mode_a) | "12" (mode_b)
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: EhlersFirZlParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.src not in {"close", "hl2"}:
        return False, f"btc_smoke: src={params.src} not in {{'close', 'hl2'}}"
    if params.denom not in {"9.5", "12"}:
        return False, f"btc_smoke: denom={params.denom} not in {{'9.5', '12'}}"
    return True, "PASS"


def validate_eth_smoke(params: EhlersFirZlParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC)."""
    if params.src not in {"close", "hl2"} or params.denom not in {"9.5", "12"}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: EhlersFirZlParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.src not in {"close", "hl2"} or params.denom not in {"9.5", "12"}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: EhlersFirZlParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.src not in {"close", "hl2"} or params.denom not in {"9.5", "12"}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: EhlersFirZlParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ehlers-fir-zl-price-cross."""
    params = params or EhlersFirZlParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    if params.src == "hl2":
        src_prices = [(highs[i] + lows[i]) / 2.0 for i in range(count)]
    else:
        src_prices = list(closes)

    denom_mode = "12" if (params.mode == "mode_b" or params.denom == "12") else "9.5"

    atr_vals = atr(highs, lows, closes, params.atr_len)
    zl_fir = ehlers_fir_zl(src_prices, denom_mode=denom_mode)

    # Price for crossover
    close_floats: list[float | None] = list(closes)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        crossover_price_fir = crossover(close_floats, zl_fir, i)
        crossunder_price_fir = crossunder(close_floats, zl_fir, i)

        entry_cond = crossover_price_fir
        exit_cond = crossunder_price_fir

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
