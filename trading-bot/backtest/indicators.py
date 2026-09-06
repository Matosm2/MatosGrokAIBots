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
