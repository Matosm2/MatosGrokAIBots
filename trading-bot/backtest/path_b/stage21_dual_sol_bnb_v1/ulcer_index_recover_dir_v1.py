"""ulcer-index-recover-dir — Peter Martin Ulcer Index recover x close-direction.

LOCKED ENCODE ORDER #3.
Thesis:
  Stage20 mid-cycle oscillators 0 BTC chop.
  Ulcer Index (Martin/McCann):
    hh = highest(close, uiLen)
    pd = 100.0 * (close - hh) / hh
    ui = sqrt(sma(pd * pd, uiLen))
    recover = ui < ui[1]
    bull = close > close[dirLen]
  Mode A = long rising-edge (recover and bull); exit when not (or ui > ui[1]).
  Mode B = sig = sma(ui, smaLen); long on crossunder(ui, sig) x bull — only if
  Mode A over-whips; identical params across all four coins.
  Prefer (14, 1) Mode A.
  != Mass Index / != ATR%ile / != VHF / != RAVI.

btc_smoke:
  CRITICAL: Kill Mode A BTC 0/chop; Kill uiLen inflate until n collapses;
  Kill Mass/ATR%ile/VHF/RAVI substitute. Prefer Mode A (14,1), 1H+.

eth_smoke:
  Kill BTC clear then ETH under 1.2x; Kill uiLen retuned only on ETH. Prefer identical.

sol_smoke:
  Kill BTC+ETH clear then SOL under 1.2x; 15m uiLen=5; stage12-20 grafts.
  Retention: SOL multi-dozen after ETH.

bnb_smoke:
  Kill 3-coin clear then BNB quiet wipe; Kill uiLen retuned only on BNB;
  Mode B only on BNB; ungated shorts; no ATR. Prefer identical; long-only; ATR.

Forbidden: Mass/ATR%ile/VHF/RAVI labeled UI; direction-blind UI-alone;
request.security; stage12-20 grafts.
Closed-bar only; long-only spot first; pyramiding 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.data import Bar
from backtest.indicators import atr, crossunder, sma, ulcer_index

STRATEGY_ID = "ulcer-index-recover-dir"


@dataclass(frozen=True)
class UlcerParams:
    mode: str = "mode_a"  # "mode_a" | "mode_b"
    ui_len: int = 14
    dir_len: int = 1
    sma_len: int = 0  # 0 = raw recover (ui < ui[1]); >0 = sma crossunder
    atr_trail_mult: float = 0.0
    atr_len: int = 14


def validate_btc_smoke(params: UlcerParams, tf: str) -> tuple[bool, str]:
    """Mandatory btc_smoke validation."""
    if tf == "15m":
        return False, "btc_smoke: 15m forbidden (1H+ required)"
    if params.ui_len not in {10, 14, 20}:
        return False, f"btc_smoke: ui_len={params.ui_len} not in locked sweep {{10, 14, 20}}"
    if params.dir_len not in {1, 3}:
        return False, f"btc_smoke: dir_len={params.dir_len} not in locked sweep {{1, 3}}"
    if params.sma_len not in {0, 5}:
        return False, f"btc_smoke: sma_len={params.sma_len} not in locked sweep {{0, 5}}"
    if params.ui_len > 35:
        return False, f"btc_smoke: ui_len={params.ui_len} collapses BTC n"
    return True, "PASS"


def validate_eth_smoke(params: UlcerParams, tf: str) -> tuple[bool, str]:
    """Mandatory eth_smoke validation (BTC->ETH PORTABILITY)."""
    if params.ui_len not in {10, 14, 20} or params.dir_len not in {1, 3} or params.sma_len not in {0, 5}:
        return False, "eth_smoke: parameters retuned away from locked set"
    return True, "PASS"


def validate_sol_smoke(params: UlcerParams, tf: str) -> tuple[bool, str]:
    """Mandatory sol_smoke validation (SOL-after-BTC+ETH)."""
    if tf == "15m" and params.ui_len <= 5:
        return False, "sol_smoke: 15m ui_len<=5 forbidden (spam)"
    if params.ui_len not in {10, 14, 20} or params.dir_len not in {1, 3} or params.sma_len not in {0, 5}:
        return False, "sol_smoke: parameters not in locked set"
    return True, "PASS"


def validate_bnb_smoke(params: UlcerParams, tf: str) -> tuple[bool, str]:
    """Mandatory bnb_smoke validation (CRITICAL after 3-coin)."""
    if params.ui_len not in {10, 14, 20} or params.dir_len not in {1, 3} or params.sma_len not in {0, 5}:
        return False, "bnb_smoke: parameters not in locked set"
    return True, "PASS"


def compute_signals(
    bars: list[Bar],
    params: UlcerParams | None = None,
) -> tuple[list[bool], list[bool], list[float | None]]:
    """Compute buys, sells, and stops for ulcer-index-recover-dir."""
    params = params or UlcerParams()
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
    ui_vals = ulcer_index(closes, ui_len=params.ui_len)

    sig_vals: list[float | None] = [None] * n
    if params.mode == "mode_b" and params.sma_len > 0:
        valid_ui: list[float] = [v if v is not None else 0.0 for v in ui_vals]
        sig_vals = sma(valid_ui, params.sma_len)

    in_pos = False
    highest_since_entry = 0.0
    prev_long_cond = False

    min_bar = max(1, params.dir_len)

    for i in range(min_bar, n):
        c = closes[i]
        h = highs[i]

        ui_cur = ui_vals[i]
        ui_prev = ui_vals[i - 1]

        if params.mode == "mode_b" and params.sma_len > 0:
            recover = crossunder(ui_vals, sig_vals, i)
        else:
            recover = bool(ui_cur is not None and ui_prev is not None and ui_cur < ui_prev)

        c_dir_prev = closes[i - params.dir_len]
        bull = c > c_dir_prev

        long_cond = recover and bull
        rising_edge = long_cond and not prev_long_cond

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

            # Exit when long_cond ceases (pain increases or bull lost)
            ui_worsened = bool(ui_cur is not None and ui_prev is not None and ui_cur > ui_prev)
            exit_trigger = stop_hit or (not long_cond) or ui_worsened
            if exit_trigger:
                sells[i] = True
                in_pos = False
                stops[i] = None

        prev_long_cond = long_cond

    return buys, sells, stops
