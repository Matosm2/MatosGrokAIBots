"""Pure-Python EMA and RSI (Wilder) matching TradingView/Pine semantics."""

from __future__ import annotations

import math


def ema(values: list[float], length: int) -> list[float | None]:
    """Exponential moving average. Seed = SMA of first `length` closes (Pine/TV)."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    seed = sum(values[:length]) / length
    out[length - 1] = seed
    mult = 2.0 / (length + 1)
    prev = seed
    for i in range(length, n):
        prev = (values[i] - prev) * mult + prev
        out[i] = prev
    return out


def rsi(values: list[float], length: int = 14) -> list[float | None]:
    """Wilder RSI as used by TradingView `ta.rsi`."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return out

    gains = 0.0
    losses = 0.0
    for i in range(1, length + 1):
        diff = values[i] - values[i - 1]
        if diff >= 0:
            gains += diff
        else:
            losses -= diff
    avg_gain = gains / length
    avg_loss = losses / length

    def _rsi(ag: float, al: float) -> float:
        if al == 0:
            return 100.0
        rs = ag / al
        return 100.0 - (100.0 / (1.0 + rs))

    out[length] = _rsi(avg_gain, avg_loss)

    for i in range(length + 1, n):
        diff = values[i] - values[i - 1]
        gain = diff if diff > 0 else 0.0
        loss = -diff if diff < 0 else 0.0
        avg_gain = (avg_gain * (length - 1) + gain) / length
        avg_loss = (avg_loss * (length - 1) + loss) / length
        out[i] = _rsi(avg_gain, avg_loss)
    return out


def crossover(a: list[float | None], b: list[float | None], i: int) -> bool:
    """True when a crosses above b on bar i (Pine ta.crossover)."""
    if i < 1:
        return False
    ai, bi = a[i], b[i]
    ap, bp = a[i - 1], b[i - 1]
    if ai is None or bi is None or ap is None or bp is None:
        return False
    return ap <= bp and ai > bi


def crossunder(a: list[float | None], b: list[float | None], i: int) -> bool:
    """True when a crosses below b on bar i (Pine ta.crossunder)."""
    if i < 1:
        return False
    ai, bi = a[i], b[i]
    ap, bp = a[i - 1], b[i - 1]
    if ai is None or bi is None or ap is None or bp is None:
        return False
    return ap >= bp and ai < bi


def sma(values: list[float], length: int) -> list[float | None]:
    """Simple moving average. First value at index length-1."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    window = sum(values[:length])
    out[length - 1] = window / length
    for i in range(length, n):
        window += values[i] - values[i - length]
        out[i] = window / length
    return out


def true_range(
    highs: list[float], lows: list[float], closes: list[float]
) -> list[float | None]:
    """True range; index 0 is high-low only (no prior close)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0:
        return out
    out[0] = highs[0] - lows[0]
    for i in range(1, n):
        out[i] = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
    return out


def rma(values: list[float | None], length: int) -> list[float | None]:
    """Wilder RMA (TradingView ta.rma). Seeds with SMA of first `length` contiguous values."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    nums: list[float] = []
    seeded = False
    prev = 0.0
    for i, v in enumerate(values):
        if v is None:
            nums = []
            seeded = False
            continue
        if not seeded:
            nums.append(v)
            if len(nums) == length:
                prev = sum(nums) / length
                out[i] = prev
                seeded = True
            continue
        prev = (prev * (length - 1) + v) / length
        out[i] = prev
    return out


def atr(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> list[float | None]:
    """Average True Range (Wilder), Pine ta.atr."""
    tr = true_range(highs, lows, closes)
    return rma(tr, length)


def bollinger(
    closes: list[float],
    length: int = 20,
    mult: float = 2.0,
) -> tuple[list[float | None], list[float | None], list[float | None], list[float | None]]:
    """
    Bollinger Bands: mid=SMA, upper/lower = mid ± mult*stdev (population of window).
    Also returns bb_width = (upper-lower)/mid when mid>0.
    """
    n = len(closes)
    mid = sma(closes, length)
    upper: list[float | None] = [None] * n
    lower: list[float | None] = [None] * n
    width: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return mid, upper, lower, width
    for i in range(length - 1, n):
        window = closes[i - length + 1 : i + 1]
        m = mid[i]
        if m is None:
            continue
        mean = m
        var = sum((x - mean) ** 2 for x in window) / length
        sd = var ** 0.5
        u = mean + mult * sd
        lo = mean - mult * sd
        upper[i] = u
        lower[i] = lo
        if mean != 0:
            width[i] = (u - lo) / mean
    return mid, upper, lower, width


def efficiency_ratio(closes: list[float], length: int = 10) -> list[float | None]:
    """Kaufman Efficiency Ratio over `length` bars: |change|/sum(|bar changes|)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return out
    for i in range(length, n):
        change = abs(closes[i] - closes[i - length])
        volatility = 0.0
        for j in range(i - length + 1, i + 1):
            volatility += abs(closes[j] - closes[j - 1])
        out[i] = (change / volatility) if volatility > 0 else 0.0
    return out


def kama(
    closes: list[float],
    length: int = 10,
    fast: int = 2,
    slow: int = 30,
) -> list[float | None]:
    """Kaufman Adaptive Moving Average (Pine-like)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return out
    er = efficiency_ratio(closes, length)
    fast_sc = 2.0 / (fast + 1)
    slow_sc = 2.0 / (slow + 1)
    # Seed KAMA at first ER bar with close
    first = None
    for i in range(n):
        if er[i] is None:
            continue
        if first is None:
            out[i] = closes[i]
            first = i
            prev = closes[i]
            continue
        e = er[i]
        sc = (e * (fast_sc - slow_sc) + slow_sc) ** 2
        prev = prev + sc * (closes[i] - prev)
        out[i] = prev
    return out


def supertrend(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    atr_len: int = 10,
    mult: float = 3.0,
) -> tuple[list[float | None], list[int | None]]:
    """
    SuperTrend (ATR-based). Returns (st_line, direction) where direction is
    +1 bullish / -1 bearish (None until ATR ready).
    Classic: basic upper/lower bands from HL2 ± mult*ATR; trail in trend direction.
    """
    n = len(closes)
    st: list[float | None] = [None] * n
    direction: list[int | None] = [None] * n
    atr_s = atr(highs, lows, closes, atr_len)
    final_upper: list[float | None] = [None] * n
    final_lower: list[float | None] = [None] * n
    for i in range(n):
        a = atr_s[i]
        if a is None:
            continue
        hl2 = (highs[i] + lows[i]) / 2.0
        basic_upper = hl2 + mult * a
        basic_lower = hl2 - mult * a
        if i == 0 or final_lower[i - 1] is None or final_upper[i - 1] is None:
            final_upper[i] = basic_upper
            final_lower[i] = basic_lower
            # bootstrap: close vs mid
            if closes[i] >= hl2:
                direction[i] = 1
                st[i] = final_lower[i]
            else:
                direction[i] = -1
                st[i] = final_upper[i]
            continue
        prev_fu = final_upper[i - 1]
        prev_fl = final_lower[i - 1]
        # final upper: lower of basic_upper and prev final_upper if close[i-1] <= prev_fu
        if closes[i - 1] <= prev_fu:
            final_upper[i] = min(basic_upper, prev_fu)
        else:
            final_upper[i] = basic_upper
        if closes[i - 1] >= prev_fl:
            final_lower[i] = max(basic_lower, prev_fl)
        else:
            final_lower[i] = basic_lower
        prev_dir = direction[i - 1]
        assert prev_dir is not None
        if prev_dir == 1:
            if closes[i] < final_lower[i]:
                direction[i] = -1
                st[i] = final_upper[i]
            else:
                direction[i] = 1
                st[i] = final_lower[i]
        else:
            if closes[i] > final_upper[i]:
                direction[i] = 1
                st[i] = final_lower[i]
            else:
                direction[i] = -1
                st[i] = final_upper[i]
    return st, direction


def adx_di(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """
    Wilder +DI, -DI, ADX (TradingView ta.dmi / ta.adx semantics).

    Returns (plus_di, minus_di, adx).
    """
    n = len(closes)
    plus_di: list[float | None] = [None] * n
    minus_di: list[float | None] = [None] * n
    adx: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return plus_di, minus_di, adx

    tr: list[float | None] = [None] * n
    plus_dm: list[float | None] = [None] * n
    minus_dm: list[float | None] = [None] * n
    tr[0] = highs[0] - lows[0]
    plus_dm[0] = 0.0
    minus_dm[0] = 0.0
    for i in range(1, n):
        up = highs[i] - highs[i - 1]
        down = lows[i - 1] - lows[i]
        plus_dm[i] = up if up > down and up > 0 else 0.0
        minus_dm[i] = down if down > up and down > 0 else 0.0
        tr[i] = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )

    atr_s = rma(tr, length)
    plus_s = rma(plus_dm, length)
    minus_s = rma(minus_dm, length)

    dx: list[float | None] = [None] * n
    for i in range(n):
        a, p, m = atr_s[i], plus_s[i], minus_s[i]
        if a is None or p is None or m is None or a == 0:
            continue
        plus_di[i] = 100.0 * p / a
        minus_di[i] = 100.0 * m / a
        s = plus_di[i] + minus_di[i]
        if s == 0:
            dx[i] = 0.0
        else:
            dx[i] = 100.0 * abs(plus_di[i] - minus_di[i]) / s

    adx = rma(dx, length)
    return plus_di, minus_di, adx


def percent_rank(values: list[float], length: int) -> list[float | None]:
    """Percent rank of values[i] vs prior `length` values (inclusive of current).

    Returns 0..100: fraction of the window (including current) that is <= values[i],
    times 100. Classic Connors uses ROC(1) percent-rank over 100 bars.
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    for i in range(length - 1, n):
        window = values[i - length + 1 : i + 1]
        cur = values[i]
        # count how many in window are <= cur
        le = sum(1 for x in window if x <= cur)
        out[i] = 100.0 * le / length
    return out


def streak_series(closes: list[float]) -> list[float]:
    """Connors up/down streak: +n consecutive up closes, -n consecutive down."""
    n = len(closes)
    out = [0.0] * n
    for i in range(1, n):
        if closes[i] > closes[i - 1]:
            out[i] = out[i - 1] + 1.0 if out[i - 1] > 0 else 1.0
        elif closes[i] < closes[i - 1]:
            out[i] = out[i - 1] - 1.0 if out[i - 1] < 0 else -1.0
        else:
            out[i] = 0.0
    return out


def connors_rsi(
    closes: list[float],
    rsi_len: int = 3,
    streak_rsi_len: int = 2,
    percent_rank_len: int = 100,
) -> list[float | None]:
    """Classic Connors RSI CRSI(rsi_len, streak_rsi_len, percent_rank_len).

    CRSI = (RSI(close, rsi_len) + RSI(streak, streak_rsi_len) + PercentRank(ROC1, percent_rank_len)) / 3
    Default CRSI(3,2,100).
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    rsi_c = rsi(closes, rsi_len)
    streaks = streak_series(closes)
    rsi_s = rsi(streaks, streak_rsi_len)
    # ROC(1) = close[i]/close[i-1] - 1; index 0 = 0
    roc1 = [0.0] * n
    for i in range(1, n):
        prev = closes[i - 1]
        roc1[i] = ((closes[i] / prev) - 1.0) if prev != 0 else 0.0
    pr = percent_rank(roc1, percent_rank_len)
    for i in range(n):
        a, b, c = rsi_c[i], rsi_s[i], pr[i]
        if a is None or b is None or c is None:
            continue
        out[i] = (a + b + c) / 3.0
    return out


def heikin_ashi(
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
) -> tuple[list[float], list[float], list[float], list[float]]:
    """Heikin-Ashi OHLC. HA open[0] = (open[0]+close[0])/2."""
    n = len(closes)
    ha_open = [0.0] * n
    ha_close = [0.0] * n
    ha_high = [0.0] * n
    ha_low = [0.0] * n
    if n == 0:
        return ha_open, ha_high, ha_low, ha_close
    ha_close[0] = (opens[0] + highs[0] + lows[0] + closes[0]) / 4.0
    ha_open[0] = (opens[0] + closes[0]) / 2.0
    ha_high[0] = max(highs[0], ha_open[0], ha_close[0])
    ha_low[0] = min(lows[0], ha_open[0], ha_close[0])
    for i in range(1, n):
        ha_close[i] = (opens[i] + highs[i] + lows[i] + closes[i]) / 4.0
        ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2.0
        ha_high[i] = max(highs[i], ha_open[i], ha_close[i])
        ha_low[i] = min(lows[i], ha_open[i], ha_close[i])
    return ha_open, ha_high, ha_low, ha_close


def obv(closes: list[float], volumes: list[float]) -> list[float]:
    """On-Balance Volume. Cumulative; flat close adds 0."""
    n = len(closes)
    out = [0.0] * n
    if n == 0:
        return out
    out[0] = volumes[0]
    for i in range(1, n):
        if closes[i] > closes[i - 1]:
            out[i] = out[i - 1] + volumes[i]
        elif closes[i] < closes[i - 1]:
            out[i] = out[i - 1] - volumes[i]
        else:
            out[i] = out[i - 1]
    return out


def ichimoku(
    highs: list[float],
    lows: list[float],
    tenkan_len: int = 9,
    kijun_len: int = 26,
    senkou_b_len: int = 52,
    displacement: int = 26,
) -> tuple[
    list[float | None],
    list[float | None],
    list[float | None],
    list[float | None],
    list[float | None],
]:
    """Classic Ichimoku 9/26/52 with displacement 26.

    Returns (tenkan, kijun, senkou_a, senkou_b, cloud_top) where senkou_* are
    plotted at bar i using values computed `displacement` bars earlier
    (no lookahead: cloud at i uses midpoints from i-displacement).
    cloud_top = max(senkou_a, senkou_b); use min for cloud bottom separately.
    """
    n = len(highs)
    tenkan: list[float | None] = [None] * n
    kijun: list[float | None] = [None] * n
    senkou_a: list[float | None] = [None] * n
    senkou_b: list[float | None] = [None] * n
    cloud_top: list[float | None] = [None] * n

    def _mid(i: int, length: int) -> float | None:
        if i + 1 < length:
            return None
        window_h = highs[i - length + 1 : i + 1]
        window_l = lows[i - length + 1 : i + 1]
        return (max(window_h) + min(window_l)) / 2.0

    raw_a: list[float | None] = [None] * n
    raw_b: list[float | None] = [None] * n
    for i in range(n):
        tenkan[i] = _mid(i, tenkan_len)
        kijun[i] = _mid(i, kijun_len)
        if tenkan[i] is not None and kijun[i] is not None:
            raw_a[i] = (tenkan[i] + kijun[i]) / 2.0
        raw_b[i] = _mid(i, senkou_b_len)

    for i in range(n):
        src = i - displacement
        if src >= 0:
            senkou_a[i] = raw_a[src]
            senkou_b[i] = raw_b[src]
            if senkou_a[i] is not None and senkou_b[i] is not None:
                cloud_top[i] = max(senkou_a[i], senkou_b[i])
    return tenkan, kijun, senkou_a, senkou_b, cloud_top



def parabolic_sar(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    *,
    af_start: float = 0.02,
    af_step: float = 0.02,
    af_max: float = 0.2,
) -> list[float | None]:
    """Wilder Parabolic SAR (Pine ta.sar / TradingView default).

    Returns SAR value per bar. First bar is None (needs prior extreme).
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n < 2:
        return out

    # Seed: assume uptrend if close[1] >= close[0], else downtrend
    bull = closes[1] >= closes[0]
    af = af_start
    ep = highs[0] if bull else lows[0]
    sar = lows[0] if bull else highs[0]
    out[0] = None

    for i in range(1, n):
        prev_sar = sar
        # Advance SAR
        sar = prev_sar + af * (ep - prev_sar)

        # Clamp SAR so it does not penetrate prior two bars' extremes
        if bull:
            if i >= 2:
                sar = min(sar, lows[i - 1], lows[i - 2])
            else:
                sar = min(sar, lows[i - 1])
        else:
            if i >= 2:
                sar = max(sar, highs[i - 1], highs[i - 2])
            else:
                sar = max(sar, highs[i - 1])

        # Check flip
        if bull:
            if lows[i] < sar:
                bull = False
                sar = ep
                ep = lows[i]
                af = af_start
            else:
                if highs[i] > ep:
                    ep = highs[i]
                    af = min(af + af_step, af_max)
        else:
            if highs[i] > sar:
                bull = True
                sar = ep
                ep = highs[i]
                af = af_start
            else:
                if lows[i] < ep:
                    ep = lows[i]
                    af = min(af + af_step, af_max)

        out[i] = sar
    return out


def cci(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 20,
    constant: float = 0.015,
) -> list[float | None]:
    """Commodity Channel Index (Pine ta.cci)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    tp = [(highs[i] + lows[i] + closes[i]) / 3.0 for i in range(n)]
    for i in range(length - 1, n):
        window = tp[i - length + 1 : i + 1]
        mean = sum(window) / length
        md = sum(abs(x - mean) for x in window) / length
        if md == 0.0:
            out[i] = 0.0
        else:
            out[i] = (tp[i] - mean) / (constant * md)
    return out


def aroon(
    highs: list[float],
    lows: list[float],
    length: int = 25,
) -> tuple[list[float | None], list[float | None]]:
    """Aroon Up / Aroon Down (Pine ta.aroon). Window is `length` bars back inclusive.

    AroonUp = 100 * (length - bars_since_highest_high) / length
    AroonDown = 100 * (length - bars_since_lowest_low) / length
    First valid at index `length` (needs length+1 highs/lows spanning lookback).
    Pine uses highest/lowest over `length` periods looking back from prior bar
    through current: period = length, first at index length.
    """
    n = len(highs)
    up: list[float | None] = [None] * n
    down: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return up, down
    for i in range(length, n):
        # lookback window of `length` bars ending at i: [i-length+1 .. i] is length bars
        # Pine ta.aroon(length): period length, uses highest of high over length,
        # bars since = length - distance from start... Standard:
        # window [i - length : i] inclusive of i is length+1? TradingView:
        # aroon length N: lookback N bars (not including current? or including?)
        # Common: for i >= length, window highs[i-length+1:i+1] length bars,
        # bars_since_hh = length - 1 - argmax (0 = most recent)
        # Actually Pine: `100 * (highestbars(high, length+1) + length)/length` wait.
        # Standard formula used by most libs (and TV):
        #   AroonUp = 100 * (n - periods_since_hh) / n  where n = length
        #   periods_since_hh in [0, n] over window of n+1 bars [i-n .. i]
        window_h = highs[i - length : i + 1]  # length+1 bars
        window_l = lows[i - length : i + 1]
        # index of max high / min low within window (0 = oldest)
        hh_idx = max(range(len(window_h)), key=lambda k: window_h[k])
        ll_idx = min(range(len(window_l)), key=lambda k: window_l[k])
        bars_since_hh = (len(window_h) - 1) - hh_idx  # 0 if high is current
        bars_since_ll = (len(window_l) - 1) - ll_idx
        up[i] = 100.0 * (length - bars_since_hh) / length
        down[i] = 100.0 * (length - bars_since_ll) / length
    return up, down


def williams_r(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> list[float | None]:
    """Williams %R (Pine ta.wpr). Range typically [-100, 0]."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    for i in range(length - 1, n):
        hh = max(highs[i - length + 1 : i + 1])
        ll = min(lows[i - length + 1 : i + 1])
        denom = hh - ll
        if denom == 0.0:
            out[i] = 0.0 if closes[i] >= hh else -100.0
        else:
            out[i] = -100.0 * (hh - closes[i]) / denom
    return out


