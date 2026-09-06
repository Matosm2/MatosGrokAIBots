"""Pure-Python EMA and RSI (Wilder) matching TradingView/Pine semantics."""

from __future__ import annotations


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

