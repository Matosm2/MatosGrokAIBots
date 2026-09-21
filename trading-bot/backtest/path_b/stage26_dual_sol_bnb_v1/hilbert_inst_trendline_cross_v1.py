"""hilbert-inst-trendline-cross — Hilbert Transform Instantaneous Trendline price cross.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage25 0-BTC siblings + NHNL ETH fail — need published adaptive trendline that can
  clear BTC >= 1.20 then port ETH denser than NHNL without cloning fixed-alpha ITrend Trigger /
  PMA / MAMA*FAMA.
  HT_TRENDLINE (Ehlers via TA-Lib; Rocket Science for Traders):
    Hilbert dominant-cycle period -> SMA(price, DCPeriodInt) -> 4-bar WMA smooth.
  Mode A:
    long crossover(close, ht)
    exit crossunder(close, ht)
  Mode B:
    require ht > ht[1] rising on entry — only if Mode A over-whips;
    identical params across all four coins.
  Prefer close x HT Mode A. No free Length (DC adaptive).
  != itrend-trigger-a007 (alpha=0.07 IIR + Trigger=2*IT - IT[2]) /
  != Predictive MA / != Decycler / != MAMA*FAMA / != SuperSmoother residual.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill n collapse (over-damp SMA-class);
  Kill ITrend-Trigger/PMA/MAMA/SuperTrend substitute. Prefer Mode A close x HT, 1H+.

eth_smoke:
  CRITICAL: Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill ITrend Trigger labeled HT_TRENDLINE.
  Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill pipeline retuned only on SOL;
  15m spam; MAMA/PMA graft; stage12-25 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill Mode B only on BNB;
  ungated shorts; no ATR; per-coin retune. Prefer identical; long-only; ATR exit.

Forbidden: itrend-trigger-a007 / fixed-alpha Trigger x ITrend labeled HT;
PMA/Decycler/MAMA/SS/SuperTrend labeled HT; request.security; stage12-25 grafts;
SOL-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, hilbert_ht_trendline

STRATEGY_ID = "hilbert-inst-trendline-cross"


@dataclass(frozen=True)
class HilbertTrendlineParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    source: str = "close"         # "close" | "hl2"
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: HilbertTrendlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.source not in {"close", "hl2"}:
        return False, f"btc_smoke: source={params.source} not in {{'close', 'hl2'}}"
    return True, "PASS"


def validate_eth_smoke(params: HilbertTrendlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC PRIMARY CRITICAL)."""
    if params.source not in {"close", "hl2"}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: HilbertTrendlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.source not in {"close", "hl2"}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: HilbertTrendlineParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.source not in {"close", "hl2"}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: HilbertTrendlineParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for hilbert-inst-trendline-cross."""
    params = params or HilbertTrendlineParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]

    if params.source == "hl2":
        source_prices = [(highs[i] + lows[i]) / 2.0 for i in range(count)]
    else:
        source_prices = closes

    atr_vals = atr(highs, lows, closes, params.atr_len)
    ht_vals = hilbert_ht_trendline(source_prices)

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_ht = ht_vals[i]
        prev_ht = ht_vals[i - 1]

        if cur_ht is None or prev_ht is None:
            continue

        co_ht = (closes[i - 1] <= prev_ht) and (c > cur_ht)
        cu_ht = (closes[i - 1] >= prev_ht) and (c < cur_ht)

        # Long entry logic
        if not in_pos:
            entry_cond = co_ht
            if params.mode == "mode_b":
                entry_cond = entry_cond and (cur_ht > prev_ht)

            if entry_cond:
                buys[i] = True
                in_pos = True
                highest_since_entry = h
                if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                    stops[i] = c - params.atr_trail_mult * atr_vals[i]
        else:
            if h > highest_since_entry:
                highest_since_entry = h

            # ATR trailing stop
            atr_stop_hit = False
            if params.atr_trail_mult > 0.0 and atr_vals[i] is not None:
                cur_stop = highest_since_entry - params.atr_trail_mult * atr_vals[i]
                stops[i] = cur_stop
                if c < cur_stop:
                    atr_stop_hit = True

            exit_cond = cu_ht or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