def vortex(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> tuple[list[float | None], list[float | None]]:
    """Vortex Indicator VI+ / VI− (Pine ta.vortex / TC2000).

    VI+ = sum(|H - prevL|, n) / sum(TR, n)
    VI− = sum(|L - prevH|, n) / sum(TR, n)
    """
    n = len(closes)
    vip: list[float | None] = [None] * n
    vim: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return vip, vim

    tr_s = true_range(highs, lows, closes)
    vm_plus = [0.0] * n
    vm_minus = [0.0] * n
    for i in range(1, n):
        vm_plus[i] = abs(highs[i] - lows[i - 1])
        vm_minus[i] = abs(lows[i] - highs[i - 1])

    # Rolling sums starting once we have `length` VM samples (from index 1)
    for i in range(length, n):
        # window i-length+1 .. i inclusive = length bars (all have VM from i>=1)
        sp = sum(vm_plus[i - length + 1 : i + 1])
        sm = sum(vm_minus[i - length + 1 : i + 1])
        tr_sum = 0.0
        ok = True
        for j in range(i - length + 1, i + 1):
            if tr_s[j] is None:
                ok = False
                break
            tr_sum += tr_s[j]  # type: ignore[operator]
        if not ok or tr_sum == 0.0:
            continue
        vip[i] = sp / tr_sum
        vim[i] = sm / tr_sum
    return vip, vim


def donchian(
    highs: list[float],
    lows: list[float],
    length: int,
) -> tuple[list[float | None], list[float | None]]:
    """Donchian channel upper/lower over the prior `length` bars (excludes current).

    upper[i] = max(highs[i-length : i])  # prior length highs
    lower[i] = min(lows[i-length : i])
    First usable index is `length` (needs length prior bars).
    """
    n = len(highs)
    upper: list[float | None] = [None] * n
    lower: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return upper, lower
    for i in range(length, n):
        upper[i] = max(highs[i - length : i])
        lower[i] = min(lows[i - length : i])
    return upper, lower


def _ema_skip_none(values: list[float | None], length: int) -> list[float | None]:
    """EMA over dense non-None values, mapped back to original indices."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0:
        return out
    dense: list[float] = []
    idx_map: list[int] = []
    for i, v in enumerate(values):
        if v is None:
            continue
        dense.append(v)
        idx_map.append(i)
    if len(dense) < length:
        return out
    smoothed = ema(dense, length)
    for j, i in enumerate(idx_map):
        out[i] = smoothed[j]
    return out


def tsi(
    closes: list[float],
    long_length: int = 25,
    short_length: int = 13,
) -> list[float | None]:
    """Blau True Strength Index (TradingView ta.tsi semantics).

    TSI = 100 * EMA(EMA(change, long), short) / EMA(EMA(|change|, long), short)
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if long_length <= 0 or short_length <= 0 or n < 2:
        return out
    change: list[float | None] = [None] * n
    abs_change: list[float | None] = [None] * n
    for i in range(1, n):
        c = closes[i] - closes[i - 1]
        change[i] = c
        abs_change[i] = abs(c)
    ds_pc = _ema_skip_none(_ema_skip_none(change, long_length), short_length)
    ds_apc = _ema_skip_none(_ema_skip_none(abs_change, long_length), short_length)
    for i in range(n):
        pc, apc = ds_pc[i], ds_apc[i]
        if pc is None or apc is None or apc == 0.0:
            continue
        out[i] = 100.0 * pc / apc
    return out


def schaff_stc(
    closes: list[float],
    fast_length: int = 23,
    slow_length: int = 50,
    cycle_length: int = 10,
    factor: float = 0.5,
) -> list[float | None]:
    """Schaff Trend Cycle (classic Doug Schaff; MACD stoch ×2 with factor smooth).

    Defaults STC(23, 50, 10) with factor 0.5.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if (
        fast_length <= 0
        or slow_length <= 0
        or cycle_length <= 0
        or n < max(fast_length, slow_length) + cycle_length
    ):
        return out

    e_fast = ema(closes, fast_length)
    e_slow = ema(closes, slow_length)
    macd: list[float | None] = [None] * n
    for i in range(n):
        if e_fast[i] is None or e_slow[i] is None:
            continue
        macd[i] = e_fast[i] - e_slow[i]  # type: ignore[operator]

    def _stoch_series(src: list[float | None], length: int) -> list[float | None]:
        st: list[float | None] = [None] * n
        for i in range(n):
            if i + 1 < length:
                continue
            window = src[i - length + 1 : i + 1]
            if any(x is None for x in window):
                continue
            vals = [float(x) for x in window]  # type: ignore[arg-type]
            hh = max(vals)
            ll = min(vals)
            if hh == ll:
                st[i] = 0.0 if vals[-1] >= hh else 100.0
            else:
                st[i] = 100.0 * (vals[-1] - ll) / (hh - ll)
        return st

    def _factor_smooth(src: list[float | None], f: float) -> list[float | None]:
        sm: list[float | None] = [None] * n
        prev: float | None = None
        for i in range(n):
            v = src[i]
            if v is None:
                continue
            if prev is None:
                prev = v
            else:
                prev = prev + f * (v - prev)
            sm[i] = prev
        return sm

    k1 = _stoch_series(macd, cycle_length)
    d1 = _factor_smooth(k1, factor)
    k2 = _stoch_series(d1, cycle_length)
    return _factor_smooth(k2, factor)


def roc(values: list[float], length: int) -> list[float | None]:
    """Rate of change in percent: 100 * (v[i] / v[i-length] - 1). Pine ta.roc."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return out
    for i in range(length, n):
        prev = values[i - length]
        if prev == 0.0:
            out[i] = 0.0
        else:
            out[i] = 100.0 * (values[i] / prev - 1.0)
    return out


def wma(values: list[float | None], length: int) -> list[float | None]:
    """Weighted moving average; most recent bar has weight `length` (Pine ta.wma)."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    denom = length * (length + 1) / 2.0
    for i in range(length - 1, n):
        window = values[i - length + 1 : i + 1]
        if any(v is None for v in window):
            continue
        s = 0.0
        for j, v in enumerate(window):
            s += float(v) * (j + 1)  # type: ignore[arg-type]
        out[i] = s / denom
    return out


def fisher_transform(
    highs: list[float],
    lows: list[float],
    length: int = 10,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Fisher Transform of median price (UsingTheFisherTransform.pdf).

    Price = (H+L)/2. Normalize over `length` with 0.33/0.67 smooth, clamp ±0.999,
    Fish = 0.5*ln((1+v)/(1-v)) + 0.5*Fish[1]. Trigger = Fish[1].
    Returns (fish, trigger).
    """
    n = len(highs)
    fish: list[float | None] = [None] * n
    trigger: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return fish, trigger

    value1 = 0.0
    prev_fish = 0.0
    for i in range(n):
        if i + 1 < length:
            continue
        price = (highs[i] + lows[i]) / 2.0
        window_p = [(highs[j] + lows[j]) / 2.0 for j in range(i - length + 1, i + 1)]
        hh = max(window_p)
        ll = min(window_p)
        if hh == ll:
            raw = 0.0
        else:
            raw = 0.33 * 2.0 * ((price - ll) / (hh - ll) - 0.5) + 0.67 * value1
        if raw > 0.99:
            raw = 0.999
        elif raw < -0.99:
            raw = -0.999
        value1 = raw
        cur = 0.5 * math.log((1.0 + value1) / (1.0 - value1)) + 0.5 * prev_fish
        fish[i] = cur
        if i >= 1 and fish[i - 1] is not None:
            trigger[i] = fish[i - 1]
        prev_fish = cur
    return fish, trigger


def coppock_curve(
    closes: list[float],
    roc_long: int = 14,
    roc_short: int = 11,
    wma_len: int = 10,
) -> list[float | None]:
    """Coppock = WMA(ROC(roc_long) + ROC(roc_short), wma_len)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    r_long = roc(closes, roc_long)
    r_short = roc(closes, roc_short)
    summed: list[float | None] = [None] * n
    for i in range(n):
        a, b = r_long[i], r_short[i]
        if a is None or b is None:
            continue
        summed[i] = a + b
    return wma(summed, wma_len)


def macd_hist(
    closes: list[float],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """MACD line, signal, histogram (EMA fast−slow; signal=EMA of MACD)."""
    n = len(closes)
    macd_line: list[float | None] = [None] * n
    signal_line: list[float | None] = [None] * n
    hist: list[float | None] = [None] * n
    if fast <= 0 or slow <= 0 or signal <= 0 or n < slow:
        return macd_line, signal_line, hist
    e_fast = ema(closes, fast)
    e_slow = ema(closes, slow)
    for i in range(n):
        if e_fast[i] is None or e_slow[i] is None:
            continue
        macd_line[i] = e_fast[i] - e_slow[i]  # type: ignore[operator]
    signal_line = _ema_skip_none(macd_line, signal)
    for i in range(n):
        if macd_line[i] is None or signal_line[i] is None:
            continue
        hist[i] = macd_line[i] - signal_line[i]  # type: ignore[operator]
    return macd_line, signal_line, hist


def force_index(
    closes: list[float], volumes: list[float]
) -> list[float | None]:
    """Elder Force Index raw: (close − close[1]) × volume."""
    n = len(closes)
    out: list[float | None] = [None] * n
    for i in range(1, n):
        out[i] = (closes[i] - closes[i - 1]) * volumes[i]
    return out


def cmf(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    length: int = 21,
) -> list[float | None]:
    """Chaikin Money Flow over `length` bars."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    mfv: list[float] = [0.0] * n
    for i in range(n):
        hl = highs[i] - lows[i]
        if hl == 0.0:
            clv = 0.0
        else:
            clv = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / hl
        mfv[i] = clv * volumes[i]
    sum_mfv = sum(mfv[:length])
    sum_vol = sum(volumes[:length])
    out[length - 1] = (sum_mfv / sum_vol) if sum_vol != 0.0 else 0.0
    for i in range(length, n):
        sum_mfv += mfv[i] - mfv[i - length]
        sum_vol += volumes[i] - volumes[i - length]
        out[i] = (sum_mfv / sum_vol) if sum_vol != 0.0 else 0.0
    return out


def mfi(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    length: int = 14,
) -> list[float | None]:
    """Money Flow Index (volume-weighted RSI of typical price)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return out
    tp = [(highs[i] + lows[i] + closes[i]) / 3.0 for i in range(n)]
    pos_mf = [0.0] * n
    neg_mf = [0.0] * n
    for i in range(1, n):
        raw = tp[i] * volumes[i]
        if tp[i] > tp[i - 1]:
            pos_mf[i] = raw
        elif tp[i] < tp[i - 1]:
            neg_mf[i] = raw
    for i in range(length, n):
        pos = sum(pos_mf[i - length + 1 : i + 1])
        neg = sum(neg_mf[i - length + 1 : i + 1])
        if neg == 0.0:
            out[i] = 100.0
        else:
            ratio = pos / neg
            out[i] = 100.0 - (100.0 / (1.0 + ratio))
    return out


def linreg_channel(
    closes: list[float],
    length: int = 20,
    k_sigma: float = 2.0,
) -> tuple[
    list[float | None],
    list[float | None],
    list[float | None],
    list[float | None],
    list[float | None],
]:
    """Rolling linear regression mid / ±kσ bands / slope / R².

    Returns (mid, upper, lower, slope, r2).
    """
    n = len(closes)
    mid: list[float | None] = [None] * n
    upper: list[float | None] = [None] * n
    lower: list[float | None] = [None] * n
    slope: list[float | None] = [None] * n
    r2: list[float | None] = [None] * n
    if length <= 1 or n < length:
        return mid, upper, lower, slope, r2
    # Precompute x stats for 0..L-1
    xs = list(range(length))
    x_mean = (length - 1) / 2.0
    ss_xx = sum((x - x_mean) ** 2 for x in xs)
    for i in range(length - 1, n):
        window = closes[i - length + 1 : i + 1]
        y_mean = sum(window) / length
        ss_xy = sum((xs[j] - x_mean) * (window[j] - y_mean) for j in range(length))
        b = ss_xy / ss_xx if ss_xx != 0.0 else 0.0
        a = y_mean - b * x_mean
        fitted = [a + b * xs[j] for j in range(length)]
        resid = [window[j] - fitted[j] for j in range(length)]
        ss_res = sum(r * r for r in resid)
        ss_tot = sum((y - y_mean) ** 2 for y in window)
        sigma = math.sqrt(ss_res / length) if length > 0 else 0.0
        mid_i = fitted[-1]
        mid[i] = mid_i
        upper[i] = mid_i + k_sigma * sigma
        lower[i] = mid_i - k_sigma * sigma
        slope[i] = b
        r2[i] = 1.0 - (ss_res / ss_tot) if ss_tot > 0.0 else 0.0
    return mid, upper, lower, slope, r2


def ultimate_oscillator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    short: int = 7,
    mid: int = 14,
    long: int = 28,
) -> list[float | None]:
    """Williams Ultimate Oscillator (7/14/28 classic weights 4:2:1)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if short <= 0 or mid <= 0 or long <= 0 or n < long + 1:
        return out
    bp = [0.0] * n
    tr = [0.0] * n
    for i in range(n):
        prev_c = closes[i - 1] if i > 0 else closes[i]
        true_low = min(lows[i], prev_c)
        true_high = max(highs[i], prev_c)
        bp[i] = closes[i] - true_low
        tr[i] = true_high - true_low
    for i in range(long, n):
        avg_s_bp = sum(bp[i - short + 1 : i + 1])
        avg_s_tr = sum(tr[i - short + 1 : i + 1])
        avg_m_bp = sum(bp[i - mid + 1 : i + 1])
        avg_m_tr = sum(tr[i - mid + 1 : i + 1])
        avg_l_bp = sum(bp[i - long + 1 : i + 1])
        avg_l_tr = sum(tr[i - long + 1 : i + 1])
        if avg_s_tr == 0.0 or avg_m_tr == 0.0 or avg_l_tr == 0.0:
            continue
        raw = (
            4.0 * (avg_s_bp / avg_s_tr)
            + 2.0 * (avg_m_bp / avg_m_tr)
            + 1.0 * (avg_l_bp / avg_l_tr)
        )
        out[i] = 100.0 * raw / 7.0
    return out


def chandelier_exit_long(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    atr_length: int = 22,
    mult: float = 3.0,
) -> list[float | None]:
    """Chandelier Exit long trail: rolling HH(atr_length) − mult×ATR(atr_length).

    Helper only — not a primary strategy seat. ≠ SuperTrend.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if atr_length <= 0 or n < atr_length:
        return out
    atr_s = atr(highs, lows, closes, atr_length)
    for i in range(atr_length - 1, n):
        a = atr_s[i]
        if a is None:
            continue
        hh = max(highs[i - atr_length + 1 : i + 1])
        out[i] = hh - mult * a
    return out

def _sma_nullable(values: list[float | None], length: int) -> list[float | None]:
    """SMA over nullable series; window must be fully non-None."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    for i in range(length - 1, n):
        window = values[i - length + 1 : i + 1]
        if any(v is None for v in window):
            continue
        out[i] = sum(float(v) for v in window) / length  # type: ignore[arg-type]
    return out


def _mass_index_sum(
    ratio: list[float | None], sum_length: int
) -> list[float | None]:
    n = len(ratio)
    out: list[float | None] = [None] * n
    if sum_length <= 0 or n < sum_length:
        return out
    for i in range(sum_length - 1, n):
        window = ratio[i - sum_length + 1 : i + 1]
        if any(v is None for v in window):
            continue
        out[i] = sum(float(v) for v in window)  # type: ignore[arg-type]
    return out


def mass_index(
    highs: list[float],
    lows: list[float],
    ema_length: int = 9,
    sum_length: int = 25,
) -> list[float | None]:
    """Dorsey Mass Index: rolling sum of Single/Double EMA(HL) ratio.

    Single = EMA(high-low, ema_length); Double = EMA(Single, ema_length).
    MI = sum(Single/Double) over sum_length bars.
    """
    n = len(highs)
    if ema_length <= 0 or sum_length <= 0 or n < ema_length:
        return [None] * n
    hl = [highs[i] - lows[i] for i in range(n)]
    single = ema(hl, ema_length)
    double = _ema_skip_none(single, ema_length)
    ratio: list[float | None] = [None] * n
    for i in range(n):
        s, d = single[i], double[i]
        if s is None or d is None or d == 0.0:
            continue
        ratio[i] = s / d
    return _mass_index_sum(ratio, sum_length)


def kst(
    closes: list[float],
    roc_lengths: tuple[int, int, int, int] = (10, 15, 20, 30),
    sma_lengths: tuple[int, int, int, int] = (10, 10, 10, 15),
    signal_length: int = 9,
    weights: tuple[float, float, float, float] = (1.0, 2.0, 3.0, 4.0),
) -> tuple[list[float | None], list[float | None]]:
    """Pring Know Sure Thing (KST) line + signal SMA.

    KST = sum weight_i * SMA(ROC(roc_i), sma_i). Signal = SMA(KST, signal_length).
    """
    n = len(closes)
    kst_line: list[float | None] = [None] * n
    if len(roc_lengths) != 4 or len(sma_lengths) != 4 or len(weights) != 4:
        return kst_line, [None] * n
    rcmas: list[list[float | None]] = []
    for roc_l, sma_l in zip(roc_lengths, sma_lengths):
        r = roc(closes, roc_l)
        rcmas.append(_sma_nullable(r, sma_l))
    for i in range(n):
        vals = [rcmas[j][i] for j in range(4)]
        if any(v is None for v in vals):
            continue
        kst_line[i] = sum(weights[j] * float(vals[j]) for j in range(4))  # type: ignore[arg-type]
    signal = _sma_nullable(kst_line, signal_length)
    return kst_line, signal


def twiggs_money_flow(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    length: int = 21,
) -> list[float | None]:
    """Twiggs Money Flow (Incredible Charts): Wilder RMA(AD) / RMA(Volume).

    AD uses True High/Low vs prior close — not CMF (SMA of CLV*vol).
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    ad: list[float | None] = [None] * n
    vol_s: list[float | None] = [None] * n
    for i in range(n):
        prev_c = closes[i - 1] if i > 0 else closes[i]
        th = max(highs[i], prev_c)
        tl = min(lows[i], prev_c)
        span = th - tl
        if span == 0.0:
            ad[i] = 0.0
        else:
            ad[i] = volumes[i] * ((closes[i] - tl) - (th - closes[i])) / span
        vol_s[i] = volumes[i]
    ad_r = rma(ad, length)
    vol_r = rma(vol_s, length)
    for i in range(n):
        a, v = ad_r[i], vol_r[i]
        if a is None or v is None:
            continue
        out[i] = 0.0 if v == 0.0 else a / v
    return out


def demarker(
    highs: list[float],
    lows: list[float],
    length: int = 14,
) -> list[float | None]:
    """DeMarker oscillator DeM(length) in [0, 1]. No RSI graft."""
    n = len(highs)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return out
    demax = [0.0] * n
    demin = [0.0] * n
    for i in range(1, n):
        if highs[i] > highs[i - 1]:
            demax[i] = highs[i] - highs[i - 1]
        if lows[i] < lows[i - 1]:
            demin[i] = lows[i - 1] - lows[i]
    for i in range(length, n):
        smax = sum(demax[i - length + 1 : i + 1])
        smin = sum(demin[i - length + 1 : i + 1])
        denom = smax + smin
        out[i] = 0.0 if denom == 0.0 else smax / denom
    return out



def relative_vigor_index(
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 10,
    signal_length: int = 4,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Relative Vigor Index + Signal (symmetric 4-bar weights).

    Value1 = ((c-o)+2*(c1-o1)+2*(c2-o2)+(c3-o3))/6
    Value2 = ((h-l)+2*(h1-l1)+2*(h2-l2)+(h3-l3))/6
    RVI = Sum(Value1, length) / Sum(Value2, length)
    Signal = (RVI+2*RVI[1]+2*RVI[2]+RVI[3])/6  (when signal_length==4 classic)
    For signal_length != 4, fall back to SMA(RVI, signal_length).
    """
    n = len(closes)
    rvi: list[float | None] = [None] * n
    signal: list[float | None] = [None] * n
    if length <= 0 or n < length + 3:
        return rvi, signal

    v1 = [0.0] * n
    v2 = [0.0] * n
    for i in range(3, n):
        v1[i] = (
            (closes[i] - opens[i])
            + 2.0 * (closes[i - 1] - opens[i - 1])
            + 2.0 * (closes[i - 2] - opens[i - 2])
            + (closes[i - 3] - opens[i - 3])
        ) / 6.0
        v2[i] = (
            (highs[i] - lows[i])
            + 2.0 * (highs[i - 1] - lows[i - 1])
            + 2.0 * (highs[i - 2] - lows[i - 2])
            + (highs[i - 3] - lows[i - 3])
        ) / 6.0

    # First RVI index needs length bars of v1/v2 starting at index 3
    first = 3 + length - 1
    if first >= n:
        return rvi, signal
    sum1 = sum(v1[3 : 3 + length])
    sum2 = sum(v2[3 : 3 + length])
    rvi[first] = 0.0 if sum2 == 0.0 else sum1 / sum2
    for i in range(first + 1, n):
        sum1 += v1[i] - v1[i - length]
        sum2 += v2[i] - v2[i - length]
        rvi[i] = 0.0 if sum2 == 0.0 else sum1 / sum2

    if signal_length == 4:
        for i in range(first + 3, n):
            a, b, c, d = rvi[i], rvi[i - 1], rvi[i - 2], rvi[i - 3]
            if a is None or b is None or c is None or d is None:
                continue
            signal[i] = (a + 2.0 * b + 2.0 * c + d) / 6.0
    else:
        signal = _sma_nullable(rvi, signal_length)
    return rvi, signal


def choppiness_index(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> list[float | None]:
    """Choppiness Index CHOP(length) in ~[0, 100].

    CHOP = 100 * log10(sum(TR, n) / (HH - LL)) / log10(n)
    Low CHOP = trending; high CHOP = choppy.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 1 or n < length:
        return out
    tr = true_range(highs, lows, closes)
    # true_range[0] is high-low; rest use prior close — fine for CHOP
    log_n = math.log10(float(length))
    if log_n == 0.0:
        return out
    for i in range(length - 1, n):
        window_tr = tr[i - length + 1 : i + 1]
        if any(x is None for x in window_tr):
            continue
        sum_tr = sum(float(x) for x in window_tr)  # type: ignore[arg-type]
        hh = max(highs[i - length + 1 : i + 1])
        ll = min(lows[i - length + 1 : i + 1])
        span = hh - ll
        if span <= 0.0 or sum_tr <= 0.0:
            out[i] = 100.0
        else:
            out[i] = 100.0 * math.log10(sum_tr / span) / log_n
    return out


def cyber_cycle(
    highs: list[float],
    lows: list[float],
    alpha: float = 0.07,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Cyber Cycle (Rocket Science for Traders) × Trigger=Cycle[1].

    Price = (H+L)/2; Smooth = (P + 2P[1] + 2P[2] + P[3]) / 6;
    Cycle = (1−0.5α)² (Smooth − 2 Smooth[1] + Smooth[2])
          + 2(1−α) Cycle[1] − (1−α)² Cycle[2].
    Trigger = Cycle[1]. No Fisher graft.
    """
    n = len(highs)
    cycle: list[float | None] = [None] * n
    trigger: list[float | None] = [None] * n
    if n == 0 or alpha <= 0.0 or alpha >= 1.0:
        return cycle, trigger

    price = [(highs[i] + lows[i]) / 2.0 for i in range(n)]
    smooth: list[float | None] = [None] * n
    for i in range(n):
        if i < 3:
            smooth[i] = price[i]
        else:
            smooth[i] = (
                price[i] + 2.0 * price[i - 1] + 2.0 * price[i - 2] + price[i - 3]
            ) / 6.0

    a = alpha
    c1 = (1.0 - 0.5 * a) ** 2
    c2 = 2.0 * (1.0 - a)
    c3 = (1.0 - a) ** 2

    # Seed first two cycles as zero (Ehlers); then recurse.
    for i in range(n):
        if i < 2:
            cycle[i] = 0.0
            continue
        s0, s1, s2 = smooth[i], smooth[i - 1], smooth[i - 2]
        cy1, cy2 = cycle[i - 1], cycle[i - 2]
        if s0 is None or s1 is None or s2 is None or cy1 is None or cy2 is None:
            cycle[i] = 0.0
            continue
        cycle[i] = c1 * (s0 - 2.0 * s1 + s2) + c2 * cy1 - c3 * cy2
        trigger[i] = cy1
    return cycle, trigger


def mesa_sine_wave(
    closes: list[float],
    dominant_cycle: int = 15,
    advance_deg: float = 45.0,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers / Tulip fixed-period MESA Sine Wave (Sine × LeadSine).

    DFT window of length `dominant_cycle` on close; phase → sin(phase),
    LeadSine = sin(phase + advance_deg). Default Advance=45° (π/4).
    No Fisher / RSI graft. Returns (sine, lead_sine); warm-up = dominant_cycle bars.
    """
    n = len(closes)
    sine: list[float | None] = [None] * n
    lead: list[float | None] = [None] * n
    period = int(dominant_cycle)
    if period < 1 or n <= period:
        return sine, lead

    pi = math.pi
    tpi = 2.0 * pi
    adv = math.radians(float(advance_deg))

    for i in range(period, n):
        rp = 0.0
        ip = 0.0
        for j in range(period):
            weight = closes[i - j]
            ang = tpi * j / period
            rp += math.cos(ang) * weight
            ip += math.sin(ang) * weight
        if abs(rp) > 0.001:
            phase = math.atan(ip / rp)
        else:
            phase = (tpi / 2.0) * (-1.0 if ip < 0 else 1.0)
        if rp < 0.0:
            phase += pi
        phase += pi / 2.0
        if phase < 0.0:
            phase += tpi
        if phase > tpi:
            phase -= tpi
        sine[i] = math.sin(phase)
        lead[i] = math.sin(phase + adv)
    return sine, lead


def ema_of_optional(values: list[float | None], length: int) -> list[float | None]:
    """EMA over non-None densified values; map results back to original indices."""
    n = len(values)
    out: list[float | None] = [None] * n
    dense: list[float] = []
    idx: list[int] = []
    for i, v in enumerate(values):
        if v is None:
            continue
        dense.append(v)
        idx.append(i)
    if length <= 0 or len(dense) < length:
        return out
    smoothed = ema(dense, length)
    for j, i in enumerate(idx):
        out[i] = smoothed[j]
    return out


def smi_blau(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 13,
    smooth1: int = 3,
    smooth2: int = 3,
    signal_len: int = 3,
) -> tuple[list[float | None], list[float | None]]:
    """Blau Stochastic Momentum Index (−100..+100) + EMA signal.

    Midpoint relative range, double-smoothed — not classic Stochastic %K/%D.
    """
    n = len(closes)
    smi: list[float | None] = [None] * n
    sig: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return smi, sig

    mid_diff: list[float | None] = [None] * n
    half_range: list[float | None] = [None] * n
    for i in range(length - 1, n):
        window_h = highs[i - length + 1 : i + 1]
        window_l = lows[i - length + 1 : i + 1]
        hh = max(window_h)
        ll = min(window_l)
        mid_diff[i] = closes[i] - 0.5 * (hh + ll)
        half_range[i] = 0.5 * (hh - ll)

    m1 = ema_of_optional(mid_diff, smooth1)
    h1 = ema_of_optional(half_range, smooth1)
    m2 = ema_of_optional(m1, smooth2)
    h2 = ema_of_optional(h1, smooth2)

    for i in range(n):
        if m2[i] is None or h2[i] is None:
            continue
        denom = h2[i]
        if denom is None or denom == 0.0:
            smi[i] = 0.0
        else:
            smi[i] = 100.0 * (m2[i] / denom)

    sig = ema_of_optional(smi, signal_len)
    return smi, sig


def accumulation_distribution_line(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
) -> list[float]:
    """Cumulative ADL (Chaikin): CLV × volume running sum."""
    n = len(closes)
    out: list[float] = [0.0] * n
    cum = 0.0
    for i in range(n):
        hl = highs[i] - lows[i]
        if hl == 0.0:
            clv = 0.0
        else:
            clv = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / hl
        cum += clv * volumes[i]
        out[i] = cum
    return out


def chaikin_oscillator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    fast: int = 3,
    slow: int = 10,
) -> list[float | None]:
    """Chaikin Oscillator = EMA(fast, ADL) − EMA(slow, ADL). Not CMF/OBV/MFI."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if fast <= 0 or slow <= 0 or n < slow:
        return out
    adl = accumulation_distribution_line(highs, lows, closes, volumes)
    e_fast = ema(adl, fast)
    e_slow = ema(adl, slow)
    for i in range(n):
        if e_fast[i] is None or e_slow[i] is None:
            continue
        out[i] = e_fast[i] - e_slow[i]  # type: ignore[operator]
    return out


def laguerre_filter(values: list[float], gamma: float = 0.8) -> list[float | None]:
    """Ehlers Laguerre filter on price (not Laguerre RSI).

    L0..L3 recursive FIR; output = (L0 + 2*L1 + 2*L2 + L3) / 6.
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if n == 0:
        return out
    g = gamma
    l0 = l1 = l2 = l3 = 0.0
    for i, price in enumerate(values):
        if i == 0:
            l0 = l1 = l2 = l3 = price
        else:
            prev0, prev1, prev2, prev3 = l0, l1, l2, l3
            l0 = (1.0 - g) * price + g * prev0
            l1 = -g * l0 + prev0 + g * prev1
            l2 = -g * l1 + prev1 + g * prev2
            l3 = -g * l2 + prev2 + g * prev3
        out[i] = (l0 + 2.0 * l1 + 2.0 * l2 + l3) / 6.0
    return out


def session_vwap_bands(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    day_ids: list[int],
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """UTC-session VWAP ±1σ (volume-weighted). Resets when day_ids change.

    src = typical price (H+L+C)/3. σ from VW variance of src (TV-style).
    Returns (vwap, lower_2sigma, upper_2sigma). ≠ Bollinger (SMA±σ of close).
    """
    n = len(closes)
    vwap: list[float | None] = [None] * n
    lo2: list[float | None] = [None] * n
    hi2: list[float | None] = [None] * n
    if n == 0:
        return vwap, lo2, hi2

    sum_pv = 0.0
    sum_v = 0.0
    sum_p2v = 0.0
    cur_day = day_ids[0] - 1

    for i in range(n):
        if day_ids[i] != cur_day:
            cur_day = day_ids[i]
            sum_pv = 0.0
            sum_v = 0.0
            sum_p2v = 0.0
        tp = (highs[i] + lows[i] + closes[i]) / 3.0
        vol = volumes[i]
        sum_pv += tp * vol
        sum_p2v += tp * tp * vol
        sum_v += vol
        if sum_v <= 0.0:
            continue
        vw = sum_pv / sum_v
        var = max(sum_p2v / sum_v - vw * vw, 0.0)
        sd = math.sqrt(var)
        vwap[i] = vw
        lo2[i] = vw - 2.0 * sd
        hi2[i] = vw + 2.0 * sd
    return vwap, lo2, hi2


def pvt(closes: list[float], volumes: list[float]) -> list[float]:
    """Price-Volume Trend (ta.pvt in TradingView).

    Formula: PVT = PVT[1] + volume * (close - close[1]) / close[1].
    """
    n = len(closes)
    out: list[float] = [0.0] * n
    if n <= 1:
        return out
    cum = 0.0
    out[0] = 0.0
    for i in range(1, n):
        prev = closes[i - 1]
        if prev != 0.0:
            cum += volumes[i] * (closes[i] - prev) / prev
        out[i] = cum
    return out


def accdist(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
) -> list[float]:
    """Accumulation/Distribution Line (ta.accdist in TradingView).

    MFM = ((close - low) - (high - close)) / (high - low) if high != low else 0.0
    MFV = MFM * volume
    ADL = cumsum(MFV)
    """
    n = len(closes)
    out: list[float] = [0.0] * n
    if n == 0:
        return out
    cum = 0.0
    for i in range(n):
        h, lo, c, v = highs[i], lows[i], closes[i], volumes[i]
        rng = h - lo
        mfm = ((c - lo) - (h - c)) / rng if rng != 0.0 else 0.0
        cum += mfm * v
        out[i] = cum
    return out


def swing_index(
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
    limit_move: float | list[float | None],
) -> list[float]:
    """Wilder's Swing Index (SI) per bar.

    SI = 50 * ( (C - Cy) + 0.5 * (C - O) + 0.25 * (Cy - Oy) ) / R * (K / T)
    where:
      Cy = prior close, Oy = prior open, Hy = prior high, Ly = prior low
      C = close, O = open, H = high, L = low
      K = max( |H - Cy|, |L - Cy| )
      T = limit-move (proxy in crypto, e.g. atr_mult*ATR or % of prior close)
      R is determined by max of:
        |H - Cy| -> R = |H - Cy| - 0.5 * |L - Cy| + 0.25 * |Cy - Oy|
        |L - Cy| -> R = |L - Cy| - 0.5 * |H - Cy| + 0.25 * |Cy - Oy|
        |H - L|  -> R = |H - L| + 0.25 * |Cy - Oy|
      If R == 0 or T <= 0, SI = 0.
    Index 0 has SI = 0.
    """
    n = len(closes)
    out: list[float] = [0.0] * n
    if n <= 1:
        return out

    is_list_t = isinstance(limit_move, (list, tuple))

    for i in range(1, n):
        t_val = limit_move[i] if is_list_t else limit_move
        if t_val is None or t_val <= 0.0:
            out[i] = 0.0
            continue

        c, o, h, lo = closes[i], opens[i], highs[i], lows[i]
        cy, oy = closes[i - 1], opens[i - 1]

        h_cy = abs(h - cy)
        l_cy = abs(lo - cy)
        h_l = h - lo

        if h_cy >= l_cy and h_cy >= h_l:
            r = h_cy - 0.5 * l_cy + 0.25 * abs(cy - oy)
        elif l_cy >= h_cy and l_cy >= h_l:
            r = l_cy - 0.5 * h_cy + 0.25 * abs(cy - oy)
        else:
            r = h_l + 0.25 * abs(cy - oy)

        if r == 0.0:
            out[i] = 0.0
            continue

        k = max(h_cy, l_cy)
        num = (c - cy) + 0.5 * (c - o) + 0.25 * (cy - oy)
        si = 50.0 * (num / r) * (k / t_val)
        out[i] = si

    return out


def accumulative_swing_index(
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
    limit_move: float | list[float | None],
) -> list[float]:
    """Accumulative Swing Index (ASI) = cumsum(SI)."""
    si = swing_index(opens, highs, lows, closes, limit_move)
    out: list[float] = [0.0] * len(si)
    cum = 0.0
    for i, s in enumerate(si):
        cum += s
        out[i] = cum
    return out


def alma(
    values: list[float],
    length: int = 9,
    offset: float = 0.85,
    sigma: float = 6.0,
) -> list[float | None]:
    """Arnaud Legoux Moving Average (ALMA).

    FIR filter with Gaussian distribution weights centered at offset * (length - 1).
    TradingView / LuxAlgo formula:
      m = floor(offset * (length - 1))  # or float in TV: offset * (length - 1)
      s = length / sigma
      weight_i = exp(- (i - m)^2 / (2 * s^2)) for i in 0 .. length - 1
      ALMA[t] = sum(weight_i * values[t - length + 1 + i]) / sum(weight_i)
    Returns None for indices < length - 1.
    """
    import math

    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length or sigma <= 0.0:
        return out

    m = offset * (length - 1)
    s = length / sigma
    two_s_sq = 2.0 * s * s

    weights = [math.exp(-((i - m) ** 2) / two_s_sq) for i in range(length)]
    sum_w = sum(weights)
    if sum_w == 0.0:
        return out

    # Pre-normalize weights
    norm_weights = [w / sum_w for w in weights]

    for t in range(length - 1, n):
        # values window from t - length + 1 up to t
        window = values[t - length + 1 : t + 1]
        val = sum(norm_weights[i] * window[i] for i in range(length))
        out[t] = val

    return out


def cmo(values: list[float], length: int = 20) -> list[float | None]:
    """Chande Momentum Oscillator (CMO).

    CMO = 100 * (Su - Sd) / (Su + Sd)
    where:
      Su = sum of positive close differences over length
      Sd = sum of absolute negative close differences over length
    Values range between -100 and +100.
    Returns None for indices < length.
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n <= length:
        return out

    # Compute 1-bar deltas
    diffs = [0.0] * n
    for i in range(1, n):
        diffs[i] = values[i] - values[i - 1]

    u = [diff if diff > 0.0 else 0.0 for diff in diffs]
    d = [-diff if diff < 0.0 else 0.0 for diff in diffs]

    su = sum(u[1 : length + 1])
    sd = sum(d[1 : length + 1])
    denom = su + sd
    out[length] = (100.0 * (su - sd) / denom) if denom != 0.0 else 0.0

    for i in range(length + 1, n):
        su += u[i] - u[i - length]
        sd += d[i] - d[i - length]
        denom = su + sd
        out[i] = (100.0 * (su - sd) / denom) if denom != 0.0 else 0.0

    return out


def ehlers_cg(
    prices: list[float],
    length: int = 10,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Center of Gravity (CG) Oscillator and Trigger.

    Price = hl2 (or input prices, e.g. (high+low)/2)
    CG = - sum_{i=0}^{length-1} (1 + i) * Price[t - i] / sum_{i=0}^{length-1} Price[t - i]
    Trigger = CG[1] (1-bar delayed CG)
    Returns (cg, trigger).
    """
    n = len(prices)
    cg: list[float | None] = [None] * n
    trigger: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return cg, trigger

    for t in range(length - 1, n):
        num = 0.0
        denom = 0.0
        for i in range(length):
            p = prices[t - i]
            num += (1.0 + i) * p
            denom += p
        if denom != 0.0:
            cg[t] = -num / denom
        else:
            cg[t] = 0.0

    for t in range(1, n):
        trigger[t] = cg[t - 1]

    return cg, trigger


def ehlers_roofing_filter(
    prices: list[float],
    hp_period: int = 48,
    ss_period: int = 10,
) -> list[float | None]:
    """Ehlers Roofing Filter.

    Two-pole HighPass filter (hp_period) cascades into a two-pole SuperSmoother filter (ss_period).
    Documented IIR coefficients (per John Ehlers, Cycle Analytics for Traders / MESA):

    HighPass (2-pole):
      theta = 0.707 * 2 * pi / hp_period
      alpha1 = (cos(theta) + sin(theta) - 1.0) / cos(theta)
      c1 = (1.0 - alpha1 / 2.0)^2
      c2 = 2.0 * (1.0 - alpha1)
      c3 = - (1.0 - alpha1)^2
      HP[t] = c1 * (Price[t] - 2*Price[t-1] + Price[t-2]) + c2 * HP[t-1] + c3 * HP[t-2]

    SuperSmoother (2-pole):
      a1 = exp(-sqrt(2) * pi / ss_period)
      b1 = 2 * a1 * cos(sqrt(2) * pi / ss_period)
      c2_ss = b1
      c3_ss = - a1^2
      c1_ss = 1.0 - c2_ss - c3_ss
      Roof[t] = c1_ss * ((HP[t] + HP[t-1]) / 2.0) + c2_ss * Roof[t-1] + c3_ss * Roof[t-2]

    Returns Roofing series (float). Warmup returns None until HP and SS stabilize (max(hp, ss)).
    """
    import math

    n = len(prices)
    roof: list[float | None] = [None] * n
    if n < 4 or hp_period <= 2 or ss_period <= 2:
        return roof

    # HighPass coefficients
    hp_rad = 0.707 * 2.0 * math.pi / hp_period
    cos_hp = math.cos(hp_rad)
    sin_hp = math.sin(hp_rad)
    if cos_hp == 0.0:
        return roof
    alpha1 = (cos_hp + sin_hp - 1.0) / cos_hp
    c1 = (1.0 - alpha1 / 2.0) ** 2
    c2 = 2.0 * (1.0 - alpha1)
    c3 = -((1.0 - alpha1) ** 2)

    # SuperSmoother coefficients
    ss_rad = math.sqrt(2.0) * math.pi / ss_period
    a1 = math.exp(-ss_rad)
    b1 = 2.0 * a1 * math.cos(ss_rad)
    c2_ss = b1
    c3_ss = -(a1**2)
    c1_ss = 1.0 - c2_ss - c3_ss

    hp = [0.0] * n
    for t in range(n):
        if t == 0:
            hp[t] = 0.0
        elif t == 1:
            hp[t] = 0.0
        else:
            diff = prices[t] - 2.0 * prices[t - 1] + prices[t - 2]
            hp[t] = c1 * diff + c2 * hp[t - 1] + c3 * hp[t - 2]

    ss = [0.0] * n
    warmup = max(hp_period, ss_period) * 2
    for t in range(n):
        if t == 0:
            ss[t] = 0.0
        elif t == 1:
            ss[t] = (hp[1] + hp[0]) / 2.0
        else:
            inp = (hp[t] + hp[t - 1]) / 2.0
            ss[t] = c1_ss * inp + c2_ss * ss[t - 1] + c3_ss * ss[t - 2]
            if t >= warmup:
                roof[t] = ss[t]

    return roof


def vwma(
    closes: list[float],
    volumes: list[float],
    length: int,
) -> list[float | None]:
    """Volume Weighted Moving Average (TradingView ta.vwma).

    VWMA = sum(close * volume, length) / sum(volume, length)
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    vp_window = sum(closes[i] * volumes[i] for i in range(length))
    v_window = sum(volumes[:length])
    out[length - 1] = vp_window / v_window if v_window > 0 else closes[length - 1]

    for i in range(length, n):
        vp_window += closes[i] * volumes[i] - closes[i - length] * volumes[i - length]
        v_window += volumes[i] - volumes[i - length]
        out[i] = vp_window / v_window if v_window > 0 else closes[i]
    return out


def t3(
    values: list[float],
    length: int,
    v_factor: float = 0.7,
) -> list[float | None]:
    """Tillson T3 Moving Average (Tim Tillson, TASC Jan 1998 / TradingView ta.t3).

    T3 is a nested Generalized DEMA (GD3):
      GD(x) = (1 + v)*EMA(x) - v*EMA(EMA(x))
      T3 = GD(GD(GD(x)))
    Or polynomial 6-EMA cascade:
      c1 = -v^3
      c2 = 3*v^2 + 3*v^3
      c3 = -6*v^2 - 3*v - 3*v^3
      c4 = 1 + 3*v + v^3 + 3*v^2
      T3 = c1*e6 + c2*e5 + c3*e4 + c4*e3
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    e1 = ema(values, length)
    e2 = _ema_skip_none(e1, length)
    e3 = _ema_skip_none(e2, length)
    e4 = _ema_skip_none(e3, length)
    e5 = _ema_skip_none(e4, length)
    e6 = _ema_skip_none(e5, length)

    v = v_factor
    c1 = -(v**3)
    c2 = 3.0 * (v**2) + 3.0 * (v**3)
    c3 = -6.0 * (v**2) - 3.0 * v - 3.0 * (v**3)
    c4 = 1.0 + 3.0 * v + (v**3) + 3.0 * (v**2)

    for i in range(n):
        if e3[i] is not None and e4[i] is not None and e5[i] is not None and e6[i] is not None:
            out[i] = c1 * e6[i] + c2 * e5[i] + c3 * e4[i] + c4 * e3[i]
    return out


def ehlers_decycler_oscillator(
    prices: list[float],
    hp_period: int = 125,
    k: float = 1.0,
) -> list[float | None]:
    """Ehlers Decycler Oscillator (John F. Ehlers, TASC Sep 2015).

    2-pole HighPass filter removes very low frequency trend components:
      alpha1 = (cos(rad1) + sin(rad1) - 1) / cos(rad1), rad1 = 0.707 * 2*pi / hp_period
      HP = (1 - alpha1/2)^2 * (Price - 2*Price[1] + Price[2]) + 2*(1 - alpha1)*HP[1] - (1 - alpha1)^2 * HP[2]
      Decycle = Price - HP
    Second HighPass filter applied to Decycle at half period (0.5 * hp_period):
      alpha2 = (cos(rad2) + sin(rad2) - 1) / cos(rad2), rad2 = 0.707 * 2*pi / (0.5 * hp_period)
      DecycleOsc = (1 - alpha2/2)^2 * (Decycle - 2*Decycle[1] + Decycle[2]) + 2*(1 - alpha2)*DecycleOsc[1] - (1 - alpha2)^2 * DecycleOsc[2]
      Osc = 100 * K * DecycleOsc / Price
    """
    n = len(prices)
    out: list[float | None] = [None] * n
    if n < 3 or hp_period <= 2:
        return out

    rad1 = 0.707 * 2.0 * math.pi / hp_period
    cos1 = math.cos(rad1)
    if cos1 == 0.0:
        return out
    alpha1 = (cos1 + math.sin(rad1) - 1.0) / cos1
    c1 = (1.0 - alpha1 / 2.0) ** 2
    c2 = 2.0 * (1.0 - alpha1)
    c3 = -((1.0 - alpha1) ** 2)

    rad2 = 0.707 * 2.0 * math.pi / (0.5 * hp_period)
    cos2 = math.cos(rad2)
    if cos2 == 0.0:
        return out
    alpha2 = (cos2 + math.sin(rad2) - 1.0) / cos2
    d1 = (1.0 - alpha2 / 2.0) ** 2
    d2 = 2.0 * (1.0 - alpha2)
    d3 = -((1.0 - alpha2) ** 2)

    hp = [0.0] * n
    decycle = [0.0] * n
    decycle_osc = [0.0] * n

    for t in range(n):
        if t == 0:
            hp[t] = 0.0
            decycle[t] = prices[0]
            decycle_osc[t] = 0.0
        elif t == 1:
            hp[t] = c1 * (prices[1] - 2.0 * prices[0] + prices[0]) + c2 * hp[0]
            decycle[t] = prices[1] - hp[t]
            decycle_osc[t] = 0.0
        else:
            hp[t] = (
                c1 * (prices[t] - 2.0 * prices[t - 1] + prices[t - 2])
                + c2 * hp[t - 1]
                + c3 * hp[t - 2]
            )
            decycle[t] = prices[t] - hp[t]
            decycle_osc[t] = (
                d1 * (decycle[t] - 2.0 * decycle[t - 1] + decycle[t - 2])
                + d2 * decycle_osc[t - 1]
                + d3 * decycle_osc[t - 2]
            )

        if prices[t] != 0.0:
            out[t] = 100.0 * k * decycle_osc[t] / prices[t]
        else:
            out[t] = 0.0

    return out


def ehlers_itrend_trigger(
    highs: list[float],
    lows: list[float],
    alpha: float = 0.07,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Instantaneous Trendline and Trigger (simplified Pine form, alpha=0.07).

    Price = (High + Low) / 2
    Seed for bars < 7: ITrend = (Price + 2*Price[1] + Price[2]) / 4
    Recursion for bars >= 7:
      ITrend = (alpha - alpha^2/4)*Price + 0.5*alpha^2*Price[1] - (alpha - 0.75*alpha^2)*Price[2]
               + 2*(1 - alpha)*ITrend[1] - (1 - alpha)^2*ITrend[2]
    Trigger = 2 * ITrend - ITrend[2]
    """
    n = len(highs)
    itrend_out: list[float | None] = [None] * n
    trigger_out: list[float | None] = [None] * n
    if n == 0 or alpha <= 0.0:
        return itrend_out, trigger_out

    prices = [(h + l) / 2.0 for h, l in zip(highs, lows)]
    itrend = [0.0] * n

    a = alpha
    a2 = a * a
    c0 = a - a2 / 4.0
    c1 = 0.5 * a2
    c2 = -(a - 0.75 * a2)
    c3 = 2.0 * (1.0 - a)
    c4 = -((1.0 - a) ** 2)

    for t in range(n):
        if t == 0:
            itrend[t] = prices[0]
        elif t == 1:
            itrend[t] = (prices[1] + 2.0 * prices[0] + prices[0]) / 4.0
        elif t < 7:
            itrend[t] = (prices[t] + 2.0 * prices[t - 1] + prices[t - 2]) / 4.0
        else:
            itrend[t] = (
                c0 * prices[t]
                + c1 * prices[t - 1]
                + c2 * prices[t - 2]
                + c3 * itrend[t - 1]
                + c4 * itrend[t - 2]
            )
        itrend_out[t] = itrend[t]
        if t >= 2:
            trigger_out[t] = 2.0 * itrend[t] - itrend[t - 2]

    return itrend_out, trigger_out


def rvol(volumes: list[float], length: int = 20) -> list[float | None]:
    """Relative Volume (RVOL) = Volume / SMA(Volume, length)."""
    n = len(volumes)
    out: list[float | None] = [None] * n
    vol_sma = sma(volumes, length)
    for i in range(n):
        s = vol_sma[i]
        if s is not None and s > 0:
            out[i] = volumes[i] / s
        else:
            out[i] = None
    return out


def pivothigh(highs: list[float], left: int, right: int) -> list[float | None]:
    """Confirmed Pivot High (Pine Script ta.pivothigh(high, left, right)).

    A bar at index `i - right` is a pivot high if its high is strictly greater than
    all highs in [i - right - left, i - right) and greater than or equal to
    all highs in (i - right, i].
    The confirmed value is returned at bar `i` (confirmation bar, closed-bar safe).
    """
    n = len(highs)
    out: list[float | None] = [None] * n
    if left < 1 or right < 1 or n < left + right + 1:
        return out

    for i in range(left + right, n):
        pivot_idx = i - right
        p_val = highs[pivot_idx]
        is_pivot = True
        # Check left
        for j in range(pivot_idx - left, pivot_idx):
            if highs[j] >= p_val:
                is_pivot = False
                break
        # Check right
        if is_pivot:
            for j in range(pivot_idx + 1, i + 1):
                if highs[j] > p_val:
                    is_pivot = False
                    break
        if is_pivot:
            out[i] = p_val
    return out


def pivotlow(lows: list[float], left: int, right: int) -> list[float | None]:
    """Confirmed Pivot Low (Pine Script ta.pivotlow(low, left, right)).

    A bar at index `i - right` is a pivot low if its low is strictly less than
    all lows in [i - right - left, i - right) and less than or equal to
    all lows in (i - right, i].
    The confirmed value is returned at bar `i` (confirmation bar, closed-bar safe).
    """
    n = len(lows)
    out: list[float | None] = [None] * n
    if left < 1 or right < 1 or n < left + right + 1:
        return out

    for i in range(left + right, n):
        pivot_idx = i - right
        p_val = lows[pivot_idx]
        is_pivot = True
        # Check left
        for j in range(pivot_idx - left, pivot_idx):
            if lows[j] <= p_val:
                is_pivot = False
                break
        # Check right
        if is_pivot:
            for j in range(pivot_idx + 1, i + 1):
                if lows[j] < p_val:
                    is_pivot = False
                    break
        if is_pivot:
            out[i] = p_val
    return out


def eom(
    highs: list[float],
    lows: list[float],
    volumes: list[float],
    length: int = 14,
    divisor: float = 10_000_000.0,
) -> list[float | None]:
    """Ease of Movement / Arms EMV (Pine Script ta.eom(length, divisor)).

    DistanceMoved = ((high + low) / 2) - ((high[1] + low[1]) / 2)
    BoxRatio = (volume / divisor) / (high - low)
    EMV_raw = DistanceMoved / BoxRatio
    EMV = SMA(EMV_raw, length)
    """
    n = len(highs)
    out: list[float | None] = [None] * n
    if n < 2 or length <= 0 or divisor <= 0:
        return out

    raw_emv: list[float] = [0.0] * n
    for i in range(1, n):
        dm = ((highs[i] + lows[i]) / 2.0) - ((highs[i - 1] + lows[i - 1]) / 2.0)
        rng = highs[i] - lows[i]
        vol = volumes[i]
        if rng > 0 and vol > 0:
            br = (vol / divisor) / rng
            raw_emv[i] = dm / br if br != 0 else 0.0
        else:
            raw_emv[i] = 0.0

    return sma(raw_emv, length)


def pvo(
    volumes: list[float],
    fast_len: int = 12,
    slow_len: int = 26,
    signal_len: int = 9,
) -> tuple[list[float | None], list[float | None]]:
    """Percentage Volume Oscillator (Pine Script PVO).

    fastV = EMA(volume, fast_len)
    slowV = EMA(volume, slow_len)
    PVO = 100 * (fastV - slowV) / slowV
    Signal = EMA(PVO, signal_len)
    """
    n = len(volumes)
    pvo_out: list[float | None] = [None] * n
    sig_out: list[float | None] = [None] * n
    if n < slow_len or fast_len <= 0 or slow_len <= 0:
        return pvo_out, sig_out

    fast_v = ema(volumes, fast_len)
    slow_v = ema(volumes, slow_len)

    for i in range(n):
        fv = fast_v[i]
        sv = slow_v[i]
        if fv is not None and sv is not None and sv > 0:
            pvo_out[i] = 100.0 * (fv - sv) / sv
        else:
            pvo_out[i] = None

    # Compute signal line as EMA over valid PVO values
    valid_pvo = [v if v is not None else 0.0 for v in pvo_out]
    sig_raw = ema(valid_pvo, signal_len)
    for i in range(n):
        if pvo_out[i] is not None:
            sig_out[i] = sig_raw[i]
        else:
            sig_out[i] = None

    return pvo_out, sig_out


def zlema(
    values: list[float],
    length: int,
) -> list[float | None]:
    """Zero-Lag Exponential Moving Average (lag-compensated form).

    lag = round((length - 1) / 2)
    src_comp = values[i] + (values[i] - values[i - lag])
    zlema = EMA(src_comp, length)

    Canonical lag-compensation formula (NOT the 2010 Ehlers-Way EC gain form).
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    lag = int(round((length - 1) / 2.0))
    src_comp: list[float] = [0.0] * n
    for i in range(n):
        if i >= lag:
            src_comp[i] = values[i] + (values[i] - values[i - lag])
        else:
            src_comp[i] = values[i]

    return ema(src_comp, length)


def cti(closes: list[float], length: int = 20) -> list[float | None]:
    """Ehlers Correlation Trend Indicator (CTI, TASC May 2020).

    Computes the Pearson correlation coefficient r between closes and an ideal rising
    straight line (Y_i = i) over a rolling window of length L.
    Values range from -1.0 (perfect downtrend) to +1.0 (perfect uptrend).

    Formula:
      X_i = closes[t - L + 1 + i], Y_i = i for i in 0..L-1
      r = (L*Sxy - Sx*Sy) / sqrt((L*Sxx - Sx^2) * (L*Syy - Sy^2))
    Returns None for indices < length - 1.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 1 or n < length:
        return out

    L = length
    Sy = L * (L - 1) / 2.0
    Syy = (L - 1) * L * (2 * L - 1) / 6.0
    denom_y = L * Syy - Sy * Sy
    if denom_y <= 0.0:
        return out

    for t in range(length - 1, n):
        window = closes[t - length + 1 : t + 1]
        Sx = sum(window)
        Sxx = sum(x * x for x in window)
        Sxy = sum(i * window[i] for i in range(L))
        denom_x = L * Sxx - Sx * Sx
        if denom_x > 1e-12:
            prod = denom_x * denom_y
            r = (L * Sxy - Sx * Sy) / math.sqrt(prod)
            out[t] = max(-1.0, min(1.0, r))
        else:
            out[t] = 0.0

    return out


def atr_percent(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> list[float | None]:
    """ATR as a percentage of close price: 100 * ATR(length) / close."""
    atr_vals = atr(highs, lows, closes, length)
    n = len(closes)
    out: list[float | None] = [None] * n
    for i in range(n):
        a = atr_vals[i]
        c = closes[i]
        if a is not None and c is not None and c > 0:
            out[i] = 100.0 * a / c
        else:
            out[i] = None
    return out


def median_filter(values: list[float], length: int = 20) -> list[float | None]:
    """Rolling median over window of size length."""
    import statistics

    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    for t in range(length - 1, n):
        window = values[t - length + 1 : t + 1]
        out[t] = statistics.median(window)
    return out


def mad(values: list[float], length: int = 20) -> list[float | None]:
    """Median Absolute Deviation (MAD) over rolling window of size length.

    For window W:
      med = median(W)
      mad = median(|x - med| for x in W)
    """
    import statistics

    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    for t in range(length - 1, n):
        window = values[t - length + 1 : t + 1]
        m = statistics.median(window)
        devs = [abs(x - m) for x in window]
        out[t] = statistics.median(devs)
    return out


def mad_channel(
    values: list[float],
    length: int = 20,
    k: float = 2.0,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """Rolling Median +/- k * (1.4826 * MAD) channel.

    1.4826 * MAD yields the normal distribution consistency estimator for sigma.
    Returns (median_series, upper_band, lower_band).
    """
    import statistics

    n = len(values)
    med_out: list[float | None] = [None] * n
    upper_out: list[float | None] = [None] * n
    lower_out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return med_out, upper_out, lower_out

    for t in range(length - 1, n):
        window = values[t - length + 1 : t + 1]
        m = statistics.median(window)
        devs = [abs(x - m) for x in window]
        mad_val = statistics.median(devs)
        mad_sigma = 1.4826 * mad_val
        med_out[t] = m
        upper_out[t] = m + k * mad_sigma
        lower_out[t] = m - k * mad_sigma

    return med_out, upper_out, lower_out


def vidya(
    closes: list[float],
    ema_len: int = 9,
    cmo_len: int = 12,
) -> list[float | None]:
    """Chande Variable Index Dynamic Average (VIDYA).

    Uses Chande Momentum Oscillator (CMO) to scale EMA smoothing constant:
      cmo = CMO(close, cmo_len)  in [-100, +100]
      F = 2.0 / (ema_len + 1)
      alpha = F * abs(cmo) / 100.0
      vidya[t] = alpha * close[t] + (1 - alpha) * vidya[t-1]

    Scale convention: CMO is in [-100, 100], |CMO|/100 in [0, 1].
    When momentum collapses (|CMO|->0), alpha->0 and VIDYA flattens.
    When momentum is extreme (|CMO|->100), alpha->F (standard EMA speed).
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if ema_len <= 0 or cmo_len <= 0 or n <= cmo_len:
        return out

    cmo_vals = cmo(closes, cmo_len)
    f_const = 2.0 / (ema_len + 1.0)

    # Initialize VIDYA at first valid CMO bar
    first_valid = -1
    for i in range(n):
        if cmo_vals[i] is not None:
            first_valid = i
            break

    if first_valid == -1 or first_valid >= n:
        return out

    out[first_valid] = closes[first_valid]
    for i in range(first_valid + 1, n):
        cm = cmo_vals[i]
        prev = out[i - 1]
        if cm is not None and prev is not None:
            alpha = f_const * (abs(cm) / 100.0)
            alpha = max(0.0, min(1.0, alpha))
            out[i] = alpha * closes[i] + (1.0 - alpha) * prev
        else:
            out[i] = prev

    return out


def supersmoother(
    prices: list[float],
    length: int = 20,
) -> list[float | None]:
    """Ehlers 2-pole SuperSmoother filter (NO high-pass filter, strictly NOT Roofing).

    Per John Ehlers (Cybernetic Analysis for Stocks and Futures, Ch. 13):
      theta = sqrt(2) * pi / length
      a1 = exp(-theta)
      b1 = 2 * a1 * cos(theta)
      c2 = b1
      c3 = - (a1^2)
      c1 = 1 - c2 - c3
      filt[t] = c1 * (price[t] + price[t-1]) / 2 + c2 * filt[t-1] + c3 * filt[t-2]

    Returns float series with warmup None for t < length - 1.
    """
    n = len(prices)
    out: list[float | None] = [None] * n
    if length <= 1 or n < 3:
        return out

    ss_rad = math.sqrt(2.0) * math.pi / length
    a1 = math.exp(-ss_rad)
    b1 = 2.0 * a1 * math.cos(ss_rad)
    c2 = b1
    c3 = -(a1**2)
    c1 = 1.0 - c2 - c3

    filt = [0.0] * n
    for t in range(n):
        if t == 0 or t == 1:
            filt[t] = prices[t]
        else:
            filt[t] = c1 * (prices[t] + prices[t - 1]) / 2.0 + c2 * filt[t - 1] + c3 * filt[t - 2]
        if t >= length - 1:
            out[t] = filt[t]

    return out


def frama(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 16,
    batch: int | None = None,
) -> list[float | None]:
    """Ehlers Fractal Adaptive Moving Average (FRAMA).

    Reference: John Ehlers, "FRAMA - Fractal Adaptive Moving Average",
    Technical Analysis of Stocks & Commodities, Oct 2005 / MESA Software.

    Formula (N even):
      half = length // 2
      For window of length N ending at bar t (from t - length + 1 to t):
        First half [t - length + 1, t - half]:
          HH1 = max(highs), LL1 = min(lows)
          N1 = (HH1 - LL1) / half
        Second half [t - half + 1, t]:
          HH2 = max(highs), LL2 = min(lows)
          N2 = (HH2 - LL2) / half
        Full window [t - length + 1, t]:
          HH3 = max(highs), LL3 = min(lows)
          N3 = (HH3 - LL3) / length

        If N1 + N2 > 0 and N3 > 0:
          D = (log(N1 + N2) - log(N3)) / log(2.0)
        Else:
          D = 1.0
        D = clamp(D, 1.0, 2.0)

        alpha = exp(-4.6 * (D - 1.0))
        alpha = clamp(alpha, 0.01, 1.0)

        frama[t] = alpha * closes[t] + (1 - alpha) * frama[t - 1]
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if length < 2 or length % 2 != 0 or n < length:
        return out

    half = length // 2
    log2 = math.log(2.0)
    prev_frama: float | None = None

    for t in range(n):
        if t < length - 1:
            continue

        w_first_h = highs[t - length + 1 : t - half + 1]
        w_first_l = lows[t - length + 1 : t - half + 1]
        hh1 = max(w_first_h)
        ll1 = min(w_first_l)
        n1 = (hh1 - ll1) / half

        w_second_h = highs[t - half + 1 : t + 1]
        w_second_l = lows[t - half + 1 : t + 1]
        hh2 = max(w_second_h)
        ll2 = min(w_second_l)
        n2 = (hh2 - ll2) / half

        w_full_h = highs[t - length + 1 : t + 1]
        w_full_l = lows[t - length + 1 : t + 1]
        hh3 = max(w_full_h)
        ll3 = min(w_full_l)
        n3 = (hh3 - ll3) / length

        if (n1 + n2) > 0.0 and n3 > 0.0:
            d = (math.log(n1 + n2) - math.log(n3)) / log2
        else:
            d = 1.0

        if d < 1.0:
            d = 1.0
        elif d > 2.0:
            d = 2.0

        alpha = math.exp(-4.6 * (d - 1.0))
        if alpha < 0.01:
            alpha = 0.01
        elif alpha > 1.0:
            alpha = 1.0

        if prev_frama is None:
            curr = closes[t]
        else:
            curr = alpha * closes[t] + (1.0 - alpha) * prev_frama

        prev_frama = curr
        out[t] = curr

    return out


def hma(values: list[float], length: int) -> list[float | None]:
    """Hull Moving Average (Alan Hull / ta.hma).

    Formula:
      HMA(n) = WMA(2 * WMA(close, n/2) - WMA(close, n), round(sqrt(n)))
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    half_len = max(1, length // 2)
    sqrt_len = max(1, int(round(math.sqrt(length))))

    wma_half = wma([float(v) for v in values], half_len)
    wma_full = wma([float(v) for v in values], length)

    raw_diff: list[float | None] = [None] * n
    for i in range(n):
        wh = wma_half[i]
        wf = wma_full[i]
        if wh is not None and wf is not None:
            raw_diff[i] = 2.0 * wh - wf

    hma_series = wma(raw_diff, sqrt_len)
    return hma_series


def mcginley_dynamic(
    values: list[float],
    length: int = 14,
    k: float = 1.0,
) -> list[float | None]:
    """McGinley Dynamic indicator (John R. McGinley).

    Formula (Investopedia standard):
      MD[t] = MD[t-1] + (close[t] - MD[t-1]) / (k * N * (close[t] / MD[t-1])^4)
      with seed MD[0] = close[0], and guard MD[t-1] != 0.
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n == 0:
        return out

    denom_mult = k * length
    prev_md: float | None = None

    for i in range(n):
        c = values[i]
        if prev_md is None:
            prev_md = c
            out[i] = c
            continue

        if prev_md != 0.0 and c > 0.0:
            ratio = c / prev_md
            ratio4 = ratio**4
            denom = denom_mult * ratio4
            if denom == 0.0:
                md_val = c
            else:
                md_val = prev_md + (c - prev_md) / denom
        else:
            md_val = c

        prev_md = md_val
        out[i] = md_val

    return out


def ehlers_super_passband(
    closes: list[float],
    p1: int = 40,
    p2: int = 60,
) -> list[float | None]:
    """Ehlers Super Passband Filter (S&C Jul 2016).

    Formula:
      alpha1 = 5.0 / P1
      alpha2 = 5.0 / P2
      PB = (alpha1 - alpha2) * Close
         + (alpha2 * (1 - alpha1) - alpha1 * (1 - alpha2)) * Close[1]
         + ((1 - alpha1) + (1 - alpha2)) * PB[1]
         - (1 - alpha1) * (1 - alpha2) * PB[2]
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if p1 <= 0 or p2 <= 0 or n < 3:
        return out

    a1 = 5.0 / p1
    a2 = 5.0 / p2

    c0 = a1 - a2
    c1 = a2 * (1.0 - a1) - a1 * (1.0 - a2)
    c2 = (1.0 - a1) + (1.0 - a2)
    c3 = (1.0 - a1) * (1.0 - a2)

    pb1 = 0.0
    pb2 = 0.0

    for i in range(n):
        if i == 0:
            out[i] = 0.0
            pb1 = 0.0
            pb2 = 0.0
            continue
        c = closes[i]
        c_prev = closes[i - 1]
        val = c0 * c + c1 * c_prev + c2 * pb1 - c3 * pb2
        out[i] = val
        pb2 = pb1
        pb1 = val

    return out


def rms(values: list[float | None], length: int = 50) -> list[float | None]:
    """Root Mean Square over `length` bars: sqrt(SMA(x^2, length))."""
    n = len(values)
    sq: list[float | None] = [None] * n
    for i in range(n):
        v = values[i]
        sq[i] = (v * v) if v is not None else None

    sma_sq = _sma_nullable(sq, length)
    out: list[float | None] = [None] * n
    for i in range(n):
        s = sma_sq[i]
        if s is not None and s >= 0.0:
            out[i] = math.sqrt(s)
        elif s is not None:
            out[i] = 0.0
    return out


def rwi_high_low(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    max_lookback: int = 64,
) -> tuple[list[float | None], list[float | None]]:
    """Random Walk Index High and Low (Michael Poulos).

    For each bar t and each i in [2, max_lookback]:
      ATR_i = ATR(highs, lows, closes, i) [or simple TR average over i bars]
      RWI_High(i) = (High[t] - Low[t - i]) / (ATR_i * sqrt(i))
      RWI_Low(i) = (High[t - i] - Low[t]) / (ATR_i * sqrt(i))
    RWI_High = max over i of RWI_High(i)
    RWI_Low = max over i of RWI_Low(i)
    """
    n = len(closes)
    rwi_h: list[float | None] = [None] * n
    rwi_l: list[float | None] = [None] * n
    if n < 3 or max_lookback < 2:
        return rwi_h, rwi_l

    # Precalculate TR for all bars
    tr_vals = true_range(highs, lows, closes)
    # Precalculate cumulative sum of TR for fast SMA calculation: TR_sum(i) = sum(tr[t - i + 1 : t + 1])
    # Note: tr_vals[0] = highs[0] - lows[0]
    cum_tr = [0.0] * (n + 1)
    for i in range(n):
        cum_tr[i + 1] = cum_tr[i] + tr_vals[i]

    # Precalculate sqrt(i)
    sqrt_i = [math.sqrt(i) for i in range(max_lookback + 1)]

    for t in range(2, n):
        max_h = -float("inf")
        max_l = -float("inf")
        curr_high = highs[t]
        curr_low = lows[t]

        limit = min(t, max_lookback)
        for i in range(2, limit + 1):
            # SMA of TR over i bars ending at t
            atr_i = (cum_tr[t + 1] - cum_tr[t + 1 - i]) / i
            denom = atr_i * sqrt_i[i]
            if denom > 0.0:
                h_disp = (curr_high - lows[t - i]) / denom
                l_disp = (highs[t - i] - curr_low) / denom
                if h_disp > max_h:
                    max_h = h_disp
                if l_disp > max_l:
                    max_l = l_disp

        if max_h != -float("inf"):
            rwi_h[t] = max_h
        if max_l != -float("inf"):
            rwi_l[t] = max_l

    return rwi_h, rwi_l


def ehlers_reverse_ema(
    closes: list[float],
    alpha: float = 0.1,
) -> list[float | None]:
    """Ehlers Reverse EMA Wave (TASC Sep 2017).

    Formula (Traders' Tips Sep 2017):
      CC = 1.0 - alpha
      EMA = alpha * Close + CC * EMA[1]
      RE1 = CC * EMA + EMA[1]
      RE2 = (CC^2) * RE1 + RE1[1]
      RE3 = (CC^4) * RE2 + RE2[1]
      RE4 = (CC^8) * RE3 + RE3[1]
      RE5 = (CC^16) * RE4 + RE4[1]
      RE6 = (CC^32) * RE5 + RE5[1]
      RE7 = (CC^64) * RE6 + RE6[1]
      RE8 = (CC^128) * RE7 + RE7[1]
      Wave = EMA - alpha * RE8
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0 or alpha <= 0.0 or alpha >= 1.0:
        return out

    cc = 1.0 - alpha
    cc_pows = [
        cc,            # for RE1
        cc ** 2,       # for RE2
        cc ** 4,       # for RE3
        cc ** 8,       # for RE4
        cc ** 16,      # for RE5
        cc ** 32,      # for RE6
        cc ** 64,      # for RE7
        cc ** 128,     # for RE8
    ]

    ema_val = 0.0
    ema_prev = 0.0
    re = [0.0] * 8
    re_prev = [0.0] * 8

    for i in range(n):
        c = closes[i]
        if i == 0:
            ema_val = c
            ema_prev = c
            # Seed RE cascades
            re[0] = cc * ema_val + ema_prev
            re_prev[0] = re[0]
            for k in range(1, 8):
                re[k] = cc_pows[k] * re[k - 1] + re_prev[k - 1]
                re_prev[k] = re[k]
            out[i] = ema_val - alpha * re[7]
            continue

        ema_val = alpha * c + cc * ema_prev
        re[0] = cc * ema_val + ema_prev
        for k in range(1, 8):
            re[k] = cc_pows[k] * re[k - 1] + re_prev[k - 1]

        out[i] = ema_val - alpha * re[7]

        ema_prev = ema_val
        for k in range(8):
            re_prev[k] = re[k]

    return out


def awesome_oscillator(
    highs: list[float],
    lows: list[float],
    fast_length: int = 5,
    slow_length: int = 34,
) -> list[float | None]:
    """Awesome Oscillator (Bill Williams).
    
    Median price = (high + low) / 2
    AO = SMA(median, fast_length) - SMA(median, slow_length)
    Explicitly uses median price (HL2), not close-SMA.
    """
    n = len(highs)
    out: list[float | None] = [None] * n
    if n == 0 or fast_length <= 0 or slow_length <= 0 or fast_length >= slow_length:
        return out

    medians = [(highs[i] + lows[i]) / 2.0 for i in range(n)]
    fast_sma = sma(medians, fast_length)
    slow_sma = sma(medians, slow_length)

    for i in range(n):
        f = fast_sma[i]
        s = slow_sma[i]
        if f is not None and s is not None:
            out[i] = f - s
    return out


def pretty_good_oscillator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> list[float | None]:
    """Pretty Good Oscillator (Mark Johnson).
    
    PGO = (close - SMA(close, length)) / EMA(TR, length)
    Guard: denominator > 0.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0 or length <= 0:
        return out

    tr_vals = true_range(highs, lows, closes)
    # EMA requires non-None floats; true_range produces floats for all indices >= 0
    tr_clean = [float(v) if v is not None else 0.0 for v in tr_vals]
    den_ema = ema(tr_clean, length)
    sma_close = sma(closes, length)

    for i in range(n):
        s = sma_close[i]
        d = den_ema[i]
        if s is not None and d is not None and d > 0.0:
            out[i] = (closes[i] - s) / d
    return out


def psychological_line(
    closes: list[float],
    length: int = 12,
) -> list[float | None]:
    """Psychological Line (PSY).

    PSY = 100 * SMA(up, length) where up = 1.0 if close[i] > close[i-1] else 0.0.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0 or length <= 0 or n < length:
        return out

    up_vals: list[float] = [0.0] * n
    for i in range(1, n):
        if closes[i] > closes[i - 1]:
            up_vals[i] = 1.0

    # ta.sma(up, length) - note bar 0 has up=0.0
    sma_up = sma(up_vals, length)
    for i in range(n):
        s = sma_up[i]
        if s is not None:
            out[i] = 100.0 * s
    return out


def disparity_index(
    closes: list[float],
    length: int = 20,
) -> list[float | None]:
    """Disparity Index (DI).

    DI = 100 * (close - SMA(close, length)) / SMA(close, length)
    Guard: SMA > 0.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0 or length <= 0 or n < length:
        return out

    ma = sma(closes, length)
    for i in range(n):
        m = ma[i]
        if m is not None and m > 0.0:
            out[i] = 100.0 * (closes[i] - m) / m
    return out


def wavetrend(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    n1: int = 10,
    n2: int = 21,
    n3: int = 4,
) -> tuple[list[float | None], list[float | None]]:
    """WaveTrend Oscillator (LazyBear).

    ap = (high + low + close) / 3.0
    esa = EMA(ap, n1)
    d = EMA(abs(ap - esa), n1)
    ci = (ap - esa) / (0.015 * d)  guard d > 0
    wt1 = EMA(ci, n2)
    wt2 = SMA(wt1, n3)
    """
    n = len(closes)
    wt1_out: list[float | None] = [None] * n
    wt2_out: list[float | None] = [None] * n
    if n == 0 or n1 <= 0 or n2 <= 0 or n3 <= 0:
        return wt1_out, wt2_out

    ap = [(highs[i] + lows[i] + closes[i]) / 3.0 for i in range(n)]
    esa = ema(ap, n1)

    abs_diff: list[float] = [0.0] * n
    for i in range(n):
        e = esa[i]
        if e is not None:
            abs_diff[i] = abs(ap[i] - e)
        else:
            abs_diff[i] = 0.0

    # In TV / LazyBear, d is EMA of abs_diff starting once esa is valid
    # abs_diff before n1-1 is 0.0, so ema(abs_diff, n1) seeds at n1-1 with sum of first n1 items
    d = ema(abs_diff, n1)

    ci: list[float] = [0.0] * n
    for i in range(n):
        e = esa[i]
        di = d[i]
        if e is not None and di is not None and di > 0.0:
            ci[i] = (ap[i] - e) / (0.015 * di)
        else:
            ci[i] = 0.0

    wt1 = ema(ci, n2)
    # wt1 has None for indices < n2-1. For SMA(wt1, n3), we only compute SMA when wt1 items are floats.
    wt1_clean = [float(v) if v is not None else 0.0 for v in wt1]
    wt2 = sma(wt1_clean, n3)

    # Clean outputs: wt1 valid from when ci/ema is valid
    for i in range(n):
        if wt1[i] is not None:
            wt1_out[i] = wt1[i]
        # wt2 requires n3 bars of valid wt1
        if i >= (n1 - 1) + (n2 - 1) + (n3 - 1) and wt2[i] is not None and wt1[i] is not None:
            wt2_out[i] = wt2[i]

    return wt1_out, wt2_out


def relative_momentum_index(
    closes: list[float],
    length: int = 20,
    momentum: int = 5,
) -> list[float | None]:
    """Relative Momentum Index (Altman RMI).

    mom = close - close[momentum]
    u = max(mom, 0.0)
    d = max(-mom, 0.0)
    U = RMA(u, length)
    D = RMA(d, length)
    rmi = 100.0 * U / (U + D)  guard (U + D) > 0
    Hard requirement: momentum >= 3 (m=1 is RSI).
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0 or length <= 0 or momentum <= 0 or n < momentum + length:
        return out

    u_vals: list[float | None] = [None] * n
    d_vals: list[float | None] = [None] * n
    for i in range(momentum, n):
        mom = closes[i] - closes[i - momentum]
        u_vals[i] = max(mom, 0.0)
        d_vals[i] = max(-mom, 0.0)

    # RMA on u and d
    u_rma = rma(u_vals, length)
    d_rma = rma(d_vals, length)

    for i in range(n):
        u_val = u_rma[i]
        d_val = d_rma[i]
        if u_val is not None and d_val is not None:
            den = u_val + d_val
            if den > 0.0:
                out[i] = 100.0 * u_val / den
            else:
                out[i] = 50.0  # neutral if zero displacement
    return out


def acceleration_bands(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 20,
    k: float = 4.0,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """Acceleration Bands (Price Headley).

    rng = (high - low) / (high + low)  guard high + low > 0
    upSrc = high * (1.0 + k * rng)
    dnSrc = low * (1.0 - k * rng)
    upper = SMA(upSrc, length)
    lower = SMA(dnSrc, length)
    mid = SMA(close, length)
    """
    n = len(closes)
    upper_out: list[float | None] = [None] * n
    lower_out: list[float | None] = [None] * n
    mid_out: list[float | None] = [None] * n
    if n == 0 or length <= 0:
        return upper_out, lower_out, mid_out

    up_src: list[float] = [0.0] * n
    dn_src: list[float] = [0.0] * n

    for i in range(n):
        h = highs[i]
        l = lows[i]
        hl_sum = h + l
        if hl_sum > 0.0:
            rng = (h - l) / hl_sum
        else:
            rng = 0.0
        up_src[i] = h * (1.0 + k * rng)
        dn_src[i] = l * (1.0 - k * rng)

    upper_out = sma(up_src, length)
    lower_out = sma(dn_src, length)
    mid_out = sma(closes, length)

    return upper_out, lower_out, mid_out


def trend_intensity_index(
    closes: list[float],
    major: int = 60,
    minor: int = 30,
) -> list[float | None]:
    """Trend Intensity Index (M.H. Pee, TASC Jun 2002).

    Formula:
      ma = ta.sma(close, major)
      for minor bars:
        dev = close - ma
        pos = max(dev, 0)
        neg = max(-dev, 0)
      sdPos = sum(pos, minor)
      sdNeg = sum(neg, minor)
      tii = 100 * sdPos / (sdPos + sdNeg)  guard (sdPos + sdNeg) > 0
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if major <= 0 or minor <= 0 or n < major:
        return out

    ma_vals = sma(closes, major)
    pos_dev: list[float] = [0.0] * n
    neg_dev: list[float] = [0.0] * n

    for i in range(n):
        m = ma_vals[i]
        if m is not None:
            c = closes[i]
            dev = c - m
            pos_dev[i] = max(dev, 0.0)
            neg_dev[i] = max(-dev, 0.0)

    # Rolling sum over minor bars
    pos_sum = 0.0
    neg_sum = 0.0
    for i in range(n):
        if ma_vals[i] is None:
            continue
        pos_sum += pos_dev[i]
        neg_sum += neg_dev[i]
        # We need at least minor bars of valid ma
        # First valid ma is at major - 1
        if i >= (major - 1) + (minor - 1):
            if i > (major - 1) + (minor - 1):
                pos_sum -= pos_dev[i - minor]
                neg_sum -= neg_dev[i - minor]
            tot = pos_sum + neg_sum
            if tot > 0.0:
                out[i] = 100.0 * pos_sum / tot
            else:
                out[i] = 50.0

    return out


def rainbow_oscillator(
    closes: list[float],
    p: int = 2,
    depth: int = 10,
) -> tuple[list[float | None], list[float | None]]:
    """Rainbow Oscillator and Rainbow Bandwidth (Mel Widner, TASC Jul 1997).

    Formula:
      ave1 = SMA(close, p)
      ave2 = SMA(ave1, p)
      ...
      ave10 = SMA(ave9, p)
      aveA = mean(ave1 .. ave10)
      rangeC = highest(close, depth + 1) - lowest(close, depth + 1)
      ro = 100 * (close - aveA) / rangeC
      rb = 100 * (max(ave1..ave10) - min(ave1..ave10)) / rangeC
    """
    n = len(closes)
    ro_out: list[float | None] = [None] * n
    rb_out: list[float | None] = [None] * n
    if p <= 0 or depth <= 0 or n < p:
        return ro_out, rb_out

    # Recursive SMAs
    aves: list[list[float | None]] = []
    curr_series = closes
    for d in range(depth):
        # Filter None values for SMA calculation
        curr_sma: list[float | None] = [None] * n
        # Compute SMA manually or via helper
        window_sum = 0.0
        valid_cnt = 0
        for i in range(n):
            v = curr_series[i]
            if v is None:
                continue
            window_sum += v
            valid_cnt += 1
            if valid_cnt >= p:
                if valid_cnt > p:
                    old_v = curr_series[i - p]
                    assert old_v is not None
                    window_sum -= old_v
                    valid_cnt -= 1
                curr_sma[i] = window_sum / p
        aves.append(curr_sma)
        curr_series = curr_sma  # recursive input

    # For each bar, compute aveA, rangeC, ro, rb
    lookback = depth + 1
    for i in range(n):
        # Check if all depth averages have valid values at bar i
        bar_aves = [aves[d][i] for d in range(depth)]
        if any(a is None for a in bar_aves):
            continue
        valid_aves = [float(a) for a in bar_aves]
        ave_a = sum(valid_aves) / depth
        max_ave = max(valid_aves)
        min_ave = min(valid_aves)

        if i + 1 < lookback:
            continue
        c_window = closes[i - lookback + 1 : i + 1]
        hh = max(c_window)
        ll = min(c_window)
        range_c = hh - ll
        if range_c > 0.0:
            ro_out[i] = 100.0 * (closes[i] - ave_a) / range_c
            rb_out[i] = 100.0 * (max_ave - min_ave) / range_c
        else:
            ro_out[i] = 0.0
            rb_out[i] = 0.0

    return ro_out, rb_out


def dorsey_relative_volatility_index(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    stdev_len: int = 10,
    avg_len: int = 14,
) -> list[float | None]:
    """Dorsey Relative Volatility Index (Donald Dorsey, TASC 1993/1995 refined).

    Refined version uses High and Low stdev:
      sH = stdev(high, stdevLen)
      sL = stdev(low, stdevLen)
      uH = high > high[1] ? sH : 0
      dH = high < high[1] ? sH : 0 (or uH vs sH in Wilder RMA)
      rviH = 100 * rma(uH, avgLen) / rma(sH, avgLen)
      Similarly for Low:
      uL = low > low[1] ? sL : 0
      rviL = 100 * rma(uL, avgLen) / rma(sL, avgLen)
      rvi = (rviH + rviL) / 2.0
    Never label as Relative Vigor Index.
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if stdev_len <= 1 or avg_len <= 0 or n < max(stdev_len, avg_len) + 1:
        return out

    # Rolling population stdev
    def _rolling_stdev(vals: list[float], length: int) -> list[float | None]:
        res: list[float | None] = [None] * n
        if n < length:
            return res
        for i in range(length - 1, n):
            win = vals[i - length + 1 : i + 1]
            mean_v = sum(win) / length
            var_v = sum((x - mean_v) ** 2 for x in win) / length
            res[i] = math.sqrt(var_v)
        return res

    s_h = _rolling_stdev(highs, stdev_len)
    s_l = _rolling_stdev(lows, stdev_len)

    u_h: list[float | None] = [None] * n
    u_l: list[float | None] = [None] * n

    for i in range(1, n):
        sh_val = s_h[i]
        sl_val = s_l[i]
        if sh_val is not None:
            u_h[i] = sh_val if highs[i] > highs[i - 1] else 0.0
        if sl_val is not None:
            u_l[i] = sl_val if lows[i] > lows[i - 1] else 0.0

    # RMA of uH, sH, uL, sL
    rma_uh = rma(u_h, avg_len)
    rma_sh = rma(s_h, avg_len)
    rma_ul = rma(u_l, avg_len)
    rma_sl = rma(s_l, avg_len)

    for i in range(n):
        ruh = rma_uh[i]
        rsh = rma_sh[i]
        rul = rma_ul[i]
        rsl = rma_sl[i]

        if ruh is not None and rsh is not None and rul is not None and rsl is not None:
            rvi_h = min(100.0, max(0.0, (100.0 * ruh / rsh))) if rsh > 0.0 else 50.0
            rvi_l = min(100.0, max(0.0, (100.0 * rul / rsl))) if rsl > 0.0 else 50.0
            out[i] = (rvi_h + rvi_l) / 2.0

    return out


def trend_continuation_factor(
    closes: list[float],
    length: int = 35,
) -> tuple[list[float | None], list[float | None]]:
    """Trend Continuation Factor (M.H. Pee, TASC Mar 2002).

    Formula:
      Change = close - close[1]
      plusChange = max(Change, 0)
      minusChange = max(-Change, 0)
      plusCF = plusChange == 0 ? 0 : plusChange + plusCF[1]
      minusCF = minusChange == 0 ? 0 : minusChange + minusCF[1]
      plusTCF = sum(plusChange - minusCF, length)
      minusTCF = sum(minusChange - plusCF, length)
    """
    n = len(closes)
    plus_tcf_out: list[float | None] = [None] * n
    minus_tcf_out: list[float | None] = [None] * n
    if length <= 0 or n < 2:
        return plus_tcf_out, minus_tcf_out

    plus_diff: list[float] = [0.0] * n
    minus_diff: list[float] = [0.0] * n

    plus_cf = 0.0
    minus_cf = 0.0

    for i in range(1, n):
        chg = closes[i] - closes[i - 1]
        pos_chg = max(chg, 0.0)
        neg_chg = max(-chg, 0.0)

        plus_cf = 0.0 if pos_chg == 0.0 else pos_chg + plus_cf
        minus_cf = 0.0 if neg_chg == 0.0 else neg_chg + minus_cf

        plus_diff[i] = pos_chg - minus_cf
        minus_diff[i] = neg_chg - plus_cf

    # Rolling sum of plus_diff and minus_diff over length
    plus_sum = 0.0
    minus_sum = 0.0
    for i in range(1, n):
        plus_sum += plus_diff[i]
        minus_sum += minus_diff[i]
        if i >= length:
            if i > length:
                plus_sum -= plus_diff[i - length]
                minus_sum -= minus_diff[i - length]
            plus_tcf_out[i] = plus_sum
            minus_tcf_out[i] = minus_sum

    return plus_tcf_out, minus_tcf_out


def dema(
    values: list[float],
    length: int,
) -> list[float | None]:
    """Double Exponential Moving Average (Patrick Mulloy, TASC Jan 1994).

    Formula:
      DEMA = 2 * EMA(values, length) - EMA(EMA(values, length), length)
    """
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out

    e1 = ema(values, length)
    # Filter None for e2 calculation
    # _ema_skip_none starts when e1 is valid
    e2: list[float | None] = [None] * n
    first_valid = -1
    for i in range(n):
        if e1[i] is not None:
            first_valid = i
            break
    if first_valid == -1 or n - first_valid < length:
        return out

    valid_vals = [float(e1[i]) for i in range(first_valid, n)]
    inner_e2 = ema(valid_vals, length)
    for i, val in enumerate(inner_e2):
        e2[first_valid + i] = val

    for i in range(n):
        v1 = e1[i]
        v2 = e2[i]
        if v1 is not None and v2 is not None:
            out[i] = 2.0 * v1 - v2

    return out


# ---------------------------------------------------------------------------
# Stage 11 Indicators: TrendScore, Pee TDI/Direction, Ehlers Leading, GMMA Osc, VQI
# ---------------------------------------------------------------------------


def chande_trendscore(
    closes: list[float],
    start_lag: int = 11,
    width: int = 10,
) -> list[float | None]:
    """Chande TrendScore (Tushar Chande, S&C Sep 1993).

    Formula:
      For i = start_lag .. start_lag + width - 1:
        ts += (close >= close[i] ? +1 : -1)
      Classic (11, 10) produces signed discrete rating in [-10 .. +10].
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    max_lookback = start_lag + width - 1
    if start_lag < 1 or width < 1 or n <= max_lookback:
        return out

    for t in range(max_lookback, n):
        c = closes[t]
        score = 0.0
        for lag in range(start_lag, start_lag + width):
            if c >= closes[t - lag]:
                score += 1.0
            else:
                score -= 1.0
        out[t] = score

    return out


def pee_tdi_direction(
    closes: list[float],
    n_len: int = 20,
) -> tuple[list[float | None], list[float | None]]:
    """Pee Trend Detection Index (TDI) & Direction Indicator (M.H. Pee, S&C Oct 2001).

    Formula:
      mom = close - close[N]
      absMom = abs(mom)
      direction = sum(mom, N)
      av = abs(direction)
      sumAM2 = sum(absMom, 2 * N)
      sumAM1 = sum(absMom, N)
      tdi = av - (sumAM2 - sumAM1)
    """
    n = len(closes)
    dir_out: list[float | None] = [None] * n
    tdi_out: list[float | None] = [None] * n
    if n_len <= 0 or n < 2 * n_len + 1:
        return dir_out, tdi_out

    moms = [0.0] * n
    abs_moms = [0.0] * n
    for t in range(n_len, n):
        m = closes[t] - closes[t - n_len]
        moms[t] = m
        abs_moms[t] = abs(m)

    # Direction = sum of mom over last N bars
    # First bar where N momentum values are valid: t = n_len + n_len - 1 = 2*n_len - 1
    mom_sum = sum(moms[n_len : 2 * n_len])
    dir_out[2 * n_len - 1] = mom_sum
    for t in range(2 * n_len, n):
        mom_sum += moms[t] - moms[t - n_len]
        dir_out[t] = mom_sum

    # TDI needs sum(absMom, 2*N) and sum(absMom, N)
    # First bar where 2*N momentum values are valid: t = n_len + 2*N - 1 = 3*N - 1
    if n >= 3 * n_len:
        sum_am_2n = sum(abs_moms[n_len : 3 * n_len])
        sum_am_1n = sum(abs_moms[2 * n_len : 3 * n_len])
        t_init = 3 * n_len - 1
        d_val = dir_out[t_init]
        if d_val is not None:
            tdi_out[t_init] = abs(d_val) - (sum_am_2n - sum_am_1n)

        for t in range(3 * n_len, n):
            sum_am_2n += abs_moms[t] - abs_moms[t - 2 * n_len]
            sum_am_1n += abs_moms[t] - abs_moms[t - n_len]
            d_val = dir_out[t]
            if d_val is not None:
                tdi_out[t] = abs(d_val) - (sum_am_2n - sum_am_1n)

    return dir_out, tdi_out


def ehlers_leading_indicator(
    highs: list[float],
    lows: list[float],
    a1: float = 0.25,
    a2: float = 0.50,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Leading Indicator: NetLead and EMA dual lines (John Ehlers).

    Formula:
      price = (high + low) / 2
      Lead = 2 * price + (a1 - 2) * price[1] + (1 - a1) * Lead[1]
      NetLead = a2 * Lead + (1 - a2) * NetLead[1]
      EMA = 0.5 * price + 0.5 * EMA[1]
    """
    n = len(highs)
    net_lead_out: list[float | None] = [None] * n
    ema_out: list[float | None] = [None] * n
    if n < 2:
        return net_lead_out, ema_out

    prices = [(highs[i] + lows[i]) / 2.0 for i in range(n)]

    # Initial conditions
    lead_prev = prices[0]
    net_lead_prev = prices[0]
    ema_prev = prices[0]

    for t in range(n):
        p = prices[t]
        if t == 0:
            lead = p
            net_lead = p
            ema_val = p
        else:
            p1 = prices[t - 1]
            lead = 2.0 * p + (a1 - 2.0) * p1 + (1.0 - a1) * lead_prev
            net_lead = a2 * lead + (1.0 - a2) * net_lead_prev
            ema_val = 0.5 * p + 0.5 * ema_prev

        lead_prev = lead
        net_lead_prev = net_lead
        ema_prev = ema_val

        # Warmup period: skip first bar
        if t >= 1:
            net_lead_out[t] = net_lead
            ema_out[t] = ema_val

    return net_lead_out, ema_out


def gmma_oscillator(
    closes: list[float],
    short_lengths: tuple[int, ...] = (3, 5, 8, 10, 12, 15),
    long_lengths: tuple[int, ...] = (30, 35, 40, 45, 50, 60),
) -> list[float | None]:
    """Guppy Multiple Moving Average Oscillator (Daryl Guppy / Leon Wilson).

    Formula:
      s = mean(EMA(close, k) for k in short_lengths)
      l = mean(EMA(close, m) for m in long_lengths)
      gmmaO = 100 * (s - l) / l  (guard l != 0)
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    max_len = max(max(short_lengths), max(long_lengths))
    if n < max_len:
        return out

    short_emas = [ema(closes, k) for k in short_lengths]
    long_emas = [ema(closes, m) for m in long_lengths]

    for t in range(n):
        # Verify all EMAs valid at bar t
        s_vals = [e[t] for e in short_emas]
        l_vals = [e[t] for e in long_emas]
        if any(v is None for v in s_vals) or any(v is None for v in l_vals):
            continue
        s_mean = sum(float(v) for v in s_vals) / len(s_vals)
        l_mean = sum(float(v) for v in l_vals) / len(l_vals)
        if l_mean != 0.0:
            out[t] = 100.0 * (s_mean - l_mean) / l_mean

    return out


def stridsman_vqi(
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
    sma_fast: int = 9,
) -> tuple[list[float | None], list[float | None]]:
    """Stridsman Volatility Quality Index (VQI) Cumulative Sum & Fast SMA (Jack Stridsman, S&C Aug 2002).

    Formula:
      TR = max(high, close[1]) - min(low, close[1])
      HL = high - low
      if TR > 0 and HL > 0:
        vqiRaw = 0.5 * ((close - close[1]) / TR + (close - open) / HL)
        vqiBar = abs(vqiRaw) * 0.5 * ((close - close[1]) + (close - open))
      else:
        vqiBar = 0.0
      vqiSum = cumsum(vqiBar)
      fast = SMA(vqiSum, sma_fast)
    """
    n = len(closes)
    vqi_sum_out: list[float | None] = [None] * n
    fast_out: list[float | None] = [None] * n
    if n < 2 or sma_fast < 1:
        return vqi_sum_out, fast_out

    cum_sum = 0.0
    raw_sums: list[float] = [0.0] * n
    vqi_sum_out[0] = 0.0
    raw_sums[0] = 0.0

    for t in range(1, n):
        c = closes[t]
        c_prev = closes[t - 1]
        o = opens[t]
        h = highs[t]
        l = lows[t]

        tr = max(h, c_prev) - min(l, c_prev)
        hl = h - l

        if tr > 0.0 and hl > 0.0:
            vqi_raw = 0.5 * ((c - c_prev) / tr + (c - o) / hl)
            vqi_bar = abs(vqi_raw) * 0.5 * ((c - c_prev) + (c - o))
        else:
            vqi_bar = 0.0

        cum_sum += vqi_bar
        raw_sums[t] = cum_sum
        vqi_sum_out[t] = cum_sum

    # Calculate SMA of vqi_sum
    sma_vals = sma(raw_sums, sma_fast)
    for t in range(n):
        fast_out[t] = sma_vals[t]

    return vqi_sum_out, fast_out


def _ema_series(series: list[float | None], length: int) -> list[float | None]:
    """Helper to compute EMA on a series that may start with None."""
    n = len(series)
    out: list[float | None] = [None] * n
    if length <= 0:
        return out
    first_valid = -1
    for i in range(n):
        if series[i] is not None:
            first_valid = i
            break
    if first_valid == -1 or n - first_valid < length:
        return out

    valid_vals = [float(series[i]) for i in range(first_valid, n)]
    inner = ema(valid_vals, length)
    for i, v in enumerate(inner):
        out[first_valid + i] = v
    return out


def blau_csi_ergodic(
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
    q: int = 1,
    r: int = 20,
    s: int = 5,
    u: int = 3,
    ul: int = 3,
) -> tuple[list[float | None], list[float | None]]:
    """Blau Candlestick Index (CSI) Ergodic & Signal (William Blau).

    Formula:
      cmtm = close - open[q - 1]
      rng = highest(high, q) - lowest(low, q)
      num = ema(ema(ema(cmtm, r), s), u)
      den = ema(ema(ema(rng, r), s), u)
      csi = 100 * num / den if den != 0 else 0
      sig = ema(csi, ul)
    """
    n = len(closes)
    csi_out: list[float | None] = [None] * n
    sig_out: list[float | None] = [None] * n
    if n < q or r <= 0 or s <= 0 or u <= 0 or ul <= 0:
        return csi_out, sig_out

    cmtm: list[float | None] = [None] * n
    rng: list[float | None] = [None] * n

    for t in range(n):
        if t < q - 1:
            continue
        c = closes[t]
        o_q = opens[t - (q - 1)]
        cmtm[t] = c - o_q
        h_window = highs[t - q + 1 : t + 1]
        l_window = lows[t - q + 1 : t + 1]
        rng[t] = max(h_window) - min(l_window)

    # Triple EMA of cmtm
    num1 = _ema_series(cmtm, r)
    num2 = _ema_series(num1, s)
    num3 = _ema_series(num2, u)

    # Triple EMA of rng
    den1 = _ema_series(rng, r)
    den2 = _ema_series(den1, s)
    den3 = _ema_series(den2, u)

    for t in range(n):
        n_val = num3[t]
        d_val = den3[t]
        if n_val is not None and d_val is not None:
            if d_val != 0.0:
                csi_out[t] = 100.0 * n_val / d_val
            else:
                csi_out[t] = 0.0

    sig_out = _ema_series(csi_out, ul)
    return csi_out, sig_out


def ehlers_edcf(
    highs: list[float],
    lows: list[float],
    length: int = 15,
) -> list[float | None]:
    """Ehlers Distance Coefficient Filter (EDCF) (John Ehlers, S&C V.19:4).

    Nonlinear FIR filter reweighting hl2 by squared price distances:
      price = (high + low) / 2
      For count = 0 .. length - 1:
        coef[count] = sum_{k=1 .. length-1} (price[count] - price[count + k])^2
      filt = sum(coef * price) / sum(coef) (fallback to price if sum(coef) == 0)
    """
    n = len(highs)
    filt_out: list[float | None] = [None] * n
    if n < length or length <= 1:
        return filt_out

    price = [(highs[i] + lows[i]) / 2.0 for i in range(n)]

    for t in range(length - 1, n):
        coefs = [0.0] * length
        # Sub-window of length bars ending at t: index 0 is bar t, index count is bar t - count
        for count in range(length):
            idx_count = t - count
            p_count = price[idx_count]
            dist_sq_sum = 0.0
            for k in range(1, length):
                idx_k = t - ((count + k) % length)
                p_k = price[idx_k]
                diff = p_count - p_k
                dist_sq_sum += diff * diff
            coefs[count] = dist_sq_sum

        sum_coef = sum(coefs)
        if sum_coef != 0.0:
            sum_prod = sum(coefs[count] * price[t - count] for count in range(length))
            filt_out[t] = sum_prod / sum_coef
        else:
            filt_out[t] = price[t]

    return filt_out


def ehlers_ultimate_smoother(
    prices: list[float],
    period: int = 10,
) -> list[float | None]:
    """Ehlers Ultimate Smoother (John Ehlers, TASC Apr 2024 / MESA).

    AllPass - HighPass filter with zero lag in passband:
      a1 = exp(-1.414 * pi / period)
      c2 = 2 * a1 * cos(1.414 * pi / period)
      c3 = -a1 * a1
      c1 = (1 + c2 - c3) / 4
      US[t] = (1 - c1)*Price[t] + (2*c1 - c2)*Price[t-1] - (c1 + c3)*Price[t-2]
              + c2*US[t-1] + c3*US[t-2]
    """
    n = len(prices)
    us_out: list[float | None] = [None] * n
    if n < 3 or period <= 0:
        return us_out

    sqrt2_pi = 1.4142135623730951 * math.pi
    a1 = math.exp(-sqrt2_pi / period)
    c2 = 2.0 * a1 * math.cos(sqrt2_pi / period)
    c3 = -a1 * a1
    c1 = (1.0 + c2 - c3) / 4.0

    # Seed US = Price for first 2 bars
    us_out[0] = prices[0]
    us_out[1] = prices[1]

    for t in range(2, n):
        p0 = prices[t]
        p1 = prices[t - 1]
        p2 = prices[t - 2]
        u1 = us_out[t - 1]
        u2 = us_out[t - 2]
        assert u1 is not None and u2 is not None
        val = (1.0 - c1) * p0 + (2.0 * c1 - c2) * p1 - (c1 + c3) * p2 + c2 * u1 + c3 * u2
        us_out[t] = val

    return us_out


def ehlers_gaussian_filter(
    prices: list[float],
    period: int = 10,
    poles: int = 2,
) -> list[float | None]:
    """Ehlers N-pole Gaussian Filter (John Ehlers, MESA / 'Gaussian and Other Low Lag Filters').

    Formula:
      w = 2 * pi / period
      beta = (1 - cos(w)) / (1.414^(2/poles) - 1)
      alpha = -beta + sqrt(beta^2 + 2*beta)

    2-pole recursion:
      f[t] = alpha^2 * price[t] + 2*(1 - alpha)*f[t-1] - (1 - alpha)^2 * f[t-2]

    4-pole recursion:
      f[t] = alpha^4 * price[t] + 4*(1 - alpha)*f[t-1] - 6*(1 - alpha)^2 * f[t-2]
             + 4*(1 - alpha)^3 * f[t-3] - (1 - alpha)^4 * f[t-4]
    """
    n = len(prices)
    out: list[float | None] = [None] * n
    if n < poles + 1 or period <= 0 or poles not in (2, 4):
        return out

    w = 2.0 * math.pi / period
    denom = (1.4142135623730951 ** (2.0 / poles)) - 1.0
    beta = (1.0 - math.cos(w)) / denom
    alpha = -beta + math.sqrt(beta * beta + 2.0 * beta)

    om_a = 1.0 - alpha

    if poles == 2:
        c0 = alpha * alpha
        c1 = 2.0 * om_a
        c2 = -(om_a ** 2)

        out[0] = prices[0]
        out[1] = prices[1]
        for t in range(2, n):
            f1 = out[t - 1]
            f2 = out[t - 2]
            assert f1 is not None and f2 is not None
            out[t] = c0 * prices[t] + c1 * f1 + c2 * f2

    elif poles == 4:
        c0 = alpha ** 4
        c1 = 4.0 * om_a
        c2 = -6.0 * (om_a ** 2)
        c3 = 4.0 * (om_a ** 3)
        c4 = -(om_a ** 4)

        for i in range(4):
            out[i] = prices[i]
        for t in range(4, n):
            f1 = out[t - 1]
            f2 = out[t - 2]
            f3 = out[t - 3]
            f4 = out[t - 4]
            assert f1 is not None and f2 is not None and f3 is not None and f4 is not None
            out[t] = c0 * prices[t] + c1 * f1 + c2 * f2 + c3 * f3 + c4 * f4

    return out


def swenlin_pmo(
    closes: list[float],
    s1: int = 35,
    s2: int = 20,
    sig_len: int = 10,
) -> tuple[list[float | None], list[float | None]]:
    """DecisionPoint Price Momentum Oscillator (PMO) & Signal (Carl Swenlin).

    Formula:
      roc1 = (close / close[1] - 1.0) * 100.0
      customSmooth(x, L):
        mult = 2.0 / L
        val[t] = prior + (x[t] - prior) * mult
      sm1 = customSmooth(roc1, s1)
      pmo = customSmooth(10.0 * sm1, s2)
      sig = ema(pmo, sig_len)
    """
    n = len(closes)
    pmo_out: list[float | None] = [None] * n
    sig_out: list[float | None] = [None] * n
    if n < 2 or s1 <= 0 or s2 <= 0 or sig_len <= 0:
        return pmo_out, sig_out

    roc1 = [0.0] * n
    for t in range(1, n):
        prev_c = closes[t - 1]
        if prev_c != 0.0:
            roc1[t] = (closes[t] / prev_c - 1.0) * 100.0
        else:
            roc1[t] = 0.0

    # Custom smooth 1
    # First valid bar is t = 1
    mult1 = 2.0 / s1
    sm1 = [0.0] * n
    sm1[1] = roc1[1]
    for t in range(2, n):
        sm1[t] = sm1[t - 1] + (roc1[t] - sm1[t - 1]) * mult1

    # Custom smooth 2 of 10 * sm1
    mult2 = 2.0 / s2
    pmo_raw = [0.0] * n
    pmo_raw[1] = 10.0 * sm1[1]
    for t in range(2, n):
        val = 10.0 * sm1[t]
        pmo_raw[t] = pmo_raw[t - 1] + (val - pmo_raw[t - 1]) * mult2

    for t in range(1, n):
        pmo_out[t] = pmo_raw[t]

    sig_out = _ema_series(pmo_out, sig_len)
    return pmo_out, sig_out


def demark_rei(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 8,
) -> list[float | None]:
    """DeMark Range Expansion Index (TD REI) (Thomas DeMark).

    Formula (DeMark / S&C V.15:8 / Sierra Chart / ProRealCode):
      For bar t >= 2:
        s[t] = (high[t] - high[t-2]) + (low[t] - low[t-2])
        v[t] = 1 if ((high[t-2] >= close[t-7] or high[t-2] >= close[t-8] or
                      high[t] >= close[t-5] or high[t] >= close[t-6]) and
                     (low[t-2] <= close[t-7] or low[t-2] <= close[t-8] or
                      low[t] <= close[t-5] or low[t] <= close[t-6]))
               else 0
        (Note: for t < 8, condition checks are bounded or evaluate false / zero).
        num[t] = sum(v[i] * s[i], length)
        den[t] = sum(abs(high[i] - high[i-2]) + abs(low[i] - low[i-2]), length)
        rei[t] = 100 * num[t] / den[t] if den[t] != 0 else 0
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n < length + 2 or length <= 0:
        return out

    s = [0.0] * n
    v = [0.0] * n
    abs_s = [0.0] * n

    for t in range(2, n):
        h = highs[t]
        l = lows[t]
        h2 = highs[t - 2]
        l2 = lows[t - 2]
        s_val = (h - h2) + (l - l2)
        s[t] = s_val
        abs_s[t] = abs(h - h2) + abs(l - l2)

        # DeMark Basic overlap test
        # Need close[t-5], close[t-6], close[t-7], close[t-8]
        # Condition 1: (H[t-2] >= C[t-7] or H[t-2] >= C[t-8] or H[t] >= C[t-5] or H[t] >= C[t-6])
        # Condition 2: (L[t-2] <= C[t-7] or L[t-2] <= C[t-8] or L[t] <= C[t-5] or L[t] <= C[t-6])
        cond1 = False
        cond2 = False
        if t >= 5:
            cond1 = cond1 or (h >= closes[t - 5])
            cond2 = cond2 or (l <= closes[t - 5])
        if t >= 6:
            cond1 = cond1 or (h >= closes[t - 6])
            cond2 = cond2 or (l <= closes[t - 6])
        if t >= 7:
            cond1 = cond1 or (h2 >= closes[t - 7])
            cond2 = cond2 or (l2 <= closes[t - 7])
        if t >= 8:
            cond1 = cond1 or (h2 >= closes[t - 8])
            cond2 = cond2 or (l2 <= closes[t - 8])

        v[t] = 1.0 if (cond1 and cond2) else 0.0

    vs = [v[i] * s[i] for i in range(n)]

    # Rolling sum of vs and abs_s over length
    # Note: REI requires at least length bars
    first_idx = length + 1  # since s starts at index 2
    if n <= first_idx:
        return out

    sum_vs = sum(vs[2 : 2 + length])
    sum_abs = sum(abs_s[2 : 2 + length])
    out[first_idx] = (100.0 * sum_vs / sum_abs) if sum_abs != 0.0 else 0.0

    for t in range(first_idx + 1, n):
        sum_vs += vs[t] - vs[t - length]
        sum_abs += abs_s[t] - abs_s[t - length]
        out[t] = (100.0 * sum_vs / sum_abs) if sum_abs != 0.0 else 0.0

    return out


def khalil_pzo(
    closes: list[float],
    n_len: int = 14,
) -> list[float | None]:
    """Khalil & Steckler Price Zone Oscillator (PZO).

    Formula (TASC Jun 2011 / thinkorswim / LuxAlgo):
      signed = close > close[1] ? close : close < close[1] ? -close : 0.0
      cp = ema(signed, n_len)
      tc = ema(close, n_len)
      pzo = 100.0 * cp / tc if tc != 0.0 else 0.0
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n < n_len + 1 or n_len <= 0:
        return out

    signed = [0.0] * n
    for t in range(1, n):
        c = closes[t]
        cp = closes[t - 1]
        if c > cp:
            signed[t] = c
        elif c < cp:
            signed[t] = -c
        else:
            signed[t] = 0.0

    cp_series = ema(signed, n_len)
    tc_series = ema(closes, n_len)

    for t in range(n):
        cp_val = cp_series[t]
        tc_val = tc_series[t]
        if cp_val is not None and tc_val is not None:
            out[t] = (100.0 * cp_val / tc_val) if tc_val != 0.0 else 0.0

    return out


def mobius_tmo(
    opens: list[float],
    closes: list[float],
    length: int = 14,
    calc_length: int = 5,
    smooth_length: int = 3,
) -> tuple[list[float | None], list[float | None]]:
    """Mobius True Momentum Oscillator (TMO) (Mobius @ ThinkScript Lounge / useThinkScript).

    Formula:
      For each bar t >= length:
        vote = sum(close[t] > open[t-i] ? 1 : close[t] < open[t-i] ? -1 : 0 for i in 0..length-1)
      ema1 = ema(vote, calc_length)
      main = ema(ema1, smooth_length)
      signal = ema(main, smooth_length)
    """
    n = len(closes)
    main_out: list[float | None] = [None] * n
    sig_out: list[float | None] = [None] * n
    if n < length or length <= 0 or calc_length <= 0 or smooth_length <= 0:
        return main_out, sig_out

    votes = [0.0] * n
    for t in range(length - 1, n):
        v = 0
        c = closes[t]
        for i in range(length):
            op = opens[t - i]
            if c > op:
                v += 1
            elif c < op:
                v -= 1
        votes[t] = float(v)

    # First valid vote is at length - 1
    valid_votes = votes[length - 1 :]
    ema1_valid = ema(valid_votes, calc_length)
    ema1_series: list[float | None] = [None] * n
    for idx, val in enumerate(ema1_valid):
        ema1_series[length - 1 + idx] = val

    main_series = _ema_series(ema1_series, smooth_length)
    sig_series = _ema_series(main_series, smooth_length)

    return main_series, sig_series


def donovan_range_filter(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 20,
    mult: float = 1.618,
    use_hl2: bool = False,
) -> tuple[list[float | None], list[int | None]]:
    """DonovanWall Range Filter (TradingView 'Range Filter [DW]').

    Formula:
      src = hl2 if use_hl2 else close
      diff = abs(src - src[1])
      wper = 2 * period - 1
      av_chg = ema(ema(diff, period), wper)
      rng = av_chg * mult

      Ratchet filt:
        if src - rng > filt[1]:
          filt = src - rng
        elif src + rng < filt[1]:
          filt = src + rng
        else:
          filt = filt[1]

      Direction flip:
        if filt > filt[1]:
          dir = 1
        elif filt < filt[1]:
          dir = -1
        else:
          dir = dir[1]
    """
    n = len(closes)
    filt_out: list[float | None] = [None] * n
    dir_out: list[int | None] = [None] * n
    if n < 2 or period <= 0:
        return filt_out, dir_out

    src = [0.0] * n
    for t in range(n):
        src[t] = (highs[t] + lows[t]) / 2.0 if use_hl2 else closes[t]

    diff = [0.0] * n
    for t in range(1, n):
        diff[t] = abs(src[t] - src[t - 1])

    wper = 2 * period - 1
    ema_diff = ema(diff, period)
    av_chg = _ema_series(ema_diff, wper)

    # Find first valid index of av_chg
    first_valid = -1
    for t in range(n):
        if av_chg[t] is not None:
            first_valid = t
            break

    if first_valid == -1:
        return filt_out, dir_out

    # Initialize at first_valid
    cur_filt = src[first_valid]
    cur_dir = 1
    filt_out[first_valid] = cur_filt
    dir_out[first_valid] = cur_dir

    for t in range(first_valid + 1, n):
        rng_val = float(av_chg[t]) * mult  # av_chg[t] is not None
        s = src[t]

        if s - rng_val > cur_filt:
            cur_filt = s - rng_val
        elif s + rng_val < cur_filt:
            cur_filt = s + rng_val

        # Direction flip
        prev_filt = filt_out[t - 1]
        assert prev_filt is not None
        if cur_filt > prev_filt:
            cur_dir = 1
        elif cur_filt < prev_filt:
            cur_dir = -1

        filt_out[t] = cur_filt
        dir_out[t] = cur_dir

    return filt_out, dir_out


def clv_sma(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    n_len: int = 14,
) -> list[float | None]:
    """Close Location Value (CLV) SMA (Achelis / Investopedia / StockCharts).

    Volume-free close-in-range oscillator.
    Formula:
      rng = high - low
      clv = (2.0 * close - high - low) / rng if rng != 0.0 else 0.0
      clvs = sma(clv, n_len)
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if n < n_len or n_len <= 0:
        return out

    clv = [0.0] * n
    for t in range(n):
        rng = highs[t] - lows[t]
        if rng != 0.0:
            clv[t] = (2.0 * closes[t] - highs[t] - lows[t]) / rng
        else:
            clv[t] = 0.0

    return sma(clv, n_len)


def pee_ttf(
    highs: list[float],
    lows: list[float],
    length: int = 15,
) -> list[float | None]:
    """Pee Trend Trigger Factor (TTF) (M.H. Pee TASC Dec 2004 / Traders' Tips).

    Formula:
      buy = highest(high, L) - lowest(low[L], L)
      sell = highest(high[L], L) - lowest(low, L)
      den = 0.5 * (buy + sell)
      ttf = 100.0 * (buy - sell) / den if den != 0 else 0.0

    Note on indexing:
      high[L] refers to high lagged by L bars.
      highest(high, L) is max over [t-L+1 .. t].
      lowest(low[L], L) is min of low lagged by L, so over [t-2*L+1 .. t-L].
      highest(high[L], L) is max of high lagged by L, so over [t-2*L+1 .. t-L].
      lowest(low, L) is min over [t-L+1 .. t].
      First valid bar is at index 2*L - 1.
    """
    n = len(highs)
    out: list[float | None] = [None] * n
    if length <= 0 or n < 2 * length:
        return out

    for t in range(2 * length - 1, n):
        # Current L-bar window: [t - length + 1 .. t]
        # Lagged L-bar window: [t - 2 * length + 1 .. t - length]
        cur_high = max(highs[t - length + 1 : t + 1])
        cur_low = min(lows[t - length + 1 : t + 1])

        lag_high = max(highs[t - 2 * length + 1 : t - length + 1])
        lag_low = min(lows[t - 2 * length + 1 : t - length + 1])

        buy = cur_high - lag_low
        sell = lag_high - cur_low
        den = 0.5 * (buy + sell)
        if den != 0.0:
            out[t] = 100.0 * (buy - sell) / den
        else:
            out[t] = 0.0

    return out


def hannula_pfe(
    closes: list[float],
    period: int = 10,
    smooth: int = 5,
) -> list[float | None]:
    """Hannula Polarized Fractal Efficiency (PFE) (Hans Hannula TASC 1994).

    Formula:
      For bar t >= period:
        path = sum(sqrt((close[i] - close[i-1])^2 + 1) for i in [t-period+1 .. t])
        straight = sqrt((close[t] - close[t-period])^2 + period^2)
        sign = 1 if close[t] > close[t-period] else -1 if close[t] < close[t-period] else 0
        raw = 100.0 * sign * straight / path if path != 0 else 0.0
      pfe = ema(raw, smooth)
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if period <= 0 or smooth <= 0 or n < period + 1:
        return out

    raw = [0.0] * n
    # Precompute step distances: hypot(close[i] - close[i-1], 1.0)
    step_dist = [0.0] * n
    for i in range(1, n):
        diff = closes[i] - closes[i - 1]
        step_dist[i] = math.sqrt(diff * diff + 1.0)

    for t in range(period, n):
        path = sum(step_dist[t - period + 1 : t + 1])
        net_diff = closes[t] - closes[t - period]
        straight = math.sqrt(net_diff * net_diff + period * period)
        if net_diff > 0:
            sign = 1.0
        elif net_diff < 0:
            sign = -1.0
        else:
            sign = 0.0

        if path != 0.0:
            raw[t] = 100.0 * sign * straight / path
        else:
            raw[t] = 0.0

    # Smooth raw with EMA starting from index period
    raw_valid = raw[period:]
    ema_valid = ema(raw_valid, smooth)
    for i, val in enumerate(ema_valid):
        out[period + i] = val

    return out


def absolute_strength_hist(
    closes: list[float],
    length: int = 9,
    smooth: int = 2,
) -> list[float | None]:
    """Absolute Strength Histogram (ASH) (RSI-method, SMA internals).

    Formula:
      d = close - close[1]
      bulls = 0.5 * (|d| + d)
      bears = 0.5 * (|d| - d)
      avgB = sma(bulls, length)
      avgS = sma(bears, length)
      smB = sma(avgB, smooth)
      smS = sma(avgS, smooth)
      ash = smB - smS
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if length <= 0 or smooth <= 0 or n < length + smooth:
        return out

    bulls = [0.0] * n
    bears = [0.0] * n
    for t in range(1, n):
        d = closes[t] - closes[t - 1]
        abs_d = abs(d)
        bulls[t] = 0.5 * (abs_d + d)
        bears[t] = 0.5 * (abs_d - d)

    # First SMA over length
    avg_b = sma(bulls, length)
    avg_s = sma(bears, length)

    # Valid values of avg_b and avg_s start at length - 1
    # We do a second SMA of length `smooth` over the valid slice of avg_b/avg_s
    first_valid = length - 1
    valid_b = [float(v) for v in avg_b[first_valid:] if v is not None]
    valid_s = [float(v) for v in avg_s[first_valid:] if v is not None]

    sm_b = sma(valid_b, smooth)
    sm_s = sma(valid_s, smooth)

    for i in range(len(sm_b)):
        vb = sm_b[i]
        vs = sm_s[i]
        if vb is not None and vs is not None:
            out[first_valid + i] = vb - vs

    return out


def leibfarth_apz(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 20,
    band_pct: float = 1.4,
) -> tuple[list[float | None], list[float | None], list[float | None], list[float | None]]:
    """Leibfarth Adaptive Price Zone (APZ) (Joe Leibfarth TASC Sep 2006 / Traders' Tips).

    Formula:
      ds = ema(ema(close, period), period)
      dsg = ema(ema(high - low, period), period)
      up = ds + band_pct * dsg
      dn = ds - band_pct * dsg

    Returns:
      (ds, dsg, up, dn)
    """
    n = len(closes)
    ds_out: list[float | None] = [None] * n
    dsg_out: list[float | None] = [None] * n
    up_out: list[float | None] = [None] * n
    dn_out: list[float | None] = [None] * n
    if period <= 0 or n < 2 * period:
        return ds_out, dsg_out, up_out, dn_out

    # Helper for chaining EMA over series with leading Nones
    def _ema_series(series: list[float | None], p: int) -> list[float | None]:
        res: list[float | None] = [None] * len(series)
        valid = [v for v in series if v is not None]
        if len(valid) < p:
            return res
        first_idx = next(i for i, v in enumerate(series) if v is not None)
        ema_valid = ema(valid, p)
        for j, val in enumerate(ema_valid):
            res[first_idx + j] = val
        return res

    ema_close1 = ema(closes, period)
    ds = _ema_series(ema_close1, period)

    ranges = [h - l for h, l in zip(highs, lows)]
    ema_range1 = ema(ranges, period)
    dsg = _ema_series(ema_range1, period)

    for t in range(n):
        ds_val = ds[t]
        dsg_val = dsg[t]
        if ds_val is not None and dsg_val is not None:
            ds_out[t] = ds_val
            dsg_out[t] = dsg_val
            up_out[t] = ds_val + band_pct * dsg_val
            dn_out[t] = ds_val - band_pct * dsg_val

    return ds_out, dsg_out, up_out, dn_out


def nadaraya_rq(
    closes: list[float],
    lookback: int = 8,
    alpha: float = 8.0,
) -> list[float | None]:
    """Causal Nadaraya-Watson Rational Quadratic Kernel estimate (ŷ).

    Formula (causal / non-repainting endpoint filter):
      For bar t >= lookback - 1:
        w_i = (1.0 + (i^2) / (2.0 * alpha * lookback^2))^(-alpha)  for i = 0 .. lookback - 1
        ŷ_t = sum(close[t - i] * w_i) / sum(w_i)
    """
    n = len(closes)
    out: list[float | None] = [None] * n
    if lookback <= 0 or alpha <= 0 or n < lookback:
        return out

    h = float(lookback)
    denom_factor = 2.0 * alpha * h * h
    weights = [
        (1.0 + (i * i) / denom_factor) ** (-alpha)
        for i in range(lookback)
    ]
    sum_w = sum(weights)

    for t in range(lookback - 1, n):
        num = sum(closes[t - i] * weights[i] for i in range(lookback))
        out[t] = num / sum_w if sum_w != 0.0 else closes[t]

    return out


# =============================================================================
# Stage 15: Dual SOL+BNB indicators
# 1. ehlers_spearman: Spearman Rank Correlation of closes over length L vs time rank
# 2. ehlers_uo2025: Ultimate Oscillator (2025) dual-HighPass / RMS
# 3. ehlers_corr_cycle: Correlation Cycle Real (corr with cos) & Imag (corr with -sin) + state
# 4. ehlers_net_myrsi: Noise Elimination Technology (Kendall concordance) on MyRSI
# 5. varadi_dvi: DV Intermediate Oscillator composite percent-rank of magnitude & stretch
# =============================================================================


def ehlers_spearman(
    closes: list[float],
    length: int = 20,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Spearman Rank Correlation (John Ehlers, TASC Jul 2020).

    Computes Spearman rank correlation rho between close prices and time ranks over a sliding window.
    For window closes[t - length + 1 .. t]:
      time_rank: 1 for oldest bar in window (i = 0), length for most recent bar (i = length - 1).
      price_rank: rank of close[t - length + 1 + i] sorted ascending (1 to length, average ranks on ties).
      d_i = time_rank_i - price_rank_i
      rho = 1.0 - 6.0 * sum(d_i^2) / (length * (length^2 - 1))
      sig = 2.0 * rho - 1.0 (or normalized)

    Returns:
      (rho, sig) where rho in [-1, +1], sig in [-1, +1]
    """
    n = len(closes)
    rho_out: list[float | None] = [None] * n
    sig_out: list[float | None] = [None] * n
    if length < 2 or n < length:
        return rho_out, sig_out

    denom = float(length * (length * length - 1))

    for t in range(length - 1, n):
        window = [closes[t - length + 1 + i] for i in range(length)]
        # Rank window ascending: index sorted by value
        sorted_indices = sorted(range(length), key=lambda idx: window[idx])
        # Assign ranks with fractional ties handling
        price_ranks = [0.0] * length
        k = 0
        while k < length:
            j = k
            while j + 1 < length and window[sorted_indices[j + 1]] == window[sorted_indices[k]]:
                j += 1
            # average rank for indices from k to j (ranks are 1-based: k+1 to j+1)
            avg_rank = (k + 1 + j + 1) / 2.0
            for m in range(k, j + 1):
                price_ranks[sorted_indices[m]] = avg_rank
            k = j + 1

        # time_rank for i in 0..length-1 is i + 1
        sum_d_sq = 0.0
        for i in range(length):
            time_rank = float(i + 1)
            d = time_rank - price_ranks[i]
            sum_d_sq += d * d

        rho = 1.0 - (6.0 * sum_d_sq) / denom
        # clamp to [-1, 1] for floating point stability
        rho = max(-1.0, min(1.0, rho))
        sig = 2.0 * rho - 1.0

        rho_out[t] = rho
        sig_out[t] = sig

    return rho_out, sig_out


def ehlers_uo2025(
    src: list[float],
    band_edge: int = 20,
    bandwidth: float = 2.0,
    rms_period: int = 100,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Ultimate Oscillator (2025) (John Ehlers, TASC Apr 2025 / Traders' Tips).

    Difference of two 2-pole HighPass filters normalized by RMS:
      HighPass(src, P):
        a1 = exp(-1.414 * pi / P)
        c2 = 2 * a1 * cos(1.414 * pi / P)
        c3 = -a1^2
        c1 = (1 + c2 - c3) / 4
        hp[t] = c1 * (src[t] - 2 * src[t-1] + src[t-2]) + c2 * hp[t-1] + c3 * hp[t-2]

      HP1 = HP(src, band_edge * bandwidth)
      HP2 = HP(src, band_edge)
      sig = HP1 - HP2
      rms = sqrt(sum(sig^2, rms_period) / rms_period)
      uo = sig / rms if rms != 0 else 0.0

    Returns:
      (uo, sig)
    """
    import math

    n = len(src)
    uo_out: list[float | None] = [None] * n
    sig_out: list[float | None] = [None] * n
    if band_edge <= 1 or bandwidth <= 0 or n < 3:
        return uo_out, sig_out

    def _calc_hp(period: float) -> list[float]:
        hp = [0.0] * n
        if period <= 1.0:
            return hp
        omega = 1.414 * math.pi / period
        a1 = math.exp(-omega)
        c2 = 2.0 * a1 * math.cos(omega)
        c3 = -a1 * a1
        c1 = (1.0 + c2 - c3) / 4.0

        # Bar 0 and 1 initial conditions
        if n > 0:
            hp[0] = 0.0
        if n > 1:
            hp[1] = 0.0

        for t in range(2, n):
            val = c1 * (src[t] - 2.0 * src[t - 1] + src[t - 2]) + c2 * hp[t - 1] + c3 * hp[t - 2]
            hp[t] = val
        return hp

    p1 = float(band_edge) * float(bandwidth)
    p2 = float(band_edge)
    hp1 = _calc_hp(p1)
    hp2 = _calc_hp(p2)

    raw_sig = [hp1[t] - hp2[t] for t in range(n)]

    # Running sum of squares for RMS
    sig_sq = [s * s for s in raw_sig]
    # For t < rms_period - 1, compute partial RMS or None.
    # Standard Ehlers uses running 100-bar sum, start producing after min bars
    min_bars = max(int(p1), rms_period)

    run_sq = 0.0
    for t in range(n):
        run_sq += sig_sq[t]
        if t >= rms_period:
            run_sq -= sig_sq[t - rms_period]

        if t >= 2:
            sig_out[t] = raw_sig[t]

        if t >= min_bars - 1:
            rms_count = min(t + 1, rms_period)
            rms = math.sqrt(run_sq / rms_count) if rms_count > 0 else 0.0
            uo_out[t] = raw_sig[t] / rms if rms > 1e-12 else 0.0

    return uo_out, sig_out


def ehlers_corr_cycle(
    closes: list[float],
    period: int = 20,
    threshold: float = 9.0,
) -> tuple[list[float | None], list[float | None], list[float | None], list[int]]:
    """Ehlers Correlation Cycle (John Ehlers, TASC Jun 2020 / Traders' Tips).

    Correlates price window with Cosine (Real) and -Sine (Imag) basis functions:
      Real = Pearson corr(close[0..period-1], cos(2*pi*i / period))
      Imag = Pearson corr(close[0..period-1], -sin(2*pi*i / period))

    State logic via phase angle:
      Angle = atan2(-Imag, Real) (scaled in degrees 0..360)
      dAngle = Angle[t] - Angle[t-1] (wrapped)
      state = +1 if TrendUp (abs(dAngle) < threshold and Real > 0),
              -1 if TrendDown (abs(dAngle) < threshold and Real < 0),
              0 otherwise (Cycle mode).

    Returns:
      (real, imag, angle, state)
    """
    import math

    n = len(closes)
    real_out: list[float | None] = [None] * n
    imag_out: list[float | None] = [None] * n
    angle_out: list[float | None] = [None] * n
    state_out: list[int] = [0] * n
    if period < 3 or n < period:
        return real_out, imag_out, angle_out, state_out

    # Precalculate basis waveforms over window [0 .. period - 1]
    # Note: in Ehlers correlation cycle, i goes from 0 (oldest) to period - 1 (newest),
    # or i goes from 0 (newest close) to period - 1.
    # In standard Ehlers formulation:
    #   For i = 0 to period - 1:
    #     Y_cos[i] = cos(2 * pi * i / period)
    #     Y_sin[i] = -sin(2 * pi * i / period)
    # Correlated against close[t - i] or close[t - period + 1 + i].
    # Both are valid as long as orientation is consistent.
    # Standard: i=0 is current bar (offset 0), i=period-1 is oldest bar.
    cos_basis = [math.cos(2.0 * math.pi * i / period) for i in range(period)]
    sin_basis = [-math.sin(2.0 * math.pi * i / period) for i in range(period)]

    mean_cos = sum(cos_basis) / period
    mean_sin = sum(sin_basis) / period
    var_cos = sum((c - mean_cos) ** 2 for c in cos_basis)
    var_sin = sum((s - mean_sin) ** 2 for s in sin_basis)
    std_cos = math.sqrt(var_cos) if var_cos > 0 else 1.0
    std_sin = math.sqrt(var_sin) if var_sin > 0 else 1.0

    raw_angles: list[float | None] = [None] * n

    for t in range(period - 1, n):
        # window: close[t - i] for i in 0..period-1
        p_window = [closes[t - i] for i in range(period)]
        mean_p = sum(p_window) / period
        var_p = sum((p - mean_p) ** 2 for p in p_window)
        if var_p <= 1e-14:
            real_out[t] = 0.0
            imag_out[t] = 0.0
            raw_angles[t] = 0.0
            angle_out[t] = 0.0
            continue

        std_p = math.sqrt(var_p)
        cov_cos = sum((p_window[i] - mean_p) * (cos_basis[i] - mean_cos) for i in range(period))
        cov_sin = sum((p_window[i] - mean_p) * (sin_basis[i] - mean_sin) for i in range(period))

        r_val = max(-1.0, min(1.0, cov_cos / (std_p * std_cos)))
        i_val = max(-1.0, min(1.0, cov_sin / (std_p * std_sin)))
        real_out[t] = r_val
        imag_out[t] = i_val

        # Angle in degrees: Ehlers computes Angle = -atan2(Imag, Real) in degrees
        # or atan2(-Imag, Real) * 180 / pi
        ang = math.atan2(-i_val, r_val) * 180.0 / math.pi
        if ang < 0.0:
            ang += 360.0
        raw_angles[t] = ang
        angle_out[t] = ang

    for t in range(period, n):
        a_curr = raw_angles[t]
        a_prev = raw_angles[t - 1]
        r_curr = real_out[t]
        if a_curr is None or a_prev is None or r_curr is None:
            continue

        d_angle = a_curr - a_prev
        # wrap delta to [-180, 180]
        while d_angle > 180.0:
            d_angle -= 360.0
        while d_angle < -180.0:
            d_angle += 360.0

        if abs(d_angle) < threshold:
            state_out[t] = 1 if r_curr > 0 else -1
        else:
            state_out[t] = 0

    return real_out, imag_out, angle_out, state_out


def ehlers_net_myrsi(
    closes: list[float],
    rsi_length: int = 14,
    net_length: int = 14,
) -> tuple[list[float | None], list[float | None]]:
    """Ehlers Noise Elimination Technology (NET) on MyRSI (John Ehlers).

    MyRSI:
      CU = sum of up deltas over rsi_length (max(C - C[1], 0))
      CD = sum of down deltas over rsi_length (max(C[1] - C, 0))
      my_rsi = (CU - CD) / (CU + CD) if (CU + CD) != 0 else 0.0  in [-1, +1]

    NET (Kendall rank concordance of MyRSI vs time slope over net_length):
      Let X[k] = my_rsi[t - net_length + 1 + k] for k in 0 .. net_length - 1
      Time rank Y[k] increases with k (0 to net_length - 1).
      For each pair (i, j) with i < j:
        Y[j] > Y[i] is always positive.
        concordance sign = sign(X[j] - X[i])
      Num = sum_{i < j} sign(X[j] - X[i])
      Pairs = 0.5 * net_length * (net_length - 1)
      net = Num / Pairs in [-1, +1]

    Returns:
      (net, my_rsi)
    """
    n = len(closes)
    net_out: list[float | None] = [None] * n
    my_out: list[float | None] = [None] * n
    if rsi_length < 1 or net_length < 2 or n < rsi_length + net_length:
        return net_out, my_out

    # Compute MyRSI
    up_deltas = [0.0] * n
    dn_deltas = [0.0] * n
    for t in range(1, n):
        d = closes[t] - closes[t - 1]
        if d > 0:
            up_deltas[t] = d
        elif d < 0:
            dn_deltas[t] = -d

    my_rsi: list[float | None] = [None] * n
    run_up = 0.0
    run_dn = 0.0
    for t in range(1, n):
        run_up += up_deltas[t]
        run_dn += dn_deltas[t]
        if t > rsi_length:
            run_up -= up_deltas[t - rsi_length]
            run_dn -= dn_deltas[t - rsi_length]

        if t >= rsi_length:
            denom = run_up + run_dn
            val = (run_up - run_dn) / denom if denom > 1e-12 else 0.0
            my_rsi[t] = val
            my_out[t] = val

    # Kendall concordance NET over sliding window of my_rsi
    pairs = 0.5 * net_length * (net_length - 1)
    min_bars = rsi_length + net_length - 1

    for t in range(min_bars, n):
        window = [my_rsi[t - net_length + 1 + k] for k in range(net_length)]
        if any(w is None for w in window):
            continue

        num = 0.0
        for i in range(net_length):
            xi = window[i]  # type: ignore[assignment]
            for j in range(i + 1, net_length):
                xj = window[j]  # type: ignore[assignment]
                diff = xj - xi
                if diff > 1e-9:
                    num += 1.0
                elif diff < -1e-9:
                    num -= 1.0

        net_val = num / pairs
        net_out[t] = max(-1.0, min(1.0, net_val))

    return net_out, my_out


def varadi_dvi(
    closes: list[float],
    n: int = 168,
    mag_weight: float = 0.8,
    str_weight: float = 0.2,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """Varadi DV Intermediate Oscillator (David Varadi / CSS Analytics / TTR DVI).

    Formulation:
      r = close / SMA(close, 3) - 1.0
      mag = SMA((SMA(r, 5) + SMA(r, 100) / 10.0) / 2.0, 5)

      b = 1.0 if close > close[1] else (-1.0 if close < close[1] else 0.0)
      str = SMA((runSum(b, 10) + runSum(b, 100) / 10.0) / 2.0, 2)

      dvi = mag_weight * PercentRank(mag, n) + str_weight * PercentRank(str, n)
      (PercentRank scaled to [0.0, 1.0], so DVI in [0.0, 1.0], midline 0.5)

    Returns:
      (dvi, mag, str)
    """
    count = len(closes)
    dvi_out: list[float | None] = [None] * count
    mag_out: list[float | None] = [None] * count
    str_out: list[float | None] = [None] * count
    if n < 5 or count < 100 + n:
        return dvi_out, mag_out, str_out

    # 1. r = close / SMA(close, 3) - 1.0
    sma3 = sma(closes, 3)
    r: list[float | None] = [None] * count
    for t in range(count):
        s3 = sma3[t]
        if s3 is not None and s3 > 0:
            r[t] = (closes[t] / s3) - 1.0

    # 2. SMA(r, 5) and SMA(r, 100)
    # Helper to calculate running SMA over a list with leading Nones
    def _run_sma(series: list[float | None], p: int) -> list[float | None]:
        res: list[float | None] = [None] * count
        run_sum = 0.0
        v_count = 0
        for i in range(count):
            val = series[i]
            if val is not None:
                run_sum += val
                v_count += 1
                if i >= p:
                    old = series[i - p]
                    if old is not None:
                        run_sum -= old
                        v_count -= 1
                if v_count == p:
                    res[i] = run_sum / float(p)
        return res

    sma_r5 = _run_sma(r, 5)
    sma_r100 = _run_sma(r, 100)

    # mag_raw = (sma_r5 + sma_r100 / 10.0) / 2.0
    mag_raw: list[float | None] = [None] * count
    for t in range(count):
        s5 = sma_r5[t]
        s100 = sma_r100[t]
        if s5 is not None and s100 is not None:
            mag_raw[t] = (s5 + s100 / 10.0) / 2.0

    # mag = SMA(mag_raw, 5)
    mag = _run_sma(mag_raw, 5)

    # 3. b = 1.0 if close > close[1] else (-1.0 if close < close[1] else 0.0)
    b_series = [0.0] * count
    for t in range(1, count):
        if closes[t] > closes[t - 1]:
            b_series[t] = 1.0
        elif closes[t] < closes[t - 1]:
            b_series[t] = -1.0

    # runSum(b, 10) and runSum(b, 100)
    sum_b10: list[float] = [0.0] * count
    sum_b100: list[float] = [0.0] * count
    r10 = 0.0
    r100 = 0.0
    for t in range(count):
        r10 += b_series[t]
        r100 += b_series[t]
        if t >= 10:
            r10 -= b_series[t - 10]
        if t >= 100:
            r100 -= b_series[t - 100]
        sum_b10[t] = r10
        sum_b100[t] = r100

    str_raw: list[float | None] = [None] * count
    for t in range(count):
        if t >= 99:
            str_raw[t] = (sum_b10[t] + sum_b100[t] / 10.0) / 2.0

    # str = SMA(str_raw, 2)
    str_series = _run_sma(str_raw, 2)

    for t in range(count):
        mag_out[t] = mag[t]
        str_out[t] = str_series[t]

    # Percent rank over window of length n for mag and str
    # PercentRank(series, n): fraction of values in window < current value
    for t in range(count):
        m_curr = mag[t]
        s_curr = str_series[t]
        if m_curr is None or s_curr is None or t < n - 1:
            continue

        # Check that we have n valid values
        m_win = [mag[t - k] for k in range(n)]
        s_win = [str_series[t - k] for k in range(n)]
        if any(x is None for x in m_win) or any(y is None for y in s_win):
            continue

        # Rank in [0, 1]
        m_less = sum(1.0 for x in m_win if x < m_curr)  # type: ignore[operator]
        m_equal = sum(1.0 for x in m_win if x == m_curr)  # type: ignore[operator]
        m_pct = (m_less + 0.5 * (m_equal - 1.0)) / float(n - 1) if n > 1 else 0.5

        s_less = sum(1.0 for y in s_win if y < s_curr)  # type: ignore[operator]
        s_equal = sum(1.0 for y in s_win if y == s_curr)  # type: ignore[operator]
        s_pct = (s_less + 0.5 * (s_equal - 1.0)) / float(n - 1) if n > 1 else 0.5

        val = mag_weight * m_pct + str_weight * s_pct
        dvi_out[t] = max(0.0, min(1.0, val))

    return dvi_out, mag_out, str_out





