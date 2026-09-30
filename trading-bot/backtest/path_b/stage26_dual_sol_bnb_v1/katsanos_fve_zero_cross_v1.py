"""katsanos-fve-zero-cross — Katsanos Finite Volume Elements zero-cross.

LOCKED ENCODE ORDER #1.
Thesis:
  Stage25 NHNL BTC 1.687x -> ETH 1.085x FAIL (n=8 THIN) + DSP/VROC/thermo 0 BTC —
  need published short-term money-flow zero-cross denser than NHNL for ETH-after-BTC
  without cloning Katsanos-VFI EXIT.
  FVE (Markos Katsanos, S&C Apr 2003 / Sep 2003):
    TP = (high + low + close) / 3
    intra = log(high) - log(low) (guard <=0)
    vintra = stdev(intra, Samples)
    inter = log(TP) - log(TP[1]) (guard <=0)
    vinter = stdev(inter, Samples)
    CutOff = (CINTRA * vintra + CINTER * vinter) * close
    MF = (close - (high + low) / 2) + (TP - TP[1])
    FveFactor = +1.0 if MF > CutOff else (-1.0 if MF < -CutOff else 0.0)
    FVE = 100 * sum(volume * FveFactor, Samples) / (sma(volume, Samples) * Samples)
  Mode A:
    long crossover(fve, 0)
    exit crossunder(fve, 0)
  Mode B:
    require fve > sma(fve, mal) mal in {10, 20} — only if Mode A over-whips;
    identical params across all four coins.
  Prefer Samples=22, CINTRA=CINTER=0.1 Mode A.
  != VFI (interday MF + volume cap / vave) / != VPCI / != VZO / != AccDist.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill fail past 1.20;
  Kill Samples inflate until n collapses;
  Kill VFI/VPCI/VZO/AccDist labeled FVE. Prefer Mode A Samples=22, 1H+.

eth_smoke:
  CRITICAL: Kill BTC clear then ETH under 1.2x; Kill ETH n thin ~8;
  Kill params retuned only on ETH; Kill VFI labeled FVE. Prefer identical; denser n >> 9.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; Kill Samples retuned only on SOL;
  15m spam; stage12-25 grafts. Prefer denser n >> 9.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill Samples retuned only on BNB;
  Mode B only on BNB. Prefer identical; long-only; ATR exit.

Forbidden: VFI/VPCI/VZO/Bostian/AccDist/CLV labeled FVE;
request.security; stage12-25 grafts; SOL/BNB-only retune.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, katsanos_fve, sma

STRATEGY_ID = "katsanos-fve-zero-cross"


@dataclass(frozen=True)
class KatsanosFveParams:
    mode: str = "mode_a"          # "mode_a" | "mode_b"
    samples: int = 22             # 14, 18, 22, 30
    cintra: float = 0.1
    cinter: float = 0.1
    mal: int = 10                 # for mode_b
    atr_trail_mult: float = 0.0   # 0.0 (off), 1.5, 2.0
    atr_len: int = 14


def validate_btc_smoke(params: KatsanosFveParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC LEAD PRIMARY CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.samples not in {14, 18, 22, 30}:
        return False, f"btc_smoke: samples={params.samples} not in {{14, 18, 22, 30}}"
    return True, "PASS"


def validate_eth_smoke(params: KatsanosFveParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (ETH-after-BTC PRIMARY CRITICAL)."""
    if params.samples not in {14, 18, 22, 30}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: KatsanosFveParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m":
        return False, "sol_smoke: 15m forbidden"
    if params.samples not in {14, 18, 22, 30}:
        return False, "sol_smoke: parameters not in locked set (never SOL-only retune)"
    return True, "PASS"


def validate_bnb_smoke(params: KatsanosFveParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (BNB-SURVIVAL)."""
    if params.samples not in {14, 18, 22, 30}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: KatsanosFveParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for katsanos-fve-zero-cross."""
    params = params or KatsanosFveParams()
    count = len(bars)
    buys = [False] * count
    sells = [False] * count
    stops: list[float | None] = [None] * count
    if count == 0:
        return buys, sells, stops

    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    volumes = [b.volume for b in bars]

    atr_vals = atr(highs, lows, closes, params.atr_len)
    fve_vals = katsanos_fve(
        highs, lows, closes, volumes,
        samples=params.samples,
        cintra=params.cintra,
        cinter=params.cinter,
    )

    fve_ma = sma([x if x is not None else 0.0 for x in fve_vals], params.mal) if params.mode == "mode_b" else None

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, count):
        c = closes[i]
        h = highs[i]
        cur_fve = fve_vals[i]
        prev_fve = fve_vals[i - 1]

        if cur_fve is None or prev_fve is None:
            continue

        co_zero = (prev_fve <= 0.0) and (cur_fve > 0.0)
        cu_zero = (prev_fve >= 0.0) and (cur_fve < 0.0)

        # Long entry logic
        if not in_pos:
            entry_cond = co_zero
            if params.mode == "mode_b" and fve_ma is not None and fve_ma[i] is not None:
                entry_cond = entry_cond and (cur_fve > fve_ma[i])

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

            exit_cond = cu_zero or atr_stop_hit
            if exit_cond:
                sells[i] = True
                in_pos = False
                stops[i] = None

    return buys, sells, stops
