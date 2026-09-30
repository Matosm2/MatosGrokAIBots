"""ppo-ema-signal-cross — Percentage Price Oscillator x EMA signal cross.

LOCKED ENCODE ORDER #2 (BTC LEAD + ETH-PORTABLE PRIMARY).
Thesis:
  Stage17 volume-intensity (III) overfit BTC then wiped ETH.
  PPO is %-scaled EMA spread (close-only):
    ppo = 100 * (ema(close, fast) - ema(close, slow)) / ema(close, slow)
    sig = ema(ppo, sigLen)
  Mode A = PPO x signal cross.
  Percentage scale is cross-asset / ETH-portable vs absolute MACD dual-mom burn
  and vs PVO (volume) stage4. Identical (12,26,9) on all four coins.
  != PVO (stage4).
  != absolute MACD dual-mom.
  != free EMA dual without %-scale.

Formula:
  ppo = 100*(ema(close,fast)-ema(close,slow))/ema(close,slow)
  sig = ema(ppo,sigLen)
  Prefer (12,26,9). Mode A PPO x sig.

Mode A (BTC-LEAD + ETH-portable PRIMARY — prefer):
  long: crossover(ppo, sig)
  exit: crossunder(ppo, sig)

Mode B (BNB quiet / Mode A+ zero bias):
  Mode A+ require ppo > 0 / longer slow — only if Mode A over-whips; identical params.

btc_smoke:
  BTC-LEAD CRITICAL: Kill (fast,slow,sig) inflate until n collapses;
  Kill PVO/MACD-hist substitute;
  Kill Mode B forced while Mode A BTC healthy. Prefer Mode A (12,26,9), 1H+.

eth_smoke:
  BTC->ETH PRIMARY CRITICAL: Kill BTC clear then ETH under 1.2x;
  Kill params retuned only on ETH; Kill PVO/III/absolute-MACD labeled PPO.
  Prefer identical (12,26,9); ETH n multi-dozen.

sol_smoke:
  SOL-after-BTC+ETH CRITICAL: Kill BTC+ETH clear then SOL under 1.2x;
  Kill PVO labeled PPO; 15m (5,13,3) spam; stage12-17 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  CRITICAL after 3-coin: different (fast,slow,sig); Mode B shorts ungated; no ATR.
  Prefer identical; long-only; ATR.

Forbidden: PVO; absolute MACD hist primary; free EMA dual without %-scale; III/CMF/OBV; stage12-17.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossover, crossunder, percentage_price_oscillator

STRATEGY_ID = "ppo-ema-signal-cross"


@dataclass(frozen=True)
class PpoParams:
    mode: str = "mode_a"  # "mode_a" (ppo x sig) | "mode_b" (ppo x sig + ppo > 0)
    fast: int = 12
    slow: int = 26
    sig: int = 9
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: PpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation (BTC-LEAD CRITICAL)."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.fast not in {8, 12}:
        return False, f"btc_smoke: fast={params.fast} not in locked sweep {{8, 12}}"
    if params.slow not in {21, 26}:
        return False, f"btc_smoke: slow={params.slow} not in locked sweep {{21, 26}}"
    if params.sig not in {5, 9}:
        return False, f"btc_smoke: sig={params.sig} not in locked sweep {{5, 9}}"
    return True, "PASS"


def validate_eth_smoke(params: PpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PRIMARY CRITICAL)."""
    if params.fast not in {8, 12} or params.slow not in {21, 26} or params.sig not in {5, 9}:
        return False, "eth_smoke: params retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: PpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH CRITICAL)."""
    if tf == "15m" and (params.fast <= 5 or params.slow <= 13):
        return False, "sol_smoke: 15m (5,13,3) forbidden (spam)"
    if params.fast not in {8, 12} or params.slow not in {21, 26} or params.sig not in {5, 9}:
        return False, "sol_smoke: params not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: PpoParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.fast not in {8, 12} or params.slow not in {21, 26} or params.sig not in {5, 9}:
        return False, "bnb_smoke: params not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: PpoParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ppo-ema-signal-cross."""
    params = params or PpoParams()
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
    ppo_vals, sig_vals, _ = percentage_price_oscillator(
        closes, fast_length=params.fast, slow_length=params.slow, signal_length=params.sig
    )

    in_pos = False
    highest_since_entry = 0.0

    for i in range(1, n):
        c = closes[i]
        h = highs[i]

        cross_up = crossover(ppo_vals, sig_vals, i)
        cross_dn = crossunder(ppo_vals, sig_vals, i)

        if params.mode == "mode_b":
            # Mode B: require ppo > 0
            val = ppo_vals[i]
            if val is None or val <= 0.0:
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
