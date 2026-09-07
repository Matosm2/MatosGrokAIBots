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
